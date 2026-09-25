"""Level B (small-area) districting via simulated annealing on the unit graph.

Move: flip a boundary unit to a neighboring district.
Feasibility: donor district stays connected (checked by BFS on its subgraph);
boundary-ON additionally forbids mixing pref 25/26 within a district.
Objectives (incremental): max pop deviation, shared-boundary cut length
(compactness surrogate), municipality splits, severed OD flow (municipal-share
closed form), future max deviation (S1; S2 evaluated post-hoc), reassignment (M5).

Every accepted final solution is re-validated by metrics.evaluate().
"""
import json
import time
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import yaml

from . import metrics
from .model_data import DISTRICTS, K, adjacency_with_perimeter, load_units

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
MODELS = ROOT / "outputs/models"
MODELS.mkdir(parents=True, exist_ok=True)
OUT = ROOT / "data/processed"


class State:
    def __init__(self, g: gpd.GeoDataFrame, edges: pd.DataFrame,
                 assign0: np.ndarray, boundary_on: bool,
                 weights: dict, tau: float, future_years=None,
                 group: np.ndarray = None):
        self.g = g
        self.n = len(g)
        self.assign = assign0.copy()
        self.boundary_on = boundary_on
        self.w = weights
        self.tau = tau
        self.pop = g["pop"].to_numpy(dtype=float)
        # group override: arbitrary two-group border (placebo); else prefecture
        self.pref = (np.asarray(group, dtype=int) + 25 if group is not None
                     else g["pref_code"].astype(int).to_numpy())
        self.muni = g["muni_code"].to_numpy()
        self.munis = sorted(set(self.muni))
        self.midx = {m: k for k, m in enumerate(self.munis)}
        self.umidx = np.array([self.midx[m] for m in self.muni])
        self.muni_pop = g.groupby("muni_code")["pop"].sum()
        # adjacency: dict i -> list[(j, w_edge)]
        self.adj = {i: [] for i in range(self.n)}
        self.cut_edges = []
        for i, j, w in edges.itertuples(index=False):
            self.adj[int(i)].append((int(j), float(w)))
            self.adj[int(j)].append((int(i), float(w)))
            if w > 0:  # shared boundary length (point-touch contributes 0)
                self.cut_edges.append((int(i), int(j), float(w)))
        # district state
        self.dp = np.bincount(assign0, weights=self.pop, minlength=K)
        self.pbar = self.pop.sum() / K
        self.pref_cnt = np.zeros((K, 3), dtype=int)
        for i, d in enumerate(assign0):
            self.pref_cnt[d, self.pref[i] - 25] += 1
        # muni membership counts per district: matrix M x K counts of units
        self.mc = np.zeros((len(self.munis), K), dtype=int)
        for i, d in enumerate(assign0):
            self.mc[self.umidx[i], d] += 1
        self.n_split = int((self.mc > 0).sum(axis=1).__gt__(1).sum())
        # flows (municipal share form)
        sym = pd.read_csv(OUT / "od_region_matrix_sym.csv", index_col=0)
        self.F = np.zeros((len(self.munis), len(self.munis)))
        names = np.array(self.munis)
        for a in sym.index:
            if a not in self.midx:
                continue
            for b in sym.columns:
                if b in self.midx:
                    self.F[self.midx[a], self.midx[b]] = sym.loc[a, b]
        self.F = np.triu(self.F, 1)
        # future pops (S1)
        self.future_years = future_years or []
        up = pd.read_parquet(OUT / "unit_projections.parquet")
        self.proj = {}
        self.dpf = {}
        pos = {u: i for i, u in enumerate(g.unit_id)}
        for y in self.future_years:
            u = up[(up.year == y) & (up.scenario == "S1")]
            v = np.zeros(self.n)
            v[[pos[t] for t in u.unit_id]] = u.pop_t.values
            self.proj[y] = v
            self.dpf[y] = np.bincount(assign0, weights=v, minlength=K)
        # boundary candidate list
        self._refresh_boundary()

    def _refresh_boundary(self):
        self.boundary_units = [i for i in range(self.n)
                               if any(self.assign[j] != self.assign[i]
                                      for j, _ in self.adj[i])]

    def donor_connected(self, i, a):
        """True if district a stays connected after removing unit i."""
        nbrs = [j for j, _ in self.adj[i] if self.assign[j] == a]
        if len(nbrs) <= 1:
            return True
        target = set(nbrs[1:])
        seen = {nbrs[0]}
        stack = [nbrs[0]]
        while stack:
            u = stack.pop()
            for v, _ in self.adj[u]:
                if v != i and self.assign[v] == a and v not in seen:
                    seen.add(v)
                    if v in target:
                        target.discard(v)
                        if not target:
                            return True
                    stack.append(v)
        return not target

    def cut_len(self):
        return sum(w for i, j, w in self.cut_edges
                   if self.assign[i] != self.assign[j])

    def flow_severed(self):
        """severed flow via municipal shares (exact closed form)."""
        S = self.mc.astype(float) / np.array(
            [self.muni_pop[m] for m in self.munis])[:, None]
        retain = (S @ S.T)
        return float((self.F * (1 - retain)).sum())

    def objective(self):
        dev = np.abs(self.dp / self.pbar - 1).max()
        fut = 0.0
        for y in self.future_years:
            pb = self.dpf[y].sum() / K
            fut = max(fut, np.abs(self.dpf[y] / pb - 1).max())
        return (self.w.get("pop", 1.0) * dev
                + self.w.get("compact", 0) * self.cut_len() / 1e6
                + self.w.get("split", 0) * self.n_split
                + self.w.get("flow", 0) * self.flow_severed() / 1e5
                + self.w.get("future", 0) * fut)

    def hard_ok(self):
        if np.abs(self.dp / self.pbar - 1).max() > self.tau:
            return False
        return not (self.boundary_on and bool(
                ((self.pref_cnt[:, 0] > 0) & (self.pref_cnt[:, 1] > 0)).any()))


