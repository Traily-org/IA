"""Small SQLite catalog: which species each trail asks the player to find.

The union of all trails' species is also the candidate list for `identify`, so the
catalog stays at a few hundred species instead of the whole French flora. This is
a local development artifact: the production source of truth belongs to `server`
(species referential, Story 2.1/2.2) — see TO_ASK.md.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from traily_ia.trail_species.selection import SelectedSpecies

SCHEMA = """
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE trails (
    trail_id TEXT PRIMARY KEY,
    name TEXT,
    lon REAL NOT NULL,
    lat REAL NOT NULL,
    length_m INTEGER,
    osm_relation INTEGER,
    departements TEXT NOT NULL DEFAULT '',
    regions TEXT NOT NULL DEFAULT ''
);
CREATE TABLE species (
    scientific_name TEXT PRIMARY KEY,
    gbif_species_key INTEGER NOT NULL
);
CREATE TABLE trail_species (
    trail_id TEXT NOT NULL REFERENCES trails(trail_id),
    scientific_name TEXT NOT NULL REFERENCES species(scientific_name),
    tier TEXT NOT NULL CHECK (tier IN ('common', 'uncommon')),
    rank INTEGER NOT NULL,
    occurrences INTEGER NOT NULL,
    PRIMARY KEY (trail_id, scientific_name)
);
"""


@dataclass(frozen=True)
class TrailRecord:
    trail_id: str
    name: str | None
    lon: float
    lat: float
    length_m: int | None
    osm_relation: int | None
    selected: Sequence[SelectedSpecies]
    # INSEE codes of the zone the trail runs through, comma-separated.
    departements: str = ""
    regions: str = ""


def write_catalog(
    path: Path, trails: Sequence[TrailRecord], meta: Mapping[str, str]
) -> None:
    """(Re)create the catalog file from scratch, in one transaction."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.unlink(missing_ok=True)
    with sqlite3.connect(path) as db:
        db.executescript(SCHEMA)
        db.executemany("INSERT INTO meta VALUES (?, ?)", sorted(meta.items()))
        for t in trails:
            db.execute(
                "INSERT INTO trails VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    t.trail_id,
                    t.name,
                    t.lon,
                    t.lat,
                    t.length_m,
                    t.osm_relation,
                    t.departements,
                    t.regions,
                ),
            )
            for s in t.selected:
                db.execute(
                    "INSERT OR IGNORE INTO species VALUES (?, ?)",
                    (s.species.scientific_name, s.species.species_key),
                )
                db.execute(
                    "INSERT INTO trail_species VALUES (?, ?, ?, ?, ?)",
                    (
                        t.trail_id,
                        s.species.scientific_name,
                        s.tier,
                        s.rank,
                        s.species.occurrences,
                    ),
                )
    db.close()


def catalog_names(path: Path) -> list[str]:
    """Every species of the catalog (candidates for `identify`), A to Z."""
    with sqlite3.connect(path) as db:
        rows = db.execute("SELECT scientific_name FROM species ORDER BY 1").fetchall()
    return [r[0] for r in rows]


def trail_names(path: Path, trail_id: str) -> list[str]:
    """One trail's species, common first then uncommon, each by decreasing rank."""
    with sqlite3.connect(path) as db:
        rows = db.execute(
            "SELECT scientific_name FROM trail_species WHERE trail_id = ? "
            "ORDER BY tier = 'uncommon', rank",
            (trail_id,),
        ).fetchall()
    return [r[0] for r in rows]
