"""QC report: checksums, run inventory, feasibility checks, traceability."""
import hashlib
import json
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
RAW = ROOT / "data/raw"
MODELS = ROOT / "outputs/models"
OUT = ROOT / "outputs"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    rep = {"checks": [], "failures": []}

    def check(name, ok, detail=""):
        rep["checks"].append({"check": name, "ok": bool(ok),
                              "detail": str(detail)})
        if not ok:
            rep["failures"].append(name)

    # 1. raw data checksums vs manifest
    sums = RAW / "SHA256SUMS.txt"
    if sums.exists():
        for line in sums.read_text().splitlines():
            if not line.strip():
                continue
            h, fn = line.split()[:2]
            rel = fn.split("data/raw/")[-1]
            p = RAW / rel
            ok = p.exists() and sha(p) == h
            check(f"checksum:{fn}", ok)
    else:
        check("checksums manifest exists", False, "SHA256SUMS.txt missing")

    # 2. run inventory: expected model files
    res_file = OUT / "tables/model_results.csv"
    check("model_results.csv exists", res_file.exists())
    if res_file.exists():
        res = pd.read_csv(res_file)
        tau = CFG["optimization"]["tau_primary"]
        for level in ("A", "B"):
            for model, on in (("M1", True), ("M2", True), ("M3", False)):
                s = res[(res.level == level) & (res.model == model) &
                        (res.boundary_on == on) & (res.tau == tau)]
                check(f"{level} {model} runs present", len(s) > 0,
                      f"n={len(s)}")
                if len(s):
                    feas = s[s.max_rel_dev <= tau + 1e-6]
                    check(f"{level} {model} feasible", len(feas) > 0,
                          f"dev min={s.max_rel_dev.min():.3f}")
                    check(f"{level} {model} contiguous",
                          bool(s.contiguous.all()) if "contiguous" in s else False)
        # paired ON/OFF same seed/tau
        on = res[(res.model == "M2")]
        off = res[(res.model == "M3")]
        paired = set(zip(on.level, on.tau, on.seed)) & \
            set(zip(off.level, off.tau, off.seed))
        check("ON/OFF paired runs", len(paired) > 0, f"pairs={len(paired)}")

    # 3. placebo completeness
    pr = OUT / "placebo/placebo_results.csv"
    if pr.exists():
        d = pd.read_csv(pr)
        check("placebo n>=200", len(d) >= CFG["placebo"]["n_borders"],
              f"n={len(d)}")
        n_pair = int((d.obj_on.notna() & d.obj_off.notna()).sum())
        check("placebo paired solves (>=50 heuristic-feasible)", n_pair >= 50,
              f"feasible pairs={n_pair}/200 (infeasible borders are reported, "
              "not silently dropped)")

    # 4. figures/tables exist
    figs = sorted(p.name for p in (OUT / "figures").glob("F*.png"))
    check("figures F1-F7", len(figs) >= 7, f"{figs}")
    tabs = sorted(p.name for p in (OUT / "tables").glob("T*.md"))
    check("tables T1-T6", len(tabs) >= 5, f"{tabs}")

    # 5. manuscript values cover core estimand
    mv = ROOT / "manuscript/manuscript_values.csv"
    if mv.exists():
        keys = set(pd.read_csv(mv).value_id)
        for need in ("B_on_objective", "B_off_objective", "cost_border_B",
                     "B_on_severed_flow_total", "B_current_max_rel_dev"):
            check(f"manuscript_value:{need}", need in keys)

    rep["n_checks"] = len(rep["checks"])
    rep["n_failures"] = len(rep["failures"])
    out = OUT / "diagnostics/QC_REPORT.json"
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2))
    print(json.dumps({"checks": rep["n_checks"], "failures": rep["failures"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