def _apply(state, i, a, b):
    """Move unit i from district a to b, updating all incremental state."""
    mi = state.umidx[i]
    was_split = (state.mc[mi] > 0).sum() > 1
    state.mc[mi, a] -= 1
    state.mc[mi, b] += 1
    is_split = (state.mc[mi] > 0).sum() > 1
    state.n_split += int(is_split) - int(was_split)
    state.assign[i] = b
    state.dp[a] -= state.pop[i]
    state.dp[b] += state.pop[i]
    state.pref_cnt[a, state.pref[i] - 25] -= 1
    state.pref_cnt[b, state.pref[i] - 25] += 1
    for y in state.future_years:
        state.dpf[y][a] -= state.proj[y][i]
        state.dpf[y][b] += state.proj[y][i]


def _allowed(state, i, b):
    """boundary-ON rule for moving unit i into district b."""
    if not state.boundary_on:
        return True
    pc = state.pref[i] - 25
    return state.pref_cnt[b, 1 - pc] == 0


def greedy_repair(state: State, max_moves=20000):
    """Deterministic population repair: repeatedly flip the boundary unit that
    most reduces max |dev|, respecting contiguity + boundary constraint."""
    state._refresh_boundary()
    moves = 0
    stale = 0
    while moves < max_moves:
        devs = state.dp / state.pbar - 1
        order = np.argsort(-np.abs(devs))
        if abs(devs[order[0]]) <= state.tau:
            break
        base_dev = np.abs(devs).max()
        # try dev-violating districts worst-first; use the best improving flip found
        best = None
        used_di = None
        for di in order:
            if abs(devs[di]) <= state.tau:
                break
            over = devs[di] > 0
            cands = []
            for i in state.boundary_units:
                a = state.assign[i]
                if over:
                    if a != di:
                        continue
                    nbr = [state.assign[j] for j, _ in state.adj[i]
                           if state.assign[j] != a]
                    if not nbr:
                        continue
                    b = min(nbr, key=lambda d: state.dp[d])
                else:
                    if a == di or not any(state.assign[j] == di
                                          for j, _ in state.adj[i]):
                        continue
                    b = di
                cands.append((i, a, b))
            for i, a, b in cands:
                if not _allowed(state, i, b):
                    continue
                if not state.donor_connected(i, a):
                    continue
                d2 = state.dp.copy()
                d2[a] -= state.pop[i]
                d2[b] += state.pop[i]
                dv = np.abs(d2 / state.pbar - 1)
                key = (dv.max(), dv[di])
                if best is None or key < best[0]:
                    best = (key, i, a, b, di)
            if best is not None and best[0][0] < base_dev - 1e-12:
                break  # strict global improvement found
        if best is None:
            break
        (gdev, ddev), i, a, b, used_di = best
        # accept strict improvement, or a plateau/worsening flip that reduces the
        # chosen district's |dev| (unlocks multi-unit transfers)
        if gdev < base_dev - 1e-12:
            stale = 0
        elif ddev < abs(devs[used_di]) - 1e-12 and stale < 50:
            stale += 1
        else:
            break
        _apply(state, i, a, b)
        moves += 1
        state._refresh_boundary()
    return moves


