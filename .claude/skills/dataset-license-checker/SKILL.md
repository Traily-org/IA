---
name: dataset-license-checker
description: Looks up and records the license terms of a dataset or pretrained model before it's used, appending an entry to DATASET_LICENSES.md. Use whenever a new dataset, image source, or pretrained model is being considered for identify/ or its evaluation set.
---

# Dataset / model license checker

When the user names a dataset, image source, or pretrained model they want
to use (e.g. "can we use PlantNet-300K", "can we fine-tune on iNaturalist
photos"), do the following:

1. Find the dataset's or model's own license/terms of use (its repo's
   LICENSE file, its official terms page, or its model card) — never guess.
2. If `DATASET_LICENSES.md` doesn't exist at the repo root, create it with
   this header:

   | Source | License | Commercial use? | Notes |
   |---|---|---|---|

3. Append one row summarizing what you found, in plain language, with a
   link to the primary source you checked.
4. Flag explicitly if commercial use is restricted, ambiguous, or requires
   a separate agreement — never mark it "OK" unless the terms are clear.
5. This documents a fact, not legal advice — tell the user to verify
   directly with the source before any real commitment, especially if the
   project's non-commercial status might change.
