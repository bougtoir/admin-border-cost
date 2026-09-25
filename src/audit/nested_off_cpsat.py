"""M3-OFF diagnostic solve with (a) hint = M2-ON incumbent and (b) extended
time limit, so the OFF incumbent cannot be worse than the validated ON
incumbent (ON assignment is OFF-feasible). Writes *_nested.json; does not
touch the original run records."""
import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd
import yaml
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from optimization import metrics
from optimization.cpsat_levelA import build_base, extract
from optimization.model_data import (
    K,
    adjacency_with_perimeter,
    load_flow_edges_levelA,
    load_units,
)

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
MODELS = ROOT / "outputs" / "models"


def solve_off_hinted(tau=0.2, seed=11, tl=600):
    g = load_units("A").reset_index(drop=True)
    edges = adjacency_with_perimeter(g)
    n = len(g)
    m, x, pop, Pbar = build_base(g, edges, False, tau)
    hint = pd.read_csv(MODELS / "A_M2_on_tau0.2_s11_assign.csv")[
        "district"].to_numpy()
    for i in range(n):
        for d in range(K):
            m.AddHint(x[i, d], 1 if hint[i] == d else 0)
    w = CFG["optimization"]["weights_primary"]
    SCAL = 1000
    obj = []
    t = m.NewIntVar(0, SCAL, "t")
    for d in range(K):
        pl = sum(int(pop[i]) * x[i, d] for i in range(n))
        m.Add(SCAL * pl - SCAL * int(Pbar) <= t * int(Pbar))
        m.Add(SCAL * int(Pbar) - SCAL * pl <= t * int(Pbar))
    obj.append(int(w.get("pop", 1.0) * SCAL) * t)
    cut = {}
    for i, j in edges[["i", "j"]].itertuples(index=False):
        c = m.NewBoolVar(f"c_{i}_{j}")
        for d in range(K):
            m.Add(c >= x[i, d] - x[j, d])
            m.Add(c >= x[j, d] - x[i, d])
        m.Add(c <= 1)
        cut[(int(i), int(j))] = c
    obj.append(int(w["compact"] * 10) *
               sum(int(round(w_)) * cut[(i, j)]
                   for i, j, w_ in edges[["i", "j", "w"]].itertuples(index=False)))
    fedges = load_flow_edges_levelA(g)
    pos = {u: i for i, u in enumerate(g.unit_id)}
    obj.append(int(w["flow"] * 100) *
               sum(int(round(r.flow)) * cut[(pos[r.o], pos[r.d])]
                   for r in fedges.itertuples()
                   if (pos[r.o], pos[r.d]) in cut))
    m.Minimize(sum(obj))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_search_workers = CFG["optimization"]["workers"]
    s.parameters.random_seed = seed
    s.parameters.log_search_progress = False
    t0 = time.time()
    status = s.Solve(m)
    rt = time.time() - t0
    rec = {"model": "M3", "boundary_on": False, "tau": tau, "seed": seed,
           "status": s.StatusName(status), "runtime_sec": rt,
           "hinted_from": "A_M2_on_tau0.2_s11_assign.csv",
           "objective": s.ObjectiveValue()
           if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
           "bound": s.BestObjectiveBound()
           if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None}
    if rec["objective"] is not None:
        rec["gap"] = (rec["objective"] - rec["bound"]) / abs(rec["objective"])
        a = extract(s, x, n)
        pd.DataFrame({"unit_id": g.unit_id, "district": a}).to_csv(
            MODELS / "A_M3_off_tau0.2_s11_nested_assign.csv", index=False)
        res = metrics.evaluate(a, g, edges, label="A_M3_off_nested")
        rec["metrics"] = {k: v for k, v in res.items()
                          if k not in ("district_pops", "polsby_popper",
                                       "district_perimeter_m",
                                       "district_area_km2")}
    (MODELS / "A_M3_off_tau0.2_s11_nested.json").write_text(
        json.dumps(rec, indent=2, default=str))
    print(json.dumps(rec, indent=2, default=str))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tl", type=int, default=600)
    args = ap.parse_args()
    solve_off_hinted(tl=args.tl)
