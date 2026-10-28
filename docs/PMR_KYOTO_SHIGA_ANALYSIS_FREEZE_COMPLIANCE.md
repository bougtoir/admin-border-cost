# PMR Kyoto–Shiga — Analysis-Freeze Compliance Report

Date: 2026-10-06 (UTC). Compares the frozen protocol
(`docs/PMR_KYOTO_SHIGA_FUNCTION_SELECTION_FREEZE.md`,
`docs/PMR_KYOTO_SHIGA_ANALYSIS_FREEZE.md`) against what was actually
executed.

## 1. Per-analysis compliance

| Analysis | Pre-specified? | Executed? | Changed vs freeze? | Why | Timing |
|---|---|---|---|---|---|
| F1 Healthcare access (ON/OFF nearest-facility assignment) | Yes (freeze §1–§8) | **No — NOT RUN** | n/a | Supply data (MLIT P04) not yet acquired; no solver run exists | — |
| F2 Education access (ON/OFF nearest-school assignment, per level) | Yes (freeze §1–§8, amended for per-level split after Devin Review) | **No — NOT RUN** | n/a | Supply data acquired (MLIT P29, 2021, Kyoto+Shiga school points); demand centroids and solver not yet run | — |
| Reference: electoral representation | Canonical (pre-existing validated pipeline) | Yes (prior validated runs) | No | — | Completed before this freeze |

## 2. Amendments after freeze

- F2 ON/OFF definition amended (2026-10-05) to require **per-level
  assignment** (elementary→elementary, junior-high→junior-high). Change
  made before any outcome existed — a protocol correction from Devin
  Review, not a post-hoc result-driven change. Frozen again.
- No exploratory or post-hoc analyses exist.

## 3. Consequence

No primary, secondary, or sensitivity result exists for F1 or F2. All
such results are PLANNED_NOT_COMPLETED. The central PMR hypothesis
(function-specific boundary cost) is **NOT YET TESTABLE**.
