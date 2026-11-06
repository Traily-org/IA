#!/usr/bin/env python
"""How many species does each protection rule remove on each test trail?

    python scripts/eval_protection_scopes.py data/trails/*.geojson

Takes each trail's full GBIF species list (no protection filter) and counts the
species removed by the three INPN scopes: national only, the trail's own région and
département ("local", the default) and anywhere in metropolitan France. Writes
docs/results/protection_scopes.json as rows, one per trail.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from traily_ia.trail_species import GbifClient, NoProtectionFilter, build_trail_species
from traily_ia.trail_species.inpn import InpnProtectionFilter
from traily_ia.trail_species.location import locate_cached

LOCATION_CACHE = Path("data/cache/locations")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("trails", type=Path, nargs="+")
    parser.add_argument(
        "--inpn-index", type=Path, default=Path("data/inpn/protected_plants.json")
    )
    parser.add_argument(
        "--out", type=Path, default=Path("docs/results/protection_scopes.json")
    )
    args = parser.parse_args()

    base = InpnProtectionFilter.from_index(args.inpn_index)
    national = InpnProtectionFilter.from_index(args.inpn_index, scope="national")
    anywhere = InpnProtectionFilter.from_index(args.inpn_index, scope="anywhere")
    gbif = GbifClient()
    rows = []
    for path in sorted(args.trails):
        feature = json.loads(path.read_text(encoding="utf-8"))
        trail_id = feature["properties"]["trail_id"]
        lines = feature["geometry"]["coordinates"]
        with tempfile.TemporaryDirectory() as tmp:
            names = build_trail_species(
                trail_id,
                lines,
                gbif=gbif,
                protection=NoProtectionFilter(),
                cache_dir=Path(tmp),
            ).names
        local = base.for_location(locate_cached(trail_id, lines, LOCATION_CACHE))
        rows.append(
            {
                "trail_id": trail_id,
                "gbif_species": len(names),
                "removed_national": sum(national.is_protected(n) for n in names),
                "removed_local": sum(local.is_protected(n) for n in names),
                "removed_anywhere": sum(anywhere.is_protected(n) for n in names),
            }
        )
        print(rows[-1])

    payload = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "protection_source": base.source,
        "rows": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
