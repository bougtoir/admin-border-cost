"""Evaluate any unit->district assignment on the full metric battery.
Works on either geography level (units table + queen adjacency edges)."""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
OUT = ROOT / "data/processed"
DISTRICTS = list(CFG["districts"]["definition"].keys())
K = CFG["districts"]["K"]


def district_pops(assign: np.ndarray, pop: np.ndarray, k=K) -> np.ndarray:
    return np.bincount(assign, weights=pop, minlength=k)


def pop_metrics(assign, pop, k=K):
    p = district_pops(assign, pop, k)
    pbar = pop.sum() / k
    dev = np.abs(p / pbar - 1)
    return {
        "district_pops": p.tolist(),
        "max_min_ratio": float(p.max() / max(p.min(), 1e-9)),
        "max_rel_dev": float(dev.max()),
        "mean_abs_dev": float(np.abs(p - pbar).mean() / pbar),
        "rms_dev": float(np.sqrt(((p / pbar - 1) ** 2).mean())),
    }


def contiguity_violations(assign, edges: pd.DataFrame) -> list:
    """Return list of dicts: {district, n_components} for districts with >1 component."""
    adj = {}
    for i, j in edges[["i", "j"]].itertuples(index=False):
        adj.setdefault(int(i), []).append(int(j))
        adj.setdefault(int(j), []).append(int(i))
    viol = []
    for d in range(assign.max() + 1):
        nodes = np.where(assign == d)[0]
        if len(nodes) <= 1:
            continue
        nset = set(nodes.tolist())
        seen = set()
        comps = 0
        for s in nodes:
            if s in seen:
                continue
            comps += 1
            stack = [int(s)]
            seen.add(int(s))
            while stack:
                u = stack.pop()
                for v in adj.get(u, []):
                    if v in nset and v not in seen:
                        seen.add(v)
                        stack.append(v)
        if comps > 1:
            viol.append({"district": DISTRICTS[d], "n_components": comps})
    return viol


def compactness(assign, g: gpd.GeoDataFrame) -> dict:
    """Per-district Polsby-Popper + shared cut length."""
    dissolved = g.copy()
    dissolved["d"] = assign
    dis = dissolved.dissolve(by="d")
    pp = []
    perim = []
    area = []
    for i in range(K):
        geom = dis.loc[i].geometry
        a = geom.area
        p = geom.length
        pp.append(4 * np.pi * a / (p * p) if p > 0 else np.nan)
        perim.append(p)
        area.append(a)
    return {
        "polsby_popper": pp,
        "polsby_popper_mean": float(np.nanmean(pp)),
        "polsby_popper_min": float(np.nanmin(pp)),
        "district_perimeter_m": perim,
        "district_area_km2": [a / 1e6 for a in area],
        "total_boundary_m": float(np.sum(perim)),
    }


def split_metrics(assign, g: gpd.GeoDataFrame) -> dict:
    df = g[["muni_code", "muni_name", "pop"]].copy()
    df["d"] = assign
    grp = df.groupby(["muni_code", "muni_name", "d"]).pop.sum().reset_index()
    counts = grp.groupby(["muni_code", "muni_name"]).size()
    split_munis = counts[counts > 1]
    split_pop = (grp.merge(split_munis.reset_index()[["muni_code"]])
                 .groupby("muni_code").pop.min())  # pop in smaller fragment
    return {
        "n_split_munis": len(split_munis),
        "split_munis": split_munis.index.get_level_values(1).tolist(),
        "split_pop_min_fragment": float(split_pop.sum()) if len(split_pop) else 0.0,
    }


