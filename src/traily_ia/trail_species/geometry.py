"""Trail trace -> search polygon, in the shape GBIF's occurrence API accepts."""

from __future__ import annotations

from collections.abc import Sequence
from typing import cast

import numpy as np
import shapely
from pyproj import Transformer
from shapely import MultiLineString, MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient

# (lon, lat) pairs, WGS84 — GeoJSON / GBIF order.
LonLat = tuple[float, float]

DEFAULT_BUFFER_M = 500.0
# GBIF takes the polygon in the URL; keep each WKT comfortably below typical
# 8 KB request-line limits.
DEFAULT_MAX_WKT_CHARS = 6000


def _reproject(
    geometry: shapely.Geometry, transformer: Transformer
) -> shapely.Geometry:
    def apply(coords: np.ndarray) -> np.ndarray:
        x, y = transformer.transform(coords[:, 0], coords[:, 1])
        return np.column_stack([x, y])

    return cast(BaseGeometry, shapely.transform(geometry, apply))


def corridor_polygons(
    lines: Sequence[Sequence[LonLat]], *, buffer_m: float = DEFAULT_BUFFER_M
) -> list[Polygon]:
    """Buffer a trace (one or more line parts) by `buffer_m` metres.

    Parts need not be ordered or connected, so an OSM route relation's ways can
    be passed as they come. The buffer is computed in a local azimuthal
    equidistant projection centred on the trace, so metres are real metres
    anywhere on Earth. Returns one polygon per disconnected corridor.
    """
    parts = [list(line) for line in lines if len(line) >= 2]
    if not parts:
        raise ValueError("trace needs at least one line with two points")
    if buffer_m <= 0:
        raise ValueError("buffer_m must be positive")

    trace = MultiLineString(parts)
    lon0, lat0 = trace.centroid.x, trace.centroid.y
    local = f"+proj=aeqd +lat_0={lat0} +lon_0={lon0} +datum=WGS84 +units=m"
    forward = Transformer.from_crs("EPSG:4326", local, always_xy=True)
    backward = Transformer.from_crs(local, "EPSG:4326", always_xy=True)

    buffered = shapely.buffer(_reproject(trace, forward), buffer_m)
    shape = _reproject(buffered, backward)
    polygons = shape.geoms if isinstance(shape, MultiPolygon) else [shape]
    # Holes inside a corridor are loops of the trail: still near the trail, so fill.
    return [Polygon(p.exterior) for p in polygons if isinstance(p, Polygon)]


def _wkt(polygon: Polygon) -> str:
    # GBIF wants counter-clockwise exterior rings.
    ring = orient(polygon, sign=1.0).exterior.coords
    points = ", ".join(f"{x:.5f} {y:.5f}" for x, y in ring)
    return f"POLYGON(({points}))"


def to_gbif_wkts(
    polygons: Sequence[Polygon], *, max_chars: int = DEFAULT_MAX_WKT_CHARS
) -> list[str]:
    """WKT strings for GBIF's `geometry` parameter, simplified to fit in a URL.

    Simplification only ever happens in coarse steps (~10 m, doubling), so the
    search area stays within a few tens of metres of the requested buffer.
    """
    tolerance_deg = 0.0001  # ~11 m
    while True:
        simplified = [
            p.simplify(tolerance_deg, preserve_topology=True) for p in polygons
        ]
        wkts = [
            _wkt(p) for p in simplified if isinstance(p, Polygon) and not p.is_empty
        ]
        if wkts and all(len(w) <= max_chars for w in wkts):
            return wkts
        if tolerance_deg > 0.01:
            raise ValueError("polygon cannot be simplified enough for a GBIF query")
        tolerance_deg *= 2
