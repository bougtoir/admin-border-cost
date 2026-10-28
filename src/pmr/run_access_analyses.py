"""Run the frozen Kyoto-Shiga ON/OFF access analyses (PMR_SI).

Functions:
  healthcare_hospital   : MLIT P04-20, P04_001=1 (hospitals)
  healthcare_clinic     : MLIT P04-20, P04_001=2 (general clinics, dental excluded)
  education_elementary  : MLIT P29-21, open public elementary schools
  education_junior_high : MLIT P29-21, open public junior-high schools

Estimand per freeze: C_s(B) = L_s*(Boundary ON) - L_s*(Boundary OFF).
ON  = nearest facility restricted to the same prefecture as the demand unit.
OFF = nearest facility anywhere in the canonical study region (Kyoto+Shiga).
All other settings identical (paired design). Assignment is uncapacitated
nearest-supply: a closed-form deterministic rule (no optimisation solver);
the solver log records that fact plus timing. Distances are geodesic
(WGS84 inverse via pyproj Geod) in km. Population weights = 2020 Census
small-area JINKO (SETAI household counts used in the weight sensitivity).

Outputs land under results/pmr_access/{healthcare,education,cross_function}.
"""
import csv, json, time
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Geod

ROOT = Path(__file__).resolve().parents[2]
DEMAND = ROOT / "data/processed/pmr_demand/smallarea_demand_units.csv"
RESULTS = ROOT / "results/pmr_access"
ADJ = ROOT / "data/processed/adj_smallarea_edges.csv"
MUNI = ROOT / "data/processed/muni_lookup.csv"
GEOD = Geod(ellps="WGS84")

SPEEDS_KMH = {"drive": 40.0, "walk": 4.0}
THRESHOLDS_KM = {
    "healthcare_hospital": [5.0, 10.0, 20.0, 30.0],
    "healthcare_clinic": [1.0, 2.0, 5.0],
    "education_elementary": [1.0, 2.0, 4.0],
    "education_junior_high": [2.0, 4.0, 8.0],
}


def geodesic_km(lon1, lat1, lon2, lat2):
    _, _, m = GEOD.inv(
        np.asarray(lon1), np.asarray(lat1), np.asarray(lon2), np.asarray(lat2))
    return m / 1000.0


def load_supply(path):
    df = pd.read_csv(path)
    return df


def assign(demand, supply, restrict_same_pref):
    """For each demand unit return (nearest facility index, geodesic km)."""
    lon_d = demand["lon"].to_numpy(); lat_d = demand["lat"].to_numpy()
    lon_s = supply["lon"].to_numpy(); lat_s = supply["lat"].to_numpy()
    pref_s = supply["pref"].astype(str).to_numpy()
    pref_d = demand["pref"].astype(str).to_numpy()
    best_idx = np.empty(len(demand), dtype=np.int64)
    best_d = np.full(len(demand), np.inf)
    CH = 400
    for a in range(0, len(demand), CH):
        n = min(CH, len(demand) - a)
        d_km = geodesic_km(
            np.repeat(lon_d[a:a + CH][:n], len(supply)),
            np.repeat(lat_d[a:a + CH][:n], len(supply)),
            np.tile(lon_s, n), np.tile(lat_s, n)).reshape(n, len(supply))
        if restrict_same_pref:
            mask = pref_d[a:a + n, None] == pref_s[None, :]
            d_km = np.where(mask, d_km, np.inf)
        idx = np.argmin(d_km, axis=1)
        best_idx[a:a + n] = idx
        best_d[a:a + n] = d_km[np.arange(n), idx]
    return best_idx, best_d


def wquantile(x, w, q):
    order = np.argsort(x)
    x, w = x[order], w[order]
    cw = np.cumsum(w)
    return float(np.interp(q * cw[-1], cw, x))


