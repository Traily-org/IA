# ADR 0001: Species identification via detection (bounding box) + BioCLIP classification

## Status
Proposed : detector choice not yet finalized (see Consequences). Provenance note (2026-10-15): this ADR comes from an earlier design discussion with Claude (chat), **not from a team meeting**; nothing in it has been validated by the team yet, and the crop-then-classify decision was reversed by the measurements in the updates below.

## Context
`ARCHITECTURE.md` marks the species-identification model "à déterminer." Real training data is scarce (on the order of tens of photos for any one species locally), ruling out training a classifier from scratch. An earlier design discussion (with Claude, chat — not a team meeting, despite how earlier versions of this ADR worded it) proposed two decisions on top of the existing BioCLIP plan: (1) `/identify` should return a bounding box around the identified subject, not just a bare label, so the plan moved to a detection-based approach rather than whole-image classification (teammates have since said they would like the box shown in the app); (2) for this version, exactly one species is assumed per photo — multi-subject detection is explicitly out of scope.

A pure classification approach (embed the whole photo, no localization) was the original default, but doesn't produce a bounding box and performs worse when the subject is a small part of a cluttered frame (the common case for trail photos) — this was a hypothesis, not measured at the time; see the 2026-10-14 update. A general computer-vision rule applies here: localizing the subject first and classifying only the crop is a different, more involved pipeline than classification alone, and the localization step itself is a real design decision, not a detail.

## Decision
Use a two-stage pipeline:

