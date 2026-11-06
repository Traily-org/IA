# Eval report — 2026-10-14 — first-16-photos

- Photos: 16 (labels from file names)
- Candidate list: `data/species_lists/catalog.txt` (190 species)
- Confidence threshold for abstaining: 0.5 (placeholder)
- Device: cuda
- Labels are PlantNet suggestions given by the team, not expert-verified: treat the second word of each name as uncertain (genus-level is more reliable).

## Setting: catalog
True species on the candidate list for 3/16 (19%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 2/16 (12%) | 2/16 (12%) | 5/16 (31%) | 0.991 / 0.737 | 5 | 2/14 (14%) |
| full | 3/16 (19%) | 3/16 (19%) | 7/16 (44%) | 0.992 / 0.869 | 10 | 3/15 (20%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 2 | 0 |
| 0.50-0.80 | 6 | 0 |
| 0.80-0.95 | 1 | 0 |
| 0.95-1.00 | 7 | 2 |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Castanea crenata → Castanea sativa ×2, Euonymus japonicus → Prunus laurocerasus ×2, Berberis soulieana → Salvia rosmarinus ×1, Carpinus betulus → Castanea sativa ×1, Cotoneaster dammeri → Ilex aquifolium ×1, Fraxinus angustifolia → Fraxinus ornus ×1, Ilex aquifolium → Castanea sativa ×1, Prunus avium → Juniperus phoenicea ×1
- full: Castanea crenata → Castanea sativa ×2, Euonymus japonicus → Prunus laurocerasus ×2, Berberis soulieana → Salvia rosmarinus ×1, Carpinus betulus → Ostrya carpinifolia ×1, Cotoneaster dammeri → Pistacia lentiscus ×1, Fraxinus angustifolia → Fraxinus excelsior ×1, Prunus avium → Betula pendula ×1, Prunus cerasus → Viburnum lantana ×1

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Berberis soulieana.JPEG | Berberis soulieana (not on list) |  | 98.4 | X Salvia rosmarinus 0.57 | X Salvia rosmarinus 0.58 |
| Carpinus betulus.JPEG | Carpinus betulus (not on list) |  | 6.6 | X Castanea sativa 0.67 | X Ostrya carpinifolia 1.00 |
| Castanea crenata(1).JPEG | Castanea crenata (not on list) |  | 1.2 | X Castanea sativa 0.97 | X Castanea sativa 1.00 |
| Castanea crenata.JPEG | Castanea crenata (not on list) |  | 86.5 | X Castanea sativa 1.00 | X Castanea sativa 1.00 |
| Cotoneaster dammeri.JPEG | Cotoneaster dammeri (not on list) |  | 0.5 | X Ilex aquifolium 0.57 | X Pistacia lentiscus 0.31 |
| Euonymys japonicus(1).JPEG | Euonymus japonicus (not on list) |  | 94.3 | X Prunus laurocerasus 1.00 | X Prunus laurocerasus 1.00 |
| Euonymys japonicus.JPEG | Euonymus japonicus (not on list) |  | 98.1 | X Prunus laurocerasus 1.00 | X Prunus laurocerasus 1.00 |
| Fraxinus angustifolia.JPEG | Fraxinus angustifolia (not on list) |  | 5.2 | X Fraxinus ornus 0.59 | X Fraxinus excelsior 1.00 |
| Ilex aquifolium.JPEG | Ilex aquifolium |  | 1.1 | X Castanea sativa 0.43 | OK Ilex aquifolium 0.98 |
| Prunus avium.JPEG | Prunus avium (not on list) |  | 0.0 | X Juniperus phoenicea 0.70 | X Betula pendula 0.94 |
| Prunus cerasus.JPEG | Prunus cerasus (not on list) |  | 53.1 | X Viburnum lantana 0.84 | X Viburnum lantana 0.94 |
| Quercus robur(1).JPEG | Quercus robur |  | 2.7 | OK Quercus robur 0.98 | OK Quercus robur 0.99 |
| Quercus robur.JPEG | Quercus robur |  | 9.6 | OK Quercus robur 1.00 | OK Quercus robur 1.00 |
| Ribes nigrum.JPEG | Ribes nigrum (not on list) |  | 32.9 | X Acer pseudoplatanus 0.66 | X Crataegus monogyna 0.92 |
| Symphoricarpos orbiculatus.JPEG | Symphoricarpos orbiculatus (not on list) |  | 98.0 | X Lonicera xylosteum 0.96 | X Lonicera xylosteum 0.97 |
| Trifolium fragiferum.JPEG | Trifolium fragiferum (not on list) |  | 1.3 | X Pteridium aquilinum 0.35 | X Trifolium pratense 0.65 |

## Setting: catalog+truth
True species on the candidate list for 16/16 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 6/16 (38%) | 8/16 (50%) | 9/16 (56%) | 0.898 / 0.629 | 3 | 5/11 (45%) |
| full | 7/16 (44%) | 13/16 (81%) | 12/16 (75%) | 0.99 / 0.759 | 3 | 7/15 (47%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 5 | 1 |
| 0.50-0.80 | 3 | 0 |
| 0.80-0.95 | 1 | 0 |
| 0.95-1.00 | 7 | 5 |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Castanea crenata → Castanea sativa ×2, Berberis soulieana → Salvia rosmarinus ×1, Carpinus betulus → Castanea sativa ×1, Cotoneaster dammeri → Euonymus japonicus ×1, Fraxinus angustifolia → Fraxinus ornus ×1, Ilex aquifolium → Castanea crenata ×1, Prunus avium → Juniperus phoenicea ×1, Prunus cerasus → Viburnum lantana ×1
- full: Castanea crenata → Castanea sativa ×2, Berberis soulieana → Salvia rosmarinus ×1, Carpinus betulus → Ostrya carpinifolia ×1, Fraxinus angustifolia → Fraxinus excelsior ×1, Prunus avium → Carpinus betulus ×1, Prunus cerasus → Prunus avium ×1, Ribes nigrum → Crataegus monogyna ×1, Trifolium fragiferum → Trifolium pratense ×1

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Berberis soulieana.JPEG | Berberis soulieana |  | 98.4 | X Salvia rosmarinus 0.57 | X Salvia rosmarinus 0.58 |
| Carpinus betulus.JPEG | Carpinus betulus |  | 6.6 | X Castanea sativa 0.53 | X Ostrya carpinifolia 0.63 |
| Castanea crenata(1).JPEG | Castanea crenata |  | 1.2 | X Castanea sativa 0.95 | X Castanea sativa 1.00 |
| Castanea crenata.JPEG | Castanea crenata |  | 86.5 | X Castanea sativa 1.00 | X Castanea sativa 1.00 |
| Cotoneaster dammeri.JPEG | Cotoneaster dammeri |  | 0.5 | X Euonymus japonicus 0.92 | OK Cotoneaster dammeri 1.00 |
| Euonymys japonicus(1).JPEG | Euonymus japonicus |  | 94.3 | OK Euonymus japonicus 0.98 | OK Euonymus japonicus 0.99 |
| Euonymys japonicus.JPEG | Euonymus japonicus |  | 98.1 | OK Euonymus japonicus 0.98 | OK Euonymus japonicus 0.97 |
| Fraxinus angustifolia.JPEG | Fraxinus angustifolia |  | 5.2 | X Fraxinus ornus 0.45 | X Fraxinus excelsior 1.00 |
| Ilex aquifolium.JPEG | Ilex aquifolium |  | 1.1 | X Castanea crenata 0.44 | OK Ilex aquifolium 0.98 |
| Prunus avium.JPEG | Prunus avium |  | 0.0 | X Juniperus phoenicea 0.62 | X Carpinus betulus 0.40 |
| Prunus cerasus.JPEG | Prunus cerasus |  | 53.1 | X Viburnum lantana 0.49 | X Prunus avium 0.77 |
| Quercus robur(1).JPEG | Quercus robur |  | 2.7 | OK Quercus robur 0.98 | OK Quercus robur 0.99 |
| Quercus robur.JPEG | Quercus robur |  | 9.6 | OK Quercus robur 1.00 | OK Quercus robur 1.00 |
| Ribes nigrum.JPEG | Ribes nigrum |  | 32.9 | OK Ribes nigrum 0.44 | X Crataegus monogyna 0.82 |
| Symphoricarpos orbiculatus.JPEG | Symphoricarpos orbiculatus |  | 98.0 | OK Symphoricarpos orbiculatus 1.00 | OK Symphoricarpos orbiculatus 1.00 |
| Trifolium fragiferum.JPEG | Trifolium fragiferum |  | 1.3 | X Pteridium aquilinum 0.32 | X Trifolium pratense 0.63 |

No previous report to compare with.
