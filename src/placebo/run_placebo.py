"""For each placebo border, solve the M2 objective twice at Level A:
  ON  : districts may not contain units from both sides of the fake border
  OFF : identical minus the border constraint
Placebo cost = objective(OFF) - objective(ON); compared against the real
border cost gap (M2 vs M3) to ask whether the real border is unusual.
"""
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from ortools.sat.python import cp_model

from src.optimization.cpsat_levelA import build_base, extract
from src.optimization.model_data import (
    K,
    adjacency_with_perimeter,
    load_flow_edges_levelA,
    load_units,
)

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
PLAC = ROOT / "outputs/placebo"
TL = CFG["placebo"].get("time_limit_sec", 60)


def solve_one(g, edges, group, boundary_on, seed, hint=None):
    tau = CFG["optimization"]["tau_primary"]
    w = CFG["optimization"]["weights_primary"]
    m, x, pop, Pbar = build_base(g, edges, boundary_on, tau, group=group)
    n = len(g)
    obj = []
    SCAL = 1000
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
    if w.get("compact", 0) > 0:
        obj.append(int(w["compact"] * 10) *
                   sum(int(round(w_)) * cut[(i, j)]
                       for i, j, w_ in edges[["i", "j", "w"]].itertuples(index=False)))
    if w.get("flow", 0) > 0:
        fedges = load_flow_edges_levelA(g)
        pos = {u: i for i, u in enumerate(g.unit_id)}
        obj.append(int(w["flow"] * 100) *
                   sum(int(round(r.flow)) * cut[(pos[r.o], pos[r.d])]
                       for r in fedges.itertuples()
                       if (pos[r.o], pos[r.d]) in cut))
    m.Minimize(sum(obj))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = TL
    if hint is not None:
        for i in range(n):
            m.AddHint(x[i, int(hint[i])], 1)
    s.parameters.num_search_workers = CFG["optimization"]["workers"]
    s.parameters.random_seed = seed
    t0 = time.time()
    status = s.Solve(m)
    return {
        "status": s.StatusName(status),
        "objective": s.ObjectiveValue() if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
        "bound": s.BestObjectiveBound() if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
        "runtime_sec": time.time() - t0,
        "assign": extract(s, x, n) if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
    }


def boundary_repair(st, max_iter=2000):
    """Eliminate districts mixing both border groups: move minority-group
    units into an adjacent district that has none of that group's units."""
    from src.optimization.local_search_levelB import _apply

    moves = 0
    while moves < max_iter:
        mixed = np.where((st.pref_cnt[:, 0] > 0) & (st.pref_cnt[:, 1] > 0))[0]
        if len(mixed) == 0:
            return moves
        moved = False
        best = None
        for d in mixed:
            minority = 0 if st.pref_cnt[d, 0] <= st.pref_cnt[d, 1] else 1
            # minority-first (removes the violation), then any unit whose move
            # keeps improvement possible; score = (new max dev, mixing left)
            for grp_ in (minority, 1 - minority):
                for i in [i for i in range(st.n)
                          if st.assign[i] == d and st.pref[i] - 25 == grp_]:
                    for j, _ in st.adj[i]:
                        b = st.assign[j]
                        if b == d or st.pref_cnt[b, 1 - grp_] > 0:
                            continue
                        if not st.donor_connected(i, d):
                            continue
                        d2 = st.dp.copy()
                        d2[d] -= st.pop[i]
                        d2[b] += st.pop[i]
                        dev_after = float(np.abs(d2 / st.pbar - 1).max())
                        pc = st.pref_cnt.copy()
                        pc[d, grp_] -= 1
                        pc[b, grp_] += 1
                        mix = int(((pc[:, 0] > 0) & (pc[:, 1] > 0)).sum())
                        key = (mix, dev_after)
                        if best is None or key < best[0]:
                            best = (key, i, d, b)
        if best is not None:
            _, i, a, b = best
            _apply(st, i, a, b)
            moves += 1
            moved = True
        if not moved:
            return -moves - 1  # infeasible for this repair heuristic
    return moves


def solve_one_h(g, edges, group, boundary_on, seed, a0, iters=20000):
    """Heuristic Level A solve: boundary repair -> greedy dev repair -> SA.
    Returns dict mimicking the CP-SAT result plus objective value."""
    from src.optimization.local_search_levelB import State, anneal, greedy_repair

    tau = CFG["optimization"]["tau_primary"]
    w = CFG["optimization"]["weights_primary"]
    t0 = time.time()
    st = State(g, edges, a0, boundary_on, w, tau, group=group)
    bm = boundary_repair(st) if boundary_on else 0
    if bm < 0:
        return {"status": "HEUR-INFEASIBLE", "objective": None,
                "bound": None, "runtime_sec": time.time() - t0, "assign": None}
    greedy_repair(st)
    best_assign, best = anneal(st, seed, iters)
    # rebuild district aggregates for best solution before final objective
    st2 = State(g, edges, best_assign, boundary_on, w, tau, group=group)
    dev2 = float(np.abs(st2.dp / st2.pbar - 1).max())
    feasible = dev2 <= tau and (
        not boundary_on
        or not bool(((st2.pref_cnt[:, 0] > 0) & (st2.pref_cnt[:, 1] > 0)).any()))
    return {
        "status": "HEUR-FEASIBLE" if feasible else "HEUR-INFEASIBLE",
        "objective": st2.objective() if feasible else None,
        "bound": None,
        "runtime_sec": time.time() - t0,
        "assign": best_assign.tolist() if feasible else None,
    }


def main():
    borders = pd.read_csv(PLAC / "borders.csv")
    g = load_units("A").reset_index(drop=True)
    edges = adjacency_with_perimeter(g)
    m1 = pd.read_csv(ROOT / "outputs/models/A_M1_on_tau0.2_s11_assign.csv")
    dmap = {str(k): v for k, v in zip(m1.unit_id, m1.district)}
    a0 = np.array([dmap[u] for u in g.unit_id])
    seeds = CFG["optimization"]["seeds"][:2]
    rows = []
    for r in borders.itertuples():
        grp = np.array(json.loads(r.group))
        on, off = None, None
        for seed in seeds:
            on = solve_one_h(g, edges, grp, True, seed, a0)
            off = solve_one_h(g, edges, grp, False, seed, a0)
            if on["objective"] is not None and off["objective"] is not None:
                break
        cost = (on["objective"] - off["objective"]
                if on["objective"] is not None and off["objective"] is not None
                else np.nan)
        rows.append({
            "placebo_id": r.placebo_id,
            "pop_share_grp1": r.pop_share_grp1,
            "boundary_len_m": r.boundary_len_m,
            "obj_on": on["objective"], "obj_off": off["objective"],
            "bound_on": on["bound"], "bound_off": off["bound"],
            "status_on": on["status"], "status_off": off["status"],
            "cost": cost,
        })
        print(f"placebo {r.placebo_id}: cost={cost}", flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(PLAC / "placebo_results.csv", index=False)
    summ = {
        "n": len(df),
        "cost_median": float(df.cost.median()),
        "cost_iqr": [float(df.cost.quantile(0.25)), float(df.cost.quantile(0.75))],
        "n_feasible": int(df.cost.notna().sum()),
        "cost_p5_p95": [float(df.cost.quantile(0.05)), float(df.cost.quantile(0.95))],
        "cost_mean": float(df.cost.mean()),
        "cost_std": float(df.cost.std()),
    }
    (PLAC / "placebo_summary.json").write_text(json.dumps(summ, indent=2))
    print(json.dumps(summ, indent=2))


if __name__ == "__main__":
    main()
