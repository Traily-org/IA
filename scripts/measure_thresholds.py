"""Measure what each confidence threshold answers and gets right.

Uses the photos uploaded after BioCLIP 2's data cutoff (unseen by the model) and
each photo's own trail species list, whole photo only. Writes
docs/results/thresholds.json for the dashboard.
"""

from __future__ import annotations

import csv
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

import numpy as np

from traily_ia.bioclip_classifier import BioClipClassifier
from traily_ia.pipeline import load_image

CUTOFF = "2024-06-01"
FOLDERS = (
    "web_test_images",
    "plantnet_test_images",
    "plantnet_flower_fruit_images",
    "plantnet_nantes_images",
    "web_nantes_images",
)
CONFIDENCE = (0.5, 0.6, 0.7, 0.8, 0.9)
OUT = Path("docs/results/thresholds.json")


def main() -> None:
    trails: dict[str, list[str]] = defaultdict(list)
    with sqlite3.connect("data/db/catalog.sqlite") as db:
        for trail, name in db.execute(
            "select trail_id, scientific_name from trail_species"
        ):
            trails[trail].append(name)
    by_species: dict[str, list[str]] = defaultdict(list)
    for trail, names in trails.items():
        for name in names:
            by_species[name].append(trail)

    photos: list[tuple[Path, str]] = []
    for folder in FOLDERS:
        path = Path("data") / folder / "labels.csv"
        with open(path, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r["photo_created"] >= CUTOFF and r["species"] in by_species:
                    photos.append((path.parent / r["file"], r["species"]))

    clf = BioClipClassifier()
    texts = {t: clf.embed_species(names) for t, names in trails.items()}
    scored: list[tuple[float, float, bool]] = []
    for path, species in photos:
        emb = clf.embed_image(load_image(path))
        trail = by_species[species][0]
        sim = texts[trail] @ emb
        z = clf.logit_scale * sim
        q = np.exp(z - z.max())
        q /= q.sum()
        i = int(np.argmax(sim))
        scored.append((float(q[i]), float(sim[i]), trails[trail][i] == species))

    a = np.array(scored, dtype=float)
    rows = []
    for t in CONFIDENCE:
        m = a[:, 0] >= t
        rows.append(
            {
                "threshold": t,
                "answered": float(m.mean()),
                "right_when_answered": float(a[m, 2].mean()),
                "wrong_answers": int((m & (a[:, 2] == 0)).sum()),
            }
        )
    OUT.write_text(
        json.dumps({"measurements": len(a), "rows": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{len(a)} measurements -> {OUT}")


if __name__ == "__main__":
    main()
