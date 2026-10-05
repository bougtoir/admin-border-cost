"""Level A (municipality/ward units) models via OR-Tools CP-SAT.

Contiguity: rooted single-commodity flow per district.
  - root var r_{i,d} in {0,1}, exactly one root per district, r_{i,d} <= x_{i,d}
  - arc flow f_{i,j,d} >= 0 on both directions of each edge, <= n * min-membership
  - balance: sum_in f - sum_out f >= x_{i,d} - n * r_{i,d}
    (members consume >=1 net; the root generates freely)

Objectives (weighted sum, weights pre-declared):
  pop   : t >= |P_d/Pbar - 1|  (t minimized; tau is a hard cap)
  comp  : sum over edges shared_perim * cut_{ij}
  flow  : sum over OD pairs F_{ij} * cut_{ij}
  split : degenerate at Level A (units are municipalities) -> skipped
  change: population assigned to a different district than current (M5)
  future: t_f >= max over years/scenarios |P_{d,t,s}/Pbar_{t,s} - 1|
"""
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from ortools.sat.python import cp_model

from . import metrics
from .model_data import (
    K,
    adjacency_with_perimeter,
    load_flow_edges_levelA,
    load_units,
)

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
DIAG = ROOT / "outputs/diagnostics"
MODELS = ROOT / "outputs/models"
MODELS.mkdir(parents=True, exist_ok=True)

PREF_OF = {"25": 0, "26": 1}  # boundary ON forbids mixing across this flag


def build_base(g, edges, boundary_on: bool, tau: float, group=None):
    n = len(g)
    pop = g["pop"].to_numpy()
    Pbar = pop.sum() / K
    m = cp_model.CpModel()
    x = {(i, d): m.NewBoolVar(f"x_{i}_{d}") for i in range(n) for d in range(K)}
    for i in range(n):
        m.Add(sum(x[i, d] for d in range(K)) == 1)
    pof = (np.asarray(group) if group is not None
           else g["pref_code"].map(PREF_OF).to_numpy())
    if boundary_on:
        for i in range(n):
            for j in range(n):
                if i < j and pof[i] != pof[j]:
                    for d in range(K):
                        m.Add(x[i, d] + x[j, d] <= 1)
    # population bounds
    cap = int(round(Pbar * (1 + tau)))
    floor = int(np.floor(Pbar * (1 - tau)))
    for d in range(K):
        pd_ = m.NewIntVar(floor, cap, f"P_{d}")
        m.Add(pd_ == sum(int(pop[i]) * x[i, d] for i in range(n)))
    # contiguity via rooted SCF
    arcs = []
    for i, j in edges[["i", "j"]].itertuples(index=False):
        arcs.append((int(i), int(j)))
        arcs.append((int(j), int(i)))
    for d in range(K):
        r = [m.NewBoolVar(f"r_{i}_{d}") for i in range(n)]
        m.Add(sum(r) == 1)
        for i in range(n):
            m.Add(r[i] <= x[i, d])
        fin, fout = {}, {}
        for a, (i, j) in enumerate(arcs):
            f = m.NewIntVar(0, n, f"f_{a}_{d}")
            m.Add(f <= n * x[i, d])
            m.Add(f <= n * x[j, d])
            fin.setdefault(j, []).append(f)
            fout.setdefault(i, []).append(f)
        for i in range(n):
            m.Add(sum(fin.get(i, [])) - sum(fout.get(i, [])) >= x[i, d] - n * r[i])
    return m, x, pop, Pbar


def solve(m, seed, time_limit):
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_search_workers = CFG["optimization"]["workers"]
    s.parameters.random_seed = seed
    s.parameters.log_search_progress = False
    t0 = time.time()
    status = s.Solve(m)
    return s, status, time.time() - t0


def extract(s, x, n):
    a = np.zeros(n, dtype=int)
    for i in range(n):
        for d in range(K):
            if s.Value(x[i, d]):
                a[i] = d
                break
    return a


