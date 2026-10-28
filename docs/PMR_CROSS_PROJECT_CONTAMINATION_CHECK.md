# PMR Cross-Project Contamination Check

Date: 2026-10-06 (UTC). Literal-string scan of all PMR-facing artifacts
in this package and the repository for denylisted terms (per the source
lock; see `docs/PMR_CONTAMINATION_ROOT_CAUSE.md`).

## Terms scanned

Tottori, Shimane, Okayama, Chugoku, Minimum Functional Guarantee,
"When Moving People Is Costly", relocation friction, mobile provision,
digital provision, asset preservation, settlement consolidation,
1-km, healthcare demand grid.

## Result: PASS

| Location scanned | Hits | Disposition |
|---|---|---|
| `docs/PMR_*.md`, `docs/PMR_SOURCE_LEDGER.csv`, `docs/PMR_ABSTRACT_RESULT_SYNC_AUDIT.md`, `docs/PMR_KYOTO_SHIGA_ADDITIONAL_ANALYSIS_RESULTS.md`, `docs/PMR_CROSS_PROJECT_CONTAMINATION_CHECK.md` | denylist terms appear ONLY in the contamination-audit and citation-ecology sections that name them to forbid them | allowed |
| `pmr_special_issue/*` (abstract + email, txt and docx) | 0 | clean |
| `data/processed/pmr_education_access/`, `outputs/pmr_education_access/`, `src/pmr/` | 0 | clean |
| `outputs/tables/prefectural_government_{offices,pair_distances}.csv` | Tottori/Shimane/Okayama rows | allowed — canonical national 1,081-pair office-distance computation (validated Kyoto–Shiga evidence; all 47 prefectures appear by design) |

No denylisted geography, service model, or result appears as a
Kyoto–Shiga empirical claim anywhere in PMR-facing artifacts.
