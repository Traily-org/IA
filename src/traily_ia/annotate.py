"""Draw an identification result on a copy of the photo (for local inspection)."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from traily_ia.result import IdentificationResult

GREEN, RED, ORANGE = (40, 200, 60), (230, 50, 50), (255, 160, 0)
TOP_ALTERNATIVES = 3


def _font_size(image: Image.Image) -> int:
    return max(18, image.width // 38)


def _text_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, int, int],
) -> None:
    """Text on a dark background so it stays readable on any photo."""
    left, top, right, bottom = draw.multiline_textbbox(xy, text, font=font)
    pad = 6
    draw.rectangle((left - pad, top - pad, right + pad, bottom + pad), fill=(0, 0, 0))
    draw.multiline_text(xy, text, font=font, fill=fill)


def annotate_image(
    image: Image.Image,
    result: IdentificationResult,
    *,
    truth: str | None = None,
) -> Image.Image:
    """Return a copy with the box, the verdict + confidence, and the top candidates.

    `truth`, when given (labelled test photos), is shown with a tick or cross and
    turns the box red when the pipeline answered something else.
    """
    canvas = image.convert("RGB")
    draw = ImageDraw.Draw(canvas)
    size = _font_size(canvas)
    font = ImageFont.load_default(size=size)
    margin = 10

    if result.abstained:
        verdict = f"ABSTAIN ({result.abstain_reason})"
        colour = ORANGE
    else:
        verdict = f"{result.species}  {result.confidence:.0%}"
        colour = GREEN
    if truth is not None and result.species != truth:
        colour = RED if not result.abstained else ORANGE

    box = result.bbox
    if box is not None:
        draw.rectangle(
            (box.x_min, box.y_min, box.x_max, box.y_max),
            outline=colour,
            width=max(4, canvas.width // 250),
        )
        label_y = box.y_min - size * 1.8 if box.y_min > size * 2 else box.y_min
        _text_box(draw, (box.x_min + 4, max(label_y, margin)), verdict, font, colour)
    else:
        _text_box(
            draw,
            (margin, canvas.height - size * 2.5),
            "no subject found",
            font,
            ORANGE,
        )

    lines = [verdict]
    lines += [
        f"{i}. {a.species}  {a.score:.0%}"
        for i, a in enumerate(result.alternatives[:TOP_ALTERNATIVES], start=1)
    ]
    if truth is not None:
        ranked = [a.species for a in result.alternatives]
        if result.species == truth:
            lines.append(f"truth: {truth}  OK")
        elif truth in ranked:
            rank = ranked.index(truth) + 1
            note = "top guess, but abstained" if rank == 1 else f"rank {rank}"
            lines.append(f"truth: {truth}  X ({note})")
        else:
            lines.append(f"truth: {truth}  X (not in candidate list)")
    _text_box(draw, (margin, margin), "\n".join(lines), font, (255, 255, 255))
    return canvas
