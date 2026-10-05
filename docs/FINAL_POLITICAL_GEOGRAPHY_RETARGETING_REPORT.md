# FINAL POLITICAL GEOGRAPHY RETARGETING REPORT — admin_border_cost

2026-10-02 (UTC). Retarget of the validated package to Political
Geography after the SEPS desk rejection. Canonical results unchanged.

## 1. Target verification
Journal facts (Elsevier; ISSN 0962-6298; EiC Filippo Menga; full-length
articles ~11,000 words; abstract ~250; ≤6 keywords; author–year
alphabetized references; highlights 3–5 ≤85 chars) recorded in
docs/JOURNAL_REQUIREMENTS.md (PG section current; SEPS/AG superseded)
and docs/POLITICAL_GEOGRAPHY_TARGETING_NOTES.md, including the two
items left [UNVERIFIED] (peer-review anonymity; live Guide text) and
the package's compensations for them.

## 2. Citation ecology rebuilt
docs/CITATION_ECOLOGY_POLITICAL_GEOGRAPHY.md: 8 verified additions
(Agnew 1994; Newman & Paasi 1998; Painter 2010; Elden 2013; Paasi 2009;
Duchin & Tenner 2024 in-journal bridge; OECD 2012; Taylor & Johnston
1979) + all 15 prior references retained and converted to
Harvard-style. Novelty boundary stated.

## 3. Case-selection validation (new analysis)
- Frozen before ranking: docs/CASE_SELECTION_ANALYSIS_FREEZE.md
- Audit + sources: docs/CASE_SELECTION_AUDIT.md
- Data: 7 new OD tables + 7 r2ka comparator zips, ledgered
  (SHA-256, fetch_all, DATA_PROVENANCE B3–B9/A3)
- Outputs: outputs/tables/case_selection_comparison_full.csv (15
  pairs), destination_pref_shares.csv, municipal_external_destinations.csv,
  case_pref_population.csv; T7 table; F8 figure;
  outputs/diagnostics/case_selection_qc.json
- Honest outcome: Kyoto–Shiga tops Kyoto's borders on the pre-specified
  normalized intensity (S = 1.99%) — but Osaka–Hyogo (2.91%), Kyoto–
  Osaka raw volume (176,231) and Nara→Osaka share (20.4%) all exceed it
  on their axes and are reported in text, table and figure.
- Proximity/institutional layer verified: 10.5 km prefectural-office
  pair (closest in Japan, nationwide ranking), ~10 min rail, RIETI
  "Keiji" cluster, JICPA Keiji body, Kyoto Shimbun footprint, Biwako
  Canal (1890), Ōmi historical routes.

## 4. Manuscript rewritten for PG
Title (candidates considered: "Institutionally divided, functionally
entangled: the price of an inherited prefectural boundary in electoral
districting, Kyoto–Shiga, Japan" (chosen); "What does a prefectural
border cost? Pricing a statutory wall inside Japan's electoral
districting"; "The boundary as estimand: territorial constraint and
representation in Kyoto–Shiga"; "Paying for the container: the
opportunity cost of a statutory boundary in Japanese districting").
Abstract 223 words. Introduction 7-point sequence on territorial
containers → electoral geometry → estimand → case → contributions →
scope. New §3.5 case-selection protocol; new §4.6 case-selection
results. Discussion 7 layers (finding / territoriality / electoral
geography / mismatch-vs-estimand / selection discipline / principle /
limits). Limitations expanded (selection bounds, secondary-source
distance ranking, OD one-dimensionality). Author–year citations;
alphabetized References; Declarations incl. AI disclosure.

## 5. Builders/QC
build_manuscript / build_inline_docx / build_cover_letter /
build_highlights / qc_report all pass: **43/43 checks**, 0 missing
value tokens, ruff clean. New cs_* values injected from
manuscript_values.csv (build_case_selection.py appends; Makefile
order fixed). PDF visual inspection of all pages performed; F/T
first-citation order verified (F1→F8, T1→T7); OMML math; TNR; no
stray asterisks found.

## 6. Packages
- submission_package_PoliticalGeography_FINAL.zip (26 files:
  manuscript.docx, manuscript_inline_PoliticalGeography_FINAL.docx,
  cover_letter_PoliticalGeography_FINAL.docx, highlights.docx,
  DECLARATIONS.md, CLAIM_EVIDENCE_MATRIX.csv, README.md, figures/ F1–F8,
  tables/ T1–T7)
- reproducibility_bundle_FULL.zip rebuilt (333 entries incl.
  case_selection code/data/outputs)

## 7. Hostile review
docs/HOSTILE_REVIEW_POLITICAL_GEOGRAPHY.md — 6 personas; residual
risks ranked (case-selection is the conceded weak flank; measurement-
forward style is the residual desk risk).

## 8. Not done / caveats
- PG peer-review anonymity model [UNVERIFIED] (portal blocked);
  package compatible with either.
- No new optimization was run (per instruction); canonical numbers
  identical to the SEPS package.
- Public mirror: synced via .github/workflows/sync-to-repos.yml on
  merge to master; verify bougtoir/admin-border-cost after merge.
