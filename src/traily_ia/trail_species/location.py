"""Which French départements and régions a trail runs through.

Used so the protection filter only applies the protections that hold where the
trail actually is (a plant protected only in Alsace stays listable in Brittany).
Lookups use the French government's geo API (https://geo.api.gouv.fr), one call
per sampled point of the trace; results are cached per trail.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import httpx

from traily_ia.trail_species.geometry import LonLat

GEO_API = "https://geo.api.gouv.fr"
MAX_POINTS = 40
# The BDC dataset still labels regional protections with the pre-2016 regions
# (ISO 3166-2 codes), so each current region (INSEE code) maps to every ISO region
# code that applies inside it, old and new.
REGION_ISO_CODES: dict[str, frozenset[str]] = {
    "11": frozenset({"FR-J"}),  # Île-de-France
    "24": frozenset({"FR-CVL"}),  # Centre-Val de Loire
    "27": frozenset({"FR-D", "FR-I"}),  # Bourgogne, Franche-Comté
    "28": frozenset({"FR-P", "FR-Q"}),  # Basse-, Haute-Normandie
    "32": frozenset({"FR-O", "FR-S"}),  # Nord-Pas-de-Calais, Picardie
    "44": frozenset({"FR-A", "FR-G", "FR-M"}),  # Alsace, Champagne-Ardenne, Lorraine
    "52": frozenset({"FR-PDL"}),  # Pays de la Loire
    "53": frozenset({"FR-BRE"}),  # Bretagne
    "75": frozenset({"FR-B", "FR-L", "FR-T"}),  # Aquitaine, Limousin, Poitou-Charentes
    "76": frozenset({"FR-K", "FR-N"}),  # Languedoc-Roussillon, Midi-Pyrénées
    "84": frozenset({"FR-C", "FR-V"}),  # Auvergne, Rhône-Alpes
    "93": frozenset({"FR-U"}),  # Provence-Alpes-Côte d'Azur
    "94": frozenset({"FR-H"}),  # Corse
}


@dataclass(frozen=True)
class Location:
    departements: frozenset[str]  # INSEE codes: "35", "2A", ...
    regions: frozenset[str]  # current-region INSEE codes: "53", ...

    @property
    def iso_codes(self) -> frozenset[str]:
        """ISO 3166-2 codes of every zone whose protections apply here."""
        codes = {f"FR-{d}" for d in self.departements}
        for region in self.regions:
            codes |= REGION_ISO_CODES[region]
        return frozenset(codes)


def sample_points(lines: Sequence[Sequence[LonLat]]) -> list[LonLat]:
    """Distinct points (~1 km grid) of the trace, at most MAX_POINTS of them."""
    seen: dict[tuple[float, float], LonLat] = {}
    for line in lines:
        for lon, lat in line:
            seen.setdefault((round(lon, 2), round(lat, 2)), (lon, lat))
    points = list(seen.values())
    if len(points) <= MAX_POINTS:
        return points
    step = (len(points) - 1) / (MAX_POINTS - 1)
    return [points[round(i * step)] for i in range(MAX_POINTS)]


def locate(
    lines: Sequence[Sequence[LonLat]], *, http: httpx.Client | None = None
) -> Location:
    """Départements and régions of the trace, via geo.api.gouv.fr.

    Raises if no point resolves to a metropolitan commune: the filter must never
    quietly fall back to "no protections apply".
    """
    client = http or httpx.Client(base_url=GEO_API, timeout=30.0)
    points = sample_points(lines)

    def lookup(point: LonLat) -> dict[str, str] | None:
        response = client.get(
            "/communes",
            params={
                "lon": point[0],
                "lat": point[1],
                "fields": "codeDepartement,codeRegion",
            },
        )
        response.raise_for_status()
        found = response.json()
        return found[0] if found else None

    with ThreadPoolExecutor(max_workers=8) as pool:
        communes = [c for c in pool.map(lookup, points) if c]
    departements = frozenset(c["codeDepartement"] for c in communes)
    regions = frozenset(c["codeRegion"] for c in communes)
    if not communes:
        raise ValueError("trail is not in any French commune (geo.api.gouv.fr)")
    unknown = regions - REGION_ISO_CODES.keys()
    if unknown:
        raise ValueError(f"unsupported (overseas?) region codes: {sorted(unknown)}")
    return Location(departements, regions)


def locate_cached(
    trail_id: str,
    lines: Sequence[Sequence[LonLat]],
    cache_dir: Path,
    *,
    http: httpx.Client | None = None,
) -> Location:
    """`locate`, remembered per trail (keyed on the sampled points)."""
    points = sample_points(lines)
    key = hashlib.sha256(json.dumps(points).encode()).hexdigest()[:16]
    path = cache_dir / f"{trail_id}.json"
    if path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        if cached["key"] == key:
            return Location(
                frozenset(cached["departements"]), frozenset(cached["regions"])
            )
    location = locate(lines, http=http)
    cache_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "key": key,
                "departements": sorted(location.departements),
                "regions": sorted(location.regions),
            }
        ),
        encoding="utf-8",
    )
    return location
