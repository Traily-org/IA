from __future__ import annotations

from PIL import Image, ImageChops

from traily_ia import BoundingBox, IdentificationResult, SpeciesScore
from traily_ia.annotate import annotate_image

BOX = BoundingBox(50, 60, 250, 260)


def result(
    species: str | None, confidence: float, *, box: BoundingBox | None = BOX
) -> IdentificationResult:
    return IdentificationResult(
        species=species,
        confidence=confidence,
        bbox=box,
        abstained=species is None,
        abstain_reason=None if species else "low_confidence",
        detection_score=0.3,
        image_width=400,
        image_height=300,
        alternatives=(
            SpeciesScore("Bellis perennis", confidence),
            SpeciesScore("Urtica dioica", 1 - confidence),
        ),
    )


def photo() -> Image.Image:
    return Image.new("RGB", (400, 300), (30, 120, 40))


def changed(out: Image.Image) -> bool:
    return ImageChops.difference(out, photo()).getbbox() is not None


def test_annotation_keeps_the_size_and_does_not_touch_the_original() -> None:
    original = photo()

    out = annotate_image(original, result("Bellis perennis", 0.9))

    assert out.size == original.size
    assert changed(out)
    assert ImageChops.difference(original, photo()).getbbox() is None


def test_abstention_and_missing_box_are_drawn_too() -> None:
    assert changed(annotate_image(photo(), result(None, 0.3)))
    assert changed(annotate_image(photo(), result(None, 0.0, box=None)))


def test_wrong_answer_turns_the_box_red_and_correct_one_green() -> None:
    right = annotate_image(
        photo(), result("Bellis perennis", 0.9), truth="Bellis perennis"
    )
    wrong = annotate_image(
        photo(), result("Bellis perennis", 0.9), truth="Urtica dioica"
    )

    # The box outline is drawn on its left edge, away from any text.
    assert right.getpixel((51, 160)) == (40, 200, 60)
    assert wrong.getpixel((51, 160)) == (230, 50, 50)
