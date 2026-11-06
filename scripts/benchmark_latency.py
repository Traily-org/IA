#!/usr/bin/env python
"""Time each stage of the pipeline per photo, on GPU and on CPU.

    python scripts/benchmark_latency.py data/web_test_images \
        --species-file data/species_lists/catalog.txt

Stages: decode (open + EXIF rotate), detector (Grounding DINO tiny; needed for the box and for the crop retry),
classifier (BioCLIP on the whole photo). Writes docs/results/latency.json as rows
{device, stage, n, mean_ms, p50_ms, p95_ms}. The target is p95 < 5 s per request
(Story 2.3 / 8.2). One untimed warm-up photo per device.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import torch

from traily_ia.bioclip_classifier import DEFAULT_MODEL_ID, BioClipClassifier
from traily_ia.grounding_dino_detector import GroundingDinoDetector
from traily_ia.pipeline import load_image
from traily_ia.species import load_species_file

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def timed(fn):
    start = time.perf_counter()
    result = fn()
    return result, (time.perf_counter() - start) * 1000


def sync(device: str) -> None:
    if device == "cuda":
        torch.cuda.synchronize()


def run_device(
    device: str, photos: list[Path], candidates: list[str], model_id: str
) -> list[dict]:
    detector = GroundingDinoDetector(device=device)
    classifier = BioClipClassifier(device=device, model_id=model_id)
    classifier.classify(load_image(photos[0]), candidates)  # warm-up (text cache too)
    detector.detect(load_image(photos[0]))
    sync(device)

    times: dict[str, list[float]] = {
        "decode": [],
        "detector": [],
        "classifier": [],
        "total": [],
    }
    for path in photos:
        image, t_decode = timed(lambda p=path: load_image(p))
        _, t_det = timed(lambda im=image: (detector.detect(im), sync(device)))
        _, t_clf = timed(
            lambda im=image: (classifier.classify(im, candidates), sync(device))
        )
        for stage, value in (
            ("decode", t_decode),
            ("detector", t_det),
            ("classifier", t_clf),
            ("total", t_decode + t_det + t_clf),
        ):
            times[stage].append(value)
    # "without detector": what the request costs if the box is not needed
    times["total_no_detector"] = [
        d + c for d, c in zip(times["decode"], times["classifier"], strict=True)
    ]
    return [
        {
            "device": device,
            "stage": stage,
            "n": len(v),
            "mean_ms": round(float(np.mean(v)), 1),
            "p50_ms": round(float(np.percentile(v, 50)), 1),
            "p95_ms": round(float(np.percentile(v, 95)), 1),
        }
        for stage, v in times.items()
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("folder", type=Path)
    parser.add_argument("--species-file", type=Path, required=True)
    parser.add_argument(
        "--cpu-photos", type=int, default=30, help="CPU is slow: fewer photos"
    )
    parser.add_argument("--out", type=Path, default=Path("docs/results/latency.json"))
    parser.add_argument(
        "--model", default=DEFAULT_MODEL_ID, help="open_clip id of the classifier"
    )
    parser.add_argument(
        "--threads", type=int, help="CPU threads (e.g. 2 to mimic a small server)"
    )
    args = parser.parse_args()
    if args.threads:
        torch.set_num_threads(args.threads)

    photos = sorted(
        p for p in args.folder.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES
    )
    candidates = load_species_file(args.species_file)
    rows: list[dict] = []
    if torch.cuda.is_available():
        rows += run_device("cuda", photos, candidates, args.model)
    rows += run_device("cpu", photos[: args.cpu_photos], candidates, args.model)

    payload = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "model": args.model,
        "candidates": len(candidates),
        "cpu_threads": torch.get_num_threads(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "rows": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    for r in rows:
        print(
            f"{r['device']:<5} {r['stage']:<18} n={r['n']:<4} p50={r['p50_ms']:>8} ms  p95={r['p95_ms']:>8} ms"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
