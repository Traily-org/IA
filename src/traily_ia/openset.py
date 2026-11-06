"""Telling "this is species X" from "none of the listed species".

BioCLIP is zero-shot over a closed list: whatever the list, the softmax picks a
winner, often with a very high probability even when the true species is not on
it. These are the candidate scores that can be thresholded to answer "none of
these", plus the metrics to compare them. Everything works on embeddings (numpy),
so one pass over the photos is enough to try every list and every score.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

# Prompts for an explicit "something else" class: if one of them wins, the photo is
# not any listed species. Kingdom-level text is meaningful to BioCLIP (it was
# trained with taxonomic strings), the others are plain-language.
OTHER_PROMPTS = (
    "a photo of Plantae.",
    "a photo of a plant.",
    "a photo of a flower.",
    "a photo of a tree.",
    "a photo of a leaf.",
    "a photo of grass.",
)


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max()
    exp = np.exp(shifted)
    return np.asarray(exp / exp.sum())


@dataclass(frozen=True)
class Scores:
    """Acceptance scores for one photo against one candidate list: higher = answer."""

    top: int  # index of the winning species
    prob: float  # softmax probability of the winner
    cosine: float  # raw cosine similarity of the winner (absolute, list-independent)
    margin: float  # winner's probability minus the runner-up's
    other: float  # winner's probability minus the best "other" class (can be < 0)


def score_photo(
    image_feat: np.ndarray,
    species_feats: np.ndarray,
    other_feats: np.ndarray,
    logit_scale: float,
) -> Scores:
    cos = species_feats @ image_feat
    probs = softmax(logit_scale * cos)
    order = np.argsort(-probs)
    top = int(order[0])
    runner_up = float(probs[order[1]]) if len(order) > 1 else 0.0

    # Same species plus the "other" prompts in one softmax: the others absorb the
    # probability mass when the photo looks like none of the species.
    joint = softmax(logit_scale * np.concatenate([cos, other_feats @ image_feat]))
    species_p, other_p = joint[: len(cos)], joint[len(cos) :]
    return Scores(
        top=top,
        prob=float(probs[top]),
        cosine=float(cos[top]),
        margin=float(probs[top]) - runner_up,
        other=float(species_p.max() - other_p.max()),
    )


def auroc(accept_scores: Sequence[float], should_accept: Sequence[bool]) -> float:
    """Chance that a random answer worth accepting outscores a random one that is not.

    0.5 = the score tells nothing, 1.0 = perfect separation (ties count half).
    """
    pos = np.array([s for s, y in zip(accept_scores, should_accept, strict=True) if y])
    neg = np.array(
        [s for s, y in zip(accept_scores, should_accept, strict=True) if not y]
    )
    if len(pos) == 0 or len(neg) == 0:
        raise ValueError("need at least one acceptable and one unacceptable answer")
    greater = (pos[:, None] > neg[None, :]).sum()
    ties = (pos[:, None] == neg[None, :]).sum()
    return float((greater + 0.5 * ties) / (len(pos) * len(neg)))


def threshold_for_recall(scores_of_correct: Sequence[float], recall: float) -> float:
    """Largest threshold that still accepts at least `recall` of the correct answers."""
    if not 0 < recall <= 1:
        raise ValueError("recall must be in (0, 1]")
    ordered = np.sort(np.array(scores_of_correct))[::-1]
    keep = max(1, int(np.ceil(recall * len(ordered))))
    return float(ordered[keep - 1])


def accept_rate(scores: Sequence[float], threshold: float) -> float:
    """Share of answers a threshold lets through (score >= threshold)."""
    return float(np.mean(np.array(scores) >= threshold)) if len(scores) else 0.0
