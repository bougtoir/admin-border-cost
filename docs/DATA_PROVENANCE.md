# Data Provenance Ledger

All inputs are official Japanese government statistics acquired on 2026-09-24 (UTC).
SHA-256 checksums are recorded in `data/raw/SHA256SUMS.txt`. Raw files are immutable;
all processing writes to `data/interim` or `data/processed`.

| ID | Dataset | Source organization | File / URL | Access date | Version / release | Resolution | Terms |
|----|---------|--------------------|------------|-------------|-------------------|------------|-------|
| A1 | 2020 Population Census small-area boundaries + population (Kyoto pref., code 26) | Statistics Bureau of Japan (MIC), e-Stat Statistical GIS | https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=26&coordSys=1&format=shape&downloadType=5&datum=2000 → `data/raw/estat_gis_boundary/r2ka26_小地域境界_京都府_2020国勢調査.zip` | 2026-09-24 | Reiwa-2 (2020) census boundary set, released 2022-06-23 | 小地域 (small area, cho/oaza level); JGD2000 geographic | Government of Japan standard terms for statistics use (attribution); e-Stat terms of service |
| A2 | Same, Shiga pref. (code 25) | Statistics Bureau of Japan (MIC), e-Stat Statistical GIS | same endpoint, code=25 → `r2ka25_小地域境界_滋賀県_2020国勢調査.zip` | 2026-09-24 | 2022-06-23 | 小地域; JGD2000 | same |
| B1 | 2020 Census Table 6-1 OD: commuting/schooling municipality×municipality flows, usual-residence municipalities of Shiga pref. (statInfId 000032222141) | Statistics Bureau (MIC), e-Stat file-download | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222141&fileKind=0 → `data/raw/estat_census_od/od_shiga_61.xlsx` | 2026-09-24 | Released 2022-07-22 | 常住地市区町村 × 従業・通学地市区町村 (incl. wards of designated cities); 男女別, 総数 used | e-Stat terms |
| B2 | Same, Kyoto pref. (statInfId 000032222142) | same | statInfId=000032222142 → `od_kyoto_61.xlsx` | 2026-09-24 | 2022-07-22 | same | e-Stat terms |
| C1 | IPSS Regional Population Projections for Japan (2023 estimates), Result Table 1: total population & index by municipality, 2020–2050 | National Institute of Population and Social Security Research (IPSS) | https://www.ipss.go.jp/pp-shicyoson/j/shicyoson23/2gaiyo_hyo/kekkahyo1.xlsx → `data/raw/ipss/ipss_kekkahyo1.xlsx` | 2026-09-24 | Reiwa-5 (2023) projection, medium fertility/mortality | 市区町村 (incl. designated-city wards); 5-year steps 2020–2050 | IPSS citation requested |
| D1 | Public Offices Election Act (公職選挙法, Law No.100 of 1950), Appendix Table 1 (別表第一): single-member district definitions | e-Gov Law API (Ministry of Internal Affairs legal database) | https://elaws.e-gov.go.jp/api/1/lawdata/昭和二十五年法律第百号 → `data/raw/egov/公職選挙法_昭和25年法律第100号_2026-09-24取得.xml` | 2026-09-24 | as amended by the 2022 redistricting act (施行 2022-12-28) | whole municipalities / Kyoto-city wards; no sub-municipal splits in Kyoto or Shiga | public law text |
| D2 | MIC official district map (区割り図), Shiga | MIC Election Department | https://www.soumu.go.jp/main_content/000853831.pdf → `data/raw/soumu/滋賀県_区割り図_000853831.pdf` | 2026-09-24 | 2022 revision | prefecture map | soumu.go.jp terms |

## Verified institutional facts (as of access date)
- House of Representatives single-member districts: Kyoto-fu = 6 (1区–6区), Shiga-ken = 3 (1区–3区). Combined K = 9.
- Legal basis: 公職選挙法別表第一 as amended by the act promulgated 2022-11-28, effective 2022-12-28 (10増10減 revision; Shiga 4→3). Kyoto composition unchanged by that act.
- Shiga-ken districts (law text): 1区=大津市・高島市; 2区=彦根市・長浜市・近江八幡市・東近江市・米原市・蒲生郡・愛知郡・犬上郡; 3区=草津市・守山市・栗東市・甲賀市・野洲市・湖南市.
- Kyoto-fu districts: 1区=京都市北・上京・中京・下京・南区; 2区=左京・東山・山科区; 3区=伏見区・向日市・長岡京市・乙訓郡; 4区=右京・西京区・亀岡市・南丹市・船井郡; 5区=福知山市・舞鶴市・綾部市・宮津市・京丹後市・与謝郡; 6区=宇治市・城陽市・八幡市・京田辺市・木津川市・久世郡・綴喜郡・相楽郡.
- Population concept for comparison: 2020 census 総人口 (JINKO) by small area, aggregated to units; district population = sum of constituent municipality/ward populations.
- Note: district populations are compared on 2020 census population, matching the census base used by the 2022 Districting Council (衆議院議員選挙区画定審議会).

## Deviations / fallbacks
- Small-area (Level B) populations are taken from the JINKO attribute embedded in the official Statistical GIS boundary DBF (which is the census small-area aggregate itself), not a separate table.
- No e-Stat API key is required: official file-download endpoints and the Statistical GIS data endpoint were used. If e-Stat rate-limits future re-downloads, register an appId and re-run `make data` — checksums allow detecting any version drift.
