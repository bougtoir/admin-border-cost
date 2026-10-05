"""Batch driver: Level A models x seeds. Results -> outputs/models/*.json"""
import sys
from pathlib import Path

import pandas as pd
import yaml

from src.optimization.cpsat_levelA import run_levelA
from src.optimization.model_data import DISTRICTS

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
SEEDS = CFG["optimization"]["seeds"][:4]  # 4 seeds at Level A for runtime
TAUS = CFG["optimization"]["tau_sensitivity"]

jobs = []
# primary
for s in SEEDS:
    jobs += [("M1", True, None, s, False, False),
             ("M2", True, None, s, False, False),
             ("M3", False, None, s, False, False),
             ("M4", True, None, s, True, False),
             ("M4", False, None, s, True, False)]
# tau sensitivity for M2/M3 on primary seed
for t in TAUS:
    jobs += [("M2", True, t, SEEDS[0], False, False),
             ("M3", False, t, SEEDS[0], False, False)]
# M5 minimum intervention
jobs += [("M5", True, None, SEEDS[0], False, True)]

MODELS = ROOT / "outputs/models"
for model, on, tau, seed, fut, mc in jobs:
    try:
        tau_eff = CFG["optimization"]["tau_primary"] if tau is None else tau
        hintf = MODELS / f"A_M1_on_tau{tau_eff}_s{seed}_assign.csv"
        hint = (pd.read_csv(hintf).district.values
                if hintf.exists() and model != "M1" else None)
        run_levelA(model, on, tau=tau, seed=seed, future=fut, min_change=mc,
                   hint_assign=hint,
                   base_assign=None if not mc else
                   pd.read_csv(ROOT / "data/processed/muni_lookup.csv").district
                   .map({d: k for k, d in enumerate(DISTRICTS)}).values)
    except Exception as e:
        print("FAIL", model, on, tau, seed, repr(e), file=sys.stderr, flush=True)
