# Quality Plan — Services IA (brouillon)

> Brouillon rédigé le 2026-11-05 sur le modèle de `QUALITY_PLAN_BACKEND.md`. Le fichier est référencé par `DEVELOPMENT_PROCESS.md` mais n'existait pas. Il vit pour l'instant dans le dépôt `IA` ; une fois relu, il peut être déposé dans `Docs`. Ce qui n'est pas encore validé par l'équipe est marqué « à valider ».

## Vue d'ensemble

Micro-service Python appelé uniquement par le backend Go, jamais directement par le mobile. Endpoints prévus : `POST /identify` (espèce d'une photo), `POST /verify` (contrôle de contenu, pipeline indépendant), `POST /recommend` (suggestion de parcours), `GET /health`. Seule `identify` existe aujourd'hui, sous forme d'une fonction Python testable (`detect_and_classify`) et d'une ligne de commande ; la couche HTTP viendra ensuite.

---

## Conventions

- Python 3.11+, environnement virtuel `.venv` toujours activé, `requirements.txt` maintenu à jour
- **[Conventional Commits](https://www.conventionalcommits.org/)** avec une portée obligatoire : `feat(identify): ...`, `fix(recommend): ...`, `docs:`, `chore:`, `test:`
- Formatage `black` + `isort` ; lint `ruff` ; typage `mypy --strict` sur `src/` : aucun code non conforme n'est fusionné
- Docstrings sur les fonctions et classes publiques ; un commentaire seulement quand le pourquoi n'est pas évident
- Branches : `feat/`, `fix/`, `chore/`, `docs/`, `test/`, avec la clé Linear réelle `TRA` (`feat/TRA-41-...`)

---

## Structure

```
src/traily_ia/
  pipeline.py        # classifieur (+ détecteur optionnel), décision de répondre ou de s'abstenir
  result.py          # types de résultat, sans dépendance à un framework
  *_classifier.py    # classifieur (BioCLIP 2, zéro-shot)
  *_detector.py      # détecteur (Grounding DINO tiny), désactivé par défaut
  trail_species/     # listes d'espèces par parcours (propriétaire à confirmer, voir plus bas)
scripts/             # évaluation, benchmarks, constructions de données
tests/
docs/                # ADR et rapports d'évaluation datés
```

- Le cœur ne dépend pas de FastAPI : la couche HTTP se contente de décoder la requête, d'appeler le cœur et de convertir le résultat, pour que le contrat puisse changer sans toucher à la logique
- Les modèles se chargent une fois et restent en mémoire
- Pas de poids de modèle (`*.pt`, `*.onnx`), de `.venv/` ni de données d'entraînement en vrac dans Git

---

## API (à valider avec `server`)

- Requête : la photo et l'identifiant du parcours ; ni organe (sans gain de précision mesuré, JOURNAL 56), ni GPS
- Réponse : espèce (ou rien si abstention), confiance, alternatives classées, raison d'abstention (`low_confidence`, `unknown_species`, `no_subject_detected`), bounding box optionnelle (coordonnées normalisées, usage interne seulement, absente tant que le détecteur est désactivé)
- Abstention : la meilleure proposition reste disponible avec un avertissement discret, et la photo part à la file de modération
- Aucune extension de la liste du parcours : une espèce absente de la liste donne `unknown_species`
- Versioning `/v1/...`, erreurs au même format que le backend, dates ISO 8601 UTC

---

## Évaluation du modèle

Un changement de modèle ou de seuil se mesure, il ne se juge pas à l'œil.

- Les photos de test ne doivent pas avoir servi à entraîner le modèle : seules les photos téléversées après la date de coupure de ses données comptent (2024-06-01 pour BioCLIP 2) ; une photo plus ancienne est signalée comme « peut-être vue »
- Mesures : exactitude top-1 et top-3 par organe et par taille de liste, calibration de la confiance, comportement quand l'espèce n'est pas dans la liste, temps de réponse
- Chaque mesure produit un rapport daté dans `docs/eval/` (jamais écrasé) ; les chiffres cités viennent de ces rapports
- Seuils (abstention, reprise avec recadrage, plancher de similarité) : fixés par l'IA à partir de vraies photos de randonneur, puis proposés à l'équipe (à valider)
- Cible de temps de réponse : p95 inférieur à 5 s, mesuré sur machine au repos ; hors charge réseau
- Les photos et jeux de données externes passent par la vérification de licence (`DATASET_LICENSES.md`) avant usage

---

## Données et modèles

- Aucun réentraînement sur les prédictions du modèle lui-même : seulement sur des étiquettes confirmées par une personne (file de modération)
- Toute nouvelle source d'images ou de données est inscrite dans `DATASET_LICENSES.md` avec sa licence et l'usage permis
- Plantes seulement (animaux et champignons exclus), espèces protégées retirées des listes

---

## Tests

- **Cible : 60–70 % de couverture globale** (alignée sur le backend) ; mesurée à environ 87 % le 2026-11-05
- Tests unitaires sur la logique de décision, avec des faux détecteur et classifieur : les tests n'ont pas besoin des poids des modèles
- Nommage : `test_<fonction>_<scénario>`

```bash
task lint   # black, isort, ruff, mypy --strict, pytest --cov
task test
```

---

## Sécurité et vie privée

- Aucun secret dans le dépôt ; `.env` ignoré par Git, un `.env.example` documenté est maintenu
- Les photos des utilisateurs servent à répondre et à la modération ; aucune coordonnée GPS n'est demandée à l'IA (le traitement de l'EXIF relève de `server` et du mobile) — à valider

---

## CI — checks bloquants sur chaque PR

| Check | Outil |
|---|---|
| Formatage | `black --check`, `isort --check` |
| Lint | `ruff check` |
| Typage | `mypy --strict src/` |
| Tests | `pytest --ci` |
| Couverture < 60 % | `pytest --cov` (warning) |

La CI n'existe pas encore (tâche E2) : `task lint` lance localement les mêmes contrôles.

---

## Workflow de développement

- Une tâche = un ticket Linear = une branche = une PR
- Jamais de commit direct sur `main` ni sur `develop` : branche, puis PR vers `develop`, revue par au moins un autre membre
- Les décisions de structure (framework, bibliothèque, détecteur) ont un ADR dans `docs/adr/`
- Les décisions et mesures sont consignées au fil de l'eau dans `JOURNAL.md`, les questions pour l'équipe dans `TO_ASK.md`, les vérifications à faire dans `TO_CHECK.md`
