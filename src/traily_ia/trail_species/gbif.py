"""GBIF occurrence API: which plant species were observed inside a polygon."""

from __future__ import annotations

from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

import httpx

GBIF_API = "https://api.gbif.org/v1"
PLANTAE_TAXON_KEY = 6
FACET_PAGE_SIZE = 1000
# Wild-occurrence evidence only: no fossils, and no LIVING_SPECIMEN (botanical
# gardens, cultivated plants).
WILD_BASIS_OF_RECORD = (
    "HUMAN_OBSERVATION",
    "OBSERVATION",
    "PRESERVED_SPECIMEN",
    "MATERIAL_SAMPLE",
    "MATERIAL_CITATION",
    "OCCURRENCE",
)
# A 19th-century herbarium sheet is no evidence a species is there today.
DEFAULT_MIN_YEAR = 1990


@dataclass(frozen=True)
class SpeciesOccurrences:
    species_key: int
    # Canonical name without authorship — what BioCLIP is prompted with.
    scientific_name: str
    occurrences: int


class GbifClient:
    def __init__(self, http: httpx.Client | None = None) -> None:
        self._owns_http = http is None
        self._http = http or httpx.Client(
            base_url=GBIF_API,
            timeout=60.0,
            headers={"User-Agent": "traily-ia/0.1 (species list generation)"},
        )
        self._names: dict[int, str] = {}

    def _polygon_counts(self, wkt: str, min_year: int) -> list[tuple[int, int]]:
        """Species counts inside one polygon: one request per polygon keeps the URL
        short, however many disconnected parts the corridor has."""
        params: list[tuple[str, str | int]] = [
            ("taxonKey", PLANTAE_TAXON_KEY),
            ("hasCoordinate", "true"),
            ("hasGeospatialIssue", "false"),
            ("occurrenceStatus", "PRESENT"),
            ("year", f"{min_year},*"),
            ("limit", 0),
            ("facet", "speciesKey"),
            ("facetLimit", FACET_PAGE_SIZE),
        ]
        params += [("basisOfRecord", b) for b in WILD_BASIS_OF_RECORD]
        params.append(("geometry", wkt))

        counts: list[tuple[int, int]] = []
        offset = 0
        while True:
            response = self._http.get(
                "/occurrence/search", params=[*params, ("facetOffset", offset)]
            )
            response.raise_for_status()
            facets = response.json().get("facets", [])
            page = facets[0]["counts"] if facets else []
            counts += [(int(c["name"]), int(c["count"])) for c in page]
            if len(page) < FACET_PAGE_SIZE:
                return counts
            offset += FACET_PAGE_SIZE

    def _species_counts(
        self, wkts: Sequence[str], min_year: int
    ) -> list[tuple[int, int]]:
        # Corridors of one trail are disjoint polygons, so counts simply add up.
        totals: dict[int, int] = {}
        for wkt in wkts:
            for key, count in self._polygon_counts(wkt, min_year):
                totals[key] = totals.get(key, 0) + count
        return list(totals.items())

    def close(self) -> None:
        """Close the HTTP client, unless the caller supplied (and owns) it."""
        if self._owns_http:
            self._http.close()

    def species_name(self, species_key: int) -> str:
        """Canonical name (no authorship) of a GBIF species key."""
        return self._canonical_name(species_key)

    def _canonical_name(self, species_key: int) -> str:
        if species_key not in self._names:
            response = self._http.get(f"/species/{species_key}")
            response.raise_for_status()
            body = response.json()
            self._names[species_key] = (
                body.get("canonicalName") or body["scientificName"]
            )
        return self._names[species_key]

    def plantae_species(
        self, wkts: Sequence[str], *, min_year: int = DEFAULT_MIN_YEAR
    ) -> list[SpeciesOccurrences]:
        """Species with occurrences inside any of `wkts`, most observed first."""
        counts = self._species_counts(wkts, min_year)
        with ThreadPoolExecutor(max_workers=8) as pool:
            names = list(pool.map(self._canonical_name, (k for k, _ in counts)))
        # Two GBIF keys can share one canonical name (a synonym, a split taxon): group
        # by name so a species is listed once, with the records of all its keys.
        by_name: dict[str, SpeciesOccurrences] = {}
        for (key, n), name in zip(counts, names, strict=True):
            seen = by_name.get(name)
            if seen is None:
                by_name[name] = SpeciesOccurrences(key, name, n)
            else:
                best = seen.species_key if seen.occurrences >= n else key
                by_name[name] = SpeciesOccurrences(best, name, seen.occurrences + n)
        return sorted(
            by_name.values(), key=lambda s: (-s.occurrences, s.scientific_name)
        )
