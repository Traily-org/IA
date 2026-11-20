"""The box clamp is pure geometry; the model itself is not loaded here."""

from __future__ import annotations

from traily_ia.owlv2_detector import clamp_box
from traily_ia.result import BoundingBox


def test_box_inside_image_is_unchanged() -> None:
    assert clamp_box(10, 20, 60, 80, 100, 120) == BoundingBox(10, 20, 60, 80)


def test_box_in_padding_area_is_clamped_to_image() -> None:
    # OWLv2 predicts in a padded square; a 200x100 image has padding below y=100.
    box = clamp_box(50, 60, 150, 190, 200, 100)

    assert box == BoundingBox(50, 60, 150, 100)


def test_box_entirely_in_padding_is_dropped() -> None:
    assert clamp_box(10, 110, 50, 190, 200, 100) is None


def test_grounding_dino_picks_the_highest_scoring_box_and_clamps_it() -> None:
    import torch

    from traily_ia.grounding_dino_detector import pick_best_detection

    scores = torch.tensor([0.2, 0.6, 0.4])
    boxes = torch.tensor([[0, 0, 5, 5], [-10, 10, 50, 300], [1, 1, 2, 2]])

    detection = pick_best_detection(scores, boxes, width=100, height=200)

    assert detection is not None
    assert abs(detection.score - 0.6) < 1e-6
    assert (detection.box.x_min, detection.box.y_max) == (0.0, 200.0)


def test_grounding_dino_returns_none_without_boxes_or_with_an_outside_box() -> None:
    import torch

    from traily_ia.grounding_dino_detector import pick_best_detection

    empty = torch.empty(0), torch.empty(0, 4)
    assert pick_best_detection(*empty, width=10, height=10) is None
    outside = torch.tensor([0.9]), torch.tensor([[20.0, 20.0, 30.0, 30.0]])
    assert pick_best_detection(*outside, width=10, height=10) is None
