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
MD = ROOT / "manuscript/manuscript_PMR_SI_KYOTO_SHIGA_FINAL_v2.md"
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
    name = "manuscript_inline_PMR_SI_KYOTO_SHIGA_FINAL_v2.docx" if inline else "manuscript_PMR_SI_KYOTO_SHIGA_FINAL_v2.docx"
    doc.save(OUT / name)
    print("wrote", OUT / name)


def cover_letter():
    doc = Document()
    style_doc(doc)
    body = """Dear Guest Editors,

I am pleased to submit "One administrative territory, multiple functional geographies: pricing territorial congruence in Kyoto–Shiga" for consideration in the Public Management Review special issue "Place-Based Strategy Design for Value Creation."

Governments routinely inherit a single territorial container — a prefecture, a district, a catchment — and run many different public functions inside it. Debates about territorial reform tend to oscillate between two poles: retain the container, or redraw it. This paper asks a prior, largely unmeasured question: what does requiring each function to respect the same boundary actually cost? I define a function-specific alignment opportunity cost C_s(B) — the difference between the best achievable objective when a function's plans must respect an inherited boundary and the matched problem with that restriction removed — and measure it for three domains on the Kyoto–Shiga prefectural boundary: electoral representation, healthcare access, and education access.

The result is, I believe, surprising in both directions. The aggregate price of congruence is near zero in every measured domain: the electoral boundary cost is bounded (and its best-found value at fine resolution is exactly zero), and the mean population-weighted access cost of the boundary is under seven metres for hospitals, clinics, elementary schools, and junior-high schools alike. But the averages are not the whole story. The measurable burden concentrates in eleven border municipalities, where the worst-decile access gap over interior areas shrinks markedly once the boundary is relaxed, and where individual small areas gain up to roughly 14–17 kilometres of avoided detour. Small aggregate cost, in other words, does not mean zero territorial consequence — it means the consequence is localized and function-specific in its distribution.

This changes the design implication. Where the average opportunity cost of an inherited boundary is low, wholesale territorial reform buys little; where marginal burdens are concentrated, the live option is selective permeability — retaining the administrative container while permitting targeted cross-boundary use for particular functions and places. I develop selective permeability as a place-based strategy implication to be evaluated, not as a tested policy.

The paper contributes directly to the special issue's concerns: it operationalizes the spatial locus of public-service ecosystems, connects inside-out and outside-in strategy through a priced estimand, separates aggregate efficiency from local distributive burden in public-value terms, and demonstrates a transparent protocol — declared estimand, paired Boundary ON/OFF design, placebo borders, declared solver status — under a prospective analysis freeze with full reproducibility artifacts.

I confirm that the manuscript is original, is not under consideration elsewhere, and uses only completed, auditable analyses.

Sincerely,
Tatsuki Onishi
Shiga University, Data Science and AI Innovation Research Promotion Center"""
    for para in body.split("\n\n"):
        doc.add_paragraph(para)
    doc.save(OUT / "cover_letter_PMR_SI_KYOTO_SHIGA_FINAL_v2.docx")
    print("wrote cover letter")


if __name__ == "__main__":
    build(inline=False)
    build(inline=True)
    cover_letter()
