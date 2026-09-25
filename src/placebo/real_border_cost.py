"""Real prefecture border cost on the same heuristic solver/scale as the
placebo borders, so the placebo percentile is an apples-to-apples
comparison: writes outputs/placebo/real_border_cost.json."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from src.optimization.model_data import adjacency_with_perimeter, load_units
from src.placebo.run_placebo import solve_one_h

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())


def main():
    g = load_units("A").reset_index(drop=True)
    edges = adjacency_with_perimeter(g)
    m1 = pd.read_csv(ROOT / "outputs/models/A_M1_on_tau0.2_s11_assign.csv")
    dmap = {str(k): v for k, v in zip(m1.unit_id, m1.district)}
    a0 = np.array([dmap[u] for u in g.unit_id])
    grp = (g.pref_code.astype(int) == 25).astype(int).to_numpy()
    costs = {}
    for seed in CFG["optimization"]["seeds"][:3]:
        on = solve_one_h(g, edges, grp, True, seed, a0)
        off = solve_one_h(g, edges, grp, False, seed, a0)
        if on["objective"] is not None and off["objective"] is not None:
            costs[seed] = on["objective"] - off["objective"]
    out = {"costs": costs, "median": float(np.median(list(costs.values()))),
           "solver": "heuristic-no-bound (same as placebo solves)"}
    (ROOT / "outputs/placebo/real_border_cost.json").write_text(
        json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
