#!/usr/bin/env python
"""Build the protected-plants index from the two PatriNat archives.

    python scripts/build_inpn_index.py

Expects data/inpn/BDC.zip and data/inpn/TAXREF_v18_2025.zip (git-ignored); see
the README for where they come from. Writes data/inpn/protected_plants.json.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from traily_ia.trail_species.inpn import build_protected_index

SOURCE_URL = (
    "https://www.patrinat.fr/fr/page-temporaire-de-telechargement-des-"
    "referentiels-de-donnees-lies-linpn-7353"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--bdc", type=Path, default=Path("data/inpn/BDC.zip"))
    parser.add_argument(
        "--taxref", type=Path, default=Path("data/inpn/TAXREF_v18_2025.zip")
    )
    parser.add_argument(
        "--out", type=Path, default=Path("data/inpn/protected_plants.json")
    )
    args = parser.parse_args()

    index = build_protected_index(
        args.bdc, args.taxref, args.out, source_url=SOURCE_URL
    )
    print(f"{index.taxa} protected plant taxa, {index.names} names -> {args.out}")
    print(f"provenance: {index.provenance}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
