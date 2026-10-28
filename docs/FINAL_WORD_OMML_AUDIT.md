# FINAL WORD OMML AUDIT — v2

python-docx XML inspection of both docx files:

- `manuscript_PMR_SI_KYOTO_SHIGA_FINAL_v2.docx`: m:oMath count = 1 (the §3 display estimand C(B) = L(Boundary ON) − L(Boundary OFF)); no raw LaTeX anywhere; no pseudo-equation text remains (the estimand line is converted to OMML by the builder). PASS.
- `manuscript_inline_PMR_SI_KYOTO_SHIGA_FINAL_v2.docx`: m:oMath = 1, same. PASS.
- Cover letter: oMath = 0 (no equations needed). PASS.
- Rendering check (LibreOffice PDF, p.5): equation renders cleanly as C(B)=L(Boundary ON)−L(Boundary OFF); earlier superscript/subscript OMML variants showed missing-glyph boxes and were rejected — plain-run OMML chosen for portability. PASS.
