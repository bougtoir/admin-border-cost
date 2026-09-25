"""Figures F1–F7 from computed artifacts only (no hard-coded numbers)."""
import json
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
OUT = ROOT / "data/processed"
MODELS = ROOT / "outputs/models"
FIG = ROOT / "outputs/figures"
FIG.mkdir(parents=True, exist_ok=True)
PLAC = ROOT / "outputs/placebo"

plt.rcParams.update({"figure.dpi": 200, "font.size": 9,
                     "font.family": "DejaVu Sans"})
C_ON, C_OFF, C_CUR = "#c0392b", "#2c7fb8", "#7f8c8d"


def load_assign(level, model, on, seed=None, tau=None):
    tau = CFG["optimization"]["tau_primary"] if tau is None else tau
    seed = CFG["optimization"]["seeds"][0] if seed is None else seed
    f = MODELS / f"{level}_{model}_{'on' if on else 'off'}_tau{tau}_s{seed}_assign.csv"
    return pd.read_csv(f, dtype={"unit_id": str}) if f.exists() else None


def map_ax(ax, gA, assign, title, pref_edges=None):
    g = gA.copy()
    g["d"] = assign
    dis = g.dissolve(by="d")
    dis.plot(ax=ax, color=plt.cm.Set3(np.linspace(0, 1, len(dis))),
             edgecolor="white", linewidth=0.3)
    if pref_edges is not None and len(pref_edges):
        for i, j, w in pref_edges:
            gi, gj = dis.geometry.union_all().boundary, None
    # prefecture border overlay
    gp = gA.copy()
    gp["p"] = gp["pref_code"].astype(int)
    pb = gp.dissolve(by="p").boundary
    pb.plot(ax=ax, color="black", linewidth=1.2)
    ax.set_title(title, fontsize=10)
    ax.set_axis_off()


