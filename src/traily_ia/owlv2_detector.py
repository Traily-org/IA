"""Stage 1 backend: OWLv2 open-vocabulary detector (HuggingFace transformers).

Provisional default — ADR 0001 lists OWLv2, YOLO-World and Grounding DINO as
candidates and none has been benchmarked yet. OWLv2 is used here because it is
the simplest to run on CPU or GPU; it sits behind the `Detector` protocol so
the others can replace it without touching the pipeline.
"""

from __future__ import annotations

from collections.abc import Sequence

import torch
from PIL import Image
from transformers import Owlv2ForObjectDetection, Owlv2Processor

from traily_ia.result import BoundingBox, Detection

DEFAULT_MODEL_ID = "google/owlv2-base-patch16-ensemble"
# Flora only (ADR 0002) — no fungi/animal prompts.
DEFAULT_PROMPTS = ("a photo of a plant", "a photo of a flower", "a photo of a leaf")
# OWLv2 scores run low even for correct boxes; this is a floor, not a confidence.
DEFAULT_SCORE_FLOOR = 0.1


def clamp_box(
    x_min: float, y_min: float, x_max: float, y_max: float, width: int, height: int
) -> BoundingBox | None:
    """Clamp a box to the image; None if nothing is left inside it."""
    box = BoundingBox(
        x_min=min(max(x_min, 0.0), width),
        y_min=min(max(y_min, 0.0), height),
        x_max=min(max(x_max, 0.0), width),
        y_max=min(max(y_max, 0.0), height),
    )
    if box.width <= 0 or box.height <= 0:
        return None
    return box


class Owlv2Detector:
    """Returns the single highest-scoring box over all prompts."""

    def __init__(
        self,
        *,
        model_id: str = DEFAULT_MODEL_ID,
        prompts: Sequence[str] = DEFAULT_PROMPTS,
        score_floor: float = DEFAULT_SCORE_FLOOR,
        device: str | None = None,
    ) -> None:
        self._device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._processor = Owlv2Processor.from_pretrained(model_id)
        model = Owlv2ForObjectDetection.from_pretrained(model_id)
        # transformers 5 types `.to` as an unbound wrapper, so mypy rejects the device.
        self._model = model.to(self._device).eval()  # type: ignore[arg-type]
        self._prompts = list(prompts)
        self._score_floor = score_floor

    def detect(self, image: Image.Image) -> Detection | None:
        width, height = image.size
        inputs = self._processor(
            text=[self._prompts], images=image, return_tensors="pt"
        ).to(self._device)
        with torch.no_grad():
            outputs = self._model(**inputs)

        # OWLv2 pads the image to a square before inference, so boxes come back
        # relative to the padded square, not the original image.
        side = max(width, height)
        results = self._processor.post_process_grounded_object_detection(
            outputs, threshold=self._score_floor, target_sizes=[(side, side)]
        )[0]
        if len(results["scores"]) == 0:
            return None

        best = int(torch.argmax(results["scores"]))
        x_min, y_min, x_max, y_max = (float(v) for v in results["boxes"][best])
        box = clamp_box(x_min, y_min, x_max, y_max, width, height)
        if box is None:
            return None
        return Detection(box=box, score=float(results["scores"][best]))
