"""Build clean + inline PMR manuscript DOCX and cover letter DOCX.

Clean: prose only (figures/tables listed at end; figures/tables as separate files
per journal convention). Inline: figures and tables embedded at the end of the
relevant section. Times New Roman 12pt body, 10pt captions, black text, OMML
equation for the estimand.
"""
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "manuscript/manuscript_PMR_REGULAR_KYOTO_SHIGA_FINAL_v1.md"
FIGDIR = ROOT / "outputs/pmr_manuscript/figures"
TABDIR = ROOT / "outputs/pmr_manuscript/tables"
OUT = ROOT / "manuscript"

FIGMAP = {
    "Figure 1": FIGDIR / "Figure1_conceptual_framework.png",
    "Figure 2": FIGDIR / "Figure2_kyoto_shiga_geography.png",
    "Figure 3": FIGDIR / "Figure3_cross_function_means.png",
    "Figure 4": FIGDIR / "Figure4_border_tail_effects.png",
}
TABMAP = {
    "Table 1": TABDIR / "Table1_functions_data_methods.csv",
    "Table 2": TABDIR / "Table2_cross_function_results.csv",
    "Table 3": TABDIR / "Table3_sensitivity.csv",
}

OMML_ESTIMAND = "C(B) = L(Boundary ON) − L(Boundary OFF)"


def style_doc(doc):
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    st.font.color.rgb = RGBColor(0, 0, 0)


def add_math_para(doc, text):
    """Add an OMML display equation; text uses _ subscript and ^ superscript."""
    p = doc.add_paragraph()
    p.alignment = 1
    omml = OxmlElement("m:oMathPara")
    omath = OxmlElement("m:oMath")
    tokens = re.split(r"(_|\^)", text)
    i = 0
    cur = omath
    run_text = ""
    def flush(txt):
        if not txt:
            return
        r = OxmlElement("m:r")
        t = OxmlElement("m:t")
        t.text = txt
        t.set(qn("xml:space"), "preserve")
        r.append(t)
        omath.append(r)
    # simple parser: handle 'X_y' and 'X^y' inline
    buf = ""
    parts = re.findall(r"[A-Za-z0-9()=−* ]+|_\S+|\^\S+", text)
    for tok in parts:
        if tok.startswith("_"):
            base = buf
            buf = ""
            ssub = OxmlElement("m:sSub")
            e = OxmlElement("m:e"); se = OxmlElement("m:sub")
            for el, val in ((e, base), (se, tok[1:])):
                r = OxmlElement("m:r"); tt = OxmlElement("m:t")
                tt.text = val; tt.set(qn("xml:space"), "preserve")
                r.append(tt); el.append(r)
            ssub.append(e); ssub.append(se); omath.append(ssub)
        elif tok.startswith("^"):
            base = buf; buf = ""
            ssup = OxmlElement("m:sSup")
            e = OxmlElement("m:e"); su = OxmlElement("m:sup")
            for el, val in ((e, base), (su, tok[1:])):
                r = OxmlElement("m:r"); tt = OxmlElement("m:t")
                tt.text = val; tt.set(qn("xml:space"), "preserve")
                r.append(tt); el.append(r)
            ssup.append(e); ssup.append(su); omath.append(ssup)
        else:
            # check trailing base char for sub/sup
            if tok.endswith("(") or " " in tok or tok == "":
                flush(tok)
            else:
                if buf:
                    flush(buf)
                buf = tok
    if buf:
        flush(buf)
    omml.append(omath)
    p._p.append(omml)


def add_table(doc, csv_path, caption):
    df = pd.read_csv(csv_path)
    p = doc.add_paragraph()
    r = p.add_run(caption)
    r.font.size = Pt(10)
    tbl = doc.add_table(rows=1, cols=len(df.columns))
    tbl.style = "Table Grid"
    for j, c in enumerate(df.columns):
        cell = tbl.rows[0].cells[j]
        run = cell.paragraphs[0].add_run(str(c))
        run.bold = True; run.font.size = Pt(10)
    for _, row in df.iterrows():
        cells = tbl.add_row().cells
        for j, v in enumerate(row):
            run = cells[j].paragraphs[0].add_run(str(v))
            run.font.size = Pt(10)


def add_figure(doc, fig_path, caption):
    p = doc.add_paragraph()
    r = p.add_run(caption)
    r.font.size = Pt(10)
    doc.add_picture(str(fig_path), width=Inches(6.0))


def is_md_table_line(l):
    return l.strip().startswith("|")


