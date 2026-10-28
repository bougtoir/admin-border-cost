# PMR Kyoto–Shiga — Pre-Run Freeze Audit
Date: 2026-10-06 (before any ON/OFF run output was inspected)

| Frozen item | Status |
|---|---|
| Functions | F1 healthcare (MLIT P04, tier-specific: hospital and general-clinic separately), F2 education (MLIT P29, per-level: elementary, junior-high) — both implemented separately; no cross-tier/level pooling |
| Estimand | C_s(B) = L_s*(Boundary ON) − L_s*(Boundary OFF), identical settings otherwise |
| Demand geography | Canonical r2ka 2020 small areas, Kyoto(26)+Shiga(25): 11,978 units (12,398 fragment records merged on KEY_CODE), population JINKO total = 3,991,697 (matches manuscript), centroids = JINKO-weighted fragment representative points (X_CODE/Y_CODE, JGD2000); 1,043 zero-population units retained with weight 0 |
| Supply | F1: P04-20 (2020 vintage, 5,652 facilities; hospital tier n=221, clinic tier n=3,584, dental excluded). F2: P29-21 open public schools (elementary 571, junior-high 256) |
| Constraints | full coverage; capacity-neutral (uncapacitated nearest assignment) |
| Metrics | mean/median/p90/p95/max pop-weighted distance; threshold exceedance; OFF cross-boundary share; border vs interior mean and worst-decile gap; border municipalities with cross-assignment under OFF |
| Sensitivities | travel-time proxies (40 km/h drive, 4 km/h walk), household-weighted means |
| Interpretation | costs reported as measured; null/mixed retained; comparison descriptive only |

## Amendments recorded
- `PMR_KYOTO_SHIGA_ANALYSIS_AMENDMENT_2026-10-06.md`: (a) primary distance metric fixed as geodesic (WGS84 inverse) — the freeze's "shortest path on the planar graph of facility points and centroids" is operationally the nearest-facility geodesic under a complete point graph; travel-time is handled via the pre-specified speed assumptions as a sensitivity; (b) age-restricted demand weights for F2 could not be produced from r2ka (total JINKO + household counts only; census age tabulations are municipality-level, not small-area) — households (SETAI) used as the alternative weight instead; (c) capacitated sensitivity not run because P04/P29 carry no capacity attributes — inventing capacities is prohibited. All decisions made at implementation time, before inspecting any ON/OFF outcome.
