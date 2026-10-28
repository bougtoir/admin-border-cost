# PMR Kyoto–Shiga — Additional-Analysis Results Summary

Date: 2026-10-06 (UTC). One row per function, per the collection prompt
§5. Only actual completed outputs are reported; planned analyses are
labelled as such — nothing is fabricated.

## Cross-function table

| Function | Boundary ON result | Boundary OFF result | Boundary cost / difference | Access effect | Equity effect | Solver status | Interpretation |
|---|---|---|---|---|---|---|---|
| Electoral representation | M2-ON incumbent 1,793,321 (bound 883,334) | M3-OFF incumbent 1,870,325 | True cost bounded [0, 532,293] (Level A); best-found difference 0 (Level B) | Real border cross-flow 39,733 < all 200 placebos; OFF severed flow ≈ same | Not an equity outcome — population-equality constraint held | Level A: FEASIBLE (not OPTIMAL); Level B: heuristic best-found | Constraint cheap inside representation |
| Healthcare access | NOT COMPLETED | NOT COMPLETED | NOT YET ESTIMATED | — | — | no run | Supply data (MLIT P04) not yet acquired; analysis frozen, not executed |
| Education access | NOT COMPLETED | NOT COMPLETED | NOT YET ESTIMATED | — | — | no run | Supply data acquired (MLIT P29; 572 open elementary / 262 open junior-high points); solver not yet run |

## Central PMR hypothesis status

Whether the same Kyoto–Shiga boundary carries different opportunity
costs for different functions: **NOT YET TESTABLE** — electoral
representation is validated; healthcare and education have no completed
runs (education has acquired supply data only). No support is claimed in
either direction.

## Notes

- Electoral figures are canonical validated results
  (`manuscript/manuscript_values.csv`; `docs/CLAIM_EVIDENCE_MATRIX.csv`),
  reported as bounds/best-found, never as proven optima.
- Function definitions, ON/OFF formulations, outcomes, equity metrics,
  resource assumptions and sensitivity sets for F1/F2 are pre-specified
  in `docs/PMR_KYOTO_SHIGA_ANALYSIS_FREEZE.md` and will produce the
  columns above once executed.
