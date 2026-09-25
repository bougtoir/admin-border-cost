# METHODS_DECISIONS — frozen protocol (pre-analysis, 2026-09-24)

Frozen before outcome-driven tuning. Changes after first results are logged in
`docs/CHANGELOG_PROTOCOL.md` with reason and timestamp.

## 1. Estimand
Cost_border = L\*(Boundary ON) − L\*(Boundary OFF), for each objective L,
with otherwise identical constraint sets, unit graph, seed bank, and solver budget.
Boundary ON: no district may contain units from both Kyoto-fu (26) and Shiga-ken (25).
Boundary OFF removes only that restriction.

## 2. Unit geography
- Level A (prototype + MAUP lower tier): municipalities + Kyoto-city wards. 45 units
  (Shiga 19 municipalities; Kyoto 15 municipalities + 11 wards).
- Level B (primary): census small areas (小地域, r2ka). ≈2,800 (Shiga) + ≈5,000 (Kyoto).
  Optimization runs on contiguous multi-scale blocks when exact CP-SAT is infeasible;
  final solutions are always validated at small-area level.
- OD (flow) geography: municipality/ward pair (census Table 6-1 resolution).
- Projection geography: municipality (IPSS). Downscaling to units documented in §7.

## 3. Constraints (primary set)
- Assignment: every unit exactly one district; K = 9 districts.
- Contiguity: mandatory (queen adjacency; islands documented — none expected on the
  mainland units; isolated census units joined to nearest unit are recorded).
- Population: max relative deviation |P_d/P̄ − 1| ≤ τ. Primary τ = 0.20
  (pre-declared: stricter than the informal ~2.0 max/min-ratio convention used by the
  Districting Council, looser than exact equality; sensitivity τ ∈ {0.10, 0.15, 0.30}).
- Boundary ON/OFF as defined above.
- Municipality non-split: soft penalty L_split (primary); hard version as sensitivity.

## 4. Objectives
- L_pop: max relative deviation from P̄ (also report max/min, MAD, RMS).
- L_compact: mean Polsby–Ppopper per district (primary); Reock/convex-hull and
  perimeter-based alternative as sensitivity.
- L_split: #split municipalities + population affected.
- L_flow: Σ F_ij·I(d_i≠d_j) over symmetric normalized flows.
  Primary F_ij = (C_ij + C_ji)/2 (raw symmetric counts; normalization invariance
  noted for severed-fraction reporting). Alternatives: origin-normalized,
  population-symmetrized. Municipal OD allocated to units proportionally to
  P_i·P_j/(P_m·P_n).
- L_future: max_{t,s,d} |P_{d,t,s}/P̄_{t,s} − 1| over IPSS 5-year steps 2025–2050.
- L_change: population/units reassigned vs current map (M5 only).

## 5. Models
- M0 CURRENT: metrics on the statutory 9-district map (D1).
- M1 BASE: min L_pop, contiguity + τ.
- M2 ON: lexicographic — hard τ; then minimize w·[pop-dev, −compactness, split,
  severed-flow]; primary weights (1, 0.3, 0.3, 0.3) pre-declared; Pareto front by
  scalar weight sweeps (pre-declared grid, not outcome-tuned).
- M3 OFF: identical to M2 minus border constraint.
- M4 FUTURE: same as M2/M3 + robust objective; scenarios = IPSS municipality
  projections downscaled (primary: proportional-share; alt: uniform shift ±10%).
- M5 MIN-INTERVENTION: min reassigned population s.t. τ and contiguity.
- Placebo: N≥200 synthetic internal borders matched on #regions and approximate
  boundary complexity; empirical percentile of true-border cost.

## 6. Solver
- Level A: OR-Tools CP-SAT, single-commodity-flow contiguity (Shirabe) or
  rooted-cut lazy constraints; multiple seeds; report bound/gap/status/runtime.
- Level B: contiguous multi-scale coarsening → CP-SAT on blocks → local-search
  refinement at small-area level; validity re-checked at fine level.
- Never claim global optimality without a proven bound; report as
  proven-optimal / bounded / heuristic.

## 7. Downscaling & uncertainty
- IPSS municipal growth factor applied proportionally to each constituent small
  area's 2020 population (primary). Alternative scenario: differential intra-
  municipal drift (±10% linear gradient to newest development — implemented as
  centroid-distance-weighted perturbation), reported as sensitivity only.
- No invention of fine-scale forecasts: only municipal values scaled.

## 8. Stopping rules
- Primary findings = M2 vs M3 pair under frozen τ, weights, seed bank (n=8 seeds).
- No post-hoc re-weighting to alter the headline cost sign/magnitude.
- If solver budget (default 600 s/model/seed Level B) prevents optimality,
  report gap honestly rather than tighten tolerance for narrative.

## 9. Pre-declared primary outputs
- Cost_border for L_pop, L_compact, L_split, L_flow; Pareto fronts; future
  durability years; placebo percentile.
- Population figures use 2020 census small-area JINKO throughout.

## Addendum (build-session decisions, frozen)
- **Fragment merge**: r2ka stores some census small areas as multiple fragment
  rows (same KEY_CODE, detached parts). They are one official unit → merged
  (union geometry, summed population). 420 fragment rows → 11,978 units.
- **Shared-boundary tolerance**: prefecture borders in r2ka do not coincide
  exactly → shared lengths measured at 30 m tolerance; Level A edge weights
  are aggregates of small-area weights (consistent across levels).
- **Bridging**: 3 residual isolated components connected via recorded
  nearest-unit edges (geography_qc.json).
- **Level B feasibility**: deterministic `greedy_repair` before SA flips
  boundary units toward the violating district until dev ≤ τ; SA then polishes.
- **Level A hints**: M1 solution passed as CP-SAT hint to M2–M5 (constraints
  are identical across models; only objectives differ).
- **Placebo design**: random spanning-tree bipartitions, matched on pop share
  (±10%), interface boundary length (±50%), two-sided contiguity; cost =
  obj_ON − obj_OFF, 60 s limit per solve, Level A only (documented scope).
- **Estimand sign**: Cost_border = L*(ON) − L*(OFF), positive = constraint cost.

## Addendum 2 — placebo solve method and real-border pricing scale

- CP-SAT at 60 s per solve never found a feasible Level A solution
  (status UNKNOWN on both sides for all pilot borders). Placebo ON/OFF
  solves therefore use the same local-search machinery as Level B
  (greedy boundary-de-mixing repair, greedy population repair, simulated
  annealing) run on the Level A graph, with `group=` overriding the
  prefecture array so arbitrary two-group borders share the constraint
  code path. Costs are heuristic (no bound); reported accordingly.
- For the placebo percentile, the REAL border is re-priced with that same
  heuristic solver (`src/placebo/real_border_cost.py`, seeds 11/23/37,
  median reported) so the comparison is on one scale — the CP-SAT
  Level A objective is on a different integer scale and is never mixed
  into the placebo distribution.
- B-level post-pass `contiguity_repair` reassigns units of non-largest
  district components to the smallest adjacent district until every
  district is one component; all B outputs were repaired (15 runs, 1
  pocket each) and metrics re-evaluated.
- Result direction: cost_border is near zero / negative at both levels
  (within solver noise). The headline finding is that the real border is
  unusually benign — 61% of matched placebo borders are ON-infeasible at
  τ=0.20 and the real border's heuristic cost is at the 10th percentile
  of feasible placebo costs.
