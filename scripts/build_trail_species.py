#!/usr/bin/env python
"""Build (and cache) the observable-species list for one or more test trails.

    python scripts/build_trail_species.py data/trails/rennes.geojson
    python scripts/build_trail_species.py data/trails/*.geojson --names-out out/lists

Protected species are removed using the INPN index built by
scripts/build_inpn_index.py. If the index is missing the script stops — it never
falls back to an unfiltered list unless --unfiltered is given explicitly, and
such lists are marked UNFILTERED in the cache (never feed them to production).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from traily_ia.trail_species import (
    GbifClient,
    NoProtectionFilter,
    ProtectionFilter,
    build_trail_species,
)
from traily_ia.trail_species.inpn import InpnProtectionFilter
from traily_ia.trail_species.location import locate_cached

CACHE_DIR = Path("data/cache/trail_species")
LOCATION_CACHE_DIR = Path("data/cache/locations")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("trails", type=Path, nargs="+", help="GeoJSON trail files")
    parser.add_argument("--buffer-m", type=float, default=500.0)
    parser.add_argument(
        "--inpn-index", type=Path, default=Path("data/inpn/protected_plants.json")
    )
    parser.add_argument(
        "--scope",
        choices=["local", "anywhere", "national"],
        default="local",
        help="local: national + the trail's own région/département (default); "
        "anywhere: protected anywhere in metropolitan France (strictest); "
        "national: national protection only",
    )
    parser.add_argument(
        "--unfiltered",
        action="store_true",
        help="skip the protection filter (local experiments only)",
    )
    parser.add_argument(
        "--names-out",
        type=Path,
        help="also write <trail>.txt species files usable with identify_local.py",
    )
    args = parser.parse_args()

    gbif = GbifClient()
    protection: ProtectionFilter
    inpn: InpnProtectionFilter | None = None
    if args.unfiltered:
        protection = NoProtectionFilter()
    else:
        inpn = InpnProtectionFilter.from_index(args.inpn_index, scope=args.scope)
        protection = inpn
        print(f"protection data: {inpn.source} ({inpn.age_days()} days old)")
        if inpn.is_stale():
            print(
                "WARNING: protection data is older than a year — new protection "
                "orders since then are not reflected. Refresh the INPN files.",
                file=sys.stderr,
            )
    for path in args.trails:
        feature = json.loads(path.read_text(encoding="utf-8"))
        if inpn is not None and args.scope == "local":
            location = locate_cached(
                feature["properties"]["trail_id"],
                feature["geometry"]["coordinates"],
                LOCATION_CACHE_DIR,
            )
            protection = inpn.for_location(location)
        result = build_trail_species(
            feature["properties"]["trail_id"],
            feature["geometry"]["coordinates"],
            gbif=gbif,
            protection=protection,
            cache_dir=CACHE_DIR,
            buffer_m=args.buffer_m,
        )
        top = ", ".join(s.scientific_name for s in result.species[:3])
        print(
            f"{result.trail_id:<22} {len(result.species):>5} species "
            f"({len(result.excluded_protected)} protected removed, "
            f"filter={result.protection_source})  top: {top}"
        )
        if args.names_out:
            args.names_out.mkdir(parents=True, exist_ok=True)
            (args.names_out / f"{result.trail_id}.txt").write_text(
                "\n".join(result.names) + "\n", encoding="utf-8"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
