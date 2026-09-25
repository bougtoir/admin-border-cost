# Data dictionary

## data/processed/units_smallarea.gpkg (11,978 units)
| column | meaning |
|---|---|
| unit_id | census small-area code (KEY_CODE; multi-polygon fragments merged) |
| muni_code / muni_name | municipality or ward (55 units) |
| pref_code | 25 = Shiga, 26 = Kyoto (JIS) |
| district | statutory district label (滋賀1区…京都6区) |
| pop, households | 2020 census population / households |
| geometry | JGD2011 plane-rectangular VI (EPSG:6674) |

## data/processed/adj_smallarea_edges.csv / _weighted.csv
Queen adjacency edge list: `i`,`j` = row indices into the units table
(weighted file adds `w` = shared boundary length m, 30 m tolerance) plus
recorded bridging edges for 3 isolated components (see geography_qc.json).

## data/processed/units_muni.gpkg, muni_lookup.csv
Municipality/ward dissolve (55 units); lookup gives statutory `district` and
total `pop` per unit.

## data/processed/od_muni.csv, od_region_matrix_{raw,sym}.csv
Census Table 6-1 OD at municipality/ward resolution: `origin`,`dest`,
`flow`, names. Region matrix retains pairs inside Kyoto+Shiga; `sym` =
(F + Fᵀ)/2 used in the severed-flow objective and metrics.

## data/processed/muni_projections.csv, unit_projections.parquet
IPSS 2023 projections: `growth` = year-pop/2020-pop per municipality;
unit_projections disaggregates to small areas under scenarios S1
(proportional) and S2 (±10% centroid-drift sensitivity).

## outputs/models/{A,B}_<model>_<on|off>_tau<τ>_s<seed>.json / _assign.csv
Per-run record: solver status/objective/bound/gap/runtime and full metrics.
`*_assign.csv` maps `unit_id` → district index (Level A: muni code; B: unit).

## outputs/placebo/{borders.csv, borders_meta.json, placebo_results.csv}
200 matched placebo borders (group vector), matching diagnostics, and paired
ON/OFF objective results per border.
