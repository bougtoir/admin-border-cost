# FIGURE VISUAL QC — PMR REGULAR v2

Rendered clean (12 pp) and inline (15 pp) docx to PDF via LibreOffice, all pages rasterized and inspected.

## Figure files (standalone)
- Figure1_conceptual_framework.png: PASS — no overlaps, all six nodes boxed with padding, arrows clear, no title text, grayscale-legible.
- Figure2_kyoto_shiga_geography.png: PASS — title removed; axes, legend, point classes intact; no clipping.
- Figure3_cross_function_means.png: PASS — title removed (previous left-edge crop gone); bars + value labels + y-axis label intact.
- Figure4_border_tail_effects.png: PASS — title removed; legend, axis, both bar series intact.
- "Figure"/"Fig."/title strings inside images: NONE (generator has no set_title/suptitle; strings exist only in Word captions). PASS.

## Word rendering
| Page (inline) | Status | Note |
|---|---|---|
| p1–p15 all | PASS | no overflow, no broken boxes, tables complete |
| Fig 1 (p4) | PASS | caption above image; new layout renders clean |
| Fig 2 (p6) | PASS | map renders at full width, legend visible |
| Fig 3 (p10–11) | PASS | caption + bar chart paired correctly |
| Fig 4 (p11) | PASS | caption + chart paired correctly |
| clean docx Figures section (p12) | PASS | all four captions listed, order 1–4 |

## Checks
- Cropping/clipping in all figures: none.
- Axis/legend/note truncation: none.
- Element overlap: none.
- Font size: adequate at 6.0in placement width.
- Science/numbers: unchanged (bars encode canonical values; md byte-identical to v1).
- Verdict: PASS.