def flow_metrics(assign, g: gpd.GeoDataFrame) -> dict:
    """Severed commuting/schooling flow via municipal-share closed form:
    retained share for pair (m,n) = Σ_d share_{m,d}·share_{n,d}."""
    muni_pop = g.groupby("muni_code")["pop"].sum()
    df = g[["muni_code", "pop"]].copy()
    df["d"] = assign
    share = df.groupby(["muni_code", "d"]).pop.sum().div(
        muni_pop, level="muni_code").unstack(fill_value=0.0)
    sym = pd.read_csv(OUT / "od_region_matrix_sym.csv", index_col=0)
    sym.index = sym.index.astype(str)
    sym.columns = sym.columns.astype(str)
    codes = [c for c in sym.index if c in share.index]
    S = share.loc[codes].values          # m x K
    F = sym.loc[codes, codes].values     # m x m
    retain = S @ S.T                     # m x m
    severed = F * (1 - retain)
    total = F.sum() / 2  # off-diagonal only double counted; diag is internal
    sev = (np.triu(severed, 1)).sum()
    cross_pref_codes = [c for c in codes]
    ky = [c for c in codes if c.startswith("26")]
    sg = [c for c in codes if c.startswith("25")]
    i_k = [codes.index(c) for c in ky]
    i_s = [codes.index(c) for c in sg]
    cross_total = F[np.ix_(i_k, i_s)].sum()
    cross_severed = severed[np.ix_(i_k, i_s)].sum()
    return {
        "severed_flow_total": float(sev),
        "severed_fraction": float(sev / max(total, 1e-9)),
        "total_od_flow_within_region": float(total),
        "cross_pref_flow": float(cross_total),
        "cross_pref_flow_severed": float(cross_severed),
        "cross_pref_flow_retained": float(cross_total - cross_severed),
        "within_district_retention": float(total - sev),
    }


def future_metrics(assign, g, years=None) -> dict:
    years = years or CFG["robustness"]["projection_years"]
    out = {"S1": {}, "S2": {}}
    if str(g.unit_id.iloc[0]).isdigit() and len(str(g.unit_id.iloc[0])) == 5:
        # Level A: municipal units -> municipal growth factors directly
        mp = pd.read_csv(OUT / "muni_projections.csv")
        pop = g["pop"].to_numpy(float)
        for scen in ["S1"]:
            for y in years:
                gy = mp[mp.year == y].set_index("muni_code")["growth"]
                py = g.muni_code.astype(int).map(gy).to_numpy() * pop
                p = np.bincount(assign, weights=py, minlength=K)
                pb = p.sum() / K
                out[scen][str(y)] = {"max_rel_dev": float(np.abs(p / pb - 1).max()),
                                     "district_pops": p.tolist()}
        out["S2"] = out["S1"]  # no intra-muni drift at municipal granularity
        return out
    up = pd.read_parquet(OUT / "unit_projections.parquet")
    pos = {u: i for i, u in enumerate(g.unit_id)}
    for scen in ["S1", "S2"]:
        for y in years:
            u = up[(up.year == y) & (up.scenario == scen)]
            idx = np.array([pos[x] for x in u.unit_id])
            a = assign[idx]
            p = np.bincount(a, weights=u.pop_t.values, minlength=K)
            pbar = p.sum() / K
            out[scen][str(y)] = {
                "max_rel_dev": float(np.abs(p / pbar - 1).max()),
                "district_pops": p.tolist(),
            }
    return out


def durability(assign, g, tau=None) -> dict:
    """Earliest year each scenario exceeds tau."""
    tau = tau if tau is not None else CFG["robustness"]["durability_threshold_tau"]
    fm = future_metrics(assign, g)
    out = {}
    for scen, ys in fm.items():
        d_ = "beyond 2050"
        for y in sorted(ys):
            if ys[y]["max_rel_dev"] > tau:
                d_ = int(y)
                break
        out[scen] = d_
    return out


def evaluate(assign, g, edges, label="") -> dict:
    res = {"label": label}
    res.update(pop_metrics(assign, g["pop"].values))
    res["contiguity_violations"] = contiguity_violations(assign, edges)
    res["contiguous"] = len(res["contiguity_violations"]) == 0
    res.update(compactness(assign, g))
    res.update(split_metrics(assign, g))
    res.update(flow_metrics(assign, g))
    res["future"] = future_metrics(assign, g)
    res["durability"] = durability(assign, g)
    return res
