# FINAL REVISION REPORT — Administrative-border constraint cost (Kyoto–Shiga)

## 1. Scope of revision
Full forensic audit and revision of the Applied Geography submission package per
`Applied_Geography_final_revision_Devin_prompt.txt` phases 0–17. Trigger: eight
flagged integrity risks including mathematically invalid negative "constraint
costs", a table/text discrepancy, suspicious equalities in the future table, and
a missing code bundle.

## 2. Forensic freeze (Phase 0)
- `docs/PRE_REVISION_FORENSIC_SNAPSHOT.md`: pipeline state, commit, file census.
- `audit/pre_revision/SHA256_snapshot.txt`: SHA-256 for 211 files.
- `audit/pre_revision/`: verbatim copies of all model JSONs, placebo outputs,
  manuscript_values.csv before any edit.
- `audit/FORENSIC_ISSUE_LEDGER.csv`: R1–R8 with reproduction status, root cause,
  classification, fix, post-fix status.

## 3. Pipeline trace (Phase 1)
`docs/PIPELINE_TRACE.md` documents every stage from raw official inputs
(e-Stat GIS, Census Table 6-1, IPSS, e-Gov statute XML) to every reported value.

## 4. Mathematical invariants (Phase 2)
`tests/test_invariants.py` implements I1–I8 (independent Level-A objective
re-evaluation, contiguity, no-mixed-districts on ON maps, evaluator/log
agreement, nesting `L*_OFF ≤ L*_ON`). All pass:
- I3: independent evaluator reproduces every recorded Level-A objective exactly →
  no objective mismatch.
- I8: the ON assignment is verified OFF-feasible (0 mixed districts) and scores
  the same under the OFF objective → OFF optimum ≤ ON incumbent.

## 5. Level A audit (Phase 3)
Root cause of the −77,004 "cost": CP-SAT returned FEASIBLE incumbents, not
optima (gaps 0.49 ON / 0.33 OFF at 300 s). A nested minimization cannot yield
negative cost — the difference between two finite-time incumbents is a search
artifact. An OFF rerun warm-started from the ON incumbent at 900 s still
returned UNKNOWN (no incumbent), so the OFF optimum is not tightly identified.
Corrected reporting: **interval [0, 532,293] objective units** (≤ 29.7% of the
incumbent scale), never a negative point estimate. See
`src/audit/nested_off_cpsat.py`, `outputs/models/A_M3_off_tau0.2_s11_nested.json`.

## 6. Level B audit (Phase 4)
Real defect found: `best_objective` recorded a pre-`contiguity_repair`
intermediate value. Fixed at source (`run_levelB` now recomputes the canonical
objective on the final assignment and stores both `final_objective` and
`anneal_best_objective`) and back-filled into all `outputs/models/B_*.json`.
OFF was additionally warm-started from the ON map (`init_assign_csv`): the
retained best is identical (0.624529) → **Cost_border(B) = 0** on corrected
accounting.

## 7. Objective/Pareto audit (Phase 5)
`outputs/tables/objective_definition.csv` records exact term weights, scaling
and units for each level/model; the boundary flag enters only the constraint
set, never the objective.

## 8. Placebo audit (Phase 6)
Per-border records retained in `outputs/placebo/placebo_results.csv`. The 122
"infeasible" cases are *no-incumbent-found* (HEUR-INFEASIBLE), never encoded as
zero cost — cost statistics use feasible pairs only. Diagnostic reruns at up to
10× iteration budget on a 12-border sample recovered 0/12 → consistent with
structural infeasibility, reported as such, not proven. Table T5 previously
rendered all cost stats as 0 due to a `:.0f` format bug — fixed; T5 now lists
n, n feasible (78), n no-incumbent (122), median/IQR/p5–p95.

## 9. Future-model audit (Phase 7)
`outputs/tables/future_assignment_audit.csv`: assignment hashes prove identical
values across rows are genuinely identical maps (contiguity repair converges
different anneal outputs to the same repaired map). Not copy artifacts.

## 10. Current-map verification (Phase 8)
Statutory map reconstructed on 2020 small-area census shows max|dev| = 0.371 —
a reconstruction property, not a legal judgment (apportionment basis/vintage
differs). Manuscript §3.1 reworded explicitly.

## 11. Watershed quantification (Phase 9)
New evidence `outputs/placebo/cross_od.csv` + `cross_od_real.json`: the real
border crosses 39,733 daily commuting/schooling trips; median matched placebo
border crosses 99,420 → real border at the **0th percentile**. Claim softened
to functional/topographic alignment consistent with the Lake Biwa watershed.

## 12. Targeted reanalysis (Phase 10)
Only demonstrated defects were fixed: B objective accounting, T5 formatting,
manuscript wording, interval reporting. No solver parameters, constraints, or
data were touched. All downstream artifacts regenerated from corrected inputs.

## 13. Hostile review (Phase 11)
- No negative cost is reported anywhere as a substantive estimate; the raw
  incumbent difference is shown once, explicitly labeled a search artifact.
- "Infeasible" phrasing removed everywhere in favor of no-incumbent-found.
- No OPTIMAL claim where status is FEASIBLE; bounds reported.
- Negative lower tail of the placebo cost distribution flagged as the same
  incumbent-time artifact class.

## 14. Manuscript rewrite (Phase 12) + numerical integrity (Phase 13)
Abstract (238 words), highlights, §3.1–3.3, discussion, conclusion rewritten
to the corrected evidence. `manuscript_values.csv` now carries the full schema
(value_id, display_value, raw_value, units, source_file, source_columns,
analysis_step, figure_table_reference, manuscript_location). DOIs: all five
listed DOIs resolve (200/redirect); Balinski & Young, Openshaw & Taylor, and
Polsby & Popper legitimately have no DOI (book/chapter/law-review).

## 15. Reproducibility + packaging (Phases 14–17)
- Report pipeline rebuilt clean from raw model JSONs + processed data
  (`aggregate → tables → figures → manuscript → qc`); QC 36/36 pass;
  invariants I1–I8 pass; ruff clean.
- Full solver recompute (CP-SAT + SA + placebo, ~10 h) was not re-run since
  defects were downstream of raw solver outputs; pipeline remains
  `make all`-reproducible.
- `submission_package_applied_geography_FINAL.zip`: manuscript.docx,
  manuscript_inline.docx, supplement.docx, cover_letter.docx, F1–F7 PNG,
  T1–T6 CSV, CLAIM_EVIDENCE_MATRIX, JOURNAL_REQUIREMENTS, manuscript_values.
- `reproducibility_bundle_FULL.zip` (57 MB, 328 files): full `src/` + `tests/`
  (incl. invariants + audit modules), config, Makefile, requirements.txt +
  env_lock.txt, raw data + `data/raw/SHA256SUMS.txt` + retrieval code,
  processed data, all model JSONs + assignment CSVs + nested-audit outputs,
  placebo raw results, future assignment audit, manuscript_values, QC report,
  claim matrix, methods/limitations docs, audit ledger + pre-revision snapshot.
