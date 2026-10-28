# FINAL audit — PMR Kyoto–Shiga executed analyses (2026-10-06)

1. Source lock honoured: every input is canonical Kyoto–Shiga (r2ka 25/26, P04-20 25/26, P29-21 filtered to 25/26, canonical adjacency/muni lookup). PASS
2. Contamination scan (denylist terms over docs/PMR_*, pmr_special_issue/*.txt, results/pmr_access/**): zero hits in deliverable-facing artifacts; matches appear only inside the two audit documents that name the excluded project by design (PMR_CONTAMINATION_ROOT_CAUSE.md, PMR_CROSS_PROJECT_CONTAMINATION_CHECK.md). PASS
3. Pre-run freeze audit written before outcome inspection: docs/PMR_KYOTO_SHIGA_PRE_RUN_FREEZE_AUDIT.md. PASS
4. Technical amendments documented outcome-blind: ANALYSIS_AMENDMENT_2026-10-06.md (geodesic-as-primary, SETAI weight, no capacitated run, tier map). PASS
5. P04 acquisition: official MLIT NLNI per-prefecture zips, retrieved 2026-10-06 UTC, SHA-256 recorded, persisted under data/raw/ksj_p04/. PASS
6. P04 availability caveat: P04-21/22 404 → P04-20 used; recorded in provenance. PASS
7. P29 reuse verified: elementary open-public 571 (freeze expectation 572 incl. all-open; 1 non-public), junior-high 256. Reconciled in education data README. PASS
8. Demand geography: 11,978 merged small areas, pop 3,991,697 exactly matches canonical totals; 1,043 zero-pop units retained at weight 0. PASS
9. Paired design: identical demand/supply/metric; only same-prefecture restriction differs. PASS
10. Estimand reported as C_s(B)=L_s*(ON)−L_s*(OFF); closed-form argmin (no solver gap claim). PASS
11. All frozen metrics reported per function incl. thresholds, cross-boundary share, border/interior, worst-decile gap, cross-assignment counts. PASS
12. Education per-level (elementary, junior-high) — no pooled headline. PASS
13. All pre-specified sensitivities run or amendment-documented; nothing EXPLORATORY silently relabelled. PASS
14. Cross-function comparison incl. electoral row; hypothesis classified "mixed / mostly similar magnitude". PASS
15. Results docs: HEALTHCARE_RESULTS.md, EDUCATION_RESULTS.md, CROSS_FUNCTION_INTERPRETATION.md, figures H1/E1/E2/X1, tables xlsx H1/E1/E2/X1. PASS
16. Source ledger extended KS-30..KS-35; claim matrix updated (CLAIM_EVIDENCE_MATRIX_PMR_UPDATED.csv). PASS
17. Abstract updated to completed results (~800 words ≤1,000); late-entry email untouched. PASS
18. GO/NO-GO recorded: docs/PMR_FULL_PAPER_GO_NO_GO.md → GO, class B. PASS
