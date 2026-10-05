"""Parse 2020 census Table 6-1 (commuting/schooling OD, municipality x municipality)
for usual-residence municipalities in Shiga(25) and Kyoto(26).
Outputs:
  data/processed/od_muni.csv            (origin_muni, dest_muni, commuters_students)
  data/processed/od_region_matrix.csv   (55x55 within-region matrix, symmetric + raw)
  outputs/diagnostics/flows_qc.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/estat_census_od"
OUT = ROOT / "data/processed"
DIAG = ROOT / "outputs/diagnostics"

FILES = {"25": "od_shiga_61.xlsx", "26": "od_kyoto_61.xlsx"}
MUNIS = pd.read_csv(OUT / "muni_lookup.csv")
MUNI_CODES = set(MUNIS.muni_code.astype(str))


def parse(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, header=None)
    dest = df.iloc[7]  # row with "code_name" for each destination column
    dest_map = {}
    for c in range(4, df.shape[1]):
        v = dest.iloc[c]
        if isinstance(v, str) and "_" in v:
            code, name = v.split("_", 1)
            dest_map[c] = (code.strip(), name.strip())
    recs = []
    for r in range(10, len(df)):
        if str(df.iloc[r, 0]) != "0_総数":
            continue
        o = df.iloc[r, 3]
        if not isinstance(o, str) or "_" not in o:
            continue
        ocode = o.split("_", 1)[0].strip()
        for c, (dcode, dname) in dest_map.items():
            v = df.iloc[r, c]
            if v in ("-", np.nan) or pd.isna(v):
                v = 0.0
            recs.append((ocode, o.split("_", 1)[1].strip(), dcode, dname, float(v)))
    return pd.DataFrame(recs, columns=["origin", "origin_name", "dest", "dest_name", "flow"])


def main():
    od = pd.concat([parse(RAW / f) for f in FILES.values()], ignore_index=True)
    # keep only municipality-level codes (5 digits); drop aggregates like 25000/26000/00000
    od = od[od.origin.str.fullmatch(r"\d{5}") & od.dest.str.fullmatch(r"\d{5}")]
    od = od[~od.origin.str.endswith("00")]  # drop 府県/市 total rows (26100_京都市 etc.)
    od = od[~od.dest.str.endswith("00")]
    od.to_csv(OUT / "od_muni.csv", index=False)

    inner = od[od.origin.isin(MUNI_CODES) & od.dest.isin(MUNI_CODES)].copy()
    inner["f_sym"] = 0.0
    p = inner.pivot_table(index="origin", columns="dest", values="flow",
                          aggfunc="sum", fill_value=0.0)
    idx = sorted(set(p.index) | set(p.columns))
    p = p.reindex(index=idx, columns=idx, fill_value=0.0)
    sym = (p.values + p.values.T) / 2.0
    sym_df = pd.DataFrame(sym, index=idx, columns=idx)
    sym_df.to_csv(OUT / "od_region_matrix_sym.csv")
    p.to_csv(OUT / "od_region_matrix_raw.csv")

    ky = [c for c in idx if c.startswith("26")]
    sg = [c for c in idx if c.startswith("25")]
    qc = {
        "n_origin_munis_with_outflows": int(od.origin.nunique()),
        "n_od_pairs_total": len(od),
        "n_within_region_pairs": len(inner),
        "total_flow_within_region": float(inner.flow.sum()),
        "cross_pref_flow_Kyoto_to_Shiga": float(inner[(inner.origin.isin(ky)) & (inner.dest.isin(sg))].flow.sum()),
        "cross_pref_flow_Shiga_to_Kyoto": float(inner[(inner.origin.isin(sg)) & (inner.dest.isin(ky))].flow.sum()),
        "flow_to_outside_region": float(od[~od.dest.isin(MUNI_CODES)].flow.sum()),
        "top_cross_pref_pairs": inner[((inner.origin.isin(ky)) & (inner.dest.isin(sg))) |
                                      ((inner.origin.isin(sg)) & (inner.dest.isin(ky)))]
                                .sort_values("flow", ascending=False).head(10)
                                .to_dict("records"),
    }
    DIAG.mkdir(parents=True, exist_ok=True)
    (DIAG / "flows_qc.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2))
    print(json.dumps(qc, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
