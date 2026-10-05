# FINAL_SEPS_PRESENTATION_QC

Date: 2026-10-02. Branch: devin/1790943487-seps-final-qc.
Deliverable: `submission_package_SEPS_FINAL_v2.zip` (journal-facing package, no supplement file).
Canonical results unchanged (qc_report: 36/36 checks pass; pytest 5/5; ruff clean).

## 1. Cover-letter strengthening
`manuscript/cover_letter.md` rewritten for an editor-facing scientific argument:
- "122 of 200 matched placebo borders produced no feasible constrained incumbent" (never "infeasible").
- "an exact CP-SAT mathematical formulation solved to the reported solver status and bounds" (never "exact CP-SAT solution").
- Editorial lines retained: "Mismatch is observable; inefficiency must be demonstrated." / "Alignment should be priced, not presumed."
- Authorship: repository carries no author name/affiliation; the letter uses "We submit" + "Corresponding author" rather than inventing identities (single authorship unverifiable → plural-neutral wording kept).
- Built to `cover_letter_SEPS_FINAL.docx`.

## 2. Supplement consolidation
S1–S8 classified: every item is either already integrated in the main text (resilience checks, ±20% tolerance rationale, MAUP discussion) or belongs in the reproducibility bundle (seed replicates, per-seed tables, solver diagnostics, sensitivity tables).
Decision: **no supplement.docx in the journal package**. `manuscript/supplement.md` stays in the repo and ships inside `reproducibility_bundle_FULL.zip`; the in-text pointer now reads "(full sensitivity tables in the reproducibility bundle)". No dangling S-number references in manuscript or cover letter (grep-verified).

## 3. Global docx typography
New `normalize_styles(doc)` in `src/report/docx_rich.py` rewrites the underlying style definitions (Normal, Title, Subtitle, Heading 1–3, Caption, Hyperlink, FollowedHyperlink): Times New Roman on all four rFonts slots (ascii/hAnsi/eastAsia/cs), theme-font attributes stripped, black #000000 with theme-color attributes removed, 12 pt body, 10 pt captions, bold headings. Wired into build_manuscript, build_inline_docx, build_cover_letter, build_supplement, and the new build_highlights. Table text renders at 12 pt (within the 10–12 pt band). Verified visually — no theme-blue remains.

## 4. Asterisk audit
Scanned every paragraph and table cell of manuscript.docx, manuscript_inline.docx, cover_letter.docx, highlights.docx:
- manuscript.docx: **0** literal asterisks.
- cover_letter.docx: **0**. highlights.docx: **0**.
- manuscript_inline.docx: **2**, both glob wildcards inside file-path strings in Table 1 (`data/raw/r2ka_*.zip`, `data/raw/od_*.xlsx`) — retained, scientifically necessary path patterns, not markdown residue.
- All optimum stars (`L*`, `D_s*`, `L*_OFF`, `L*_ON`) are inside OMML equations, not text asterisks.

## 5. Native equations (OMML)
All substantive math converts to Word-native OMML via latex2mathml → docx_equation: C_border, L*(Boundary ON/OFF), ±τ, ±20%, ±10%, ±50%, 10×, max|dev|, max/min, D_s* = argmin_D L_s(D), C_s(B) = L_s*(B) − L_s*(0) ≥ 0, F_B ⊂ F_0, L*_OFF ≤ L*_ON, s ∈ {1, …, S}, C(B), F_0, F_B, L_s, x-sums. Counts: manuscript 39 OMML / inline 37 / cover letter 1 (the C_border estimand). Semantic spot-audit on rendered pages: equations correct and legible; prose numbers (300 s, 60 s, 39,733, percentiles) correctly left as text.

## 6. Visual QC
All four docx rendered to PDF via LibreOffice and inspected page by page (manuscript 11 pp, inline 18 pp, cover letter 2 pp, highlights 1 p): equations visible and correct, no missing symbols, serif TNR throughout including headings, all-black text, no stray asterisks, figures uncropped, captions at 10 pt beside their objects, no broken page breaks.

## 7. Claim consistency
- Level A: FEASIBLE not OPTIMAL; cost stated only as interval [0, 532,293] (~30% of incumbent scale); wrong-sign incumbent diff flagged as search artifact.
- Level B zero = "best-found difference", explicitly not a proven optimum.
- 122/200 = "no feasible constrained incumbent", never infeasibility.
- Watershed = associative framing ("consistent with"), no causal claim.
- Scarcity = stated as principle; ±20% = experimental design parameter, not legal judgment.
- Fixed one factual slip found during visual QC: §4.4 had "61% (78 feasible of 200)" — the parenthetical mixed share and feasible count; now "61% (122 of 200)".

## 8. Figure/table citation order
First-citation order verified in built text: Figures 1→2→3→4→5→6→7, Tables 1→2→3→4→5→6 strictly increasing. Inline docx embeds each object immediately after its first-citation paragraph with a preceding caption.

## 9. References
All 15 entries verified against live metadata during the SEPS retarget pass (DOIs checked). Every in-text citation [1]–[15] maps to an entry and every entry is cited; first-appearance order is exactly 1→15 (elsarticle-num compliant).

## 10. Current SEPS guide re-check
Re-checked 2026-10-02 (Wayback copy of the live Elsevier guide; ScienceDirect blocked by Cloudflare): single anonymized review, "Your Paper Your Way" (no word limit), concise factual abstract, ≤6 keywords, highlights where applicable (ours ≤85 chars), numbered sections, numbered references in order of appearance, declarations for interest/funding/AI/data. Package conforms; no overrides needed.

## 11. Reproducibility bundle
`reproducibility_bundle_FULL.zip` unchanged and complete: source code, configs, tests, solver diagnostics, seeds, provenance manifests, manuscript_values.csv, lock files, REPRODUCIBILITY.md, plus manuscript/supplement.md (the consolidated supplement detail). `data/raw/` restored from the bundle to re-verify the SHA-256 manifest before this pass.

## 12–14. Final files, package, gates
- `submission_package_SEPS_FINAL_v2.zip`: manuscript.docx, manuscript_inline_SEPS_FINAL.docx, cover_letter_SEPS_FINAL.docx, highlights.docx, DECLARATIONS.md, CLAIM_EVIDENCE_MATRIX.csv, README.md, figures/ F1–F7, tables/ T1–T6(+T6b). No supplement (per §2).
- Regenerated reproducibility_bundle_FULL.zip left in place.
- Gates: QC 36/36 pass, pytest 5/5 pass, ruff clean, visual QC pass, asterisk audit pass (2 documented glob wildcards only), citation-order pass, reference cross-check pass.
