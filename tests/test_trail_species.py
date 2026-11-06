"""Trail species list generation, with GBIF replaced by an in-memory transport."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest
from shapely import Point
from shapely.geometry import Polygon

from traily_ia.trail_species import (
    GbifClient,
    NoProtectionFilter,
    build_trail_species,
)
from traily_ia.trail_species.geometry import corridor_polygons, to_gbif_wkts

# ~1.5 km east-west near Rennes
TRACE = [[(-1.700, 48.100), (-1.690, 48.100), (-1.680, 48.105)]]


class DummyProtection:
    source = "test-protection-v1"

    def is_protected(self, scientific_name: str) -> bool:
        return scientific_name == "Orchis protecta"


def fake_gbif(
    counts: list[tuple[int, int]], names: dict[int, str]
) -> tuple[GbifClient, list[httpx.Request]]:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path.endswith("/occurrence/search"):
            offset = int(request.url.params.get("facetOffset", 0))
            page = counts[offset : offset + 1000]
            facet = [{"name": str(k), "count": n} for k, n in page]
            return httpx.Response(200, json={"facets": [{"counts": facet}]})
        key = int(request.url.path.rsplit("/", 1)[1])
        return httpx.Response(200, json={"canonicalName": names[key]})

    http = httpx.Client(
        base_url="https://gbif.test/v1", transport=httpx.MockTransport(handler)
    )
    return GbifClient(http), seen


def test_corridor_contains_trace_and_has_roughly_requested_width() -> None:
    (polygon,) = corridor_polygons(TRACE, buffer_m=500)

    assert all(polygon.contains(Point(x, y)) for x, y in TRACE[0])
    # 400 m north of the trace is inside a 500 m buffer, 700 m is not.
    assert polygon.contains(Point(-1.690, 48.100 + 400 / 111_000))
    assert not polygon.contains(Point(-1.690, 48.100 + 700 / 111_000))


def test_disconnected_parts_give_separate_polygons() -> None:
    far_apart = [[(-1.70, 48.10), (-1.69, 48.10)], [(-1.20, 48.50), (-1.19, 48.50)]]

    assert len(corridor_polygons(far_apart, buffer_m=300)) == 2


@pytest.mark.parametrize("bad", [[], [[(0.0, 0.0)]]])
def test_trace_without_a_line_is_rejected(bad: list[list[tuple[float, float]]]) -> None:
    with pytest.raises(ValueError, match="two points"):
        corridor_polygons(bad)


def test_wkt_is_counter_clockwise_and_fits_the_url_budget() -> None:
    # A jagged 3000-vertex corridor that must be simplified to fit.
    line = [(-1.7 + i * 0.00001, 48.1 + (0.0002 if i % 2 else 0)) for i in range(3000)]
    polygons = corridor_polygons([line], buffer_m=200)

    (wkt,) = to_gbif_wkts(polygons, max_chars=3000)

    assert len(wkt) <= 3000
    ring = [
        tuple(map(float, p.split())) for p in wkt[len("POLYGON((") : -2].split(", ")
    ]
    assert Polygon(ring).exterior.is_ccw


def test_gbif_pages_facets_and_resolves_names_once() -> None:
    counts = [(i, 1000 - i) for i in range(1, 1501)]  # forces a second facet page
    names = {i: f"Species {i}" for i in range(1, 1501)}
    gbif, seen = fake_gbif(counts, names)

    species = gbif.plantae_species(["POLYGON((0 0, 1 0, 1 1, 0 0))"])

    assert len(species) == 1500
    assert species[0].scientific_name == "Species 1" and species[0].occurrences == 999
    assert sum(r.url.path.endswith("/occurrence/search") for r in seen) == 2
    gbif.plantae_species(["POLYGON((0 0, 1 0, 1 1, 0 0))"])
    assert sum(r.url.path.startswith("/v1/species/") for r in seen) == 1500  # cached


def test_build_removes_protected_species_and_reports_them(tmp_path: Path) -> None:
    gbif, _ = fake_gbif([(1, 50), (2, 5)], {1: "Bellis perennis", 2: "Orchis protecta"})

    result = build_trail_species(
        "t1", TRACE, gbif=gbif, protection=DummyProtection(), cache_dir=tmp_path
    )

    assert result.names == ["Bellis perennis"]
    assert [s.scientific_name for s in result.excluded_protected] == ["Orchis protecta"]
    assert result.protection_source == "test-protection-v1"


def test_second_build_is_served_from_cache(tmp_path: Path) -> None:
    gbif, seen = fake_gbif([(1, 50)], {1: "Bellis perennis"})
    first = build_trail_species(
        "t1", TRACE, gbif=gbif, protection=DummyProtection(), cache_dir=tmp_path
    )
    calls = len(seen)

    second = build_trail_species(
        "t1", TRACE, gbif=gbif, protection=DummyProtection(), cache_dir=tmp_path
    )

    assert second == first
    assert len(seen) == calls


def test_changing_protection_source_or_polygon_invalidates_cache(
    tmp_path: Path,
) -> None:
    gbif, seen = fake_gbif([(1, 50)], {1: "Bellis perennis"})
    build_trail_species(
        "t1", TRACE, gbif=gbif, protection=DummyProtection(), cache_dir=tmp_path
    )
    calls = len(seen)

    build_trail_species(
        "t1", TRACE, gbif=gbif, protection=NoProtectionFilter(), cache_dir=tmp_path
    )
    after_filter_change = len(seen)
    build_trail_species(
        "t1",
        TRACE,
        gbif=gbif,
        protection=NoProtectionFilter(),
        cache_dir=tmp_path,
        buffer_m=900,
    )

    assert after_filter_change > calls
    assert len(seen) > after_filter_change


def test_unfiltered_lists_are_marked_in_their_source() -> None:
    assert "UNFILTERED" in NoProtectionFilter().source
