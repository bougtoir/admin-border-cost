"""Build the PMR education-access evaluation dataset from P29 school data.

Input:  data/raw/ksj_p29_schools/P29-21.geojson (unzipped from the official
        MLIT National Land Numerical Information P29-21_GML.zip archive).
Output: data/processed/pmr_education_access/*.csv — Kyoto (26) + Shiga (25)
        school points, all levels, plus open elementary / junior-high
        subsets (whole and public-only) used by the F2 access analysis.

Code lists (verified empirically against the 2021 release, 57,230 records):
P29_003 school type: 16001 elementary, 16002 junior_high, 16003 secondary
    school, 16004 high_school, 16005 technical_college, 16006 junior_college,
    16007 university, 16011 kindergarten, 16012 special_needs, 16013 kodomoen,
    16014 compulsory_education_school, 16015 specialized_training,
    16016 miscellaneous_school.
P29_006 admin: 0 national_univ_corp, 1 national, 2 prefectural_public,
    3 municipal_public, 4 private (is_public = code != 4).
P29_007 status: 1 open; 9 closed (closed schools excluded from the *_open
    files); 0 unclassified (retained in _all only — mostly private schools).
"""
import csv
import json
import os

RAW = "data/raw/ksj_p29_schools/P29-21.geojson"
OUT_DIR = "data/processed/pmr_education_access"

TYPE = {
    16001: "elementary", 16002: "junior_high", 16003: "secondary_school",
    16004: "high_school", 16005: "technical_college", 16006: "junior_college",
    16007: "university", 16011: "kindergarten", 16012: "special_needs",
    16013: "kodomoen", 16014: "compulsory_education_school",
    16015: "specialized_training", 16016: "miscellaneous_school",
}
ADMIN = {
    0: "national_univ_corp", 1: "national", 2: "prefectural_public",
    3: "municipal_public", 4: "private",
}


def main():
    with open(RAW, encoding="utf-8") as fh:
        geo = json.load(fh)
    rows = []
    for feat in geo["features"]:
        p = feat["properties"]
        code = p["P29_001"]
        if not (code.startswith("25") or code.startswith("26")):
            continue
        lon, lat = feat["geometry"]["coordinates"]
        rows.append({
            "admin_area_code": code,
            "prefecture": "Shiga" if code.startswith("25") else "Kyoto",
            "school_code": p["P29_002"],
            "school_type_code": p["P29_003"],
            "school_type": TYPE.get(p["P29_003"], "unknown"),
            "name": p["P29_004"],
            "address": p.get("P29_005", ""),
            "admin_code": p["P29_006"],
            "admin": ADMIN.get(p["P29_006"], "unknown"),
            "is_public": p["P29_006"] != 4,
            "open_flag_code": p["P29_007"],
            "is_open": p["P29_007"] == 1,
            "lon": lon, "lat": lat, "crs": "JGD2011",
        })
    rows.sort(key=lambda r: (r["prefecture"], r["admin_area_code"],
                             r["school_type_code"], r["school_code"]))
    os.makedirs(OUT_DIR, exist_ok=True)

    def dump(name, subset):
        path = os.path.join(OUT_DIR, name)
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(subset)
        print(path, len(subset))

    dump("p29_schools_kyoto_shiga_all.csv", rows)
    for lvl in ("elementary", "junior_high"):
        open_rows = [r for r in rows if r["school_type"] == lvl and r["is_open"]]
        dump(f"p29_{lvl}_open_kyoto_shiga.csv", open_rows)
        dump(f"p29_{lvl}_open_public_kyoto_shiga.csv",
             [r for r in open_rows if r["is_public"]])


if __name__ == "__main__":
    main()
