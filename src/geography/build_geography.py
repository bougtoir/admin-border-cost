"""Build unit geography (Level B small areas + Level A municipalities/wards),
adjacency graphs, and statutory district assignment for Kyoto(26)/Shiga(25).
Outputs:
  data/processed/units_smallarea.gpkg      (small-area units, EPSG:6674)
  data/processed/units_muni.gpkg           (municipality/ward units)
  data/processed/adj_smallarea_edges.csv
  data/processed/muni_lookup.csv           (muni_code, name, pref, district)
  outputs/diagnostics/geography_qc.json
"""
import json
import zipfile
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config/config.yaml").read_text())
CRS = CFG["project"]["crs_projected"]
RAW = ROOT / "data/raw/estat_gis_boundary"
OUT = ROOT / "data/processed"
DIAG = ROOT / "outputs/diagnostics"
OUT.mkdir(parents=True, exist_ok=True)
DIAG.mkdir(parents=True, exist_ok=True)

ZIPS = {"25": "r2ka25_小地域境界_滋賀県_2020国勢調査.zip",
        "26": "r2ka26_小地域境界_京都府_2020国勢調査.zip"}


def load_pref(pref: str) -> gpd.GeoDataFrame:
    z = RAW / ZIPS[pref]
    with zipfile.ZipFile(z) as zf:
        zf.extractall(ROOT / "data/interim" / f"r2ka{pref}")
    shp = next((ROOT / "data/interim" / f"r2ka{pref}").glob("*.shp"))
    g = gpd.read_file(shp)
    g["muni_code"] = g["PREF"].astype(int).astype(str) + g["CITY"].astype(int).astype(str).str.zfill(3)
    g["pref_code"] = g["PREF"].astype(int).astype(str)
    g["unit_id"] = g["KEY_CODE"].astype(str)
    g["pop"] = g["JINKO"].astype(float)
    g = g[["unit_id", "pref_code", "muni_code", "CITY_NAME", "S_NAME", "pop", "SETAI", "geometry"]]
    return g.rename(columns={"CITY_NAME": "muni_name", "S_NAME": "area_name", "SETAI": "households"})


def queen_edges(g: gpd.GeoDataFrame) -> pd.DataFrame:
    """Queen adjacency via spatial index on touching/intersecting boundaries."""
    edges = set()
    for i, geom in enumerate(g.geometry.values):
        for j in g.sindex.query(geom, predicate="intersects"):
            if j <= i:
                continue
            other = g.geometry.values[j]
            # queen contiguity: geometries share at least a point; area overlap by
            # adjacent polygons is typical; touching at a point also counts (queen)
            if geom.touches(other) or geom.intersects(other):
                if geom.intersection(other).is_empty:
                    continue
                edges.add((i, j))
    return pd.DataFrame(sorted(edges), columns=["i", "j"])


