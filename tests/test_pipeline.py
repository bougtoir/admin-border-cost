"""Sanity tests: geography, flows, projections, metrics consistency."""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
OUT = ROOT / "data/processed"


def test_units_exist():
    import geopandas as gpd
    g = gpd.read_file(OUT / "units_smallarea.gpkg")
    assert len(g) > 11000
    assert g.unit_id.is_unique
    assert g["pop"].sum() == pytest.approx(3991697, rel=1e-6)


def test_adjacency_connected():
    import networkx as nx
    e = pd.read_csv(OUT / "adj_smallarea_edges.csv")
    G = nx.Graph()
    G.add_edges_from(e[["i", "j"]].itertuples(index=False))
    assert nx.number_connected_components(G) == 1


def test_flow_matrix():
    sym = pd.read_csv(OUT / "od_region_matrix_sym.csv", index_col=0)
    assert np.allclose(sym.values, sym.values.T, atol=1)


def test_projections_census_anchor():
    mp = pd.read_csv(OUT / "muni_projections.csv")
    p2020 = mp[mp.year == 2020].pop_ipss.sum()
    assert p2020 == pytest.approx(3991697, rel=1e-3)


def test_metrics_current_map():
    from src.optimization import metrics
    from src.optimization.model_data import DISTRICTS, adjacency_with_perimeter, load_units
    g = load_units("A").reset_index(drop=True)
    e = adjacency_with_perimeter(g)
    a = g["district"].map({d: k for k, d in enumerate(DISTRICTS)}).values
    r = metrics.evaluate(a, g, e)
    assert r["contiguous"]
    assert 0.3 < r["max_rel_dev"] < 0.5
    assert 1.8 < r["max_min_ratio"] < 2.2
