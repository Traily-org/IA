# Open-set report — 2026-10-15 — 'none of these'

- Calibration photos: 130 from `data/web_test_images` (true species always on the 214-species list)
- Whole-photo classification only (no detector crop); confidence from BioCLIP zero-shot.
- IN: 114 correct + 16 wrong answers. ABSENT: 130 cases with the true species removed, of which 44 still have a species of the same genus on the list (hard: a look-alike is available).
- Labels: iNaturalist research-grade (community-validated).

## Today's rule (softmax probability ≥ 0.5)
Keeps 98% of the correct IN answers, but still answers 76% of the ABSENT cases (wrongly) and 81% of the wrong IN answers.

## Separating a correct answer from a wrong or unknown one (AUROC, 0.5 = useless, 1 = perfect)

| score | AUROC |
|---|---|
| softmax probability (today's rule) | 0.882 |
| raw cosine similarity | 0.929 |
| margin top-1 minus top-2 | 0.873 |
| explicit 'other' classes | 0.899 |

## Threshold that keeps 95% of the correct IN answers

| score | threshold | wrong IN answers still accepted | ABSENT answered | ABSENT answered (look-alike on list) | ABSENT answered (no look-alike) |
|---|---|---|---|---|---|
| softmax probability (today's rule) | 0.627 | 56% | 65% | 70% | 62% |
| raw cosine similarity | 0.273 | 69% | 32% | 34% | 31% |
| margin top-1 minus top-2 | 0.421 | 38% | 65% | 73% | 60% |
| explicit 'other' classes | 0.626 | 50% | 53% | 59% | 50% |

## Threshold that keeps 90% of the correct IN answers

| score | threshold | wrong IN answers still accepted | ABSENT answered | ABSENT answered (look-alike on list) | ABSENT answered (no look-alike) |
|---|---|---|---|---|---|
| softmax probability (today's rule) | 0.825 | 31% | 41% | 39% | 42% |
| raw cosine similarity | 0.291 | 38% | 18% | 25% | 14% |
| margin top-1 minus top-2 | 0.701 | 31% | 44% | 39% | 47% |
| explicit 'other' classes | 0.825 | 19% | 32% | 30% | 34% |

## Threshold that keeps 80% of the correct IN answers

| score | threshold | wrong IN answers still accepted | ABSENT answered | ABSENT answered (look-alike on list) | ABSENT answered (no look-alike) |
|---|---|---|---|---|---|
| softmax probability (today's rule) | 0.945 | 19% | 22% | 25% | 21% |
| raw cosine similarity | 0.310 | 19% | 8% | 11% | 6% |
| margin top-1 minus top-2 | 0.916 | 19% | 22% | 25% | 20% |
| explicit 'other' classes | 0.943 | 19% | 19% | 23% | 17% |

## Applied to a naturally mixed folder: `data/test_images` (16 photos, 12 whose species is not on the list)
Thresholds from the 90% setting above. 'Wrongly answered' = a species was given for a photo whose species is not on the list; 'right' = correct species given for a listed one.

| score | wrongly answered (not on list) | right (on list) | on-list photos wrongly rejected or wrong |
|---|---|---|---|
| softmax probability (today's rule) | 6/12 | 2/4 | 2/4 |
| raw cosine similarity | 6/12 | 2/4 | 2/4 |
| margin top-1 minus top-2 | 6/12 | 2/4 | 2/4 |
| explicit 'other' classes | 6/12 | 2/4 | 2/4 |
