#!/usr/bin/env python
"""Download a handful of hiking loops across France to use as test trails.

Routes are found with Waymarked Trails' API and their geometry is fetched from
the OpenStreetMap API; both are OpenStreetMap data (ODbL, see
DATASET_LICENSES.md). Output goes to data/trails/ (git-ignored):

    python scripts/fetch_test_trails.py
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import httpx

WAYMARKED = "https://hiking.waymarkedtrails.org/api/v1"
OSM_API = "https://api.openstreetmap.org/api/0.6"
HEADERS = {"User-Agent": "traily-ia-dev/0.1 (test trail download; contact via repo)"}
OUT_DIR = Path("data/trails")

# (slug, lon, lat): spread over very different French flora.
AREAS = [
    ("erdre-nantes", -1.50, 47.40),
    ("broceliande", -2.20, 48.02),
    ("fontainebleau", 2.70, 48.40),
    ("etretat", 0.20, 49.71),
    ("vosges-alsace", 7.10, 48.00),
    ("morvan", 4.00, 47.20),
    ("puy-de-dome", 2.96, 45.77),
    ("vercors", 5.45, 45.05),
    ("chamonix", 6.87, 45.92),
    ("pyrenees-cauterets", -0.11, 42.90),
    ("calanques-marseille", 5.45, 43.21),
    ("camargue", 4.40, 43.50),
    ("mercantour", 7.20, 44.10),
    ("corse-calvi", 8.90, 42.40),
]
MIN_LENGTH_M, MAX_LENGTH_M = 4_000, 20_000
HALF_WIDTH_DEG = 0.15


def web_mercator(lon: float, lat: float) -> tuple[float, float]:
    x = lon * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    return x, y * 20037508.34 / 180


def find_loop(http: httpx.Client, lon: float, lat: float) -> dict | None:
    x0, y0 = web_mercator(lon - HALF_WIDTH_DEG, lat - HALF_WIDTH_DEG)
    x1, y1 = web_mercator(lon + HALF_WIDTH_DEG, lat + HALF_WIDTH_DEG)
    listing = http.get(
        f"{WAYMARKED}/list/by_area",
        params={"bbox": f"{x0},{y0},{x1},{y1}", "limit": 40},
    ).json()
    for item in listing.get("results", []):
        if item.get("group") not in {"LOC", "REG"}:
            continue
        details = http.get(f"{WAYMARKED}/details/relation/{item['id']}").json()
        length = details.get("route", {}).get("length", 0)
        loop = details.get("tags", {}).get("roundtrip") == "yes"
        if loop and MIN_LENGTH_M <= length <= MAX_LENGTH_M:
            return {"id": item["id"], "name": item.get("name"), "length_m": length}
        time.sleep(0.3)
    return None


def relation_lines(http: httpx.Client, relation_id: int) -> list[list[list[float]]]:
    body = http.get(f"{OSM_API}/relation/{relation_id}/full.json").json()
    nodes = {
        e["id"]: [e["lon"], e["lat"]] for e in body["elements"] if e["type"] == "node"
    }
    return [
        [nodes[n] for n in e["nodes"] if n in nodes]
        for e in body["elements"]
        if e["type"] == "way"
    ]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with httpx.Client(headers=HEADERS, timeout=60.0) as http:
        for slug, lon, lat in AREAS:
            loop = find_loop(http, lon, lat)
            if loop is None:
                print(f"{slug:<22} no suitable loop found")
                continue
            lines = relation_lines(http, loop["id"])
            feature = {
                "type": "Feature",
                "properties": {
                    "trail_id": slug,
                    "name": loop["name"],
                    "osm_relation": loop["id"],
                    "length_m": loop["length_m"],
                    "source": "OpenStreetMap contributors (ODbL)",
                },
                "geometry": {"type": "MultiLineString", "coordinates": lines},
            }
            (OUT_DIR / f"{slug}.geojson").write_text(
                json.dumps(feature), encoding="utf-8"
            )
            print(f"{slug:<22} {loop['name']!s:<40} {loop['length_m'] / 1000:.1f} km")
            time.sleep(1)


if __name__ == "__main__":
    main()
