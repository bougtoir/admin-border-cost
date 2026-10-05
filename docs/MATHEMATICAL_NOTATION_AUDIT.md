# MATHEMATICAL NOTATION AUDIT — underscore token classification

Date: 2026-10-03. Scope: all journal-facing DOCX artifacts
(manuscript.docx, manuscript_inline.docx, cover_letter.docx,
highlights.docx) plus their markdown sources.

Category A = mathematical notation → OMML.
Category B = machine variable used as scientific notation →
publication header label.
Category C = file path / code / dataset identifier → retained.
Category D = other.

## Tokens found in DOCX (post-repair state)

Extracted from all four journal-facing DOCX files:

| Token | Category | Action |
|---|---|---|
| CASE_SELECTION_ANALYSIS_FREEZE (in docs/ path) | C | retained — literal doc path |
| CASE_SELECTION_AUDIT (docs/ path) | C | retained |
| METHODS_DECISIONS (docs/ path) | C | retained |
| r2ka_*.zip, od_*.xlsx (T1 data-source cells) | C | retained — raw filenames; wildcard `*` intentional |
| ipss_kekkahyo1 (T1 raw-path cell) | C | retained — filename |
| law_kosenkyoho (T1 raw-path cell) | C | retained — filename |

No category-A or B underscore token remains in any journal-facing
DOCX after repair.

## Tokens converted (source markdown → OMML rules in
src/report/docx_rich.py)

| Source token | Category | Rendered as |
|---|---|---|
| F_ij, F_ji | A | F_{i→j}, F_{j→i} (rewritten to F_{i→j} in source; legacy rule retained) |
| F_bi | A | F_{ij}^{bi} |
| R_ij = F_ij/T_i | A | R_{i→j} = F_{i→j}/T_i (OMML fraction) |
| R_ext | A | R_ext (true "ext" subscript) |
| S2 (normalization metric) | A | S_2 (true subscript) |
| S = F_bi/(P_i+P_j) | A | S_{ij} = F_{ij}^{bi}/(P_i+P_j) (OMML fraction) |
| S = value (results prose) | A | S_{ij} = value |
| T_i, P_i, P_j | A | T_i, P_i, P_j (subscript OMML) |
| Cost_border = L*(Boundary ON) − L*(Boundary OFF) | A | C_border = L*(Boundary ON) − L*(Boundary OFF) |
| C_s(B) = L_s*(B) − L_s*(0) ≥ 0 | A | OMML, pre-existing |
| D_s* = argmin_D L_s(D) | A | OMML, pre-existing |
| F_B ⊂ F_0, F_B, F_0 | A | OMML, pre-existing |
| L_s(D), L_s(B), L_s(0), L_s, D_s*, C_s(B), C(B) | A | OMML, pre-existing |
| L*_OFF ≤ L*_ON, L*_ON, L*_OFF | A | OMML, pre-existing |
| τ, ±τ | A | OMML τ, pre-existing |
| max\|dev\| | A | \|dev\|_max OMML |
| max/min | A | max/min OMML |
| ±20%, ±10%, ±50%, ±10% km | A | OMML, pre-existing |

## Tokens intentionally retained (not math)

- `S1`, `S2` as IPSS projection-scenario labels (M4 bullet, future
  robustness) — literal scenario names, not indexed math.
- All `{{token}}` template keys (filled from manuscript_values.csv —
  none survives into DOCX).
- `M0`–`M5`, `M2-ON`, `M3-OFF`, `I8` — model/invariant labels.
- File paths, repo doc names, config.yaml.

## Table headers (B → publication labels)

Applied at DOCX render time in build_inline_docx.py HEADER_LABELS —
the underlying CSV column names are unchanged (canonical machine
files):

| CSV column | DOCX header |
|---|---|
| pair | border pair |
| flow_i_to_j | F_{i→j} (OMML) |
| flow_j_to_i | F_{j→i} (OMML) |
| flow_bidirectional | F_{ij}^{bi} (OMML) |
| R_i_to_j_pct | R_{i→j} (%) (OMML) |
| R_j_to_i_pct | R_{j→i} (%) (OMML) |
| S_pct | S_{ij} (%) (OMML) |
| tau | τ |
| splits | munis split |
| severed | severed |
| max\|dev\|, max/min | OMML rules apply |

T5 (statistic/value), T6 (model/years) needed no change.
