# Submission package — Political Geography

Manuscript: "Institutionally divided, functionally entangled: the price of an
inherited prefectural boundary in electoral districting, Kyoto–Shiga, Japan"

## Contents
- manuscript.docx — journal manuscript (figures/tables as separate files)
- manuscript_inline_PoliticalGeography_FINAL.docx — review copy with
  figures and tables embedded at first citation
- cover_letter_PoliticalGeography_FINAL.docx — cover letter
- highlights.docx — 5 highlights (each ≤85 characters)
- DECLARATIONS.md — ethics / competing interests / AI / data & code
  availability statements
- CLAIM_EVIDENCE_MATRIX.csv — every manuscript claim mapped to its
  evidence artifact
- figures/ — F1–F8 (PNG, separate files per journal convention)
- tables/ — T1–T7 (CSV; T7 = case-selection prefecture-pair comparison) + national prefectural-government office locations and all-pairs distances

## Canonical results (unchanged from validated pipeline)
- Level A (municipality, CP-SAT): FEASIBLE incumbents; true border cost
  bounded in [0, 532,293] objective units.
- Level B (small area, seeded SA): best-found ON–OFF difference = 0.
- Placebo: 200 matched borders; 78 feasible, 122 no feasible constrained
  incumbent found; real-border heuristic cost 0.0245 (10th percentile);
  cross-border OD 39,733 vs placebo median ~99,420.
- Case selection (new for this submission): frozen comparison of 15
  prefecture pairs; Kyoto–Shiga tops Kyoto's borders on normalized
  intensity S = 1.99% while Osaka–Hyogo (2.91%) and Kyoto–Osaka raw
  volume (176,231) are reported unfavourably; see Table 7 and
  docs/CASE_SELECTION_AUDIT.md in the repository.
