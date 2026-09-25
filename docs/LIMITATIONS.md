# Limitations and negative results

## Solver status
- Level A (CP-SAT, 55 units) reports FEASIBLE/OPTIMAL plus objective bound and gap;
  no global-optimality claim is made when gap > 0.
- Level B (11,978 units) is seeded simulated annealing — a heuristic with no bound.
  Results are medians/best over seeds, not optima.
- CP-SAT at Level A under τ=0.20 can be slow to find a first feasible solution;
  M1's solution is passed as a CP-SAT hint for M2–M5.

## Measurement approximations
- **Severed flow** at Level B uses the municipal-share closed form
  (a small area inherits its municipality's share of each OD pair) — exact only
  if flows distribute uniformly within municipalities. Level A flow cuts are
  exact at municipality granularity.
- **Compactness** uses shared-boundary length cut as objective and Polsby–Popper
  as the reported metric; boundaries across prefectures in r2ka do not coincide
  geometrically, so shared lengths use a 30 m tolerance (measured once,
  aggregated to municipalities).
- **Projections**: S1 downscales IPSS municipal growth proportionally to small
  areas; S2 adds ±10% centroid-drift sensitivity. Projections are scenario
  inputs, not forecasts with uncertainty bands.

## Geography preprocessing
- 420 small-area records are multi-polygon fragments of a single census unit
  (detached parts sharing KEY_CODE); they are merged into one unit with summed
  population — the official unit definition.
- 3 isolated components (islands/peninsulas) are connected by nearest-unit
  bridging edges, all recorded in `geography_qc.json`.
- The Kyoto–Shiga prefecture border measures ~118 km under the 30 m tolerance —
  sensitive to tolerance choice; sensitivity is reported in the supplement.

## Audit corrections (final revision)
- **Level A cost is an interval, not a point estimate.** CP-SAT runs are
  FEASIBLE (open gaps), and the OFF optimum resisted identification even at
  900 s of hinted search. Because the verified ON assignment is itself
  OFF-feasible, the OFF optimum is bounded above by the ON incumbent; the
  defensible interval for Cost_border(A) is [0, inc_ON − bound_OFF] =
  [0, 532,293] objective units. The earlier headline difference
  (inc_ON − inc_OFF = −77,004) violated the nesting invariant
  (L*_OFF ≤ L*_ON) and is a search artifact, not a cost.
- **Level B recorded objectives were pre-repair intermediate values.** The
  annealer's recorded "best" predated the contiguity-repair pass; objectives
  are now recomputed on the final contiguous assignments
  (`final_objective` vs `anneal_best_objective` in each model JSON). With
  corrected accounting, ON and OFF best-found maps coincide (cost = 0).
- **Placebo "infeasible" means no-incumbent-found**, not proven infeasibility.
  Diagnostic reruns at up to 10× iteration budget on a 12-border sample
  recovered none of them, consistent with structural infeasibility.
- **Future-series identical values are real**: assignment hashes show several
  seeds converge to the same map after repair, so equal metrics across rows
  are genuine shared solutions, not copy artifacts.

## Scope
- Nonpartisan by construction: no party, candidate, incumbent, vote share, or
  competitiveness variable exists anywhere in the pipeline.
- The placebo benchmark is statistical matching, not causal identification.
- Kyoto+Shiga is a deliberately hard case (border through a commuting field);
  costs will differ for rural borders — generalization requires replication.
