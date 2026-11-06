# Eval report — 2026-10-14 — hybrid-crop-experiment

- Photos: 16 (labels from file names)
- Candidate list: `data/species_lists/catalog.txt` (214 species)
- Confidence threshold for abstaining: 0.5 (placeholder)
- Device: cuda
- Labels are PlantNet suggestions given by the team, not expert-verified: treat the second word of each name as uncertain (genus-level is more reliable).

## Setting: catalog
True species on the candidate list for 4/16 (25%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 1/16 (6%) | 2/16 (12%) | 6/16 (38%) | 0.981 / 0.698 | 5 | 1/13 (8%) |
| full | 2/16 (12%) | 4/16 (25%) | 6/16 (38%) | 0.947 / 0.785 | 6 | 2/14 (14%) |
| hybrid>=2 | 2/16 (12%) | 3/16 (19%) | 7/16 (44%) | 0.982 / 0.761 | 5 | 2/14 (14%) |
| hybrid>=5 | 1/16 (6%) | 3/16 (19%) | 7/16 (44%) | 0.982 / 0.758 | 5 | 1/14 (7%) |
| hybrid>=10 | 2/16 (12%) | 4/16 (25%) | 7/16 (44%) | 0.947 / 0.814 | 7 | 2/14 (14%) |
| hybrid>=20 | 2/16 (12%) | 4/16 (25%) | 7/16 (44%) | 0.947 / 0.814 | 7 | 2/14 (14%) |
| hybrid>=40 | 2/16 (12%) | 4/16 (25%) | 6/16 (38%) | 0.947 / 0.794 | 6 | 2/14 (14%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 3 | 0 |
| 0.50-0.80 | 6 | 0 |
| 0.80-0.95 | 1 | 0 |
| 0.95-1.00 | 6 | 1 |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Castanea crenata → Castanea sativa ×2, Euonymus japonicus → Prunus laurocerasus ×2, Berberis soulieana → Salvia rosmarinus ×1, Carpinus betulus → Castanea sativa ×1, Cotoneaster dammeri → Ilex aquifolium ×1, Fraxinus angustifolia → Fraxinus ornus ×1, Ilex aquifolium → Castanea sativa ×1, Prunus avium → Juniperus phoenicea ×1
- full: Castanea crenata → Castanea sativa ×2, Euonymus japonicus → Prunus laurocerasus ×2, Berberis soulieana → Salvia rosmarinus ×1, Carpinus betulus → Ostrya carpinifolia ×1, Cotoneaster dammeri → Pistacia lentiscus ×1, Fraxinus angustifolia → Fraxinus excelsior ×1, Prunus avium → Betula pendula ×1, Prunus cerasus → Viburnum lantana ×1

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Berberis soulieana.JPEG | Berberis soulieana (not on list) |  | 98.4 | X Salvia rosmarinus 0.56 | X Salvia rosmarinus 0.58 |
| Carpinus betulus.JPEG | Carpinus betulus (not on list) |  | 6.6 | X Castanea sativa 0.53 | X Ostrya carpinifolia 0.97 |
| Castanea crenata(1).JPEG | Castanea crenata (not on list) |  | 1.2 | X Castanea sativa 0.97 | X Castanea sativa 1.00 |
| Castanea crenata.JPEG | Castanea crenata (not on list) |  | 86.5 | X Castanea sativa 1.00 | X Castanea sativa 1.00 |
| Cotoneaster dammeri.JPEG | Cotoneaster dammeri (not on list) |  | 0.5 | X Ilex aquifolium 0.56 | X Pistacia lentiscus 0.28 |
| Euonymys japonicus(1).JPEG | Euonymus japonicus (not on list) |  | 94.3 | X Prunus laurocerasus 0.99 | X Prunus laurocerasus 1.00 |
| Euonymys japonicus.JPEG | Euonymus japonicus (not on list) |  | 98.1 | X Prunus laurocerasus 1.00 | X Prunus laurocerasus 1.00 |
| Fraxinus angustifolia.JPEG | Fraxinus angustifolia |  | 5.2 | X Fraxinus ornus 0.58 | X Fraxinus excelsior 1.00 |
| Ilex aquifolium.JPEG | Ilex aquifolium |  | 1.1 | X Castanea sativa 0.34 | OK Ilex aquifolium 0.98 |
| Prunus avium.JPEG | Prunus avium (not on list) |  | 0.0 | X Juniperus phoenicea 0.61 | X Betula pendula 0.77 |
| Prunus cerasus.JPEG | Prunus cerasus (not on list) |  | 53.1 | X Viburnum lantana 0.79 | X Viburnum lantana 0.69 |
| Quercus robur(1).JPEG | Quercus robur |  | 2.7 | OK Quercus robur 0.98 | X Quercus pubescens 0.73 |
| Quercus robur.JPEG | Quercus robur |  | 9.6 | X Quercus pubescens 0.85 | OK Quercus robur 0.91 |
| Ribes nigrum.JPEG | Ribes nigrum (not on list) |  | 32.9 | X Ribes rubrum 0.95 | X Crataegus monogyna 0.68 |
| Symphoricarpos orbiculatus.JPEG | Symphoricarpos orbiculatus (not on list) |  | 98.0 | X Rubus fruticosus 0.46 | X Berberis aetnensis 0.42 |
| Trifolium fragiferum.JPEG | Trifolium fragiferum (not on list) |  | 1.3 | X Pteridium aquilinum 0.27 | X Medicago lupulina 0.89 |

## Setting: catalog+truth
True species on the candidate list for 16/16 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 4/16 (25%) | 7/16 (44%) | 9/16 (56%) | 0.987 / 0.645 | 4 | 4/11 (36%) |
| full | 6/16 (38%) | 13/16 (81%) | 11/16 (69%) | 0.974 / 0.75 | 3 | 6/15 (40%) |
| hybrid>=2 | 6/16 (38%) | 11/16 (69%) | 11/16 (69%) | 0.988 / 0.693 | 3 | 6/12 (50%) |
| hybrid>=5 | 5/16 (31%) | 11/16 (69%) | 11/16 (69%) | 0.989 / 0.696 | 3 | 5/12 (42%) |
| hybrid>=10 | 6/16 (38%) | 13/16 (81%) | 11/16 (69%) | 0.976 / 0.755 | 4 | 6/14 (43%) |
| hybrid>=20 | 6/16 (38%) | 13/16 (81%) | 11/16 (69%) | 0.976 / 0.755 | 4 | 6/14 (43%) |
| hybrid>=40 | 6/16 (38%) | 13/16 (81%) | 10/16 (62%) | 0.976 / 0.726 | 3 | 6/14 (43%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 5 | 0 |
| 0.50-0.80 | 2 | 0 |
| 0.80-0.95 | 4 | 0 |
| 0.95-1.00 | 5 | 4 |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Castanea crenata → Castanea sativa ×2, Berberis soulieana → Salvia rosmarinus ×1, Carpinus betulus → Castanea sativa ×1, Cotoneaster dammeri → Euonymus japonicus ×1, Fraxinus angustifolia → Fraxinus ornus ×1, Ilex aquifolium → Castanea crenata ×1, Prunus avium → Juniperus phoenicea ×1, Prunus cerasus → Viburnum lantana ×1
- full: Castanea crenata → Castanea sativa ×2, Berberis soulieana → Salvia rosmarinus ×1, Carpinus betulus → Ostrya carpinifolia ×1, Fraxinus angustifolia → Fraxinus excelsior ×1, Prunus avium → Carpinus betulus ×1, Prunus cerasus → Prunus avium ×1, Quercus robur → Quercus pubescens ×1, Ribes nigrum → Crataegus monogyna ×1

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Berberis soulieana.JPEG | Berberis soulieana |  | 98.4 | X Salvia rosmarinus 0.56 | X Salvia rosmarinus 0.57 |
| Carpinus betulus.JPEG | Carpinus betulus |  | 6.6 | X Castanea sativa 0.44 | X Ostrya carpinifolia 0.62 |
| Castanea crenata(1).JPEG | Castanea crenata |  | 1.2 | X Castanea sativa 0.95 | X Castanea sativa 1.00 |
| Castanea crenata.JPEG | Castanea crenata |  | 86.5 | X Castanea sativa 1.00 | X Castanea sativa 1.00 |
| Cotoneaster dammeri.JPEG | Cotoneaster dammeri |  | 0.5 | X Euonymus japonicus 0.92 | OK Cotoneaster dammeri 1.00 |
| Euonymys japonicus(1).JPEG | Euonymus japonicus |  | 94.3 | OK Euonymus japonicus 0.98 | OK Euonymus japonicus 0.99 |
| Euonymys japonicus.JPEG | Euonymus japonicus |  | 98.1 | OK Euonymus japonicus 0.98 | OK Euonymus japonicus 0.97 |
| Fraxinus angustifolia.JPEG | Fraxinus angustifolia |  | 5.2 | X Fraxinus ornus 0.44 | X Fraxinus excelsior 1.00 |
| Ilex aquifolium.JPEG | Ilex aquifolium |  | 1.1 | X Castanea crenata 0.39 | OK Ilex aquifolium 0.98 |
| Prunus avium.JPEG | Prunus avium |  | 0.0 | X Juniperus phoenicea 0.55 | X Carpinus betulus 0.37 |
| Prunus cerasus.JPEG | Prunus cerasus |  | 53.1 | X Viburnum lantana 0.48 | X Prunus avium 0.72 |
| Quercus robur(1).JPEG | Quercus robur |  | 2.7 | OK Quercus robur 0.98 | X Quercus pubescens 0.73 |
| Quercus robur.JPEG | Quercus robur |  | 9.6 | X Quercus pubescens 0.85 | OK Quercus robur 0.91 |
| Ribes nigrum.JPEG | Ribes nigrum |  | 32.9 | X Ribes rubrum 0.92 | X Crataegus monogyna 0.62 |
| Symphoricarpos orbiculatus.JPEG | Symphoricarpos orbiculatus |  | 98.0 | OK Symphoricarpos orbiculatus 1.00 | OK Symphoricarpos orbiculatus 1.00 |
| Trifolium fragiferum.JPEG | Trifolium fragiferum |  | 1.3 | X Pteridium aquilinum 0.25 | X Medicago lupulina 0.88 |

## Compared with the previous report (2026-10-14, local-protection-catalog)
- catalog / crop: top-1 1/16 → 1/16
- catalog / full: top-1 2/16 → 2/16
- catalog+truth / crop: top-1 4/16 → 4/16
- catalog+truth / full: top-1 6/16 → 6/16
