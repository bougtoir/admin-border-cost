"""IPSS 2023 municipality projections -> unit-level population scenarios.
Primary scenario S1: proportional downscaling (unit pop_t = pop_2020 * muni growth).
Scenario S2 (sensitivity): intra-municipal drift toward the municipal
population-weighted centroid by a linear +/-10% factor (documented, arbitrary
magnitude for stress-testing only; not a forecast).
Outputs:
  data/processed/muni_projections.csv    (muni_code, year, pop_ipss, growth_factor)
  data/processed/unit_projections.parquet (unit_id, year, scenario, pop)
  outputs/diagnostics/projections_qc.json
"""
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/processed"
DIAG = ROOT / "outputs/diagnostics"
YEARS = [2025, 2030, 2035, 2040, 2045, 2050]


def main():
    raw = pd.read_excel(ROOT / "data/raw/ipss/ipss_kekkahyo1.xlsx", header=None)
    df = raw.iloc[5:].copy()  # data rows start at index 5
    df.columns = ["code", "shikibetsu", "pref", "muni_name"] + \
                 [f"p{y}" for y in [2020] + YEARS] + \
                 [f"idx{y}" for y in [2020] + YEARS]
    df = df[df.pref.isin(["京都府", "滋賀県"])].copy()
    # wards (0), cities (2), towns/villages (3); exclude designated-city total rows
    # (shikibetsu=1, e.g. 26100 京都市) since their wards are separate units
    df = df[df.shikibetsu.isin([0, 2, 3])].copy()
    df["muni_code"] = df["code"].astype(int).astype(str)
    keep = ["muni_code", "pref", "muni_name"] + [f"p{y}" for y in [2020] + YEARS]
    df = df[keep].melt(id_vars=["muni_code", "pref", "muni_name"],
                       value_vars=[f"p{y}" for y in [2020] + YEARS],
                       var_name="year", value_name="pop_ipss")
    df["year"] = df["year"].str.replace("p", "").astype(int)
    base = df[df.year == 2020].set_index("muni_code")["pop_ipss"]
    df["growth"] = df["pop_ipss"] / df["muni_code"].map(base)
    df.to_csv(OUT / "muni_projections.csv", index=False)

    g = gpd.read_file(OUT / "units_smallarea.gpkg", layer="units")
    grow = df.set_index(["muni_code", "year"])["growth"]
    rows = []
    # S1 proportional
    up = g[["unit_id", "muni_code", "pop"]].copy()
    for y in YEARS:
        for scen in ["S1", "S2"]:
            u = up.copy()
            u["g"] = u.muni_code.map(grow.xs(y, level="year"))
            if scen == "S2":
                # drift factor: units nearer the muni population-weighted centroid
                # get up to +10%, farther units down to -10% (linear in rank)
                parts = []
                for mc, sub in g.groupby("muni_code"):
                    cen = sub.geometry.representative_point()
                    cw = np.average([p.x for p in cen], weights=sub["pop"])
                    cs = np.average([p.y for p in cen], weights=sub["pop"])
                    d = np.hypot(cen.x - cw, cen.y - cs)
                    rank = pd.Series(d, index=sub.index).rank(pct=True)
                    parts.append(1.0 + 0.10 * (0.5 - rank))  # nearer -> higher
                drift = pd.concat(parts)
                u["g"] = u["g"] * u.index.map(drift)
            u["year"] = y
            u["scenario"] = scen
            u["pop_t"] = u["pop"] * u["g"]
            rows.append(u[["unit_id", "year", "scenario", "pop_t"]])
    upj = pd.concat(rows, ignore_index=True)
    upj.to_parquet(OUT / "unit_projections.parquet", index=False)

    qc = {
        "munis_with_projection": int(df.muni_code.nunique()),
        "missing_units": int(up[~up.muni_code.isin(set(df.muni_code))].unit_id.nunique()),
        "region_pop_by_year_S1": upj[upj.scenario == "S1"].groupby("year").pop_t.sum().to_dict(),
        "ipss_region_pop_by_year": df.groupby("year").pop_ipss.sum().to_dict(),
    }
    # S1 should reproduce IPSS totals per year (muni total preserved)
    check = {y: abs(qc["region_pop_by_year_S1"][y] - qc["ipss_region_pop_by_year"][y])
             for y in YEARS}
    qc["max_abs_error_S1_vs_IPSS"] = max(check.values())
    (DIAG / "projections_qc.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2))
    print(json.dumps(qc, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
