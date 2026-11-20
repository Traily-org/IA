"""Plain data types returned by the identification pipeline.

Deliberately framework-free (stdlib dataclasses only): the future FastAPI layer
maps these onto its own Pydantic response models, so the `/identify` contract
can change without touching the core logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AbstainReason = Literal["no_subject_detected", "low_confidence", "unknown_species"]


@dataclass(frozen=True)
class BoundingBox:
    """Axis-aligned box in pixel coordinates of the *original* image."""

    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def width(self) -> float:
        return self.x_max - self.x_min

    @property
    def height(self) -> float:
        return self.y_max - self.y_min


@dataclass(frozen=True)
class Detection:
    """Output of stage 1: the single most likely main subject."""

    box: BoundingBox
    score: float


@dataclass(frozen=True)
class SpeciesScore:
    """One candidate species with its probability among the candidates."""

    species: str
    score: float
    # Raw cosine similarity between the photo and the species name (BioCLIP only).
    # Unlike `score` it does not depend on the other candidates, so it can tell a
    # good match from the least-bad of a list that lacks the true species.
    similarity: float | None = None
    # French common name for display only; None when unknown. `species` stays the key.
    common_name: str | None = None


@dataclass(frozen=True)
class IdentificationResult:
    """Result of `detect_and_classify` for one photo.

    When `abstained` is true, `species` is None: the pipeline never guesses
    (CLAUDE.md — route to human moderation instead). `alternatives` still
    carries the ranked candidates (when a subject was found) for the
    moderation queue and for debugging.
    """

    species: str | None
    confidence: float
    bbox: BoundingBox | None
    abstained: bool
    abstain_reason: AbstainReason | None
    detection_score: float
    image_width: int
    image_height: int
    alternatives: tuple[SpeciesScore, ...] = ()
    # False when the classifier saw the whole photo instead of the detector's crop.
    used_crop: bool = True
    # French common name of `species` (display only), None if abstained or unknown.
    common_name: str | None = None
