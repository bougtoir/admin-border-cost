# FINAL PMR Kyoto–Shiga Special-Issue Assessment

Date: 2026-10-05 (UTC). Scope: source-locked rebuild of PMR-facing artifacts
for the SI "Place-Based Strategy Design for Value Creation". No new
empirical analysis was run; the two extension functions are frozen and
labelled PLANNED.

## 1. Deliverables produced

| # | Path | Status |
|---|---|---|
| 1 | `docs/PMR_CONTAMINATION_ROOT_CAUSE.md` | created |
| 2 | `docs/PMR_SPECIAL_ISSUE_FIT_KYOTO_SHIGA.md` | created — judgment **A** (conceptual paper + worked example sufficient; two pre-specified extensions optional) |
| 3 | `docs/PMR_SOURCE_LEDGER.csv` | created — 26 claims, every empirical sentence traceable |
| 4 | `docs/PMR_CITATION_ECOLOGY_KYOTO_SHIGA.md` | created |
| 5 | `docs/PMR_KYOTO_SHIGA_FUNCTION_SELECTION_FREEZE.md` | created — selected: healthcare access, education access |
| 6 | `docs/PMR_KYOTO_SHIGA_ANALYSIS_FREEZE.md` | created — ON/OFF, constraints, equity metrics, sensitivities, interpretation rules pre-specified |
| 7 | `docs/PMR_KYOTO_SHIGA_NEW_DATA_PROVENANCE.md` | created — no data acquired yet; provenance protocol + stop rule |
| 8 | `docs/PMR_KYOTO_SHIGA_OVERLAP_AUDIT.md` | created |
| 9 | `pmr_special_issue/PMR_SI_ABSTRACT_PROPOSAL_KYOTO_SHIGA_FINAL.docx` | created |
| 10 | `pmr_special_issue/PMR_SI_ABSTRACT_PROPOSAL_KYOTO_SHIGA_FINAL.txt` | created — body ~670 words |
| 11 | `pmr_special_issue/PMR_SI_LATE_ENTRY_INQUIRY_KYOTO_SHIGA_FINAL.docx` | created |
| 12 | `pmr_special_issue/PMR_SI_LATE_ENTRY_INQUIRY_KYOTO_SHIGA_FINAL.txt` | created |
| 13 | this file | created |

Builder: `pmr_special_issue/build_pmr_docx.py` (docx regenerated from the
.txt sources; rerun after any text edit).

## 2. Verified call facts

- SI: "Place-Based Strategy Design for Value Creation", *Public Management
  Review*; guest editors Bianchi (Palermo), Nasi (Bocconi), Chen (Baruch),
  Lotta (FGV-São Paulo).
- Abstracts ≤1,000 words excluding references, Word format, emailed to
  guest editors; deadline 2026-05-31 **passed** → late-entry inquiry
  required (deliverables 11/12).
- Full paper deadline 2027-04-30; SI publication Q4 2027.

## 3. Denylist scan result

Literal-string scan over the repository for: Tottori, Shimane, Okayama,
Chugoku, 1-km, healthcare demand grid, Minimum Functional Guarantee,
"When Moving People Is Costly…", settlement consolidation, mobile
service, digital substitution, relocation friction, asset preservation.

**PASS** — zero occurrences in PMR-facing artifacts. The only hits are
(a) `outputs/tables/prefectural_government_{offices,pair_distances}.csv`,
the canonical national 1,081-pair computation that IS the validated
proximity result (all 47 prefectures necessarily appear); and
(b) contamination-audit / citation-ecology documentation that names the
denylisted terms to forbid them. Abstract, email, and all PMR docs are
clean.

## 4. Gate checklist

- [x] No unrelated project facts in PMR-facing artifacts.
- [x] Kyoto–Shiga is the only empirical geography.
- [x] All existing empirical claims trace to canonical sources
      (`docs/PMR_SOURCE_LEDGER.csv`, 26 rows).
- [x] New analyses, if any, are explicitly NEW and reproducible — frozen
      pre-computation; none run yet.
- [x] Planned analyses never written as completed (abstract and email
      label them "planned"/"proposed, not yet completed").
- [x] Electoral evidence remains one-function evidence.
- [x] SI fit evaluated, not assumed — judgment A with explicit weakness.
- [x] Late-entry email polished and ready to send.
- [x] Abstract ≤1,000 words excluding references (~670-word body).
- [x] Denylist contamination scan passes.
- [x] Source ledger audit passes.
- [x] No prior rejection history in inquiry.
- [x] No fabricated service results.

## 5. What was deliberately NOT done

- No full PMR manuscript was drafted (gated on SI admission + user go).
- No new data were downloaded and no service analyses were computed;
  both are frozen and pre-specified for a later pass.
- The canonical manuscript, values, and Political Geography submission
  package were not modified.