def run_levelA(model: str, boundary_on: bool, tau=None, weights=None,
               seed=11, future=False, min_change=False, base_assign=None,
               hint_assign=None):
    tau = CFG["optimization"]["tau_primary"] if tau is None else tau
    weights = weights or CFG["optimization"]["weights_primary"]
    g = load_units("A").reset_index(drop=True)
    edges = adjacency_with_perimeter(g)
    n = len(g)
    m, x, pop, Pbar = build_base(g, edges, boundary_on, tau)

    if hint_assign is not None:
        # solution hint speeds up feasibility discovery (e.g. M1 result)
        for i in range(n):
            for d in range(K):
                m.AddHint(x[i, d], 1 if hint_assign[i] == d else 0)
    obj = []
    SCAL = 1000
    if not min_change:
        t = m.NewIntVar(0, SCAL, "t")
        for d in range(K):
            pd_lin = sum(int(pop[i]) * x[i, d] for i in range(n))
            m.Add(SCAL * pd_lin - SCAL * int(Pbar) <= t * int(Pbar))
            m.Add(SCAL * int(Pbar) - SCAL * pd_lin <= t * int(Pbar))
        obj.append(int(weights.get("pop", 1.0) * SCAL) * t)

    # cut indicators shared by compactness + flow objectives
    cut = {}
    for (i, j) in edges[["i", "j"]].itertuples(index=False):
        c = m.NewBoolVar(f"c_{i}_{j}")
        for d in range(K):
            m.Add(c >= x[i, d] - x[j, d])
            m.Add(c >= x[j, d] - x[i, d])
        m.Add(c <= 1)
        cut[(i, j)] = c
    if weights.get("compact", 0) > 0:
        obj.append(int(weights["compact"] * 10) *
                   sum(int(round(w)) * c for (_, _, w), c in
                       [(e, cut[(e[0], e[1])]) for e in
                        edges[["i", "j", "w"]].itertuples(index=False)]))
    if weights.get("flow", 0) > 0:
        fedges = load_flow_edges_levelA(g)
        pos = {u: i for i, u in enumerate(g.unit_id)}
        obj.append(int(weights["flow"] * 100) *
                   sum(int(round(r.flow)) * cut[(pos[r.o], pos[r.d])]
                       for r in fedges.itertuples()
                       if (pos[r.o], pos[r.d]) in cut or (pos[r.d], pos[r.o]) in cut))
    if future:
        up = pd.read_parquet(ROOT / "data/processed/unit_projections.parquet")
        gB = load_units("B")
        posB = {u: i for i, u in enumerate(gB.unit_id)}
        # Level A future: muni-level growth applied to muni totals directly
        mp = pd.read_csv(ROOT / "data/processed/muni_projections.csv")
        for y in CFG["robustness"]["projection_years"]:
            gy = mp[mp.year == y].set_index("muni_code")["growth"]
            py = g.muni_code.astype(int).map(gy).to_numpy() * pop
            pbary = py.sum() / K
            tf = m.NewIntVar(0, SCAL, f"tf_{y}")
            for d in range(K):
                plin = sum(int(round(py[i])) * x[i, d] for i in range(n))
                m.Add(SCAL * plin - SCAL * int(pbary) <= tf * int(pbary))
                m.Add(SCAL * int(pbary) - SCAL * plin <= tf * int(pbary))
            obj.append(int(weights.get("future", 0.3) * SCAL) * tf)
    if min_change and base_assign is not None:
        ch = sum(int(round(pop[i])) * (1 - x[i, int(base_assign[i])])
                 for i in range(n))
        m.Minimize(ch)
    else:
        m.Minimize(sum(obj))

    s, status, rt = solve(m, seed, CFG["optimization"]["time_limit_level_a_sec"])
    assign = extract(s, x, n) if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    rec = {
        "model": model, "boundary_on": boundary_on, "tau": tau, "seed": seed,
        "status": s.StatusName(status), "runtime_sec": rt,
        "objective": s.ObjectiveValue() if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
        "bound": s.BestObjectiveBound() if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
        "gap": (s.ObjectiveValue() - s.BestObjectiveBound()) / max(abs(s.ObjectiveValue()), 1e-9)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
    }
    fn = MODELS / f"A_{model}_{'on' if boundary_on else 'off'}_tau{tau}_s{seed}.json"
    if assign is not None:
        pd.DataFrame({"unit_id": g.unit_id, "district": assign}) \
            .to_csv(MODELS / fn.name.replace(".json", "_assign.csv"), index=False)
        res = metrics.evaluate(assign, g, edges,
                               label=f"A_{model}_{'on' if boundary_on else 'off'}")
        rec["metrics"] = {k: v for k, v in res.items()
                          if k not in ("district_pops", "polsby_popper",
                                       "district_perimeter_m",
                                       "district_area_km2")}
        rec["metrics"]["district_pops"] = res["district_pops"]
        rec["metrics"]["polsby_popper"] = res["polsby_popper"]
    fn.write_text(json.dumps(rec, indent=2))
    print(json.dumps(rec, indent=2))
    return assign, rec


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="M2")
    ap.add_argument("--off", action="store_true")
    ap.add_argument("--tau", type=float, default=None)
    ap.add_argument("--seed", type=int, default=11)
    args = ap.parse_args()
    run_levelA(args.model, not args.off, tau=args.tau, seed=args.seed,
               future=(args.model == "M4"))
