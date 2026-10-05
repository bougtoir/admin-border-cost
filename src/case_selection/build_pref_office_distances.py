"""National prefectural-government proximity validation (primary-data pass).

Source: MLIT National Land Numerical Information, public-facility dataset
P02 (2006 edition, JPGIS 2.1 GML/SHP, world geodetic system / JGD2000),
feature subclass P02_003 == "12001" (prefectural government office).
47 prefecture archives in data/raw/ksj_p02_publicfacilities/.

Computes geodesic distances for all 47-choose-2 = 1081 pairs on GRS80
via pyproj.Geod and ranks them. Manuscript values cs_capital_* are
written to manuscript/manuscript_values.csv.

Outputs:
  outputs/tables/prefectural_government_offices.csv
  outputs/tables/prefectural_government_pair_distances.csv
  outputs/diagnostics/pref_office_proximity_qc.json
"""
import json
import zipfile
from itertools import combinations
from pathlib import Path

import pandas as pd
from pyproj import Geod

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/ksj_p02_publicfacilities"
OUT_T = ROOT / "outputs/tables"
DIAG = ROOT / "outputs/diagnostics"

PREF_EN = {
    "北海道": "Hokkaido", "青森県": "Aomori", "岩手県": "Iwate", "宮城県": "Miyagi",
    "秋田県": "Akita", "山形県": "Yamagata", "福島県": "Fukushima", "茨城県": "Ibaraki",
    "栃木県": "Tochigi", "群馬県": "Gunma", "埼玉県": "Saitama", "千葉県": "Chiba",
    "東京都": "Tokyo", "神奈川県": "Kanagawa", "新潟県": "Niigata", "富山県": "Toyama",
    "石川県": "Ishikawa", "福井県": "Fukui", "山梨県": "Yamanashi", "長野県": "Nagano",
    "岐阜県": "Gifu", "静岡県": "Shizuoka", "愛知県": "Aichi", "三重県": "Mie",
    "滋賀県": "Shiga", "京都府": "Kyoto", "大阪府": "Osaka", "兵庫県": "Hyogo",
    "奈良県": "Nara", "和歌山県": "Wakayama", "鳥取県": "Tottori", "島根県": "Shimane",
    "岡山県": "Okayama", "広島県": "Hiroshima", "山口県": "Yamaguchi", "徳島県": "Tokushima",
    "香川県": "Kagawa", "愛媛県": "Ehime", "高知県": "Kochi", "福岡県": "Fukuoka",
    "佐賀県": "Saga", "長崎県": "Nagasaki", "熊本県": "Kumamoto", "大分県": "Oita",
    "宮崎県": "Miyazaki", "鹿児島県": "Kagoshima", "沖縄県": "Okinawa",
}
DATASET = ("MLIT National Land Numerical Information, public facilities "
           "(P02, 2006, feature subclass 12001 prefectural government office)")
METHOD = "geodesic distance, pyproj.Geod"
ELLIPSOID = "GRS80"


def load_offices() -> pd.DataFrame:
    import geopandas as gpd

    rows = []
    for z in sorted(RAW.glob("P02-06_*_GML.zip")):
        pfc = z.stem.split("_")[1]
        with zipfile.ZipFile(z) as zz:
            shp = next(n for n in zz.namelist() if n.lower().endswith(".shp"))
        g = gpd.read_file(f"zip://{z}!{shp}")
        s = g[g.P02_003.astype(str).str.strip() == "12001"]
        if len(s) != 1:
            raise RuntimeError(f"{z}: expected 1 prefectural office, got {len(s)}")
        r = s.iloc[0]
        name_ja = r.P02_004.strip()
        pref_ja = name_ja.replace("庁", "")
        rows.append({
            "prefecture_code": pfc,
            "prefecture_name_ja": pref_ja,
            "prefecture_name_en": PREF_EN[pref_ja],
            "government_office_name": name_ja,
            "latitude": r.geometry.y,
            "longitude": r.geometry.x,
            "source_feature_id": "P02_003=12001",
            "source_dataset": "P02-06_" + pfc + "_GML.zip",
            "validation_status": "single record per prefecture",
        })
    return pd.DataFrame(rows)


