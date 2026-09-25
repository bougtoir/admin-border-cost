"""Batch driver: Level B models x seeds, warm-started from Level A maps.

Each job uses the matching Level A assignment (same model/boundary/tau/seed)
as its initial map via muni_code inheritance; falls back to M1 of the same
seed, then to the current map if no Level A file exists yet.
Results -> outputs/models/B_*.json + *_assign.csv
"""
import sys
from pathlib import Path

import yaml

from src.optimization.local_search_levelB import run_levelB

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
SEEDS = CFG["optimization"]["seeds"][:4]
TAUS = CFG["optimization"]["tau_sensitivity"]
MODELS = ROOT / "outputs/models"


def init_for(model, on, tau, seed):
    cands = [
        MODELS / f"A_{model}_{'on' if on else 'off'}_tau{tau}_s{seed}_assign.csv",
        MODELS / f"A_M1_on_tau{tau}_s{seed}_assign.csv",
        MODELS / f"A_M1_on_tau{CFG['optimization']['tau_primary']}_s{seed}_assign.csv",
    ]
    for c in cands:
        if c.exists():
            return str(c)
    return None


jobs = []
for s in SEEDS:
    jobs += [("M1", True, None, s, False, False),
             ("M2", True, None, s, False, False),
             ("M3", False, None, s, False, False),
             ("M4", True, None, s, True, False),
             ("M4", False, None, s, True, False)]
for t in TAUS:
    jobs += [("M2", True, t, SEEDS[0], False, False),
             ("M3", False, t, SEEDS[0], False, False)]
jobs += [("M5", True, None, SEEDS[0], False, True)]

ITERS = 120000
for model, on, tau, seed, fut, mc in jobs:
    tau_eff = CFG["optimization"]["tau_primary"] if tau is None else tau
    try:
        run_levelB(model, on, seed=seed, tau=tau, iters=ITERS, future=fut,
                   min_change=mc,
                   init_csv=None if mc else init_for(model, on, tau_eff, seed))
    except Exception as e:
        print("FAIL", model, on, tau, seed, repr(e), file=sys.stderr, flush=True)
