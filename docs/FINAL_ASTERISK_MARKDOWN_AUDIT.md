# FINAL ASTERISK / MARKDOWN AUDIT — v2

- Literal `*` count in journal-facing docx: manuscript v2 = 0, inline v2 = 0, cover letter v2 = 0 (python-docx paragraph scan). Prior v1 had 4 literal asterisks from inline `L*(Boundary ON)` in abstract and §3 prose — all removed; estimand notation is now `C(B) = L(ON) − L(OFF)` in OMML only.
- Raw markdown heading markers: prior build emitted literal "###" for level-3 headings in docx; builder now maps `### `→Heading 2. Zero "###" strings remain in docx text.
- No `**`, `_`, or other markdown residue in docx text. PASS.
