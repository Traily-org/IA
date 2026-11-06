"""Pipeline logic tested with fake stages — no model weights, no torch."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import pytest
from PIL import Image

from traily_ia import (
    BoundingBox,
    Detection,
    IdentificationPipeline,
    SpeciesScore,
    detect_and_classify,
)

BOX = BoundingBox(x_min=10, y_min=20, x_max=60, y_max=80)


class FakeDetector:
    def __init__(self, detection: Detection | None) -> None:
        self._detection = detection

    def detect(self, image: Image.Image) -> Detection | None:
        return self._detection


class FakeClassifier:
    def __init__(self, scores: list[SpeciesScore]) -> None:
        self._scores = scores
        self.crops: list[tuple[int, int]] = []

    def classify(
        self, crop: Image.Image, candidates: Sequence[str]
    ) -> list[SpeciesScore]:
        self.crops.append(crop.size)
        return self._scores


def make_pipeline(
    detection: Detection | None,
    scores: list[SpeciesScore],
    threshold: float = 0.5,
    crop_min_area_fraction: float = 0.0,
    min_similarity: float | None = None,
) -> tuple[IdentificationPipeline, FakeClassifier]:
    classifier = FakeClassifier(scores)
    pipeline = IdentificationPipeline(
        FakeDetector(detection),
        classifier,
        confidence_threshold=threshold,
        crop_min_area_fraction=crop_min_area_fraction,
        min_similarity=min_similarity,
    )
    return pipeline, classifier


def blank(width: int = 100, height: int = 120) -> Image.Image:
    return Image.new("RGB", (width, height), "green")


def test_confident_match_returns_species_and_box() -> None:
    pipeline, classifier = make_pipeline(
        Detection(BOX, 0.4),
        [SpeciesScore("Bellis perennis", 0.9), SpeciesScore("Urtica dioica", 0.1)],
    )

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert result.species == "Bellis perennis"
    assert result.confidence == 0.9
    assert result.bbox == BOX
    assert not result.abstained
    assert result.abstain_reason is None
    assert result.detection_score == 0.4
    assert (result.image_width, result.image_height) == (100, 120)
    assert [a.species for a in result.alternatives] == [
        "Bellis perennis",
        "Urtica dioica",
    ]
    assert classifier.crops == [(50, 60)]  # classifier sees only the crop


def test_low_confidence_abstains_instead_of_guessing() -> None:
    pipeline, _ = make_pipeline(
        Detection(BOX, 0.4),
        [SpeciesScore("Bellis perennis", 0.3), SpeciesScore("Urtica dioica", 0.2)],
    )

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert result.abstained
    assert result.species is None
    assert result.abstain_reason == "low_confidence"
    assert result.bbox == BOX
    assert result.alternatives[0].species == "Bellis perennis"


def test_confidence_exactly_at_threshold_is_accepted() -> None:
    pipeline, _ = make_pipeline(
        Detection(BOX, 0.4), [SpeciesScore("Bellis perennis", 0.5)], threshold=0.5
    )

    assert (
        pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"]).species
        == "Bellis perennis"
    )


def test_no_detection_abstains_without_classifying() -> None:
    pipeline, classifier = make_pipeline(None, [SpeciesScore("Bellis perennis", 1.0)])

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert result.abstained
    assert result.abstain_reason == "no_subject_detected"
    assert result.species is None
    assert result.bbox is None
    assert result.confidence == 0.0
    assert classifier.crops == []


def test_empty_candidate_list_is_rejected() -> None:
    pipeline, _ = make_pipeline(Detection(BOX, 0.4), [])

    with pytest.raises(ValueError, match="at least one species"):
        pipeline.identify(blank(), [])


def test_duplicate_candidate_names_are_scored_once() -> None:
    seen: list[list[str]] = []

    class RecordingClassifier:
        def classify(
            self, crop: Image.Image, candidates: Sequence[str]
        ) -> list[SpeciesScore]:
            seen.append(list(candidates))
            return [SpeciesScore("Quercus robur", 0.9)]

    pipeline = IdentificationPipeline(None, RecordingClassifier())
    pipeline.identify(
        Image.new("RGB", (40, 40)),
        ["Quercus robur", "Quercus robur", "Ilex aquifolium"],
    )
    assert seen == [["Quercus robur", "Ilex aquifolium"]]


def test_common_names_are_added_for_display_and_the_scientific_name_stays() -> None:
    scores = [SpeciesScore("Quercus robur", 0.9), SpeciesScore("Ilex aquifolium", 0.1)]
    pipeline = IdentificationPipeline(
        None, FakeClassifier(scores), common_names={"Quercus robur": "Chêne pédonculé"}
    )

    result = pipeline.identify(blank(), ["Quercus robur", "Ilex aquifolium"])

    assert result.species == "Quercus robur"
    assert result.common_name == "Chêne pédonculé"
    assert result.alternatives[0].common_name == "Chêne pédonculé"
    assert result.alternatives[1].common_name is None


def test_an_abstained_result_has_no_common_name() -> None:
    pipeline = IdentificationPipeline(
        None,
        FakeClassifier([SpeciesScore("Quercus robur", 0.3)]),
        common_names={"Quercus robur": "Chêne pédonculé"},
    )

    result = pipeline.identify(blank(), ["Quercus robur"])

    assert result.abstained and result.common_name is None


def test_a_single_candidate_never_gives_an_answer() -> None:
    pipeline = IdentificationPipeline(
        None, FakeClassifier([SpeciesScore("Quercus robur", 1.0)])
    )

    result = pipeline.identify(blank(), ["Quercus robur"])

    assert result.species is None
    assert result.abstained and result.abstain_reason == "low_confidence"
    assert result.confidence == 0.0
    assert result.alternatives[0].species == "Quercus robur"


def test_models_are_loaded_once_even_when_the_settings_change(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from traily_ia import bioclip_classifier, pipeline

    built: list[str | None] = []

    class CountingClassifier:
        def __init__(self, device: str | None = None) -> None:
            built.append(device)

        def classify(
            self, crop: Image.Image, candidates: Sequence[str]
        ) -> list[SpeciesScore]:
            return [SpeciesScore("a", 1.0)]

    monkeypatch.setattr(bioclip_classifier, "BioClipClassifier", CountingClassifier)
    pipeline._bioclip.cache_clear()

    pipeline.build_default_pipeline(confidence_threshold=0.5)
    pipeline.build_default_pipeline(confidence_threshold=0.9)
    pipeline.build_default_pipeline(confidence_threshold=0.5, min_similarity=0.7)

    assert built == [None]
    pipeline._bioclip.cache_clear()


def test_degenerate_box_still_yields_a_valid_crop() -> None:
    sliver = BoundingBox(x_min=10.2, y_min=20.2, x_max=10.4, y_max=20.4)
    pipeline, classifier = make_pipeline(
        Detection(sliver, 0.2), [SpeciesScore("Bellis perennis", 0.9)]
    )

    pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert classifier.crops[0][0] >= 1 and classifier.crops[0][1] >= 1


def test_detect_and_classify_reads_file_and_applies_exif_orientation(
    tmp_path: Path,
) -> None:
    path = tmp_path / "photo.jpg"
    img = Image.new("RGB", (200, 100), "green")
    exif = Image.Exif()
    exif[0x0112] = 6  # rotate 90° clockwise when displayed
    img.save(path, exif=exif)
    pipeline, _ = make_pipeline(
        Detection(BOX, 0.4), [SpeciesScore("Bellis perennis", 0.9)]
    )

    result = detect_and_classify(
        path, ["Bellis perennis", "Urtica dioica"], pipeline=pipeline
    )

    assert (result.image_width, result.image_height) == (100, 200)
    assert result.species == "Bellis perennis"


SCORES = [SpeciesScore("Bellis perennis", 0.9), SpeciesScore("Urtica dioica", 0.1)]


def test_small_box_falls_back_to_the_whole_photo_but_keeps_the_box() -> None:
    # BOX covers 50x60 of a 100x120 photo = 25 %
    pipeline, classifier = make_pipeline(
        Detection(BOX, 0.4), SCORES, crop_min_area_fraction=0.4
    )

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert classifier.crops == [(100, 120)]
    assert not result.used_crop
    assert result.bbox == BOX
    assert result.species == "Bellis perennis"


def test_large_enough_box_is_cropped() -> None:
    pipeline, classifier = make_pipeline(
        Detection(BOX, 0.4), SCORES, crop_min_area_fraction=0.2
    )

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert classifier.crops == [(50, 60)]
    assert result.used_crop


def test_no_subject_uses_the_whole_photo_when_a_fraction_is_set() -> None:
    pipeline, classifier = make_pipeline(None, SCORES, crop_min_area_fraction=0.2)

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert classifier.crops == [(100, 120)]
    assert result.bbox is None and not result.used_crop
    assert result.species == "Bellis perennis" and result.abstain_reason is None


def test_default_classifies_the_whole_photo_and_still_returns_the_box() -> None:
    classifier = FakeClassifier(SCORES)
    pipeline = IdentificationPipeline(FakeDetector(Detection(BOX, 0.4)), classifier)

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert classifier.crops == [(100, 120)]
    assert result.bbox == BOX and not result.used_crop
    assert result.species == "Bellis perennis"


def test_default_does_not_abstain_when_no_subject_is_found() -> None:
    classifier = FakeClassifier(SCORES)
    pipeline = IdentificationPipeline(FakeDetector(None), classifier)

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert result.bbox is None and result.species == "Bellis perennis"
    assert result.abstain_reason is None and classifier.crops == [(100, 120)]


def test_zero_fraction_keeps_the_old_always_crop_behaviour() -> None:
    pipeline, classifier = make_pipeline(Detection(BOX, 0.4), SCORES)

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert classifier.crops == [(50, 60)] and result.used_crop


def sim_scores(similarity: float | None) -> list[SpeciesScore]:
    return [
        SpeciesScore("Bellis perennis", 0.95, similarity),
        SpeciesScore("Urtica dioica", 0.05, 0.1),
    ]


def test_low_similarity_means_none_of_these_even_when_softmax_is_confident() -> None:
    pipeline, _ = make_pipeline(
        Detection(BOX, 0.4), sim_scores(0.2), min_similarity=0.29
    )

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert result.abstained and result.species is None
    assert result.abstain_reason == "unknown_species"
    assert result.confidence == 0.95  # the softmax value is still reported


def test_similarity_above_the_minimum_is_answered() -> None:
    pipeline, _ = make_pipeline(
        Detection(BOX, 0.4), sim_scores(0.35), min_similarity=0.29
    )

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert result.species == "Bellis perennis" and result.abstain_reason is None


def test_similarity_rule_is_off_by_default_and_ignores_missing_similarity() -> None:
    default, _ = make_pipeline(Detection(BOX, 0.4), sim_scores(0.05))
    no_value, _ = make_pipeline(
        Detection(BOX, 0.4), sim_scores(None), min_similarity=0.29
    )

    assert default.identify(blank(), ["a", "b"]).species == "Bellis perennis"
    assert no_value.identify(blank(), ["a", "b"]).species == "Bellis perennis"


class SizeAwareClassifier:
    """Confidence depends on whether it sees the whole photo or a crop."""

    def __init__(self, whole: float, crop: float) -> None:
        self._whole, self._crop = whole, crop
        self.sizes: list[tuple[int, int]] = []

    def classify(
        self, crop: Image.Image, candidates: Sequence[str]
    ) -> list[SpeciesScore]:
        self.sizes.append(crop.size)
        score = self._whole if crop.size == (100, 120) else self._crop
        return [SpeciesScore("Bellis perennis", score)]


class CountingDetector(FakeDetector):
    def __init__(self, detection: Detection | None) -> None:
        super().__init__(detection)
        self.calls = 0

    def detect(self, image: Image.Image) -> Detection | None:
        self.calls += 1
        return super().detect(image)


def retry_pipeline(
    whole: float, crop: float, *, always_detect: bool = True
) -> tuple[IdentificationPipeline, SizeAwareClassifier, CountingDetector]:
    classifier = SizeAwareClassifier(whole, crop)
    detector = CountingDetector(Detection(BOX, 0.4))
    pipeline = IdentificationPipeline(
        detector,
        classifier,
        crop_retry_below=0.7,
        always_detect=always_detect,
    )
    return pipeline, classifier, detector


def test_confident_whole_photo_is_not_retried() -> None:
    pipeline, classifier, _ = retry_pipeline(whole=0.9, crop=0.95)

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert classifier.sizes == [(100, 120)]
    assert result.confidence == 0.9 and not result.used_crop
    assert result.bbox == BOX


def test_unsure_whole_photo_retries_with_the_crop_and_keeps_the_better() -> None:
    pipeline, classifier, _ = retry_pipeline(whole=0.4, crop=0.8)

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert classifier.sizes == [(100, 120), (50, 60)]
    assert result.confidence == 0.8 and result.used_crop


def test_crop_is_dropped_when_it_is_less_confident() -> None:
    pipeline, _, _ = retry_pipeline(whole=0.5, crop=0.3)

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert result.confidence == 0.5 and not result.used_crop


def test_lazy_detector_only_runs_when_a_retry_needs_it() -> None:
    confident, _, detector = retry_pipeline(0.9, 0.95, always_detect=False)
    result = confident.identify(blank(), ["Bellis perennis", "Urtica dioica"])
    assert detector.calls == 0 and result.bbox is None

    unsure, _, detector = retry_pipeline(0.4, 0.8, always_detect=False)
    result = unsure.identify(blank(), ["Bellis perennis", "Urtica dioica"])
    assert detector.calls == 1 and result.bbox == BOX and result.used_crop


def test_incompatible_crop_settings_are_rejected() -> None:
    with pytest.raises(ValueError):
        IdentificationPipeline(
            FakeDetector(None),
            FakeClassifier([]),
            crop_min_area_fraction=0.4,
            crop_retry_below=0.7,
        )
    with pytest.raises(ValueError):
        IdentificationPipeline(
            FakeDetector(None), FakeClassifier([]), always_detect=False
        )


def test_without_a_detector_the_classifier_alone_sees_the_whole_photo() -> None:
    classifier = SizeAwareClassifier(0.4, 0.9)
    pipeline = IdentificationPipeline(None, classifier)

    result = pipeline.identify(blank(), ["Bellis perennis", "Urtica dioica"])

    assert result.bbox is None and not result.used_crop
    assert result.detection_score == 0.0
    assert result.confidence == 0.4 and result.abstained
    assert pipeline.detector is None


def test_a_crop_setting_needs_a_detector() -> None:
    with pytest.raises(ValueError, match="detector"):
        IdentificationPipeline(None, FakeClassifier([]), crop_retry_below=0.7)
    with pytest.raises(ValueError, match="detector"):
        IdentificationPipeline(None, FakeClassifier([]), crop_min_area_fraction=0.0)
