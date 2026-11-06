#!/usr/bin/env python
"""Build the French common-name table for the catalog species.

    python scripts/build_french_names.py

Reads TaxRef (data/inpn/TAXREF/) and the species of data/species_lists/catalog.txt,
writes data/species_lists/french_names.json. Names are display-only; scientific
names stay the key everywhere (README, "Common names").
"""

from __future__ import annotations

import argparse
from pathlib import Path

from traily_ia.species import load_species_file
from traily_ia.trail_species.vernacular import build_french_names, save_french_names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--taxref-dir", type=Path, default=Path("data/inpn/TAXREF"))
    parser.add_argument(
        "--species-file", type=Path, default=Path("data/species_lists/catalog.txt")
    )
    parser.add_argument(
        "--out", type=Path, default=Path("data/species_lists/french_names.json")
    )
    args = parser.parse_args()

    species = load_species_file(args.species_file)
    names = build_french_names(
        args.taxref_dir / "TAXREFv18.txt", args.taxref_dir / "TAXVERNv18.txt", species
    )
    save_french_names(names, args.out)
    missing = [s for s in species if s not in names]
    print(f"{len(names)}/{len(species)} species have a French name -> {args.out}")
    if missing:
        print("No French name (scientific name shown instead):", ", ".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
