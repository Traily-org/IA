"""Shared helpers of the evaluation scripts that use the unseen photos.

Unseen = uploaded after BioCLIP 2's data cutoff, so the model cannot have trained on
them. Each photo is compared with the species list of a trail that contains its
species, as in the other evaluations.
"""

from __future__ import annotations

import csv
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from traily_ia.bioclip_classifier import BioClipClassifier

CUTOFF = "2024-06-01"
FOLDERS = (
    "web_test_images",
    "plantnet_test_images",
    "plantnet_flower_fruit_images",
    "plantnet_nantes_images",
    "web_nantes_images",
)


@dataclass(frozen=True)
class Photo:
    path: Path
    species: str
    organ: str
    creator: str
    licence: str
    source: str


@dataclass(frozen=True)
class Measure:
    photo: Photo
    trail: str
    top: tuple[
        tuple[str, float, float], ...
    ]  # (species, score, similarity), best first

    @property
    def correct(self) -> bool:
        return self.top[0][0] == self.photo.species

    @property
    def score(self) -> float:
        return self.top[0][1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_photos() -> list[Photo]:
    photos: list[Photo] = []
    for folder in FOLDERS:
        root = Path("data") / folder
        credit = {r["file"]: r for r in read_csv(root / "ATTRIBUTION.csv")}
        for r in read_csv(root / "labels.csv"):
            if r["photo_created"] < CUTOFF:
                continue
            c = credit[r["file"]]
            photos.append(
                Photo(
                    path=root / r["file"],
                    species=r["species"],
                    organ=r.get("organ") or "",
                    creator=c["creator"],
                    licence=c["licence"],
                    source=c.get("source") or c.get("photo_page") or "",
                )
            )
    return photos


def load_trails() -> dict[str, list[str]]:
    trails: dict[str, list[str]] = defaultdict(list)
    with sqlite3.connect("data/db/catalog.sqlite") as db:
        for trail, name in db.execute(
            "select trail_id, scientific_name from trail_species"
        ):
            trails[trail].append(name)
    return trails


def softmax_scores(
    clf: BioClipClassifier, text: np.ndarray, names: list[str], emb: np.ndarray
) -> tuple[tuple[str, float, float], ...]:
    sims = text @ emb
    z = clf.logit_scale * sims
    q = np.exp(z - z.max())
    q /= q.sum()
    order = np.argsort(-q)[:3]
    return tuple((names[i], float(q[i]), float(sims[i])) for i in order)
