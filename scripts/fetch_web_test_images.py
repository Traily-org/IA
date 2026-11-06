#!/usr/bin/env python
"""Download licensed test photos of catalog species seen near a place.

    python scripts/fetch_web_test_images.py            # around Rennes, 40 km

Source: iNaturalist research-grade observations served through GBIF. Only photos
whose own licence is CC0 or CC BY 4.0 are kept (reuse with attribution is allowed);
CC BY-NC and all-rights-reserved photos are skipped. Output, git-ignored, in
data/web_test_images/: the photos, labels.csv (file,species,organ) and
ATTRIBUTION.csv (creator, licence, source page for every photo).
"""

from __future__ import annotations

import argparse
import csv
import re
import time
from pathlib import Path

import httpx

from traily_ia.species import load_species_file
from traily_ia.trail_species import GbifClient
from traily_ia.trail_species.geometry import corridor_polygons, to_gbif_wkts

GBIF = "https://api.gbif.org/v1/occurrence/search"
INAT_RESEARCH_GRADE = "50c9509d-22c7-4a22-a47d-8c48425ef4a7"
IMAGE_HOST = "https://inaturalist-open-data.s3.amazonaws.com/photos/"
ALLOWED_MEDIA_LICENCES = {
    "http://creativecommons.org/publicdomain/zero/1.0/": "CC0 1.0",
    "http://creativecommons.org/licenses/by/4.0/": "CC BY 4.0",
}
MAX_BYTES = 5_000_000
HEADERS = {"User-Agent": "traily-ia-dev/0.1 (test photo download for an evaluation)"}


def occurrence_filters(wkts: list[str]) -> list[tuple[str, str | int]]:
    return [
        ("datasetKey", INAT_RESEARCH_GRADE),
        ("taxonKey", 6),
        ("mediaType", "StillImage"),
        ("license", "CC0_1_0"),
        ("license", "CC_BY_4_0"),
        ("hasGeospatialIssue", "false"),
        ("occurrenceStatus", "PRESENT"),
        ("year", "2015,*"),
        *[("geometry", w) for w in wkts],
    ]


def gbif_get(http: httpx.Client, params: list[tuple[str, str | int]]) -> dict:
    """GET the occurrence search, retrying a few times on transient errors."""
    for attempt in range(4):
        response = http.get(GBIF, params=params)
        if response.status_code == 200 and isinstance(response.json(), dict):
            return response.json()
        time.sleep(2 * (attempt + 1))
    response.raise_for_status()
    raise RuntimeError(f"unexpected GBIF answer: {response.text[:200]}")


def usable_photos(occurrence: dict) -> list[dict]:
    """Photos of one observation that may be used and can be downloaded."""
    photos = []
    for media in occurrence.get("media", []):
        licence = ALLOWED_MEDIA_LICENCES.get(media.get("license", ""))
        match = re.fullmatch(
            re.escape(IMAGE_HOST) + r"(\d+)/original\.(jpe?g|png)",
            media.get("identifier", ""),
        )
        if licence and match and media.get("type") == "StillImage":
            photos.append(
                {
                    **media,
                    "licence_name": licence,
                    "photo_id": match[1],
                    "extension": match[2],
                }
            )
    return photos


def download(http: httpx.Client, photo: dict) -> bytes | None:
    """The 1024 px 'large' rendition (falls back to the original)."""
    for size in ("large", "original"):
        url = f"{IMAGE_HOST}{photo['photo_id']}/{size}.{photo['extension']}"
        response = http.get(url)
        is_image = response.headers.get("content-type", "").startswith("image/")
        if (
            response.status_code == 200
            and is_image
            and len(response.content) <= MAX_BYTES
        ):
            return response.content
    return None