def metrics(demand, dist, fid_pref, label, thresholds):
    w = demand["jinko"].to_numpy(dtype=float)
    total = w.sum()
    row = {"function": label}
    for stat, v in [
        ("mean_km", float(np.average(dist, weights=w))),
        ("median_km", wquantile(dist, w, 0.5)),
        ("p90_km", wquantile(dist, w, 0.9)),
        ("p95_km", wquantile(dist, w, 0.95)),
        ("max_km", float(dist.max())),
        ("pop_weighted_km_total", float((dist * w).sum())),
    ]:
        row[stat] = v
    for t in thresholds:
        row[f"pop_share_beyond_{t:g}km"] = float(w[dist > t].sum() / total)
    row["cross_boundary_share"] = float(
        w[fid_pref != demand["pref"].astype(str).to_numpy()].sum() / total)
    border = demand["border_muni"].to_numpy(bool)
    row["mean_km_border_muni"] = float(np.average(dist[border], weights=w[border]))
    row["mean_km_interior"] = float(np.average(dist[~border], weights=w[~border]))
    row["border_minus_interior_km"] = row["mean_km_border_muni"] - row["mean_km_interior"]
    return row


def run_function(name, supply_csv, thresholds):
    t0 = time.time()
    demand = pd.read_csv(DEMAND, dtype={"pref": str, "muni_code": str})
    supply = pd.read_csv(supply_csv)
    if "pref" not in supply.columns:  # P29 files carry prefecture names
        supply["pref"] = supply["prefecture"].map({"Shiga": "25", "Kyoto": "26"}).astype(str)
    else:
        supply["pref"] = supply["pref"].astype(str)
    log = {
        "function": name,
        "method": "uncapacitated nearest-supply assignment (closed-form argmin over geodesic distance); no solver, no seeds",
        "demand_units": int(len(demand)),
        "supply_points": int(len(supply)),
        "demand_pop": int(demand["jinko"].sum()),
        "pairing": "Boundary ON vs OFF; identical demand geography, supply set, distance metric; only same-prefecture restriction differs",
    }
    out = {"assignment": {}, "metrics": [], "log": log}
    results = {}
    for mode, restr in [("ON", True), ("OFF", False)]:
        idx, dist = assign(demand, supply, restr)
        fid_pref = supply["pref"].astype(str).to_numpy()[idx]
        results[mode] = (idx, dist, fid_pref)
        m = metrics(demand, dist, fid_pref, f"{name}_{mode}", thresholds)
        out["metrics"].append(m)
        log[f"{mode}_seconds"] = round(time.time() - t0, 3)
    diff = {"function": f"{name}_ON_minus_OFF"}
    mo, mf = out["metrics"]
    for k in mo:
        if k == "function":
            continue
        diff[k] = mo[k] - mf[k]
    out["metrics"].append(diff)
    # assignment csv (ON and OFF side by side)
    a = demand[["key_code", "pref", "muni_code", "s_name", "city_name",
                "jinko", "setai", "lon", "lat", "border_muni"]].copy()
    for mode in ("ON", "OFF"):
        idx, dist, _ = results[mode]
        a[f"fac_{mode}"] = supply["name"].to_numpy()[idx]
        a[f"fac_{mode}_pref"] = supply["pref"].astype(str).to_numpy()[idx]
        a[f"dist_{mode}_km"] = np.round(dist, 4)
    a["dist_ON_minus_OFF_km"] = np.round(
        a["dist_ON_km"] - a["dist_OFF_km"], 4)
    out["assignment_df"] = a
    out["supply"] = supply
    out["demand"] = demand
    return out


