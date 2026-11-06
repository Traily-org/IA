"""INPN index + filter, built from tiny synthetic BDC/TAXREF archives."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from datetime import date
from pathlib import Path

import pytest

from traily_ia.trail_species.inpn import InpnProtectionFilter, build_protected_index
from traily_ia.trail_species.location import Location

BDC_COLUMNS = [
    "REGNE",
    "CD_TYPE_STATUT",
    "CD_REF",
    "LB_NOM",
    "LB_ADM_TR",
    "CODE_STATUT",
    "CD_ISO3166_2",
]
TAXREF_COLUMNS = ["CD_NOM", "CD_REF", "RANG", "LB_NOM"]

BDC_ROWS = [
    # Nationally protected species, with a synonym in TAXREF.
    ["Plantae", "PN", "1", "Armeria ruscinonensis", "France métropolitaine", "NV1", ""],
    # Regionally protected only.
    ["Plantae", "PR", "2", "Orchis militaris", "Centre", "RV24", "FR-CVL"],
    # Protected overseas only: irrelevant to metropolitan trails.
    ["Plantae", "PR", "3", "Metrosideros collina", "Guyane", "GF1", "FR-GF"],
    # Accepted protected subspecies: its parent species becomes unsafe.
    ["Plantae", "PD", "4", "Gentiana lutea subsp. aurantiaca", "Isère", "D38", "FR-38"],
    # Protected species whose TAXREF synonyms include a subspecies named after a
    # common species (the real Bellis sylvestris case).
    ["Plantae", "PR", "5", "Bellis sylvestris", "Poitou-Charentes", "RV54", "FR-T"],
    # Not protection (red list) and not a plant: both ignored.
    ["Plantae", "LRN", "6", "Bellis rotundifolia", "France métropolitaine", "VU", ""],
    ["Animalia", "PN", "7", "Ursus arctos", "France métropolitaine", "A1", ""],
]
TAXREF_ROWS = [
    ["1", "1", "ES", "Armeria ruscinonensis"],
    ["11", "1", "ES", "Armeria arenaria var. old-name"],
    ["12", "1", "ES", "Statice ruscinonensis"],
    ["2", "2", "ES", "Orchis militaris"],
    ["3", "3", "ES", "Metrosideros collina"],
    ["4", "4", "SSES", "Gentiana lutea subsp. aurantiaca"],
    ["5", "5", "ES", "Bellis sylvestris"],
    ["51", "5", "SSES", "Bellis perennis subsp. sylvestris"],
    ["8", "8", "ES", "Bellis perennis"],
]


def _csv_text(columns: list[str], rows: list[list[str]], delimiter: str = ",") -> str:
    out = io.StringIO()
    writer = csv.writer(out, delimiter=delimiter)
    writer.writerow(columns)
    writer.writerows(rows)
    return out.getvalue()


def _zip(path: Path, member: str, text: str, stamp: tuple[int, ...]) -> Path:
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr(zipfile.ZipInfo(member, date_time=stamp), text)  # type: ignore[arg-type]
    return path


@pytest.fixture
def index_path(tmp_path: Path) -> Path:
    bdc = _zip(
        tmp_path / "BDC.zip",
        "BDC_18/bdc_18_01.csv",
        _csv_text(BDC_COLUMNS, BDC_ROWS),
        (2025, 7, 24, 0, 0, 0),
    )
    taxref = _zip(
        tmp_path / "TAXREF.zip",
        "TAXREFv18.txt",
        _csv_text(TAXREF_COLUMNS, TAXREF_ROWS, delimiter="\t"),
        (2025, 1, 9, 0, 0, 0),
    )
    out = tmp_path / "index.json"
    build_protected_index(bdc, taxref, out, source_url="https://example.test/page")
    return out


def test_index_records_provenance_of_both_inputs(index_path: Path) -> None:
    prov = json.loads(index_path.read_text(encoding="utf-8"))["provenance"]

    assert prov["bdc"]["content_date"] == "2025-07-24"
    assert prov["taxref"]["content_date"] == "2025-01-09"
    assert prov["bdc"]["version"] == prov["taxref"]["version"] == "18"
    assert len(prov["bdc"]["zip_sha256"]) == 64
    assert prov["source_url"] == "https://example.test/page"


def test_anywhere_scope_flags_national_regional_and_synonyms(index_path: Path) -> None:
    f = InpnProtectionFilter.from_index(index_path, scope="anywhere")

    assert f.is_protected("Armeria ruscinonensis")  # national
    assert f.is_protected("Statice ruscinonensis")  # synonym of a protected taxon
    assert f.is_protected("Orchis militaris")  # regional only
    assert f.is_protected("Gentiana lutea")  # parent of a protected subspecies


def test_national_scope_ignores_regional_protection(index_path: Path) -> None:
    f = InpnProtectionFilter.from_index(index_path, scope="national")

    assert f.is_protected("Armeria ruscinonensis")
    assert not f.is_protected("Orchis militaris")


def test_overseas_only_protection_does_not_affect_metropolitan_lists(
    index_path: Path,
) -> None:
    f = InpnProtectionFilter.from_index(index_path, scope="anywhere")

    assert not f.is_protected("Metrosideros collina")


def test_common_species_named_by_a_synonym_subspecies_is_not_flagged(
    index_path: Path,
) -> None:
    """Regression: 'Bellis perennis subsp. sylvestris' is a synonym of the protected
    Bellis sylvestris, which must not make the common daisy protected."""
    f = InpnProtectionFilter.from_index(index_path, scope="anywhere")

    assert f.is_protected("Bellis sylvestris")
    assert not f.is_protected("Bellis perennis")


def test_non_protection_statuses_and_other_kingdoms_are_ignored(
    index_path: Path,
) -> None:
    f = InpnProtectionFilter.from_index(index_path, scope="anywhere")

    assert not f.is_protected("Bellis rotundifolia")  # red list only
    assert not f.is_protected("Ursus arctos")  # animal


def test_source_names_the_data_versions_and_scope(index_path: Path) -> None:
    f = InpnProtectionFilter.from_index(index_path, scope="national")

    assert f.source.startswith("inpn-bdc18-2025-07-24+taxref18-2025-01-09#")
    assert f.source.endswith(":national")


def test_staleness_is_measured_from_the_oldest_input(index_path: Path) -> None:
    f = InpnProtectionFilter.from_index(index_path)

    assert f.data_date == date(2025, 1, 9)
    assert not f.is_stale(today=date(2025, 12, 31))
    assert f.is_stale(today=date(2026, 10, 9))


def test_missing_index_fails_instead_of_silently_not_filtering(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="unfiltered"):
        InpnProtectionFilter.from_index(tmp_path / "nope.json")


def test_source_changes_when_the_index_content_changes(index_path: Path) -> None:
    before = InpnProtectionFilter.from_index(index_path).source
    raw = json.loads(index_path.read_text(encoding="utf-8"))
    raw["aliases"].pop("Statice ruscinonensis")
    index_path.write_text(json.dumps(raw), encoding="utf-8")

    after = InpnProtectionFilter.from_index(index_path).source

    assert after != before  # cached lists built with the old rules get rebuilt


BRETAGNE = Location(frozenset({"35"}), frozenset({"53"}))
CENTRE = Location(frozenset({"45"}), frozenset({"24"}))
ISERE_AURA = Location(frozenset({"38"}), frozenset({"84"}))
POITOU = Location(frozenset({"86"}), frozenset({"75"}))  # new region Nouvelle-Aquitaine


def test_local_scope_applies_only_the_trails_own_regional_protections(
    index_path: Path,
) -> None:
    base = InpnProtectionFilter.from_index(index_path)

    assert base.for_location(CENTRE).is_protected("Orchis militaris")  # FR-CVL
    assert not base.for_location(BRETAGNE).is_protected("Orchis militaris")


def test_local_scope_always_applies_national_protection(index_path: Path) -> None:
    base = InpnProtectionFilter.from_index(index_path)

    assert base.for_location(BRETAGNE).is_protected("Armeria ruscinonensis")
    assert base.for_location(BRETAGNE).is_protected("Statice ruscinonensis")


def test_local_scope_matches_departement_protection(index_path: Path) -> None:
    base = InpnProtectionFilter.from_index(index_path)

    assert base.for_location(ISERE_AURA).is_protected("Gentiana lutea")  # FR-38
    assert not base.for_location(CENTRE).is_protected("Gentiana lutea")


def test_old_region_protection_applies_inside_the_new_merged_region(
    index_path: Path,
) -> None:
    """Bellis sylvestris is protected in the former Poitou-Charentes (FR-T), which
    is now part of Nouvelle-Aquitaine (INSEE 75)."""
    base = InpnProtectionFilter.from_index(index_path)

    assert base.for_location(POITOU).is_protected("Bellis sylvestris")
    assert not base.for_location(BRETAGNE).is_protected("Bellis sylvestris")


def test_local_scope_without_a_location_fails_instead_of_guessing(
    index_path: Path,
) -> None:
    f = InpnProtectionFilter.from_index(index_path, scope="local")

    with pytest.raises(ValueError, match="location"):
        f.is_protected("Orchis militaris")


def test_source_of_a_local_filter_names_its_zone(index_path: Path) -> None:
    base = InpnProtectionFilter.from_index(index_path)

    assert base.for_location(BRETAGNE).source.endswith(":local[FR-35,FR-BRE]")
    assert base.for_location(BRETAGNE).source != base.for_location(CENTRE).source


def test_index_build_refuses_a_zone_code_it_cannot_place(tmp_path: Path) -> None:
    rows = [
        ["Plantae", "PR", "9", "Nowhere nowhere", "Atlantis", "X", "FR-ZZ"],
    ]
    bdc = _zip(
        tmp_path / "BDC.zip",
        "BDC_18/bdc_18_01.csv",
        _csv_text(BDC_COLUMNS, rows),
        (2025, 7, 24, 0, 0, 0),
    )
    taxref = _zip(
        tmp_path / "T.zip",
        "TAXREFv18.txt",
        _csv_text(TAXREF_COLUMNS, [], delimiter="\t"),
        (2025, 1, 9, 0, 0, 0),
    )

    with pytest.raises(ValueError, match="FR-ZZ"):
        build_protected_index(bdc, taxref, tmp_path / "i.json", source_url="x")
