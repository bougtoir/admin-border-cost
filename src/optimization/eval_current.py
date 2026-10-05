"""M0: evaluate the current statutory map at both levels -> models JSONs."""
import json
from pathlib import Path

import yaml

from . import metrics
from .model_data import DISTRICTS, adjacency_with_perimeter, load_units

ROOT = Path(__file__).resolve().parents[2]
MODELS = ROOT / "outputs/models"
MODELS.mkdir(exist_ok=True)
TAU = yaml.safe_load((ROOT / "config/config.yaml").read_text())[
    "optimization"]["tau_primary"]


def main():
    for level in ("A", "B"):
        g = load_units(level).reset_index(drop=True)
        e = adjacency_with_perimeter(g)
        a = g["district"].map({d: k for k, d in enumerate(DISTRICTS)}).values
        res = metrics.evaluate(a, g, e, label=f"{level}_M0_current")
        rec = {"model": "M0", "boundary_on": True, "tau": TAU, "seed": None,
               "status": "CURRENT-MAP", "solver": "none",
               "optimality": "n/a (statutory map)"}
        rec["metrics"] = {k: v for k, v in res.items()
                          if k not in ("district_pops", "polsby_popper",
                                       "district_perimeter_m",
                                       "district_area_km2")}
        rec["metrics"]["district_pops"] = res["district_pops"]
        rec["metrics"]["polsby_popper"] = res["polsby_popper"]
        (MODELS / f"{level}_M0_on_tau{TAU}_s0.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2, default=str))
        print(level, "contig", res["contiguous"], "maxdev",
              round(res["max_rel_dev"], 3))


if __name__ == "__main__":
    main()
