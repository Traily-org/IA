from __future__ import annotations

import numpy as np
import pytest

from traily_ia.openset import (
    accept_rate,
    auroc,
    score_photo,
    softmax,
    threshold_for_recall,
)


def unit(*v: float) -> np.ndarray:
    a = np.array(v, dtype=float)
    return a / np.linalg.norm(a)


def test_softmax_sums_to_one_and_is_stable_for_large_logits() -> None:
    p = softmax(np.array([1000.0, 999.0, 0.0]))

    assert p.sum() == pytest.approx(1.0)
    assert p[0] > p[1] > p[2]


def test_a_photo_that_matches_one_species_scores_high_everywhere() -> None:
    species = np.stack([unit(1, 0, 0), unit(0, 1, 0)])
    others = np.stack([unit(0, 0, 1)])

    s = score_photo(unit(1, 0.05, 0), species, others, logit_scale=100.0)

    assert s.top == 0
    assert s.prob > 0.99 and s.cosine > 0.99
    assert s.margin > 0.99 and s.other > 0.9


def test_a_photo_closer_to_an_other_class_gets_a_negative_other_score() -> None:
    species = np.stack([unit(1, 0, 0), unit(0, 1, 0)])
    others = np.stack([unit(0, 0, 1)])

    s = score_photo(unit(0.3, 0.3, 1), species, others, logit_scale=100.0)

    assert s.other < 0  # an "other" prompt beats every species
    # the plain softmax is still confident about *some* species — the failure mode
    assert s.prob == pytest.approx(0.5, abs=0.01) or s.prob > 0.4


def test_softmax_confidence_is_blind_to_how_poor_the_match_is() -> None:
    species = np.stack([unit(1, 0, 0), unit(0, 1, 0)])
    others = np.stack([unit(0, 0, 1)])
    good = score_photo(unit(1, 0.1, 0), species, others, logit_scale=100.0)
    poor = score_photo(unit(1, 0.1, 5), species, others, logit_scale=100.0)

    assert abs(good.prob - poor.prob) < 0.01  # same softmax answer...
    assert poor.cosine < good.cosine - 0.5  # ...but the raw similarity differs


def test_auroc_extremes_and_ties() -> None:
    assert auroc([0.9, 0.8, 0.2, 0.1], [True, True, False, False]) == 1.0
    assert auroc([0.1, 0.2, 0.8, 0.9], [True, True, False, False]) == 0.0
    assert auroc([0.5, 0.5], [True, False]) == 0.5
    with pytest.raises(ValueError):
        auroc([0.5, 0.6], [True, True])


def test_threshold_keeps_the_requested_share_of_correct_answers() -> None:
    correct = [0.99, 0.95, 0.9, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

    t = threshold_for_recall(correct, 0.8)

    assert accept_rate(correct, t) >= 0.8
    assert t == 0.3
    with pytest.raises(ValueError):
        threshold_for_recall(correct, 0.0)


def test_accept_rate_counts_scores_at_the_threshold() -> None:
    assert accept_rate([0.2, 0.5, 0.9], 0.5) == pytest.approx(2 / 3)
    assert accept_rate([], 0.5) == 0.0
