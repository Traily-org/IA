# Open-set report — 2026-10-30 — 'none of these'

- Calibration photos: 130 from `data/web_test_images` (true species always on the 214-species list)
- Whole-photo classification only (no detector crop); confidence from BioCLIP zero-shot.
- IN: 130 correct + 0 wrong answers. ABSENT: 130 cases with the true species removed, of which 44 still have a species of the same genus on the list (hard: a look-alike is available).
- Labels: iNaturalist research-grade (community-validated).

## Today's rule (softmax probability ≥ 0.5)
Keeps 99% of the correct IN answers, but still answers 46% of the ABSENT cases (wrongly) and 0% of the wrong IN answers.

## Separating a correct answer from a wrong or unknown one (AUROC, 0.5 = useless, 1 = perfect)

| score | AUROC |
|---|---|
| softmax probability (today's rule) | 0.978 |
| raw cosine similarity | 0.998 |
| margin top-1 minus top-2 | 0.971 |
| explicit 'other' classes | 0.982 |

## Threshold that keeps 95% of the correct IN answers

| score | threshold | wrong IN answers still accepted | ABSENT answered | ABSENT answered (look-alike on list) | ABSENT answered (no look-alike) |
|---|---|---|---|---|---|
| softmax probability (today's rule) | 0.812 | 0% | 15% | 16% | 15% |
| raw cosine similarity | 0.711 | 0% | 1% | 2% | 0% |
| margin top-1 minus top-2 | 0.655 | 0% | 20% | 23% | 19% |
| explicit 'other' classes | 0.808 | 0% | 12% | 11% | 13% |

## Threshold that keeps 90% of the correct IN answers

| score | threshold | wrong IN answers still accepted | ABSENT answered | ABSENT answered (look-alike on list) | ABSENT answered (no look-alike) |
|---|---|---|---|---|---|
| softmax probability (today's rule) | 0.970 | 0% | 4% | 5% | 3% |
| raw cosine similarity | 0.718 | 0% | 0% | 0% | 0% |
| margin top-1 minus top-2 | 0.947 | 0% | 4% | 5% | 3% |
| explicit 'other' classes | 0.969 | 0% | 4% | 5% | 3% |

## Threshold that keeps 80% of the correct IN answers

| score | threshold | wrong IN answers still accepted | ABSENT answered | ABSENT answered (look-alike on list) | ABSENT answered (no look-alike) |
|---|---|---|---|---|---|
| softmax probability (today's rule) | 0.991 | 0% | 2% | 0% | 2% |
| raw cosine similarity | 0.722 | 0% | 0% | 0% | 0% |
| margin top-1 minus top-2 | 0.986 | 0% | 2% | 0% | 2% |
| explicit 'other' classes | 0.991 | 0% | 1% | 0% | 1% |

## Applied to a naturally mixed folder: `data/test_images` (16 photos, 12 whose species is not on the list)
Thresholds from the 90% setting above. 'Wrongly answered' = a species was given for a photo whose species is not on the list; 'right' = correct species given for a listed one.

| score | wrongly answered (not on list) | right (on list) | on-list photos wrongly rejected or wrong |
|---|---|---|---|
| softmax probability (today's rule) | 5/12 | 2/4 | 2/4 |
| raw cosine similarity | 2/12 | 3/4 | 1/4 |
| margin top-1 minus top-2 | 5/12 | 2/4 | 2/4 |
| explicit 'other' classes | 5/12 | 2/4 | 2/4 |
