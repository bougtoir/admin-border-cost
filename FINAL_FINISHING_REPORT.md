# FINAL FINISHING REPORT — submission preflight pass

Target: Applied Geography. Scope: finishing pass only; no primary analyses re-run;
all canonical results preserved.

## 1. Wording/consistency changes made
- Highlights: "Exact (CP-SAT, municipality level)" → "Exact CP-SAT formulation
  (municipality level)"; "exactly zero at census small-area resolution" →
  "a best-found difference of zero".
- Methods §2.3: "Level A solves the problem exactly by CP-SAT" →
  "Level A is formulated exactly as a mixed-integer program and solved by CP-SAT
  to the reported solver status and bounds".
- Introduction: "two optimal maps" → "two maps".
- Results §3.2: "Cost_border(B) = 0" → "a best-found ON–OFF difference of 0",
  plus "removing the border constraint produces no improvement in the
  best-found small-area solution".
- Results §3.3: "consistent with structural infeasibility" → "persistent
  non-recovery under extended search, consistent with severe feasibility/search
  difficulty… but not a proof of mathematical infeasibility".
- Results §3.4: "ON-optimal map" → "ON best-found map".
- Discussion/Conclusion: "most matched alternative borders are either infeasible
  outright" → "admit no feasible constrained incumbent"; "permits a feasible map
  where most placebo lines cannot" → "yield no feasible incumbent".
- Figure list: "F3 optimal ON vs OFF maps" → "F3 best-found ON vs OFF maps";
  F3 caption in inline docx likewise; F6 annotation "ON-infeasible borders" →
  "borders with no feasible incumbent".
- Cover letter: "within solver noise" → "best-found cost is zero at small-area
  scale and bounded at municipality scale"; "infeasible or costlier" →
  "admit no feasible constrained incumbent or are costlier".
- Precision: template-value renderer fixed to format whole floats as integers
  with thousands separators (61.000% → 61%, 78.000 → 78) and other floats to
  3 decimals (532,293; 0.625; 0.371; 39,733); raw full-precision values remain
  only in machine-readable tables. (Previously mixed-type CSV reading rendered
  full machine precision into prose.)

## 2. Numerical results
No primary numerical result changed. All canonical values unchanged:
interval [0, 532,293] (Level A); best-found difference 0 (Level B);
placebo 200 / 78 feasible / 122 no-incumbent; median 0.0647, IQR 0.0222–0.0727;
cross-OD 39,733 vs placebo median 99,419.5 (0th percentile); real-border cost
10th percentile.

## 3. Level-A solver wording
"CP-SAT formulation … solved to the reported solver status and bounds";
Results report FEASIBLE (not OPTIMAL) incumbents with bound/gap and the
defensible interval [0, 532,293]. No global-optimality claim remains.

## 4. Level-B best-found wording
"best-found ON–OFF difference of 0"; "the constrained and unconstrained
best-found maps coincide"; heuristic SA labelled as such.

## 5. Placebo no-incumbent wording
"122 of 200 yielded no feasible constrained map — no-incumbent-found outcomes,
not proven infeasibility; persistent non-recovery under extended search…
not a proof of mathematical infeasibility." Consistent across Highlights,
Abstract, Results, cover letter, F6 annotation, T5 row label
("n ON-infeasible (no incumbent found)").

## 6. Watershed wording
"coincides with / largely coincides with the Lake Biwa watershed"; "consistent
with a real topographic divide"; supported quantitatively by cross-OD 0th
percentile. No causal claim.

## 7. QC/test outcome
- `qc_report`: 36/36 checks pass.
- `tests/test_invariants.py` I1–I8: all pass (independent evaluator reproduces
  every Level-A objective; ON assignment verified OFF-feasible).
- ruff: clean.

## 8. Applied Geography instruction check (current Guide for Authors)
- Abstract: 238 words ≤ 250, unstructured ✓
- Keywords: 7 ≤ 7 ✓
- References: APA 7th; all 5 listed DOIs resolve; book/chapter/law-review
  entries legitimately DOI-less ✓
- Figures/tables cited in first-appearance order; captions self-contained ✓
- Double-anonymized; no identifying info ✓
- Nonpartisan positioning retained; no electoral recommendation ✓
- NOTE: main text ~2,800 words incl. references — below the journal's stated
  4,500–8,000 range for research articles. Length was not padded in this pass
  (design unchanged); flagged for the author's decision.

## 9. Final artifact paths
- Manuscript: manuscript/manuscript.docx; inline-figure review copy:
  manuscript/manuscript_inline.docx; source: manuscript/manuscript_text.md
- Supplement: manuscript/supplement.docx; cover letter: manuscript/cover_letter.docx
- Submission ZIP: submission_package_applied_geography_FINAL.zip (22 files)
- Reproducibility bundle: reproducibility_bundle_FULL.zip (329 files, ~57 MB —
  src, tests incl. invariants/audit, config, Makefile, requirements.txt +
  env_lock.txt, raw+processed data with SHA256SUMS, all model JSONs/assignments
  incl. nested-audit runs, placebo raw, future audit, manuscript_values,
  QC report, claim matrix, methods/limitations, audit ledger, forensic snapshot)
