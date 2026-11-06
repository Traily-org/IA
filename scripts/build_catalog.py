#!/usr/bin/env python
"""Build the species catalog: a short common/uncommon list per trail, combined.

    python scripts/build_catalog.py data/trails/*.geojson

Per trail: GBIF species (cached) -> protected species removed -> at most 20
selected, mostly common and a few uncommon. Writes data/db/catalog.sqlite and
data/species_lists/catalog.txt (the union, usable as --species-file).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from shapely import MultiLineString

from traily_ia.trail_species import GbifClient, build_trail_species
from traily_ia.trail_species.catalog import TrailRecord, catalog_names, write_catalog
from traily_ia.trail_species.inpn import InpnProtectionFilter
from traily_ia.trail_species.location import locate_cached
from traily_ia.trail_species.selection import (
    DEFAULT_MAX_SPECIES,
    DEFAULT_MIN_OCCURRENCES,
    DEFAULT_UNCOMMON_FROM,
    DEFAULT_UNCOMMON_SHARE,
    select_species,
)

CACHE_DIR = Path("data/cache/trail_species")
LOCATION_CACHE_DIR = Path("data/cache/locations")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("trails", type=Path, nargs="+", help="GeoJSON trail files")
    parser.add_argument("--max-species", type=int, default=DEFAULT_MAX_SPECIES)
    parser.add_argument("--uncommon-share", type=float, default=DEFAULT_UNCOMMON_SHARE)
    parser.add_argument("--min-occurrences", type=int, default=DEFAULT_MIN_OCCURRENCES)
    parser.add_argument(
        "--scope",
        choices=["local", "anywhere", "national"],
        default="local",
        help="local: national + the trail's own région/département protections "
        "(default); anywhere: protected anywhere in metropolitan France; "
        "national: national only",
    )
    parser.add_argument(
        "--inpn-index", type=Path, default=Path("data/inpn/protected_plants.json")
    )
    parser.add_argument("--db", type=Path, default=Path("data/db/catalog.sqlite"))
    parser.add_argument(
        "--names-out", type=Path, default=Path("data/species_lists/catalog.txt")
    )
    args = parser.parse_args()

    base = InpnProtectionFilter.from_index(args.inpn_index, scope=args.scope)
    print(f"protection data: {base.source} ({base.age_days()} days old)")
    if base.is_stale():
        print("WARNING: protection data is older than a year.", file=sys.stderr)

    gbif = GbifClient()
    records = []
    for path in args.trails:
        feature = json.loads(path.read_text(encoding="utf-8"))
        props, lines = feature["properties"], feature["geometry"]["coordinates"]
        protection = base
        zone = ""
        if args.scope == "local":
            location = locate_cached(props["trail_id"], lines, LOCATION_CACHE_DIR)
            protection = base.for_location(location)
            zone = (
                f"dép {','.join(sorted(location.departements))} "
                f"rég {','.join(sorted(location.regions))}"
            )
        full = build_trail_species(
            props["trail_id"],
            lines,
            gbif=gbif,
            protection=protection,
            cache_dir=CACHE_DIR,
        )
        selected = select_species(
            full.species,
            max_species=args.max_species,
            uncommon_share=args.uncommon_share,
            min_occurrences=args.min_occurrences,
        )
        centre = MultiLineString(lines).centroid
        records.append(
            TrailRecord(
                props["trail_id"],
                props.get("name"),
                centre.x,
                centre.y,
                props.get("length_m"),
                props.get("osm_relation"),
                selected,
                (
                    ",".join(sorted(location.departements))
                    if args.scope == "local"
                    else ""
                ),
                ",".join(sorted(location.regions)) if args.scope == "local" else "",
            )
        )
        common = sum(s.tier == "common" for s in selected)
        print(
            f"{props['trail_id']:<22} {zone:<28} "
            f"{len(full.species):>4} after protection "
            f"-> {len(selected):>2} selected ({common} common, "
            f"{len(selected) - common} uncommon)"
        )

    meta = {
        "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "protection_scope": args.scope,
        "protection_base_source": base.source,
        "max_species": str(args.max_species),
        "uncommon_share": str(args.uncommon_share),
        "uncommon_from": str(DEFAULT_UNCOMMON_FROM),
        "min_occurrences": str(args.min_occurrences),
        "gbif_filters": "Plantae, wild records, year>=1990, PRESENT, 500 m buffer",
    }
    write_catalog(args.db, records, meta)
    names = catalog_names(args.db)
    args.names_out.parent.mkdir(parents=True, exist_ok=True)
    args.names_out.write_text("\n".join(names) + "\n", encoding="utf-8")
    print(f"\n{len(names)} distinct species over {len(records)} trails -> {args.db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
