# Eval report — 2026-10-30 — plantnet-bark-trees

- Photos: 70 (labels from labels.csv)
- Candidate list: `data/species_lists/catalog.txt` (214 species)
- Confidence threshold for abstaining: 0.5 (placeholder)
- Device: cuda
- Labels are PlantNet suggestions given by the team, not expert-verified: treat the second word of each name as uncertain (genus-level is more reliable).

## Setting: catalog
True species on the candidate list for 70/70 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 1/70 (1%) | 6/70 (9%) | 1/70 (1%) | 0.907 / 0.46 | 1 | 1/11 (9%) |
| full | 35/70 (50%) | 47/70 (67%) | 38/70 (54%) | 0.792 / 0.531 | 3 | 33/51 (65%) |
| hybrid>=2 | 25/70 (36%) | 41/70 (59%) | 28/70 (40%) | 0.779 / 0.515 | 3 | 24/46 (52%) |
| hybrid>=5 | 29/70 (41%) | 45/70 (64%) | 32/70 (46%) | 0.787 / 0.519 | 3 | 28/49 (57%) |
| hybrid>=10 | 29/70 (41%) | 45/70 (64%) | 32/70 (46%) | 0.787 / 0.526 | 3 | 28/50 (56%) |
| hybrid>=20 | 33/70 (47%) | 45/70 (64%) | 36/70 (51%) | 0.812 / 0.513 | 3 | 32/50 (64%) |
| hybrid>=40 | 34/70 (49%) | 47/70 (67%) | 37/70 (53%) | 0.802 / 0.526 | 3 | 33/51 (65%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 12 | 0 |
| 0.50-0.80 | 8 | 0 |
| 0.80-0.95 | 3 | 1 |
| 0.95-1.00 | 0 | 0 |

Could BioCLIP have seen these photos? Split by iNaturalist upload date (cutoff 2024-01-01: its training data predates Nov 2023):

| subset | photos | full top-1 | full top-3 | crop top-1 | crop top-3 |
|---|---|---|---|---|---|
| uploaded on/after 2024-01-01 (cannot be in training data) | 70 | 35/70 (50%) | 47/70 (67%) | 1/70 (1%) | 6/70 (9%) |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Abies alba → Bellis perennis ×1, Acacia dealbata → Cytisus scoparius ×1, Alnus alnobetula → Trifolium repens ×1, Alnus alnobetula → Betula pendula ×1, Buxus sempervirens → Bellis perennis ×1, Castanea sativa → Arabidopsis thaliana ×1, Cornus sanguinea → Gentiana lutea ×1, Corylus avellana → Viburnum lantana ×1
- full: Abies alba → Acer pseudoplatanus ×2, Alnus alnobetula → Quercus robur ×1, Castanea sativa → Quercus petraea ×1, Castanea sativa → Cornus mas ×1, Corylus avellana → Fraxinus excelsior ×1, Crataegus monogyna → Sorbus aucuparia ×1, Crataegus monogyna → Anthoxanthum odoratum ×1, Fagus sylvatica → Ostrya carpinifolia ×1

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Abies_alba_bark_1.jpg | Abies alba | bark | 0.8 | X Bellis perennis 0.60 | X Acer pseudoplatanus 0.22 |
| Abies_alba_bark_2.jpg | Abies alba | bark | 0.0 | - | X Acer pseudoplatanus 0.88 |
| Acacia_dealbata_bark_1.jpg | Acacia dealbata | bark | 18.5 | X Cytisus scoparius 0.59 | OK Acacia dealbata 1.00 |
| Acacia_dealbata_bark_2.jpg | Acacia dealbata | bark | 0.0 | - | OK Acacia dealbata 0.85 |
| Acer_pseudoplatanus_bark_1.jpg | Acer pseudoplatanus | bark | 0.0 | - | OK Acer pseudoplatanus 0.54 |
| Acer_pseudoplatanus_bark_2.jpg | Acer pseudoplatanus | bark | 0.0 | - | OK Acer pseudoplatanus 0.99 |
| Alnus_alnobetula_bark_1.jpg | Alnus alnobetula | bark | 0.9 | X Trifolium repens 0.94 | X Quercus robur 0.65 |
| Alnus_alnobetula_bark_2.jpg | Alnus alnobetula | bark | 13.7 | X Betula pendula 0.58 | OK Alnus alnobetula 1.00 |
| Betula_pendula_bark_1.jpg | Betula pendula | bark | 0.0 | - | OK Betula pendula 0.84 |
| Betula_pendula_bark_2.jpg | Betula pendula | bark | 0.0 | - | OK Betula pendula 1.00 |
| Buxus_sempervirens_bark_1.jpg | Buxus sempervirens | bark | 0.0 | - | OK Buxus sempervirens 0.39 |
| Buxus_sempervirens_bark_2.jpg | Buxus sempervirens | bark | 2.3 | X Bellis perennis 0.71 | OK Buxus sempervirens 0.97 |
| Castanea_sativa_bark_1.jpg | Castanea sativa | bark | 0.0 | - | X Quercus petraea 0.58 |
| Castanea_sativa_bark_2.jpg | Castanea sativa | bark | 1.6 | X Arabidopsis thaliana 0.79 | X Cornus mas 0.74 |
| Cornus_mas_bark_1.jpg | Cornus mas | bark | 0.0 | - | OK Cornus mas 0.97 |
| Cornus_mas_bark_2.jpg | Cornus mas | bark | 0.0 | - | OK Cornus mas 0.77 |
| Cornus_sanguinea_bark_1.jpg | Cornus sanguinea | bark | 28.8 | X Gentiana lutea 0.15 | OK Cornus sanguinea 0.56 |
| Cornus_sanguinea_bark_2.jpg | Cornus sanguinea | bark | 0.0 | - | OK Cornus sanguinea 1.00 |
| Corylus_avellana_bark_1.jpg | Corylus avellana | bark | 0.0 | - | X Fraxinus excelsior 0.39 |
| Corylus_avellana_bark_2.jpg | Corylus avellana | bark | 22.0 | X Viburnum lantana 0.59 | OK Corylus avellana 0.81 |
| Crataegus_monogyna_bark_1.jpg | Crataegus monogyna | bark | 0.0 | - | X Sorbus aucuparia 0.56 |
| Crataegus_monogyna_bark_2.jpg | Crataegus monogyna | bark | 1.5 | X Silybum marianum 0.23 | X Anthoxanthum odoratum 0.15 |
| Fagus_sylvatica_bark_1.jpg | Fagus sylvatica | bark | 0.0 | - | X Ostrya carpinifolia 0.32 |
| Fagus_sylvatica_bark_2.jpg | Fagus sylvatica | bark | 0.0 | - | OK Fagus sylvatica 0.63 |
| Fraxinus_angustifolia_bark_1.jpg | Fraxinus angustifolia | bark | 0.0 | - | X Ligustrum vulgare 0.22 |
| Fraxinus_angustifolia_bark_2.jpg | Fraxinus angustifolia | bark | 0.0 | - | X Cornus mas 0.77 |
| Fraxinus_excelsior_bark_1.jpg | Fraxinus excelsior | bark | 0.0 | - | OK Fraxinus excelsior 0.98 |
| Fraxinus_excelsior_bark_2.jpg | Fraxinus excelsior | bark | 0.0 | - | X Acacia dealbata 0.97 |
| Fraxinus_ornus_bark_1.jpg | Fraxinus ornus | bark | 0.0 | - | X Crataegus monogyna 0.62 |
| Fraxinus_ornus_bark_2.jpg | Fraxinus ornus | bark | 0.0 | - | X Ilex aquifolium 0.56 |
| Ilex_aquifolium_bark_1.jpg | Ilex aquifolium | bark | 1.4 | X Bellis perennis 0.57 | OK Ilex aquifolium 0.61 |
| Ilex_aquifolium_bark_2.jpg | Ilex aquifolium | bark | 0.0 | - | X Betula pendula 0.46 |
| Juniperus_communis_bark_1.jpg | Juniperus communis | bark | 0.0 | - | OK Juniperus communis 0.73 |
| Juniperus_communis_bark_2.jpg | Juniperus communis | bark | 1.1 | X Pteridium aquilinum 0.15 | OK Juniperus communis 1.00 |
| Juniperus_oxycedrus_bark_1.jpg | Juniperus oxycedrus | bark | 0.0 | - | X Buxus sempervirens 0.61 |
| Juniperus_oxycedrus_bark_2.jpg | Juniperus oxycedrus | bark | 0.0 | - | OK Juniperus oxycedrus 0.53 |
| Juniperus_phoenicea_bark_1.jpg | Juniperus phoenicea | bark | 37.1 | OK Juniperus phoenicea 0.91 | X Genista salzmannii 0.70 |
| Juniperus_phoenicea_bark_2.jpg | Juniperus phoenicea | bark | 0.0 | - | OK Juniperus phoenicea 0.78 |
| Ligustrum_vulgare_bark_1.jpg | Ligustrum vulgare | bark | 0.0 | - | OK Ligustrum vulgare 0.99 |
| Ligustrum_vulgare_bark_2.jpg | Ligustrum vulgare | bark | 18.6 | X Senecio ovatus 0.86 | OK Ligustrum vulgare 0.99 |
| Ostrya_carpinifolia_bark_1.jpg | Ostrya carpinifolia | bark | 0.0 | - | X Castanea sativa 0.47 |
| Ostrya_carpinifolia_bark_2.jpg | Ostrya carpinifolia | bark | 0.0 | - | X Sorbus aucuparia 0.35 |
| Phillyrea_latifolia_bark_1.jpg | Phillyrea latifolia | bark | 0.3 | X Bellis perennis 0.23 | X Ilex aquifolium 0.35 |
| Phillyrea_latifolia_bark_2.jpg | Phillyrea latifolia | bark | 0.4 | X Plantago coronopus 0.28 | X Fraxinus angustifolia 0.46 |
| Pinus_nigra_bark_1.jpg | Pinus nigra | bark | 0.0 | - | X Cornus mas 0.46 |
| Pinus_nigra_bark_2.jpg | Pinus nigra | bark | 0.0 | - | X Pinus sylvestris 0.47 |
| Pinus_pinaster_bark_1.jpg | Pinus pinaster | bark | 0.0 | - | X Pinus sylvestris 0.92 |
| Pinus_pinaster_bark_2.jpg | Pinus pinaster | bark | 0.0 | - | X Castanea sativa 0.95 |
| Pinus_sylvestris_bark_1.jpg | Pinus sylvestris | bark | 0.0 | - | X Crataegus monogyna 0.60 |
| Pinus_sylvestris_bark_2.jpg | Pinus sylvestris | bark | 0.0 | - | X Juniperus phoenicea 0.56 |
| Pistacia_lentiscus_bark_1.jpg | Pistacia lentiscus | bark | 8.8 | X Trifolium repens 0.21 | X Cornus mas 0.54 |
| Pistacia_lentiscus_bark_2.jpg | Pistacia lentiscus | bark | 2.6 | X Acer pseudoplatanus 0.37 | OK Pistacia lentiscus 0.93 |
| Prunus_laurocerasus_bark_1.jpg | Prunus laurocerasus | bark | 97.9 | X Quercus robur 0.36 | OK Prunus laurocerasus 0.44 |
| Prunus_laurocerasus_bark_2.jpg | Prunus laurocerasus | bark | 17.5 | X Bupleurum fruticosum 0.56 | OK Prunus laurocerasus 0.98 |
| Prunus_spinosa_bark_1.jpg | Prunus spinosa | bark | 0.0 | - | X Cornus mas 0.88 |
| Prunus_spinosa_bark_2.jpg | Prunus spinosa | bark | 0.0 | - | OK Prunus spinosa 0.58 |
| Quercus_coccifera_bark_1.jpg | Quercus coccifera | bark | 0.0 | - | X Crataegus monogyna 0.34 |
| Quercus_coccifera_bark_2.jpg | Quercus coccifera | bark | 4.3 | X Trifolium repens 0.37 | OK Quercus coccifera 0.50 |
| Quercus_ilex_bark_1.jpg | Quercus ilex | bark | 4.9 | X Acacia dealbata 0.47 | OK Quercus ilex 0.95 |
| Quercus_ilex_bark_2.jpg | Quercus ilex | bark | 0.0 | - | OK Quercus ilex 0.57 |
| Quercus_petraea_bark_1.jpg | Quercus petraea | bark | 1.3 | X Pteridium aquilinum 0.16 | X Cornus mas 0.37 |
| Quercus_petraea_bark_2.jpg | Quercus petraea | bark | 0.0 | - | OK Quercus petraea 0.96 |
| Quercus_pubescens_bark_1.jpg | Quercus pubescens | bark | 0.0 | - | X Pinus nigra 0.22 |
| Quercus_pubescens_bark_2.jpg | Quercus pubescens | bark | 0.0 | - | X Acacia dealbata 0.37 |
| Quercus_robur_bark_1.jpg | Quercus robur | bark | 0.0 | - | X Quercus ilex 0.54 |
| Quercus_robur_bark_2.jpg | Quercus robur | bark | 0.0 | - | X Crataegus monogyna 0.29 |
| Sorbus_aucuparia_bark_1.jpg | Sorbus aucuparia | bark | 0.0 | - | OK Sorbus aucuparia 0.90 |
| Sorbus_aucuparia_bark_2.jpg | Sorbus aucuparia | bark | 0.0 | - | OK Sorbus aucuparia 0.82 |
| Viburnum_lantana_bark_1.jpg | Viburnum lantana | bark | 0.0 | - | OK Viburnum lantana 0.52 |
| Viburnum_lantana_bark_2.jpg | Viburnum lantana | bark | 0.3 | X Arabidopsis thaliana 0.33 | OK Viburnum lantana 0.64 |

## Setting: catalog+truth
True species on the candidate list for 70/70 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 1/70 (1%) | 6/70 (9%) | 1/70 (1%) | 0.907 / 0.46 | 1 | 1/11 (9%) |
| full | 35/70 (50%) | 47/70 (67%) | 38/70 (54%) | 0.792 / 0.531 | 3 | 33/51 (65%) |
| hybrid>=2 | 25/70 (36%) | 41/70 (59%) | 28/70 (40%) | 0.779 / 0.515 | 3 | 24/46 (52%) |
| hybrid>=5 | 29/70 (41%) | 45/70 (64%) | 32/70 (46%) | 0.787 / 0.519 | 3 | 28/49 (57%) |
| hybrid>=10 | 29/70 (41%) | 45/70 (64%) | 32/70 (46%) | 0.787 / 0.526 | 3 | 28/50 (56%) |
| hybrid>=20 | 33/70 (47%) | 45/70 (64%) | 36/70 (51%) | 0.812 / 0.513 | 3 | 32/50 (64%) |
| hybrid>=40 | 34/70 (49%) | 47/70 (67%) | 37/70 (53%) | 0.802 / 0.526 | 3 | 33/51 (65%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 12 | 0 |
| 0.50-0.80 | 8 | 0 |
| 0.80-0.95 | 3 | 1 |
| 0.95-1.00 | 0 | 0 |

Could BioCLIP have seen these photos? Split by iNaturalist upload date (cutoff 2024-01-01: its training data predates Nov 2023):

| subset | photos | full top-1 | full top-3 | crop top-1 | crop top-3 |
|---|---|---|---|---|---|
| uploaded on/after 2024-01-01 (cannot be in training data) | 70 | 35/70 (50%) | 47/70 (67%) | 1/70 (1%) | 6/70 (9%) |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Abies alba → Bellis perennis ×1, Acacia dealbata → Cytisus scoparius ×1, Alnus alnobetula → Trifolium repens ×1, Alnus alnobetula → Betula pendula ×1, Buxus sempervirens → Bellis perennis ×1, Castanea sativa → Arabidopsis thaliana ×1, Cornus sanguinea → Gentiana lutea ×1, Corylus avellana → Viburnum lantana ×1
- full: Abies alba → Acer pseudoplatanus ×2, Alnus alnobetula → Quercus robur ×1, Castanea sativa → Quercus petraea ×1, Castanea sativa → Cornus mas ×1, Corylus avellana → Fraxinus excelsior ×1, Crataegus monogyna → Sorbus aucuparia ×1, Crataegus monogyna → Anthoxanthum odoratum ×1, Fagus sylvatica → Ostrya carpinifolia ×1

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Abies_alba_bark_1.jpg | Abies alba | bark | 0.8 | X Bellis perennis 0.60 | X Acer pseudoplatanus 0.22 |
| Abies_alba_bark_2.jpg | Abies alba | bark | 0.0 | - | X Acer pseudoplatanus 0.88 |
| Acacia_dealbata_bark_1.jpg | Acacia dealbata | bark | 18.5 | X Cytisus scoparius 0.59 | OK Acacia dealbata 1.00 |
| Acacia_dealbata_bark_2.jpg | Acacia dealbata | bark | 0.0 | - | OK Acacia dealbata 0.85 |
| Acer_pseudoplatanus_bark_1.jpg | Acer pseudoplatanus | bark | 0.0 | - | OK Acer pseudoplatanus 0.54 |
| Acer_pseudoplatanus_bark_2.jpg | Acer pseudoplatanus | bark | 0.0 | - | OK Acer pseudoplatanus 0.99 |
| Alnus_alnobetula_bark_1.jpg | Alnus alnobetula | bark | 0.9 | X Trifolium repens 0.94 | X Quercus robur 0.65 |
| Alnus_alnobetula_bark_2.jpg | Alnus alnobetula | bark | 13.7 | X Betula pendula 0.58 | OK Alnus alnobetula 1.00 |
| Betula_pendula_bark_1.jpg | Betula pendula | bark | 0.0 | - | OK Betula pendula 0.84 |
| Betula_pendula_bark_2.jpg | Betula pendula | bark | 0.0 | - | OK Betula pendula 1.00 |
| Buxus_sempervirens_bark_1.jpg | Buxus sempervirens | bark | 0.0 | - | OK Buxus sempervirens 0.39 |
| Buxus_sempervirens_bark_2.jpg | Buxus sempervirens | bark | 2.3 | X Bellis perennis 0.71 | OK Buxus sempervirens 0.97 |
| Castanea_sativa_bark_1.jpg | Castanea sativa | bark | 0.0 | - | X Quercus petraea 0.58 |
| Castanea_sativa_bark_2.jpg | Castanea sativa | bark | 1.6 | X Arabidopsis thaliana 0.79 | X Cornus mas 0.74 |
| Cornus_mas_bark_1.jpg | Cornus mas | bark | 0.0 | - | OK Cornus mas 0.97 |
| Cornus_mas_bark_2.jpg | Cornus mas | bark | 0.0 | - | OK Cornus mas 0.77 |
| Cornus_sanguinea_bark_1.jpg | Cornus sanguinea | bark | 28.8 | X Gentiana lutea 0.15 | OK Cornus sanguinea 0.56 |
| Cornus_sanguinea_bark_2.jpg | Cornus sanguinea | bark | 0.0 | - | OK Cornus sanguinea 1.00 |
| Corylus_avellana_bark_1.jpg | Corylus avellana | bark | 0.0 | - | X Fraxinus excelsior 0.39 |
| Corylus_avellana_bark_2.jpg | Corylus avellana | bark | 22.0 | X Viburnum lantana 0.59 | OK Corylus avellana 0.81 |
| Crataegus_monogyna_bark_1.jpg | Crataegus monogyna | bark | 0.0 | - | X Sorbus aucuparia 0.56 |
| Crataegus_monogyna_bark_2.jpg | Crataegus monogyna | bark | 1.5 | X Silybum marianum 0.23 | X Anthoxanthum odoratum 0.15 |
| Fagus_sylvatica_bark_1.jpg | Fagus sylvatica | bark | 0.0 | - | X Ostrya carpinifolia 0.32 |
| Fagus_sylvatica_bark_2.jpg | Fagus sylvatica | bark | 0.0 | - | OK Fagus sylvatica 0.63 |
| Fraxinus_angustifolia_bark_1.jpg | Fraxinus angustifolia | bark | 0.0 | - | X Ligustrum vulgare 0.22 |
| Fraxinus_angustifolia_bark_2.jpg | Fraxinus angustifolia | bark | 0.0 | - | X Cornus mas 0.77 |
| Fraxinus_excelsior_bark_1.jpg | Fraxinus excelsior | bark | 0.0 | - | OK Fraxinus excelsior 0.98 |
| Fraxinus_excelsior_bark_2.jpg | Fraxinus excelsior | bark | 0.0 | - | X Acacia dealbata 0.97 |
| Fraxinus_ornus_bark_1.jpg | Fraxinus ornus | bark | 0.0 | - | X Crataegus monogyna 0.62 |
| Fraxinus_ornus_bark_2.jpg | Fraxinus ornus | bark | 0.0 | - | X Ilex aquifolium 0.56 |
| Ilex_aquifolium_bark_1.jpg | Ilex aquifolium | bark | 1.4 | X Bellis perennis 0.57 | OK Ilex aquifolium 0.61 |
| Ilex_aquifolium_bark_2.jpg | Ilex aquifolium | bark | 0.0 | - | X Betula pendula 0.46 |
| Juniperus_communis_bark_1.jpg | Juniperus communis | bark | 0.0 | - | OK Juniperus communis 0.73 |
| Juniperus_communis_bark_2.jpg | Juniperus communis | bark | 1.1 | X Pteridium aquilinum 0.15 | OK Juniperus communis 1.00 |
| Juniperus_oxycedrus_bark_1.jpg | Juniperus oxycedrus | bark | 0.0 | - | X Buxus sempervirens 0.61 |
| Juniperus_oxycedrus_bark_2.jpg | Juniperus oxycedrus | bark | 0.0 | - | OK Juniperus oxycedrus 0.53 |
| Juniperus_phoenicea_bark_1.jpg | Juniperus phoenicea | bark | 37.1 | OK Juniperus phoenicea 0.91 | X Genista salzmannii 0.70 |
| Juniperus_phoenicea_bark_2.jpg | Juniperus phoenicea | bark | 0.0 | - | OK Juniperus phoenicea 0.78 |
| Ligustrum_vulgare_bark_1.jpg | Ligustrum vulgare | bark | 0.0 | - | OK Ligustrum vulgare 0.99 |
| Ligustrum_vulgare_bark_2.jpg | Ligustrum vulgare | bark | 18.6 | X Senecio ovatus 0.86 | OK Ligustrum vulgare 0.99 |
| Ostrya_carpinifolia_bark_1.jpg | Ostrya carpinifolia | bark | 0.0 | - | X Castanea sativa 0.47 |
| Ostrya_carpinifolia_bark_2.jpg | Ostrya carpinifolia | bark | 0.0 | - | X Sorbus aucuparia 0.35 |
| Phillyrea_latifolia_bark_1.jpg | Phillyrea latifolia | bark | 0.3 | X Bellis perennis 0.23 | X Ilex aquifolium 0.35 |
| Phillyrea_latifolia_bark_2.jpg | Phillyrea latifolia | bark | 0.4 | X Plantago coronopus 0.28 | X Fraxinus angustifolia 0.46 |
| Pinus_nigra_bark_1.jpg | Pinus nigra | bark | 0.0 | - | X Cornus mas 0.46 |
| Pinus_nigra_bark_2.jpg | Pinus nigra | bark | 0.0 | - | X Pinus sylvestris 0.47 |
| Pinus_pinaster_bark_1.jpg | Pinus pinaster | bark | 0.0 | - | X Pinus sylvestris 0.92 |
| Pinus_pinaster_bark_2.jpg | Pinus pinaster | bark | 0.0 | - | X Castanea sativa 0.95 |
| Pinus_sylvestris_bark_1.jpg | Pinus sylvestris | bark | 0.0 | - | X Crataegus monogyna 0.60 |
| Pinus_sylvestris_bark_2.jpg | Pinus sylvestris | bark | 0.0 | - | X Juniperus phoenicea 0.56 |
| Pistacia_lentiscus_bark_1.jpg | Pistacia lentiscus | bark | 8.8 | X Trifolium repens 0.21 | X Cornus mas 0.54 |
| Pistacia_lentiscus_bark_2.jpg | Pistacia lentiscus | bark | 2.6 | X Acer pseudoplatanus 0.37 | OK Pistacia lentiscus 0.93 |
| Prunus_laurocerasus_bark_1.jpg | Prunus laurocerasus | bark | 97.9 | X Quercus robur 0.36 | OK Prunus laurocerasus 0.44 |
| Prunus_laurocerasus_bark_2.jpg | Prunus laurocerasus | bark | 17.5 | X Bupleurum fruticosum 0.56 | OK Prunus laurocerasus 0.98 |
| Prunus_spinosa_bark_1.jpg | Prunus spinosa | bark | 0.0 | - | X Cornus mas 0.88 |
| Prunus_spinosa_bark_2.jpg | Prunus spinosa | bark | 0.0 | - | OK Prunus spinosa 0.58 |
| Quercus_coccifera_bark_1.jpg | Quercus coccifera | bark | 0.0 | - | X Crataegus monogyna 0.34 |
| Quercus_coccifera_bark_2.jpg | Quercus coccifera | bark | 4.3 | X Trifolium repens 0.37 | OK Quercus coccifera 0.50 |
| Quercus_ilex_bark_1.jpg | Quercus ilex | bark | 4.9 | X Acacia dealbata 0.47 | OK Quercus ilex 0.95 |
| Quercus_ilex_bark_2.jpg | Quercus ilex | bark | 0.0 | - | OK Quercus ilex 0.57 |
| Quercus_petraea_bark_1.jpg | Quercus petraea | bark | 1.3 | X Pteridium aquilinum 0.16 | X Cornus mas 0.37 |
| Quercus_petraea_bark_2.jpg | Quercus petraea | bark | 0.0 | - | OK Quercus petraea 0.96 |
| Quercus_pubescens_bark_1.jpg | Quercus pubescens | bark | 0.0 | - | X Pinus nigra 0.22 |
| Quercus_pubescens_bark_2.jpg | Quercus pubescens | bark | 0.0 | - | X Acacia dealbata 0.37 |
| Quercus_robur_bark_1.jpg | Quercus robur | bark | 0.0 | - | X Quercus ilex 0.54 |
| Quercus_robur_bark_2.jpg | Quercus robur | bark | 0.0 | - | X Crataegus monogyna 0.29 |
| Sorbus_aucuparia_bark_1.jpg | Sorbus aucuparia | bark | 0.0 | - | OK Sorbus aucuparia 0.90 |
| Sorbus_aucuparia_bark_2.jpg | Sorbus aucuparia | bark | 0.0 | - | OK Sorbus aucuparia 0.82 |
| Viburnum_lantana_bark_1.jpg | Viburnum lantana | bark | 0.0 | - | OK Viburnum lantana 0.52 |
| Viburnum_lantana_bark_2.jpg | Viburnum lantana | bark | 0.3 | X Arabidopsis thaliana 0.33 | OK Viburnum lantana 0.64 |

No previous report to compare with.