def _score(state: State):
    """Annealing score: feasibility repair dominates until dev <= tau."""
    dev = float(np.abs(state.dp / state.pbar - 1).max())
    if dev > state.tau:
        return 10.0 * dev
    return state.objective()


def anneal(state: State, seed: int, iters: int, t0=0.05, t1=0.002,
           min_change=False, base=None, log_every=20000):
    rng = np.random.default_rng(seed)
    cur = (float(state.pop[state.assign != base].sum()) if min_change
           else _score(state))
    best = cur
    best_assign = state.assign.copy()
    pop = state.pop
    n = state.n
    T0, T1 = t0, t1
    accept = 0
    for it in range(iters):
        if it % 4096 == 0:
            state._refresh_boundary()
        i = state.boundary_units[rng.integers(len(state.boundary_units))]
        a = state.assign[i]
        nbr_d = [j for j, _ in state.adj[i] if state.assign[j] != a]
        if not nbr_d:
            continue
        b = state.assign[rng.choice(nbr_d)]
        # boundary constraint
        if state.boundary_on:
            if state.pref[i] - 25 == 0 and state.pref_cnt[b, 1] > 0:
                continue
            if state.pref[i] - 25 == 1 and state.pref_cnt[b, 0] > 0:
                continue
        if not state.donor_connected(i, a):
            continue
        # apply
        state.assign[i] = b
        mi = state.umidx[i]
        was_split = (state.mc[mi] > 0).sum() > 1
        state.mc[mi, a] -= 1
        state.mc[mi, b] += 1
        is_split = (state.mc[mi] > 0).sum() > 1
        split_delta = int(is_split) - int(was_split)
        state.dp[a] -= pop[i]
        state.dp[b] += pop[i]
        state.pref_cnt[a, state.pref[i] - 25] -= 1
        state.pref_cnt[b, state.pref[i] - 25] += 1
        dpf_old = {y: (state.dpf[y][a], state.dpf[y][b]) for y in state.future_years}
        for y in state.future_years:
            state.dpf[y][a] -= state.proj[y][i]
            state.dpf[y][b] += state.proj[y][i]
        state.n_split += split_delta
        new = state.objective()
        if min_change:
            new = float((pop[state.assign != base]).sum())
        dev = float(np.abs(state.dp / state.pbar - 1).max())
        if dev > state.tau and not min_change:
            new = 10.0 * dev  # repair phase: population feasibility dominates
        elif min_change and dev > state.tau:
            new = 1e9 + 10.0 * dev  # M5: still enforce feasibility
        T = T0 * (T1 / T0) ** (it / iters)
        if new <= cur or rng.random() < np.exp(-(new - cur) / max(T, 1e-9)):
            cur = new
            accept += 1
            if new < best and state.hard_ok():
                best = new
                best_assign = state.assign.copy()
        else:
            # revert
            state.assign[i] = a
            state.mc[mi, a] += 1
            state.mc[mi, b] -= 1
            state.dp[a] += pop[i]
            state.dp[b] -= pop[i]
            state.pref_cnt[a, state.pref[i] - 25] += 1
            state.pref_cnt[b, state.pref[i] - 25] -= 1
            for y in state.future_years:
                state.dpf[y][a], state.dpf[y][b] = dpf_old[y]
            state.n_split -= split_delta
        if it % log_every == 0:
            print(f"it={it} T={T:.4f} obj={cur:.4f} best={best:.4f} acc={accept}")
    return best_assign, best


def contiguity_repair(assign, g, adj, boundary_on, pref):
    """Reassign units of non-largest district components to a neighboring
    district so every district is one connected component. For boundary_on,
    a unit of group c may only join districts without the other group."""
    assign = assign.copy()
    grp_cnt = None
    if boundary_on:
        grp_cnt = np.zeros((K, 2), dtype=int)
        for i, d in enumerate(assign):
            grp_cnt[d, pref[i] - 25] += 1
    for _ in range(64):  # outer passes
        changed = False
        for d in range(K):
            idx = [i for i in range(len(g)) if assign[i] == d]
            sset = set(idx)
            seen = set()
            comps = []
            for i in idx:
                if i in seen:
                    continue
                comp = []
                stack = [i]
                seen.add(i)
                while stack:
                    u = stack.pop()
                    comp.append(u)
                    for v, _ in adj[u]:
                        if v in sset and v not in seen:
                            seen.add(v)
                            stack.append(v)
                comps.append(comp)
            if len(comps) <= 1:
                continue
            comps.sort(key=len, reverse=True)
            for comp in comps[1:]:  # detach non-largest components
                # candidate receiving districts touching this component
                nbr_d = {assign[v] for u in comp for v, _ in adj[u]
                         if assign[v] != d}
                if not nbr_d:
                    continue
                target = min(nbr_d, key=lambda b: len(
                    [i for i in range(len(g)) if assign[i] == b]))
                for u in comp:
                    if boundary_on:
                        pc = pref[u] - 25
                        if grp_cnt[target, 1 - pc] > 0:
                            continue
                        grp_cnt[d, pc] -= 1
                        grp_cnt[target, pc] += 1
                    assign[u] = target
                    changed = True
        if not changed:
            break
    return assign


