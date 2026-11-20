"""BioClipClassifier logic with a tiny fake open_clip model (no weights downloaded)."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import pytest
import torch
from PIL import Image

from traily_ia import bioclip_classifier as module
from traily_ia.bioclip_classifier import PROMPT_TEMPLATE, BioClipClassifier

# One axis per species: a prompt "a photo of <name>." embeds to that species' axis.
AXES = {"Quercus robur": 0, "Ilex aquifolium": 1, "Fagus sylvatica": 2}
DIM = 4


class FakeModel:
    def __init__(self, image_vector: list[float]) -> None:
        self.image_vector = torch.tensor([image_vector])
        self.logit_scale = torch.tensor(math.log(100.0))
        self.text_calls = 0

    def to(self, device: str) -> FakeModel:
        return self

    def eval(self) -> FakeModel:
        return self

    def encode_text(self, tokens: torch.Tensor) -> torch.Tensor:
        self.text_calls += 1
        return tokens.float()

    def encode_image(self, pixels: torch.Tensor) -> torch.Tensor:
        return self.image_vector


def fake_tokenizer(prompts: Sequence[str]) -> torch.Tensor:
    rows = torch.zeros(len(prompts), DIM)
    for i, prompt in enumerate(prompts):
        name = prompt.removeprefix("a photo of ").removesuffix(".")
        rows[i, AXES.get(name, 3)] = 1.0
    return rows


def make_classifier(
    monkeypatch: pytest.MonkeyPatch, image_vector: list[float]
) -> tuple[BioClipClassifier, FakeModel]:
    model = FakeModel(image_vector)

    def create(model_id: str) -> tuple[Any, None, Any]:
        return model, None, lambda image: torch.zeros(3, 2, 2)

    monkeypatch.setattr(module.open_clip, "create_model_and_transforms", create)
    monkeypatch.setattr(
        module.open_clip, "get_tokenizer", lambda model_id: fake_tokenizer
    )
    return BioClipClassifier(device="cpu"), model


PHOTO = Image.new("RGB", (8, 8))


def test_candidates_are_ranked_by_probability_and_probabilities_sum_to_one(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clf, _ = make_classifier(monkeypatch, [0.2, 0.9, 0.1, 0.0])

    scores = clf.classify(PHOTO, list(AXES))

    assert [s.species for s in scores][0] == "Ilex aquifolium"
    assert [s.score for s in scores] == sorted((s.score for s in scores), reverse=True)
    assert sum(s.score for s in scores) == pytest.approx(1.0)


def test_similarity_is_the_raw_cosine_and_ignores_the_other_candidates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clf, _ = make_classifier(monkeypatch, [3.0, 4.0, 0.0, 0.0])

    short = clf.classify(PHOTO, ["Ilex aquifolium"])
    long = clf.classify(PHOTO, list(AXES))

    # (0, 1, 0, 0) . (3, 4, 0, 0) / 5 = 0.8, whatever else is on the list.
    assert short[0].similarity == pytest.approx(0.8)
    best = next(s for s in long if s.species == "Ilex aquifolium")
    assert best.similarity == pytest.approx(0.8)


def test_the_text_embeddings_of_a_list_are_computed_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clf, model = make_classifier(monkeypatch, [1.0, 0.0, 0.0, 0.0])

    clf.classify(PHOTO, list(AXES))
    clf.classify(PHOTO, list(AXES))

    assert model.text_calls == 1


def test_the_text_cache_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    clf, _ = make_classifier(monkeypatch, [1.0, 0.0, 0.0, 0.0])
    monkeypatch.setattr(module, "TEXT_CACHE_SIZE", 2)

    for name in AXES:
        clf.classify(PHOTO, [name])

    assert len(clf._text_cache) == 2
    assert ("Quercus robur",) not in clf._text_cache


def test_logit_scale_is_the_models_temperature(monkeypatch: pytest.MonkeyPatch) -> None:
    clf, _ = make_classifier(monkeypatch, [1.0, 0.0, 0.0, 0.0])

    assert clf.logit_scale == pytest.approx(100.0)


def test_species_embeddings_use_the_standard_prompt_and_are_normalised(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clf, _ = make_classifier(monkeypatch, [1.0, 0.0, 0.0, 0.0])

    emb = clf.embed_species(["Quercus robur"])

    assert PROMPT_TEMPLATE.format("x") == "a photo of x."
    assert emb.shape == (1, DIM)
    assert float((emb**2).sum()) == pytest.approx(1.0)
    assert emb[0, AXES["Quercus robur"]] == pytest.approx(1.0)
