"""Aggregate all model JSONs (Level A + B, tau sensitivity, M5, placebo,
flow-normalization sensitivity, geography QC) into:
  outputs/tables/model_results.csv   — one row per run
  manuscript/manuscript_values.csv   — key,value traceability for prose
"""
import glob
import json
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
MODELS = ROOT / "outputs/models"
TAB = ROOT / "outputs/tables"
TAB.mkdir(parents=True, exist_ok=True)
MAN = ROOT / "manuscript"
MAN.mkdir(exist_ok=True)

FLAT = ["max_min_ratio", "max_rel_dev", "mean_abs_dev", "rms_dev",
        "contiguous", "polsby_popper_mean", "polsby_popper_min",
        "n_split_munis", "severed_flow_total", "severed_fraction",
        "within_district_retention", "cross_pref_flow",
        "cross_pref_flow_severed", "cross_pref_flow_retained",
        "reassigned_pop", "reassigned_units", "reassigned_pop_frac",
        "total_boundary_m"]


def flatten(rec):
    m = rec.get("metrics", {}) or {}
    row = {k: rec.get(k) for k in
           ("model", "boundary_on", "tau", "seed", "status", "solver",
            "runtime_sec", "objective", "bound", "gap", "best_objective",
            "iters", "optimality", "greedy_repair_moves")}
    for k in FLAT:
        if k in m:
            row[k] = m[k]
    fut = m.get("future", {}).get("S1", {})
    for y, d in fut.items():
        row[f"fut_S1_{y}_maxdev"] = d.get("max_rel_dev")
    dur = m.get("durability") or {}
    for scen, y in dur.items():
        row[f"durability_{scen}"] = y
    return row


