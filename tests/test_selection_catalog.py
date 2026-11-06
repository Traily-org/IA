from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from traily_ia.trail_species.catalog import (
    TrailRecord,
    catalog_names,
    trail_names,
    write_catalog,
)
from traily_ia.trail_species.gbif import SpeciesOccurrences
from traily_ia.trail_species.selection import select_species


def occ(n: int, count: int) -> SpeciesOccurrences:
    return SpeciesOccurrences(
        species_key=n, scientific_name=f"Species {n:03}", occurrences=count
    )


def ladder(size: int) -> list[SpeciesOccurrences]:
    """Species 1..size with strictly decreasing counts, shuffled-safe."""
    return [occ(i, 1000 - i) for i in range(1, size + 1)]


def test_large_list_gets_common_majority_and_a_few_uncommon() -> None:
    chosen = select_species(ladder(500))

    assert len(chosen) == 20
    assert [s.tier for s in chosen].count("common") == 14
    common = [s for s in chosen if s.tier == "common"]
    uncommon = [s for s in chosen if s.tier == "uncommon"]
    assert [s.rank for s in common] == list(range(1, 15))  # the 14 most observed
    # uncommon ones come from beyond the top 20 % (rank 100) and are not rare-tail
    assert [s.rank for s in uncommon] == list(range(101, 107))
    assert max(s.rank for s in chosen) < 500 * 0.5


def test_small_trail_keeps_all_its_species() -> None:
    chosen = select_species(ladder(10))

    assert len(chosen) == 10
    assert [s.tier for s in chosen] == ["common"] * 7 + ["uncommon"] * 3


def test_very_rare_species_are_never_selected() -> None:
    species = [occ(1, 50), occ(2, 2), occ(3, 1)]

    assert [s.species.scientific_name for s in select_species(species)] == [
        "Species 001"
    ]


def test_list_just_above_the_cap_still_returns_the_cap() -> None:
    chosen = select_species(ladder(25))

    assert len(chosen) == 20
    assert len({s.species.scientific_name for s in chosen}) == 20


def test_ties_are_broken_by_name_for_stable_output() -> None:
    tied = [occ(3, 9), occ(1, 9), occ(2, 9)]

    names = [s.species.scientific_name for s in select_species(tied)]

    assert names == ["Species 001", "Species 002", "Species 003"]


def test_empty_input_and_bad_parameters() -> None:
    assert select_species([]) == []
    with pytest.raises(ValueError, match="max_species"):
        select_species(ladder(5), max_species=0)
    with pytest.raises(ValueError, match="uncommon_share"):
        select_species(ladder(5), uncommon_share=1.0)


def test_catalog_combines_trails_and_dedupes_shared_species(tmp_path: Path) -> None:
    db = tmp_path / "db" / "catalog.sqlite"
    a = TrailRecord("a", "Trail A", -1.7, 48.1, 5000, 1, select_species(ladder(8)))
    b = TrailRecord("b", None, 2.7, 48.4, None, None, select_species(ladder(4)))

    write_catalog(db, [a, b], {"protection_source": "test"})

    assert len(catalog_names(db)) == 8  # trail b's 4 species are a subset of a's
    assert trail_names(db, "b") == [f"Species {i:03}" for i in range(1, 5)]
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM trail_species").fetchone() == (12,)
        meta = dict(conn.execute("SELECT key, value FROM meta"))
    assert meta["protection_source"] == "test"


def test_catalog_lists_common_before_uncommon_and_rebuilds_from_scratch(
    tmp_path: Path,
) -> None:
    db = tmp_path / "catalog.sqlite"
    rec = TrailRecord("a", "A", 0.0, 0.0, None, None, select_species(ladder(10)))
    write_catalog(db, [rec], {})

    names = trail_names(db, "a")
    assert names[:7] == [f"Species {i:03}" for i in range(1, 8)]

    write_catalog(db, [], {})  # rebuilt, not appended to
    assert catalog_names(db) == []