def main():
    import numpy as np

    off = load_offices()
    off.to_csv(OUT_T / "prefectural_government_offices.csv", index=False)

    geod = Geod(ellps="GRS80")
    o = off.set_index("prefecture_code")
    pairs = []
    for a, b in combinations(o.index, 2):
        ra, rb = o.loc[a], o.loc[b]
        _, _, d = geod.inv(rb.longitude, rb.latitude, ra.longitude, ra.latitude)
        pairs.append({
            "prefecture_a": ra.prefecture_name_en,
            "prefecture_b": rb.prefecture_name_en,
            "lat_a": ra.latitude, "lon_a": ra.longitude,
            "lat_b": rb.latitude, "lon_b": rb.longitude,
            "distance_km": d / 1000.0,
            "method": METHOD, "ellipsoid": ELLIPSOID,
            "source_dataset": DATASET,
        })
    comp = pd.DataFrame(pairs).sort_values("distance_km").reset_index(drop=True)
    comp["national_rank"] = np.arange(1, len(comp) + 1)
    comp = comp[["prefecture_a", "prefecture_b", "lat_a", "lon_a",
                 "lat_b", "lon_b", "distance_km", "national_rank",
                 "method", "ellipsoid", "source_dataset"]]
    comp.to_csv(OUT_T / "prefectural_government_pair_distances.csv", index=False)

    top = comp.head(5)
    ks = comp[((comp.prefecture_a == "Kyoto") & (comp.prefecture_b == "Shiga"))
              | ((comp.prefecture_a == "Shiga") & (comp.prefecture_b == "Kyoto"))].iloc[0]
    qc = {
        "n_offices": int(len(off)),
        "n_pairs": int(len(comp)),
        "kyoto_shiga_distance_km": float(ks.distance_km),
        "kyoto_shiga_rank": int(ks.national_rank),
        "rank1_pair": f"{comp.prefecture_a[0]}-{comp.prefecture_b[0]}",
        "rank1_km": float(comp.distance_km[0]),
        "rank2_pair": f"{comp.prefecture_a[1]}-{comp.prefecture_b[1]}",
        "rank2_km": float(comp.distance_km[1]),
        "margin_km": float(comp.distance_km[1] - comp.distance_km[0]),
        "top5": top[["prefecture_a", "prefecture_b", "distance_km"]].to_dict("records"),
    }
    DIAG.mkdir(parents=True, exist_ok=True)
    (DIAG / "pref_office_proximity_qc.json").write_text(
        json.dumps(qc, ensure_ascii=False, indent=2))
    print(json.dumps(qc, ensure_ascii=False, indent=2))

    # manuscript values: verified distance replaces secondary-source 10.5 km
    mv_path = ROOT / "manuscript/manuscript_values.csv"
    prov = {"units": "km", "source_file": "outputs/tables/prefectural_government_pair_distances.csv",
            "source_columns": "distance_km,national_rank", "analysis_step": "case_selection",
            "figure_table_reference": "T7,F8", "manuscript_location": "§4.6"}
    cs = {
        "cs_capital_km": f"{ks.distance_km:.1f} km",
        "cs_capital_rank": int(ks.national_rank),
        "cs_capital_margin_km": f"{qc['margin_km']:.1f} km",
        "n_pref_pairs": f"{len(comp):,}",
    }
    new = pd.DataFrame([{"value_id": k, "display_value": v, "raw_value": v, **prov}
                        for k, v in cs.items()])
    mv = pd.read_csv(mv_path)
    mv = mv[~mv.value_id.isin(new.value_id)]
    pd.concat([mv, new], ignore_index=True).to_csv(mv_path, index=False)
    print("cs_capital_* values updated")


if __name__ == "__main__":
    main()
