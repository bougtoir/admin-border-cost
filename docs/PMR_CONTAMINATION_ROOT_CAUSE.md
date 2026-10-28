# PMR Retargeting — Contamination Root-Cause Audit

Date: 2026-10-05 (UTC). Scope: reconstruction of how an earlier PMR-facing draft
came to contain empirical material from an unrelated shrinking-region project,
and the controls now in force.

## 1. Root cause

1. The previous retargeting prompt violated project isolation: it invited reuse
   of an unrelated public-service / shrinking-region project and offered
   public-service examples (healthcare, mobile provision, digital substitution,
   settlement consolidation, a "Minimum Functional Guarantee") that the
   Kyoto–Shiga source files do not contain.
2. Those service examples were then written into PMR-facing text as if they
   were supported evidence. They are not: the only validated empirical study
   in this repository prices **electoral representation** for the Kyoto–Shiga
   boundary (see `docs/CLAIM_EVIDENCE_MATRIX.csv`).
3. No allowlist, denylist, or per-claim source ledger existed at the time, so
   gap-filling pulled content from another project's results. The failure mode
   was silent import, not a data error inside admin_border_cost itself.
4. This was a **prompt-governance failure**, not a data-discovery failure: the
   canonical Kyoto–Shiga data and results were and remain clean; the
   instructions given to the drafting process were not.
5. Corrective control now in force: a strict source lock (only the canonical
   project files listed in §1 of the governing prompt), an explicit denylist
   (§2), and a per-claim source ledger (`docs/PMR_SOURCE_LEDGER.csv`) under
   which every empirical sentence in PMR-facing artifacts must trace to a
   canonical source file or be labelled CONCEPTUAL_ONLY /
   PLANNED_NOT_COMPLETED.

## 2. Contaminated-claim disposition table

All statements in the earlier PMR draft that drew on the unrelated project are
dispositioned REMOVE. None may reappear in PMR-facing artifacts unless
independently recreated, explicitly approved, and documented as a NEW
Kyoto–Shiga analysis with its own provenance.

| Contaminated claim / term | Disposition |
|---|---|
| Tottori (region, data, results) | REMOVE |
| Shimane (region, data, results) | REMOVE |
| Okayama (region, data, results) | REMOVE |
| Chugoku (region, data, results) | REMOVE |
| 1-km healthcare demand grid | REMOVE |
| Minimum Functional Guarantee | REMOVE |
| Asset-preservation results from the other project | REMOVE |
| Settlement-consolidation results from the other project | REMOVE |
| Mobile-service provision results from the other project | REMOVE |
| Digital-substitution results from the other project | REMOVE |
| Relocation-friction grid / results from the other project | REMOVE |
| "When Moving People Is Costly, Move Functions" | REMOVE |

## 3. What is permitted instead

Only canonical Kyoto–Shiga facts (source-locked; see
`docs/PMR_SOURCE_LEDGER.csv`): Kyoto + Shiga prefectures; 55 municipal/ward
units; 11,978 census small areas; 2020 population 3,991,697; Kyoto 6 + Shiga 3
single-member districts (K = 9); the statutory no-straddle rule; the
10.5 km prefectural-government-office proximity (national rank 1 of 1,081
pairs); 79,466 daily cross-prefecture commuting/schooling trips (Kyoto–Osaka
176,231 reported alongside); normalized symmetric intensity ≈1.99%;
Shiga→Kyoto ≈7.2% (65.5% of Shiga out-of-prefecture trips); Kyoto the largest
external destination for 18/19 Shiga municipalities; Level A true cost bounded
[0, 532,293] (FEASIBLE, not OPTIMAL); Level B best-found ON–OFF difference 0
(heuristic); real border crossing flow 39,733 below all 200 matched placebos
(78 feasible, 122 no-feasible-incumbent; feasible median ≈0.0647; real border
≈10th percentile). The paper prices ONE function — electoral representation —
and does not empirically estimate healthcare, education, emergency, or other
service systems.

## 4. Standing controls

- Literal-string denylist scan over PMR-facing artifacts before every
  completion declaration (results recorded in
  `FINAL_PMR_KYOTO_SHIGA_SPECIAL_ISSUE_ASSESSMENT.md`).
- Every empirical sentence in the abstract, email, and any future manuscript
  plan or cover letter requires a row in `docs/PMR_SOURCE_LEDGER.csv`.
- Planned analyses are always labelled planned; null or mixed results are
  retained, not substituted.