def sensitivity(demand, supply, results, name, thresholds):
    """Frozen sensitivities: travel-time proxy, household weights, and
    excluding border-line facilities (robustness of the cross-flow driver)."""
    rows = []
    w_pop = demand["jinko"].to_numpy(dtype=float)
    w_hh = demand["setai"].to_numpy(dtype=float)
    for mode in ("ON", "OFF"):
        dist = results[mode][1]
        for spd, v in SPEEDS_KMH.items():
            t = dist / v * 60.0
            rows.append({"function": name, "mode": mode, "sensitivity": f"travel_time_{spd}_{v:g}kmh",
                         "metric": "mean_min", "value": float(np.average(t, weights=w_pop))})
        t40 = dist / SPEEDS_KMH["drive"] * 60
        rows.append({"function": name, "mode": mode, "sensitivity": "travel_time_drive_40kmh",
                     "metric": "p90_min", "value": float(wquantile(t40, w_pop, 0.9))})
        rows.append({"function": name, "mode": mode, "sensitivity": "weight_households",
                     "metric": "mean_km", "value": float(np.average(dist, weights=w_hh))})
    # difference rows for time proxy + hh weights
    d_on, d_off = results["ON"][1], results["OFF"][1]
    rows.append({"function": name, "mode": "ON_minus_OFF", "sensitivity": "travel_time_drive_40kmh",
                 "metric": "mean_min", "value": float(np.average((d_on - d_off) / 40 * 60, weights=w_pop))})
    rows.append({"function": name, "mode": "ON_minus_OFF", "sensitivity": "weight_households",
                 "metric": "mean_km", "value": float(np.average(d_on - d_off, weights=w_hh))})
    return rows


def main():
    demand = pd.read_csv(DEMAND, dtype={"pref": str, "muni_code": str})
    # border municipalities: any small-area adjacency edge that crosses pref
    adj = pd.read_csv(ADJ, dtype=str)
    cross = adj[adj["i"].str[:2] != adj["j"].str[:2]]
    border_munis = set(cross["i"].str[:5]) | set(cross["j"].str[:5])
    demand["border_muni"] = demand["muni_code"].isin(border_munis)
    demand.to_csv(DEMAND, index=False)
    print("border municipalities:", len(border_munis),
          "units in them:", int(demand["border_muni"].sum()))

    specs = [
        ("healthcare_hospital", ROOT / "data/processed/pmr_healthcare_access/p04_hospital_kyoto_shiga.csv",
         THRESHOLDS_KM["healthcare_hospital"], "healthcare"),
        ("healthcare_clinic", ROOT / "data/processed/pmr_healthcare_access/p04_clinic_kyoto_shiga.csv",
         THRESHOLDS_KM["healthcare_clinic"], "healthcare"),
        ("education_elementary", ROOT / "data/processed/pmr_education_access/p29_elementary_open_public_kyoto_shiga.csv",
         THRESHOLDS_KM["education_elementary"], "education"),
        ("education_junior_high", ROOT / "data/processed/pmr_education_access/p29_junior_high_open_public_kyoto_shiga.csv",
         THRESHOLDS_KM["education_junior_high"], "education"),
    ]
    all_metrics, all_sens = [], []
    for name, csvp, thr, group in specs:
        res = run_function(name, csvp, thr)
        d = RESULTS / group
        d.mkdir(parents=True, exist_ok=True)
        res["assignment_df"].to_csv(d / f"{name}_assignment.csv", index=False)
        pd.DataFrame(res["metrics"]).to_csv(d / f"{name}_metrics.csv", index=False)
        sens = sensitivity(res["demand"], res["supply"],
                           {"ON": (None, res["assignment_df"]["dist_ON_km"].to_numpy(), None),
                            "OFF": (None, res["assignment_df"]["dist_OFF_km"].to_numpy(), None)},
                           name, thr)
        pd.DataFrame(sens).to_csv(d / f"{name}_sensitivity.csv", index=False)
        (d / f"{name}_solver_log.txt").write_text(json.dumps(res["log"], indent=2))
        all_metrics += res["metrics"]
        all_sens += sens
        print(name, "done")
    xdir = RESULTS / "cross_function"
    xdir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(all_metrics).to_csv(xdir / "cross_function_metrics.csv", index=False)
    pd.DataFrame(all_sens).to_csv(xdir / "cross_function_sensitivity.csv", index=False)


if __name__ == "__main__":
    main()
