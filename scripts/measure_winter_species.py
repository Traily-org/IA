#!/usr/bin/env python
"""Count, per trail, the plant species with enough GBIF records in one season.

    python scripts/measure_winter_species.py

For each trail polygon (500 m corridor): species with at least 3 records in
December-February (winter) and in October-November (autumn), all plants and mosses
alone. Protected species are not removed, so the real numbers are a little lower.
Writes docs/results/winter_species.json. Shows why a winter list cannot be built from
winter records alone.
"""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx

from traily_ia.trail_species.geometry import corridor_polygons, to_gbif_wkts

PLANTAE, BRYOPHYTA = 6, 35
BASIS = ("HUMAN_OBSERVATION", "OBSERVATION", "PRESERVED_SPECIMEN", "MATERIAL_SAMPLE")
WINTER, AUTUMN = (12, 1, 2), (10, 11)


def trail_lines(path: Path) -> list[list[tuple[float, float]]]:
    geo = json.loads(path.read_text(encoding="utf-8"))
    features = geo.get("features", [geo])
    lines: list[list[tuple[float, float]]] = []
    for feature in features:
        geom = feature["geometry"]
        parts = (
            [geom["coordinates"]]
            if geom["type"] == "LineString"
            else geom["coordinates"]
        )
        lines += [[(c[0], c[1]) for c in part] for part in parts]
    return lines


def species_with_records(
    http: httpx.Client, wkts: list[str], taxon: int, months: tuple[int, ...]
) -> int:
    params: list[tuple[str, str | int]] = [
        ("taxonKey", taxon),
        ("hasCoordinate", "true"),
        ("hasGeospatialIssue", "false"),
        ("occurrenceStatus", "PRESENT"),
        ("year", "1990,*"),
        ("limit", 0),
        ("facet", "speciesKey"),
        ("facetLimit", 1000),
    ]
    params += [("basisOfRecord", b) for b in BASIS]
    params += [("month", m) for m in months] + [("geometry", w) for w in wkts]
    for _ in range(5):
        response = http.get("https://api.gbif.org/v1/occurrence/search", params=params)
        if response.status_code == 200:
            break
        time.sleep(5)
    response.raise_for_status()
    facets = response.json()["facets"]
    counts = facets[0]["counts"] if facets else []
    return sum(1 for c in counts if c["count"] >= 3)


def main() -> int:
    rows = []
    with httpx.Client(timeout=90) as http:
        for path in sorted(Path("data/trails").glob("*.geojson")):
            wkts = to_gbif_wkts(corridor_polygons(trail_lines(path), buffer_m=500))
            rows.append(
                {
                    "trail_id": path.stem,
                    "winter_species": species_with_records(http, wkts, PLANTAE, WINTER),
                    "winter_mosses": species_with_records(
                        http, wkts, BRYOPHYTA, WINTER
                    ),
                    "autumn_species": species_with_records(http, wkts, PLANTAE, AUTUMN),
                }
            )
            print(rows[-1], flush=True)
            time.sleep(1)
    out = Path("docs/results/winter_species.json")
    out.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
                "min_records_per_species": 3,
                "rows": rows,
            },
            indent=1,
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
