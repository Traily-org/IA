"""Pick a small, player-friendly herbier list from a trail's full species list.

"Commonness" is how often a species is recorded inside the trail's corridor in
GBIF. That is a proxy: it also reflects where observers go and which plants they
like to record, so it needs a naturalist's eye before release (see TO_CHECK.md).
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from traily_ia.trail_species.gbif import SpeciesOccurrences

Tier = Literal["common", "uncommon"]

DEFAULT_MAX_SPECIES = 20
# Share of the list reserved for "uncommon" species (worth more points).
DEFAULT_UNCOMMON_SHARE = 0.3
# "Uncommon" species are drawn from beyond this share of the most-observed ones.
DEFAULT_UNCOMMON_FROM = 0.2
# Fewer records than this and a species is too rare to ask a player to find.
DEFAULT_MIN_OCCURRENCES = 3


@dataclass(frozen=True)
class SelectedSpecies:
    species: SpeciesOccurrences
    tier: Tier
    rank: int  # 1 = most observed on this trail, among all eligible species


def select_species(
    species: Sequence[SpeciesOccurrences],
    *,
    max_species: int = DEFAULT_MAX_SPECIES,
    uncommon_share: float = DEFAULT_UNCOMMON_SHARE,
    uncommon_from: float = DEFAULT_UNCOMMON_FROM,
    min_occurrences: int = DEFAULT_MIN_OCCURRENCES,
) -> list[SelectedSpecies]:
    """Most-observed species first, then a few uncommon ones, at most `max_species`.

    * Species with fewer than `min_occurrences` records are never selected.
    * If at most `max_species` remain they are all kept (a trail with 10 species
      gets 10): the top `1 - uncommon_share` of them are labelled common, the rest
      uncommon.
    * Otherwise the most-observed `(1 - uncommon_share) * max_species` are common,
      and the uncommon ones are the most-observed species ranked beyond the top
      `uncommon_from` share of the eligible list — findable, but not everywhere.

    The result is ordered common first, then uncommon, each by decreasing count.
    """
    if max_species < 1:
        raise ValueError("max_species must be at least 1")
    if not 0 <= uncommon_share < 1:
        raise ValueError("uncommon_share must be in [0, 1)")

    eligible = sorted(
        (s for s in species if s.occurrences >= min_occurrences),
        key=lambda s: (-s.occurrences, s.scientific_name),
    )
    ranked = [(i + 1, s) for i, s in enumerate(eligible)]
    n_common = max_species - round(max_species * uncommon_share)

    if len(ranked) <= max_species:
        n_common = math.ceil(len(ranked) * (1 - uncommon_share))
        return [
            SelectedSpecies(s, "common" if i <= n_common else "uncommon", i)
            for i, s in ranked
        ]

    common = ranked[:n_common]
    start = max(math.floor(len(ranked) * uncommon_from), n_common)
    uncommon = ranked[start : start + (max_species - n_common)]
    return [SelectedSpecies(s, "common", i) for i, s in common] + [
        SelectedSpecies(s, "uncommon", i) for i, s in uncommon
    ]