def main():
    rows = []
    for fn in sorted(glob.glob(str(MODELS / "*.json"))):
        rec = json.loads(Path(fn).read_text())
        row = flatten(rec)
        row["level"] = "A" if Path(fn).name.startswith("A_") else "B"
        row["file"] = Path(fn).name
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(TAB / "model_results.csv", index=False)
    print(df[["file", "status", "max_rel_dev", "contiguous"]].to_string())

    # manuscript values: key metrics of primary runs
    vals = {}

    def pick(level, model, on, tau=None, seed=None):
        tau = CFG["optimization"]["tau_primary"] if tau is None else tau
        seed = CFG["optimization"]["seeds"][0] if seed is None else seed
        q = (df.level == level) & (df.model == model) & (df.boundary_on == on)
        if model != "M0":
            q &= (df.tau == tau) & (df.seed == seed)
        r = df[q]
        return r.iloc[0] if len(r) else None

    for level in ("A", "B"):
        for tag, model, on in (("base", "M1", True), ("on", "M2", True),
                               ("off", "M3", False)):
            # primary = median over seeds by max_rel_dev
            sub = df[(df.level == level) & (df.model == model) &
                     (df.boundary_on == on) &
                     (df.tau == CFG["optimization"]["tau_primary"])]
            if len(sub):
                best = sub.loc[sub.objective.idxmin()] \
                    if "objective" in sub and sub.objective.notna().any() \
                    else sub.iloc[0]
                for k in FLAT:
                    if k in best and pd.notna(best[k]):
                        vals[f"{level}_{tag}_{k}"] = best[k]
                obj = best.get("objective")
                vals[f"{level}_{tag}_objective"] = \
                    obj if pd.notna(obj) else best.get("best_objective")
                vals[f"{level}_{tag}_status"] = best.get("status")
        # core estimand
        if f"{level}_off_objective" in vals and f"{level}_on_objective" in vals \
           and vals[f"{level}_off_objective"] and vals[f"{level}_on_objective"]:
            vals[f"cost_border_{level}"] = (vals[f"{level}_on_objective"]
                                          - vals[f"{level}_off_objective"])
    # defensible interval for the true Level-A cost:
    # L*_ON in [bound_on, inc_on]; L*_OFF in [bound_off, inc_on] because the ON
    # assignment is OFF-feasible. Hence cost in [0, inc_on - bound_off].
    sub_on = df[(df.level == "A") & (df.model == "M2") & (df.boundary_on == True)
                & (df.tau == CFG["optimization"]["tau_primary"])]
    sub_off = df[(df.level == "A") & (df.model == "M3") & (df.boundary_on == False)
                 & (df.tau == CFG["optimization"]["tau_primary"]) &
                 (df.status == "FEASIBLE")]
    if len(sub_on) and len(sub_off):
        inc_on = float(sub_on.objective.min())
        bound_off = float(sub_off.bound.min())
        vals["cost_border_A_lo"] = 0.0
        vals["cost_border_A_hi"] = inc_on - bound_off
        vals["cost_border_A_hi_frac"] = (inc_on - bound_off) / inc_on
        vals["A_on_bound"] = float(sub_on.bound.min())
    # M0 current map
    for level in ("A", "B"):
        r = pick(level, "M0", True)
        if r is not None:
            for k in FLAT:
                if k in r and pd.notna(r[k]):
                    vals[f"{level}_current_{k}"] = r[k]
    # M5
    r = pick("B", "M5", True)
    if r is not None:
        for k in ("reassigned_pop", "reassigned_units", "reassigned_pop_frac"):
            if k in r and pd.notna(r[k]):
                vals[f"M5_{k}"] = r[k]
    # placebo
    prf = ROOT / "outputs/placebo/placebo_results.csv"
    ps = ROOT / "outputs/placebo/placebo_summary.json"
    if prf.exists():
        d = pd.read_csv(prf)
        vals["placebo_n"] = len(d)
        vals["placebo_n_feasible"] = int(d.cost.notna().sum())
        vals["placebo_infeasible_share"] = float(d.cost.isna().mean() * 100)
        vals["placebo_cost_median"] = float(d.cost.median())
        vals["placebo_cost_iqr"] = (f"{d.cost.quantile(.25):.4f} – "
                                    f"{d.cost.quantile(.75):.4f}")
        # real border cost on the same heuristic scale (real_border_cost.py)
        rc = ROOT / "outputs/placebo/real_border_cost.json"
        if rc.exists():
            r = json.loads(rc.read_text())
            vals["cost_border_heuristic"] = float(r["median"])
            vals["placebo_pct"] = float(
                (d.cost < vals["cost_border_heuristic"]).mean() * 100)
        # functional alignment: OD crossing the real border vs placebo borders
        co = ROOT / "outputs/placebo/cross_od.csv"
        if co.exists():
            c = pd.read_csv(co)
            vals["cross_od_real"] = float(json.loads(
                (ROOT / "outputs/placebo/cross_od_real.json").read_text()
            )["real_cross_od"])
            vals["cross_od_placebo_median"] = float(c.cross_od.median())
            vals["cross_od_placebo_iqr"] = (f"{c.cross_od.quantile(.25):.0f} – "
                                          f"{c.cross_od.quantile(.75):.0f}")
            vals["cross_od_real_pct"] = float(
                (c.cross_od < vals["cross_od_real"]).mean() * 100)
    elif ps.exists():
        s = json.loads(ps.read_text())
        vals.update({f"placebo_{k}": v for k, v in s.items()})

    # region stats + future/durability keys used in prose
    ml = pd.read_csv(OUT := ROOT / "data/processed" / "muni_lookup.csv")
    vals["n_muni"] = len(ml)
    vals["region_pop"] = float(ml["pop"].sum()) if "pop" in ml else None
    fq = ROOT / "outputs/diagnostics/flows_qc.json"
    if fq.exists():
        f = json.loads(fq.read_text())
        vals["n_cross"] = float(f.get("cross_pref_flow_Kyoto_to_Shiga", 0)
                                + f.get("cross_pref_flow_Shiga_to_Kyoto", 0))
        vals["total_flow_within_region"] = f.get("total_flow_within_region")
    gq = ROOT / "outputs/diagnostics/geography_qc.json"
    if gq.exists():
        g = json.loads(gq.read_text())
        vals["n_small"] = g.get("n_smallarea_units")
    res = df
    pop25 = res  # placeholder no-op
    gA = ml
    vals["pop_shiga"] = float(gA[gA.pref_code.astype(int) == 25]["pop"].sum()) \
        if "pref_code" in gA else None
    vals["pop_kyoto"] = float(gA[gA.pref_code.astype(int) == 26]["pop"].sum()) \
        if "pref_code" in gA else None
    for level in ("A", "B"):
        for tag, model, on in (("on", "M2", True), ("off", "M3", False),
                               ("m4on", "M4", True), ("m4off", "M4", False)):
            sub = df[(df.level == level) & (df.model == model) &
                     (df.boundary_on == on) &
                     (df.tau == CFG["optimization"]["tau_primary"])]
            if not len(sub):
                continue
            best = sub.iloc[0]
            for c in sub.columns:
                if c.startswith("fut_") or c.startswith("durability_"):
                    if pd.notna(best[c]):
                        vals[f"{level}_{tag}_{c}"] = best[c]
    def prov(key):
        """Numerical-integrity provenance per key (Phase-13 audit schema)."""
        p = {"units": "", "source_file": "outputs/tables/model_results.csv",
             "source_columns": "", "analysis_step": "aggregate_results",
             "figure_table_reference": "", "manuscript_location": ""}
        if key.startswith(("cost_border", "A_on_", "A_off_", "B_on_", "B_off_",
                           "A_current", "B_current", "M5_")):
            p["source_columns"] = "objective,best_objective,bound,metrics"
            p["figure_table_reference"] = "T3"
            p["manuscript_location"] = "Results §3.2"
        elif key.startswith("placebo"):
            p["source_file"] = "outputs/placebo/placebo_results.csv"
            p["source_columns"] = "cost,status,border_id"
            p["figure_table_reference"] = "T5,F6"
            p["manuscript_location"] = "Results §3.3"
        elif key.startswith("cross_od"):
            p["source_file"] = "outputs/placebo/cross_od.csv"
            p["source_columns"] = "cross_od"
            p["units"] = "daily trips"
            p["figure_table_reference"] = "F6"
            p["manuscript_location"] = "Results §3.2-3.3"
        elif key in ("n_cross", "total_flow_within_region"):
            p["source_file"] = "outputs/diagnostics/flows_qc.json"
            p["units"] = "daily trips"
            p["manuscript_location"] = "§1-2"
        elif key in ("n_muni", "n_small", "region_pop", "pop_shiga",
                     "pop_kyoto"):
            p["source_file"] = "data/processed/muni_lookup.csv; geography_qc.json"
            p["units"] = "count/persons"
            p["manuscript_location"] = "§2 Data"
        elif "fut_" in key or "durability_" in key:
            p["figure_table_reference"] = "T6,F7"
            p["manuscript_location"] = "Results §3.4"
        elif key.endswith("_polsby_popper_mean") or key.endswith("_n_split_munis") \
                or key.endswith("_severed_flow_total") or key.endswith("_max_rel_dev"):
            p["figure_table_reference"] = "T3"
            p["manuscript_location"] = "Results §3.2"
        return p
    mv = pd.DataFrame([
        {"value_id": k, "display_value": v, "raw_value": v, **prov(k)}
        for k, v in vals.items()])
    mv.to_csv(MAN / "manuscript_values.csv", index=False)
    # keep legacy two-column view for template substitution
    pd.DataFrame({"key": mv.value_id, "value": mv.display_value}) \
      .to_csv(MAN / "manuscript_values_kv.csv", index=False)
    print(f"rows={len(df)} values={len(vals)}")


if __name__ == "__main__":
    main()
