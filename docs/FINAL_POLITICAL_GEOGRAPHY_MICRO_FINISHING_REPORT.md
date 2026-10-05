# FINAL POLITICAL GEOGRAPHY MICRO-FINISHING REPORT

Date: 2026-10-03 (UTC). Scope: four claim-calibration fixes, cover-letter
heat check, and fixed submission QC on the existing Political Geography
package. No canonical numerical result was changed; no primary analysis
was rerun.

## 1. "Single urban system" — occurrences and replacements

| Location | Old | New |
|---|---|---|
| manuscript §1 (was line 27) | "Two prefectural governments thus sit on top of what is functionally close to a single urban system — institutionally divided, functionally entangled." | "The two prefectures are thus institutionally separate yet functionally entangled within a wider polycentric regional system." |

No other occurrence of "single/integrated/one metropolitan urban system"
exists in journal-facing artifacts.

## 2. "Maximal severity" — occurrences and replacements

| Location | Old | New |
|---|---|---|
| manuscript §4.6 | "…at maximal geographic severity, not because it tops every measure" | "…in the country's most proximate prefectural-government pairing by geodesic distance, not because it tops every measure" |
| docs/HOSTILE_REVIEW_POLITICAL_GEOGRAPHY.md | "maximal-severity test: closest prefectural-government pair" | "most-proximate-pair test: closest prefectural-government-office pair" |
| docs/POLITICAL_GEOGRAPHY_TARGETING_NOTES.md | "a case of maximal test severity" | "a case of extreme spatial proximity" (and "prefectural-government pair" → "-office pair") |

## 3. Cover letter — "should bind hard" old/new

Old: "If any administrative line in Japan should bind hard inside a
representation system, it is this one."
New: "This juxtaposition makes Kyoto–Shiga an unusually sharp test of
whether functional entanglement necessarily makes an inherited political
boundary spatially costly." The following paragraph's payoff
("It does not.") is retained, so the narrative arc is unchanged.

## 4. "Continuous urban fabric" — occurrences and replacements

| Location | Old | New |
|---|---|---|
| manuscript §1 | "the border bisects a continuous urban fabric carrying {{n_cross}} daily cross-prefecture commuting and schooling trips" | "the border crosses an exceptionally proximate and functionally connected cross-border setting linked by {{n_cross}} daily cross-prefecture commuting and schooling trips" |
| manuscript §5 (mismatch paragraph) | "it bisects a continuous urban fabric carrying {{n_cross}} daily cross-prefecture trips" | "it bisects an exceptionally proximate cross-border setting linked by {{n_cross}} daily cross-prefecture trips" |
| cover letter | "across a continuous urban fabric carrying 79,466 daily cross-border commuting and schooling trips" | "in an exceptionally proximate and functionally connected cross-border setting carrying 79,466 daily cross-border commuting and schooling trips" |

No DID/built-up-area analysis exists in the canonical repository, so the
claim was removed rather than re-grounded, per instructions.

## 5. Final wording of the national proximity claim

- Highlights: "Kyoto–Shiga: the closest prefectural-government-office
  pair in Japan."
- Abstract: "it separates the two closest prefectural government
  offices in Japan by geodesic distance (10.5 km)".
- §1: "The two prefectural government offices sit 10.5 km apart — the
  closest such pair in Japan by geodesic distance".
- §4.6: "the closest of all 1,081 prefectural-government-office pairs
  in Japan, 8.5 km closer than the runner-up pair".
- Cover letter: "the closest pair of prefectural government offices in
  Japan — 10.5 km by geodesic distance".
- Machine-readable truth (unchanged): 10.45188 km, rank 1/1,081;
  runner-up Saitama–Tokyo 18.96726 km; margin 8.51538 km — MLIT P02
  (2006), GRS80, pyproj.Geod, in
  `outputs/tables/prefectural_government_pair_distances.csv`.
- Rail time remains a separate accessibility illustration
  ({{cs_rail_min}}).

## 6. Where the 18/19 result appears

§4.6 (Results / case selection): "Kyoto is the largest external
prefectural destination for 18 of Shiga's 19 municipalities (the sole
exception, Maibara…)" — commuting/schooling OD, canonical metric.
Cover letter now also carries it ("Kyoto is the largest
out-of-prefecture destination for 18 of Shiga's 19 municipalities").
No "dependence/dominance" label is applied to the metric.

## 7. Kyoto–Osaka counterfactual — still visible

Abstract ("Osaka dominates raw volume, a comparison we report in
full"), §4.6 (176,231 vs 79,466; Nara→Osaka 20.4% directional share;
Osaka tops 23 Kyoto municipalities), Table 7, cover letter ("Kyoto–Osaka
raw mobility is more than twice Kyoto–Shiga's"). Nothing suppressed.

## 8. SEPS-style framing — absent

§2/§5 are framed as "inherited territory as a constraint on
representation"; the estimand C(B) = L*_B − L*_0 with F_B ⊆ F_0 is
retained with OMML. Generic service examples appear only in the
transferability coda, not as drivers.

## 9. Canonical numbers — unchanged

Level A [0, 532,293]; Level B diff 0; placebos 78/122; OD 39,733;
Kyoto–Osaka 176,231; Kyoto–Shiga 79,466; S 1.99%/2.91%; Nara→Osaka
20.4%; 18/19; 10.45188 km rank 1/1,081. `manuscript_values.csv`
numeric fields untouched by this pass.

## 10. Cover-letter heat-check changes

Beyond the "should bind hard" replacement, the case paragraph now also
carries the 18/19 municipality result and the polycentric-network
sentence (Kyoto–Osaka >2× raw flow) up front, making the
juxtaposition sharper. The arc — territory → sharp test → bounded
cost → placebos → why Political Geography — is intact. No "we":
single-author "I" throughout.

## 11. Typography / asterisks / OMML / visual QC

- `qc_report`: all checks pass (97 checks, 0 failures; asterisk and
  claim audits included). `ruff check src` clean.
- DOCX→PDF visual spot check (title/abstract, methods, study area,
  cover letter): TNR body, black text, equations render as OMML
  (C_border = L*(Boundary ON) − L*(Boundary OFF) visible inline),
  figures/captions in place, no literal markdown asterisks.
- Figure/table numbering unchanged (F1–F8, T1–T7) — no caption edits
  were needed, so first-citation order is preserved.

## 12. Final file paths

- `submission_package_PoliticalGeography_FINAL/manuscript.docx`
- `submission_package_PoliticalGeography_FINAL/manuscript_inline_PoliticalGeography_FINAL_v3.docx`
- `submission_package_PoliticalGeography_FINAL/cover_letter_PoliticalGeography_FINAL_v3.docx`
- `submission_package_PoliticalGeography_FINAL/highlights.docx`
- `submission_package_PoliticalGeography_FINAL.zip`
- `reproducibility_bundle_FULL.zip`
- Sources: `manuscript/manuscript_text.md`, `manuscript/cover_letter.md`

## Final gates

All gates pass: no single-urban-system / maximal-severity /
should-bind-hard / continuous-urban-fabric wording; the closest-pair
claim explicitly concerns prefectural government offices by geodesic
distance; 18/19 visible; Kyoto–Osaka not hidden; polycentric reading
preserved; no SEPS generic-service driver; solver/placebo caveats
intact; no canonical number changed; cover letter retains energy.
