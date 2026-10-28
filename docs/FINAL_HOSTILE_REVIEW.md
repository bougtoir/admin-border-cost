# FINAL HOSTILE REVIEW — PMR SI Kyoto–Shiga v2

Adversarial read of the v2 manuscript. Severity: FATAL/MAJOR/MODERATE/MINOR.

| # | Attack | Severity | Evidence | Required fix | Status |
|---|---|---|---|---|---|
| 1 | "Boundary ON is an analytical counterfactual, not an actual legal barrier — the healthcare/education results are meaningless policy claims" | MAJOR | ON/OFF is explicitly a pricing estimand, not a policy simulation (§3) | State plainly it is a measurement device; already done §3/§8 | FIXED — framed as estimand, not intervention |
| 2 | Costs are tiny (+0.0005–0.0060 km); "the paper measures nothing" | MODERATE | Small mean is the finding; tail concentration (worst-decile 0.28–0.75 km gaps; max unit +8–17 km) is the policy-relevant result | Emphasize distribution not mean — already §6.2–6.4, §9 | NO FIX NEEDED — result is honest |
| 3 | Near-zero mean ≠ boundary irrelevant (opposite reading) | MODERATE | A hostile reader could claim the boundary is free | Paper already blocks this: concentrated burden in 11 border munis is the substantive result | NO FIX NEEDED |
| 4 | Electoral Level A bound [0,532,293] is "not an answer" | MODERATE | Solver status is FEASIBLE not OPTIMAL | Reported as bound, not claimed high — §6.1 already correct | FIXED — wording verified (never claims optimum/high) |
| 5 | Cross-function comparison mixes objective units | MODERATE | km vs weighted districting criterion | §5.4/§3 already restricts comparison to direction/structure | NO FIX NEEDED |
| 6 | Case selection: Kyoto–Shiga is "cherry-picked" | MODERATE | Rank-1 institutional proximity + middling entanglement argued as informative not extreme | §4 calibrated claim incl. Kyoto–Osaka 176,231 comparator | FIXED (Kyoto–Osaka comparator kept) |
| 7 | External validity: single boundary, Japanese context | MODERATE | §8 limitations state generalization scope | Explicit limitation present | NO FIX NEEDED |
| 8 | Uncapacitated nearest-facility is unrealistic for hospitals | MODERATE | No capacity attribute in P04; capacitated variant not run | Declared limitation (§5.2, §8, Table 3) | NO FIX NEEDED |
| 9 | "Selective permeability" is an untested policy masquerading as result | MAJOR | Could read as policy prescription | §3/§7 frame it as design implication/hypothesis, not tested optimum | FIXED — verified wording |
| 10 | Demand weight is total population for schools (not school-age pop) | MINOR | Proxy declared | Stated as limitation in §5.3/§8 | NO FIX NEEDED |
| 11 | Travel-time proxy values previously mislabeled (+6.9 s vs true +0.41 s) | MINOR | Table 3 | Corrected to +0.41 s / +0.54 s in Table 3 | FIXED |
| 12 | Education reassignment claimed "all border-adjacent"; 5 of 151 units lie outside the 11 border munis | MINOR | assignment CSVs | §6.3 now reports 67/70 and 79/81 border-muni counts | FIXED |
| 13 | "1,081 ordered pairs" wrong — pairs are unordered (C(47,2)) | MINOR | distances CSV | Fixed to unordered + precise 10.45188 km | FIXED |
| 14 | Orphan references (Bozeman 2007, Moore 1995, Radnor 2014, Onishi companion) | MINOR | bibliography audit | All four now cited substantively in text | FIXED |

No FATAL issues. All MAJOR criticisms are answered in-text or by fixes above. Residual risk: reviewer may still dispute estimand choice (#1) — mitigated by honest framing.
