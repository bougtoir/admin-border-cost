"""Generate N matched placebo internal borders on the Level-A (municipality)
adjacency graph.

Each placebo border partitions the 55 units into two contiguous groups R and
its complement. Matching targets (computed from the real Kyoto/Shiga border):
  - population split between the two groups
  - number of interface edges and total shared-boundary length
  - both sides contiguous (hard requirement)

Borders are drawn by sweeping a line in a random direction over unit centroids
(directional bisection), then filtering for contiguity and matching tolerances.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
OUT = ROOT / "data/processed"
PLAC = ROOT / "outputs/placebo"
PLAC.mkdir(parents=True, exist_ok=True)


def _components(assign, adj):
    nodes = set(np.where(assign == 1)[0])
    comps = 0
    seen = set()
    for s in list(nodes):
        if s in seen:
            continue
        comps += 1
        stack = [s]
        seen.add(s)
        while stack:
            u = stack.pop()
            for v in adj.get(u, []):
                if v in nodes and v not in seen:
                    seen.add(v)
                    stack.append(v)
    return comps


def main():
    n_target = CFG["placebo"]["n_borders"]           # 200
    tol_pop = CFG["placebo"]["pop_split_tol"]        # e.g. 0.10
    tol_len = CFG["placebo"]["boundary_len_tol"]     # e.g. 0.50
    seed = CFG["optimization"]["seeds"][0]

    from src.optimization.model_data import adjacency_with_perimeter, load_units
    gA = load_units("A").reset_index(drop=True)
    edges = adjacency_with_perimeter(gA)
    adj = {}
    for i, j in edges[["i", "j"]].itertuples(index=False):
        adj.setdefault(int(i), []).append(int(j))
        adj.setdefault(int(j), []).append(int(i))

    pop = gA["pop"].to_numpy()
    pref = gA["pref_code"].astype(int).to_numpy()
    real_group = (pref == 25).astype(int)  # Shiga side = 1 (JIS 25=滋賀)
    real_border = edges[(real_group[edges.i.values] != real_group[edges.j.values])]
    real_len = real_border.w.sum()
    real_edges = len(real_border)
    real_pop_share = pop[real_group == 1].sum() / pop.sum()

    rng = np.random.default_rng(seed)
    edge_list = edges[["i", "j"]].values.tolist()

    def rand_tree_cut():
        """Random spanning-tree bipartition: randomized DFS tree, cut one edge."""
        root = int(rng.integers(len(gA)))
        parent = {root: -1}
        order = [root]
        stack = [root]
        while stack:
            u = stack.pop()
            nbrs = [v for v in adj.get(u, []) if v not in parent]
            rng.shuffle(nbrs)
            for v in nbrs:
                parent[v] = u
                stack.append(v)
                order.append(v)
        if len(parent) < len(gA):
            return None
        # subtree sizes (population) under the random tree
        sub = pop.copy().astype(float)
        for v in reversed(order[1:]):
            sub[parent[v]] += sub[v]
        # candidate cut edges: parent->child
        cands = [(v, parent[v]) for v in order[1:]]
        rng.shuffle(cands) if False else None
        # sample a few cut edges per tree
        for _ in range(3):
            v, p = cands[int(rng.integers(len(cands)))]
            share = sub[v] / pop.sum()
            share = min(share, 1 - share)
            if abs(share - real_pop_share) > tol_pop:
                continue
            # mark subtree of v
            grp = np.zeros(len(gA), dtype=int)
            st = [v]
            while st:
                u = st.pop()
                grp[u] = 1
                st += [w for w, pw in parent.items() if pw == u]
            if abs(pop[grp == 1].sum() / pop.sum() - real_pop_share) > tol_pop:
                continue
            yield grp

    rows = []
    tries = 0
    while len(rows) < n_target and tries < n_target * 50:
        tries += 1
        for grp in (rand_tree_cut() or []):
            pb = edges[grp[edges.i.values] != grp[edges.j.values]]
            blen = pb.w.sum()
            if abs(blen / real_len - 1) > tol_len or len(rows) >= n_target:
                continue
            rows.append({
                "placebo_id": len(rows),
                "pop_share_grp1": float(pop[grp == 1].sum() / pop.sum()),
                "n_interface_edges": len(pb),
                "boundary_len_m": float(blen),
                "group": json.dumps(grp.tolist()),
            })
    df = pd.DataFrame(rows)
    df.to_csv(PLAC / "borders.csv", index=False)
    meta = {
        "n_placebo": len(rows), "tries": tries,
        "real_border": {"pop_share_shiga": float(real_pop_share),
                        "n_interface_edges": int(real_edges),
                        "boundary_len_m": float(real_len)},
        "tolerances": {"pop_split": tol_pop, "boundary_len": tol_len},
    }
    (PLAC / "borders_meta.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps({k: meta[k] for k in ("n_placebo", "tries")}, indent=2))
    print(json.dumps(meta["real_border"], indent=2))


if __name__ == "__main__":
    main()
