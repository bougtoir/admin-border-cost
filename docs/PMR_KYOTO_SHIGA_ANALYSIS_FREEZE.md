# PMR Kyoto–Shiga Extension — Analysis Freeze

Date: 2026-10-05 (UTC). Status: **FROZEN before any new analysis.**
This document pre-specifies the two selected extension analyses
(healthcare access; education access) so that outcomes cannot be
reverse-engineered into the design. Nothing below has been computed.

## 1. Selected functions

- F1: Healthcare access (facility points, tiered by service level).
- F2: Education access (public elementary/junior-high school points).

Reference function (completed, for comparison only): electoral
representation (canonical study, `manuscript/manuscript_values.csv`).

## 2. Primary outcome (per function)

Population-weighted access cost under matched plans:

    Cost_border,s = L_s*(Boundary ON) − L_s*(Boundary OFF)

where L_s is the declared access objective and the Boundary ON plan is
required to assign every demand unit (census small-area population
centroid) only to facilities in the same prefecture; Boundary OFF removes
that restriction with all else held constant.

## 3. ON/OFF definitions

- **F1 ON:** small area served by nearest same-prefecture facility of the
  required tier (shortest path distance on the planar graph of facility
  points and small-area centroids; travel time via stated speed
  assumptions). **OFF:** nearest facility regardless of prefecture.
- **F2 ON:** elementary and junior-high levels are analysed separately —
  each small area is assigned to the nearest same-prefecture school *of
  the same level* (elementary-to-elementary, junior-high-to-junior-high).
  Pooling levels is invalid: a child cannot attend the other level's
  school, so a pooled assignment would not measure valid access cost.
  **OFF:** same per-level assignment ignoring the prefecture.

## 4. Constraints

- Every small area assigned (coverage hard constraint).
- F1: tier-specific analyses (primary care vs hospital tier) run
  separately; no cross-tier pooling.
- No capacity constraints in the primary specification (capacity-neutral
  proxy — declared limitation); a capacitated sensitivity is
  pre-specified below.

## 5. Equity metrics (pre-specified, all reported)

- Mean and max population-weighted access distance by prefecture.
- Share of population beyond distance thresholds (e.g., 5 km F2;
  thresholds fixed at data-inspection time and recorded before solving).
- Small-area disparity: worst-decile access gap between border-adjacent
  and interior areas.
- Municipal-split analogue: count of border municipalities whose optimal
  assignment crosses the line under OFF.

## 6. Resource/capacity assumptions

- Facilities used as-is from official point datasets; no
  opening/closure scenario in primary specification.
- Capacitated sensitivity: uniform per-facility capacity proportional to
  observed attributes (e.g., bed count for hospitals where present);
  treated as sensitivity, never as the headline.

## 7. Sensitivity analyses (pre-specified)

- Distance metric: geodesic vs network-proxy distance.
- Speed/travel-time assumptions where network time is used.
- Alternative small-area demand weights (total population vs
  age-restricted population for F2 — school-age population where official
  tabulations permit).
- τ-analogue: none needed (no population-equality constraint), but
  robustness to facility-tier definitions.

## 8. Interpretation rules

- Each function's Cost_border,s is reported as measured (bound or
  best-found as applicable, same honesty rules as the electoral study).
- Comparison across functions is descriptive (this is NOT a welfare
  ranking; different objectives are not commensurate).
- The core PMR hypothesis is supported descriptively if the sign or
  magnitude ordering of measured costs differs across functions;
  unsupported if identical or if data do not permit estimation.
- **Null/mixed results are retained.** A finding that healthcare and
  education costs are also ~zero is a reportable result, not a failure.
- No function is dropped post hoc; an infeasible data situation reverts
  the function to conceptual discussion and the paper falls back to the
  validated electoral example.
- Planned analyses are always labelled planned in abstracts, emails, and
  manuscripts until computed and QC'd.