def build(inline: bool):
    doc = Document()
    style_doc(doc)
    text = MD.read_text()
    paras = text.split("\n")
    fig_captions = {}
    tab_captions = {}
    for line in paras:
        m = re.match(r"^(Figure \d+)\. (.+)$", line.strip())
        if m:
            fig_captions[m.group(1)] = m.group(0)
        m = re.match(r"^(Table \d+)\. (.+)$", line.strip())
        if m:
            tab_captions[m.group(1)] = m.group(0)

    in_refs = False
    for raw in paras:
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("# "):
            doc.add_heading(line[2:].strip(), level=0)
            continue
        if line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=2)
            continue
        if line.startswith("## "):
            h = line[3:].strip()
            if h == "References":
                in_refs = True
            if h == "Figures and tables":
                continue
            doc.add_heading(h, level=1)
            continue
        if re.match(r"^(Figure|Table) \d+\.", line.strip()):
            continue  # captions emitted with assets or at end
        # strip markdown bold/italics markers for plain docx
        clean = line.replace("**", "")
        if clean.startswith(("Author:", "Keywords:")):
            p = doc.add_paragraph()
            p.add_run(clean).bold = True
            continue
        # inline figure/table insertion points
        if inline:
            inserted = False
            for fname in ("## 5.", "section"):  # placeholder
                pass
            # after specific paragraphs, embed assets
            pass
        if clean.startswith(("C(B) = ", "C_s(B) = ")):
            add_math_para(doc, OMML_ESTIMAND)
            continue
        doc.add_paragraph(clean)
        if inline:
            t = clean
            if "Figure 1" in t and fig_captions.get("Figure 1"):
                add_figure(doc, FIGMAP["Figure 1"], fig_captions["Figure 1"])
            if "Figure 2" in t and fig_captions.get("Figure 2"):
                add_figure(doc, FIGMAP["Figure 2"], fig_captions["Figure 2"])
            if "Figure 3" in t and fig_captions.get("Figure 3"):
                add_figure(doc, FIGMAP["Figure 3"], fig_captions["Figure 3"])
            if "Figure 4" in t and fig_captions.get("Figure 4"):
                add_figure(doc, FIGMAP["Figure 4"], fig_captions["Figure 4"])
            if "Table 1 summarizes" in t:
                add_table(doc, TABMAP["Table 1"], tab_captions["Table 1"])
            if "Table 2" in t:
                add_table(doc, TABMAP["Table 2"], tab_captions["Table 2"])
            if "Table 3" in t:
                add_table(doc, TABMAP["Table 3"], tab_captions["Table 3"])
    if not inline:
        doc.add_heading("Figures", level=1)
        for k in sorted(fig_captions):
            p = doc.add_paragraph(); p.add_run(fig_captions[k]).font.size = Pt(10)
        doc.add_heading("Tables", level=1)
        for k in sorted(tab_captions):
            p = doc.add_paragraph(); p.add_run(tab_captions[k]).font.size = Pt(10)
    name = "manuscript_inline_PMR_REGULAR_KYOTO_SHIGA_FINAL_v1.docx" if inline else "manuscript_PMR_REGULAR_KYOTO_SHIGA_FINAL_v1.docx"
    doc.save(OUT / name)
    print("wrote", OUT / name)


def cover_letter():
    doc = Document()
    style_doc(doc)
    body = """Dear Editor,

I am pleased to submit "One administrative territory, multiple functional geographies: pricing territorial congruence in Kyoto–Shiga" for consideration as a regular article in Public Management Review.

Governments routinely organize multiple functions within inherited territorial containers, yet the opportunity cost of requiring those functions to respect one common boundary is rarely measured. This paper operationalizes territorial congruence as a measurable design variable — a function-specific alignment opportunity cost defined as the difference between the best achievable objective when a function's plans must respect an inherited boundary and the matched problem with that restriction removed — and measures it across three domains on the Kyoto–Shiga prefectural boundary in Japan: electoral representation, healthcare access, and education access.

The counterintuitive result is twofold. Aggregate boundary costs are small in every domain examined: the electoral cost is bounded at [0, 532,293] objective units (with a best-found value of zero at small-area resolution), and the mean population-weighted access cost of the boundary is under seven metres for hospitals, clinics, elementary schools, and junior-high schools alike. Yet the residual burden is spatially concentrated: measurable penalties cluster in eleven border municipalities, where the worst-decile access gap over interior areas narrows markedly once the boundary restriction is relaxed.

This finding shifts the design question from wholesale boundary reform toward selective territorial permeability — retaining the administrative container where its aggregate price is low while evaluating targeted cross-boundary access where local penalties are concentrated. The paper speaks to Public Management Review's core concerns: place-based strategy, public-service ecosystems, public value, and cross-jurisdiction service design. Selective permeability is developed as a design implication to be evaluated, not as a tested optimal policy.

All results are computed from official Japanese public data (2020 Population Census, MLIT National Land Numerical Information, the Public Offices Election Act constraint). The full analysis code and data pipeline are public, and the reported results have been reproduced from a clean clone of the public repository, with a complete provenance and quality-control ledger accompanying the submission.

Following an inquiry concerning a now-closed Public Management Review special issue, Professor Carmine Bianchi kindly encouraged me to consider submitting the completed paper through the journal's regular submission process.

I confirm that the manuscript is original, is not under consideration elsewhere, and has a single author.

Sincerely,
Tatsuki Onishi
Shiga University, Data Science and AI Innovation Research Promotion Center"""
    for para in body.split("\n\n"):
        doc.add_paragraph(para)
    doc.save(OUT / "cover_letter_PMR_REGULAR_KYOTO_SHIGA_FINAL_v1.docx")
    Path(OUT / "cover_letter_PMR_REGULAR_KYOTO_SHIGA_FINAL_v1.txt").write_text(body)
    print("wrote cover letter")


def title_page():
    doc = Document()
    style_doc(doc)
    doc.add_heading("Title page", level=1)
    for para in [
        "Title: One administrative territory, multiple functional geographies: pricing territorial congruence in Kyoto–Shiga",
        "Author: Tatsuki Onishi (corresponding author)",
        "Affiliation: Shiga University, Data Science and AI Innovation Research Promotion Center",
        "Article type: Regular article",
        "Declarations: The author declares no competing interests. No funding was received for this work. Data availability: all inputs are official Japanese public data; code and processed artifacts are available in the public repository bougtoir/admin-border-cost.",
        "Anonymization: the main manuscript is anonymized for double-anonymous review; this title page is submitted separately.",
    ]:
        doc.add_paragraph(para)
    doc.save(OUT / "title_page_PMR_REGULAR_KYOTO_SHIGA_FINAL_v1.docx")
    print("wrote title page")


if __name__ == "__main__":
    build(inline=False)
    build(inline=True)
    cover_letter()
    title_page()
