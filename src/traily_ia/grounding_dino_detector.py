"""Stage 1 backend: Grounding DINO open-vocabulary detector (HuggingFace transformers).

Chosen over OWLv2, OWL-ViT and Grounding DINO base by `scripts/benchmark_detectors.py`
(ADR 0001): it found the subject on every benchmark photo, with a box
that overlapped the true one (IoU >= 0.5) on 88-95% of the pasted-subject cases,
at about the same speed as OWLv2.
"""

from __future__ import annotations

from collections.abc import Sequence

import torch
from PIL import Image
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

from traily_ia.owlv2_detector import DEFAULT_SCORE_FLOOR, clamp_box
from traily_ia.result import Detection

DEFAULT_MODEL_ID = "IDEA-Research/grounding-dino-tiny"
# Flora only (ADR 0002) — no fungi/animal prompts. Grounding DINO takes one text
# with the phrases separated by full stops.
DEFAULT_PROMPTS = ("a plant", "a flower", "a leaf")
# The processor's own default (shortest side 800) is slower for no gain here: at 512
# the box overlapped the true one (IoU >= 0.5) as often on 60 photos with the subject
# at 15% and 25% of the width (93-97%), and CPU time dropped by roughly 40%.
DEFAULT_SHORTEST_EDGE = 512


def pick_best_detection(
    scores: torch.Tensor, boxes: torch.Tensor, width: int, height: int
) -> Detection | None:
    """The highest-scoring box, clamped to the image; None if nothing is left."""
    if len(scores) == 0:
        return None
    best = int(torch.argmax(scores))
    x_min, y_min, x_max, y_max = (float(v) for v in boxes[best])
    box = clamp_box(x_min, y_min, x_max, y_max, width, height)
    if box is None:
        return None
    return Detection(box=box, score=float(scores[best]))


class GroundingDinoDetector:
    """Returns the single highest-scoring box over all prompts."""

    def __init__(
        self,
        *,
        model_id: str = DEFAULT_MODEL_ID,
        prompts: Sequence[str] = DEFAULT_PROMPTS,
        score_floor: float = DEFAULT_SCORE_FLOOR,
        device: str | None = None,
        shortest_edge: int = DEFAULT_SHORTEST_EDGE,
    ) -> None:
        self._device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._processor = AutoProcessor.from_pretrained(model_id)  # type: ignore[no-untyped-call]
        self._processor.image_processor.size = {
            "shortest_edge": shortest_edge,
            "longest_edge": round(shortest_edge * 1333 / 800),
        }
        model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id)
        self._model = model.to(self._device).eval()
        self._text = ". ".join(prompts) + "."
        self._score_floor = score_floor

    def detect(self, image: Image.Image) -> Detection | None:
        width, height = image.size
        inputs = self._processor(images=image, text=self._text, return_tensors="pt").to(
            self._device
        )
        with torch.no_grad():
            outputs = self._model(**inputs)
        results = self._processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=self._score_floor,
            text_threshold=self._score_floor,
            target_sizes=[(height, width)],
        )[0]
        return pick_best_detection(results["scores"], results["boxes"], width, height)
