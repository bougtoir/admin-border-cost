"""Download all raw inputs into data/raw/ (never overwrites existing files).
URLs and identifiers are recorded in docs/DATA_PROVENANCE.md; after download,
append new entries to data/raw/SHA256SUMS.txt.
"""
import hashlib
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw"

FILES = [
    # e-Stat statistical GIS small-area boundaries (r2ka), JGD2000 latlon
    ("estat_gis_boundary/r2ka25.zip",
     "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=25&coordSys=1&format=shape&downloadType=5&datum=2000"),
    ("estat_gis_boundary/r2ka26.zip",
     "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=26&coordSys=1&format=shape&downloadType=5&datum=2000"),
    # 2020 Census Table 6-1 municipality OD (commuting/schooling)
    ("estat_census_od/od_shiga.xlsx",
     "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222141&fileKind=0"),
    ("estat_census_od/od_kyoto.xlsx",
     "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222142&fileKind=0"),
    # case-selection comparison set (PG retarget): all Kinki origin prefs
    ("estat_census_od/od_fukui_61.xlsx",
     "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222134&fileKind=0"),
    ("estat_census_od/od_gifu_61.xlsx",
     "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222137&fileKind=0"),
    ("estat_census_od/od_mie_61.xlsx",
     "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222140&fileKind=0"),
    ("estat_census_od/od_osaka_61.xlsx",
     "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222143&fileKind=0"),
    ("estat_census_od/od_hyogo_61.xlsx",
     "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222144&fileKind=0"),
    ("estat_census_od/od_nara_61.xlsx",
     "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222145&fileKind=0"),
    ("estat_census_od/od_wakayama_61.xlsx",
     "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032222146&fileKind=0"),
    # r2ka boundary+population for comparator prefectures (prefecture sums)
    ("estat_gis_boundary/r2ka18.zip",
     "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=18&coordSys=1&format=shape&downloadType=5&datum=2000"),
    ("estat_gis_boundary/r2ka21.zip",
     "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=21&coordSys=1&format=shape&downloadType=5&datum=2000"),
    ("estat_gis_boundary/r2ka24.zip",
     "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=24&coordSys=1&format=shape&downloadType=5&datum=2000"),
    ("estat_gis_boundary/r2ka27.zip",
     "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=27&coordSys=1&format=shape&downloadType=5&datum=2000"),
    ("estat_gis_boundary/r2ka28.zip",
     "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=28&coordSys=1&format=shape&downloadType=5&datum=2000"),
    ("estat_gis_boundary/r2ka29.zip",
     "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=29&coordSys=1&format=shape&downloadType=5&datum=2000"),
    ("estat_gis_boundary/r2ka30.zip",
     "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=30&coordSys=1&format=shape&downloadType=5&datum=2000"),
    # MLIT National Land Numerical Information: public facilities (P02, 2006),
    # all 47 prefectures — subclass 12001 = prefectural government office
] + [
    (f"ksj_p02_publicfacilities/P02-06_{i:02d}_GML.zip",
     f"https://nlftp.mlit.go.jp/ksj/gml/data/P02/P02-06/P02-06_{i:02d}_GML.zip")
    for i in range(1, 48)
] + [
    # IPSS municipal projections 2023
    ("ipss/kekkahyo1.xlsx",
     "https://www.ipss.go.jp/pp-shicyoson/j/shicyoson23/2gaiyo_hyo/kekkahyo1.xlsx"),
    # Public Offices Election Act XML
    ("egov/kosenkyoho.xml",
     "https://elaws.e-gov.go.jp/api/1/lawdata/昭和二十五年法律第百号"),
    # MIC district map PDF (Shiga example)
    ("soumu/shiga_map.pdf",
     "https://www.soumu.go.jp/main_content/000853831.pdf"),
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    sums = RAW / "SHA256SUMS.txt"
    done = set()
    if sums.exists():
        done = {l.split()[-1] for l in sums.read_text().splitlines() if l.strip()}
    new_lines = []
    for rel, url in FILES:
        p = RAW / rel
        if p.exists() and rel in done:
            print("skip (archived):", rel)
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(url, timeout=300)
        r.raise_for_status()
        p.write_bytes(r.content)
        h = sha256(p)
        new_lines.append(f"{h}  {rel}")
        print(f"{rel}: {len(r.content)} bytes sha256={h[:12]}… "
              f"(UTC {time.strftime('%Y-%m-%d %H:%M', time.gmtime())})")
    if new_lines:
        with open(sums, "a") as f:
            f.write("\n".join(new_lines) + "\n")


if __name__ == "__main__":
    main()
