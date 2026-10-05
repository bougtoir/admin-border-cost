# Hostile review — Political Geography submission (2026-10-02)

Six-persona adversarial pass, conducted after the retargeting build and
before packaging. Ratings: 最優先 (must fix) / 高 / 中 / 任意.

## Persona 1 — PG desk editor
- 高: "OR paper wearing political-geography clothes." Mitigated:
  Introduction and Discussion now lead with the territory/boundary
  canon (Agnew; Newman & Paasi; Painter; Elden; Paasi) and the
  journal's own computational-electoral-geometry bridge (Duchin &
  Tenner 2024); the estimand is framed as *pricing a boundary*, not a
  facility problem. Residual risk acknowledged — the paper is still
  measurement-forward; the cover letter argues fit explicitly.
- 中: peer-review model unverified (ScienceDirect blocked). Package is
  self-contained; title page separable for either anonymity model.
- 中: AI disclosure — declaration added to manuscript + package.

## Persona 2 — political geographer
- 最優先: "single-case empiricism without conceptual pay-off."
  Addressed: divide/entanglement typology; institutional-persistence
  vs functional-inefficiency distinction; case-selection protocol as
  methodological contribution. 最優先→高 residual: theory layer is a
  lens, not a framework — acceptable for a measurement paper.
- 高: Japanese context under-translated → proximity facts, Keiji
  economy, media/water institutions now sourced and narrated.

## Persona 3 — electoral-geography reviewer
- 高: no electoral outcome anywhere → flagged as deliberate scope;
  nonpartisan statement in §1 and cover letter.
- 中: statutory ±20% reconstruction vs legal tolerance → already
  disclaimed as experimental parameter.

## Persona 4 — spatial/OR reviewer
- 高: Level A not OPTIMAL → reported as interval [0, 532,293], never
  claimed; Level B zero labeled best-found.
- 中: composite weights arbitrary → declared weights + τ sensitivity
  retained; acknowledged in Limitations.
- 任意: municipal-share severed-flow closed form → limitation stated.

## Persona 5 — case-selection reviewer (the dangerous one)
- 最優先: cherry-picking → frozen protocol (FREEZE doc), all 15 pairs
  in Table 7/full CSV, exploratory measures flagged.
- 最優先: unfavourable results → *all retained*: Kyoto–Osaka raw
  volume 176,231 > 79,466; Osaka–Hyogo S = 2.91% > Kyoto–Shiga 1.99%;
  Nara→Osaka 20.4% > Shiga→Kyoto 7.2%. §4.6 states each explicitly.
- 高 residual: "then why not Osaka–Hyogo?" — answered honestly in
  §4.6/§5 (most-proximate-pair test: closest prefectural-government-office pair
  in Japan + named Keiji entanglement + hard statutory wall), not
  measure-maximizing. This is the paper's weakest flank and it is
  conceded openly rather than hidden.
- 中: nationwide "closest pair" rests on a compiled secondary ranking
  (uub.jp) → disclosed as such in Limitations; sanity-checked against
  office coordinates.

## Persona 6 — reproducibility reviewer
- 高: public mirror staleness → sync-to-repos path checked; PR note.
- 中: new raw data → ledgered (SHA-256, statInfIds, fetch_all rows,
  DATA_PROVENANCE B3–B9 + A3).
- 中: `make manuscript` order → case_selection depends on aggregate
  in Makefile.

## Mechanical audit results
- QC: 43/43 checks pass; ruff clean; no [MISSING] tokens.
- Citation order: F1→F8 and T1→T7 strictly by first citation; refs
  author–year, alphabetized; all new DOIs verified via Crossref.
- Fonts/styles: TNR 12pt body, 10pt captions, black; OMML math inline;
  PDF page inspection of all 22 inline-docx pages performed.
- Canonical results untouched: A [0,532,293]; B diff 0; 78/122 split;
  0.0245/10th pct; 39,733 vs ~99,420.
