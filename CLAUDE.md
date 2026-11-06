# ia — Traily species identification, NSFW check & recommendation

Stack: Python 3.11+, FastAPI, Pydantic, Docker.
Endpoints: `POST /identify`, `POST /verify` (independent NSFW pipeline), `POST /recommend`, `GET /health`.
Called by: `server` (Go) over internal HTTP only — never by mobile directly.

Hardware: CPU-only is documented for `recommend` specifically (sentence-transformers + FAISS, per `HARDWARE_REQUIREMENTS.md`) — that does **not** mean "no GPU anywhere in the project." Training/fine-tuning (if it ever happens) uses a GPU. `identify` no longer needs one (decided 2026-11-05, JOURNAL 59): with the detector switched off, the classifier alone takes 0.5 s p95 on 16 CPU threads and 0.03 s on GPU, so the <5s p95 target (Story 8.2) holds on CPU. `Docs/HARDWARE_REQUIREMENTS.md` describes CPU only and is not editable from here.

## Species-ID approach (current plan — drafted in an earlier design discussion with Claude (chat), Oct 2026; **partly validated**: the plants-only scope (no animals, insects or fungi) was confirmed in a team meeting (reported 2026-10-30), and on 2026-11-05 one species per photo, protected species excluded, GBIF lists per trail and abstaining below a threshold (value still to be set on real photos); zero-shot only (few-shot dropped for now) and the model choices are not yet validated, see `TO_ASK.md`; ADR 0001 and ADR 0002)

