"""French common names for species, from TaxRef's vernacular-name table.

The pipeline always works on scientific names (unambiguous). Common names are
display-only: `server` or the app shows "Chêne pédonculé" while the scientific name
stays the key. A species with no French name keeps no common name (the caller falls
back to the scientific name).
"""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from pathlib import Path


def _read(path: Path) -> Iterable[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        yield from csv.DictReader(fh, delimiter="\t")


def first_name(raw: str) -> str:
    """TaxRef lists several names in one cell ("Sapin blanc, Sapin pectiné"): keep the
    first, which is the most usual one."""
    return raw.split(",")[0].strip()


def build_french_names(
    taxref: Path, taxvern: Path, scientific_names: Iterable[str]
) -> dict[str, str]:
    """Map each scientific name to its French common name, when TaxRef has one.

    A name is looked up under its own TaxRef id and under the id of the accepted name
    it is a synonym of. When several French entries exist the first listed wins.
    """
    wanted = set(scientific_names)
    ids: dict[str, set[str]] = {}
    for row in _read(taxref):
        if row["LB_NOM"] in wanted:
            ids.setdefault(row["LB_NOM"], set()).update((row["CD_NOM"], row["CD_REF"]))
    french: dict[str, str] = {}
    for row in _read(taxvern):
        if row["ISO639_3"] == "fra" and row["LB_VERN"].strip():
            french.setdefault(row["CD_NOM"], first_name(row["LB_VERN"]))
    out: dict[str, str] = {}
    for name in sorted(wanted):
        for cd in sorted(ids.get(name, ())):
            if cd in french:
                out[name] = french[cd]
                break
    return out


def save_french_names(names: dict[str, str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(names, ensure_ascii=False, indent=1), encoding="utf-8")


def load_french_names(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in data.items()}
