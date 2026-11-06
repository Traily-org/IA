"""Per-trail observable-species list: GBIF occurrences minus protected species."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from traily_ia.trail_species.gbif import (
    DEFAULT_MIN_YEAR,
    GbifClient,
    SpeciesOccurrences,
)
from traily_ia.trail_species.geometry import (
    DEFAULT_BUFFER_M,
    LonLat,
    corridor_polygons,
    to_gbif_wkts,
)
from traily_ia.trail_species.protection import ProtectionFilter


@dataclass(frozen=True)
class TrailSpeciesList:
    trail_id: str
    species: tuple[SpeciesOccurrences, ...]
    excluded_protected: tuple[SpeciesOccurrences, ...]
    protection_source: str
    buffer_m: float
    min_year: int
    created_at: str

    @property
    def names(self) -> list[str]:
        """Candidate names for `detect_and_classify`, most observed first."""
        return [s.scientific_name for s in self.species]


def _cache_key(wkts: Sequence[str], min_year: int, protection: ProtectionFilter) -> str:
    payload = json.dumps([sorted(wkts), min_year, protection.source])
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _load(path: Path) -> TrailSpeciesList:
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw.pop("cache_key")
    raw["species"] = tuple(SpeciesOccurrences(**s) for s in raw["species"])
    raw["excluded_protected"] = tuple(
        SpeciesOccurrences(**s) for s in raw["excluded_protected"]
    )
    return TrailSpeciesList(**raw)


def build_trail_species(
    trail_id: str,
    lines: Sequence[Sequence[LonLat]],
    *,
    gbif: GbifClient,
    protection: ProtectionFilter,
    cache_dir: Path,
    buffer_m: float = DEFAULT_BUFFER_M,
    min_year: int = DEFAULT_MIN_YEAR,
) -> TrailSpeciesList:
    """Return the trail's species list, querying GBIF only on a cache miss.

    The cache is keyed on the search polygon, the year cut-off and the
    protection source, so changing any of them regenerates the list.
    """
    wkts = to_gbif_wkts(corridor_polygons(lines, buffer_m=buffer_m))
    key = _cache_key(wkts, min_year, protection)
    cache_path = cache_dir / f"{trail_id}.json"
    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if cached.get("cache_key") == key:
            return _load(cache_path)

    found = gbif.plantae_species(wkts, min_year=min_year)
    kept = tuple(s for s in found if not protection.is_protected(s.scientific_name))
    dropped = tuple(s for s in found if protection.is_protected(s.scientific_name))
    result = TrailSpeciesList(
        trail_id=trail_id,
        species=kept,
        excluded_protected=dropped,
        protection_source=protection.source,
        buffer_m=buffer_m,
        min_year=min_year,
        created_at=datetime.now(UTC).isoformat(timespec="seconds"),
    )
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps({"cache_key": key, **asdict(result)}, indent=1, ensure_ascii=False),
        encoding="utf-8",
    )
    return result
