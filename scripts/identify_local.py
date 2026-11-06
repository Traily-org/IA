#!/usr/bin/env python
"""Run the identification pipeline over a folder of test images (no HTTP).

    python scripts/identify_local.py data/test_images \
        --species-file examples/species_sample.txt --annotate out/

Prints one line per image (species, confidence, box, seconds). Models are
loaded before the first image so the per-image time is inference only.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

from traily_ia import DEFAULT_CONFIDENCE_THRESHOLD, IdentificationResult
from traily_ia.annotate import annotate_image
from traily_ia.pipeline import build_default_pipeline, detect_and_classify, load_image
from traily_ia.species import load_species_file

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def find_images(folder: Path) -> list[Path]:
    return sorted(
        p
        for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )


def format_line(name: str, result: IdentificationResult, seconds: float) -> str:
    if result.abstained:
        verdict = f"ABSTAIN ({result.abstain_reason})"
        if result.alternatives:
            top = result.alternatives[0]
            verdict += f" best guess: {top.species}"
    else:
        verdict = str(result.species)
    b = result.bbox
    coords = (
        ""
        if b is None
        else f"({b.x_min:.0f},{b.y_min:.0f},{b.x_max:.0f},{b.y_max:.0f})"
    )
    box = f"box={coords}" if coords else "no box"
    return f"{name:<30} {verdict:<50} conf={result.confidence:.2f} {box} {seconds:.2f}s"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("folder", type=Path, help="folder of test images")
    parser.add_argument(
        "--species-file",
        type=Path,
        required=True,
        help="candidate species, one name per line ('#' comments allowed)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_CONFIDENCE_THRESHOLD,
        help="below this confidence the pipeline abstains (default: %(default)s)",
    )
    parser.add_argument(
        "--crop-retry-below",
        type=float,
        default=0.7,
        help="when the whole photo's confidence is under this value, also classify "
        "the detector's crop and keep the more confident (default 0.7; ignored "
        "when --crop-min-fraction is set)",
    )
    parser.add_argument(
        "--detector",
        action="store_true",
        help="turn the detector on: it then runs only on unsure photos and its crop "
        "is classified too (off by default: on real photos it did more harm than "
        "good, see ADR 0001)",
    )
    parser.add_argument(
        "--box-on-every-photo",
        action="store_true",
        help="run the detector on every photo so each result has a box (about "
        "4 s slower on CPU); implies --detector",
    )
    parser.add_argument(
        "--crop-min-fraction",
        type=float,
        default=None,
        help="default: classify the whole photo (the detector only supplies the "
        "box). 0 = always classify the detector's crop; t > 0 = the crop only "
        "when its box covers at least that fraction of the photo (e.g. 0.4)",
    )
    parser.add_argument(
        "--min-similarity",
        type=float,
        default=None,
        help="'none of these' rule: abstain when the best match's raw cosine "
        "similarity is below this (about 0.71 for BioCLIP 2, 0.29 for BioCLIP 1); "
        "off by default",
    )
    parser.add_argument("--device", default=None, help="cpu / cuda (default: auto)")
    parser.add_argument("--annotate", type=Path, help="write images with boxes here")
    parser.add_argument("--json", action="store_true", help="print JSON, not a table")
    args = parser.parse_args()

    if not args.folder.is_dir():
        parser.error(f"not a folder: {args.folder}")
    candidates = load_species_file(args.species_file)
    if not candidates:
        parser.error(f"no species found in {args.species_file}")
    images = find_images(args.folder)
    if not images:
        parser.error(
            f"no images ({', '.join(sorted(IMAGE_SUFFIXES))}) in {args.folder}"
        )

    print(f"Loading models (device={args.device or 'auto'})...", file=sys.stderr)
    pipeline = build_default_pipeline(
        device=args.device,
        confidence_threshold=args.threshold,
        crop_min_area_fraction=args.crop_min_fraction,
        min_similarity=args.min_similarity,
        crop_retry_below=(
            None if args.crop_min_fraction is not None else args.crop_retry_below
        ),
        always_detect=args.box_on_every_photo,
        use_detector=(
            args.detector
            or args.box_on_every_photo
            or args.crop_min_fraction is not None
        ),
    )

    records = []
    for path in images:
        start = time.perf_counter()
        result = detect_and_classify(path, candidates, pipeline=pipeline)
        seconds = time.perf_counter() - start
        if args.annotate:
            args.annotate.mkdir(parents=True, exist_ok=True)
            annotate_image(load_image(path), result).save(
                args.annotate / f"{path.stem}.annotated.jpg"
            )
        if args.json:
            records.append({"image": path.name, "seconds": seconds, **asdict(result)})
        else:
            print(format_line(path.name, result, seconds))

    if args.json:
        print(json.dumps(records, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