def run_levelB(model: str, boundary_on: bool, seed: int, tau=None, iters=60000,
               future=False, min_change=False, start_from_current=True,
               init_csv=None, init_assign_csv=None):
    tau = CFG["optimization"]["tau_primary"] if tau is None else tau
    weights = dict(CFG["optimization"]["weights_primary"])
    if future:
        weights["future"] = 0.3
    g = load_units("B")
    edges = adjacency_with_perimeter(g)
    d2i = {d: k for k, d in enumerate(DISTRICTS)}
    if init_assign_csv:
        # unit-level init (e.g. warm-start OFF from the best ON assignment)
        am = pd.read_csv(init_assign_csv, dtype={"unit_id": str})
        m2d = am.set_index("unit_id")["district"]
        a0 = g["unit_id"].astype(str).map(m2d).fillna(-1).to_numpy(dtype=int)
        if (a0 < 0).any():
            raise ValueError("init_assign_csv does not cover all units")
    elif init_csv:
        # multilevel init: Level A assignment mapped down via muni_code
        am = pd.read_csv(init_csv, dtype={"unit_id": str})
        m2d = am.set_index("unit_id")["district"]
        a0 = g["muni_code"].astype(str).map(m2d).fillna(-1).to_numpy(dtype=int)
        if (a0 < 0).any():
            raise ValueError("init_csv does not cover all municipalities")
    else:
        a0 = g["district"].map(d2i).to_numpy()
    # boundary OFF start: if start map violates OFF nothing; fine for both
    st = State(g, edges, a0, boundary_on, weights, tau,
               future_years=CFG["robustness"]["projection_years"] if future else [])
    t_start = time.time()
    n_rep = greedy_repair(st)
    print(f"greedy_repair moves={n_rep} dev={np.abs(st.dp/st.pbar-1).max():.4f}")
    best, best_obj = anneal(st, seed, iters, min_change=min_change,
                            base=a0)
    best = contiguity_repair(best, g, st.adj, boundary_on, st.pref)
    # canonical objective is computed on the FINAL (post-repair) assignment;
    # the annealing best may refer to a pre-repair intermediate solution.
    stf = State(g, edges, best, boundary_on, weights, tau,
                future_years=st.future_years, group=None)
    final_obj = stf.objective()
    res = metrics.evaluate(best, g, edges, label=f"B_{model}_{'on' if boundary_on else 'off'}")
    if min_change:
        res["reassigned_pop"] = float(st.pop[best != a0].sum())
        res["reassigned_units"] = int((best != a0).sum())
        res["reassigned_pop_frac"] = float(
            st.pop[best != a0].sum() / st.pop.sum())
    rec = {"model": model, "boundary_on": boundary_on, "tau": tau, "seed": seed,
           "greedy_repair_moves": int(n_rep),
           "iters": iters, "runtime_sec": time.time() - t_start,
           "best_objective": float(final_obj),
           "anneal_best_objective": best_obj,
           "solver": "simulated_annealing(heuristic)",
           "optimality": "heuristic-no-bound"}
    fn = MODELS / f"B_{model}_{'on' if boundary_on else 'off'}_tau{tau}_s{seed}.json"
    pd.DataFrame({"unit_id": g.unit_id, "district": best}).to_csv(
        MODELS / fn.name.replace(".json", "_assign.csv"), index=False)
    rec["metrics"] = {k: v for k, v in res.items()
                      if k not in ("district_pops", "polsby_popper",
                                   "district_perimeter_m", "district_area_km2")}
    rec["metrics"]["district_pops"] = res["district_pops"]
    rec["metrics"]["polsby_popper"] = res["polsby_popper"]
    fn.write_text(json.dumps(rec, ensure_ascii=False, indent=2, default=str))
    print(json.dumps({k: rec[k] for k in ("model", "boundary_on", "seed",
                                          "best_objective", "runtime_sec")},
                     indent=2))
    return best, rec
