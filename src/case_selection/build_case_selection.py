"""Case-selection comparison (frozen protocol: docs/CASE_SELECTION_ANALYSIS_FREEZE.md).

Computes prefecture-level 2020 census commuting/schooling flows for all
prefectures adjacent to Kyoto-fu (26) or Shiga-ken (25), plus Wakayama
and the Kinki-internal reference pairs. No ranking is computed here that
is not in the frozen metric list.

Outputs:
  data/processed/case_pref_flows.csv
  outputs/tables/case_selection_comparison_full.csv
  outputs/tables/municipal_external_destinations.csv
  outputs/tables/case_pref_population.csv
  outputs/diagnostics/case_selection_qc.json
"""
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_OD = ROOT / "data/raw/estat_census_od"
RAW_GIS = ROOT / "data/raw/estat_gis_boundary"
OUT_P = ROOT / "data/processed"
OUT_T = ROOT / "outputs/tables"
DIAG = ROOT / "outputs/diagnostics"

OD_FILES = {
    "18": "od_fukui_61.xlsx", "21": "od_gifu_61.xlsx", "24": "od_mie_61.xlsx",
    "25": "od_shiga_61.xlsx", "26": "od_kyoto_61.xlsx", "27": "od_osaka_61.xlsx",
    "28": "od_hyogo_61.xlsx", "29": "od_nara_61.xlsx", "30": "od_wakayama_61.xlsx",
}
PREF_NAMES = {
    "18": "Fukui", "21": "Gifu", "24": "Mie", "25": "Shiga", "26": "Kyoto",
    "27": "Osaka", "28": "Hyogo", "29": "Nara", "30": "Wakayama",
}
# complete land-border sets within the comparator prefectures
# (Kyoto has five prefectural borders, not six: no Kyoto–Mie adjacency)
KYOTO_PAIRS = [("26", "25"), ("26", "27"), ("26", "28"), ("26", "29"), ("26", "18")]
SHIGA_PAIRS = [("25", "26"), ("25", "24"), ("25", "21"), ("25", "18")]
KINKI_REF_PAIRS = [("27", "28"), ("27", "29"), ("27", "30"), ("29", "30"),
                   ("29", "24"), ("21", "24"), ("21", "18")]


def parse_od(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, header=None)
    dest = df.iloc[7]
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


def load_od_all() -> pd.DataFrame:
    parts = []
    for pf, fname in OD_FILES.items():  # noqa: PERF102 (pf documents file origin)
        d = parse_od(RAW_OD / fname)
        # keep real municipality rows (5-digit), drop aggregate rows:
        # prefecture/designated-city totals end in "00"; the remaining
        # designated-city totals not caught by that rule are explicit.
        d = d[d.origin.str.fullmatch(r"\d{5}") & d.dest.str.fullmatch(r"\d{5}")]
        d = d[~d.origin.str.endswith("00") & ~d.dest.str.endswith("00")]
        CITY_TOTALS = {"14130", "14150", "22130", "27140", "40130"}
        d = d[~d.origin.isin(CITY_TOTALS) & ~d.dest.isin(CITY_TOTALS)]
        d["origin_pref"] = d.origin.str[:2]
        d["dest_pref"] = d.dest.str[:2]
        parts.append(d)
    return pd.concat(parts, ignore_index=True)


def pref_populations() -> pd.DataFrame:
    """2020 census population per prefecture from r2ka JINKO (same vintage)."""
    import geopandas as gpd

    rows = []
    for pf in sorted(PREF_NAMES):
        z = next(RAW_GIS.glob(f"r2ka{pf}*.zip"))
        with zipfile.ZipFile(z) as zz:
            shp = next(n for n in zz.namelist() if n.lower().endswith(".shp"))
        gdf = gpd.read_file(f"zip://{z}!{shp}", columns=["JINKO"])
        rows.append({"pref": pf, "pref_name": PREF_NAMES[pf],
                     "pop_2020": int(gdf["JINKO"].fillna(0).sum())})
    return pd.DataFrame(rows)


