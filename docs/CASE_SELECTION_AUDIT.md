# Case-Selection Audit — Kyoto–Shiga (Political Geography retarget)

Date: 2026-10-02 (UTC). Scope: documented validation of the Kyoto–Shiga
border pair before the manuscript's case-selection claims were written.
All comparisons were frozen *before* any ranking was produced; see
`docs/CASE_SELECTION_ANALYSIS_FREEZE.md` for the pre-specified
comparison set, metrics and falsification logic.

## 1. What was frozen before computing

- Comparison set (frozen): all five borders of Kyoto Prefecture
  (Osaka, Shiga, Nara, Hyogo, Fukui) plus Shiga's remaining borders
  (Mie, Gifu, Fukui) and the remaining adjacencies among the
  comparator prefectures (Osaka–Hyogo, Osaka–Nara, Osaka–Wakayama,
  Nara–Wakayama, Nara–Mie, Mie–Gifu, Gifu–Fukui) — 15 unordered pair
  rows in total. Post-freeze correction (2026-10-03, code review):
  the initial enumeration erroneously listed Kyoto–Mie, Hyogo–Nara and
  Mie–Wakayama (non-adjacencies) and omitted Nara–Wakayama, Nara–Mie
  and Gifu–Fukui; a first deduplication fix then wrongly dropped real
  municipalities ending in "0" (e.g. Yawata 26210). Final rule drops
  only "*00" totals plus the explicit designated-city-total set
  {14130, 14150, 22130, 27140, 40130}; all tables/values regenerated.
- Metrics (frozen): raw directional flows F_ij and F_ji, raw
  bidirectional F_bi; primary directional R_ij = F_ij/T_ij-commuters;
  primary symmetric S = F_bi/(P_i+P_j); exploratory R_ext = F_ij/E_i
  and S2 = F_bi/sqrt(P_i P_j). Populations P are 2020 census
  populations of the *prefectures* (r2ka), consistent with the OD
  table's geography.
- Anti-cherry-picking rule (frozen): every measure, including ones
  unfavourable to the study pair, is reported; no measure is dropped
  post hoc; a pair ranking first on any *pre-specified* measure is a
  positive result, ranking is otherwise stated as-is.

## 2. Data provenance

- 2020 Census OD, Statistics Bureau (e-Stat): Table 6-1 residence ×
  usual workplace/school prefecture pairs, same release family as the
  Kyoto/Shiga files already used by the pipeline
  (statInfId 000032222118–000032222130). Files added this session:
  `od_osaka_61.xlsx`, `od_hyogo_61.xlsx`, `od_nara_61.xlsx`,
  `od_fukui_61.xlsx`, `od_gifu_61.xlsx`, `od_mie_61.xlsx`,
  `od_wakayama_61.xlsx` under `data/raw/estat_census_od/`
  (SHA-256 ledgered in `data/raw/SHA256SUMS.txt`; downloader rows added
  to `src/download/fetch_all.py`).
- Prefecture populations: r2ka 2020 census ZIPs for prefs
  18, 21, 24, 27, 28, 29, 30, `data/raw/estat_r2ka/` (same ledger).
- Analytic code: `src/case_selection/build_case_selection.py`
  (same Table 6-1 row schema as `src/flows/build_flows.py`).

## 3. Results (all reported; unfavourable retained)

`outputs/tables/case_selection_comparison_full.csv` — 15 pair rows,
every frozen measure.

Headline pattern:

- Kyoto–Osaka is the largest *raw* bidirectional link: F_bi = 176,231
  vs Kyoto–Shiga 79,466. Osaka dominates raw volume, as expected of a
  metropolis of 8.84 M. **Not suppressed.**
- On the *pre-specified* normalized symmetric intensity
  S = F_bi/(P_i+P_j), Kyoto–Shiga ranks first among Kyoto's borders:
  0.0199 vs Kyoto–Osaka 0.0157, Kyoto–Nara 0.0094.
