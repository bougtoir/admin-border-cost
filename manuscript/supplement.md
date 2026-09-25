# Supplementary material

S1. District definitions (statutory, verbatim from 公職選挙法 別表第一) — in `config/config.yaml`.

S2. Unit construction details
- r2ka multi-polygon fragments: 420 rows merged into parent units (list in
  `outputs/diagnostics/geography_qc.json`).
- Bridging edges for isolated components (3 joins; islands: Okishima,
  Chikubushima environs; Awaji-side peninsular fragments n/a).
- Boundary-length tolerance sweep: real-border length at tol ∈ {0, 10, 30,
  50, 100} m (see `outputs/placebo/borders_meta.json` and Table S2 below).

S3. OD normalization sensitivity — severed-flow metrics under
  raw_bidirectional / origin_normalized / population_symmetric variants.

S4. Seed replicates — per-seed objectives and metrics (outputs/models/*.json,
  summarized in model_results.csv).

S5. Solver diagnostics — CP-SAT status/objective/bound/gap/runtime; SA
  acceptance curves and repair counts.

S6. Placebo matching diagnostics — accepted-border distributions of pop share,
  interface edges, boundary length vs the real border (borders_meta.json).

S7. MAUP — Level A vs B side-by-side metrics (Table T3).

S8. Computational environment — versions (requirements.txt), hardware
  (2 vCPU), runtime budget, deterministic seeds.
