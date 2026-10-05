# Case-selection analysis freeze (pre-ranking)

Frozen before any pair ranking is computed or inspected.
Commit context: branch `devin/1790984595-political-geography-retarget`,
base commit `b6d76986` (master, post-SEPS package). Freeze timestamp
(UTC): 2026-10-02 ~23:45. Purpose: decide, ex ante, how Kyoto–Shiga is
compared with alternative prefecture pairs so the case rationale cannot
be tuned post hoc.

## Comparison set (fixed)

Origin files (2020 Census Table 6-1, e-Stat, commuters + students,
municipality→municipality): prefecture-of-residence tables for every
prefecture adjacent to Kyoto-fu (26) or Shiga-ken (25):

- Kyoto (26) statInfId 000032222142 — already canonical (od_kyoto_61.xlsx)
- Shiga (25) statInfId 000032222141 — already canonical (od_shiga_61.xlsx)
- Osaka (27) statInfId 000032222143 — new download (od_osaka_61.xlsx)
- Hyōgo (28) statInfId 000032222144 — new download (od_hyogo_61.xlsx)
- Nara (29) statInfId 000032222145 — new download (od_nara_61.xlsx)
- Fukui (18) statInfId 000032222134 — new download (od_fukui_61.xlsx)
- Gifu (21) statInfId 000032222137 — new download (od_gifu_61.xlsx)
- Mie (24) statInfId 000032222140 — new download (od_mie_61.xlsx)
- Wakayama (30) statInfId 000032222146 — new download (od_wakayama_61.xlsx)

Wakayama and Gifu are included as justified interactors: Wakayama is an
Osaka-adjacent control for Kinki commuting structure; Gifu/Mie/Fukui are
Shiga-adjacent. Pairs reported (all adjacencies, no selection):

- Kyoto pairs: Kyoto–Shiga, Kyoto–Osaka, Kyoto–Hyōgo, Kyoto–Nara,
  Kyoto–Fukui (Kyoto's complete set of five prefectural borders).
- Shiga pairs: Shiga–Kyoto, Shiga–Mie, Shiga–Gifu, Shiga–Fukui
  (Shiga's complete set).
- Reference pairs (remaining land-border adjacencies among the
  comparator prefectures, exploratory): Osaka–Hyōgo, Osaka–Nara,
  Osaka–Wakayama, Nara–Wakayama, Nara–Mie, Mie–Gifu, Gifu–Fukui.

> Post-freeze correction (code review, 2026-10-03): the enumeration
> above replaces the original list, which included the non-adjacencies
> Kyoto–Mie, Hyōgo–Nara and Mie–Wakayama and omitted Nara–Wakayama,
> Nara–Mie and Gifu–Fukui. The corrected set still contains 15
> unordered pairs; metrics were unchanged.

## Metrics (fixed, computed before interpretation)

For each ordered pair (i → j):

1. F_ij — raw directional flow (sum of commuters+students, all
   municipality→municipality cells crossing the border, both directions
   are computed independently from the two residence tables).
2. F_bi = F_ij + F_ji — raw bidirectional.
3. R_ij = F_ij / T_i — PRIMARY directional measure; T_i = total
   commuters+students residing in prefecture i (all destinations,
   including within-prefecture). Interpretation: dependence of i's
   work/school geography on j.
4. R_ext_ij = F_ij / E_i — EXPLORATORY only; E_i = i's commuters going
   outside i. Share-of-external-trips.
5. S_ij = F_bi / (P_i + P_j) — PRIMARY symmetric normalized measure;
   P = 2020 census population (r2ka JINKO, same census vintage).
   Chosen before ranking because it is an interaction intensity per
   combined-capita and does not privilege either direction.
6. S2_ij = F_bi / sqrt(P_i P_j) — EXPLORATORY alternative gravity-style
   normalization, reported but not used for the headline claim.

## Directional asymmetry (fixed)

- Destination shares of every out-of-prefecture trip for Shiga
  residents and Kyoto residents (rank + magnitude).
- Whether Kyoto is the largest external prefectural destination for
  Shiga, and which prefecture is largest for Kyoto.
- Municipal concentration: for every municipality in Shiga (and Kyoto),
  the prefecture of its largest external destination (D_m =
  argmax_j F_mj over external prefectures); count/report municipalities
  whose largest external destination is Kyoto (resp. Osaka, Nara, …).
- HHI over destination-prefecture shares — exploratory, report only if
  it adds information beyond the share table.

## Proximity checks (separate from OD)

- Kyoto Sta.–Ōtsu Sta. rail time (JR Biwako Line; verify exact service
  and duration from JR West/official timetable sources).
- Kyoto Prefectural Government–Shiga Prefectural Government travel
  time/distance; the reported claim that they are the closest
  prefectural-government pair among the six Kinki prefectural
  governments must be independently verified before use.
- No "closest in Japan" claim without a nationwide check.

## Outputs (fixed)

- `data/processed/case_pref_flows.csv` — directional pair flows and
  denominators (all origins, all destination prefectures).
- `outputs/tables/case_selection_comparison_full.csv` — every pair,
  every metric, including results unfavorable to the case rationale;
  shipped in the reproducibility bundle.
- `outputs/tables/municipal_external_destinations.csv` — per-municipality
  largest external prefectural destination.
- `docs/CASE_SELECTION_AUDIT.md` — supported/unsupported hypotheses and
  what entered the manuscript.

Post-freeze additions are labeled exploratory in all outputs.
