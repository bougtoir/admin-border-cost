# FINAL MATHEMATICAL NOTATION / OMML AUDIT — REPORT

Date: 2026-10-03 (UTC). Typography-only repair; no scientific content
changed. Token-by-token classification: docs/MATHEMATICAL_NOTATION_AUDIT.md.

## 1. Underscore occurrences before repair

Journal-facing DOCX (all four files): 6 distinct underscore tokens
before repair — 3 doc-path strings (CASE_SELECTION_*,
METHODS_DECISIONS) and 3 raw filenames (r2ka_*, od_*, ipss_kekkahyo1,
law_kosenkyoho) — all category C. Category A/B math underscores
existed only in source markdown prose (F_ij, F_ji, F_bi, R_ij, T_i,
P_i, P_j, R_ext, S2) and in T2–T7 CSV headers (flow_i_to_j,
flow_j_to_i, flow_bidirectional, R_i_to_j_pct, R_j_to_i_pct, S_pct,
splits, severed, tau), which the DOCX renderer had been printing
verbatim.

## 2. Mathematical underscore tokens found

F_ij, F_ji, F_bi, R_ij (=F_ij/T_i), R_ext, S2, S (=F_bi/(P_i+P_j)),
T_i, P_i, P_j — plus the T7 header row.

## 3. Tokens converted to OMML

All of the above via ordered rules in `src/report/docx_rich.py`:
F_{i→j}, F_{j→i}, F_{ij}^{bi}, R_{i→j}, R_{j→i}, R_{i→j}=F_{i→j}/T_i
(fraction), S_{ij}, S_{ij}=F_{ij}^{bi}/(P_i+P_j) (fraction), R_ext,
S_2, T_i, P_i, P_j; legacy F_ij/F_ji/F_bi/R_ij safety rules retained.

## 4. Machine-style table headers replaced

See audit doc table: T7 fully replaced (F_{i→j}, F_{j→i},
F_{ij}^{bi}, R_{i→j}(%), R_{j→i}(%), S_{ij}(%), "border pair");
T2/T3/T4: tau→τ, splits→"munis split", severed→"severed",
max|dev|→|dev|_max, max/min→max/min OMML.

## 5. Underscores intentionally retained

docs/ paths (CASE_SELECTION_ANALYSIS_FREEZE.md, CASE_SELECTION_AUDIT.md,
METHODS_DECISIONS.md) and raw filenames (r2ka_*.zip, od_*.xlsx,
ipss_kekkahyo1.xlsx, law_kosenkyoho_*.xml) in Table 1 — literal
reproducibility identifiers, category C.

## 6. OMML object counts (document.xml m:oMath)

- manuscript.docx: 39 → 48
- manuscript_inline.docx: 38 → 59
- cover_letter.docx: 1 (unchanged)
- highlights.docx: 0 (no math; unchanged)

## 7. Notation consistency decisions

One system: directional flow F_{i→j} / F_{j→i}; bidirectional
F_{ij}^{bi}; directional rate R_{i→j} = F_{i→j}/T_i; symmetric
intensity S_{ij} = F_{ij}^{bi}/(P_i+P_j); exploratory R_ext and S_2.
"F_{ij}^{bi}" never denotes a directional quantity; IPSS scenarios
keep literal S1/S2 labels (not math). Estimand notation unchanged:
C_border = L*(ON) − L*(OFF); C_s(B) = L_s*(B) − L_s*(0) ≥ 0;
F_B ⊂ F_0; L*_OFF ≤ L*_ON.

## 8. Table 7 old/new headers

pair→border pair; flow_i_to_j→F_{i→j}; flow_j_to_i→F_{j→i};
flow_bidirectional→F_{ij}^{bi}; R_i_to_j_pct→R_{i→j} (%);
R_j_to_i_pct→R_{j→i} (%); S_pct→S_{ij} (%). Values unchanged
(verified: CSV bytes untouched).

## 9. Tables 2–6 notation changes

tau→τ (T4 header + caption "τ sensitivity"); splits→"munis split";
severed→"severed"; max|dev|→|dev|_max (OMML); max/min→max/min (OMML).
T1/T5/T6 unchanged.

## 10. Asterisk audit

DOCX text contains exactly 2 literal `*`: inside the file-path cells
`data/raw/r2ka_*.zip` and `data/raw/od_*.xlsx` (T1) — intentional
wildcards. No markdown asterisk residue; scientific stars live inside
OMML (L*, D_s*).

## 11. Visual QC (page by page, inline + clean DOCX → PDF)

- §2 (clean p4): s∈{1,…,S}, F_0, L_s(D), D_s*=argmin_D L_s(D),
  F_B⊂F_0, C_s(B)=L_s*(B)−L_s*(0)≥0 — all OMML, correct.
- §3.3–3.5 (inline p7): τ, ±τ, estimand C_border=L*(Boundary ON)−
  L*(Boundary OFF), F_{i→j}, F_{ij}^{bi}, R_{i→j}=F_{i→j}/T_i fraction
  — all render.
- T2/T3 (p9): headers |dev|_max, max/min, PP, munis split, severed,
  objective — legible (LibreOffice shows the | glyph thin; correct in
  Word OMML).
- T4 (p12): τ header + caption; τ sweep OMML in §4.3.
- T7 (p15): all six OMML headers render correctly; 15-row values
  unchanged; no overflow.
- No missing symbols, no blue text, TNR 12pt body / 10pt captions, no
  clipped equations, no literal markdown asterisks.

## 12. Canonical numbers — unchanged

All values in manuscript_values.csv and every CSV byte-identical;
only prose notation and DOCX header labels changed. Additionally,
§Limitations wording updated: the stale "secondary source" clause for
the proximity ranking was replaced with the accurate caveat
(2006-vintage coordinates on official MLIT P02 data).

## 13. Final file paths

- `submission_package_PoliticalGeography_FINAL/manuscript.docx`
- `submission_package_PoliticalGeography_FINAL/manuscript_inline_PoliticalGeography_FINAL_v5.docx`
- `submission_package_PoliticalGeography_FINAL/cover_letter_PoliticalGeography_FINAL_v4.docx` (unchanged)
- `submission_package_PoliticalGeography_FINAL_v5.zip`
- `reproducibility_bundle_FULL.zip`
- Builders: `src/report/docx_rich.py` (MATH_RULES),
  `src/report/build_inline_docx.py` (HEADER_LABELS)

## Gates

All gates pass: every DOCX underscore classified; no raw underscore
math; T7 publication notation; τ native; OMML for structured math; no
LaTeX; legitimate path underscores kept; no markdown asterisks;
consistent notation; equations render; tables readable; no canonical
result changed; fixed QC satisfied.
