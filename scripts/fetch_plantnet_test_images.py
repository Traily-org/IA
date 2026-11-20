#!/usr/bin/env python
"""Download Pl@ntNet test photos that name their organ, for per-organ evaluation.

    python scripts/fetch_plantnet_test_images.py --organs bark leaf

Source: the "Pl@ntNet observations" dataset on GBIF, whose image descriptions end
with the organ ("Fagus sylvatica L.: bark"). Only photos uploaded from 2024-01-01
(after BioCLIP's November 2023 evaluation) and whose own licence is
CC0, CC BY or CC BY-SA are kept. Evaluation only, never redistributed: output goes to
git-ignored data/plantnet_test_images/ (photos, labels.csv with file,species,organ and
ATTRIBUTION.csv). Labels are Pl@ntNet's own "valid species" names, not an expert check.
"""

from __future__ import annotations

import argparse
import csv
import re
import time
from pathlib import Path

import httpx

from traily_ia.species import load_species_file

GBIF = "https://api.gbif.org/v1/occurrence/search"
PLANTNET_DATASET = "7a3679ef-5582-4aaa-81f0-8c2545cafc81"
IMAGE_HOST = "https://bs.plantnet.org/image/"
ORGANS = ("leaf", "flower", "fruit", "bark", "habit", "other")
ALLOWED_LICENCES = {"cc0": "CC0", "cc-by": "CC BY", "cc-by-sa": "CC BY-SA"}
MAX_BYTES = 5_000_000
HEADERS = {"User-Agent": "traily-ia-dev/0.1 (test photo download for an evaluation)"}


def organ_of(media: dict) -> str | None:
    """'Fagus sylvatica L.: bark' -> 'bark' (None if not a known organ)."""
    organ = (media.get("description") or "").rsplit(":", 1)[-1].strip().lower()
    return organ if organ in ORGANS else None


def licence_of(media: dict) -> str | None:
    """'amy15820 (cc-by-sa)' -> 'CC BY-SA' (None if not allowed)."""
    match = re.search(r"\(([^()]+)\)\s*$", media.get("license") or "")
    return ALLOWED_LICENCES.get(match[1].strip().lower()) if match else None


def search(http: httpx.Client, species: str, country: str) -> list[dict]:
    params = {
        "datasetKey": PLANTNET_DATASET,
        "scientificName": species,
        "mediaType": "StillImage",
        "year": "2024,*",
        "country": country,
        "occurrenceStatus": "PRESENT",
        "limit": 300,
    }
    for attempt in range(4):
        response = http.get(GBIF, params=params)
        if response.status_code == 200:
            return response.json().get("results", [])
        time.sleep(2 * (attempt + 1))
    response.raise_for_status()
    return []


def download(http: httpx.Client, identifier: str) -> bytes | None:
    """Medium rendition first (`/m/`), then the identifier as published."""
    hash_ = identifier.rstrip("/").rsplit("/", 1)[-1]
    for url in (f"{IMAGE_HOST}m/{hash_}", identifier):
        response = http.get(url)
        if (
            response.status_code == 200
            and response.headers.get("content-type", "").startswith("image/")
            and len(response.content) <= MAX_BYTES
        ):
            return response.content
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--organs", nargs="+", default=["bark", "leaf"], choices=ORGANS)
    parser.add_argument("--per-species-organ", type=int, default=2)
    parser.add_argument("--country", default="FR")
    parser.add_argument(
        "--species-file", type=Path, default=Path("data/species_lists/catalog.txt")
    )
    parser.add_argument("--out", type=Path, default=Path("data/plantnet_test_images"))
    args = parser.parse_args()

    species_list = load_species_file(args.species_file)
    args.out.mkdir(parents=True, exist_ok=True)
    labels, attribution = [], []
    with httpx.Client(headers=HEADERS, timeout=60.0, follow_redirects=True) as http:
        for name in species_list:
            kept: dict[str, int] = {o: 0 for o in args.organs}
            seen_creators: dict[str, set[str]] = {o: set() for o in args.organs}
            for occ in search(http, name, args.country):
                for media in occ.get("media", []):
                    organ, licence = organ_of(media), licence_of(media)
                    created = (media.get("created") or "")[:10]
                    creator = media.get("creator") or ""
                    if (
                        organ not in kept
                        or licence is None
                        or created < "2024-01-01"
                        or kept[organ] >= args.per_species_organ
                        or creator in seen_creators[organ]
                    ):
                        continue
                    data = download(http, media.get("identifier", ""))
                    if data is None:
                        continue
                    kept[organ] += 1
                    seen_creators[organ].add(creator)
                    file = f"{name.replace(' ', '_')}_{organ}_{kept[organ]}.jpg"
                    (args.out / file).write_bytes(data)
                    labels.append(
                        {
                            "file": file,
                            "species": name,
                            "organ": organ,
                            "photo_created": created,
                        }
                    )
                    attribution.append(
                        {
                            "file": file,
                            "species": name,
                            "organ": organ,
                            "creator": creator,
                            "licence": licence,
                            "photo_created": created,
                            "source": media.get("source", ""),
                        }
                    )
                    time.sleep(0.2)
            print(f"  {name:<32} " + " ".join(f"{o}:{n}" for o, n in kept.items()))

    if not labels:
        print("no photo found")
        return 1
    for filename, rows in (("labels.csv", labels), ("ATTRIBUTION.csv", attribution)):
        with (args.out / filename).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    by_organ = {o: sum(1 for r in labels if r["organ"] == o) for o in args.organs}
    print(f"\n{len(labels)} photos {by_organ} -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
