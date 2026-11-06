#!/usr/bin/env python
"""Compare zero-shot image-text models on the labelled test photos.

    python scripts/benchmark_models.py

Every model scores each photo (whole photo, prompt "a photo of {species}.") against
(a) the species list of a trail that contains the true species (one measurement per
such trail, the product setting) and (b) the whole catalog (the pessimistic setting).
Results are split by organ and by upload date: only photos uploaded after a model's
training-data cut-off are an unbiased test of that model (see CUTOFFS).
Report: docs/eval/<date>-model-benchmark.md (+ .json).
"""

from __future__ import annotations

import argparse
import collections
import csv
import gc
import json
import sqlite3
import time
from datetime import date
from pathlib import Path

import numpy as np
import torch

from traily_ia.bioclip_classifier import BioClipClassifier
from traily_ia.pipeline import load_image
from traily_ia.species import load_species_file

# name -> (open_clip model id, last upload date that may be in its training data)
MODELS: dict[str, tuple[str, str | None]] = {
    "bioclip": ("hf-hub:imageomics/bioclip", "2023-11-30"),
    "bioclip-2": ("hf-hub:imageomics/bioclip-2", "2024-05-01"),
    "bioclip-2.5-huge": ("hf-hub:imageomics/bioclip-2.5-vith14", None),
    "biotrove-clip": ("hf-hub:BGLab/BioTrove-CLIP", None),
    "siglip2-base (generic)": ("hf-hub:timm/ViT-B-16-SigLIP2", None),
    "openclip-laion-b16 (generic)": (
        "hf-hub:laion/CLIP-ViT-B-16-laion2B-s34B-b88K",
        None,
    ),
}
# Photos uploaded on/after this date are treated as unseen by every model whose
# cut-off is known or covered by it; models with an unknown cut-off are only
# *probably* clean and are flagged in the report.
CLEAN_FROM = "2024-06-01"
DATASETS = (
    "web_test_images",
    "plantnet_test_images",
    "plantnet_flower_fruit_images",
    "plantnet_nantes_images",
    "web_nantes_images",
)


def load_photos() -> list[dict[str, str]]:
    photos = []
    for folder in DATASETS:
        base = Path("data") / folder
        for row in csv.DictReader((base / "labels.csv").open(encoding="utf-8")):
            photos.append({**row, "path": str(base / row["file"])})
    return photos


def trail_lists(db_path: Path) -> dict[str, list[str]]:
    trails: dict[str, list[str]] = collections.defaultdict(list)
    with sqlite3.connect(db_path) as db:
        for trail, name in db.execute(
            "select trail_id, scientific_name from trail_species"
        ):
            trails[trail].append(name)
    return trails


def evaluate(
    name: str,
    model_id: str,
    photos: list[dict[str, str]],
    trails: dict[str, list[str]],
    catalog: list[str],
) -> dict:
    classifier = BioClipClassifier(model_id=model_id)
    start = time.perf_counter()
    embeddings = [
        (
            classifier.embed_image(load_image(p["path"]))
            if p["species"] in catalog
            else None
        )
        for p in photos
    ]
    seconds = time.perf_counter() - start
    n_embedded = sum(e is not None for e in embeddings)
    catalog_text = classifier.embed_species(catalog)
    trail_text = {t: classifier.embed_species(names) for t, names in trails.items()}
    by_species: dict[str, list[str]] = collections.defaultdict(list)
    for trail, names in trails.items():
        for species in names:
            by_species[species].append(trail)

    rows = []
    for photo, emb in zip(photos, embeddings, strict=True):
        if emb is None:
            continue
        clean = photo["photo_created"] >= CLEAN_FROM
        organ = photo.get("organ") or "unlabelled"
        settings = [("catalog", catalog, catalog_text)]
        settings += [
            ("trail", trails[t], trail_text[t])
            for t in by_species.get(photo["species"], [])
        ]
        for setting, names, text in settings:
            order = np.argsort(-(text @ emb))
            ranked = [names[i] for i in order[:3]]
            rows.append(
                (
                    setting,
                    organ,
                    clean,
                    ranked[0] == photo["species"],
                    photo["species"] in ranked,
                )
            )
    del classifier
    gc.collect()
    torch.cuda.empty_cache()
    return {
        "model": name,
        "ms_per_image": round(1000 * seconds / max(n_embedded, 1), 1),
        "rows": rows,
    }


def summarize(rows: list, setting: str, organ: str | None, clean_only: bool) -> str:
    chosen = [
        r
        for r in rows
        if r[0] == setting
        and (organ is None or r[1] == organ)
        and (not clean_only or r[2])
    ]
    if not chosen:
        return "-"
    top1 = sum(r[3] for r in chosen) / len(chosen)
    top3 = sum(r[4] for r in chosen) / len(chosen)
    return f"{top1:.0%} / {top3:.0%} (n={len(chosen)})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--only", nargs="+", choices=list(MODELS))
    parser.add_argument("--db", type=Path, default=Path("data/db/catalog.sqlite"))
    parser.add_argument(
        "--species-file", type=Path, default=Path("data/species_lists/catalog.txt")
    )
    args = parser.parse_args()

    photos = load_photos()
    trails = trail_lists(args.db)
    catalog = load_species_file(args.species_file)
    results = []
    for name in args.only or MODELS:
        model_id, _ = MODELS[name]
        print(f"== {name}", flush=True)
        results.append(evaluate(name, model_id, photos, trails, catalog))

    today = date.today().isoformat()
    out = ["# Model benchmark — " + today, ""]
    out.append(
        f"{len(photos)} labelled photos (iNaturalist via GBIF + Pl@ntNet), whole photo, "
        'prompt "a photo of {species}.". Cells: top-1 / top-3 (number of measurements). '
        f"**Unseen** = uploaded on/after {CLEAN_FROM}: after the cut-off of BioCLIP (2023-11) "
        "and BioCLIP 2 (GBIF snapshot 2024-05-01). Cut-offs of BioCLIP 2.5 and BioTrove-CLIP "
        "are not published in the sources read, and generic models were trained on web data of "
        "unknown dates: their *unseen* column is probably, not provably, clean."
    )
    for setting in ("trail", "catalog"):
        for clean_only in (True, False):
            title = f"{setting} list, " + (
                "unseen photos only" if clean_only else "all photos"
            )
            out += [
                "",
                f"## {title}",
                "",
                "| model | all organs | bark | leaf | flower | fruit | habit | unlabelled |",
                "|---|---|---|---|---|---|---|---|",
            ]
            for r in results:
                cells = [
                    summarize(r["rows"], setting, o, clean_only)
                    for o in (
                        None,
                        "bark",
                        "leaf",
                        "flower",
                        "fruit",
                        "habit",
                        "unlabelled",
                    )
                ]
                out.append(f"| {r['model']} | " + " | ".join(cells) + " |")
    out += [
        "",
        "## Speed (GPU, image embedding only)",
        "",
        "| model | ms per image |",
        "|---|---|",
    ]
    out += [f"| {r['model']} | {r['ms_per_image']} |" for r in results]
    report = Path("docs/eval") / f"{today}-model-benchmark"
    report.with_suffix(".md").write_text("\n".join(out) + "\n", encoding="utf-8")
    report.with_suffix(".json").write_text(json.dumps(results), encoding="utf-8")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
