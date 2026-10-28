# PMR Kyoto–Shiga Extension — New-Data Provenance Protocol

Date: 2026-10-05 (UTC); updated 2026-10-06 with the F2 school-data
acquisition (section 4). This file
pre-specifies provenance requirements for the extension analyses frozen
in `docs/PMR_KYOTO_SHIGA_FUNCTION_SELECTION_FREEZE.md`. It is created
now so that any acquisition inherits the rules before it happens.

## 1. Requirements for any new dataset

Every new input must be Kyoto–Shiga-specific and documented with:

- official source URL;
- dataset name and version/release;
- retrieval timestamp (UTC);
- license/terms status;
- SHA-256 checksum (added to `data/raw/SHA256SUMS.txt`);
- geographic coverage;
- variables used;
- transformations applied (in `src/`, never manual edits to raw).

Raw originals are immutable snapshots under `data/raw/`; processing writes
only to `data/interim`/`data/processed`. Re-downloads never overwrite an
existing snapshot. Processed data from any unrelated project must not be
reused.

## 2. Planned sources (candidates, to verify at acquisition)

| Function | Planned source | Host | Notes |
|---|---|---|---|
| F1 Healthcare access | National Land Numerical Information, medical/welfare facilities (P04), Kyoto (26) + Shiga (25) archives | MLIT, nlftp.mlit.go.jp/ksj | Facility points; tier by facility class |
| F2 Education access | National Land Numerical Information, educational institutions, Kyoto + Shiga | MLIT, nlftp.mlit.go.jp/ksj | Public elementary/junior-high points |
| Demand weights | 2020 census small-area population (already held: A1/A2 in `docs/DATA_PROVENANCE.md`) | MIC e-Stat | Reuse of THIS project's canonical data is permitted |
| Optional travel time | Open road-network data only if license-clean; otherwise geodesic with speed assumption | TBD at acquisition | Recorded before solving |

## 4. Acquisitions to date

| Date (UTC) | Dataset | Source URL | Version | File | SHA-256 | Coverage | Status |
|---|---|---|---|---|---|---|---|
| 2026-10-06 | MLIT National Land Numerical Information P29 学校 (schools) | https://nlftp.mlit.go.jp/ksj/gml/data/P29/P29-21/P29-21_GML.zip | 2021 data year (released 2022-03), JGD2011 | `data/raw/ksj_p29_schools/P29-21_GML.zip` (ledgered in `data/raw/SHA256SUMS.txt`) | 1e161d40ec3319e6840628a3de524a84098c3be38157d54f82fcaa4ef0c37591 | national; filtered to Kyoto 26 + Shiga 25 → `data/processed/pmr_education_access/` | acquired, processed CSVs built by `src/pmr/build_education_access_data.py` |

Evaluation package delivered as `pmr_education_access_data_v1.zip`
(supply-side school points; see `data/processed/pmr_education_access/README.md`).

## 5. Stop rule

If suitable official data cannot be obtained and ledgered, the empirical
extension **stops**: the PMR paper proceeds as conceptual + electoral
worked example only. No service analysis may be fabricated or imported
from another project.
