# PMR Kyoto–Shiga — New-Data Provenance (FINAL)

Date: 2026-10-06 (UTC). Consolidated provenance for all data acquired for
the PMR extension analyses. Every entry follows
`docs/PMR_KYOTO_SHIGA_NEW_DATA_PROVENANCE.md` §1.

## Acquired

| Field | Value |
|---|---|
| Dataset | National Land Numerical Information, P29 学校 (schools) |
| Source | Ministry of Land, Infrastructure, Transport and Tourism (MLIT), nlftp.mlit.go.jp/ksj |
| URL | https://nlftp.mlit.go.jp/ksj/gml/data/P29/P29-21/P29-21_GML.zip |
| Version/date | 2021 data year (Reiwa-3), released 2022-03; national file, JGD2011, 57,230 records |
| Retrieval UTC | 2026-10-06 |
| License/status | MLIT National Land Numerical Information usage terms (attribution; research use permitted) |
| SHA-256 | 1e161d40ec3319e6840628a3de524a84098c3be38157d54f82fcaa4ef0c37591 (ledgered in `data/raw/SHA256SUMS.txt`) |
| Geographic coverage | National → filtered to Kyoto (admin codes 26xxx) + Shiga (25xxx) |
| Variables used | P29_001 admin area code; P29_002 school code; P29_003 school type; P29_004 name; P29_005 address; P29_006 admin type; P29_007 open/closed flag; point coordinates |
| Transformations | Prefecture filter (25/26); per-level open subsets (P29_007==1); public subsets (P29_006!=4). Builder: `src/pmr/build_education_access_data.py`. Raw archive untouched. |
| Outputs | `data/processed/pmr_education_access/p29_schools_kyoto_shiga_all.csv` (1,877); `p29_elementary_open_kyoto_shiga.csv` (572); `p29_elementary_open_public_kyoto_shiga.csv` (571); `p29_junior_high_open_kyoto_shiga.csv` (262); `p29_junior_high_open_public_kyoto_shiga.csv` (256) |

## Not yet acquired

- Healthcare facility points (candidate: MLIT P04 medical/welfare
  facilities, Kyoto + Shiga) — needed for F1.
- Demand-side centroids: reuse of canonical 2020 census small-area
  populations (A1/A2, `docs/DATA_PROVENANCE.md`) — permitted, no new
  acquisition required.

## Rule status

No data from any unrelated project is included. If further data cannot
be obtained under these rules, the extension stops and the paper
proceeds as conceptual + electoral worked example (§3 stop rule of the
provenance protocol).


## §5 P04 acquisition record (executed 2026-10-06)

| item | value |
|---|---|
| dataset | MLIT National Land Numerical Information P04, 医療機関 (medical institutions), 2020 vintage |
| URLs | https://nlftp.mlit.go.jp/ksj/gml/data/P04/P04-20/P04-20_25_GML.zip ; https://nlftp.mlit.go.jp/ksj/gml/data/P04/P04-20/P04-20_26_GML.zip (note: accessed as nlftp.mlit.go.jp for both) |
| retrieved (UTC) | 2026-10-06 ~03:25 |
| saved | data/raw/ksj_p04/P04-20_25_GML.zip ; data/raw/ksj_p04/P04-20_26_GML.zip |
| SHA-256 (25) | 7690d995a85b6ba6858187916232b46e58840885cbc9e9b6eefbeb8c9bc80b8d |
| SHA-256 (26) | 765a4970dc49b1f648e82e063df3d603fdcd24451ceb37b66ff5bd1da5404e62 |
| license | 国土数値情報利用規約 (MLIT terms of use; redistribution of raw data not republished) |
| records | Kyoto 3,960 / Shiga 1,692 = 5,652; tiers via P04_001: 1=hospital(221), 2=general clinic(3,584), 3=dental(1,847, excluded) |
| vintage note | P04-21/P04-22 per-prefecture zips return 404; P04-20 is the latest obtainable per-prefecture build and matches the 2020 census base year — recorded as a version note, not hidden |
| demand geography | r2ka25/r2ka26 re-downloaded 2026-10-06 from the e-Stat URLs in src/download/fetch_all.py; SHA-256 match the values in data/raw/estat_gis_boundary/SHA256SUMS.txt exactly (befa77…, de30f9…) |
