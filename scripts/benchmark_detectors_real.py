#!/usr/bin/env python
"""Benchmark detectors on REAL unseen photos, without hand-drawn boxes.

    python scripts/benchmark_detectors_real.py [--photos 600] [--only NAME ...]

The earlier benchmark (benchmark_detectors.py) used simulated photos. Here the
photos are real (same unseen set and trail lists as build_examples.py) and the
species label stands in for a box: if the detector's box captures the plant, the
crop's species answer is as good as the whole photo's. Per detector and prompt set:

  - how often a box is found, and how often it is tiny (5% of the photo or less) or
    nearly the whole frame (90% or more);
  - crop-only top-1 against the whole photo's top-1 on the same photos;
  - the production retry (crop classified when the whole photo is under the
    threshold, the more confident answer kept): photos rescued, photos broken and
    confident wrong answers, over ALL photos, not only the unsure ones.

Prompt sets: "default" (the detector's own three prompts), "plant" ("a plant" only)
and, for Grounding DINO tiny, "organ" (a prompt that names the photo's organ).
Writes docs/eval/<date>-detector-real-benchmark.json.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np  # noqa: E402

from traily_ia.bioclip_classifier import BioClipClassifier  # noqa: E402
from traily_ia.grounding_dino_detector import GroundingDinoDetector  # noqa: E402
from traily_ia.owlv2_detector import Owlv2Detector  # noqa: E402
from traily_ia.pipeline import (  # noqa: E402
    DEFAULT_CONFIDENCE_THRESHOLD,
    _crop,
    load_image,
)
from unseen_photos import (  # noqa: E402
    Photo,
    load_photos,
    load_trails,
    softmax_scores,
)

ORGAN_PROMPT = {
    "bark": "tree bark",
    "leaf": "a leaf",
    "flower": "a flower",
    "fruit": "a fruit",
    "habit": "a plant",
}


def make(name: str) -> Any:
    if name == "grounding-dino-tiny":
        return GroundingDinoDetector(model_id="IDEA-Research/grounding-dino-tiny")
    if name == "grounding-dino-base":
        return GroundingDinoDetector(model_id="IDEA-Research/grounding-dino-base")
    if name == "owlv2-base":
        return Owlv2Detector()
    if name == "owlv2-large":
        return Owlv2Detector(model_id="google/owlv2-large-patch14-ensemble")
    raise SystemExit(f"unknown detector {name}")


def set_prompts(det: Any, prompts: tuple[str, ...]) -> None:
    """Change the detector's text prompts in place (avoids reloading the weights)."""
    if isinstance(det, GroundingDinoDetector):
        det._text = ". ".join(prompts) + "."
    else:
        det._prompts = [f"a photo of {p}" for p in prompts]


def get_prompts(det: Any) -> Any:
    return det._text if isinstance(det, GroundingDinoDetector) else list(det._prompts)


def restore_prompts(det: Any, saved: Any) -> None:
    if isinstance(det, GroundingDinoDetector):
        det._text = saved
    else:
        det._prompts = list(saved)


CONFIGS = [
    ("grounding-dino-tiny", "default"),
    ("grounding-dino-tiny", "plant"),
    ("grounding-dino-tiny", "organ"),
    ("grounding-dino-base", "default"),
    ("grounding-dino-base", "plant"),
    ("owlv2-base", "default"),
    ("owlv2-base", "plant"),
    ("owlv2-large", "default"),
    ("owlv2-large", "plant"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--photos", type=int, default=600)
    parser.add_argument("--only", nargs="+", help="detector names to run")
    args = parser.parse_args()
    threshold = DEFAULT_CONFIDENCE_THRESHOLD

    trails = load_trails()
    first_trail: dict[str, str] = {}
    for t, names in trails.items():
        for n in names:
            first_trail.setdefault(n, t)
    pool = [p for p in load_photos() if p.species in first_trail]
    random.Random(0).shuffle(pool)
    photos: list[Photo] = pool[: args.photos]

    clf = BioClipClassifier()
    text = {t: clf.embed_species(names) for t, names in trails.items()}

    def top(image: Any, p: Photo) -> tuple[bool, float]:
        t = first_trail[p.species]
        best = softmax_scores(clf, text[t], trails[t], clf.embed_image(image))[0]
        return best[0] == p.species, best[1]

    whole = [top(load_image(p.path), p) for p in photos]
    print(
        f"{len(photos)} photos, whole-photo top-1 "
        f"{np.mean([w[0] for w in whole]):.3f}",
        flush=True,
    )

    out: list[dict[str, Any]] = []
    loaded: dict[str, Any] = {}
    saved: dict[str, Any] = {}
    for name, prompt_set in CONFIGS:
        if args.only and name not in args.only:
            continue
        if name not in loaded:
            loaded.clear()
            loaded[name] = make(name)
            saved[name] = get_prompts(loaded[name])
        det = loaded[name]
        restore_prompts(det, saved[name])
        print("==", name, prompt_set, flush=True)
        found = tiny = full = 0
        crop_right = whole_right_found = 0
        rescued = hurt = answered_wrong = whole_answered_wrong = 0
        retries = 0
        ms: list[float] = []
        for p, (w_right, w_conf) in zip(photos, whole, strict=True):
            image = load_image(p.path)
            if prompt_set == "plant":
                set_prompts(det, ("a plant",))
            elif prompt_set == "organ":
                set_prompts(det, (ORGAN_PROMPT.get(p.organ, "a plant"),))
            start = time.perf_counter()
            d = det.detect(image)
            ms.append((time.perf_counter() - start) * 1000)
            if w_conf >= threshold and not w_right:
                whole_answered_wrong += 1
            c_right = c_conf = None
            if d is not None:
                found += 1
                frac = (
                    (d.box.x_max - d.box.x_min)
                    * (d.box.y_max - d.box.y_min)
                    / (image.width * image.height)
                )
                tiny += frac <= 0.05
                full += frac >= 0.90
                c_right, c_conf = top(_crop(image, d.box), p)
                crop_right += c_right
                whole_right_found += w_right
            # production policy: retry only under the threshold, keep the more confident
            final_right, final_conf = w_right, w_conf
            if w_conf < threshold and c_conf is not None:
                retries += 1
                if c_conf > w_conf:
                    final_right, final_conf = bool(c_right), c_conf
            rescued += final_right and not w_right
            hurt += w_right and not final_right
            answered_wrong += final_conf >= threshold and not final_right
        n = len(photos)
        out.append(
            {
                "detector": name,
                "prompts": prompt_set,
                "photos": n,
                "found_rate": found / n,
                "tiny_box_rate": tiny / max(1, found),
                "whole_frame_box_rate": full / max(1, found),
                "crop_only_top1": crop_right / max(1, found),
                "whole_top1_same_photos": whole_right_found / max(1, found),
                "retries": retries,
                "rescued": int(rescued),
                "hurt": int(hurt),
                "confident_wrong_whole_only": whole_answered_wrong,
                "confident_wrong_with_retry": int(answered_wrong),
                "median_ms": float(np.median(ms)),
            }
        )
        print(json.dumps(out[-1]), flush=True)
        path = (
            Path("docs/eval")
            / f"{date.today().isoformat()}-detector-real-benchmark.json"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "date": date.today().isoformat(),
                    "photos": n,
                    "whole_top1": float(np.mean([w[0] for w in whole])),
                    "threshold": threshold,
                    "rows": out,
                },
                indent=1,
            ),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
