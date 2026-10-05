# Reproducibility

## Environment
- Python 3.10, venv at `.venv`; pinned deps in `requirements.txt` (geopandas,
  ortools, pandas, numpy, scipy, networkx, matplotlib, shapely, pyproj,
  openpyxl, python-docx, pyarrow, pyyaml, pydantic).
- `python -m venv .venv && .venv/bin/pip install -r requirements.txt`

## Data acquisition
Raw files are fetched once into `data/raw/` and hashed into
`data/raw/SHA256SUMS.txt`; `docs/DATA_PROVENANCE.md` records URL, retrieval
time (UTC), version, license/terms, and checksum for every file.
Scripts: `src/download/fetch_all.py` re-downloads into a fresh directory
(never overwrites archived snapshots).

## One-command rebuild
```
make all          # data -> primary (A+B) -> placebo -> figures/tables -> manuscript -> qc
make data         # geography + flows + projections
make levelA       # CP-SAT batch (M1,M2,M3,M4 x seeds, tau sensitivity, M5)
make levelB       # SA batch warm-started from Level A
make placebo      # 200 matched borders x ON/OFF solves
make figures tables manuscript qc
```

## Traceability
- Every number in the manuscript is a `{{key}}` filled from
  `manuscript/manuscript_values.csv`, itself generated only from
  `outputs/models/*.json` and processed data — no prose number is hard-coded.
- `outputs/diagnostics/QC_REPORT.json` audits checksums, run inventory,
  feasibility, pairing, placebo completeness, and value coverage.
- `docs/CLAIM_EVIDENCE_MATRIX.csv` maps each manuscript claim to the
  artifact(s) that support it.

## Determinism notes
- CP-SAT uses `random_seed` + fixed worker count; results are reproducible in
  objective value up to solver nondeterminism under time limits (gaps are
  reported, not hidden).
- SA uses fixed seeds (config `optimization.seeds`); plots/metrics are
  deterministic given the seed list.
- CRS: EPSG:6674 (JGD2011 Plane Rectangular VI).
