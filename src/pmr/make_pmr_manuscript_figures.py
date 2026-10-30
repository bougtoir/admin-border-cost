"""Regenerate the four PMR manuscript figures from computed artifacts only.

Journal rule: figure numbers and titles live in the Word caption only.
No "Figure", "Fig.", or title text may appear inside the image files.
Figure 1 is a 2-row flowchart (the original single-row layout overlapped).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "outputs/pmr_manuscript/figures"
FIG.mkdir(parents=True, exist_ok=True)
CF = ROOT / "results/pmr_access/cross_function"
DEM = ROOT / "data/processed/pmr_demand"
HOS = ROOT / "data/processed/pmr_healthcare_access"

plt.rcParams.update({"figure.dpi": 200, "font.size": 10,
                     "font.family": "DejaVu Sans"})
C_ON, C_OFF = "#c0392b", "#2c7fb8"


def box(ax, x, y, w, h, text, fs=10):
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h,
                 facecolor="white", edgecolor="#2c3e50",
                 linewidth=1.4, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=3)


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#2c3e50",
                                lw=1.6, shrinkA=2, shrinkB=2))


def figure1():
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.set_axis_off()

    # Row 1 (top): inputs -> comparison
    box(ax, 1.7, 4.15, 2.9, 1.3,
        "Inherited administrative\nboundary $B$\n(Kyoto-fu | Shiga-ken)")
    box(ax, 5.0, 4.15, 2.9, 1.3,
        "Function $s$: feasible\nplans $F_s$, objective\n$L_s(\\cdot)$")
    box(ax, 8.3, 4.15, 2.9, 1.3,
        "Boundary ON plan\nvs boundary OFF\nplan (same $F_s$, $L_s$)")

    # Row 2 (bottom): estimand -> distribution -> decision
    box(ax, 1.7, 1.35, 2.9, 1.3,
        "Alignment opportunity\ncost\n$C_s(B) = L_s(\\mathrm{ON}) - L_s(\\mathrm{OFF})$")
    box(ax, 5.0, 1.35, 2.9, 1.3,
        "Decompose: aggregate\nmean AND local\n(border-decile) tails")
    box(ax, 8.3, 1.35, 2.9, 1.3,
        "Aggregate low but tail\nconcentrated $\\Rightarrow$\nselective permeability\nas design question")

    arrow(ax, 1.7, 3.50, 1.7, 2.00)
    arrow(ax, 5.0, 3.50, 5.0, 2.00)
    arrow(ax, 8.3, 3.50, 8.3, 2.00)
    arrow(ax, 3.15, 4.15, 3.55, 4.15)
    arrow(ax, 6.45, 4.15, 6.85, 4.15)
    arrow(ax, 3.15, 1.35, 3.55, 1.35)
    arrow(ax, 6.45, 1.35, 6.85, 1.35)

    fig.savefig(FIG / "Figure1_conceptual_framework.png",
                bbox_inches="tight")
    plt.close(fig)


def figure2():
    u = pd.read_csv(DEM / "smallarea_demand_units.csv")
    h = pd.read_csv(HOS / "p04_hospital_kyoto_shiga.csv")
    fig, ax = plt.subplots(figsize=(7, 7))
    inside = u[~u.border_muni]
    border = u[u.border_muni]
    ax.scatter(inside.lon, inside.lat, s=4, color="#8da0cb",
               label="interior small areas")
    ax.scatter(border.lon, border.lat, s=6, color="#d43d51",
               label="border municipalities (11)")
    ax.scatter(h.lon, h.lat, s=26, marker="^", color="black",
               label="hospitals (P04-20)")
    ax.set_xlabel("longitude (JGD2000)")
    ax.set_ylabel("latitude")
    ax.legend(loc="lower left", fontsize=9)
    fig.savefig(FIG / "Figure2_kyoto_shiga_geography.png",
                bbox_inches="tight")
    plt.close(fig)


def figure3():
    m = pd.read_csv(CF / "cross_function_metrics.csv")
    d = m[m.function.str.endswith("_ON_minus_OFF")]
    order = ["healthcare_clinic", "healthcare_hospital",
             "education_junior_high", "education_elementary"]
    labels = ["clinic", "hospital", "junior-high", "elementary"]
    vals = [float(d[d.function.str.startswith(f)].mean_km.iloc[0]) * 1000
            for f in order]
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    bars = ax.bar(labels, vals, color="#4878cf")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.1, f"+{v:.1f} m",
                ha="center", fontsize=10)
    ax.set_ylabel("mean ON\u2212OFF access cost (metres)")
    ax.set_ylim(0, max(vals) * 1.18)
    fig.savefig(FIG / "Figure3_cross_function_means.png",
                bbox_inches="tight")
    plt.close(fig)


def figure4():
    e = pd.read_csv(CF / "cross_function_equity_extra.csv")
    order = [("healthcare_hospital", "hospital"),
             ("healthcare_clinic", "clinic"),
             ("education_elementary", "elementary"),
             ("education_junior_high", "junior-high")]
    on, off, labels = [], [], []
    for f, lb in order:
        on.append(float(e.loc[e.function == f + "_ON",
                              "worst_decile_border_minus_interior_km"].iloc[0]))
        off.append(float(e.loc[e.function == f + "_OFF",
                               "worst_decile_border_minus_interior_km"].iloc[0]))
        labels.append(lb)
    x = range(len(labels))
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.bar([i - 0.2 for i in x], on, width=0.4, color="#d43d51",
           label="Boundary ON")
    ax.bar([i + 0.2 for i in x], off, width=0.4, color="#4878cf",
           label="Boundary OFF")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("worst-decile border\u2212interior gap (km)")
    ax.legend()
    fig.savefig(FIG / "Figure4_border_tail_effects.png",
                bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    figure1()
    figure2()
    figure3()
    figure4()
    print("done:", sorted(p.name for p in FIG.glob("Figure*.png")))
