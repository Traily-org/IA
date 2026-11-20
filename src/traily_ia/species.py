"""Candidate species lists.

In production the list comes from the per-trail GBIF cache (ADR 0002). Until
that exists, the pipeline just takes a plain list of names.
"""

from __future__ import annotations

from pathlib import Path


def load_species_file(path: Path) -> list[str]:
    """Read one species name per line; blank lines and `#` comments are skipped.

    Duplicates are dropped (first occurrence wins) so a name is never scored twice.
    """
    names: list[str] = []
    seen: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line and line not in seen:
            seen.add(line)
            names.append(line)
    return names