- Directional asymmetry is real and large:
  - Shiga→Kyoto R = 7.2% of all Shiga commuters/students; that trip is
    65.3% of all Shiga out-of-prefecture trips.
  - Kyoto→Shiga R = 1.8% (15.4% of Kyoto's external trips).
  - Kyoto→Osaka R = 7.1% — almost identical directional dependence
    for Kyoto in the opposite direction (polycentric Kyoto;
    Kyoto-oriented Shiga — "Fallback 2" pattern of the prompt).
  - Nara→Osaka R = 20.4% — a stronger single-direction dependence than
    Shiga→Kyoto. Retained in the table; Kyoto–Shiga is *not* the
    bloc maximum on this measure, and the manuscript says so.
- Municipal concentration: Kyoto is the largest external prefectural
  destination for **18 of 19** Shiga municipalities (sole exception:
  Maibara → Gifu, at the opposite end of the prefecture). For Kyoto's
  municipalities, Osaka is the top external destination for 24 and
  Shiga for 1 (Yamashina-ku, the ward directly adjoining Otsu) — i.e.
  the asymmetry is territorial, not driven by a single urban core.
- Pseudo-destinations "不詳・外国" / "不詳" (dest_pref codes 99998,
  99999) are excluded from external-flow and argmax calculations but
  kept in denominators T_i — documented in code.

## 4. Contextual verification (multi-source, sourced)

| Claim | Evidence | Source |
|---|---|---|
| Prefectural-office distance Kyoto↔Otsu = 10.45 km — closest of all 1,081 Japanese prefectural-government pairs (runner-up Saitama–Tokyo 18.97 km; margin 8.5 km) | PRIMARY: independently computed on GRS80 geodesic (pyproj.Geod) from MLIT National Land Numerical Information P02 public-facility data (2006), subclass 12001, one office per prefecture, 47/47 found — `src/case_selection/build_pref_office_distances.py`, `outputs/tables/prefectural_government_pair_distances.csv` |
| Otsu → Kyoto rail ≈ 10 min | JR Biwako Line rapid ≈ 9–10 min | JR West timetable / Otsu city documentation |
| "Keiji" (京滋) treated as an economic unit | RIETI–Kyoto University 2007 joint study "京滋地域企業の技術革新力に関する調査" (machinery/metal manufacturing cluster Kyoto-city vicinity → southern Shiga) | rieti.go.jp/jp/events/07111901/pdf/03_kodama_paper.pdf |
| Organizational "京滋" usage | Japan Institute of CPAs 京滋会 (Kyoto+Shiga); TKC近畿京滋会 (~400 members); 総合経済京滋税理士協同組合; corporate 京滋支店 | keiji.jicpa.or.jp; tkc.jp/kinki-keiji; protaag.com/keiji-zeikyo |
| Media footprint | Kyoto Shimbun circulation/subscription area = Kyoto + Shiga only; 滋賀本社 in Otsu | kyoto-np.co.jp corporate/area pages |
| Shared infrastructure/governance | Lake Biwa Canal (琵琶湖疏水) completed 1890, owned and operated by Kyoto City, draws Lake Biwa water at Otsu, still supplies Kyoto; Yodo-river basin shared water resource; both prefectures in Kansai Wide-Area Union | city.kyoto.lg.jp/suido/page/0000007153.html |
| History | Ōmi-shū / Ōtsu capital (667); Tōkaidō & Nakasendō through Ōtsu–Kusatsu | standard historical record |

## 5. Claim calibration

- "Closest prefectural-government pair in Japan" is now backed by a
  primary-data national computation: 10.45 km, rank 1 of 1,081 pairs
  on GRS80, runner-up Saitama–Tokyo 18.97 km (margin 8.5 km). The
  earlier secondary ranking (uub.jp: 10.5/19.0 km) is consistent and
  retained only as a cross-check, not the evidentiary basis.
- Coordinate vintage caveat: P02 is 2006-vintage; offices that
  relocated since would move their point, but an 8.5 km margin to rank
  2 makes the Kyoto–Shiga superlative robust to building-level error.
- No bilateral 京滋 cooperation council was found; governance claims
  therefore rest on shared water infrastructure (Biwako Canal,
  Yodo basin) and Kansai-wide bodies — stated as such.
- The manuscript must not claim Kyoto–Shiga is "the strongest
  functional divide/union" — it is *a* strongly entangled pair that
  also fails or underperforms on several measures (raw volume,
  Nara→Osaka directional share). That mixed picture is the honest
  justification: the pair is chosen because the *normalized,
  pre-specified* intensity is highest and the border case is a
  hard institutional test (two prefectural governments, not a
  functional-region boundary).
