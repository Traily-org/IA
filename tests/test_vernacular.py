"""French common names from TaxRef-style tables."""

from __future__ import annotations

from pathlib import Path

from traily_ia.trail_species.vernacular import (
    build_french_names,
    first_name,
    load_french_names,
    save_french_names,
)

TAXREF = (
    "CD_NOM\tCD_REF\tLB_NOM\n1\t1\tAbies alba\n2\t1\tPicea synonym\n3\t3\tNo name\n"
)
TAXVERN = (
    "CD_VERN\tCD_NOM\tLB_VERN\tISO639_3\n"
    '10\t1\t"Sapin blanc, Sapin pectiné"\tfra\n'
    '11\t1\t"Silver fir"\teng\n'
)


def write(tmp_path: Path) -> tuple[Path, Path]:
    taxref, taxvern = tmp_path / "ref.txt", tmp_path / "vern.txt"
    taxref.write_text(TAXREF, encoding="utf-8")
    taxvern.write_text(TAXVERN, encoding="utf-8")
    return taxref, taxvern


def test_first_listed_french_name_is_kept(tmp_path: Path) -> None:
    taxref, taxvern = write(tmp_path)

    names = build_french_names(taxref, taxvern, ["Abies alba"])

    assert names == {"Abies alba": "Sapin blanc"}


def test_a_synonym_gets_the_name_of_its_accepted_taxon(tmp_path: Path) -> None:
    taxref, taxvern = write(tmp_path)

    names = build_french_names(taxref, taxvern, ["Picea synonym"])

    assert names == {"Picea synonym": "Sapin blanc"}


def test_species_without_a_french_name_are_left_out(tmp_path: Path) -> None:
    taxref, taxvern = write(tmp_path)

    assert build_french_names(taxref, taxvern, ["No name", "Unknown"]) == {}


def test_names_survive_a_save_and_load(tmp_path: Path) -> None:
    path = tmp_path / "names.json"
    save_french_names({"Abies alba": "Sapin blanc"}, path)

    assert load_french_names(path) == {"Abies alba": "Sapin blanc"}


def test_first_name_splits_on_commas() -> None:
    assert first_name("Érable sycomore, Grand Érable") == "Érable sycomore"
