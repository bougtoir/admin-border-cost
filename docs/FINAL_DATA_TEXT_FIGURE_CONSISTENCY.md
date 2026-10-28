# FINAL DATA–TEXT–FIGURE CONSISTENCY — v2

Cross-check of prose vs tables vs figures vs canonical CSVs.

- Means (+0.0046 / +0.0005 / +0.0060 / +0.0042 km): text = Table 2 = Figure 3 = metrics_summary.csv. PASS.
- OFF cross shares (0.17/0.11/0.20/0.19%): text = cross_function CSVs. PASS.
- Unit counts 45/41/70/81 and max gains +8.383/+3.077/+14.11/+16.55: text = CSVs (unit-level maxima, not difference-of-maxima). PASS.
- Worst-decile gaps (0.662→0.457 etc.): text = Figure 4 = CSVs. PASS.
- 39,733 trips / 79,466 / 176,231 / 1.991% / 2.91% / 7.2% / 65.5% / 18/19: text = registry/census. PASS.
- [0, 532,293]: text = aggregate_results.py derivation (1,793,321−1,261,028). PASS.
- Level B 0.6245294675 best-found = 0 cost: text = model_results.csv. PASS.
- Placebo 200/78/122, median 0.0647, IQR 0.0222–0.0727: text = T5_placebo.csv. PASS.
- 11,978 units, 11 border munis, supply counts: text = processed CSVs. PASS.
- Table 3 travel-time seconds: fixed to +0.41 s / +0.54 s (was mislabeled +6.9 s/+9.0 s). PASS after fix.
- Border-muni reassignment shares: text now 67/70 elem, 79/81 JHS (was "all border-adjacent"). PASS after fix.
