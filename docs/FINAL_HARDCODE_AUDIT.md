# FINAL HARDCODE AUDIT — v2

Every number in the v2 manuscript classified: GENERATED (from pipeline artifacts), SOURCE_METADATA (published dataset facts), LEGITIMATE_CONSTANT (definitions), HARDCODE_RISK, UNMAPPED.

Method: all prose numbers extracted and traced to the source map (FINAL_QC_SOURCE_MAP.md). Canonical registry: `manuscript/manuscript_values.csv` + `manuscript_values_kv.csv` + `docs/PMR_SOURCE_LEDGER.csv`.

- GENERATED: all ON/OFF means, deltas, shares, counts, max gains, worst-decile gaps, [0,532,293], Level-B 0.6245294675, placebo stats, travel-time sensitivity, cross shares. Verified equal to CSV sources. PASS.
- SOURCE_METADATA: 11,978 units / pop 3,991,697 / 1,043 zero-pop; 221/3,584/571/256 supply; 79,466 trips; 176,231; 18/19; 7.2%; 65.5%; 10.45188 km rank 1 / 1,081 pairs; census/register vintages. PASS.
- LEGITIMATE_CONSTANT: 11 border municipalities (defined geography), 47 prefectures → C(47,2)=1,081, tau=0.20, 40 km/h proxy. PASS.
- HARDCODE_RISK: none. The seconds values in Table 3 were a mislabel, now regenerated from sensitivity CSV (+0.41 s / +0.54 s). PASS.
- UNMAPPED: none.

Verdict: PASS. Prose numbers are manually written but each equals a canonical registry/source value; the builder injects no numbers.
