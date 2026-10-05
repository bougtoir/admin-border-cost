# FINAL Political Geography Submission-Lock Report (v7)

Date: 2026-10-02. Mode: three targeted wording fixes + regression check. No analysis, optimization, case-selection or distance computations rerun; no canonical number, figure, table, formula or OMML object changed.

## 1. Manuscript proximity sentence
- Old: "The two prefectural government offices sit {{cs_capital_km}} apart — the closest such pair in Japan by geodesic distance — separated by roughly {{cs_rail_min}} of commuter rail; the border crosses an exceptionally proximate and functionally connected cross-border setting …"
- New: "The two prefectural government offices sit {{cs_capital_km}} apart — the closest such pair in Japan by geodesic distance — while the border separates an exceptionally proximate and functionally connected cross-border setting …"
- §4.6 also carried "— linked by roughly {{cs_rail_min}} of commuter rail." → deleted (clause removed, rest of sentence unchanged).

## 2. Cover-letter proximity sentence
- Old: "…the closest pair of prefectural government offices in Japan — 10.5 km by geodesic distance, ten minutes by rail — in an exceptionally proximate …"
- New: "…the closest pair of prefectural government offices in Japan — approximately 10.5 km apart by geodesic distance — within an exceptionally proximate …"

## 3. Rail-time wording
Removed entirely from all journal-facing artifacts (manuscript Introduction, §4.6, cover letter). No station-to-station rail statement retained; government-office / rail conflation eliminated. Grep for rail/minutes over manuscript_text.md + cover_letter.md: 0 hits.

## 4. Duplicated Limitations sentence removed
"Commuting flow is one functional dimension of connectivity, not all of it." (second occurrence) deleted; the first, more specific formulation retained: "uses commuting/schooling flow as the functional layer (one dimension of connectivity, not all of it)".

## 5. Cover-letter "It does not." wording
- Old: "It does not. Solving matched optimization problems …"
- New: "The answer is not the large penalty that visible cross-border entanglement might suggest. Solving matched optimization problems …"

## 6. Canonical numbers unchanged
Verified post-edit in manuscript source and regenerated DOCX: 47 offices / 1,081 pairs / GRS80 / ~10.5 km / rank 1 / margin 8.5 km; [0, 532,293]; Level B best-found 0; 200 placebos 78/122; 39,733; 176,231; 79,466; S 1.99% vs 2.91%; 7.2%/7.1%/1.8%/65.5%; 18/19; Nara→Osaka 20.4%; all placebo/future values.

## 7. Regression-search results
ten minutes / 10 minutes / commuter rail / rail: 0 hits.
It does not.: 0 hits.
single urban system / continuous urban fabric / maximal|maximum severity / should bind hard / natural|genuine divide / SEPS / Socio-Economic: 0 hits.
dependence/dependency: only "engineered cross-border dependency" for the Lake Biwa water canal (legitimate physical dependency, retained from prior pass).
infeasible: only inside explicit no-incumbent caveats ("not proven infeasibility", "not a proof of mathematical infeasibility") — correct usage.
exact solution / optimal solution / cost is exactly zero: 0 hits. Level B remains best-found; Level A an interval.

## 8. QC
qc_report: 97 checks, 0 failures. ruff: clean. OMML counts unchanged (48 clean / 59 inline). No literal asterisks, no raw math underscores. Clean/inline paragraph parity re-verified after edits (identical prose sequence). Rendered pages visually inspected: intro proximity sentence, §4.6 proximity paragraph, cover-letter pp.1 — all correct. TNR 12pt body, 10pt captions, black text.

## 9. Final paths
- manuscript/manuscript.docx (clean)
- manuscript/manuscript_inline.docx → submission_package_PoliticalGeography_FINAL_v7/manuscript_inline_PoliticalGeography_FINAL_v7.docx
- manuscript/cover_letter.docx → cover_letter_PoliticalGeography_FINAL_v7.docx
- manuscript/manuscript_inline.html
- submission_package_PoliticalGeography_FINAL_v7.zip
