# PMR Education-Access Evaluation Data (Kyoto–Shiga, F2)

Retrieved 2026-10-06 (UTC). This package is the evaluation dataset for the
pre-specified F2 (education access) extension analysis in
`docs/PMR_KYOTO_SHIGA_FUNCTION_SELECTION_FREEZE.md` /
`docs/PMR_KYOTO_SHIGA_ANALYSIS_FREEZE.md`. Supply-side (school points)
only; demand-side small-area populations are canonical project data
(r2ka JINKO, `docs/DATA_PROVENANCE.md` A1/A2).

## Contents

| File | Description |
|---|---|
| `raw/P29-21_GML.zip` | Immutable raw download from MLIT National Land Numerical Information (schools, 2021 data year). SHA-256 `1e161d40ec3319e6840628a3de524a84098c3be38157d54f82fcaa4ef0c37591`. |
| `p29_schools_kyoto_shiga_all.csv` | All 1,877 school points in Kyoto (26) + Shiga (25), all school types. |
| `p29_elementary_open_kyoto_shiga.csv` | 572 open elementary schools (incl. private). |
| `p29_elementary_open_public_kyoto_shiga.csv` | 571 open public elementary schools (F2 primary supply set). |
| `p29_junior_high_open_kyoto_shiga.csv` | 262 open junior-high schools (incl. private). |
| `p29_junior_high_open_public_kyoto_shiga.csv` | 256 open public junior-high schools (F2 primary supply set). |
| `build_education_access_data.py` | Regeneration script (`src/pmr/`). |

## Provenance

- Source: Ministry of Land, Infrastructure, Transport and Tourism (MLIT),
  National Land Numerical Information, dataset P29 学校 (schools).
- File: `https://nlftp.mlit.go.jp/ksj/gml/data/P29/P29-21/P29-21_GML.zip`
  (national file, 世界測地系 JGD2011, 57,230 records).
- Data year: 2021 (Reiwa-3); released 2022-03; chosen to match the
  2020-census geography. Latest 2023 release (P29-23) is a reduced
  national file kept as an alternative if a newer vintage is wanted.
- License/terms: MLIT National Land Numerical Information usage terms
  (attribution; free for research/redistribution under stated terms).
- Transformations: filter to prefecture codes 25/26; per-level open
  subsets (P29_007==1); public subsets (P29_006!=4). No coordinate or
  attribute edits; CRS remains JGD2011 to match the project's small-area
  geometry (JGD2000 ≈ JGD2011 at this scale — recorded, not converted).

## Interpretation rules (from the analysis freeze)

- Elementary and junior-high levels are analysed separately (a child
  cannot attend the other level's school).
- Closed schools (P29_007==9) are excluded from the open files; unverified
  code 0 records are retained only in the _all file.
- These are supply points; catchment/assignment results do not exist yet.
