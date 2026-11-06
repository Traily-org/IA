# Eval report — 2026-10-30 — web-rennes-inat-dated

- Photos: 130 (labels from labels.csv)
- Candidate list: `data/species_lists/catalog.txt` (214 species)
- Confidence threshold for abstaining: 0.5 (placeholder)
- Device: cuda
- Labels are PlantNet suggestions given by the team, not expert-verified: treat the second word of each name as uncertain (genus-level is more reliable).

## Setting: catalog
True species on the candidate list for 130/130 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 109/130 (84%) | 112/130 (86%) | 110/130 (85%) | 0.951 / 0.353 | 0 | 105/109 (96%) |
| full | 130/130 (100%) | 130/130 (100%) | 130/130 (100%) | 0.976 / None | 0 | 129/129 (100%) |
| hybrid>=2 | 127/130 (98%) | 128/130 (98%) | 128/130 (98%) | 0.969 / 0.498 | 0 | 125/127 (98%) |
| hybrid>=5 | 129/130 (99%) | 130/130 (100%) | 130/130 (100%) | 0.978 / 0.585 | 0 | 128/129 (99%) |
| hybrid>=10 | 129/130 (99%) | 130/130 (100%) | 130/130 (100%) | 0.978 / 0.585 | 0 | 128/129 (99%) |
| hybrid>=20 | 130/130 (100%) | 130/130 (100%) | 130/130 (100%) | 0.979 / None | 0 | 129/129 (100%) |
| hybrid>=40 | 130/130 (100%) | 130/130 (100%) | 130/130 (100%) | 0.979 / None | 0 | 129/129 (100%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 21 | 4 |
| 0.50-0.80 | 11 | 7 |
| 0.80-0.95 | 6 | 6 |
| 0.95-1.00 | 92 | 92 |

Could BioCLIP have seen these photos? Split by iNaturalist upload date (cutoff 2024-06-01: BioCLIP 2 training data ends with a GBIF snapshot of 2024-05-01):

| subset | photos | full top-1 | full top-3 | crop top-1 | crop top-3 |
|---|---|---|---|---|---|
| uploaded on/after 2024-06-01 (cannot be in training data) | 103 | 103/103 (100%) | 103/103 (100%) | 85/103 (83%) | 88/103 (85%) |
| uploaded earlier (may be in training data) | 27 | 27/27 (100%) | 27/27 (100%) | 24/27 (89%) | 24/27 (89%) |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Eupatorium cannabinum → Ophioglossum vulgatum ×1, Digitalis purpurea → Ecballium elaterium ×1, Urtica dioica → Viburnum lantana ×1, Quercus robur → Quercus petraea ×1, Ulex europaeus → Gentiana lutea ×1, Ulex europaeus → Scorzonera humilis ×1, Achillea millefolium → Thymus vulgaris ×1, Plantago lanceolata → Hedera helix ×1
- full: none

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Asplenium_scolopendrium_1.jpg | Asplenium scolopendrium |  | 46.0 | OK Asplenium scolopendrium 1.00 | OK Asplenium scolopendrium 1.00 |
| Eupatorium_cannabinum_1.jpg | Eupatorium cannabinum |  | 0.7 | X Ophioglossum vulgatum 0.38 | OK Eupatorium cannabinum 1.00 |
| Ilex_aquifolium_1.jpg | Ilex aquifolium |  | 94.7 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Ilex_aquifolium_2.jpg | Ilex aquifolium |  | 93.9 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Orchis_mascula_1.jpg | Orchis mascula |  | 7.8 | OK Orchis mascula 1.00 | OK Orchis mascula 1.00 |
| Orchis_mascula_2.jpg | Orchis mascula |  | 11.5 | OK Orchis mascula 1.00 | OK Orchis mascula 0.99 |
| Pteridium_aquilinum_1.jpg | Pteridium aquilinum |  | 53.4 | OK Pteridium aquilinum 1.00 | OK Pteridium aquilinum 0.99 |
| Pteridium_aquilinum_2.jpg | Pteridium aquilinum |  | 95.7 | OK Pteridium aquilinum 1.00 | OK Pteridium aquilinum 1.00 |
| Fagus_sylvatica_1.jpg | Fagus sylvatica |  | 93.6 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Fagus_sylvatica_2.jpg | Fagus sylvatica |  | 16.2 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Cornus_sanguinea_1.jpg | Cornus sanguinea |  | 10.1 | OK Cornus sanguinea 1.00 | OK Cornus sanguinea 1.00 |
| Prunus_laurocerasus_1.jpg | Prunus laurocerasus |  | 76.7 | OK Prunus laurocerasus 1.00 | OK Prunus laurocerasus 1.00 |
| Prunus_laurocerasus_2.jpg | Prunus laurocerasus |  | 9.9 | OK Prunus laurocerasus 1.00 | OK Prunus laurocerasus 1.00 |
| Ajuga_reptans_1.jpg | Ajuga reptans |  | 3.1 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_2.jpg | Ajuga reptans |  | 3.7 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Dryopteris_filix-mas_1.jpg | Dryopteris filix-mas |  | 77.0 | OK Dryopteris filix-mas 1.00 | OK Dryopteris filix-mas 0.99 |
| Rabelera_holostea_1.jpg | Rabelera holostea |  | 1.2 | OK Rabelera holostea 1.00 | OK Rabelera holostea 1.00 |
| Rabelera_holostea_2.jpg | Rabelera holostea |  | 22.7 | OK Rabelera holostea 1.00 | OK Rabelera holostea 1.00 |
| Corylus_avellana_1.jpg | Corylus avellana |  | 46.9 | OK Corylus avellana 1.00 | OK Corylus avellana 1.00 |
| Corylus_avellana_2.jpg | Corylus avellana |  | 5.0 | OK Corylus avellana 1.00 | OK Corylus avellana 1.00 |
| Ligustrum_vulgare_1.jpg | Ligustrum vulgare |  | 75.1 | OK Ligustrum vulgare 0.94 | OK Ligustrum vulgare 0.81 |
| Phragmites_australis_1.jpg | Phragmites australis |  | 58.8 | OK Phragmites australis 0.95 | OK Phragmites australis 0.82 |
| Prunus_spinosa_1.jpg | Prunus spinosa |  | 98.0 | OK Prunus spinosa 1.00 | OK Prunus spinosa 1.00 |
| Digitalis_purpurea_1.jpg | Digitalis purpurea |  | 11.6 | OK Digitalis purpurea 0.76 | OK Digitalis purpurea 0.99 |
| Digitalis_purpurea_2.jpg | Digitalis purpurea |  | 0.2 | X Ecballium elaterium 0.55 | OK Digitalis purpurea 1.00 |
| Urtica_dioica_1.jpg | Urtica dioica |  | 79.7 | OK Urtica dioica 1.00 | OK Urtica dioica 1.00 |
| Urtica_dioica_2.jpg | Urtica dioica |  | 1.0 | X Viburnum lantana 0.09 | OK Urtica dioica 1.00 |
| Solanum_dulcamara_1.jpg | Solanum dulcamara |  | 14.6 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Solanum_dulcamara_2.jpg | Solanum dulcamara |  | 97.3 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Sedum_acre_1.jpg | Sedum acre |  | 64.2 | OK Sedum acre 0.99 | OK Sedum acre 0.99 |
| Quercus_robur_1.jpg | Quercus robur |  | 12.0 | X Quercus petraea 0.58 | OK Quercus robur 0.81 |
| Quercus_robur_2.jpg | Quercus robur |  | 5.2 | OK Quercus robur 0.83 | OK Quercus robur 0.81 |
| Ulex_europaeus_1.jpg | Ulex europaeus |  | 0.1 | X Gentiana lutea 0.15 | OK Ulex europaeus 0.99 |
| Ulex_europaeus_2.jpg | Ulex europaeus |  | 0.2 | X Scorzonera humilis 0.17 | OK Ulex europaeus 0.95 |
| Cirsium_vulgare_1.jpg | Cirsium vulgare |  | 0.5 | OK Cirsium vulgare 0.49 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_2.jpg | Cirsium vulgare |  | 3.4 | OK Cirsium vulgare 1.00 | OK Cirsium vulgare 1.00 |
| Hyacinthoides_non-scripta_1.jpg | Hyacinthoides non-scripta |  | 4.7 | OK Hyacinthoides non-scripta 1.00 | OK Hyacinthoides non-scripta 1.00 |
| Achillea_millefolium_1.jpg | Achillea millefolium |  | 0.4 | X Thymus vulgaris 0.29 | OK Achillea millefolium 1.00 |
| Trifolium_pratense_1.jpg | Trifolium pratense |  | 5.7 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Trifolium_pratense_2.jpg | Trifolium pratense |  | 14.2 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Castanea_sativa_1.jpg | Castanea sativa |  | 1.4 | OK Castanea sativa 1.00 | OK Castanea sativa 0.62 |
| Castanea_sativa_2.jpg | Castanea sativa |  | 1.2 | OK Castanea sativa 0.99 | OK Castanea sativa 1.00 |
| Plantago_lanceolata_1.jpg | Plantago lanceolata |  | 0.4 | X Hedera helix 0.44 | OK Plantago lanceolata 1.00 |
| Plantago_lanceolata_2.jpg | Plantago lanceolata |  | 3.9 | X Scorzonera humilis 0.67 | OK Plantago lanceolata 0.99 |
| Acer_pseudoplatanus_1.jpg | Acer pseudoplatanus |  | 12.9 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Acer_pseudoplatanus_2.jpg | Acer pseudoplatanus |  | 40.5 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Crataegus_monogyna_1.jpg | Crataegus monogyna |  | 5.1 | OK Crataegus monogyna 1.00 | OK Crataegus monogyna 1.00 |
| Crataegus_monogyna_2.jpg | Crataegus monogyna |  | 13.0 | OK Crataegus monogyna 1.00 | OK Crataegus monogyna 1.00 |
| Sambucus_ebulus_1.jpg | Sambucus ebulus |  | 6.6 | OK Sambucus ebulus 1.00 | OK Sambucus ebulus 1.00 |
| Echium_vulgare_1.jpg | Echium vulgare |  | 66.8 | OK Echium vulgare 1.00 | OK Echium vulgare 1.00 |
| Teucrium_scorodonia_1.jpg | Teucrium scorodonia |  | 96.7 | OK Teucrium scorodonia 0.98 | OK Teucrium scorodonia 0.98 |
| Teucrium_scorodonia_2.jpg | Teucrium scorodonia |  | 96.2 | OK Teucrium scorodonia 0.99 | OK Teucrium scorodonia 0.95 |
| Heracleum_sphondylium_1.jpg | Heracleum sphondylium |  | 3.3 | OK Heracleum sphondylium 1.00 | OK Heracleum sphondylium 1.00 |
| Heracleum_sphondylium_2.jpg | Heracleum sphondylium |  | 96.6 | OK Heracleum sphondylium 0.93 | OK Heracleum sphondylium 0.91 |
| Plantago_coronopus_1.jpg | Plantago coronopus |  | 31.5 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Plantago_coronopus_2.jpg | Plantago coronopus |  | 77.6 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Chelidonium_majus_1.jpg | Chelidonium majus |  | 1.8 | OK Chelidonium majus 0.93 | OK Chelidonium majus 1.00 |
| Chelidonium_majus_2.jpg | Chelidonium majus |  | 27.0 | OK Chelidonium majus 1.00 | OK Chelidonium majus 1.00 |
| Fraxinus_excelsior_1.jpg | Fraxinus excelsior |  | 95.7 | OK Fraxinus excelsior 0.46 | OK Fraxinus excelsior 0.39 |
| Trifolium_repens_1.jpg | Trifolium repens |  | 4.6 | OK Trifolium repens 1.00 | OK Trifolium repens 1.00 |
| Trifolium_repens_2.jpg | Trifolium repens |  | 8.1 | OK Trifolium repens 1.00 | OK Trifolium repens 1.00 |
| Geranium_dissectum_1.jpg | Geranium dissectum |  | 9.4 | OK Geranium dissectum 1.00 | OK Geranium dissectum 1.00 |
| Geranium_dissectum_2.jpg | Geranium dissectum |  | 20.0 | OK Geranium dissectum 1.00 | OK Geranium dissectum 1.00 |
| Vicia_sepium_1.jpg | Vicia sepium |  | 8.5 | OK Vicia sepium 1.00 | OK Vicia sepium 1.00 |
| Cytisus_scoparius_1.jpg | Cytisus scoparius |  | 95.9 | OK Cytisus scoparius 1.00 | OK Cytisus scoparius 0.99 |
| Asplenium_ceterach_1.jpg | Asplenium ceterach |  | 47.0 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Asplenium_ceterach_2.jpg | Asplenium ceterach |  | 91.5 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Anthoxanthum_odoratum_1.jpg | Anthoxanthum odoratum |  | 15.0 | OK Anthoxanthum odoratum 1.00 | OK Anthoxanthum odoratum 1.00 |
| Vicia_cracca_1.jpg | Vicia cracca |  | 3.6 | OK Vicia cracca 1.00 | OK Vicia cracca 1.00 |
| Medicago_lupulina_1.jpg | Medicago lupulina |  | 1.0 | OK Medicago lupulina 0.76 | OK Medicago lupulina 1.00 |
| Agrimonia_eupatoria_1.jpg | Agrimonia eupatoria |  | 1.9 | OK Agrimonia eupatoria 1.00 | OK Agrimonia eupatoria 1.00 |
| Catapodium_rigidum_1.jpg | Catapodium rigidum |  | 78.2 | OK Catapodium rigidum 1.00 | OK Catapodium rigidum 1.00 |
| Dactylis_glomerata_1.jpg | Dactylis glomerata |  | 1.2 | X Molinia caerulea 0.42 | OK Dactylis glomerata 0.99 |
| Hypericum_perforatum_1.jpg | Hypericum perforatum |  | 2.7 | OK Hypericum perforatum 1.00 | OK Hypericum perforatum 1.00 |
| Erica_cinerea_1.jpg | Erica cinerea |  | 0.3 | X Ulex europaeus 0.19 | OK Erica cinerea 0.99 |
| Erica_cinerea_2.jpg | Erica cinerea |  | 0.9 | OK Erica cinerea 0.97 | OK Erica cinerea 0.99 |
| Scorzonera_humilis_1.jpg | Scorzonera humilis |  | 2.2 | OK Scorzonera humilis 0.96 | OK Scorzonera humilis 1.00 |
| Struthiopteris_spicant_1.jpg | Struthiopteris spicant |  | 92.6 | OK Struthiopteris spicant 0.98 | OK Struthiopteris spicant 0.98 |
| Struthiopteris_spicant_2.jpg | Struthiopteris spicant |  | 58.5 | OK Struthiopteris spicant 1.00 | OK Struthiopteris spicant 1.00 |
| Phalaris_arundinacea_1.jpg | Phalaris arundinacea |  | 80.8 | OK Phalaris arundinacea 0.98 | OK Phalaris arundinacea 0.98 |
| Lotus_corniculatus_1.jpg | Lotus corniculatus |  | 1.2 | OK Lotus corniculatus 0.79 | OK Lotus corniculatus 0.97 |
| Argentina_anserina_1.jpg | Argentina anserina |  | 94.9 | OK Argentina anserina 1.00 | OK Argentina anserina 1.00 |
| Anacamptis_pyramidalis_1.jpg | Anacamptis pyramidalis |  | 8.7 | OK Anacamptis pyramidalis 0.97 | OK Anacamptis pyramidalis 0.99 |
| Anacamptis_pyramidalis_2.jpg | Anacamptis pyramidalis |  | 18.3 | OK Anacamptis pyramidalis 0.99 | OK Anacamptis pyramidalis 1.00 |
| Calluna_vulgaris_1.jpg | Calluna vulgaris |  | 97.1 | OK Calluna vulgaris 0.99 | OK Calluna vulgaris 0.99 |
| Primula_veris_1.jpg | Primula veris |  | 3.0 | OK Primula veris 1.00 | OK Primula veris 0.99 |
| Primula_veris_2.jpg | Primula veris |  | 13.8 | OK Primula veris 1.00 | OK Primula veris 1.00 |
| Bellis_perennis_1.jpg | Bellis perennis |  | 0.6 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Bellis_perennis_2.jpg | Bellis perennis |  | 8.4 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Lathyrus_pratensis_1.jpg | Lathyrus pratensis |  | 2.1 | OK Lathyrus pratensis 0.63 | OK Lathyrus pratensis 0.99 |
| Lathyrus_pratensis_2.jpg | Lathyrus pratensis |  | 1.1 | OK Lathyrus pratensis 0.80 | OK Lathyrus pratensis 0.99 |
| Dactylorhiza_maculata_1.jpg | Dactylorhiza maculata |  | 2.6 | OK Dactylorhiza maculata 0.95 | OK Dactylorhiza maculata 0.88 |
| Hedera_helix_1.jpg | Hedera helix |  | 2.3 | OK Hedera helix 0.96 | OK Hedera helix 1.00 |
| Hedera_helix_2.jpg | Hedera helix |  | 25.1 | OK Hedera helix 1.00 | OK Hedera helix 1.00 |
| Juncus_acutiflorus_1.jpg | Juncus acutiflorus |  | 0.9 | X Trifolium pratense 0.41 | OK Juncus acutiflorus 1.00 |
| Juncus_acutiflorus_2.jpg | Juncus acutiflorus |  | 0.3 | X Bupleurum baldense 0.33 | OK Juncus acutiflorus 0.98 |
| Arrhenatherum_elatius_1.jpg | Arrhenatherum elatius |  | 0.3 | X Digitalis purpurea 0.47 | OK Arrhenatherum elatius 0.98 |
| Impatiens_balfourii_1.jpg | Impatiens balfourii |  | 8.0 | OK Impatiens balfourii 1.00 | OK Impatiens balfourii 1.00 |
| Alopecurus_pratensis_1.jpg | Alopecurus pratensis |  | 0.2 | X Impatiens balfourii 0.19 | OK Alopecurus pratensis 1.00 |
| Borago_officinalis_1.jpg | Borago officinalis |  | 3.8 | OK Borago officinalis 1.00 | OK Borago officinalis 1.00 |
| Teesdalia_nudicaulis_1.jpg | Teesdalia nudicaulis |  | 1.7 | OK Teesdalia nudicaulis 1.00 | OK Teesdalia nudicaulis 1.00 |
| Teesdalia_nudicaulis_2.jpg | Teesdalia nudicaulis |  | 21.5 | OK Teesdalia nudicaulis 1.00 | OK Teesdalia nudicaulis 1.00 |
| Lotus_pedunculatus_1.jpg | Lotus pedunculatus |  | 5.3 | OK Lotus pedunculatus 0.99 | OK Lotus pedunculatus 0.98 |
| Potentilla_erecta_1.jpg | Potentilla erecta |  | 0.7 | OK Potentilla erecta 0.79 | OK Potentilla erecta 1.00 |
| Potentilla_erecta_2.jpg | Potentilla erecta |  | 25.2 | OK Potentilla erecta 0.96 | OK Potentilla erecta 0.99 |
| Alliaria_petiolata_1.jpg | Alliaria petiolata |  | 0.3 | X Bellis perennis 0.28 | OK Alliaria petiolata 0.98 |
| Galium_mollugo_1.jpg | Galium mollugo |  | 8.9 | OK Galium mollugo 1.00 | OK Galium mollugo 1.00 |
| Aulacomnium_palustre_1.jpg | Aulacomnium palustre |  | 95.2 | OK Aulacomnium palustre 1.00 | OK Aulacomnium palustre 1.00 |
| Carex_panicea_1.jpg | Carex panicea |  | 96.9 | OK Carex panicea 0.61 | OK Carex panicea 0.61 |
| Carex_hirta_1.jpg | Carex hirta |  | 2.8 | OK Carex hirta 1.00 | OK Carex hirta 1.00 |
| Viburnum_lantana_1.jpg | Viburnum lantana |  | 3.5 | OK Viburnum lantana 1.00 | OK Viburnum lantana 1.00 |
| Fagopyrum_esculentum_1.jpg | Fagopyrum esculentum |  | 26.2 | OK Fagopyrum esculentum 1.00 | OK Fagopyrum esculentum 1.00 |
| Buxus_sempervirens_1.jpg | Buxus sempervirens |  | 0.5 | X Impatiens balfourii 0.41 | OK Buxus sempervirens 1.00 |
| Sorbus_aucuparia_1.jpg | Sorbus aucuparia |  | 4.2 | OK Sorbus aucuparia 0.91 | OK Sorbus aucuparia 1.00 |
| Picris_hieracioides_1.jpg | Picris hieracioides |  | 37.0 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Picris_hieracioides_2.jpg | Picris hieracioides |  | 13.7 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Pinus_sylvestris_1.jpg | Pinus sylvestris |  | 3.4 | OK Pinus sylvestris 0.64 | OK Pinus sylvestris 0.75 |
| Molinia_caerulea_1.jpg | Molinia caerulea |  | 76.7 | OK Molinia caerulea 1.00 | OK Molinia caerulea 1.00 |
| Anthriscus_sylvestris_1.jpg | Anthriscus sylvestris |  | 0.3 | X Achillea millefolium 0.72 | OK Anthriscus sylvestris 1.00 |
| Capsella_bursa-pastoris_1.jpg | Capsella bursa-pastoris |  | 6.5 | OK Capsella bursa-pastoris 0.99 | OK Capsella bursa-pastoris 1.00 |
| Bromus_hordeaceus_1.jpg | Bromus hordeaceus |  | 45.5 | OK Bromus hordeaceus 1.00 | OK Bromus hordeaceus 1.00 |
| Holcus_lanatus_1.jpg | Holcus lanatus |  | 0.9 | OK Holcus lanatus 0.96 | OK Holcus lanatus 0.97 |
| Carex_flacca_1.jpg | Carex flacca |  | 2.1 | OK Carex flacca 0.48 | OK Carex flacca 1.00 |
| Neottia_ovata_1.jpg | Neottia ovata |  | 4.3 | X Melittis melissophyllum 0.24 | OK Neottia ovata 1.00 |
| Galium_odoratum_1.jpg | Galium odoratum |  | 7.2 | OK Galium odoratum 0.99 | OK Galium odoratum 1.00 |
| Rubus_idaeus_1.jpg | Rubus idaeus |  | 0.1 | X Hyacinthoides non-scripta 0.32 | OK Rubus idaeus 0.98 |
| Arabidopsis_thaliana_1.jpg | Arabidopsis thaliana |  | 1.4 | X Plantago coronopus 0.10 | OK Arabidopsis thaliana 1.00 |
| Melissa_officinalis_1.jpg | Melissa officinalis |  | 0.3 | OK Melissa officinalis 0.49 | OK Melissa officinalis 1.00 |
| Helleborus_foetidus_1.jpg | Helleborus foetidus |  | 90.2 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Petasites_hybridus_1.jpg | Petasites hybridus |  | 12.7 | OK Petasites hybridus 0.97 | OK Petasites hybridus 1.00 |

## Setting: catalog+truth
True species on the candidate list for 130/130 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 109/130 (84%) | 112/130 (86%) | 110/130 (85%) | 0.951 / 0.353 | 0 | 105/109 (96%) |
| full | 130/130 (100%) | 130/130 (100%) | 130/130 (100%) | 0.976 / None | 0 | 129/129 (100%) |
| hybrid>=2 | 127/130 (98%) | 128/130 (98%) | 128/130 (98%) | 0.969 / 0.498 | 0 | 125/127 (98%) |
| hybrid>=5 | 129/130 (99%) | 130/130 (100%) | 130/130 (100%) | 0.978 / 0.585 | 0 | 128/129 (99%) |
| hybrid>=10 | 129/130 (99%) | 130/130 (100%) | 130/130 (100%) | 0.978 / 0.585 | 0 | 128/129 (99%) |
| hybrid>=20 | 130/130 (100%) | 130/130 (100%) | 130/130 (100%) | 0.979 / None | 0 | 129/129 (100%) |
| hybrid>=40 | 130/130 (100%) | 130/130 (100%) | 130/130 (100%) | 0.979 / None | 0 | 129/129 (100%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 21 | 4 |
| 0.50-0.80 | 11 | 7 |
| 0.80-0.95 | 6 | 6 |
| 0.95-1.00 | 92 | 92 |

Could BioCLIP have seen these photos? Split by iNaturalist upload date (cutoff 2024-06-01: BioCLIP 2 training data ends with a GBIF snapshot of 2024-05-01):

| subset | photos | full top-1 | full top-3 | crop top-1 | crop top-3 |
|---|---|---|---|---|---|
| uploaded on/after 2024-06-01 (cannot be in training data) | 103 | 103/103 (100%) | 103/103 (100%) | 85/103 (83%) | 88/103 (85%) |
| uploaded earlier (may be in training data) | 27 | 27/27 (100%) | 27/27 (100%) | 24/27 (89%) | 24/27 (89%) |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Eupatorium cannabinum → Ophioglossum vulgatum ×1, Digitalis purpurea → Ecballium elaterium ×1, Urtica dioica → Viburnum lantana ×1, Quercus robur → Quercus petraea ×1, Ulex europaeus → Gentiana lutea ×1, Ulex europaeus → Scorzonera humilis ×1, Achillea millefolium → Thymus vulgaris ×1, Plantago lanceolata → Hedera helix ×1
- full: none

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Asplenium_scolopendrium_1.jpg | Asplenium scolopendrium |  | 46.0 | OK Asplenium scolopendrium 1.00 | OK Asplenium scolopendrium 1.00 |
| Eupatorium_cannabinum_1.jpg | Eupatorium cannabinum |  | 0.7 | X Ophioglossum vulgatum 0.38 | OK Eupatorium cannabinum 1.00 |
| Ilex_aquifolium_1.jpg | Ilex aquifolium |  | 94.7 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Ilex_aquifolium_2.jpg | Ilex aquifolium |  | 93.9 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Orchis_mascula_1.jpg | Orchis mascula |  | 7.8 | OK Orchis mascula 1.00 | OK Orchis mascula 1.00 |
| Orchis_mascula_2.jpg | Orchis mascula |  | 11.5 | OK Orchis mascula 1.00 | OK Orchis mascula 0.99 |
| Pteridium_aquilinum_1.jpg | Pteridium aquilinum |  | 53.4 | OK Pteridium aquilinum 1.00 | OK Pteridium aquilinum 0.99 |
| Pteridium_aquilinum_2.jpg | Pteridium aquilinum |  | 95.7 | OK Pteridium aquilinum 1.00 | OK Pteridium aquilinum 1.00 |
| Fagus_sylvatica_1.jpg | Fagus sylvatica |  | 93.6 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Fagus_sylvatica_2.jpg | Fagus sylvatica |  | 16.2 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Cornus_sanguinea_1.jpg | Cornus sanguinea |  | 10.1 | OK Cornus sanguinea 1.00 | OK Cornus sanguinea 1.00 |
| Prunus_laurocerasus_1.jpg | Prunus laurocerasus |  | 76.7 | OK Prunus laurocerasus 1.00 | OK Prunus laurocerasus 1.00 |
| Prunus_laurocerasus_2.jpg | Prunus laurocerasus |  | 9.9 | OK Prunus laurocerasus 1.00 | OK Prunus laurocerasus 1.00 |
| Ajuga_reptans_1.jpg | Ajuga reptans |  | 3.1 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_2.jpg | Ajuga reptans |  | 3.7 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Dryopteris_filix-mas_1.jpg | Dryopteris filix-mas |  | 77.0 | OK Dryopteris filix-mas 1.00 | OK Dryopteris filix-mas 0.99 |
| Rabelera_holostea_1.jpg | Rabelera holostea |  | 1.2 | OK Rabelera holostea 1.00 | OK Rabelera holostea 1.00 |
| Rabelera_holostea_2.jpg | Rabelera holostea |  | 22.7 | OK Rabelera holostea 1.00 | OK Rabelera holostea 1.00 |
| Corylus_avellana_1.jpg | Corylus avellana |  | 46.9 | OK Corylus avellana 1.00 | OK Corylus avellana 1.00 |
| Corylus_avellana_2.jpg | Corylus avellana |  | 5.0 | OK Corylus avellana 1.00 | OK Corylus avellana 1.00 |
| Ligustrum_vulgare_1.jpg | Ligustrum vulgare |  | 75.1 | OK Ligustrum vulgare 0.94 | OK Ligustrum vulgare 0.81 |
| Phragmites_australis_1.jpg | Phragmites australis |  | 58.8 | OK Phragmites australis 0.95 | OK Phragmites australis 0.82 |
| Prunus_spinosa_1.jpg | Prunus spinosa |  | 98.0 | OK Prunus spinosa 1.00 | OK Prunus spinosa 1.00 |
| Digitalis_purpurea_1.jpg | Digitalis purpurea |  | 11.6 | OK Digitalis purpurea 0.76 | OK Digitalis purpurea 0.99 |
| Digitalis_purpurea_2.jpg | Digitalis purpurea |  | 0.2 | X Ecballium elaterium 0.55 | OK Digitalis purpurea 1.00 |
| Urtica_dioica_1.jpg | Urtica dioica |  | 79.7 | OK Urtica dioica 1.00 | OK Urtica dioica 1.00 |
| Urtica_dioica_2.jpg | Urtica dioica |  | 1.0 | X Viburnum lantana 0.09 | OK Urtica dioica 1.00 |
| Solanum_dulcamara_1.jpg | Solanum dulcamara |  | 14.6 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Solanum_dulcamara_2.jpg | Solanum dulcamara |  | 97.3 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Sedum_acre_1.jpg | Sedum acre |  | 64.2 | OK Sedum acre 0.99 | OK Sedum acre 0.99 |
| Quercus_robur_1.jpg | Quercus robur |  | 12.0 | X Quercus petraea 0.58 | OK Quercus robur 0.81 |
| Quercus_robur_2.jpg | Quercus robur |  | 5.2 | OK Quercus robur 0.83 | OK Quercus robur 0.81 |
| Ulex_europaeus_1.jpg | Ulex europaeus |  | 0.1 | X Gentiana lutea 0.15 | OK Ulex europaeus 0.99 |
| Ulex_europaeus_2.jpg | Ulex europaeus |  | 0.2 | X Scorzonera humilis 0.17 | OK Ulex europaeus 0.95 |
| Cirsium_vulgare_1.jpg | Cirsium vulgare |  | 0.5 | OK Cirsium vulgare 0.49 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_2.jpg | Cirsium vulgare |  | 3.4 | OK Cirsium vulgare 1.00 | OK Cirsium vulgare 1.00 |
| Hyacinthoides_non-scripta_1.jpg | Hyacinthoides non-scripta |  | 4.7 | OK Hyacinthoides non-scripta 1.00 | OK Hyacinthoides non-scripta 1.00 |
| Achillea_millefolium_1.jpg | Achillea millefolium |  | 0.4 | X Thymus vulgaris 0.29 | OK Achillea millefolium 1.00 |
| Trifolium_pratense_1.jpg | Trifolium pratense |  | 5.7 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Trifolium_pratense_2.jpg | Trifolium pratense |  | 14.2 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Castanea_sativa_1.jpg | Castanea sativa |  | 1.4 | OK Castanea sativa 1.00 | OK Castanea sativa 0.62 |
| Castanea_sativa_2.jpg | Castanea sativa |  | 1.2 | OK Castanea sativa 0.99 | OK Castanea sativa 1.00 |
| Plantago_lanceolata_1.jpg | Plantago lanceolata |  | 0.4 | X Hedera helix 0.44 | OK Plantago lanceolata 1.00 |
| Plantago_lanceolata_2.jpg | Plantago lanceolata |  | 3.9 | X Scorzonera humilis 0.67 | OK Plantago lanceolata 0.99 |
| Acer_pseudoplatanus_1.jpg | Acer pseudoplatanus |  | 12.9 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Acer_pseudoplatanus_2.jpg | Acer pseudoplatanus |  | 40.5 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Crataegus_monogyna_1.jpg | Crataegus monogyna |  | 5.1 | OK Crataegus monogyna 1.00 | OK Crataegus monogyna 1.00 |
| Crataegus_monogyna_2.jpg | Crataegus monogyna |  | 13.0 | OK Crataegus monogyna 1.00 | OK Crataegus monogyna 1.00 |
| Sambucus_ebulus_1.jpg | Sambucus ebulus |  | 6.6 | OK Sambucus ebulus 1.00 | OK Sambucus ebulus 1.00 |
| Echium_vulgare_1.jpg | Echium vulgare |  | 66.8 | OK Echium vulgare 1.00 | OK Echium vulgare 1.00 |
| Teucrium_scorodonia_1.jpg | Teucrium scorodonia |  | 96.7 | OK Teucrium scorodonia 0.98 | OK Teucrium scorodonia 0.98 |
| Teucrium_scorodonia_2.jpg | Teucrium scorodonia |  | 96.2 | OK Teucrium scorodonia 0.99 | OK Teucrium scorodonia 0.95 |
| Heracleum_sphondylium_1.jpg | Heracleum sphondylium |  | 3.3 | OK Heracleum sphondylium 1.00 | OK Heracleum sphondylium 1.00 |
| Heracleum_sphondylium_2.jpg | Heracleum sphondylium |  | 96.6 | OK Heracleum sphondylium 0.93 | OK Heracleum sphondylium 0.91 |
| Plantago_coronopus_1.jpg | Plantago coronopus |  | 31.5 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Plantago_coronopus_2.jpg | Plantago coronopus |  | 77.6 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Chelidonium_majus_1.jpg | Chelidonium majus |  | 1.8 | OK Chelidonium majus 0.93 | OK Chelidonium majus 1.00 |
| Chelidonium_majus_2.jpg | Chelidonium majus |  | 27.0 | OK Chelidonium majus 1.00 | OK Chelidonium majus 1.00 |
| Fraxinus_excelsior_1.jpg | Fraxinus excelsior |  | 95.7 | OK Fraxinus excelsior 0.46 | OK Fraxinus excelsior 0.39 |
| Trifolium_repens_1.jpg | Trifolium repens |  | 4.6 | OK Trifolium repens 1.00 | OK Trifolium repens 1.00 |
| Trifolium_repens_2.jpg | Trifolium repens |  | 8.1 | OK Trifolium repens 1.00 | OK Trifolium repens 1.00 |
| Geranium_dissectum_1.jpg | Geranium dissectum |  | 9.4 | OK Geranium dissectum 1.00 | OK Geranium dissectum 1.00 |
| Geranium_dissectum_2.jpg | Geranium dissectum |  | 20.0 | OK Geranium dissectum 1.00 | OK Geranium dissectum 1.00 |
| Vicia_sepium_1.jpg | Vicia sepium |  | 8.5 | OK Vicia sepium 1.00 | OK Vicia sepium 1.00 |
| Cytisus_scoparius_1.jpg | Cytisus scoparius |  | 95.9 | OK Cytisus scoparius 1.00 | OK Cytisus scoparius 0.99 |
| Asplenium_ceterach_1.jpg | Asplenium ceterach |  | 47.0 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Asplenium_ceterach_2.jpg | Asplenium ceterach |  | 91.5 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Anthoxanthum_odoratum_1.jpg | Anthoxanthum odoratum |  | 15.0 | OK Anthoxanthum odoratum 1.00 | OK Anthoxanthum odoratum 1.00 |
| Vicia_cracca_1.jpg | Vicia cracca |  | 3.6 | OK Vicia cracca 1.00 | OK Vicia cracca 1.00 |
| Medicago_lupulina_1.jpg | Medicago lupulina |  | 1.0 | OK Medicago lupulina 0.76 | OK Medicago lupulina 1.00 |
| Agrimonia_eupatoria_1.jpg | Agrimonia eupatoria |  | 1.9 | OK Agrimonia eupatoria 1.00 | OK Agrimonia eupatoria 1.00 |
| Catapodium_rigidum_1.jpg | Catapodium rigidum |  | 78.2 | OK Catapodium rigidum 1.00 | OK Catapodium rigidum 1.00 |
| Dactylis_glomerata_1.jpg | Dactylis glomerata |  | 1.2 | X Molinia caerulea 0.42 | OK Dactylis glomerata 0.99 |
| Hypericum_perforatum_1.jpg | Hypericum perforatum |  | 2.7 | OK Hypericum perforatum 1.00 | OK Hypericum perforatum 1.00 |
| Erica_cinerea_1.jpg | Erica cinerea |  | 0.3 | X Ulex europaeus 0.19 | OK Erica cinerea 0.99 |
| Erica_cinerea_2.jpg | Erica cinerea |  | 0.9 | OK Erica cinerea 0.97 | OK Erica cinerea 0.99 |
| Scorzonera_humilis_1.jpg | Scorzonera humilis |  | 2.2 | OK Scorzonera humilis 0.96 | OK Scorzonera humilis 1.00 |
| Struthiopteris_spicant_1.jpg | Struthiopteris spicant |  | 92.6 | OK Struthiopteris spicant 0.98 | OK Struthiopteris spicant 0.98 |
| Struthiopteris_spicant_2.jpg | Struthiopteris spicant |  | 58.5 | OK Struthiopteris spicant 1.00 | OK Struthiopteris spicant 1.00 |
| Phalaris_arundinacea_1.jpg | Phalaris arundinacea |  | 80.8 | OK Phalaris arundinacea 0.98 | OK Phalaris arundinacea 0.98 |
| Lotus_corniculatus_1.jpg | Lotus corniculatus |  | 1.2 | OK Lotus corniculatus 0.79 | OK Lotus corniculatus 0.97 |
| Argentina_anserina_1.jpg | Argentina anserina |  | 94.9 | OK Argentina anserina 1.00 | OK Argentina anserina 1.00 |
| Anacamptis_pyramidalis_1.jpg | Anacamptis pyramidalis |  | 8.7 | OK Anacamptis pyramidalis 0.97 | OK Anacamptis pyramidalis 0.99 |
| Anacamptis_pyramidalis_2.jpg | Anacamptis pyramidalis |  | 18.3 | OK Anacamptis pyramidalis 0.99 | OK Anacamptis pyramidalis 1.00 |
| Calluna_vulgaris_1.jpg | Calluna vulgaris |  | 97.1 | OK Calluna vulgaris 0.99 | OK Calluna vulgaris 0.99 |
| Primula_veris_1.jpg | Primula veris |  | 3.0 | OK Primula veris 1.00 | OK Primula veris 0.99 |
| Primula_veris_2.jpg | Primula veris |  | 13.8 | OK Primula veris 1.00 | OK Primula veris 1.00 |
| Bellis_perennis_1.jpg | Bellis perennis |  | 0.6 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Bellis_perennis_2.jpg | Bellis perennis |  | 8.4 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Lathyrus_pratensis_1.jpg | Lathyrus pratensis |  | 2.1 | OK Lathyrus pratensis 0.63 | OK Lathyrus pratensis 0.99 |
| Lathyrus_pratensis_2.jpg | Lathyrus pratensis |  | 1.1 | OK Lathyrus pratensis 0.80 | OK Lathyrus pratensis 0.99 |
| Dactylorhiza_maculata_1.jpg | Dactylorhiza maculata |  | 2.6 | OK Dactylorhiza maculata 0.95 | OK Dactylorhiza maculata 0.88 |
| Hedera_helix_1.jpg | Hedera helix |  | 2.3 | OK Hedera helix 0.96 | OK Hedera helix 1.00 |
| Hedera_helix_2.jpg | Hedera helix |  | 25.1 | OK Hedera helix 1.00 | OK Hedera helix 1.00 |
| Juncus_acutiflorus_1.jpg | Juncus acutiflorus |  | 0.9 | X Trifolium pratense 0.41 | OK Juncus acutiflorus 1.00 |
| Juncus_acutiflorus_2.jpg | Juncus acutiflorus |  | 0.3 | X Bupleurum baldense 0.33 | OK Juncus acutiflorus 0.98 |
| Arrhenatherum_elatius_1.jpg | Arrhenatherum elatius |  | 0.3 | X Digitalis purpurea 0.47 | OK Arrhenatherum elatius 0.98 |
| Impatiens_balfourii_1.jpg | Impatiens balfourii |  | 8.0 | OK Impatiens balfourii 1.00 | OK Impatiens balfourii 1.00 |
| Alopecurus_pratensis_1.jpg | Alopecurus pratensis |  | 0.2 | X Impatiens balfourii 0.19 | OK Alopecurus pratensis 1.00 |
| Borago_officinalis_1.jpg | Borago officinalis |  | 3.8 | OK Borago officinalis 1.00 | OK Borago officinalis 1.00 |
| Teesdalia_nudicaulis_1.jpg | Teesdalia nudicaulis |  | 1.7 | OK Teesdalia nudicaulis 1.00 | OK Teesdalia nudicaulis 1.00 |
| Teesdalia_nudicaulis_2.jpg | Teesdalia nudicaulis |  | 21.5 | OK Teesdalia nudicaulis 1.00 | OK Teesdalia nudicaulis 1.00 |
| Lotus_pedunculatus_1.jpg | Lotus pedunculatus |  | 5.3 | OK Lotus pedunculatus 0.99 | OK Lotus pedunculatus 0.98 |
| Potentilla_erecta_1.jpg | Potentilla erecta |  | 0.7 | OK Potentilla erecta 0.79 | OK Potentilla erecta 1.00 |
| Potentilla_erecta_2.jpg | Potentilla erecta |  | 25.2 | OK Potentilla erecta 0.96 | OK Potentilla erecta 0.99 |
| Alliaria_petiolata_1.jpg | Alliaria petiolata |  | 0.3 | X Bellis perennis 0.28 | OK Alliaria petiolata 0.98 |
| Galium_mollugo_1.jpg | Galium mollugo |  | 8.9 | OK Galium mollugo 1.00 | OK Galium mollugo 1.00 |
| Aulacomnium_palustre_1.jpg | Aulacomnium palustre |  | 95.2 | OK Aulacomnium palustre 1.00 | OK Aulacomnium palustre 1.00 |
| Carex_panicea_1.jpg | Carex panicea |  | 96.9 | OK Carex panicea 0.61 | OK Carex panicea 0.61 |
| Carex_hirta_1.jpg | Carex hirta |  | 2.8 | OK Carex hirta 1.00 | OK Carex hirta 1.00 |
| Viburnum_lantana_1.jpg | Viburnum lantana |  | 3.5 | OK Viburnum lantana 1.00 | OK Viburnum lantana 1.00 |
| Fagopyrum_esculentum_1.jpg | Fagopyrum esculentum |  | 26.2 | OK Fagopyrum esculentum 1.00 | OK Fagopyrum esculentum 1.00 |
| Buxus_sempervirens_1.jpg | Buxus sempervirens |  | 0.5 | X Impatiens balfourii 0.41 | OK Buxus sempervirens 1.00 |
| Sorbus_aucuparia_1.jpg | Sorbus aucuparia |  | 4.2 | OK Sorbus aucuparia 0.91 | OK Sorbus aucuparia 1.00 |
| Picris_hieracioides_1.jpg | Picris hieracioides |  | 37.0 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Picris_hieracioides_2.jpg | Picris hieracioides |  | 13.7 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Pinus_sylvestris_1.jpg | Pinus sylvestris |  | 3.4 | OK Pinus sylvestris 0.64 | OK Pinus sylvestris 0.75 |
| Molinia_caerulea_1.jpg | Molinia caerulea |  | 76.7 | OK Molinia caerulea 1.00 | OK Molinia caerulea 1.00 |
| Anthriscus_sylvestris_1.jpg | Anthriscus sylvestris |  | 0.3 | X Achillea millefolium 0.72 | OK Anthriscus sylvestris 1.00 |
| Capsella_bursa-pastoris_1.jpg | Capsella bursa-pastoris |  | 6.5 | OK Capsella bursa-pastoris 0.99 | OK Capsella bursa-pastoris 1.00 |
| Bromus_hordeaceus_1.jpg | Bromus hordeaceus |  | 45.5 | OK Bromus hordeaceus 1.00 | OK Bromus hordeaceus 1.00 |
| Holcus_lanatus_1.jpg | Holcus lanatus |  | 0.9 | OK Holcus lanatus 0.96 | OK Holcus lanatus 0.97 |
| Carex_flacca_1.jpg | Carex flacca |  | 2.1 | OK Carex flacca 0.48 | OK Carex flacca 1.00 |
| Neottia_ovata_1.jpg | Neottia ovata |  | 4.3 | X Melittis melissophyllum 0.24 | OK Neottia ovata 1.00 |
| Galium_odoratum_1.jpg | Galium odoratum |  | 7.2 | OK Galium odoratum 0.99 | OK Galium odoratum 1.00 |
| Rubus_idaeus_1.jpg | Rubus idaeus |  | 0.1 | X Hyacinthoides non-scripta 0.32 | OK Rubus idaeus 0.98 |
| Arabidopsis_thaliana_1.jpg | Arabidopsis thaliana |  | 1.4 | X Plantago coronopus 0.10 | OK Arabidopsis thaliana 1.00 |
| Melissa_officinalis_1.jpg | Melissa officinalis |  | 0.3 | OK Melissa officinalis 0.49 | OK Melissa officinalis 1.00 |
| Helleborus_foetidus_1.jpg | Helleborus foetidus |  | 90.2 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Petasites_hybridus_1.jpg | Petasites hybridus |  | 12.7 | OK Petasites hybridus 0.97 | OK Petasites hybridus 1.00 |

## Compared with the previous report (2026-10-15, web-rennes-inat-dated)
- catalog / crop: top-1 80/130 → 109/130
- catalog / full: top-1 114/130 → 130/130
- catalog+truth / crop: top-1 80/130 → 109/130
- catalog+truth / full: top-1 114/130 → 130/130