def connect_isolates(g: gpd.GeoDataFrame, edges: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """Attach isolated units and disconnected island components to the mainland
    graph via nearest-centroid edges. Returns extended edge list + audit records."""
    extra = []
    cent = g.geometry.representative_point()

    def comps():
        G = nx.Graph()
        G.add_nodes_from(range(len(g)))
        G.add_edges_from(edges.itertuples(index=False))
        return [sorted(c) for c in nx.connected_components(G)]

    while True:
        cs = comps()
        if len(cs) == 1:
            break
        giant = max(range(len(cs)), key=lambda k: len(cs[k]))
        comp = min((c for k, c in enumerate(cs) if k != giant), key=len)
        sub = cent.iloc[comp]
        # prefer a same-municipality unit so the statutory map stays contiguous
        comp_munis = set(g.muni_code.iloc[comp])
        same = g.index[(g.muni_code.isin(comp_munis)) & (~g.index.isin(comp))]
        rest = cent.loc[same] if len(same) else cent.drop(index=comp)
        d = rest.apply(lambda p, sub=sub: sub.distance(p).min())
        j = int(d.idxmin())
        i = int(sub.distance(rest.loc[j]).idxmin())
        edges.loc[len(edges)] = [min(i, j), max(i, j)]
        extra.append({"component_size": len(comp),
                      "unit_ids_in_component": [g.unit_id.iloc[t] for t in comp],
                      "bridge": [g.unit_id.iloc[i], g.unit_id.iloc[j]],
                      "dist_m": float(sub.distance(rest.loc[j]).min()),
                      "reason": "disconnected component (island cluster) bridged to nearest unit"})
    # any remaining singletons
    adj = edges_to_adj(edges, len(g))
    for i in range(len(g)):
        if len(adj[i]) == 0:
            d = cent.distance(cent.iloc[i])
            j = int(d.drop(i).idxmin())
            edges.loc[len(edges)] = [min(i, j), max(i, j)]
            extra.append({"unit_id": g.unit_id.iloc[i], "joined_to": g.unit_id.iloc[j],
                          "dist_m": float(d.loc[j]), "reason": "isolated unit joined to nearest"})
            adj = edges_to_adj(edges, len(g))
    # municipal enclaves: a unit with no same-municipality neighbor is a detached
    # fragment (legal 飛び地); bridge it to its nearest same-municipality unit so
    # municipal/district contiguity is preserved
    muni = g.muni_code.to_numpy()
    for i in range(len(g)):
        if not any(muni[j] == muni[i] for j in adj.get(i, ())):
            cand = np.where(muni == muni[i])[0]
            cand = cand[cand != i]
            if len(cand) == 0:
                continue
            d = cent.iloc[cand].distance(cent.iloc[i])
            j = int(cand[d.argmin()])
            key = (min(i, j), max(i, j))
            if key not in set(map(tuple, edges[["i", "j"]].values.tolist())):
                edges.loc[len(edges)] = list(key)
                extra.append({"unit_id": g.unit_id.iloc[i], "joined_to": g.unit_id.iloc[j],
                              "dist_m": float(d.min()),
                              "reason": "municipal enclave bridged to same municipality"})
                adj = edges_to_adj(edges, len(g))
    return edges.reset_index(drop=True), extra


def edges_to_adj(edges: pd.DataFrame, n: int) -> dict[int, set[int]]:
    adj = {i: set() for i in range(n)}
    for i, j in edges.itertuples(index=False):
        adj[i].add(j)
        adj[j].add(i)
    return adj


def district_map(muni_names: pd.Series) -> pd.Series:
    name2dist = {}
    for d, names in CFG["districts"]["definition"].items():
        for n in names:
            name2dist[n] = d
    mapping = muni_names.map(name2dist)
    missing = sorted(set(muni_names[mapping.isna()]))
    if missing:
        raise ValueError(f"municipalities missing district assignment: {missing}")
    return mapping


def main():
    gdf = pd.concat([load_pref(p) for p in CFG["region"]["prefectures"]], ignore_index=True)
    gdf = gpd.GeoDataFrame(gdf, geometry="geometry", crs="EPSG:6668")  # JGD2000 geographic ~ EPSG:6668
    gdf = gdf.to_crs(CRS)
    # Some small areas are stored as several fragment rows (detached parts of one
    # census small area sharing KEY_CODE). They are one official unit: merge them
    # (unioned MultiPolygon, summed population) — 420 fragment rows -> base units.
    n_rows = len(gdf)
    gdf = (gdf.dissolve(by="unit_id",
                        aggfunc={"pop": "sum", "households": "sum",
                                 "pref_code": "first", "muni_code": "first",
                                 "muni_name": "first", "area_name": "first"})
              .reset_index())
    n_frag = n_rows - len(gdf)
    gdf["unit_id"] = gdf["unit_id"].astype(str)
    gdf = gdf.reset_index(drop=True)
    gdf["uid"] = gdf.index

    edges = queen_edges(gdf)
    edges, joins = connect_isolates(gdf, edges)

    # municipality/ward level
    muni = gdf.dissolve(by="muni_code", aggfunc={"pop": "sum", "households": "sum",
                                               "muni_name": "first", "pref_code": "first"})
    muni = muni.reset_index()
    muni["district"] = district_map(muni["muni_name"])
    gdf["district"] = gdf["muni_code"].map(muni.set_index("muni_code")["district"])

    # QC
    G = nx.Graph()
    G.add_edges_from(edges.itertuples(index=False))
    qc = {
        "n_smallarea_units": len(gdf),
        "n_fragment_rows_merged": int(n_frag),
        "n_muni_units": len(muni),
        "n_edges": len(edges),
        "n_components": int(nx.number_connected_components(G)),
        "n_isolate_joins": len(joins),
        "total_pop": float(gdf["pop"].sum()),
        "pop_by_pref": gdf.groupby("pref_code")["pop"].sum().to_dict(),
        "pop_by_district": gdf.groupby("district")["pop"].sum().to_dict(),
        "units_by_district": gdf.groupby("district")["unit_id"].count().to_dict(),
        "muni_by_district": muni.groupby("district")["muni_name"].apply(list).to_dict(),
        "isolate_joins": joins,
    }
    gdf.to_file(OUT / "units_smallarea.gpkg", layer="units", driver="GPKG")
    muni.to_file(OUT / "units_muni.gpkg", layer="units", driver="GPKG")
    edges.assign(i=gdf.unit_id[edges.i].values, j=gdf.unit_id[edges.j].values) \
        .to_csv(OUT / "adj_smallarea_edges.csv", index=False)
    muni[["muni_code", "muni_name", "pref_code", "district", "pop"]].to_csv(
        OUT / "muni_lookup.csv", index=False)
    (DIAG / "geography_qc.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in qc.items() if k != "muni_by_district" and k != "isolate_joins"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
