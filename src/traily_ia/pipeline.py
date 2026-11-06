"""Species identification: classify the whole photo; an optional detector adds a crop.

This module is the whole core of `/identify` and knows nothing about HTTP. The
future FastAPI layer should only decode the upload, call `detect_and_classify`
(or `IdentificationPipeline.identify`) and map the result to a response model.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageOps

from traily_ia.interfaces import Classifier, Detector
from traily_ia.result import (
    AbstainReason,
    BoundingBox,
    IdentificationResult,
)

# Temporary value until real hiker photos allow a calibration: on 1,233 unseen
# photos, 0.7 answers 97.1% of them and 99.0% of the answers are right.
# Scores are a softmax over the candidate list, so this is not comparable across
# lists of different sizes — measure it with scripts/measure_thresholds.py.
DEFAULT_CONFIDENCE_THRESHOLD = 0.7
# Whole-photo confidence under which the optional detector's crop is classified too.
# Same value as the abstain threshold: one number to explain.
DEFAULT_CROP_RETRY_BELOW = 0.7


def load_image(image_path: Path | str) -> Image.Image:
    """Open an image as RGB, honouring EXIF orientation (phone photos)."""
    with Image.open(image_path) as img:
        return ImageOps.exif_transpose(img).convert("RGB")


def _crop(image: Image.Image, box: BoundingBox) -> Image.Image:
    left, top = int(box.x_min), int(box.y_min)
    right = max(int(box.x_max + 0.5), left + 1)
    bottom = max(int(box.y_max + 0.5), top + 1)
    return image.crop((left, top, right, bottom))


class IdentificationPipeline:
    """Holds a detector and a classifier; models are loaded once and reused."""

    def __init__(
        self,
        detector: Detector | None,
        classifier: Classifier,
        *,
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
        crop_min_area_fraction: float | None = None,
        min_similarity: float | None = None,
        crop_retry_below: float | None = None,
        always_detect: bool = True,
        common_names: Mapping[str, str] | None = None,
    ) -> None:
        """`detector` is None in the default setup: the classifier alone looks at the
        whole photo (ADR 0001). Without a detector there is no box and no crop, so
        `crop_min_area_fraction` and `crop_retry_below` must stay None.

        `crop_retry_below`: when the whole photo's confidence is under this value,
        also classify the detector's crop and keep the more confident of the two. On
        200 unseen photos with simulated mess this matched "always both" at a fraction
        of the detector calls and rescued tiny subjects (49% -> 66-74% top-1 at
        25% of the width) but not on real photos (ADR 0001). None (default) never
        retries.
        `always_detect`: run the detector on every photo so the box is always
        returned. False runs it only when a retry needs it (the box is then None for
        confident photos); it cannot be combined with `crop_min_area_fraction`.

        `common_names`: scientific name -> French common name, copied onto the result
        and the alternatives for display; the scientific name stays the key.

        `min_similarity`: abstain ("unknown_species") when the best match's raw
        cosine similarity is below it — the "none of these" rule. On 130 labelled
        photos with BioCLIP 2 a value around 0.71 kept 95% of the correct answers
        while cutting the answers given for species missing from the list from 46%
        (softmax rule at 0.5) to 1%; the scale is model-specific (about 0.29 with
        BioCLIP 1). None (default) disables it.

        `crop_min_area_fraction` decides what the classifier sees:

        None (default) — always the whole photo. The detector only supplies the
        bounding box returned with the result (None if no subject is found, which
        does not stop the identification).
        0.0 — always the detector's crop; no subject found = abstain.
        t > 0 — the crop only when its box covers at least a fraction t of the
        photo, otherwise the whole photo.

        Whole photo is the default because on labelled photos classifying the crop
        was far worse (tiny boxes): see docs/eval/ and ADR 0001.
        """
        self._common_names: Mapping[str, str] = common_names or {}
        self._detector = detector
        self._classifier = classifier
        self._threshold = confidence_threshold
        self._crop_min_area_fraction = crop_min_area_fraction
        self._min_similarity = min_similarity
        if detector is None and (
            crop_min_area_fraction is not None or crop_retry_below is not None
        ):
            raise ValueError("a crop needs a detector")
        if crop_min_area_fraction is not None and crop_retry_below is not None:
            raise ValueError("use crop_min_area_fraction or crop_retry_below, not both")
        if not always_detect and (
            crop_min_area_fraction is not None or crop_retry_below is None
        ):
            raise ValueError("always_detect=False needs crop_retry_below alone")
        self._crop_retry_below = crop_retry_below
        self._always_detect = always_detect and detector is not None

    @property
    def detector(self) -> Detector | None:
        return self._detector

    @property
    def classifier(self) -> Classifier:
        return self._classifier

    def identify(
        self,
        image: Image.Image,
        candidates: Sequence[str],
    ) -> IdentificationResult:
        # A name listed twice would split its probability and cause a false abstain.
        candidates = list(dict.fromkeys(candidates))
        if not candidates:
            raise ValueError("candidates must contain at least one species name")

        width, height = image.size
        detector = self._detector
        detection = (
            detector.detect(image)
            if detector is not None and self._always_detect
            else None
        )
        fraction = self._crop_min_area_fraction
        if detection is None and fraction is not None and fraction <= 0:
            return IdentificationResult(
                species=None,
                confidence=0.0,
                bbox=None,
                abstained=True,
                abstain_reason="no_subject_detected",
                detection_score=0.0,
                image_width=width,
                image_height=height,
            )

        use_crop = (
            fraction is not None
            and detection is not None
            and detection.box.width * detection.box.height >= fraction * width * height
        )
        region = _crop(image, detection.box) if use_crop and detection else image
        scores = self._classifier.classify(region, candidates)
        if len(candidates) == 1:
            # A softmax over one name is always 1.0: the confidence is undefined, so
            # never answer (CLAUDE.md: never guess).
            return IdentificationResult(
                species=None,
                confidence=0.0,
                bbox=detection.box if detection else None,
                abstained=True,
                abstain_reason="low_confidence",
                detection_score=detection.score if detection else 0.0,
                image_width=width,
                image_height=height,
                alternatives=tuple(scores),
                used_crop=use_crop,
            )
        retry = self._crop_retry_below
        if retry is not None and scores[0].score < retry:
            if detector is not None and detection is None and not self._always_detect:
                detection = detector.detect(image)
            if detection is not None:
                crop_scores = self._classifier.classify(
                    _crop(image, detection.box), candidates
                )
                if crop_scores[0].score > scores[0].score:
                    scores, use_crop = crop_scores, True
        if self._common_names:
            scores = [
                replace(s, common_name=self._common_names.get(s.species))
                for s in scores
            ]
        best = scores[0]
        unknown = (
            self._min_similarity is not None
            and best.similarity is not None
            and best.similarity < self._min_similarity
        )
        abstained = unknown or best.score < self._threshold
        reason: AbstainReason | None = None
        if abstained:
            reason = "unknown_species" if unknown else "low_confidence"
        return IdentificationResult(
            species=None if abstained else best.species,
            confidence=best.score,
            bbox=detection.box if detection else None,
            abstained=abstained,
            abstain_reason=reason,
            detection_score=detection.score if detection else 0.0,
            image_width=width,
            image_height=height,
            alternatives=tuple(scores),
            used_crop=use_crop,
            common_name=None if abstained else best.common_name,
        )


@lru_cache(maxsize=2)
def _grounding_dino(device: str | None) -> Detector:
    from traily_ia.grounding_dino_detector import GroundingDinoDetector

    return GroundingDinoDetector(device=device)


@lru_cache(maxsize=2)
def _bioclip(device: str | None) -> Classifier:
    from traily_ia.bioclip_classifier import BioClipClassifier

    return BioClipClassifier(device=device)


def build_default_pipeline(
    *,
    device: str | None = None,
    confidence_threshold: float,
    crop_min_area_fraction: float | None = None,
    min_similarity: float | None = None,
    crop_retry_below: float | None = DEFAULT_CROP_RETRY_BELOW,
    always_detect: bool = False,
    use_detector: bool = False,
) -> IdentificationPipeline:
    """Build the pipeline with the current default models (loaded lazily).

    By default there is no detector: BioCLIP 2 classifies the whole photo, nothing
    else (on 1,443 real measurements the crop retry rescued 4 photos and broke 6).
    `use_detector=True` adds Grounding DINO tiny, which then runs only when the whole
    photo's confidence is under `crop_retry_below`, or on every photo
    with `always_detect`. `crop_min_area_fraction` also turns the detector on.

    When a detector is wanted, Grounding DINO tiny is the one used (ADR 0001 update,
    2026-10-30 benchmark); OWLv2 stays available as `Owlv2Detector`.
    The models are loaded once per device and reused (`_bioclip`, `_grounding_dino`), so
    building a pipeline again with other thresholds is cheap. Imports are local so
    importing this module never pulls in torch.
    """
    if crop_min_area_fraction is not None:
        use_detector = True
        crop_retry_below = None
    if not use_detector:
        crop_retry_below = None
    if crop_retry_below is None:
        always_detect = True

    return IdentificationPipeline(
        _grounding_dino(device) if use_detector else None,
        _bioclip(device),
        confidence_threshold=confidence_threshold,
        crop_min_area_fraction=crop_min_area_fraction,
        min_similarity=min_similarity,
        crop_retry_below=crop_retry_below,
        always_detect=always_detect,
    )


def detect_and_classify(
    image_path: Path | str,
    candidates: Sequence[str],
    *,
    pipeline: IdentificationPipeline | None = None,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
    crop_min_area_fraction: float | None = None,
    min_similarity: float | None = None,
    device: str | None = None,
    crop_retry_below: float | None = DEFAULT_CROP_RETRY_BELOW,
    always_detect: bool = False,
    use_detector: bool = False,
) -> IdentificationResult:
    """Identify the main subject of one photo among `candidates`.

    Pass a prebuilt `pipeline` to use specific (or fake, in tests) stages;
    otherwise the default models are built once and cached for later calls.
    """
    if pipeline is None:
        pipeline = build_default_pipeline(
            device=device,
            confidence_threshold=confidence_threshold,
            crop_min_area_fraction=crop_min_area_fraction,
            min_similarity=min_similarity,
            crop_retry_below=crop_retry_below,
            always_detect=always_detect,
            use_detector=use_detector,
        )
    return pipeline.identify(load_image(image_path), candidates)
