# FINAL POLITICAL GEOGRAPHY WORDING LOCK

Date: 2026-10-03 (UTC). Wording-only lock pass. No analysis rerun; no
canonical number changed.

## 1. "Depends" sentence — old/new

Old (§4.6): "Kyoto is polycentric: {{cs_ko_T}} travel to Osaka but only
{{cs_ks_T}} to Shiga — Kyoto depends on Osaka at almost the same rate
Shiga depends on Kyoto. For full disclosure, Shiga→Kyoto is not the
bloc's maximum directional dependence: Nara→Osaka reaches {{cs_no_T}}
(Table 7)."

New: "Kyoto is polycentric: {{cs_ko_T}} travel to Osaka but only
{{cs_ks_T}} to Shiga — a directional rate of similar magnitude to
Shiga's toward Kyoto. For full disclosure, Shiga→Kyoto is not the
bloc's maximum directional share: Nara→Osaka reaches {{cs_no_T}}
(Table 7)."

## 2. "Extreme case" sentence — old/new

Old (§1): "The Kyoto–Shiga prefectural boundary in Japan's Kinki
region is a deliberately extreme case, chosen under pre-specified
criteria…"

New: "The Kyoto–Shiga prefectural boundary in Japan's Kinki region was
deliberately selected as a case of exceptional institutional proximity
and multilayer cross-border entanglement, under pre-specified
criteria…"

Cover letter old: "The case is deliberately extreme."
Cover letter new: "The case is deliberately extreme on one verified
dimension: institutional proximity."

## 3. Remaining depend/extreme occurrences — all valid

| File | Occurrence | Disposition |
|---|---|---|
| manuscript §4.6 | "an engineered cross-border dependency older than the current electoral system" | RETAINED — refers to Kyoto City's water supply drawn from Lake Biwa at Ōtsu through its own canal since 1890; a genuine infrastructure dependence, not a mobility construct |
| cover letter | same "water dependency" phrase | RETAINED, same reason |
| manuscript §5 | "The case is extreme on proximity and institutional entanglement but not on raw flow" | RETAINED — "extreme" is tied to the named, verified dimension (proximity) |
| cover letter | "deliberately extreme on one verified dimension: institutional proximity" | RETAINED — qualified by verified dimension |
| manuscript references | Tam Cho & Liu 2016 title "…identifying extreme redistricting plans" | RETAINED — verbatim published article title |
| manuscript_values.csv | token names only | not journal-facing text |

No remaining "dependence/dependency/reliance" applied to the mobility
result. No unqualified "extreme case" remains.

## 4. Canonical values — unchanged

7.1% (Kyoto→Osaka share), 7.2% (Shiga→Kyoto share), 65.5% (Shiga
out-of-prefecture share to Kyoto), 1.8% (Kyoto→Shiga), 20.4%
(Nara→Osaka), 18/19 municipalities, 79,466/176,231 flows, S 1.99%/2.91%,
Level A [0, 532,293], Level B 0, 78/122 placebos, 10.45188 km rank
1/1,081, margin 8.51538 km — all byte-identical in
`manuscript_values.csv` and outputs.

## 5. National proximity wording — precise

All journal-facing instances say "prefectural government offices … by
geodesic distance" (abstract, §1, §4.6, highlights, cover letter); rank
is 1 of 1,081 pairs on GRS80 from MLIT P02 primary data.

## 6. Cover-letter impact

Only the opening sentence of the case paragraph changed
("deliberately extreme on one verified dimension: institutional
proximity"). Scientific energy retained; single-author "I"; all
required elements (container-of-representation framing, national
proximity, multilayer entanglement, Kyoto–Osaka counterfactual, 18/19,
ON/OFF estimand, 200 placebos, counterintuitive bounded cost, journal
fit) intact.

## 7. Regression QC

- Global grep (single urban system / integrated urban / continuous
  urban fabric / maximal severity / maximum severity / should bind
  hard / dependence / extreme case / most integrated / closest
  capitals / natural divide / genuine divide): no unsupported
  occurrences.
- "infeasible" appears only in hedged forms (no-incumbent-found;
  "not a proof of mathematical infeasibility").
- Level A remains FEASIBLE + cost interval (not proven optimal);
  Level B zero remains best-found.
- qc_report: all 97 checks pass, 0 failures (includes asterisk and
  claim audits). ruff clean.
- DOCX→PDF spot check (results pages, cover letter): OMML equations
  render, TNR body black text, F8/T7 in place, no literal asterisks,
  no caption regression; figure/table numbering F1–F8/T1–T7 unchanged.

## 8. Final file paths

- `submission_package_PoliticalGeography_FINAL/manuscript.docx`
- `submission_package_PoliticalGeography_FINAL/manuscript_inline_PoliticalGeography_FINAL_v4.docx`
- `submission_package_PoliticalGeography_FINAL/cover_letter_PoliticalGeography_FINAL_v4.docx`
- `submission_package_PoliticalGeography_FINAL/highlights.docx` (unchanged content)
- `submission_package_PoliticalGeography_FINAL_v4.zip` (new name)
- `reproducibility_bundle_FULL.zip`
- Sources: `manuscript/manuscript_text.md`, `manuscript/cover_letter.md`
