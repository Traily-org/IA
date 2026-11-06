"""Traily IA — species identification core logic (no HTTP layer here)."""

from traily_ia.pipeline import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    IdentificationPipeline,
    detect_and_classify,
)
from traily_ia.result import (
    BoundingBox,
    Detection,
    IdentificationResult,
    SpeciesScore,
)

__all__ = [
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "BoundingBox",
    "Detection",
    "IdentificationPipeline",
    "IdentificationResult",
    "SpeciesScore",
    "detect_and_classify",
]