- **Classifier alone by default; the detector is switched off** (decided 2026-11-05, JOURNAL 58-59): **BioCLIP 2** embeds the **whole photo** and classifies by nearest-neighbor matching — zero-shot (compare against each candidate species' *name*, as text); few-shot was dropped for now (JOURNAL 55). An open-vocabulary detector (Grounding DINO tiny, prompts "a plant", "a flower", "a leaf") is built but off: on 1,443 real unseen measurements the crop retry (whole-photo confidence under 0.7) rescued 4 photos, broke 6 and made 6 confident wrong answers; its 44% → 85% gain was measured only on simulated small subjects, and its box is often tiny or the whole frame on real photos. `use_detector=True` (`--detector` in `identify_local.py`) turns it on; a later benchmark on 600 real photos (4 detectors, 9 prompt versions, JOURNAL 60) found no version that gives a real gain (at best +2 photos out of 600, and more confident errors), so it stays off for the photos tested, which mostly show a plant filling the frame; for distant plants it is not measured (JOURNAL 62), so the code is kept for now. Crop alone was also worse than the whole photo (62% vs 88%, JOURNAL 21-22; `crop_min_area_fraction` re-enables it). The box is never shown to the player.
- **No organ input** (decided 2026-11-05, AI side): the team accepted on 2026-10-30 that the app sends the organ photographed, but it gave no accuracy gain (naming it in the prompt made bark 77% → 71%; 98% top-1 without it), so the AI neither needs nor returns it. Whether the app still wants it for gameplay is a product matter. JOURNAL 56.
- **Distance and clutter: not measured** (JOURNAL 62): without a detector the AI looks at the whole frame, but how much of it the plant must fill is unknown; the simulated tests (a photo pasted into another picture) were withdrawn as invalid. Only a precaution is advised to players (the plant fills at least about three quarters of the picture, sharp and lit), explicitly not a measured limit; the real limit needs real photos at measured distances (`docs/PHOTO_DISTANCE_TEST.md`, plan task B4).
- **Single species per photo for now** — no multi-subject detection in this version.
- Current defaults (benchmarked 2026-10-30, still unvalidated by the team): BioCLIP 2 classifier on the whole photo; Grounding DINO tiny kept as an optional, switched-off detector. Don't treat them as settled until ADR 0001's status is "Accepted"; the 0.7 threshold must be recomputed with real photos (`TO_CHECK.md`).
- `/identify`'s response has an optional bounding-box field (normalised 0-1, internal use only, present only if the detector is switched on, so absent by default; to be confirmed by `server` and mobile) alongside species + confidence — update the contract with whoever owns `server` before building against the old (classification-only) shape.
- **Geographic scope**: the observable-species list for a given trail is generated automatically from GBIF occurrence data (buffer the trail's GPS trace into a polygon, query GBIF's occurrence API once, cache the result per trail) — `/identify` matches against *that* cached list, not the whole species catalog.
- **Herbier (flora collection) scope: flora only** (confirmed in a team meeting, reported 2026-10-30). `Animalia` and `Fungi` are both excluded — animal-welfare reasons for the former, identification-reliability/safety reasons for the latter (misidentifying a mushroom has real physical-safety consequences a misidentified plant doesn't). See ADR 0002.
- **Legally protected species are excluded from the generated list.** GBIF itself has no legal-protection field (`iucnRedListCategory` is *global threat status*, not French legal protection — don't conflate the two). Cross-reference by scientific name / TaxRef `cd_nom` against INPN's "Espèces protégées et réglementées" dataset (the authoritative French source) before caching a trail's list. Exact integration (bulk download vs. TaxRef's own status API) is still to be implemented — see ADR 0002.
- **Response format** (decided 2026-11-05, AI side): `ia` defines its own `/identify` response format (species, confidence, alternatives, abstain reason, similarity, optional box); `server` maps it onto its own tables. Details to agree in plan task A2.
- **Request input** (decided 2026-11-05, AI side): `ia` receives the photo and the trail id, no organ, no GPS. Stripping or keeping the photo's EXIF location is a `server`/mobile privacy matter.
- **No list widening** (decided 2026-11-05, keep it simple): the AI only compares with the trail's list; a species not on it gets `unknown_species`, never a wider search (département, France) as Pl@ntNet does. Whether a species found outside the list earns points is a product matter.
- **Thresholds** (accuracy target, abstain, retry, similarity floor): set by the AI side from real hiker photos (Paimpont), then proposed to the team for agreement (decided 2026-11-05). Temporary value until then: abstain and crop retry both at 0.7, similarity floor off (JOURNAL 55; `scripts/measure_thresholds.py`).
- **Zero-shot only** (decided 2026-11-05): few-shot (plan task C5) is reopened only if real photos show a look-alike problem.
- Confidence below threshold → abstain, route to Epic 2.4's human moderation queue. Never guess. Decided 2026-11-05 (AI side, not yet accepted by product/mobile): for both abstain reasons (`low_confidence`, `unknown_species`) the player still sees the best proposal (`alternatives[0]`) with a soft warning and the confusable species; `species` stays None and the photo goes to moderation.
- **Never retrain on the model's own predictions** — only from validated, human-confirmed labels (Epic 2.4's moderation output).

## Conventions

- Branch names: `feat/TRA-XXX-<short-desc>`, `fix/TRA-XXX-...`, `hotfix/...` (ticket = Linear, team key `TRA`)
- Commits: Conventional Commits with a mandatory scope — `feat(identify): ...`, `fix(recommend): ...`, `docs:`, `chore:`, `test:`
- Always activate `.venv` before running anything; keep `requirements.txt` in sync
- Before opening a PR: `black --check .`, `isort --check .`, `ruff check .`, `mypy --strict src/`, `pytest --cov` — or just `task lint` for all four at once
- Never commit `.venv/`, model weights (`*.pt`, `*.onnx`), or raw/bulk training data (see `.gitignore`)
- Any reference images or dataset pulled from outside your own photography go through the `dataset-license-checker` skill before use, logged in `DATASET_LICENSES.md` — never add a new image source silently

## Process (ESP / Golden Rule of T9)

- If a documented step fails, STOP. Do not silently work around it.
- Log the friction in `DELTA_LOG.md` (prescribed action / observed friction / corrective action) — the `delta-log-entry` skill does this for you.
- Fix the actual source (README, script, `.env.example`), then rerun clean.
- Structural decisions (framework, library, service boundary, detector choice) get an ADR in `docs/adr/` — the `adr-writer` skill scaffolds one.
- Keep running notes as you go, not at the end (`JOURNAL.md`, `TO_ASK.md` and `TO_CHECK.md` are **git-ignored, local to the AI owner**, so references to "JOURNAL 58" in tracked files point to the local journal): `JOURNAL.md` (one entry per decision — Observation / Décision / Pourquoi, French, measured not assumed), `TO_ASK.md` (questions for teammates), `TO_CHECK.md` (facts to verify, measurements still to do). Add to them in the same session the decision or doubt comes up.

## Do not

- Modify any files outside this `IA` repo — `Docs` and `backend` (separate repos in Traily-org, added as read-only context folders) are read freely, since that's useful, but edited by hand, never through this session. If something there genuinely needs to change, say so and let the person decide, don't edit it directly. (This is also enforced technically, not just by this line — see `.claude/settings.json`.)
- Run `git commit` or `git push` without asking first, every time — prepare the change, show the exact commit message (or PR description) and wait for an explicit go-ahead before running it. (Also enforced technically by the local, git-ignored `.claude/settings.json` `ask` rule.)
- Push directly to `main` or `develop` — always via a branch + pull request, opened against `develop`
- Treat any line above as fixed forever. Everything under "Species-ID approach" reflects working decisions that have not all been validated by the team (see `TO_ASK.md`), not unchangeable law — if the team changes its mind, update this file the same day, don't let it silently drift out of sync with reality
