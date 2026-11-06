"""Stage interfaces for the two-stage pipeline.

ADR 0001 has not settled on a detector yet, so the pipeline depends on these
protocols rather than on any concrete model. Swapping YOLO-World / OWLv2 /
Grounding DINO means adding one class here-and-there, not touching the pipeline.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from PIL import Image

from traily_ia.result import Detection, SpeciesScore


class Detector(Protocol):
    """Stage 1 — localise the single main subject of a trail photo."""

    def detect(self, image: Image.Image) -> Detection | None:
        """Return the best box, or None if no subject is found."""
        ...


class Classifier(Protocol):
    """Stage 2 — match a cropped subject against candidate species."""

    def classify(
        self, crop: Image.Image, candidates: Sequence[str]
    ) -> list[SpeciesScore]:
        """Return every candidate with its probability, best first.

        Scores are a softmax over `candidates`, so they sum to ~1 and are only
        meaningful relative to that candidate list.
        """
        ...
