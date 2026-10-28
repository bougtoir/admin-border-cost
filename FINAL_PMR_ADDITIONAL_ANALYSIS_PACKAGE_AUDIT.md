# FINAL PMR Additional-Analysis Package Audit

Date: 2026-10-06 (UTC).

1. **Healthcare analysis completed?** NO — NOT FOUND / NOT COMPLETED.
   Frozen design exists; supply data (MLIT P04) not acquired; no solver
   run, outputs, or logs exist.
2. **Education analysis completed?** NO — NOT COMPLETED. Supply data
   acquired and processed (MLIT P29 → `data/processed/pmr_education_access/`),
   but the pre-specified ON/OFF assignment was never run; no result
   artifacts exist.
3. **Source paths searched.** Repo-wide content search over
   `admin_border_cost/`: `src/`, `outputs/`, `data/processed/`,
   `submission_package*`, `docs/`, plus newer-than-manuscript file scan.
   Hits were all electoral-pipeline files and the P29 supply dataset —
   no healthcare/education analysis artifacts.
4. **Primary results.** Electoral (validated): Level A cost bounded
   [0, 532,293]; Level B best-found 0; cross-flow 39,733 < 200 placebos.
   F1/F2: none (no runs).
5. **Solver status.** Electoral: Level A FEASIBLE-not-OPTIMAL, Level B
   heuristic best-found — reported as bounds, never proven optimum.
   F1/F2: n/a.
6. **Sensitivity completeness.** None for F1/F2 (not run); the frozen
   sensitivity set is documented in the analysis freeze.
7. **Freeze compliance.** `docs/PMR_KYOTO_SHIGA_ANALYSIS_FREEZE_COMPLIANCE.md`:
   one pre-outcome protocol amendment (F2 per-level split); zero
   post-hoc changes.
8. **Data provenance completeness.** P29 acquisition fully ledgered
   (URL, version, retrieval UTC, SHA-256, coverage, variables,
   transformations) in `docs/PMR_KYOTO_SHIGA_NEW_DATA_PROVENANCE_FINAL.md`
   and `data/raw/SHA256SUMS.txt`.
9. **Contamination scan.** PASS — see
   `docs/PMR_CROSS_PROJECT_CONTAMINATION_CHECK.md`.
10. **Abstract/email updated?** Not needed — both correctly describe the
    extensions as planned; sync audit in
    `docs/PMR_ABSTRACT_RESULT_SYNC_AUDIT.md`.
11. **ZIP path.** `admin_border_cost/PMR_KYOTO_SHIGA_ADDITIONAL_ANALYSES_FULL.zip`.

## Gate

- [x] healthcare status resolved → NOT COMPLETED
- [x] education status resolved → NOT COMPLETED (supply data acquired)
- [x] all actual result files included (education supply data; no result files exist)
- [x] code/configs/logs included (builder script; no solver logs exist — documented)
- [x] provenance files included
- [x] cross-function summary exists
- [x] abstract/email status matches reality (planned = planned)
- [x] contamination scan passes
- [x] final ZIP created
