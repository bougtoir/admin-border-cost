# admin_border_cost

The cost of an administrative-border constraint in electoral-district spatial
optimization: Kyoto-fu × Shiga-ken, Japan. Nonpartisan, fully reproducible
paired optimization (Boundary ON vs OFF) at two spatial scales.

## Layout
- `config/config.yaml` — districts, τ, weights, seeds, placebo, robustness
- `data/{raw,interim,processed}` — archived official inputs + built artifacts
- `src/` — download, geography, flows, projections, optimization (CP-SAT
  Level A / SA Level B), placebo, visualization, report
- `outputs/` — models (per-run JSON + assignments), figures, tables,
  placebo, diagnostics
- `manuscript/` — manuscript_text.md ({{key}} placeholders) → manuscript.docx
- `docs/` — DATA_PROVENANCE, METHODS_DECISIONS, DATA_DICTIONARY,
  REPRODUCIBILITY, LIMITATIONS, CLAIM_EVIDENCE_MATRIX
- `Makefile` — `make all` end-to-end

## Reproduce
```
python -m venv .venv && .venv/bin/pip install -r requirements.txt
make all
```
See docs/REPRODUCIBILITY.md. All manuscript numbers come from
`manuscript_values.csv`, generated only from run artifacts.
