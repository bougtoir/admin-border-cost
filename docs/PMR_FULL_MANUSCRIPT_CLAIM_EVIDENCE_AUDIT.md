# Claim-evidence audit — PMR full manuscript

| claim in manuscript | evidence | status |
|---|---|---|
| offices 10.5 km apart, rank 1/1,081 | outputs/models + case-selection audit | OK |
| 79,466 cross-prefecture trips; Kyoto–Osaka 176,231; 18/19; 7.2%/65.5%; S≈1.99% | census OD artifacts; manuscript_values.csv | OK |
| Level A bound [0,532,293] FEASIBLE; Level B best-found 0 (0.6245294675); 39,733 < all 200 placebos; 78 feasible/122 no-incumbent | outputs/models, outputs/placebo | OK |
| supply: 221 hospitals / 3,584 clinics / 571 elem / 256 JHS | processed P04/P29 CSVs | OK |
| mean ON−OFF: +0.0046/+0.0005/+0.0060/+0.0042 km | results/pmr_access metrics CSVs | OK |
| OFF cross-boundary share 0.11–0.20% | same | OK |
| 11 border municipalities; reassigned units 45/41/70/81 | adj_smallarea_edges + assignment CSVs | OK |
| worst-decile gaps (hosp 0.66→0.46; clinic 0.22→0.17; elem 0.75→0.28; JHS 0.57→0.45) | cross_function_equity_extra.csv | OK |
| max unit gains +8.38/+3.08/+14.11/+16.55 km | assignment CSVs dist_ON_minus_OFF | OK — note: supersedes the earlier "≈4.9–5.0 km" phrasing in the post-result abstract, which was the difference of maxima, not the max unit difference; post-result abstract txt+docx corrected to 14/17 km |
| travel-time sensitivity +6.9 s / +9.0 s | sensitivity CSVs | OK |
| selective permeability | framed as design implication only | calibrated |
| no "high-cost electoral", no "different optimal boundaries", no "boundary causes inequity" | scan of manuscript text | PASS |
