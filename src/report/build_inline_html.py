"""Build a single self-contained HTML version of the inline manuscript
(values filled, figures embedded, math as MathML via the same rules as
the DOCX builder)."""
import base64
import re

import pandas as pd
from latex2mathml.converter import convert as latex_to_mathml

from .build_inline_docx import FIG, FIG_FILES, HEADER_LABELS, MAN, TAB, TABLES, fill
from .docx_rich import _MATH_SPAN_RE, _latex_for


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rich(text):
    """md inline (**bold**, *italic*, declared math) -> HTML."""
    out, last = [], 0
    for m in _MATH_SPAN_RE.finditer(text):
        latex = _latex_for(m.group(0))
        if latex is None:
            continue
        if m.start() > last:
            out.append(_italics(esc(text[last:m.start()])))
        out.append(latex_to_mathml(latex))
        last = m.end()
    out.append(_italics(esc(text[last:])))
    return "".join(out)

def _italics(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", t)
    return t

def table_html(csv_path):
    df = pd.read_csv(csv_path)
    h = ["<table><tr>"]
    for c in df.columns:
        h.append(f"<th>{rich(HEADER_LABELS.get(c, str(c)))}</th>")
    h.append("</tr>")
    for _, row in df.iterrows():
        h.append("<tr>" + "".join(f"<td>{esc(str(x))}</td>" for x in row) + "</tr>")
    h.append("</table>")
    return "".join(h)

def fig_html(fn):
    data = base64.b64encode((FIG / fn).read_bytes()).decode()
    return f'<img src="data:image/png;base64,{data}" style="max-width:100%;">'

def main():
    body = fill((MAN / "manuscript_text.md").read_text())
    parts = ["""<!doctype html><html><head><meta charset="utf-8">
<style>
body{font-family:'Times New Roman',serif;max-width:820px;margin:2em auto;
line-height:1.5;font-size:16px;padding:0 1em}
table{border-collapse:collapse;margin:1em 0;font-size:14px}
th,td{border:1px solid #444;padding:3px 8px}
h1{font-size:26px}h2{font-size:21px;border-bottom:1px solid #999}
h3{font-size:18px}.cap{font-weight:bold;font-size:14px}
</style></head><body>"""]
    fig_inserted, tab_inserted, skip = set(), set(), False
    for line in body.splitlines():
        s = line.rstrip()
        if s.startswith("## Figures") or s.startswith("## Tables"):
            skip = True; continue
        if s.startswith("## "):
            skip = False
        if skip and s.strip().startswith("- "):
            continue
        if s.startswith("# "):
            parts.append(f"<h1>{esc(s[2:])}</h1>")
        elif s.startswith("## "):
            parts.append(f"<h2>{rich(s[3:])}</h2>")
        elif s.startswith("### "):
            parts.append(f"<h3>{rich(s[4:])}</h3>")
        elif s.strip().startswith("- "):
            parts.append(f"<ul><li>{rich(s.strip()[2:])}</li></ul>")
        elif s.strip():
            parts.append(f"<p>{rich(s)}</p>")
        for cap, fn in FIG_FILES:
            tag = fn.split("_")[0]; num = tag[1:]
            if tag not in fig_inserted and re.search(rf"Figure {num}(?![\d-])", s) and (FIG/fn).exists():
                parts.append(f'<p class="cap">{esc(cap)}</p>{fig_html(fn)}')
                fig_inserted.add(tag)
        for cap, fn in TABLES:
            tag = fn.split("_")[0]; num = tag[1:]
            if tag not in tab_inserted and re.search(rf"Table {num}(?![\d-])", s) and (TAB/fn).exists():
                parts.append(f'<p class="cap">{esc(cap)}</p>{table_html(TAB/fn)}')
                tab_inserted.add(tag)
    parts.append("</body></html>")
    out = MAN / "manuscript_inline.html"
    out.write_text("".join(parts), encoding="utf-8")
    print(out, out.stat().st_size)

main()