def backfill_dates(out_dir: Path) -> None:
    """Add photo_created / observed dates to an existing download (no downloads)."""
    rows = list(csv.DictReader((out_dir / "ATTRIBUTION.csv").open(encoding="utf-8")))
    labels = list(csv.DictReader((out_dir / "labels.csv").open(encoding="utf-8")))
    with httpx.Client(headers=HEADERS, timeout=60.0) as http:
        for row in rows:
            key = row["observation"].rsplit("/", 1)[1]
            occ = http.get(f"https://api.gbif.org/v1/occurrence/{key}").json()
            photo_id = row["photo_page"].rsplit("/", 1)[1]
            created = next(
                (
                    m.get("created", "")
                    for m in occ.get("media", [])
                    if m.get("references", "").endswith(f"/{photo_id}")
                ),
                "",
            )
            row["photo_created"] = created[:10]
            row["observed"] = (occ.get("eventDate") or "")[:10]
            time.sleep(0.1)
    created_by_file = {r["file"]: r["photo_created"] for r in rows}
    for label in labels:
        label["photo_created"] = created_by_file[label["file"]]
    for name, data in (("ATTRIBUTION.csv", rows), ("labels.csv", labels)):
        with (out_dir / name).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
    print(f"dates added for {len(rows)} photos in {out_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--lon", type=float, default=-1.6778)
    parser.add_argument("--lat", type=float, default=48.1173)
    parser.add_argument("--radius-km", type=float, default=40.0)
    parser.add_argument("--per-species", type=int, default=2)
    parser.add_argument(
        "--species-file", type=Path, default=Path("data/species_lists/catalog.txt")
    )
    parser.add_argument("--out", type=Path, default=Path("data/web_test_images"))
    parser.add_argument(
        "--backfill-dates",
        action="store_true",
        help="only add photo upload/observation dates to an existing download",
    )
    args = parser.parse_args()
    if args.backfill_dates:
        backfill_dates(args.out)
        return 0

    catalog = set(load_species_file(args.species_file))
    wkts = to_gbif_wkts(
        corridor_polygons(
            [[(args.lon, args.lat), (args.lon + 1e-4, args.lat + 1e-4)]],
            buffer_m=args.radius_km * 1000,
        )
    )
    filters = occurrence_filters(wkts)
    gbif = GbifClient()
    args.out.mkdir(parents=True, exist_ok=True)

    with httpx.Client(headers=HEADERS, timeout=60.0, follow_redirects=True) as http:
        facets = http.get(
            GBIF,
            params=[
                *filters,
                ("limit", 0),
                ("facet", "speciesKey"),
                ("facetLimit", 1000),
            ],
        ).json()["facets"][0]["counts"]
        species = [
            (int(c["name"]), name)
            for c in facets
            if (name := gbif.species_name(int(c["name"]))) in catalog
        ]
        print(
            f"{len(species)} catalog species have usable photos "
            f"within {args.radius_km:g} km"
        )

        labels, attribution = [], []
        for key, name in species:
            found = gbif_get(http, [*filters, ("speciesKey", key), ("limit", 100)])[
                "results"
            ]
            seen_creators: set[str] = set()
            kept = 0
            for occ in found:
                creator = occ.get("recordedBy") or ""
                if creator in seen_creators:
                    continue  # different observers = more varied photos
                photos = usable_photos(occ)
                if not photos:
                    continue
                data = download(http, photos[0])
                if data is None:
                    continue
                seen_creators.add(creator)
                kept += 1
                file = f"{name.replace(' ', '_')}_{kept}.jpg"
                (args.out / file).write_bytes(data)
                labels.append(
                    {
                        "file": file,
                        "species": name,
                        "organ": "",
                        "photo_created": photos[0].get("created", "")[:10],
                    }
                )
                attribution.append(
                    {
                        "file": file,
                        "species": name,
                        "creator": photos[0].get("creator", ""),
                        "licence": photos[0]["licence_name"],
                        "photo_created": photos[0].get("created", "")[:10],
                        "observed": (occ.get("eventDate") or "")[:10],
                        "photo_page": photos[0].get("references", ""),
                        "observation": f"https://www.gbif.org/occurrence/{occ['key']}",
                    }
                )
                time.sleep(0.2)
                if kept == args.per_species:
                    break
            print(f"  {name:<30} {kept} photo(s)")

    for filename, rows in (("labels.csv", labels), ("ATTRIBUTION.csv", attribution)):
        with (args.out / filename).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    n_species = len({r["species"] for r in labels})
    print(f"\n{len(labels)} photos of {n_species} species -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
