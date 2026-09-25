"""Nesting-invariant audit reruns (Phase 3/4 targeted reanalysis).

Level A: M3-OFF re-solved with the validated M2-ON incumbent as a CP-SAT hint,
guaranteeing the OFF incumbent is no worse than the ON incumbent (the ON
assignment is OFF-feasible: 0 mixed districts, contiguous, same objective).

Level B: M3-OFF annealed starting from the M2-ON best assignment
(init_assign_csv), so the retained best-so-far cannot exceed the ON best.

Outputs tagged *_nested* to distinguish from the original independent runs.
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from optimization import cpsat_levelA, local_search_levelB

MODELS = Path(__file__).resolve().parents[2] / "outputs" / "models"
A_ON = MODELS / "A_M2_on_tau0.2_s11_assign.csv"
B_ON = MODELS / "B_M2_on_tau0.2_s11_assign.csv"


def levelA(seed=11, tau=0.2):
    hint = pd.read_csv(A_ON)["district"].to_numpy()
    assign, rec = cpsat_levelA.run_levelA(
        "M3", boundary_on=False, tau=tau, seed=seed, hint_assign=hint)
    rec["nested_from"] = A_ON.name
    (MODELS / "A_M3_off_tau0.2_s11_nested.json").write_text(
        json.dumps(rec, indent=2, default=str))
    src = MODELS / "A_M3_off_tau0.2_s11_assign.csv"
    if src.exists():
        src.replace(MODELS / "A_M3_off_tau0.2_s11_nested_assign.csv")
    return rec


def levelB(seed=11, tau=0.2, iters=60000):
    best, rec = local_search_levelB.run_levelB(
        "M3", boundary_on=False, seed=seed, tau=tau, iters=iters,
        init_assign_csv=str(B_ON))
    rec["nested_from"] = B_ON.name
    (MODELS / "B_M3_off_tau0.2_s11_nested.json").write_text(
        json.dumps(rec, indent=2, default=str))
    src = MODELS / "B_M3_off_tau0.2_s11_assign.csv"
    if src.exists():
        src.replace(MODELS / "B_M3_off_tau0.2_s11_nested_assign.csv")
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", default="A")
    args = ap.parse_args()
    if args.level == "A":
        levelA()
    else:
        levelB()
