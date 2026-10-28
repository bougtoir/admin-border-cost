# PMR Kyoto–Shiga — Additional-Analyses Package (README)

Package: `PMR_KYOTO_SHIGA_ADDITIONAL_ANALYSES_FULL.zip`
Date: 2026-10-06 (UTC).

## Status up front

- Electoral representation: **COMPLETED** (canonical validated study).
- Healthcare access (F1): **NOT COMPLETED** — analysis frozen, supply
  data not yet acquired, no solver run exists.
- Education access (F2): **NOT COMPLETED** — analysis frozen; supply
  data acquired (MLIT P29 school points, Kyoto+Shiga) but the ON/OFF
  assignment solver was never run. No result artifacts exist.

This package therefore contains: all planning/freeze/provenance files,
the acquired education supply dataset, a supply-inventory map and
status tables — plus the electoral results cited as the reference
function. Nothing is fabricated.

## Layout

- `results/` — cross-function results summary
  (`PMR_KYOTO_SHIGA_ADDITIONAL_ANALYSIS_RESULTS.md`) with per-function
  status; `healthcare/` and `education/` hold status notes instead of
  result artifacts.
- `protocol/` — function-selection freeze, analysis freeze, and the
  freeze-compliance report.
- `data_provenance/` — final new-data provenance
  (`PMR_KYOTO_SHIGA_NEW_DATA_PROVENANCE_FINAL.md`).
- `data/` — education supply CSVs (`p29_*_kyoto_shiga*.csv`) and the
  supply-inventory map (`Figure_E0_SchoolSupply_Map.png`).
- `code/` — `build_education_access_data.py` (rebuilds the supply CSVs
  from the raw P29 archive).
- `tables/` — `Table_X1_CrossFunction_Summary.xlsx`,
  `Table_E1_Education_Results.xlsx`, `Table_H1_Healthcare_Results.xlsx`
  (status tables; no fabricated results).
- `pmr_submission/` — abstract proposal + late-entry inquiry (docx/txt)
  + `PMR_ABSTRACT_RESULT_SYNC_AUDIT.md`.
- `audit/` — `PMR_SOURCE_LEDGER.csv`, contamination check, electoral
  `CLAIM_EVIDENCE_MATRIX.csv`, final package audit.
- `logs/` — no solver logs exist (no runs performed); contains a note
  to that effect.

## Reproducing the education supply data

1. Download `https://nlftp.mlit.go.jp/ksj/gml/data/P29/P29-21/P29-21_GML.zip`
   and unzip (the zip is NOT redistributed inside this package; SHA-256
   `1e161d40ec3319e6840628a3de524a84098c3be38157d54f82fcaa4ef0c37591`).
2. Place `P29-21.geojson` under `data/raw/ksj_p29_schools/` in the repo.
3. `python src/pmr/build_education_access_data.py` → regenerates the
   CSVs under `data/processed/pmr_education_access/`.

Environment: Python 3.10+, pandas (CSV build uses only the stdlib
json/csv; tables/figures use pandas, openpyxl, matplotlib).
No solver runs exist to reproduce — the electoral pipeline is documented
in the repo root `README.md` / `docs/REPRODUCIBILITY.md`.
