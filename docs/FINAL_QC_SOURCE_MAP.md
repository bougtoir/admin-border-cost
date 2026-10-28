# FINAL QC SOURCE MAP — PMR SI Kyoto–Shiga (v2)

Date: 2026-10-28. Scope: every number/claim in `manuscript/manuscript_PMR_SI_KYOTO_SHIGA_FINAL_v2.md` mapped to its canonical source artifact.

## Access opportunity costs (Boundary ON/OFF, nearest-facility geodesic, uncapacitated)
| Claim | Value | Source |
|---|---|---|
| Hospital mean ON/OFF | 1.630615 / 1.626012 km → +0.004604 | `results/pmr_access/healthcare/metrics_summary.csv` |
| Hospital max unit gain | +8.383 km; 45 units; OFF cross share 0.17% | `results/pmr_access/healthcare/cross_function_equity_extra.csv`, `assignments_*` |
| Clinic mean ON/OFF | 0.452674 / 0.452141 → +0.000532; 0.11%; 41 units; max +3.077 | `results/pmr_access/healthcare/metrics_summary.csv`, `cross_function_equity_extra.csv` |
| Elementary ON/OFF | 0.752088 / 0.746101 → +0.005987; 0.20%; 70 units (67 border muni); max +14.114 | `results/pmr_access/education/metrics_summary.csv`, `assignments_*` |
| Junior-high ON/OFF | 1.145760 / 1.141514 → +0.004246; 0.19%; 81 units (79 border); max +16.547 | `results/pmr_access/education/metrics_summary.csv`, `assignments_*` |
| Worst-decile gaps ON→OFF | hosp 0.662→0.457; clinic 0.217→0.174; elem 0.746→0.281; JHS 0.570→0.452 | `results/pmr_access/*/worst_decile_gaps.csv` |
| Border munis w/ cross assignment | hosp 7, clinic 8, elem 6, JHS 9 | `results/pmr_access/cross_function/cross_function_equity_extra.csv` |
| Household-weight & travel-time sensitivity | elem +0.0059; +0.41 s hosp / +0.54 s elem @40 km/h | `results/pmr_access/*/sensitivity.csv` |

## Electoral (Level A municipality / Level B small-area districting)
| Claim | Value | Source |
|---|---|---|
| Level A cost bound | [0, 532,293] objective units | `src/report/aggregate_results.py` (inc_on 1,793,321 − bound_off 1,261,028, tau=0.20, FEASIBLE) |
| Level B best-found cost | 0 (ON=OFF best-found 0.6245294675099053) | `outputs/tables/model_results.csv` |
| Real border cross flow | 39,733 trips < all 200 placebos | `outputs/placebo/T5_placebo.csv` |
| Placebo stats | n=200, 78 feasible, 122 no feasible incumbent; median 0.0647, IQR 0.0222–0.0727 | `outputs/placebo/T5_placebo.csv`, `manuscript/manuscript_values.csv` |
| Normalized border share | S ≈ 1.991%; Osaka–Hyogo max 2.91% | `manuscript/manuscript_values.csv` |

## Case geography / flows
| Claim | Value | Source |
|---|---|---|
| Prefectural offices distance | 10.45188 km, rank 1 of 1,081 unordered pairs (C(47,2)) | `outputs/tables/prefectural_government_pair_distances.csv` |
| Cross-prefecture trips | 79,466; Kyoto largest ext. dest. for 18/19 Shiga munis; 7.2% / 65.5% | 2020 Census OD tables; `manuscript/manuscript_values.csv` |
| Kyoto–Osaka trips | 176,231 | `manuscript/manuscript_values.csv` |
| Demand | 11,978 units, pop 3,991,697, 1,043 zero-pop units | `data/processed/smallarea_demand_units.csv` |
| Supply | 221 hospitals (164/57); 3,584 clinics (2,505/1,079); 571 elementary; 256 JHS | `data/processed/facilities_*.csv` |
| Border municipalities | 11 | `data/processed/border_municipalities.csv` |

All prose values verified equal to these sources (rounded per manuscript convention); registry = `manuscript/manuscript_values.csv` / `manuscript_values_kv.csv`.