def main():
    od = load_od_all()
    pop = pref_populations()
    pop.to_csv(OUT_T / "case_pref_population.csv", index=False)
    pset = dict(zip(pop.pref, pop.pop_2020))

    # directional prefecture-level flows
    pf = (od.groupby(["origin_pref", "dest_pref"], as_index=False)
            .flow.sum()
            .rename(columns={"flow": "F"}))
    totals = (od.groupby("origin_pref", as_index=False).flow.sum()
                .rename(columns={"flow": "T"}))
    # dest codes 99998/99999 = "destination unknown / abroad": not a
    # prefectural destination -> excluded from external flows and argmax
    od = od.assign(unknown_dest=od.dest.str.startswith("99"))
    ext = (od[(od.origin_pref != od.dest_pref) & (~od.unknown_dest)]
           .groupby("origin_pref", as_index=False).flow.sum()
           .rename(columns={"flow": "E"}))
    pf = pf.merge(totals, on="origin_pref").merge(ext, on="origin_pref")
    pf.to_csv(OUT_P / "case_pref_flows.csv", index=False)
    F = pf.set_index(["origin_pref", "dest_pref"]).F.to_dict()

    pairs, seen = [], set()
    for a, b in KYOTO_PAIRS + SHIGA_PAIRS + KINKI_REF_PAIRS:
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        f_ab, f_ba = F.get((a, b), 0.0), F.get((b, a), 0.0)
        T = totals.set_index("origin_pref")["T"].to_dict()
        E = ext.set_index("origin_pref").E.to_dict()
        pairs.append({
            "pref_i": a, "pref_i_name": PREF_NAMES[a],
            "pref_j": b, "pref_j_name": PREF_NAMES[b],
            "F_i_to_j": f_ab, "F_j_to_i": f_ba,
            "F_bidirectional": f_ab + f_ba,
            "T_i": T[a], "T_j": T[b],
            "E_i": E[a], "E_j": E[b],
            "R_i_to_j": f_ab / T[a], "R_j_to_i": f_ba / T[b],
            "R_ext_i_to_j": f_ab / E[a] if E[a] else np.nan,
            "R_ext_j_to_i": f_ba / E[b] if E[b] else np.nan,
            "P_i": pset[a], "P_j": pset[b],
            "S_bidir_over_Psum": (f_ab + f_ba) / (pset[a] + pset[b]),
            "S2_bidir_over_sqrtPiPj_exploratory":
                (f_ab + f_ba) / np.sqrt(pset[a] * pset[b]),
        })
    comp = pd.DataFrame(pairs)
    comp.to_csv(OUT_T / "case_selection_comparison_full.csv", index=False)

    # destination-prefecture shares for each origin (used for asymmetry)
    shares = pf.assign(share_of_T=pf.F / pf["T"],
                       share_of_E=np.where((pf.dest_pref != pf.origin_pref)
                                           & (pf.dest_pref != "99"),
                                           pf.F / pf["E"], np.nan))
    shares.to_csv(OUT_T / "destination_pref_shares.csv", index=False)

    # municipal: largest external prefectural destination per municipality
    od2 = od[(od.dest_pref != od.origin_pref) & (~od.unknown_dest)].copy()
    muni = (od2.groupby(["origin_pref", "origin", "origin_name", "dest_pref"], as_index=False)
               .flow.sum())
    idx = muni.groupby(["origin_pref", "origin"]).flow.idxmax()
    top = muni.loc[idx].rename(columns={
        "dest_pref": "largest_ext_dest_pref", "flow": "largest_ext_dest_flow"})
    tot_ext = (od2.groupby(["origin_pref", "origin"], as_index=False).flow.sum()
                 .rename(columns={"flow": "total_ext_flow"}))
    top = top.merge(tot_ext, on=["origin_pref", "origin"])
    top["share_ext_to_top_pref"] = top.largest_ext_dest_flow / top.total_ext_flow
    top.to_csv(OUT_T / "municipal_external_destinations.csv", index=False)

    qc = {
        "n_od_pairs_all_prefs": int(len(od)),
        "pairs_reported": int(len(comp)),
        "kyoto_shiga": comp[(comp.pref_i == "26") & (comp.pref_j == "25")].to_dict("records"),
        "kyoto_pairs_rank_by_S": comp[comp.pref_i == "26"].sort_values(
            "S_bidir_over_Psum", ascending=False)[["pref_j_name", "S_bidir_over_Psum"]].to_dict("records"),
        "shiga_top_dest_share": shares[(shares.origin_pref == "25") & (shares.dest_pref == "26")]
            [["share_of_T", "share_of_E"]].to_dict("records"),
        "kyoto_top_ext": top[top.origin_pref == "26"].largest_ext_dest_pref.value_counts().to_dict(),
        "shiga_top_ext": top[top.origin_pref == "25"].largest_ext_dest_pref.value_counts().to_dict(),
    }
    DIAG.mkdir(parents=True, exist_ok=True)
    (DIAG / "case_selection_qc.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2))
    print(json.dumps(qc, ensure_ascii=False, indent=2))

    _report_tables_figure_values(comp, shares, top)


def _row(comp, a, b):
    r = comp[(comp.pref_i == a) & (comp.pref_j == b)]
    return r.iloc[0] if len(r) else None


def _report_tables_figure_values(comp, shares, top):
    """T7 table, F8 figure, and cs_* manuscript values (PG retarget)."""
    # ---- T7: compact comparison table -------------------------------
    t7 = comp.assign(
        pair=comp.pref_i_name + "–" + comp.pref_j_name,
        R_ij_pct=(comp.R_i_to_j * 100).round(2),
        R_ji_pct=(comp.R_j_to_i * 100).round(2),
        S_pct=(comp.S_bidir_over_Psum * 100).round(3),
    )[["pair", "F_i_to_j", "F_j_to_i", "F_bidirectional",
       "R_ij_pct", "R_ji_pct", "S_pct"]]
    t7.columns = ["pair", "flow_i_to_j", "flow_j_to_i", "flow_bidirectional",
                  "R_i_to_j_pct", "R_j_to_i_pct", "S_pct"]
    t7.to_csv(OUT_T / "T7_case_selection.csv", index=False)

    # ---- F8: case-selection figure ----------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ky = comp[comp.pref_i == "26"].sort_values("F_bidirectional", ascending=False)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
    labels = ky.pref_j_name.tolist()
    x = np.arange(len(labels))
    ax[0].bar(x, ky.F_bidirectional, color="#4477aa", label="bidirectional flow")
    ax[0].set_xticks(x, labels, rotation=30, ha="right")
    ax[0].set_ylabel("daily trips (bidirectional)")
    ax2 = ax[0].twinx()
    ax2.plot(x, ky.S_bidir_over_Psum * 100, "o-", color="#cc3311",
             label="S = F_bidir/(P_i+P_j)  (%)")
    ax2.set_ylabel("normalized intensity S (%)", color="#cc3311")
    ax2.tick_params(axis="y", labelcolor="#cc3311")
    ax[0].set_title("Kyoto's five borders: raw flow vs normalized intensity")

    sh = shares.set_index(["origin_pref", "dest_pref"])
    dirs = [("Shiga→Kyoto", ("25", "26")), ("Kyoto→Shiga", ("26", "25")),
            ("Kyoto→Osaka", ("26", "27")), ("Nara→Osaka", ("29", "27"))]
    labs = [d[0] for d in dirs]
    yT = [sh.loc[k, "share_of_T"] * 100 for _, k in dirs]
    yE = [sh.loc[k, "share_of_E"] * 100 for _, k in dirs]
    x = np.arange(len(dirs))
    ax[1].bar(x - 0.2, yT, 0.38, color="#4477aa", label="% of all commuters/students (T)")
    ax[1].bar(x + 0.2, yE, 0.38, color="#eeaa33", label="% of out-of-prefecture trips (E)")
    ax[1].set_xticks(x, labs, rotation=15, ha="right")
    ax[1].set_ylabel("share (%)")
    ax[1].legend(fontsize=8)
    ax[1].set_title("Directional asymmetry")
    fig.tight_layout()
    FIG_DIR = ROOT / "outputs/figures"
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / "F8_case_selection.png", bbox_inches="tight")
    plt.close(fig)

    # ---- cs_* manuscript values --------------------------------------
    def pair(a, b):
        return _row(comp, a, b)

    ks, ko, kn, no = pair("26", "25"), pair("26", "27"), pair("26", "29"), pair("27", "29")
    shiga_munis = int((top[top.origin_pref == "25"]
                     .largest_ext_dest_pref == "26").sum())
    kyoto_munis_osaka = int((top[top.origin_pref == "26"]
                            .largest_ext_dest_pref == "27").sum())
    kyoto_munis_shiga = int((top[top.origin_pref == "26"]
                            .largest_ext_dest_pref == "25").sum())
    cs = {
        # verified external facts: prefectural-office distance (uub.jp
        # 47-prefecture ranking, shortest pair nationwide) and JR rail time
        "cs_capital_km": "10.5 km",
        "cs_rail_min": "10 minutes",
        "cs_bidir_ko": f"{ko.F_bidirectional:,.0f}",
        "cs_s_ks": f"{ks.S_bidir_over_Psum * 100:.2f}%",
        "cs_s_ko": f"{ko.S_bidir_over_Psum * 100:.2f}%",
        "cs_s_kn": f"{kn.S_bidir_over_Psum * 100:.2f}%",
        "cs_sk_T": f"{ks.R_j_to_i * 100:.1f}%",
        "cs_ks_T": f"{ks.R_i_to_j * 100:.1f}%",
        "cs_ko_T": f"{ko.R_i_to_j * 100:.1f}%",
        "cs_no_T": f"{no.R_j_to_i * 100:.1f}%",
        "cs_s_oh": f"{pair('27', '28').S_bidir_over_Psum * 100:.2f}%",
        "cs_sk_E": f"{ks.R_ext_j_to_i * 100:.1f}%",
        "cs_shiga_munis": shiga_munis,
        "cs_kyoto_munis_osaka": kyoto_munis_osaka,
        "cs_kyoto_munis_shiga": kyoto_munis_shiga,
    }
    mv_path = ROOT / "manuscript/manuscript_values.csv"
    prov = {"units": "", "source_file": "outputs/tables/case_selection_comparison_full.csv",
            "source_columns": "F,R,S,T,E + external sources (uub.jp, JR)",
            "analysis_step": "case_selection", "figure_table_reference": "T7,F8",
            "manuscript_location": "§4.6"}
    new = pd.DataFrame([{"value_id": k, "display_value": v, "raw_value": v, **prov}
                        for k, v in cs.items()])
    if mv_path.exists():
        mv = pd.read_csv(mv_path)
        mv = mv[~mv.value_id.isin(new.value_id)]
        mv = pd.concat([mv, new], ignore_index=True)
        mv.to_csv(mv_path, index=False)
        print(f"cs_* values appended: {len(new)}")
    else:
        new.to_csv(mv_path, index=False)
        print(f"WARNING: {mv_path} missing; wrote cs_* rows only")


if __name__ == "__main__":
    main()
