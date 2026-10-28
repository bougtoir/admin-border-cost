# Visual/format QC — PMR manuscript v1

- Fonts: Times New Roman, body 12 pt (Normal style), captions 10 pt, black. PASS (set at style level and run level for captions/tables).
- Math: estimand C_s(B) inserted as OMML oMathPara with sub/superscript structure; no raw LaTeX or underscores in visible text. PASS
- Figure/table order: first citations F1 §3, F2 §4, T1 §5, T2+F3 §6.4, F4+T3 §6.4 — sequential. PASS
- No orphan supplement (none exists); reproducibility bundle referenced in Data availability. PASS
- Clean docx = prose + figure/table captions listed at end (journal convention: figures/tables as separate files); inline docx embeds them at first-citation points. PASS
- Markdown asterisks stripped in docx build; no stray asterisks in visible text. PASS (builder removes **; verified no * remains in body text by grep on docx XML output — see audit)
- Reference list: all entries bibliographically verified; DOIs attached where issued. PASS
