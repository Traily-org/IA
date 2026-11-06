---
name: model-eval-report
description: Runs the labeled validation set against the current identify/ model and produces a formatted report (top-1/top-3 accuracy, per-species confusion, confidence calibration). Use whenever a model or threshold change needs to be measured, not just "looks like it works."
---

# Model evaluation report

1. Locate the labeled validation set and the current model/embedding
   pipeline in `identify/`.
2. Run inference over the validation set and compute: top-1 accuracy,
   top-3 accuracy, a confusion matrix for the most-confused species pairs,
   and a calibration check (does "80% confident" mean ~80% correct?).
3. Write the results to a dated file under `docs/eval/` (create it if
   missing) — never overwrite a previous report, so accuracy over time
   stays visible.
4. Compare against the previous report if one exists, and call out any
   regression explicitly.
5. This is what QUALITY_PLAN_AI_SERVICES.md's "seuil cible à définir avec
   l'équipe" needs to actually get defined — use the report to propose a
   number instead of leaving it blank.
