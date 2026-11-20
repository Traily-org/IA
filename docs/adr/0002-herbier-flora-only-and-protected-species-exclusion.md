# ADR 0002: The herbier (flora collection) covers plants only; lists generated from GBIF; legally protected species excluded

## Status
Proposed

## Context
The trail species-collection feature (the "Herbier", the team's official name for the flora collection, Epic 3.1): a per-trail list of observable species, grayed out until a user's identified photo unlocks them, builds on `BACKLOG.md`'s Story 2.2 ("Génération de listes d'espèces observables") and Epic 2.4 (moderation). Two scope questions came up during design and were settled in an earlier design discussion with Claude (chat — not a team meeting; not yet validated by the team, see `TO_ASK.md`): which kingdoms to include, and whether the feature could inadvertently encourage harmful behavior (disturbing wildlife, or seeking out legally protected species).

## Decision
- **Scope is Plantae only.** `Animalia` is excluded so the app never incentivizes someone to chase, corner, or disturb a wild animal just to complete a collection. `Fungi` is also excluded: unlike common plants, reliable mushroom identification from a single photo is unreliable even for professional mycologists, and a wrong answer here isn't just a mislabel — a toxic species can closely resemble an edible one. Both are product/safety decisions, not just technical simplifications.
- **The observable-species list is generated automatically per trail**, by buffering the trail's GPS trace (already in `server`'s PostGIS) into a polygon and querying GBIF's occurrence API once, cached per trail (a natural fit alongside the `aggregate/` batch job, Story 8.4).
- **Legally protected species are excluded from the generated list.** GBIF itself has no legal-protection field — its `iucnRedListCategory` parameter is *global conservation threat status* (IUCN Red List), not French legal protection, and the two should not be conflated. The authoritative source for French legal protection is INPN/TaxRef's "Espèces protégées et réglementées" dataset (Muséum national d'Histoire naturelle), which covers over 60,000 taxon-status records derived from the actual legal texts ("arrêtés de protection"), keyed by TaxRef's `cd_nom` identifier: https://www.data.gouv.fr/fr/datasets/inpn-especes-protegees-et-reglementees/ — TaxRef also exposes its own status API (https://taxref.mnhn.fr/taxref-web/api/webservice), though its exact request/response schema still needs to be verified directly before integration.

## Consequences
- Narrower kingdom scope simplifies the identification problem for `identify/` (one kingdom's visual diversity instead of three) and removes the need to design foraging-safety UX for fungi.
- Adds a new batch-time dependency (INPN/TaxRef data, cross-referenced by `cd_nom`) alongside the existing GBIF query — exact integration method (bulk download vs. the TaxRef status API) is still to be implemented and tested; budget real time for this, don't assume it's a one-line filter.
- `iucnRedListCategory` remains useful as a secondary, global conservation-status signal (e.g. for the "rarity tiers" gamification idea), but must never be used as a stand-in for actual French legal protection status.
- Worth writing jointly with whoever owns Story 2.2 and the `aggregate/` job, since this touches `server`'s PostGIS data and the batch pipeline as much as `ia`.

## Update 2026-10-09 — protection filter implemented (status still Proposed)
- **Integration method chosen: bulk download**, not the TaxRef status API. INPN's own site (`inpn.mnhn.fr`) is down after a cyberattack on MNHN servers; PatriNat publishes temporary links on `assets.patrinat.fr`. Files used: BDC v18 (statuses; content 2025-07-24) + TaxRef v18 (synonyms; content 2025-01-09). These links are temporary and no licence is stated — see `DATASET_LICENSES.md`.
- **Matching**: by scientific name, via TaxRef so that a protected taxon is also recognised under its synonyms; a protected *accepted* subspecies/variety also makes its parent species unlisted. Only BDC "Protection" statuses (PN, PR, PD, POM) count; "Réglementation" (invasives, picking rules) does not.
- **Scope**: default `anywhere` (national, or any metropolitan region/département) because the trail's own region is not yet used. This removes between 13 of 118 (Rennes) and 236 of 608 (Vercors) of the GBIF species on the 13 test trails, versus 1 to 12 with national protection only. A region/département-aware filter would keep many more species and is the natural follow-up.
- **Freshness**: the index records its inputs' versions and dates, and the cache key includes them; a warning is raised above 365 days. The data was already 442–638 days old when first used.
- See `JOURNAL.md` entries 6–10 for the observations behind these choices.

## Update 2026-10-14 — scope is now the trail's own zone
- Default scope changed from `anywhere` to `local`: national protection (PN) plus the régional (PR) and départemental (PD) protections of the départements/régions the trail runs through. The zone comes from `geo.api.gouv.fr` (sampled points of the trace, cached) and is part of the cache key. BDC still labels regional protections with the pre-2016 regions, so each current region maps to its former regions.
- Effect on the 13 test trails (5,072 trail-species pairs): 86 removed with national protection only, **256 with `local`**, 1,422 with `anywhere` (still available via `--scope anywhere`).
- Fails closed: `local` without a location raises; the index build refuses a metropolitan PR/PD zone code it cannot place.
- Known gaps: the 500 m corridor edge is not sampled for the zone; the combined catalog can contain a species protected in another region (see `TO_ASK.md`); no overseas support.

