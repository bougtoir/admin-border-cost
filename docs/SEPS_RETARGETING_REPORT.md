# SEPS retargeting report (2026-10-02)

Scope: journal retargeting + conceptual reframing only. No analyses,
optimizations, placebos, figures, or table data were rerun or changed.
Canonical results and manuscript_values.csv are identical to the audited
Applied Geography package.

## Venue

Socio-Economic Planning Sciences (SEPS), "The International Journal of
Public Sector Decision-Making" (Elsevier; Editor-in-Chief Rajan Batta;
portal editorialmanager.com/SEPS). Official Guide for Authors consulted
2026-10-02 (archived copy; see docs/JOURNAL_REQUIREMENTS.md).

## Conceptual changes

- Central reframing: territorial alignment of public functions is a
  constrained-planning decision whose opportunity cost can be measured;
  mismatch is an observation, inefficiency an estimand. Multi-service
  extension labeled conceptual only.
- New Section 2 "Territorial alignment as a constrained planning problem":
  D_s* = argmin_D L_s(D); F_B ⊂ F_0; C_s(B) = L_s*(B) − L_s*(0) ≥ 0;
  three-way distinction between true optimum cost, Level-A bound
  interval, and Level-B best-found difference.
- New title signals the planning contribution while keeping the electoral
  application explicit.
- Discussion rewritten in four layers: empirical → mismatch-reform
  implication → general planning principle (calibrated, with
  resource-scarcity language and explicit disclaimer that transition/
  coordination costs are not estimated) → transferability flagged as
  future applications.
- Conclusion rewritten to end on the decision principle.
- Limitations expanded per SEPS prompt checklist (single function, one
  case, one flow dimension, declared weights, open Level-A gap, heuristic
  Level B, no-incumbent ≠ infeasible, no alignment-benefit estimation).
- New references added: Larson & Odoni (2007, Urban Operations Research,
  Dynamic Ideas) and Owen & Daskin (1998, EJOR 111(3):423–447,
  doi:10.1016/S0377-2217(98)00186-6) — both verified against publisher/
  catalog listings. No other references added or removed; all carry-overs
  unchanged.

## Sections rewritten

Title, Highlights (≤85 chars each), Abstract, Keywords (≤6),
Introduction (full resequencing), new Section 2, Results lead paragraph
(reordered, results unchanged), Discussion, Limitations, Conclusion,
Declarations, References (converted to numbered elsarticle-num style,
numbered by first appearance [1]–[15]).

## Numerical results

UNCHANGED. Every figure, table, and number traces to the same run
artifacts via manuscript_values.csv. qc_report: 36/36 checks pass.
CLAIM_EVIDENCE_MATRIX extended with class column (A empirical,
B methodological implication, C conceptual generalization,
D future application).

## SEPS fit rationale

SEPS publishes quantitative public-sector decision-making; the paper now
prices a planning constraint rather than describing an electoral-
geography curiosity. See docs/SEPS_TARGETING_NOTES.md.

## Hostile-review pass

- SEPS-editor concern (electoral-geography retitle): mitigated by leading
  framing, Section 2 formalism, planning-first intro/discussion.
- OR concern (constraint cost meaningful under incomplete optimization):
  estimand vs bound vs best-found explicitly distinguished throughout.
- Overgeneralization: health/schools/etc. appear only as labeled
  future-application examples; claim discipline enforced (no "mismatch
  is efficient" type claims).
- Spatial concern: MAUP bounded at two resolutions; watershed language
  stays associative ("consistent with").
- Reproducibility: full bundle preserved; raw data + SHA-256 ledger
  restored locally (data/raw, gitignored but present).

## Applied Geography residue

None in manuscript, cover letter, supplement, or package. Historical
reports and the superseded guideline section retain mentions by design.

## Final file paths

- manuscript/manuscript_text.md, manuscript.docx, manuscript_inline.docx
- manuscript/supplement.md, supplement.docx
- manuscript/cover_letter.md, cover_letter.docx, highlights.docx
- docs/JOURNAL_REQUIREMENTS.md, SEPS_TARGETING_NOTES.md,
  SEPS_RETARGETING_REPORT.md, CLAIM_EVIDENCE_MATRIX.csv
- submission_package_SEPS/ and submission_package_SEPS_FINAL.zip
- reproducibility_bundle_FULL.zip (pre-existing, preserved)
