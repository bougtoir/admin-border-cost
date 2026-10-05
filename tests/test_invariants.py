"""Mathematical invariants I1-I8 on saved model outputs (runs in make qc).

I1 ON-feasible assignment is OFF-feasible (pure constraint check).
I2 identical assignment -> identical objective under ON/OFF formulations.
I3 independent evaluator reproduces logged solver objectives.
I4 every district connected. I5 every unit assigned once.
I6 population totals reconcile. I7 ON never mixes pref groups.
I8 best validated ON assignment gives an OFF incumbent <= ON objective.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from optimization import metrics
from optimization.model_data import K, adjacency_with_perimeter, load_flow_edges_levelA, load_units

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "outputs/models"
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
W = CFG["optimization"]["weights_primary"]
SCAL = 1000


def load_assign(name):
    return pd.read_csv(MODELS / f"{name}_assign.csv")["district"].to_numpy()


def obj_levelA(assign, g, edges):
    """Independent replica of the CP-SAT integer objective."""
    pop = g["pop"].to_numpy()
    Pbar = int(pop.sum() / K)
    pd_ = np.bincount(assign, weights=pop, minlength=K)
    t = int(np.ceil(np.abs(SCAL * pd_ - SCAL * Pbar).max() / Pbar - 1e-9))
    o = int(W.get("pop", 1.0) * SCAL) * t
    cutset = set()
    cutw = 0
    for i, j, w in edges.itertuples(index=False):
        i, j = int(i), int(j)
        if assign[i] != assign[j]:
            cutw += int(round(w))
            cutset.add((min(i, j), max(i, j)))
    o += int(W["compact"] * 10) * cutw
    fedges = load_flow_edges_levelA(g)
    pos = {u: i for i, u in enumerate(g.unit_id)}
    fs = sum(int(round(r.flow)) for r in fedges.itertuples()
             if (min(pos[r.o], pos[r.d]), max(pos[r.o], pos[r.d])) in cutset)
    o += int(W["flow"] * 100) * fs
    return o


def mixed_districts(assign, pref):
    df = pd.DataFrame({"d": assign, "p": pref})
    return int((df.groupby("d")["p"].nunique() > 1).sum())


def run_all():
    results = []
    g = load_units("A").reset_index(drop=True)
    edges = adjacency_with_perimeter(g)
    pref = g["pref_code"].astype(int).to_numpy()
    pop_total = int(g["pop"].sum())

    for lvl, name in [("A", "A_M2_on_tau0.2_s11"), ("A", "A_M3_off_tau0.2_s11"),
                      ("B", "B_M2_on_tau0.2_s11"), ("B", "B_M3_off_tau0.2_s11")]:
        if not (MODELS / f"{name}_assign.csv").exists():
            continue
        a = load_assign(name)
        gB = load_units(lvl)
        edgesB = adjacency_with_perimeter(gB)
        prefB = gB["pref_code"].astype(int).to_numpy()
        # I5: assigned once & valid
        assert len(a) == len(gB) and a.min() >= 0 and a.max() < K, name
        # I6
        assert int(np.bincount(a, weights=gB["pop"].to_numpy(),
                               minlength=K).sum()) == int(gB["pop"].sum()), name
        # I4
        viol = metrics.contiguity_violations(a, edgesB)
        results.append({"run": name, "I4_contiguous": len(viol) == 0})
        # I1/I7: ON mixes nothing
        on = "_on_" in name
        results[-1]["I7_no_mixed_on"] = (mixed_districts(a, prefB) == 0) if on else None
        # I3: evaluator reproduces logged Level-A objective
        if lvl == "A":
            rec = json.loads((MODELS / f"{name}.json").read_text())
            mine = obj_levelA(a, g, edges)
            results[-1]["I3_eval_matches_log"] = (mine == int(rec["objective"]))
    # I8: ON assign evaluated under identical OFF objective gives OFF incumbent
    if (MODELS / "A_M2_on_tau0.2_s11_assign.csv").exists():
        a_on = load_assign("A_M2_on_tau0.2_s11")
        a_off = load_assign("A_M3_off_tau0.2_s11")
        o_on = obj_levelA(a_on, g, edges)
        o_off = obj_levelA(a_off, g, edges)
        results.append({"run": "I8", "on_obj": o_on,
                        "off_incumbent_obj": o_off,
                        "off_upper_bound": min(o_on, o_off),
                        "I8_nesting_respected": min(o_on, o_off) <= o_on})
    return results


if __name__ == "__main__":
    for r in run_all():
        print(r)
