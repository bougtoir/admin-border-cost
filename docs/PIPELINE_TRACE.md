# Pipeline trace — claim → code → artifacts

| Claim/value | Source script | Inputs | Output artifact |
|---|---|---|---|
| 55 Level A units / 11,978 Level B units | src/geography/build_geography.py | data/raw r2ka_25/26 | data/processed/*.parquet |
| adjacency + shared-boundary weights (30 m tol) | src/geography/build_geography.py | unit geometries | data/processed/adj_*.csv |
| OD flow matrix (municipal, ward-resolved) | src/flows/build_flows.py | e-Stat Census Table 6-1 | data/processed/od_region_matrix_sym.csv |
| n_cross = 79,466 cross-pref trips | build_flows (raw OD, non-symmetrized, both directions) | od_muni.csv | manuscript_values.csv |
| M0–M5 Level A runs | src/optimization/cpsat_levelA.py (CP-SAT, 300 s) | units A, adj, flow | outputs/models/A_*.json + _assign.csv |
| M0–M5 Level B runs | src/optimization/local_search_levelB.py (SA + repairs) | units B | outputs/models/B_*.json + _assign.csv |
| metrics (pop/compact/split/flow/future/durability) | src/optimization/metrics.py | assign + units + od | inside each *_json |
| 200 placebo borders | src/placebo/gen_placebo.py | units A | outputs/placebo/borders.csv |
| placebo costs | src/placebo/run_placebo.py (heuristic solve_one_h) | borders | outputs/placebo/placebo_results.csv |
| real border priced on same heuristic | src/placebo/real_border_cost.py | group=pref | outputs/placebo/real_border_cost.json |
| cross-OD per border | audit (cross_od.csv) | borders + od sym | outputs/placebo/cross_od.csv |
| aggregated values | src/report/aggregate_results.py | all above | manuscript/manuscript_values.csv |
| tables T1–T6 | src/report/make_tables.py | model_results.csv, placebo | outputs/tables/T*.md/.csv |
| figures F1–F7 | src/visualization/make_figures.py | geo + results | outputs/figures/*.png |
| manuscript docx | src/report/build_manuscript.py | manuscript_text.md + values | manuscript/manuscript.docx |
| inline docx | src/report/build_inline_docx.py | same + figures/tables | manuscript/manuscript_inline.docx |
| invariants I1–I8 | tests/test_invariants.py | saved assigns + logs | make qc |
| nesting reruns | src/audit/nested_off_runs.py, nested_off_cpsat.py | ON incumbents | outputs/models/*_nested* |
| future-assignment audit | assign-hash comparison | all _assign.csv | outputs/tables/future_assignment_audit.csv |
