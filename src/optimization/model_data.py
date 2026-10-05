"""Shared model data: unit table, adjacency with shared-perimeter weights,
flow edge weights, projections, district memberships. Used by CP-SAT (Level A)
and local search (Level B)."""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
OUT = ROOT / "data/processed"
DISTRICTS = list(CFG["districts"]["definition"].keys())
K = CFG["districts"]["K"]


def load_units(level: str = "B"):
    g = gpd.read_file(OUT / "units_smallarea.gpkg", layer="units")
    if level == "A":
        return aggregate_to_muni(g)
    return g


def aggregate_to_muni(g: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    m = g.dissolve(by="muni_code", aggfunc={"pop": "sum", "households": "sum",
                                          "muni_name": "first", "pref_code": "first",
                                          "district": "first"})
    m = m.reset_index()
    m["unit_id"] = m["muni_code"]
    m["area_name"] = m["muni_name"]
    return m


def adjacency_with_perimeter(g: gpd.GeoDataFrame) -> pd.DataFrame:
    """Edges between adjacent units, weighted by shared boundary length (m).
    Uses the authoritative small-area edge list for level B (already built),
    spatial predicate for level A."""
    if "unit_id" not in g.columns:
        g = g.copy()
    if len(g) > 5000:  # Level B: reuse stored edges (cached weighted version)
        cache = OUT / "adj_smallarea_edges_weighted.csv"
        if cache.exists():
            return pd.read_csv(cache)
        e = pd.read_csv(OUT / "adj_smallarea_edges.csv", dtype={"i": str, "j": str})
        pos = {u: i for i, u in enumerate(g.unit_id)}
        ia = np.array([pos[u] for u in e.i])
        ib = np.array([pos[u] for u in e.j])
        geom = g.geometry.values
        # Shared-boundary length with 30 m tolerance: r2ka boundaries do not
        # coincide exactly across prefectures, so exact boundary∩boundary
        # understates shared length there.
        TOL = 30.0
        w = [geom[a].boundary.intersection(geom[b].buffer(TOL)).length
             for a, b in zip(ia, ib)]
        df = pd.DataFrame({"i": ia, "j": ib, "w": np.asarray(w)})
        df.to_csv(cache, index=False)
        return df
    # Level A: aggregate the authoritative small-area edge weights by
    # municipality pair (cross-prefecture polygon boundaries in r2ka do not
    # coincide exactly, so a direct predicate understates shared length).
    gB = load_units("B")
    eB = pd.read_csv(OUT / "adj_smallarea_edges_weighted.csv")
    muni_of = gB["muni_code"].to_numpy()
    mpos = {m: k for k, m in enumerate(g.muni_code)}
    ia = np.array([mpos[muni_of[int(i)]] for i in eB.i])
    ib = np.array([mpos[muni_of[int(j)]] for j in eB.j])
    df = pd.DataFrame({"i": ia, "j": ib, "w": eB.w.to_numpy()})
    df = df[df.i != df.j]
    df["a"] = df[["i", "j"]].min(axis=1)
    df["b"] = df[["i", "j"]].max(axis=1)
    agg = df.groupby(["a", "b"]).w.sum().reset_index()
    return agg.rename(columns={"a": "i", "b": "j"})[["i", "j", "w"]]


def load_flow_edges_levelA(g: gpd.GeoDataFrame, normalization="symmetric") -> pd.DataFrame:
    """Flow edges between Level A units (municipalities/wards)."""
    od = pd.read_csv(OUT / "od_muni.csv")
    codes = g.unit_id.tolist()
    pop = g.set_index("unit_id")["pop"]
    inr = od[od.origin.isin(codes) & od.dest.isin(codes)]
    if normalization == "symmetric":
        f = inr.groupby(["origin", "dest"]).flow.sum()
        f = f.reindex(pd.MultiIndex.from_tuples(
            [(a, b) for a in codes for b in codes])).fillna(0.0).unstack()
        sym = (f + f.T) / 2.0
        edges = [(a, b, sym.loc[a, b]) for a in codes for b in codes if a < b
                 and sym.loc[a, b] > 0]
        return pd.DataFrame(edges, columns=["o", "d", "flow"])
    raise NotImplementedError


def unit_flow_weights(g, od_sym_path=OUT / "od_region_matrix_sym.csv"):
    """Allocate municipal symmetric flows to small-area unit pairs' aggregate:
    returns dict keyed by (muniA, muniB) -> flow, used via district-share form."""
    m = pd.read_csv(od_sym_path, index_col=0)
    return m


def current_assignment(g: gpd.GeoDataFrame) -> np.ndarray:
    d2i = {d: k for k, d in enumerate(DISTRICTS)}
    return g["district"].map(d2i).to_numpy()


def load_projections() -> pd.DataFrame:
    return pd.read_parquet(OUT / "unit_projections.parquet")