def main():
    gA = gpd.read_file(OUT / "units_muni.gpkg")
    gB = gpd.read_file(OUT / "units_smallarea.gpkg")
    dist = gA.copy()
    d2i = {d: k for k, d in enumerate(
        yaml.safe_load((ROOT / "config/config.yaml").read_text())
        ["districts"]["definition"].keys())}
    dist["d"] = dist["district"].map(d2i)

    # F1 study area: prefectures + municipalities + small areas
    fig, ax = plt.subplots(figsize=(6, 6))
    gB.plot(ax=ax, color="#eeeeee", edgecolor="none")
    gA.plot(ax=ax, color="none", edgecolor="#999999", linewidth=0.4)
    gA.assign(p=gA.pref_code.astype(int)).dissolve(by="p").boundary.plot(
        ax=ax, color="black", linewidth=1.4)
    en = {"大津市": "Otsu", "京都市中京区": "Nakagyo (Kyoto)",
          "彦根市": "Hikone", "福知山市": "Fukuchiyama", "宇治市": "Uji"}
    for m, label in en.items():
        c = gA[gA.muni_name == m].geometry.centroid.iloc[0]
        ax.annotate(label, (c.x, c.y), fontsize=7, ha="center")
    ax.annotate("Shiga-ken", (12300, -105000), fontsize=9, weight="bold")
    ax.annotate("Kyoto-fu", (-50600, -105000), fontsize=9, weight="bold")
    ax.set_title("Study region: Kyoto-fu and Shiga-ken (JGD2011 CS VI)")
    ax.set_axis_off()
    fig.savefig(FIG / "F1_study_area.png", bbox_inches="tight")
    plt.close(fig)

    # F2 current statutory districts
    fig, ax = plt.subplots(figsize=(6, 6))
    map_ax(ax, dist, dist["d"].values, "Current statutory districts (M0)")
    fig.savefig(FIG / "F2_current_map.png", bbox_inches="tight")
    plt.close(fig)

    # F3 optimal ON vs OFF (Level A primary seed)
    a_on = load_assign("A", "M2", True)
    a_off = load_assign("A", "M3", False)
    if a_on is not None or a_off is not None:
        fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
        g = gA.sort_values("muni_code").reset_index(drop=True)
        for ax, a, t in ((axes[0], a_on, "Boundary ON (M2)"),
                         (axes[1], a_off, "Boundary OFF (M3)")):
            if a is None:
                ax.set_title(t + " — not run")
                ax.set_axis_off()
                continue
            dmap = dict(zip(a.unit_id.astype(str), a.district))
            asg = g.muni_code.astype(str).map(dmap).values
            map_ax(ax, g, asg, t)
        fig.savefig(FIG / "F3_optimal_on_off.png", bbox_inches="tight")
        plt.close(fig)

    # F4 cross-border OD flow network
    od = pd.read_csv(OUT / "od_muni.csv")
    cen = {r.muni_code: r.geometry.centroid for r in gA.itertuples()}
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    gA.plot(ax=ax, color="#f5f5f5", edgecolor="#bbbbbb", linewidth=0.4)
    od = od.assign(origin=od.origin.astype(str), dest=od.dest.astype(str))
    odx = od[(od.origin.str[:2] != od.dest.str[:2])]
    top = odx.sort_values("flow", ascending=False).head(60)
    for r in top.itertuples():
        if r.origin in cen and r.dest in cen:
            a, b = cen[r.origin], cen[r.dest]
            ax.plot([a.x, b.x], [a.y, b.y], color="#d95f02", alpha=0.5,
                    linewidth=0.4 + 2.5 * r.flow / top.flow.max())
    gA.assign(p=gA.pref_code.astype(int)).dissolve(by="p").boundary.plot(
        ax=ax, color="black", linewidth=1.4)
    ax.set_title("Cross-prefecture commuting/schooling OD flows (top 60)")
    ax.set_axis_off()
    fig.savefig(FIG / "F4_flow_network.png", bbox_inches="tight")
    plt.close(fig)

    # F5 metric comparison bars
    res = TAB = pd.read_csv(ROOT / "outputs/tables/model_results.csv") \
        if (ROOT / "outputs/tables/model_results.csv").exists() else None
    if res is not None and len(res):
        mets = ["max_rel_dev", "polsby_popper_mean", "n_split_munis",
                "severed_flow_total"]
        labels = ["max |dev|", "Polsby–Popper", "split munis",
                  "severed flow"]
        fig, axes = plt.subplots(1, 4, figsize=(12, 3.2))
        prim = res[(res.tau == CFG["optimization"]["tau_primary"])]
        groups = [("M0/current", "M1", True), ("ON", "M2", True),
                  ("OFF", "M3", False)]
        for ax, m, lb in zip(axes, mets, labels):
            vals = []
            for tag, model, on in groups:
                s = prim[(prim.model == model) & (prim.boundary_on == on)]
                vals.append(s[m].median() if len(s) and m in s else np.nan)
            ax.bar([g[0] for g in groups], vals,
                   color=[C_CUR, C_ON, C_OFF])
            ax.set_title(lb)
            for i, v in enumerate(vals):
                if np.isfinite(v):
                    ax.text(i, v, f"{v:.3g}" if abs(v) < 100 else f"{v:.0f}",
                            ha="center", va="bottom", fontsize=8)
        fig.suptitle("Current vs optimized maps (primary seed/τ; median over seeds)")
        fig.tight_layout()
        fig.savefig(FIG / "F5_metric_comparison.png", bbox_inches="tight")
        plt.close(fig)

    # F6 placebo cost distribution
    pr = PLAC / "placebo_results.csv"
    if pr.exists():
        d = pd.read_csv(pr)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(d.cost.dropna(), bins=30, color="#8073ac", alpha=0.8)
        # real border cost on the same heuristic scale (real_border_cost.py)
        rcf = PLAC / "real_border_cost.json"
        if rcf.exists():
            rc = float(json.loads(rcf.read_text())["median"])
            ax.axvline(rc, color=C_ON, linewidth=2,
                       label=f"real border cost = {rc:.3f}")
            ax.legend()
        n_infeasible = int(d.cost.isna().sum())
        ax.text(0.02, 0.95, f"borders with no feasible incumbent: {n_infeasible}/{len(d)}",
                transform=ax.transAxes, fontsize=8, va="top")
        ax.set_xlabel("placebo border cost (obj_ON − obj_OFF)")
        ax.set_ylabel("count")
        ax.set_title(f"Placebo borders (n={len(d)}) vs real border")
        fig.savefig(FIG / "F6_placebo.png", bbox_inches="tight")
        plt.close(fig)

    # F7 future max dev trajectory by model
    res = TAB if TAB is not None else None
    if res is not None and len(res):
        yrs = CFG["robustness"]["projection_years"]
        fig, ax = plt.subplots(figsize=(6.5, 4))
        for tag, model, on, c in (("current", "M1", True, C_CUR),
                                  ("M2 ON", "M2", True, C_ON),
                                  ("M3 OFF", "M3", False, C_OFF),
                                  ("M4 ON", "M4", True, "#e7298a"),
                                  ("M4 OFF", "M4", False, "#66a61e")):
            s = res[(res.model == model) & (res.boundary_on == on) &
                    (res.tau == CFG["optimization"]["tau_primary"])]
            cols = [f"fut_S1_{y}_maxdev" for y in yrs]
            if not len(s) or not all(c in s for c in cols):
                continue
            ax.plot(yrs, s[cols].median().values, "-o", ms=3, label=tag,
                    color=c)
        ax.axhline(CFG["optimization"]["tau_primary"], ls="--", color="k",
                   lw=0.8, label="τ")
        ax.set_xlabel("year"); ax.set_ylabel("max |pop dev| (S1)")
        ax.legend(fontsize=8)
        ax.set_title("Future population-imbalance robustness")
        fig.savefig(FIG / "F7_future_robustness.png", bbox_inches="tight")
        plt.close(fig)
    print("figures:", sorted(p.name for p in FIG.glob("F*.png")))


if __name__ == "__main__":
    main()