1. **Localization**: a pretrained, open-vocabulary (zero-shot) object detector takes the full photo and a generic text prompt (e.g. "plant", "flower", "mushroom") and returns **one** bounding box around the most likely main subject. No custom training.
2. **Classification** *(superseded in part, see the 2026-10-15 update: the whole photo is classified by default, not the crop)*: the cropped region is embedded with **BioCLIP** and matched against candidate species — **zero-shot** (comparing against each species' *name* as text) by default, with **few-shot** (a handful of reference images, Waypoint 05 of the onboarding guide) added only for species an evaluation shows zero-shot measurably struggling with.

Candidate detectors evaluated for the localization step (none yet benchmarked against the project's own `<5s p95` CPU latency target — that benchmarking is the next concrete step before this ADR can move to "Accepted"):

| Candidate | Fit | Source |
|---|---|---|
| YOLO-World (Tencent AILab) | Best CPU-latency fit of the three; built for real-time use; exports to ONNX/TFLite-INT8 | https://github.com/AILab-CVC/YOLO-World |
| OWLv2 (Google DeepMind) | Simplest to integrate (ships in HuggingFace `transformers`, CPU-capable); no published CPU latency numbers — needs local profiling | https://huggingface.co/docs/transformers/en/model_doc/owlv2 |
| Grounding DINO (IDEA-Research) | Likely most accurate on organic/irregular shapes (plants, fungi); heavier; Apache-2.0, has a `--cpu-only` mode | https://github.com/idea-research/groundingdino |

All three were trained on rigid-object benchmarks (COCO/LVIS-style), not biological shapes specifically — this is a known limitation worth validating empirically (the `model-eval-report` skill), not assuming away.

## Consequences
- `/identify`'s response contract gains a bounding-box field alongside species + confidence — needs to be re-confirmed with whoever owns `server`, since the previously-proposed MVP shape (species + confidence only) is now out of date.
- Adds a second model/dependency to the inference path, on top of BioCLIP itself — total latency against the `<5s p95` target needs real measurement, not assumption, once a detector candidate is chosen.
- Single-subject assumption means a photo with multiple distinct organisms will only ever report one of them for now; revisit as its own future ADR if that turns out to matter in practice.
- This decision should move from "Proposed" to "Accepted" only after the detector benchmarking step above is actually run — don't treat the candidate table as a final choice.

## Update 2026-10-14 — first measurements (status still Proposed)
- The pipeline now runs end to end with OWLv2 (provisional) + BioCLIP zero-shot. Labelled evaluation: 130 licensed iNaturalist photos of catalog species (closed list of 214, true species always on it) and 16 team photos (labels from PlantNet, unverified).
- **Classifying the detector's crop was clearly worse than classifying the whole photo**: top-1 62% vs 88%, top-3 71% vs 97% on the 130 photos. Damage comes from small boxes: 36 photos had a box under 5% of the image (crop 5 right, whole photo 32); with a box of 40% or more both are equal. No "crop only if the box is at least T% of the photo" variant beat the whole photo.
- Caveat: these photos are centred on their subject. The case that motivated the detector — a small subject in a cluttered trail photo — is not represented yet.
- First implemented as an option (`crop_min_area_fraction`), then made the default on 2026-10-15 — see below. This benchmark does not yet compare detectors (OWLv2 vs YOLO-World vs Grounding DINO), so the ADR stays Proposed.
- Details: `JOURNAL.md` entries 20–21, reports in `docs/eval/`.

## Update 2026-10-15 — whole photo is classified; the box is kept for display only
- Context: this ADR (and the `CLAUDE.md` section) came from a design discussion with Claude (chat), not from the team, so there was no team commitment to the crop-then-classify design. Teammates would like the bounding box displayed in the app, so the detector stays.
- **Decision:** the classifier now sees the **whole photo** by default (`crop_min_area_fraction=None`). The detector only supplies the box returned in the response; no detected subject no longer blocks identification (the box is simply absent). Classifying the crop remains available (`0.0` = always crop, `t > 0` = crop only if the box covers at least `t` of the photo).
- **Why:** 130 labelled photos: top-1 88% / top-3 97% (whole photo) vs 62% / 71% (crop); no threshold variant beat the whole photo. Confirmed through the CLI path after the change (114/130 and 126/130, box returned on 125 photos).
- **Consequences:** the detector is now a display feature. It costs about 0.2 s per photo and one extra model. If the team stops wanting the box, it can be removed with no loss in accuracy; if trail-style photos (small subject in a cluttered frame) ever show the crop helping, `crop_min_area_fraction` re-enables it. The `/identify` contract still has to be agreed with whoever owns `server` (`TO_ASK.md`).


## Update 2026-10-30 — BioCLIP 2, Grounding DINO tiny, and a retry with the crop (status still Proposed)
- **Classifier:** `imageomics/bioclip-2` replaces BioCLIP. On 624 measurements with photos it cannot have seen (uploaded after its 2024-05-01 data), trail species list: top-1 97% vs 89%, bark 94% vs 77%; against the 214-species catalog 91% vs 70%. Costs 3x the parameters, 1.6 GB of weights, about 0.4-0.65 s more on CPU. BioCLIP 2.5 Huge adds nothing measurable for 1.6x the time; BioTrove-CLIP and generic CLIP/SigLIP2 are far behind (`docs/eval/2026-10-30-model-benchmark.md`, JOURNAL 34-35).
- **Detector:** Grounding DINO tiny replaces OWLv2. 150 unseen photos, subject pasted small so the true box is known: it finds the subject on 100% of photos (OWLv2 73-85%) and its box overlaps the true one (IoU >= 0.5) on 88-95% of the cases (OWLv2 43-49%) at the same speed (172 ms GPU, 3.6 s on 16 CPU threads). OWLv2 large is 5x slower for no gain; OWL-ViT is very fast (0.33 s CPU) but misses the subject too often; Grounding DINO base is slower with no gain; YOLO-World was not tested (ultralytics is AGPL). `docs/eval/2026-10-30-detector-benchmark.md`, JOURNAL 38.
- **Retry with the crop:** the whole photo stays the first look. When its confidence is under 0.7 (`crop_retry_below`, not calibrated on real photos) the detector's crop is classified too and the more confident answer is kept. With simulated mess this matched "always both" and lifted tiny subjects (25% of the width) from 49% to about 72-91%, depending on the detector, without hurting clean photos (JOURNAL 36-37).
- **Limits:** the mess is simulated by code, not real hiker photos, and the benchmark may favour Grounding DINO because a pasted subject has sharp edges on a blurred background. Thresholds must be recomputed with real photos (`TO_CHECK.md`). The training data of the BioCLIP family mixes non-commercial licences (`DATASET_LICENSES.md`).
- The status stays Proposed: nobody on the team has validated these choices.

## Update 2026-11-05 — the detector is switched off by default (status still Proposed)

On the 1,443 real measurements unseen by BioCLIP 2 (trail lists), 40 had a whole-photo confidence under 0.7 and went through the detector and the crop retry. The whole photo alone gave 28 right proposals out of 40, all withheld; with the crop, 26 out of 40 (4 rescued, 6 broken), 18 photos passed the 0.7 threshold, 12 right and 6 wrong. Its boxes covered 5% of the photo or less in 9 cases and 90% or more in 16. The 44% → 85% gain of the retry (JOURNAL 36-37) and the 92-99% box accuracy (JOURNAL 38) come from simulated photos, a clean photo pasted small on a blurred copy of itself, where the plant is the only sharp object. At most 26 of the 1,443 first answers are wrong, which caps what any detector can fix.

**Decision.** The pipeline is the classifier alone by default (`use_detector=False`); the detector code stays, behind `use_detector=True`, for a re-test on real photos with hand-drawn boxes (plan task C6, possibly with the Eindhoven Wildflower Dataset after a licence check, and a single "a plant" prompt). The stage-1 detector decision of the 2026-10-30 update is therefore suspended, not reversed. See JOURNAL 58-59.

## Update 2026-11-06 — no detector or prompt helps on real photos (status still Proposed)

Tested on 600 real unseen photos (`scripts/benchmark_detectors_real.py`): Grounding DINO tiny and base, OWLv2 base and large, each with its default prompts and with "a plant" only (and, for tiny, a prompt naming the organ). With the default prompts 24-32% of the boxes are tiny and 21-28% cover the whole frame; with "a plant" the tiny boxes disappear but 52-63% become the whole frame. At best the retry rescues 2 photos more than it breaks out of 600 (Grounding DINO base, default prompts), and every version adds confident wrong answers (6 to 11 against 5 for the whole photo alone). The detector stays off and its code can be deleted once the team agrees. See JOURNAL 60.
