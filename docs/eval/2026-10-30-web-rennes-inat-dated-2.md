# Eval report — 2026-10-30 — web-rennes-inat-dated

- Photos: 130 (labels from labels.csv)
- Candidate list: `data/species_lists/catalog.txt` (225 species)
- Confidence threshold for abstaining: 0.5 (placeholder)
- Device: cuda
- Labels are PlantNet suggestions given by the team, not expert-verified: treat the second word of each name as uncertain (genus-level is more reliable).

## Setting: catalog
True species on the candidate list for 123/130 (95%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 105/130 (81%) | 108/130 (83%) | 106/130 (82%) | 0.961 / 0.391 | 1 | 104/112 (93%) |
| full | 123/130 (95%) | 123/130 (95%) | 123/130 (95%) | 0.973 / 0.286 | 0 | 122/124 (98%) |
| hybrid>=2 | 120/130 (92%) | 121/130 (93%) | 121/130 (93%) | 0.967 / 0.335 | 0 | 119/122 (98%) |
| hybrid>=5 | 122/130 (94%) | 123/130 (95%) | 123/130 (95%) | 0.974 / 0.32 | 0 | 121/123 (98%) |
| hybrid>=10 | 122/130 (94%) | 123/130 (95%) | 123/130 (95%) | 0.975 / 0.308 | 0 | 121/124 (98%) |
| hybrid>=20 | 123/130 (95%) | 123/130 (95%) | 123/130 (95%) | 0.974 / 0.262 | 0 | 122/124 (98%) |
| hybrid>=40 | 123/130 (95%) | 123/130 (95%) | 123/130 (95%) | 0.973 / 0.266 | 0 | 122/124 (98%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 18 | 1 |
| 0.50-0.80 | 11 | 5 |
| 0.80-0.95 | 15 | 13 |
| 0.95-1.00 | 86 | 86 |

Could BioCLIP have seen these photos? Split by iNaturalist upload date (cutoff 2024-06-01: BioCLIP 2 training data ends with a GBIF snapshot of 2024-05-01):

| subset | photos | full top-1 | full top-3 | crop top-1 | crop top-3 |
|---|---|---|---|---|---|
| uploaded on/after 2024-06-01 (cannot be in training data) | 103 | 99/103 (96%) | 99/103 (96%) | 83/103 (81%) | 85/103 (83%) |
| uploaded earlier (may be in training data) | 27 | 24/27 (89%) | 24/27 (89%) | 22/27 (81%) | 23/27 (85%) |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Eupatorium cannabinum → Iris pseudacorus ×1, Prunus laurocerasus → Castanea sativa ×1, Prunus laurocerasus → Phillyrea latifolia ×1, Digitalis purpurea → Ecballium elaterium ×1, Quercus robur → Quercus petraea ×1, Ulex europaeus → Gentiana lutea ×1, Ulex europaeus → Crocus vernus ×1, Achillea millefolium → Thymus vulgaris ×1
- full: Prunus laurocerasus → Castanea sativa ×2, Chelidonium majus → Alliaria petiolata ×2, Capsella bursa-pastoris → Teesdalia nudicaulis ×1, Arabidopsis thaliana → Saxifraga granulata ×1, Melissa officinalis → Melittis melissophyllum ×1

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Asplenium_scolopendrium_1.jpg | Asplenium scolopendrium |  | 45.6 | OK Asplenium scolopendrium 1.00 | OK Asplenium scolopendrium 1.00 |
| Eupatorium_cannabinum_1.jpg | Eupatorium cannabinum |  | 0.6 | X Iris pseudacorus 0.27 | OK Eupatorium cannabinum 1.00 |
| Ilex_aquifolium_1.jpg | Ilex aquifolium |  | 94.9 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Ilex_aquifolium_2.jpg | Ilex aquifolium |  | 94.7 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Orchis_mascula_1.jpg | Orchis mascula |  | 7.7 | OK Orchis mascula 1.00 | OK Orchis mascula 1.00 |
| Orchis_mascula_2.jpg | Orchis mascula |  | 11.4 | OK Orchis mascula 1.00 | OK Orchis mascula 0.99 |
| Pteridium_aquilinum_1.jpg | Pteridium aquilinum |  | 51.6 | OK Pteridium aquilinum 0.99 | OK Pteridium aquilinum 0.96 |
| Pteridium_aquilinum_2.jpg | Pteridium aquilinum |  | 95.9 | OK Pteridium aquilinum 0.98 | OK Pteridium aquilinum 0.98 |
| Fagus_sylvatica_1.jpg | Fagus sylvatica |  | 93.5 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Fagus_sylvatica_2.jpg | Fagus sylvatica |  | 16.4 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Cornus_sanguinea_1.jpg | Cornus sanguinea |  | 9.8 | OK Cornus sanguinea 1.00 | OK Cornus sanguinea 1.00 |
| Prunus_laurocerasus_1.jpg | Prunus laurocerasus (not on list) |  | 76.4 | X Castanea sativa 0.34 | X Castanea sativa 0.48 |
| Prunus_laurocerasus_2.jpg | Prunus laurocerasus (not on list) |  | 9.8 | X Phillyrea latifolia 0.29 | X Castanea sativa 0.51 |
| Ajuga_reptans_1.jpg | Ajuga reptans |  | 2.1 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_2.jpg | Ajuga reptans |  | 3.7 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Dryopteris_filix-mas_1.jpg | Dryopteris filix-mas |  | 77.3 | OK Dryopteris filix-mas 0.89 | OK Dryopteris filix-mas 0.78 |
| Rabelera_holostea_1.jpg | Rabelera holostea |  | 1.2 | OK Rabelera holostea 1.00 | OK Rabelera holostea 1.00 |
| Rabelera_holostea_2.jpg | Rabelera holostea |  | 22.7 | OK Rabelera holostea 1.00 | OK Rabelera holostea 1.00 |
| Corylus_avellana_1.jpg | Corylus avellana |  | 45.3 | OK Corylus avellana 1.00 | OK Corylus avellana 0.99 |
| Corylus_avellana_2.jpg | Corylus avellana |  | 5.1 | OK Corylus avellana 1.00 | OK Corylus avellana 1.00 |
| Ligustrum_vulgare_1.jpg | Ligustrum vulgare |  | 74.5 | OK Ligustrum vulgare 0.95 | OK Ligustrum vulgare 0.83 |
| Phragmites_australis_1.jpg | Phragmites australis |  | 77.5 | OK Phragmites australis 0.97 | OK Phragmites australis 0.82 |
| Prunus_spinosa_1.jpg | Prunus spinosa |  | 97.7 | OK Prunus spinosa 1.00 | OK Prunus spinosa 1.00 |
| Digitalis_purpurea_1.jpg | Digitalis purpurea |  | 4.8 | OK Digitalis purpurea 0.88 | OK Digitalis purpurea 0.99 |
| Digitalis_purpurea_2.jpg | Digitalis purpurea |  | 0.3 | X Ecballium elaterium 0.54 | OK Digitalis purpurea 1.00 |
| Urtica_dioica_1.jpg | Urtica dioica |  | 79.2 | OK Urtica dioica 1.00 | OK Urtica dioica 1.00 |
| Urtica_dioica_2.jpg | Urtica dioica |  | 44.6 | OK Urtica dioica 1.00 | OK Urtica dioica 1.00 |
| Solanum_dulcamara_1.jpg | Solanum dulcamara |  | 14.6 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Solanum_dulcamara_2.jpg | Solanum dulcamara |  | 97.0 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Sedum_acre_1.jpg | Sedum acre |  | 69.2 | OK Sedum acre 1.00 | OK Sedum acre 0.99 |
| Quercus_robur_1.jpg | Quercus robur |  | 11.9 | X Quercus petraea 0.64 | OK Quercus robur 0.81 |
| Quercus_robur_2.jpg | Quercus robur |  | 25.5 | OK Quercus robur 0.93 | OK Quercus robur 0.81 |
| Ulex_europaeus_1.jpg | Ulex europaeus |  | 0.1 | X Gentiana lutea 0.12 | OK Ulex europaeus 0.99 |
| Ulex_europaeus_2.jpg | Ulex europaeus |  | 0.1 | X Crocus vernus 0.31 | OK Ulex europaeus 0.95 |
| Cirsium_vulgare_1.jpg | Cirsium vulgare |  | 0.5 | OK Cirsium vulgare 0.56 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_2.jpg | Cirsium vulgare |  | 2.9 | OK Cirsium vulgare 0.99 | OK Cirsium vulgare 1.00 |
| Hyacinthoides_non-scripta_1.jpg | Hyacinthoides non-scripta |  | 4.8 | OK Hyacinthoides non-scripta 1.00 | OK Hyacinthoides non-scripta 1.00 |
| Achillea_millefolium_1.jpg | Achillea millefolium |  | 0.4 | X Thymus vulgaris 0.29 | OK Achillea millefolium 1.00 |
| Trifolium_pratense_1.jpg | Trifolium pratense |  | 5.7 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Trifolium_pratense_2.jpg | Trifolium pratense |  | 14.1 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Castanea_sativa_1.jpg | Castanea sativa |  | 1.4 | OK Castanea sativa 1.00 | OK Castanea sativa 0.62 |
| Castanea_sativa_2.jpg | Castanea sativa |  | 1.2 | OK Castanea sativa 1.00 | OK Castanea sativa 1.00 |
| Plantago_lanceolata_1.jpg | Plantago lanceolata |  | 72.6 | OK Plantago lanceolata 1.00 | OK Plantago lanceolata 1.00 |
| Plantago_lanceolata_2.jpg | Plantago lanceolata |  | 67.2 | OK Plantago lanceolata 0.99 | OK Plantago lanceolata 0.99 |
| Acer_pseudoplatanus_1.jpg | Acer pseudoplatanus |  | 13.2 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Acer_pseudoplatanus_2.jpg | Acer pseudoplatanus |  | 40.8 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Crataegus_monogyna_1.jpg | Crataegus monogyna |  | 5.1 | OK Crataegus monogyna 1.00 | OK Crataegus monogyna 1.00 |
| Crataegus_monogyna_2.jpg | Crataegus monogyna |  | 0.5 | X Ribes rubrum 0.18 | OK Crataegus monogyna 1.00 |
| Sambucus_ebulus_1.jpg | Sambucus ebulus |  | 7.1 | OK Sambucus ebulus 1.00 | OK Sambucus ebulus 1.00 |
| Echium_vulgare_1.jpg | Echium vulgare |  | 0.3 | X Hyacinthoides non-scripta 0.29 | OK Echium vulgare 1.00 |
| Teucrium_scorodonia_1.jpg | Teucrium scorodonia |  | 96.3 | OK Teucrium scorodonia 0.93 | OK Teucrium scorodonia 1.00 |
| Teucrium_scorodonia_2.jpg | Teucrium scorodonia |  | 2.4 | OK Teucrium scorodonia 1.00 | OK Teucrium scorodonia 1.00 |
| Heracleum_sphondylium_1.jpg | Heracleum sphondylium |  | 3.2 | OK Heracleum sphondylium 1.00 | OK Heracleum sphondylium 1.00 |
| Heracleum_sphondylium_2.jpg | Heracleum sphondylium |  | 96.8 | OK Heracleum sphondylium 0.83 | OK Heracleum sphondylium 0.90 |
| Plantago_coronopus_1.jpg | Plantago coronopus |  | 30.1 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Plantago_coronopus_2.jpg | Plantago coronopus |  | 77.5 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Chelidonium_majus_1.jpg | Chelidonium majus (not on list) |  | 89.2 | X Alliaria petiolata 0.09 | X Alliaria petiolata 0.09 |
| Chelidonium_majus_2.jpg | Chelidonium majus (not on list) |  | 27.4 | X Urtica dioica 0.09 | X Alliaria petiolata 0.12 |
| Fraxinus_excelsior_1.jpg | Fraxinus excelsior |  | 95.6 | OK Fraxinus excelsior 0.50 | OK Fraxinus excelsior 0.39 |
| Trifolium_repens_1.jpg | Trifolium repens |  | 3.8 | OK Trifolium repens 1.00 | OK Trifolium repens 1.00 |
| Trifolium_repens_2.jpg | Trifolium repens |  | 8.3 | OK Trifolium repens 1.00 | OK Trifolium repens 1.00 |
| Geranium_dissectum_1.jpg | Geranium dissectum |  | 94.5 | OK Geranium dissectum 1.00 | OK Geranium dissectum 1.00 |
| Geranium_dissectum_2.jpg | Geranium dissectum |  | 19.8 | OK Geranium dissectum 1.00 | OK Geranium dissectum 1.00 |
| Vicia_sepium_1.jpg | Vicia sepium |  | 8.6 | OK Vicia sepium 1.00 | OK Vicia sepium 1.00 |
| Cytisus_scoparius_1.jpg | Cytisus scoparius |  | 96.1 | OK Cytisus scoparius 1.00 | OK Cytisus scoparius 0.99 |
| Asplenium_ceterach_1.jpg | Asplenium ceterach |  | 46.7 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Asplenium_ceterach_2.jpg | Asplenium ceterach |  | 91.6 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Anthoxanthum_odoratum_1.jpg | Anthoxanthum odoratum |  | 0.5 | X Prenanthes purpurea 0.17 | OK Anthoxanthum odoratum 1.00 |
| Vicia_cracca_1.jpg | Vicia cracca |  | 3.8 | OK Vicia cracca 1.00 | OK Vicia cracca 1.00 |
| Medicago_lupulina_1.jpg | Medicago lupulina |  | 0.9 | X Primula veris 0.45 | OK Medicago lupulina 1.00 |
| Agrimonia_eupatoria_1.jpg | Agrimonia eupatoria |  | 1.8 | OK Agrimonia eupatoria 0.98 | OK Agrimonia eupatoria 1.00 |
| Catapodium_rigidum_1.jpg | Catapodium rigidum |  | 79.2 | OK Catapodium rigidum 1.00 | OK Catapodium rigidum 1.00 |
| Dactylis_glomerata_1.jpg | Dactylis glomerata |  | 39.6 | OK Dactylis glomerata 0.98 | OK Dactylis glomerata 0.99 |
| Hypericum_perforatum_1.jpg | Hypericum perforatum |  | 2.7 | OK Hypericum perforatum 1.00 | OK Hypericum perforatum 1.00 |
| Erica_cinerea_1.jpg | Erica cinerea |  | 95.1 | OK Erica cinerea 0.97 | OK Erica cinerea 0.99 |
| Erica_cinerea_2.jpg | Erica cinerea |  | 27.1 | OK Erica cinerea 1.00 | OK Erica cinerea 0.99 |
| Scorzonera_humilis_1.jpg | Scorzonera humilis |  | 2.2 | OK Scorzonera humilis 0.90 | OK Scorzonera humilis 1.00 |
| Struthiopteris_spicant_1.jpg | Struthiopteris spicant |  | 92.6 | OK Struthiopteris spicant 0.98 | OK Struthiopteris spicant 0.98 |
| Struthiopteris_spicant_2.jpg | Struthiopteris spicant |  | 57.3 | OK Struthiopteris spicant 1.00 | OK Struthiopteris spicant 1.00 |
| Phalaris_arundinacea_1.jpg | Phalaris arundinacea |  | 82.2 | OK Phalaris arundinacea 0.98 | OK Phalaris arundinacea 0.98 |
| Lotus_corniculatus_1.jpg | Lotus corniculatus |  | 94.8 | OK Lotus corniculatus 0.95 | OK Lotus corniculatus 0.97 |
| Argentina_anserina_1.jpg | Argentina anserina |  | 95.6 | OK Argentina anserina 1.00 | OK Argentina anserina 1.00 |
| Anacamptis_pyramidalis_1.jpg | Anacamptis pyramidalis |  | 8.7 | OK Anacamptis pyramidalis 0.97 | OK Anacamptis pyramidalis 0.99 |
| Anacamptis_pyramidalis_2.jpg | Anacamptis pyramidalis |  | 18.3 | OK Anacamptis pyramidalis 0.99 | OK Anacamptis pyramidalis 1.00 |
| Calluna_vulgaris_1.jpg | Calluna vulgaris |  | 97.0 | OK Calluna vulgaris 0.99 | OK Calluna vulgaris 0.99 |
| Primula_veris_1.jpg | Primula veris |  | 3.1 | OK Primula veris 1.00 | OK Primula veris 0.99 |
| Primula_veris_2.jpg | Primula veris |  | 13.7 | OK Primula veris 1.00 | OK Primula veris 1.00 |
| Bellis_perennis_1.jpg | Bellis perennis |  | 0.8 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Bellis_perennis_2.jpg | Bellis perennis |  | 8.4 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Lathyrus_pratensis_1.jpg | Lathyrus pratensis |  | 2.8 | X Aristolochia clematitis 0.19 | OK Lathyrus pratensis 0.99 |
| Lathyrus_pratensis_2.jpg | Lathyrus pratensis |  | 2.9 | OK Lathyrus pratensis 0.94 | OK Lathyrus pratensis 0.99 |
| Dactylorhiza_maculata_1.jpg | Dactylorhiza maculata |  | 2.6 | OK Dactylorhiza maculata 0.92 | OK Dactylorhiza maculata 0.88 |
| Hedera_helix_1.jpg | Hedera helix |  | 2.0 | OK Hedera helix 0.78 | OK Hedera helix 1.00 |
| Hedera_helix_2.jpg | Hedera helix |  | 25.1 | OK Hedera helix 1.00 | OK Hedera helix 1.00 |
| Juncus_acutiflorus_1.jpg | Juncus acutiflorus |  | 0.9 | X Trifolium pratense 0.27 | OK Juncus acutiflorus 1.00 |
| Juncus_acutiflorus_2.jpg | Juncus acutiflorus |  | 44.5 | OK Juncus acutiflorus 1.00 | OK Juncus acutiflorus 0.98 |
| Arrhenatherum_elatius_1.jpg | Arrhenatherum elatius |  | 0.3 | X Digitalis purpurea 0.31 | OK Arrhenatherum elatius 0.98 |
| Impatiens_balfourii_1.jpg | Impatiens balfourii |  | 7.9 | OK Impatiens balfourii 1.00 | OK Impatiens balfourii 1.00 |
| Alopecurus_pratensis_1.jpg | Alopecurus pratensis |  | 0.3 | X Impatiens balfourii 0.57 | OK Alopecurus pratensis 1.00 |
| Borago_officinalis_1.jpg | Borago officinalis |  | 3.8 | OK Borago officinalis 1.00 | OK Borago officinalis 1.00 |
| Teesdalia_nudicaulis_1.jpg | Teesdalia nudicaulis |  | 1.7 | OK Teesdalia nudicaulis 0.97 | OK Teesdalia nudicaulis 1.00 |
| Teesdalia_nudicaulis_2.jpg | Teesdalia nudicaulis |  | 21.8 | OK Teesdalia nudicaulis 1.00 | OK Teesdalia nudicaulis 1.00 |
| Lotus_pedunculatus_1.jpg | Lotus pedunculatus |  | 5.4 | OK Lotus pedunculatus 0.99 | OK Lotus pedunculatus 0.98 |
| Potentilla_erecta_1.jpg | Potentilla erecta |  | 0.9 | OK Potentilla erecta 0.85 | OK Potentilla erecta 0.99 |
| Potentilla_erecta_2.jpg | Potentilla erecta |  | 25.3 | OK Potentilla erecta 0.94 | OK Potentilla erecta 0.99 |
| Alliaria_petiolata_1.jpg | Alliaria petiolata |  | 1.2 | OK Alliaria petiolata 1.00 | OK Alliaria petiolata 0.98 |
| Galium_mollugo_1.jpg | Galium mollugo |  | 9.0 | OK Galium mollugo 1.00 | OK Galium mollugo 1.00 |
| Aulacomnium_palustre_1.jpg | Aulacomnium palustre |  | 95.4 | OK Aulacomnium palustre 1.00 | OK Aulacomnium palustre 1.00 |
| Carex_panicea_1.jpg | Carex panicea |  | 96.7 | OK Carex panicea 0.63 | OK Carex panicea 0.59 |
| Carex_hirta_1.jpg | Carex hirta |  | 2.8 | OK Carex hirta 1.00 | OK Carex hirta 1.00 |
| Viburnum_lantana_1.jpg | Viburnum lantana |  | 3.5 | OK Viburnum lantana 1.00 | OK Viburnum lantana 1.00 |
| Fagopyrum_esculentum_1.jpg | Fagopyrum esculentum |  | 26.2 | OK Fagopyrum esculentum 1.00 | OK Fagopyrum esculentum 1.00 |
| Buxus_sempervirens_1.jpg | Buxus sempervirens |  | 0.5 | X Impatiens balfourii 0.69 | OK Buxus sempervirens 1.00 |
| Sorbus_aucuparia_1.jpg | Sorbus aucuparia |  | 4.3 | OK Sorbus aucuparia 0.94 | OK Sorbus aucuparia 1.00 |
| Picris_hieracioides_1.jpg | Picris hieracioides |  | 37.2 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Picris_hieracioides_2.jpg | Picris hieracioides |  | 13.6 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Pinus_sylvestris_1.jpg | Pinus sylvestris |  | 3.1 | OK Pinus sylvestris 0.84 | OK Pinus sylvestris 0.75 |
| Molinia_caerulea_1.jpg | Molinia caerulea |  | 0.3 | X Carex paniculata 0.90 | OK Molinia caerulea 1.00 |
| Anthriscus_sylvestris_1.jpg | Anthriscus sylvestris |  | 0.4 | X Achillea millefolium 0.87 | OK Anthriscus sylvestris 1.00 |
| Capsella_bursa-pastoris_1.jpg | Capsella bursa-pastoris (not on list) |  | 6.6 | X Lapsana communis 0.46 | X Teesdalia nudicaulis 0.15 |
| Bromus_hordeaceus_1.jpg | Bromus hordeaceus |  | 45.2 | OK Bromus hordeaceus 1.00 | OK Bromus hordeaceus 1.00 |
| Holcus_lanatus_1.jpg | Holcus lanatus |  | 0.8 | OK Holcus lanatus 0.96 | OK Holcus lanatus 0.97 |
| Carex_flacca_1.jpg | Carex flacca |  | 2.5 | OK Carex flacca 0.62 | OK Carex flacca 1.00 |
| Neottia_ovata_1.jpg | Neottia ovata |  | 4.3 | X Lycopus europaeus 0.60 | OK Neottia ovata 1.00 |
| Galium_odoratum_1.jpg | Galium odoratum |  | 7.2 | OK Galium odoratum 0.99 | OK Galium odoratum 1.00 |
| Rubus_idaeus_1.jpg | Rubus idaeus |  | 46.3 | OK Rubus idaeus 0.58 | OK Rubus idaeus 0.92 |
| Arabidopsis_thaliana_1.jpg | Arabidopsis thaliana (not on list) |  | 1.4 | X Castanea sativa 0.13 | X Saxifraga granulata 0.14 |
| Melissa_officinalis_1.jpg | Melissa officinalis (not on list) |  | 0.3 | X Melittis melissophyllum 0.72 | X Melittis melissophyllum 0.50 |
| Helleborus_foetidus_1.jpg | Helleborus foetidus |  | 90.7 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Petasites_hybridus_1.jpg | Petasites hybridus |  | 12.3 | OK Petasites hybridus 0.96 | OK Petasites hybridus 1.00 |

## Setting: catalog+truth
True species on the candidate list for 130/130 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 111/130 (85%) | 114/130 (88%) | 112/130 (86%) | 0.957 / 0.406 | 1 | 109/116 (94%) |
| full | 130/130 (100%) | 130/130 (100%) | 130/130 (100%) | 0.973 / None | 0 | 129/129 (100%) |
| hybrid>=2 | 127/130 (98%) | 128/130 (98%) | 128/130 (98%) | 0.968 / 0.469 | 0 | 126/128 (98%) |
| hybrid>=5 | 129/130 (99%) | 130/130 (100%) | 130/130 (100%) | 0.975 / 0.637 | 0 | 128/129 (99%) |
| hybrid>=10 | 129/130 (99%) | 130/130 (100%) | 130/130 (100%) | 0.976 / 0.637 | 0 | 128/129 (99%) |
| hybrid>=20 | 130/130 (100%) | 130/130 (100%) | 130/130 (100%) | 0.975 / None | 0 | 129/129 (100%) |
| hybrid>=40 | 130/130 (100%) | 130/130 (100%) | 130/130 (100%) | 0.974 / None | 0 | 129/129 (100%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 14 | 2 |
| 0.50-0.80 | 10 | 5 |
| 0.80-0.95 | 16 | 14 |
| 0.95-1.00 | 90 | 90 |

Could BioCLIP have seen these photos? Split by iNaturalist upload date (cutoff 2024-06-01: BioCLIP 2 training data ends with a GBIF snapshot of 2024-05-01):

| subset | photos | full top-1 | full top-3 | crop top-1 | crop top-3 |
|---|---|---|---|---|---|
| uploaded on/after 2024-06-01 (cannot be in training data) | 103 | 103/103 (100%) | 103/103 (100%) | 87/103 (84%) | 89/103 (86%) |
| uploaded earlier (may be in training data) | 27 | 27/27 (100%) | 27/27 (100%) | 24/27 (89%) | 25/27 (93%) |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Eupatorium cannabinum → Iris pseudacorus ×1, Digitalis purpurea → Ecballium elaterium ×1, Quercus robur → Quercus petraea ×1, Ulex europaeus → Gentiana lutea ×1, Ulex europaeus → Crocus vernus ×1, Achillea millefolium → Thymus vulgaris ×1, Crataegus monogyna → Ribes rubrum ×1, Echium vulgare → Hyacinthoides non-scripta ×1
- full: none

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Asplenium_scolopendrium_1.jpg | Asplenium scolopendrium |  | 45.6 | OK Asplenium scolopendrium 1.00 | OK Asplenium scolopendrium 1.00 |
| Eupatorium_cannabinum_1.jpg | Eupatorium cannabinum |  | 0.6 | X Iris pseudacorus 0.27 | OK Eupatorium cannabinum 1.00 |
| Ilex_aquifolium_1.jpg | Ilex aquifolium |  | 94.9 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Ilex_aquifolium_2.jpg | Ilex aquifolium |  | 94.7 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Orchis_mascula_1.jpg | Orchis mascula |  | 7.7 | OK Orchis mascula 1.00 | OK Orchis mascula 1.00 |
| Orchis_mascula_2.jpg | Orchis mascula |  | 11.4 | OK Orchis mascula 1.00 | OK Orchis mascula 0.99 |
| Pteridium_aquilinum_1.jpg | Pteridium aquilinum |  | 51.6 | OK Pteridium aquilinum 0.99 | OK Pteridium aquilinum 0.96 |
| Pteridium_aquilinum_2.jpg | Pteridium aquilinum |  | 95.9 | OK Pteridium aquilinum 0.98 | OK Pteridium aquilinum 0.98 |
| Fagus_sylvatica_1.jpg | Fagus sylvatica |  | 93.5 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Fagus_sylvatica_2.jpg | Fagus sylvatica |  | 16.4 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Cornus_sanguinea_1.jpg | Cornus sanguinea |  | 9.8 | OK Cornus sanguinea 1.00 | OK Cornus sanguinea 1.00 |
| Prunus_laurocerasus_1.jpg | Prunus laurocerasus |  | 76.4 | OK Prunus laurocerasus 1.00 | OK Prunus laurocerasus 1.00 |
| Prunus_laurocerasus_2.jpg | Prunus laurocerasus |  | 9.8 | OK Prunus laurocerasus 1.00 | OK Prunus laurocerasus 1.00 |
| Ajuga_reptans_1.jpg | Ajuga reptans |  | 2.1 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_2.jpg | Ajuga reptans |  | 3.7 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Dryopteris_filix-mas_1.jpg | Dryopteris filix-mas |  | 77.3 | OK Dryopteris filix-mas 0.89 | OK Dryopteris filix-mas 0.78 |
| Rabelera_holostea_1.jpg | Rabelera holostea |  | 1.2 | OK Rabelera holostea 1.00 | OK Rabelera holostea 1.00 |
| Rabelera_holostea_2.jpg | Rabelera holostea |  | 22.7 | OK Rabelera holostea 1.00 | OK Rabelera holostea 1.00 |
| Corylus_avellana_1.jpg | Corylus avellana |  | 45.3 | OK Corylus avellana 1.00 | OK Corylus avellana 0.99 |
| Corylus_avellana_2.jpg | Corylus avellana |  | 5.1 | OK Corylus avellana 1.00 | OK Corylus avellana 1.00 |
| Ligustrum_vulgare_1.jpg | Ligustrum vulgare |  | 74.5 | OK Ligustrum vulgare 0.94 | OK Ligustrum vulgare 0.81 |
| Phragmites_australis_1.jpg | Phragmites australis |  | 77.5 | OK Phragmites australis 0.97 | OK Phragmites australis 0.82 |
| Prunus_spinosa_1.jpg | Prunus spinosa |  | 97.7 | OK Prunus spinosa 1.00 | OK Prunus spinosa 1.00 |
| Digitalis_purpurea_1.jpg | Digitalis purpurea |  | 4.8 | OK Digitalis purpurea 0.86 | OK Digitalis purpurea 0.99 |
| Digitalis_purpurea_2.jpg | Digitalis purpurea |  | 0.3 | X Ecballium elaterium 0.53 | OK Digitalis purpurea 1.00 |
| Urtica_dioica_1.jpg | Urtica dioica |  | 79.2 | OK Urtica dioica 1.00 | OK Urtica dioica 1.00 |
| Urtica_dioica_2.jpg | Urtica dioica |  | 44.6 | OK Urtica dioica 1.00 | OK Urtica dioica 1.00 |
| Solanum_dulcamara_1.jpg | Solanum dulcamara |  | 14.6 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Solanum_dulcamara_2.jpg | Solanum dulcamara |  | 97.0 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Sedum_acre_1.jpg | Sedum acre |  | 69.2 | OK Sedum acre 1.00 | OK Sedum acre 0.99 |
| Quercus_robur_1.jpg | Quercus robur |  | 11.9 | X Quercus petraea 0.64 | OK Quercus robur 0.81 |
| Quercus_robur_2.jpg | Quercus robur |  | 25.5 | OK Quercus robur 0.93 | OK Quercus robur 0.81 |
| Ulex_europaeus_1.jpg | Ulex europaeus |  | 0.1 | X Gentiana lutea 0.12 | OK Ulex europaeus 0.99 |
| Ulex_europaeus_2.jpg | Ulex europaeus |  | 0.1 | X Crocus vernus 0.30 | OK Ulex europaeus 0.95 |
| Cirsium_vulgare_1.jpg | Cirsium vulgare |  | 0.5 | OK Cirsium vulgare 0.56 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_2.jpg | Cirsium vulgare |  | 2.9 | OK Cirsium vulgare 0.99 | OK Cirsium vulgare 1.00 |
| Hyacinthoides_non-scripta_1.jpg | Hyacinthoides non-scripta |  | 4.8 | OK Hyacinthoides non-scripta 1.00 | OK Hyacinthoides non-scripta 1.00 |
| Achillea_millefolium_1.jpg | Achillea millefolium |  | 0.4 | X Thymus vulgaris 0.29 | OK Achillea millefolium 1.00 |
| Trifolium_pratense_1.jpg | Trifolium pratense |  | 5.7 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Trifolium_pratense_2.jpg | Trifolium pratense |  | 14.1 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Castanea_sativa_1.jpg | Castanea sativa |  | 1.4 | OK Castanea sativa 1.00 | OK Castanea sativa 0.62 |
| Castanea_sativa_2.jpg | Castanea sativa |  | 1.2 | OK Castanea sativa 1.00 | OK Castanea sativa 1.00 |
| Plantago_lanceolata_1.jpg | Plantago lanceolata |  | 72.6 | OK Plantago lanceolata 1.00 | OK Plantago lanceolata 1.00 |
| Plantago_lanceolata_2.jpg | Plantago lanceolata |  | 67.2 | OK Plantago lanceolata 0.99 | OK Plantago lanceolata 0.99 |
| Acer_pseudoplatanus_1.jpg | Acer pseudoplatanus |  | 13.2 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Acer_pseudoplatanus_2.jpg | Acer pseudoplatanus |  | 40.8 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Crataegus_monogyna_1.jpg | Crataegus monogyna |  | 5.1 | OK Crataegus monogyna 1.00 | OK Crataegus monogyna 1.00 |
| Crataegus_monogyna_2.jpg | Crataegus monogyna |  | 0.5 | X Ribes rubrum 0.18 | OK Crataegus monogyna 1.00 |
| Sambucus_ebulus_1.jpg | Sambucus ebulus |  | 7.1 | OK Sambucus ebulus 1.00 | OK Sambucus ebulus 1.00 |
| Echium_vulgare_1.jpg | Echium vulgare |  | 0.3 | X Hyacinthoides non-scripta 0.29 | OK Echium vulgare 1.00 |
| Teucrium_scorodonia_1.jpg | Teucrium scorodonia |  | 96.3 | OK Teucrium scorodonia 0.92 | OK Teucrium scorodonia 0.98 |
| Teucrium_scorodonia_2.jpg | Teucrium scorodonia |  | 2.4 | OK Teucrium scorodonia 0.94 | OK Teucrium scorodonia 0.95 |
| Heracleum_sphondylium_1.jpg | Heracleum sphondylium |  | 3.2 | OK Heracleum sphondylium 1.00 | OK Heracleum sphondylium 1.00 |
| Heracleum_sphondylium_2.jpg | Heracleum sphondylium |  | 96.8 | OK Heracleum sphondylium 0.83 | OK Heracleum sphondylium 0.90 |
| Plantago_coronopus_1.jpg | Plantago coronopus |  | 30.1 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Plantago_coronopus_2.jpg | Plantago coronopus |  | 77.5 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Chelidonium_majus_1.jpg | Chelidonium majus |  | 89.2 | OK Chelidonium majus 1.00 | OK Chelidonium majus 1.00 |
| Chelidonium_majus_2.jpg | Chelidonium majus |  | 27.4 | OK Chelidonium majus 1.00 | OK Chelidonium majus 1.00 |
| Fraxinus_excelsior_1.jpg | Fraxinus excelsior |  | 95.6 | OK Fraxinus excelsior 0.50 | OK Fraxinus excelsior 0.39 |
| Trifolium_repens_1.jpg | Trifolium repens |  | 3.8 | OK Trifolium repens 1.00 | OK Trifolium repens 1.00 |
| Trifolium_repens_2.jpg | Trifolium repens |  | 8.3 | OK Trifolium repens 1.00 | OK Trifolium repens 1.00 |
| Geranium_dissectum_1.jpg | Geranium dissectum |  | 94.5 | OK Geranium dissectum 1.00 | OK Geranium dissectum 1.00 |
| Geranium_dissectum_2.jpg | Geranium dissectum |  | 19.8 | OK Geranium dissectum 1.00 | OK Geranium dissectum 1.00 |
| Vicia_sepium_1.jpg | Vicia sepium |  | 8.6 | OK Vicia sepium 1.00 | OK Vicia sepium 1.00 |
| Cytisus_scoparius_1.jpg | Cytisus scoparius |  | 96.1 | OK Cytisus scoparius 1.00 | OK Cytisus scoparius 0.99 |
| Asplenium_ceterach_1.jpg | Asplenium ceterach |  | 46.7 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Asplenium_ceterach_2.jpg | Asplenium ceterach |  | 91.6 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Anthoxanthum_odoratum_1.jpg | Anthoxanthum odoratum |  | 0.5 | X Prenanthes purpurea 0.17 | OK Anthoxanthum odoratum 1.00 |
| Vicia_cracca_1.jpg | Vicia cracca |  | 3.8 | OK Vicia cracca 1.00 | OK Vicia cracca 1.00 |
| Medicago_lupulina_1.jpg | Medicago lupulina |  | 0.9 | X Primula veris 0.45 | OK Medicago lupulina 1.00 |
| Agrimonia_eupatoria_1.jpg | Agrimonia eupatoria |  | 1.8 | OK Agrimonia eupatoria 0.98 | OK Agrimonia eupatoria 1.00 |
| Catapodium_rigidum_1.jpg | Catapodium rigidum |  | 79.2 | OK Catapodium rigidum 1.00 | OK Catapodium rigidum 1.00 |
| Dactylis_glomerata_1.jpg | Dactylis glomerata |  | 39.6 | OK Dactylis glomerata 0.98 | OK Dactylis glomerata 0.99 |
| Hypericum_perforatum_1.jpg | Hypericum perforatum |  | 2.7 | OK Hypericum perforatum 1.00 | OK Hypericum perforatum 1.00 |
| Erica_cinerea_1.jpg | Erica cinerea |  | 95.1 | OK Erica cinerea 0.97 | OK Erica cinerea 0.99 |
| Erica_cinerea_2.jpg | Erica cinerea |  | 27.1 | OK Erica cinerea 1.00 | OK Erica cinerea 0.99 |
| Scorzonera_humilis_1.jpg | Scorzonera humilis |  | 2.2 | OK Scorzonera humilis 0.90 | OK Scorzonera humilis 1.00 |
| Struthiopteris_spicant_1.jpg | Struthiopteris spicant |  | 92.6 | OK Struthiopteris spicant 0.98 | OK Struthiopteris spicant 0.98 |
| Struthiopteris_spicant_2.jpg | Struthiopteris spicant |  | 57.3 | OK Struthiopteris spicant 1.00 | OK Struthiopteris spicant 1.00 |
| Phalaris_arundinacea_1.jpg | Phalaris arundinacea |  | 82.2 | OK Phalaris arundinacea 0.98 | OK Phalaris arundinacea 0.98 |
| Lotus_corniculatus_1.jpg | Lotus corniculatus |  | 94.8 | OK Lotus corniculatus 0.95 | OK Lotus corniculatus 0.97 |
| Argentina_anserina_1.jpg | Argentina anserina |  | 95.6 | OK Argentina anserina 1.00 | OK Argentina anserina 1.00 |
| Anacamptis_pyramidalis_1.jpg | Anacamptis pyramidalis |  | 8.7 | OK Anacamptis pyramidalis 0.97 | OK Anacamptis pyramidalis 0.99 |
| Anacamptis_pyramidalis_2.jpg | Anacamptis pyramidalis |  | 18.3 | OK Anacamptis pyramidalis 0.99 | OK Anacamptis pyramidalis 1.00 |
| Calluna_vulgaris_1.jpg | Calluna vulgaris |  | 97.0 | OK Calluna vulgaris 0.99 | OK Calluna vulgaris 0.99 |
| Primula_veris_1.jpg | Primula veris |  | 3.1 | OK Primula veris 1.00 | OK Primula veris 0.99 |
| Primula_veris_2.jpg | Primula veris |  | 13.7 | OK Primula veris 1.00 | OK Primula veris 1.00 |
| Bellis_perennis_1.jpg | Bellis perennis |  | 0.8 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Bellis_perennis_2.jpg | Bellis perennis |  | 8.4 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Lathyrus_pratensis_1.jpg | Lathyrus pratensis |  | 2.8 | X Aristolochia clematitis 0.19 | OK Lathyrus pratensis 0.99 |
| Lathyrus_pratensis_2.jpg | Lathyrus pratensis |  | 2.9 | OK Lathyrus pratensis 0.94 | OK Lathyrus pratensis 0.99 |
| Dactylorhiza_maculata_1.jpg | Dactylorhiza maculata |  | 2.6 | OK Dactylorhiza maculata 0.92 | OK Dactylorhiza maculata 0.88 |
| Hedera_helix_1.jpg | Hedera helix |  | 2.0 | OK Hedera helix 0.77 | OK Hedera helix 1.00 |
| Hedera_helix_2.jpg | Hedera helix |  | 25.1 | OK Hedera helix 1.00 | OK Hedera helix 1.00 |
| Juncus_acutiflorus_1.jpg | Juncus acutiflorus |  | 0.9 | X Trifolium pratense 0.27 | OK Juncus acutiflorus 1.00 |
| Juncus_acutiflorus_2.jpg | Juncus acutiflorus |  | 44.5 | OK Juncus acutiflorus 1.00 | OK Juncus acutiflorus 0.98 |
| Arrhenatherum_elatius_1.jpg | Arrhenatherum elatius |  | 0.3 | X Digitalis purpurea 0.31 | OK Arrhenatherum elatius 0.98 |
| Impatiens_balfourii_1.jpg | Impatiens balfourii |  | 7.9 | OK Impatiens balfourii 1.00 | OK Impatiens balfourii 1.00 |
| Alopecurus_pratensis_1.jpg | Alopecurus pratensis |  | 0.3 | X Impatiens balfourii 0.57 | OK Alopecurus pratensis 1.00 |
| Borago_officinalis_1.jpg | Borago officinalis |  | 3.8 | OK Borago officinalis 1.00 | OK Borago officinalis 1.00 |
| Teesdalia_nudicaulis_1.jpg | Teesdalia nudicaulis |  | 1.7 | OK Teesdalia nudicaulis 0.97 | OK Teesdalia nudicaulis 1.00 |
| Teesdalia_nudicaulis_2.jpg | Teesdalia nudicaulis |  | 21.8 | OK Teesdalia nudicaulis 0.99 | OK Teesdalia nudicaulis 1.00 |
| Lotus_pedunculatus_1.jpg | Lotus pedunculatus |  | 5.4 | OK Lotus pedunculatus 0.99 | OK Lotus pedunculatus 0.98 |
| Potentilla_erecta_1.jpg | Potentilla erecta |  | 0.9 | OK Potentilla erecta 0.85 | OK Potentilla erecta 0.99 |
| Potentilla_erecta_2.jpg | Potentilla erecta |  | 25.3 | OK Potentilla erecta 0.94 | OK Potentilla erecta 0.99 |
| Alliaria_petiolata_1.jpg | Alliaria petiolata |  | 1.2 | OK Alliaria petiolata 0.99 | OK Alliaria petiolata 0.98 |
| Galium_mollugo_1.jpg | Galium mollugo |  | 9.0 | OK Galium mollugo 1.00 | OK Galium mollugo 1.00 |
| Aulacomnium_palustre_1.jpg | Aulacomnium palustre |  | 95.4 | OK Aulacomnium palustre 1.00 | OK Aulacomnium palustre 1.00 |
| Carex_panicea_1.jpg | Carex panicea |  | 96.7 | OK Carex panicea 0.63 | OK Carex panicea 0.59 |
| Carex_hirta_1.jpg | Carex hirta |  | 2.8 | OK Carex hirta 1.00 | OK Carex hirta 1.00 |
| Viburnum_lantana_1.jpg | Viburnum lantana |  | 3.5 | OK Viburnum lantana 1.00 | OK Viburnum lantana 1.00 |
| Fagopyrum_esculentum_1.jpg | Fagopyrum esculentum |  | 26.2 | OK Fagopyrum esculentum 1.00 | OK Fagopyrum esculentum 1.00 |
| Buxus_sempervirens_1.jpg | Buxus sempervirens |  | 0.5 | X Impatiens balfourii 0.68 | OK Buxus sempervirens 1.00 |
| Sorbus_aucuparia_1.jpg | Sorbus aucuparia |  | 4.3 | OK Sorbus aucuparia 0.94 | OK Sorbus aucuparia 1.00 |
| Picris_hieracioides_1.jpg | Picris hieracioides |  | 37.2 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Picris_hieracioides_2.jpg | Picris hieracioides |  | 13.6 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Pinus_sylvestris_1.jpg | Pinus sylvestris |  | 3.1 | OK Pinus sylvestris 0.84 | OK Pinus sylvestris 0.75 |
| Molinia_caerulea_1.jpg | Molinia caerulea |  | 0.3 | X Carex paniculata 0.90 | OK Molinia caerulea 1.00 |
| Anthriscus_sylvestris_1.jpg | Anthriscus sylvestris |  | 0.4 | X Achillea millefolium 0.87 | OK Anthriscus sylvestris 1.00 |
| Capsella_bursa-pastoris_1.jpg | Capsella bursa-pastoris |  | 6.6 | OK Capsella bursa-pastoris 0.98 | OK Capsella bursa-pastoris 1.00 |
| Bromus_hordeaceus_1.jpg | Bromus hordeaceus |  | 45.2 | OK Bromus hordeaceus 1.00 | OK Bromus hordeaceus 1.00 |
| Holcus_lanatus_1.jpg | Holcus lanatus |  | 0.8 | OK Holcus lanatus 0.96 | OK Holcus lanatus 0.97 |
| Carex_flacca_1.jpg | Carex flacca |  | 2.5 | OK Carex flacca 0.62 | OK Carex flacca 1.00 |
| Neottia_ovata_1.jpg | Neottia ovata |  | 4.3 | X Lycopus europaeus 0.58 | OK Neottia ovata 1.00 |
| Galium_odoratum_1.jpg | Galium odoratum |  | 7.2 | OK Galium odoratum 0.99 | OK Galium odoratum 1.00 |
| Rubus_idaeus_1.jpg | Rubus idaeus |  | 46.3 | OK Rubus idaeus 0.58 | OK Rubus idaeus 0.92 |
| Arabidopsis_thaliana_1.jpg | Arabidopsis thaliana |  | 1.4 | X Castanea sativa 0.12 | OK Arabidopsis thaliana 1.00 |
| Melissa_officinalis_1.jpg | Melissa officinalis |  | 0.3 | OK Melissa officinalis 0.45 | OK Melissa officinalis 1.00 |
| Helleborus_foetidus_1.jpg | Helleborus foetidus |  | 90.7 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Petasites_hybridus_1.jpg | Petasites hybridus |  | 12.3 | OK Petasites hybridus 0.96 | OK Petasites hybridus 1.00 |

## Compared with the previous report (2026-10-30, web-rennes-inat-dated)
**The candidate list changed (214 -> 225 species): a drop can come from new look-alike species on the list rather than from the model. Compare with care.**
- catalog / crop: top-1 109/130 → 105/130  **REGRESSION**
- catalog / full: top-1 130/130 → 123/130  **REGRESSION**
- catalog+truth / crop: top-1 109/130 → 111/130
- catalog+truth / full: top-1 130/130 → 130/130
