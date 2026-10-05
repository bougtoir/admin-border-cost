"""Tables T1–T6 (markdown + csv) from computed artifacts only."""
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
OUT = ROOT / "data/processed"
MODELS = ROOT / "outputs/models"
TAB = ROOT / "outputs/tables"
TAB.mkdir(parents=True, exist_ok=True)
PLAC = ROOT / "outputs/placebo"


def _md(df, path):
    path.write_text(df.to_markdown(index=False))
    df.to_csv(path.with_suffix(".csv"), index=False)


def main():
    res = pd.read_csv(TAB / "model_results.csv")

    # T1 data sources (from provenance ledger summary, static structure)
    t1 = pd.DataFrame([
        ["Small-area boundaries + population", "e-Stat 統計GIS r2ka (2020 census)",
         "data/raw/r2ka_*.zip", "12,398 polygons (11,978 units)"],
        ["Commuting/schooling OD", "e-Stat Census Table 6-1 (2020)",
         "data/raw/od_*.xlsx", "municipality×municipality (ward-level)"],
        ["Population projections", "IPSS 2023 municipal projections",
         "data/raw/ipss_kekkahyo1.xlsx", "2020–2050, 55 municipal units"],
        ["Statutory districts", "公職選挙法 別表第一 (e-Gov law API)",
         "data/raw/law_kosenkyoho.xml", "Kyoto 6 + Shiga 3 = 9"],
    ], columns=["dataset", "source", "raw path", "coverage"])
    _md(t1, TAB / "T1_data_sources.md")

    # T2 current map metrics (Level B M0 if present else Level A)
    cur = res[(res.model == "M1") & (res.boundary_on == True)]
    m0 = res[(res.model == "M0")] if (res.model == "M0").any() else None
    rows = []
    for level in ("A", "B"):
        s = res[(res.level == level) & (res.model.isin(["M0", "M1"]))]
        if m0 is not None:
            s0 = res[(res.level == level) & (res.model == "M0")]
            if len(s0):
                rows.append([level, "current", *[_fmt(s0.iloc[0], k) for k in
                             ("max_min_ratio", "max_rel_dev", "polsby_popper_mean",
                              "n_split_munis", "severed_flow_total")]])
    t2 = pd.DataFrame(rows, columns=["level", "map", "max/min",
                                     "max|dev|", "PP", "splits", "severed"])
    _md(t2, TAB / "T2_current_metrics.md")

    # T3 ON vs OFF core estimand (per level, median over seeds)
    rows = []
    for level in ("A", "B"):
        for tag, model, on in (("M1 base", "M1", True), ("M2 ON", "M2", True),
                               ("M3 OFF", "M3", False), ("M4 ON", "M4", True),
                               ("M4 OFF", "M4", False)):
            s = res[(res.level == level) & (res.model == model) &
                    (res.boundary_on == on) &
                    (res.tau == CFG["optimization"]["tau_primary"])]
            if not len(s):
                continue
            rows.append([
                level, tag, s.max_rel_dev.median(),
                s.max_min_ratio.median(),
                s.polsby_popper_mean.median() if "polsby_popper_mean" in s else np.nan,
                s.n_split_munis.median() if "n_split_munis" in s else np.nan,
                s.severed_flow_total.median() if "severed_flow_total" in s else np.nan,
                s.objective.median() if "objective" in s
                and s.objective.notna().any()
                else (s.best_objective.median()
                      if "best_objective" in s else np.nan),
            ])
    t3 = pd.DataFrame(rows, columns=["level", "model", "max|dev|", "max/min",
                                     "PP", "splits", "severed", "objective"])
    _md(t3, TAB / "T3_on_off.md")

    # T4 tau sensitivity
    rows = []
    for tau in sorted(res.tau.dropna().unique()):
        for model, on in (("M2", True), ("M3", False)):
            s = res[(res.level == "B") & (res.model == model) &
                    (res.boundary_on == on) & (res.tau == tau)]
            if len(s):
                rows.append([tau, f"{model}{'ON' if on else 'OFF'}",
                             s.max_rel_dev.median(), s.polsby_popper_mean.median(),
                             s.severed_flow_total.median(),
                             s.objective.median() if "objective" in s else np.nan])
    t4 = pd.DataFrame(rows, columns=["tau", "model", "max|dev|", "PP",
                                     "severed", "objective"])
    _md(t4, TAB / "T4_tau_sensitivity.md")

    # T5 placebo summary
    if (PLAC / "placebo_results.csv").exists():
        d = pd.read_csv(PLAC / "placebo_results.csv")
        t5 = pd.DataFrame([
            ["n", len(d)],
            ["n generated", len(d)],
            ["n feasible ON+OFF", int(d.cost.notna().sum())],
            ["n ON-infeasible (no incumbent found)", int(d.cost.isna().sum())],
            ["cost median (feasible)", f"{d.cost.median():.4f}"],
            ["cost IQR (feasible)", f"{d.cost.quantile(.25):.4f} – {d.cost.quantile(.75):.4f}"],
            ["cost p5–p95 (feasible)", f"{d.cost.quantile(.05):.4f} – {d.cost.quantile(.95):.4f}"],
        ], columns=["statistic", "value"])
        _md(t5, TAB / "T5_placebo.md")

    # T6 future robustness + M5
    rows = []
    yrs = CFG["robustness"]["projection_years"]
    for model, on in (("M2", True), ("M3", False), ("M4", True), ("M4", False)):
        s = res[(res.level == "B") & (res.model == model) &
                (res.boundary_on == on) &
                (res.tau == CFG["optimization"]["tau_primary"])]
        if len(s):
            cols = [f"fut_S1_{y}_maxdev" for y in yrs]
            have = [c for c in cols if c in s]
            rows.append([f"{model}{'ON' if on else 'OFF'}"] +
                        [round(s[c].median(), 3) for c in have])
    if rows:
        t6 = pd.DataFrame(rows, columns=["model"] +
                          [c.replace("fut_S1_", "").replace("_maxdev", "")
                           for c in have])
        _md(t6, TAB / "T6_future.md")
    m5 = res[res.model == "M5"]
    if len(m5):
        t6b = m5[["level", "seed", "reassigned_pop", "reassigned_units",
                  "reassigned_pop_frac", "max_rel_dev"]].copy()
        _md(t6b, TAB / "T6b_min_intervention.md")
    print("tables:", sorted(p.name for p in TAB.glob("T*")))


def _fmt(r, k):
    v = r.get(k)
    return round(v, 4) if pd.notna(v) else "—"


if __name__ == "__main__":
    main()
