"""BioCLIP 2 zero-shot classification of a photo.

Zero-shot only for now (ADR 0001): the photo is embedded and compared with the
text embedding of each candidate species name. Few-shot reference images get
added later, per species, only where evaluation shows zero-shot struggling.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from collections.abc import Sequence

import numpy as np
import open_clip
import torch
from PIL import Image

from traily_ia.result import SpeciesScore

DEFAULT_MODEL_ID = "hf-hub:imageomics/bioclip-2"
PROMPT_TEMPLATE = "a photo of {}."
# Text embeddings kept per candidate list (one per trail): the least recently used
# list is dropped beyond this, so memory stays bounded however many trails exist.
TEXT_CACHE_SIZE = 64


class BioClipClassifier:
    def __init__(
        self, *, model_id: str = DEFAULT_MODEL_ID, device: str | None = None
    ) -> None:
        self._device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        model, _, preprocess = open_clip.create_model_and_transforms(model_id)
        self._model = model.to(self._device).eval()
        self._preprocess = preprocess
        self._tokenizer = open_clip.get_tokenizer(model_id)
        self._text_cache: OrderedDict[tuple[str, ...], torch.Tensor] = OrderedDict()
        self._cache_lock = threading.Lock()

    def _text_features(self, candidates: Sequence[str]) -> torch.Tensor:
        # Candidate lists are per trail and reused across many photos.
        key = tuple(candidates)
        with self._cache_lock:
            cached = self._text_cache.get(key)
            if cached is not None:
                self._text_cache.move_to_end(key)
                return cached
        tokens = self._tokenizer([PROMPT_TEMPLATE.format(c) for c in candidates])
        with torch.no_grad():
            feats = self._model.encode_text(tokens.to(self._device))
        features = torch.nn.functional.normalize(feats, dim=-1)
        with self._cache_lock:
            self._text_cache[key] = features
            while len(self._text_cache) > TEXT_CACHE_SIZE:
                self._text_cache.popitem(last=False)
        return features

    @property
    def logit_scale(self) -> float:
        """Temperature BioCLIP learned: probabilities = softmax(scale * cosine)."""
        return float(self._model.logit_scale.exp())

    def embed_image(self, image: Image.Image) -> np.ndarray:
        """L2-normalised image embedding, shape (d,)."""
        pixels = self._preprocess(image).unsqueeze(0).to(self._device)
        with torch.no_grad():
            feats = torch.nn.functional.normalize(
                self._model.encode_image(pixels), dim=-1
            )
        return np.asarray(feats[0].cpu().numpy())

    def embed_texts(self, texts: Sequence[str]) -> np.ndarray:
        """L2-normalised embeddings of raw prompts (no template added), (n, d)."""
        tokens = self._tokenizer(list(texts))
        with torch.no_grad():
            feats = torch.nn.functional.normalize(
                self._model.encode_text(tokens.to(self._device)), dim=-1
            )
        return np.asarray(feats.cpu().numpy())

    def embed_species(self, names: Sequence[str]) -> np.ndarray:
        """Embeddings of species names with the standard prompt, (n, d)."""
        return self.embed_texts([PROMPT_TEMPLATE.format(n) for n in names])

    def classify(
        self, crop: Image.Image, candidates: Sequence[str]
    ) -> list[SpeciesScore]:
        text_features = self._text_features(candidates)
        pixels = self._preprocess(crop).unsqueeze(0).to(self._device)
        with torch.no_grad():
            image_features = torch.nn.functional.normalize(
                self._model.encode_image(pixels), dim=-1
            )
            cosines = (image_features @ text_features.T)[0]
            logits = self._model.logit_scale.exp() * cosines
            probs = logits.softmax(dim=-1).tolist()
            sims = cosines.tolist()
        ranked = sorted(
            zip(candidates, probs, sims, strict=True), key=lambda row: -row[1]
        )
        return [
            SpeciesScore(species=name, score=float(p), similarity=float(c))
            for name, p, c in ranked
        ]
