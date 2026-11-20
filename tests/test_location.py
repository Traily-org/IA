"""Trail -> départements/régions, with the geo API replaced by a mock transport."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from traily_ia.trail_species.location import (
    MAX_POINTS,
    locate,
    locate_cached,
    sample_points,
)


def geo_client(
    table: dict[tuple[str, str], tuple[str, str] | None],
) -> tuple[httpx.Client, list[httpx.Request]]:
    """table: (rounded lon, rounded lat) -> (département, région) or None."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        key = (
            f"{float(request.url.params['lon']):.1f}",
            f"{float(request.url.params['lat']):.1f}",
        )
        hit = table[key]
        body = [{"codeDepartement": hit[0], "codeRegion": hit[1]}] if hit else []
        return httpx.Response(200, json=body)

    client = httpx.Client(
        base_url="https://geo.test", transport=httpx.MockTransport(handler)
    )
    return client, seen


def test_locate_collects_every_departement_and_region_crossed() -> None:
    client, _ = geo_client(
        {("-1.7", "48.1"): ("35", "53"), ("-2.2", "47.9"): ("56", "53")}
    )
    lines = [[(-1.7, 48.1), (-2.2, 47.9)]]

    location = locate(lines, http=client)

    assert location.departements == {"35", "56"}
    assert location.regions == {"53"}


def test_iso_codes_include_old_and_new_regions_and_departements() -> None:
    client, _ = geo_client({("7.0", "48.0"): ("68", "44")})

    location = locate([[(7.0, 48.0), (7.01, 48.0)]], http=client)

    assert location.iso_codes == {"FR-68", "FR-A", "FR-G", "FR-M"}


def test_point_outside_any_commune_is_skipped_but_all_outside_fails() -> None:
    client, _ = geo_client({("-1.7", "48.1"): ("35", "53"), ("-9.0", "40.0"): None})
    assert locate([[(-1.7, 48.1), (-9.0, 40.0)]], http=client).departements == {"35"}

    nothing, _ = geo_client({("-9.0", "40.0"): None})
    with pytest.raises(ValueError, match="commune"):
        locate([[(-9.0, 40.0), (-9.0, 40.001)]], http=nothing)


def test_overseas_region_is_rejected() -> None:
    client, _ = geo_client({("-61.5", "16.2"): ("971", "01")})

    with pytest.raises(ValueError, match="overseas"):
        locate([[(-61.5, 16.2), (-61.5, 16.201)]], http=client)


def test_sampling_dedupes_and_caps_the_number_of_lookups() -> None:
    dense = [[(-1.7 + i * 0.001, 48.1 + i * 0.001) for i in range(2000)]]

    points = sample_points(dense)

    assert len(points) <= MAX_POINTS
    assert points[0] == dense[0][0]
    assert len(sample_points([[(1.0, 2.0), (1.0001, 2.0001)]])) == 1  # same 1 km cell


def test_locate_cached_calls_the_api_once_per_trail(tmp_path: Path) -> None:
    client, seen = geo_client({("-1.7", "48.1"): ("35", "53")})
    lines = [[(-1.7, 48.1), (-1.701, 48.101)]]

    first = locate_cached("t", lines, tmp_path, http=client)
    calls = len(seen)
    second = locate_cached("t", lines, tmp_path, http=client)

    assert second == first
    assert len(seen) == calls


def border_client(boundary_lon: float) -> httpx.Client:
    """Département 35 west of `boundary_lon`, 22 east of it."""

    def handler(request: httpx.Request) -> httpx.Response:
        west = float(request.url.params["lon"]) < boundary_lon
        code = "35" if west else "22"
        return httpx.Response(200, json=[{"codeDepartement": code, "codeRegion": "53"}])

    return httpx.Client(
        base_url="https://geo.test", transport=httpx.MockTransport(handler)
    )


def test_a_border_inside_the_corridor_but_not_on_the_trace_is_found() -> None:
    # The trace stays in département 35; the border lies 300 m east of it, inside the
    # 500 m corridor GBIF will search, so département 22's protections must apply too.
    lines = [[(0.0, 48.0), (0.0, 48.01)]]

    location = locate(lines, http=border_client(boundary_lon=0.004))

    assert location.departements == {"35", "22"}


def test_a_client_made_by_locate_is_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    from traily_ia.trail_species import location as module

    made: list[httpx.Client] = []
    real_client = httpx.Client

    def make(**kwargs: object) -> httpx.Client:
        client = real_client(
            base_url="https://geo.test",
            transport=httpx.MockTransport(
                lambda r: httpx.Response(
                    200, json=[{"codeDepartement": "35", "codeRegion": "53"}]
                )
            ),
        )
        made.append(client)
        return client

    monkeypatch.setattr(module.httpx, "Client", make)

    locate([[(0.0, 48.0), (0.0, 48.01)]])

    assert made and all(c.is_closed for c in made)
