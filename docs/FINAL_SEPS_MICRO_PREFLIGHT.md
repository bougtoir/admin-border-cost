# FINAL_SEPS_MICRO_PREFLIGHT

Date: 2026-10-02. Branch: devin/1790943487-seps-final-qc (follow-up to PR #575).
Deliverable: `submission_package_SEPS_FINAL_v3.zip`.
Scope: four targeted fixes only; canonical results unchanged (qc_report 36/36, pytest 5/5, ruff clean).

## 1. Abstract — "exact CP-SAT" wording
- OLD (abstract): "an exact CP-SAT formulation at municipality scale" was previously "exact CP-SAT on municipalities" →
- NEW: "an exact CP-SAT formulation at municipality scale" (formulation-exact retained; no implication the solve reached proven OPTIMAL).
- Methods §3.3 keeps the legitimate formulation-exact statement: "formulated exactly as a mixed-integer program and solved by CP-SAT (OR-Tools) to the reported solver status and bounds" — unchanged by design.
- Cover letter already compliant: "an exact CP-SAT mathematical formulation solved to the reported status and bounds".
- Grep over all artifacts: no "exact solution" / "solved exactly" / "exact optimization" / standalone "exact CP-SAT" remains anywhere.

## 2. Highlights — placebo feasibility wording
- OLD: "Most placebo borders admit no feasible constrained map at the same tolerance."
- NEW: "No feasible constrained incumbent was found for 122 of 200 placebo borders." (75 chars, ≤85)
- Abstract aligned in the same pass: OLD "61% of placebo borders admit no feasible map at the same tolerance" → NEW "no feasible constrained incumbent was found for 122 of 200 placebo borders at the same tolerance" (count injected via new `{{placebo_n_infeasible}}` token = 122, computed in `src/report/aggregate_results.py` from `outputs/placebo/placebo_results.csv` — not hardcoded).
- §4.4 body aligned: "yielded no feasible constrained map" → "returned no feasible constrained incumbent" (the surrounding "no-incumbent-found outcomes, not proven infeasibility" framing unchanged).
- No artifact converts "no incumbent found" into proven infeasibility (grep-verified across manuscript, cover letter, highlights, README).

## 3. Cover letter — single-author voice
Authorship metadata: the repository carries no author list/affiliation anywhere; the manuscript is the sole-author work of Tatsuki Onishi (submission identity). Cover letter corrected to first-person singular:
- "We submit" → "I submit"
- "Our central claim" → "The central claim"
- "We estimate" → "I estimate"
- "we obtain a counterintuitive result" → "the manuscript obtains a counterintuitive result"
- "We are explicit that the study" → "The study is explicit that it"
- "We believe the manuscript fits" → "I believe the manuscript fits"
- "all authors approve its submission" → "the sole author approves its submission"
SEPS-specific scientific argument retained verbatim (constraint-to-be-priced framing, resource-scarcity reading, "mismatch is observable; inefficiency must be demonstrated", 39,733/99,420/122-of-200 evidence). Not shortened.

## 4. OMML visual verification
Both docx rendered to PDF (LibreOffice) and inspected page by page again after the edits. Verified rendered objects: C_border = L*(Boundary ON) − L*(Boundary OFF) in the paired-estimand sentence (abstract + §3.3), ±τ / τ = 20% / 10-15-30% / ±20% / ±10% / ±50% / 10× (methods, placebo, sensitivity), D_s* = argmin_D L_s(D) and C_s(B) = L_s*(B) − L_s*(0) ≥ 0 (§2), F_B ⊂ F_0, L*_OFF ≤ L*_ON, s ∈ {1, …, S}, max|dev|, max/min (§3.5), bare L_s, C(B), F_0, F_B (§2–3), cover-letter C_border. No blanks, no clipping, no raw LaTeX, stars attach to L*/D_s*, subscripts ON/OFF correct, Greek renders. Line heights normal.
Defect found and fixed during this pass: year values 2040 rendered as "2,040" by the thousands-separator formatter in both builders → `val()` now emits year-range integers (1900–2100) without commas. Re-verified in PDF: "breaches τ in 2040".

## 5. Canonical numbers
Unchanged — no solver/simulation rerun; only `aggregate_results.py` gained the `placebo_n_infeasible` (122) derived key from the existing placebo CSV. All prose tokens resolve; manuscript_values.csv regenerated from existing outputs.

## 6. Typography / asterisks / styles
`normalize_styles` unchanged and applied in all builders: TNR (all four rFonts slots, theme attrs stripped), black, 12 pt body, 10 pt captions. Asterisk re-scan: manuscript 0, cover letter 0, highlights 0; inline docx retains only the 2 documented file-glob wildcards in Table 1 (`r2ka_*.zip`, `od_*.xlsx`).

## 7. Supplement
Still absent from the journal package (S1–S8 in reproducibility bundle / main text). No supplement references reintroduced.

## 8. Figure/table order
First-citation order verified in rebuilt text: Figures 1→7 and Tables 1→6 strictly increasing; inline docx embeds each object after its first-citation paragraph; no orphans; no supplement numbering residue.

## 9. Final files
- `manuscript/manuscript.docx` (clean manuscript)
- `submission_package_SEPS_FINAL_v3/manuscript_inline_SEPS_FINAL.docx`
- `submission_package_SEPS_FINAL_v3/cover_letter_SEPS_FINAL.docx`
- `submission_package_SEPS_FINAL_v3/highlights.docx`
- `submission_package_SEPS_FINAL_v3.zip` (23 files; figures/ F1–F7, tables/ T1–T6b, DECLARATIONS.md, CLAIM_EVIDENCE_MATRIX.csv, README.md)
- `reproducibility_bundle_FULL.zip` unchanged (still complete; no package-sync change needed)
- This report: `docs/FINAL_SEPS_MICRO_PREFLIGHT.md`

## Gates
[x] no proven-optimum implication anywhere; [x] "exact" modifies formulation only;
[x] 122/200 = no-feasible-incumbent-found everywhere; [x] cover letter singular "I";
[x] SEPS motivation retained; [x] OMML objects render correctly;
[x] no raw LaTeX/broken equations; [x] no stray asterisks;
[x] TNR/12 pt/10 pt captions/black preserved; [x] supplement stays removed;
[x] no canonical number changed; [x] v3 ZIP regenerated.
