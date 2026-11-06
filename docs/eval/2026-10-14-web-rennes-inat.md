# Eval report — 2026-10-14 — web-rennes-inat

- Photos: 130 (labels from labels.csv)
- Candidate list: `data/species_lists/catalog.txt` (214 species)
- Confidence threshold for abstaining: 0.5 (placeholder)
- Device: cuda
- Labels are PlantNet suggestions given by the team, not expert-verified: treat the second word of each name as uncertain (genus-level is more reliable).

## Setting: catalog
True species on the candidate list for 130/130 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 80/130 (62%) | 92/130 (71%) | 80/130 (62%) | 0.939 / 0.592 | 4 | 77/107 (72%) |
| full | 114/130 (88%) | 126/130 (97%) | 115/130 (88%) | 0.948 / 0.674 | 4 | 112/125 (90%) |
| hybrid>=2 | 98/130 (75%) | 107/130 (82%) | 98/130 (75%) | 0.942 / 0.587 | 2 | 95/115 (83%) |
| hybrid>=5 | 107/130 (82%) | 117/130 (90%) | 107/130 (82%) | 0.946 / 0.634 | 2 | 104/121 (86%) |
| hybrid>=10 | 110/130 (85%) | 120/130 (92%) | 110/130 (85%) | 0.948 / 0.643 | 2 | 108/123 (88%) |
| hybrid>=20 | 113/130 (87%) | 125/130 (96%) | 114/130 (88%) | 0.951 / 0.629 | 2 | 111/124 (90%) |
| hybrid>=40 | 114/130 (88%) | 125/130 (96%) | 115/130 (88%) | 0.954 / 0.618 | 2 | 112/124 (90%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 18 | 3 |
| 0.50-0.80 | 26 | 5 |
| 0.80-0.95 | 24 | 16 |
| 0.95-1.00 | 57 | 56 |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Pteridium aquilinum → Betula pendula ×1, Pteridium aquilinum → Dryopteris filix-mas ×1, Fagus sylvatica → Carex echinata ×1, Cornus sanguinea → Neottia ovata ×1, Prunus laurocerasus → Asplenium scolopendrium ×1, Ajuga reptans → Hedera helix ×1, Ajuga reptans → Corylus avellana ×1, Rabelera holostea → Bellis perennis ×1
- full: Asplenium scolopendrium → Struthiopteris spicant ×1, Orchis mascula → Anacamptis pyramidalis ×1, Prunus laurocerasus → Ligustrum vulgare ×1, Corylus avellana → Alnus alnobetula ×1, Ligustrum vulgare → Buxus sempervirens ×1, Ulex europaeus → Cytisus scoparius ×1, Plantago lanceolata → Scorzonera humilis ×1, Heracleum sphondylium → Bupleurum fruticosum ×1

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Asplenium_scolopendrium_1.jpg | Asplenium scolopendrium |  | 43.8 | OK Asplenium scolopendrium 0.64 | X Struthiopteris spicant 0.85 |
| Eupatorium_cannabinum_1.jpg | Eupatorium cannabinum |  | 26.8 | OK Eupatorium cannabinum 1.00 | OK Eupatorium cannabinum 1.00 |
| Ilex_aquifolium_1.jpg | Ilex aquifolium |  | 96.2 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Ilex_aquifolium_2.jpg | Ilex aquifolium |  | 98.1 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Orchis_mascula_1.jpg | Orchis mascula |  | 12.9 | OK Orchis mascula 0.92 | OK Orchis mascula 0.97 |
| Orchis_mascula_2.jpg | Orchis mascula |  | 10.8 | OK Orchis mascula 0.89 | X Anacamptis pyramidalis 0.66 |
| Pteridium_aquilinum_1.jpg | Pteridium aquilinum |  | 0.4 | X Betula pendula 0.19 | OK Pteridium aquilinum 1.00 |
| Pteridium_aquilinum_2.jpg | Pteridium aquilinum |  | 98.0 | X Dryopteris filix-mas 0.67 | OK Pteridium aquilinum 0.50 |
| Fagus_sylvatica_1.jpg | Fagus sylvatica |  | 3.3 | X Carex echinata 0.16 | OK Fagus sylvatica 1.00 |
| Fagus_sylvatica_2.jpg | Fagus sylvatica |  | 16.3 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Cornus_sanguinea_1.jpg | Cornus sanguinea |  | 3.9 | X Neottia ovata 0.70 | OK Cornus sanguinea 0.85 |
| Prunus_laurocerasus_1.jpg | Prunus laurocerasus |  | 1.2 | X Asplenium scolopendrium 0.86 | X Ligustrum vulgare 0.48 |
| Prunus_laurocerasus_2.jpg | Prunus laurocerasus |  | 11.6 | OK Prunus laurocerasus 1.00 | OK Prunus laurocerasus 1.00 |
| Ajuga_reptans_1.jpg | Ajuga reptans |  | 1.4 | X Hedera helix 1.00 | OK Ajuga reptans 0.99 |
| Ajuga_reptans_2.jpg | Ajuga reptans |  | 3.7 | X Corylus avellana 0.40 | OK Ajuga reptans 1.00 |
| Dryopteris_filix-mas_1.jpg | Dryopteris filix-mas |  | 78.8 | OK Dryopteris filix-mas 0.98 | OK Dryopteris filix-mas 0.98 |
| Rabelera_holostea_1.jpg | Rabelera holostea |  | 2.6 | X Bellis perennis 0.42 | OK Rabelera holostea 0.96 |
| Rabelera_holostea_2.jpg | Rabelera holostea |  | 21.6 | OK Rabelera holostea 0.97 | OK Rabelera holostea 0.99 |
| Corylus_avellana_1.jpg | Corylus avellana |  | 0.0 | - | OK Corylus avellana 1.00 |
| Corylus_avellana_2.jpg | Corylus avellana |  | 5.0 | OK Corylus avellana 1.00 | X Alnus alnobetula 0.96 |
| Ligustrum_vulgare_1.jpg | Ligustrum vulgare |  | 79.4 | X Ilex aquifolium 0.68 | X Buxus sempervirens 0.33 |
| Phragmites_australis_1.jpg | Phragmites australis |  | 78.3 | OK Phragmites australis 1.00 | OK Phragmites australis 0.98 |
| Prunus_spinosa_1.jpg | Prunus spinosa |  | 0.3 | X Salvia rosmarinus 0.20 | OK Prunus spinosa 0.96 |
| Digitalis_purpurea_1.jpg | Digitalis purpurea |  | 12.0 | X Melittis melissophyllum 0.69 | OK Digitalis purpurea 0.99 |
| Digitalis_purpurea_2.jpg | Digitalis purpurea |  | 58.4 | OK Digitalis purpurea 1.00 | OK Digitalis purpurea 1.00 |
| Urtica_dioica_1.jpg | Urtica dioica |  | 0.3 | X Prenanthes purpurea 0.90 | OK Urtica dioica 1.00 |
| Urtica_dioica_2.jpg | Urtica dioica |  | 2.8 | OK Urtica dioica 0.86 | OK Urtica dioica 1.00 |
| Solanum_dulcamara_1.jpg | Solanum dulcamara |  | 15.7 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Solanum_dulcamara_2.jpg | Solanum dulcamara |  | 2.8 | X Asplenium scolopendrium 0.33 | OK Solanum dulcamara 1.00 |
| Sedum_acre_1.jpg | Sedum acre |  | 66.7 | OK Sedum acre 1.00 | OK Sedum acre 0.99 |
| Quercus_robur_1.jpg | Quercus robur |  | 11.5 | OK Quercus robur 0.76 | OK Quercus robur 0.57 |
| Quercus_robur_2.jpg | Quercus robur |  | 22.4 | OK Quercus robur 0.83 | OK Quercus robur 0.49 |
| Ulex_europaeus_1.jpg | Ulex europaeus |  | 0.1 | X Capsella bursa-pastoris 0.76 | OK Ulex europaeus 0.75 |
| Ulex_europaeus_2.jpg | Ulex europaeus |  | 64.8 | X Cytisus scoparius 0.42 | X Cytisus scoparius 0.99 |
| Cirsium_vulgare_1.jpg | Cirsium vulgare |  | 46.0 | OK Cirsium vulgare 1.00 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_2.jpg | Cirsium vulgare |  | 97.6 | OK Cirsium vulgare 1.00 | OK Cirsium vulgare 1.00 |
| Hyacinthoides_non-scripta_1.jpg | Hyacinthoides non-scripta |  | 60.3 | OK Hyacinthoides non-scripta 1.00 | OK Hyacinthoides non-scripta 1.00 |
| Achillea_millefolium_1.jpg | Achillea millefolium |  | 55.7 | OK Achillea millefolium 1.00 | OK Achillea millefolium 1.00 |
| Trifolium_pratense_1.jpg | Trifolium pratense |  | 5.0 | OK Trifolium pratense 0.98 | OK Trifolium pratense 1.00 |
| Trifolium_pratense_2.jpg | Trifolium pratense |  | 39.9 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Castanea_sativa_1.jpg | Castanea sativa |  | 1.5 | X Betula pendula 0.38 | OK Castanea sativa 0.87 |
| Castanea_sativa_2.jpg | Castanea sativa |  | 3.9 | OK Castanea sativa 0.99 | OK Castanea sativa 1.00 |
| Plantago_lanceolata_1.jpg | Plantago lanceolata |  | 2.6 | OK Plantago lanceolata 0.40 | OK Plantago lanceolata 1.00 |
| Plantago_lanceolata_2.jpg | Plantago lanceolata |  | 3.2 | X Lotus pedunculatus 0.44 | X Scorzonera humilis 0.68 |
| Acer_pseudoplatanus_1.jpg | Acer pseudoplatanus |  | 13.0 | OK Acer pseudoplatanus 0.99 | OK Acer pseudoplatanus 0.99 |
| Acer_pseudoplatanus_2.jpg | Acer pseudoplatanus |  | 48.9 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Crataegus_monogyna_1.jpg | Crataegus monogyna |  | 72.1 | OK Crataegus monogyna 1.00 | OK Crataegus monogyna 1.00 |
| Crataegus_monogyna_2.jpg | Crataegus monogyna |  | 7.5 | X Bellis perennis 0.91 | OK Crataegus monogyna 1.00 |
| Sambucus_ebulus_1.jpg | Sambucus ebulus |  | 6.4 | OK Sambucus ebulus 0.49 | OK Sambucus ebulus 1.00 |
| Echium_vulgare_1.jpg | Echium vulgare |  | 67.0 | OK Echium vulgare 1.00 | OK Echium vulgare 1.00 |
| Teucrium_scorodonia_1.jpg | Teucrium scorodonia |  | 94.3 | OK Teucrium scorodonia 0.92 | OK Teucrium scorodonia 0.98 |
| Teucrium_scorodonia_2.jpg | Teucrium scorodonia |  | 98.2 | X Melittis melissophyllum 0.60 | OK Teucrium scorodonia 0.59 |
| Heracleum_sphondylium_1.jpg | Heracleum sphondylium |  | 98.1 | OK Heracleum sphondylium 1.00 | OK Heracleum sphondylium 1.00 |
| Heracleum_sphondylium_2.jpg | Heracleum sphondylium |  | 1.4 | X Acer pseudoplatanus 0.73 | X Bupleurum fruticosum 0.91 |
| Plantago_coronopus_1.jpg | Plantago coronopus |  | 0.1 | X Trifolium repens 0.52 | OK Plantago coronopus 1.00 |
| Plantago_coronopus_2.jpg | Plantago coronopus |  | 98.3 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Chelidonium_majus_1.jpg | Chelidonium majus |  | 94.4 | OK Chelidonium majus 1.00 | OK Chelidonium majus 1.00 |
| Chelidonium_majus_2.jpg | Chelidonium majus |  | 55.4 | OK Chelidonium majus 0.99 | OK Chelidonium majus 1.00 |
| Fraxinus_excelsior_1.jpg | Fraxinus excelsior |  | 98.1 | OK Fraxinus excelsior 0.92 | OK Fraxinus excelsior 0.82 |
| Trifolium_repens_1.jpg | Trifolium repens |  | 12.9 | OK Trifolium repens 0.99 | OK Trifolium repens 1.00 |
| Trifolium_repens_2.jpg | Trifolium repens |  | 7.5 | OK Trifolium repens 0.97 | OK Trifolium repens 0.69 |
| Geranium_dissectum_1.jpg | Geranium dissectum |  | 97.9 | OK Geranium dissectum 0.94 | OK Geranium dissectum 0.97 |
| Geranium_dissectum_2.jpg | Geranium dissectum |  | 15.3 | X Teucrium scorodonia 0.81 | X Geranium sylvaticum 0.50 |
| Vicia_sepium_1.jpg | Vicia sepium |  | 98.9 | OK Vicia sepium 1.00 | OK Vicia sepium 1.00 |
| Cytisus_scoparius_1.jpg | Cytisus scoparius |  | 98.7 | OK Cytisus scoparius 0.95 | OK Cytisus scoparius 0.63 |
| Asplenium_ceterach_1.jpg | Asplenium ceterach |  | 46.2 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Asplenium_ceterach_2.jpg | Asplenium ceterach |  | 94.0 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Anthoxanthum_odoratum_1.jpg | Anthoxanthum odoratum |  | 22.5 | OK Anthoxanthum odoratum 0.96 | OK Anthoxanthum odoratum 1.00 |
| Vicia_cracca_1.jpg | Vicia cracca |  | 3.7 | X Solanum dulcamara 0.70 | OK Vicia cracca 1.00 |
| Medicago_lupulina_1.jpg | Medicago lupulina |  | 1.7 | X Trifolium pratense 0.91 | OK Medicago lupulina 1.00 |
| Agrimonia_eupatoria_1.jpg | Agrimonia eupatoria |  | 14.4 | X Anthoxanthum odoratum 0.30 | OK Agrimonia eupatoria 1.00 |
| Catapodium_rigidum_1.jpg | Catapodium rigidum |  | 84.2 | OK Catapodium rigidum 0.94 | OK Catapodium rigidum 0.85 |
| Dactylis_glomerata_1.jpg | Dactylis glomerata |  | 0.0 | - | OK Dactylis glomerata 1.00 |
| Hypericum_perforatum_1.jpg | Hypericum perforatum |  | 69.5 | OK Hypericum perforatum 1.00 | OK Hypericum perforatum 1.00 |
| Erica_cinerea_1.jpg | Erica cinerea |  | 98.4 | OK Erica cinerea 1.00 | OK Erica cinerea 1.00 |
| Erica_cinerea_2.jpg | Erica cinerea |  | 26.1 | X Calluna vulgaris 0.67 | OK Erica cinerea 0.97 |
| Scorzonera_humilis_1.jpg | Scorzonera humilis |  | 60.3 | X Hyacinthoides non-scripta 0.25 | X Lactuca perennis 0.54 |
| Struthiopteris_spicant_1.jpg | Struthiopteris spicant |  | 0.4 | X Ligustrum vulgare 0.59 | OK Struthiopteris spicant 0.86 |
| Struthiopteris_spicant_2.jpg | Struthiopteris spicant |  | 59.9 | X Pteridium aquilinum 0.61 | X Polystichum lonchitis 0.81 |
| Phalaris_arundinacea_1.jpg | Phalaris arundinacea |  | 0.0 | - | X Arrhenatherum elatius 0.28 |
| Lotus_corniculatus_1.jpg | Lotus corniculatus |  | 98.7 | OK Lotus corniculatus 0.90 | OK Lotus corniculatus 0.92 |
| Argentina_anserina_1.jpg | Argentina anserina |  | 1.4 | X Urtica dioica 0.51 | OK Argentina anserina 1.00 |
| Anacamptis_pyramidalis_1.jpg | Anacamptis pyramidalis |  | 8.2 | X Gymnadenia conopsea 0.48 | X Dactylorhiza maculata 0.62 |
| Anacamptis_pyramidalis_2.jpg | Anacamptis pyramidalis |  | 30.4 | OK Anacamptis pyramidalis 0.89 | OK Anacamptis pyramidalis 0.98 |
| Calluna_vulgaris_1.jpg | Calluna vulgaris |  | 98.7 | OK Calluna vulgaris 1.00 | OK Calluna vulgaris 0.99 |
| Primula_veris_1.jpg | Primula veris |  | 10.5 | X Acer pseudoplatanus 0.69 | OK Primula veris 1.00 |
| Primula_veris_2.jpg | Primula veris |  | 13.2 | X Trifolium repens 0.84 | OK Primula veris 0.99 |
| Bellis_perennis_1.jpg | Bellis perennis |  | 1.2 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Bellis_perennis_2.jpg | Bellis perennis |  | 8.1 | OK Bellis perennis 0.97 | OK Bellis perennis 1.00 |
| Lathyrus_pratensis_1.jpg | Lathyrus pratensis |  | 5.0 | X Vincetoxicum hirundinaria 0.54 | OK Lathyrus pratensis 0.82 |
| Lathyrus_pratensis_2.jpg | Lathyrus pratensis |  | 7.0 | OK Lathyrus pratensis 0.75 | OK Lathyrus pratensis 0.71 |
| Dactylorhiza_maculata_1.jpg | Dactylorhiza maculata |  | 44.2 | OK Dactylorhiza maculata 0.91 | OK Dactylorhiza maculata 0.97 |
| Hedera_helix_1.jpg | Hedera helix |  | 3.7 | OK Hedera helix 0.99 | OK Hedera helix 0.98 |
| Hedera_helix_2.jpg | Hedera helix |  | 10.1 | OK Hedera helix 0.79 | OK Hedera helix 1.00 |
| Juncus_acutiflorus_1.jpg | Juncus acutiflorus |  | 98.7 | OK Juncus acutiflorus 0.85 | OK Juncus acutiflorus 0.88 |
| Juncus_acutiflorus_2.jpg | Juncus acutiflorus |  | 47.4 | X Luzula luzuloides 0.89 | X Luzula luzuloides 0.96 |
| Arrhenatherum_elatius_1.jpg | Arrhenatherum elatius |  | 98.9 | OK Arrhenatherum elatius 1.00 | OK Arrhenatherum elatius 1.00 |
| Impatiens_balfourii_1.jpg | Impatiens balfourii |  | 7.5 | OK Impatiens balfourii 0.83 | OK Impatiens balfourii 1.00 |
| Alopecurus_pratensis_1.jpg | Alopecurus pratensis |  | 7.7 | X Holcus lanatus 0.74 | OK Alopecurus pratensis 0.84 |
| Borago_officinalis_1.jpg | Borago officinalis |  | 98.9 | OK Borago officinalis 1.00 | OK Borago officinalis 1.00 |
| Teesdalia_nudicaulis_1.jpg | Teesdalia nudicaulis |  | 0.7 | X Hedera helix 0.70 | OK Teesdalia nudicaulis 0.80 |
| Teesdalia_nudicaulis_2.jpg | Teesdalia nudicaulis |  | 20.4 | OK Teesdalia nudicaulis 0.92 | OK Teesdalia nudicaulis 0.98 |
| Lotus_pedunculatus_1.jpg | Lotus pedunculatus |  | 98.5 | OK Lotus pedunculatus 0.99 | OK Lotus pedunculatus 0.99 |
| Potentilla_erecta_1.jpg | Potentilla erecta |  | 2.7 | X Carex echinata 0.44 | OK Potentilla erecta 1.00 |
| Potentilla_erecta_2.jpg | Potentilla erecta |  | 23.2 | OK Potentilla erecta 1.00 | OK Potentilla erecta 1.00 |
| Alliaria_petiolata_1.jpg | Alliaria petiolata |  | 98.2 | OK Alliaria petiolata 0.98 | OK Alliaria petiolata 0.99 |
| Galium_mollugo_1.jpg | Galium mollugo |  | 36.6 | OK Galium mollugo 0.49 | OK Galium mollugo 0.89 |
| Aulacomnium_palustre_1.jpg | Aulacomnium palustre |  | 1.1 | X Plantago lanceolata 0.71 | OK Aulacomnium palustre 1.00 |
| Carex_panicea_1.jpg | Carex panicea |  | 3.5 | X Holcus lanatus 0.50 | OK Carex panicea 0.94 |
| Carex_hirta_1.jpg | Carex hirta |  | 98.8 | OK Carex hirta 0.96 | OK Carex hirta 0.96 |
| Viburnum_lantana_1.jpg | Viburnum lantana |  | 12.8 | OK Viburnum lantana 0.98 | OK Viburnum lantana 1.00 |
| Fagopyrum_esculentum_1.jpg | Fagopyrum esculentum |  | 32.9 | OK Fagopyrum esculentum 0.97 | X Alliaria petiolata 0.68 |
| Buxus_sempervirens_1.jpg | Buxus sempervirens |  | 0.2 | X Carex echinata 0.28 | OK Buxus sempervirens 0.97 |
| Sorbus_aucuparia_1.jpg | Sorbus aucuparia |  | 1.3 | X Teucrium scorodonia 0.30 | OK Sorbus aucuparia 1.00 |
| Picris_hieracioides_1.jpg | Picris hieracioides |  | 35.3 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Picris_hieracioides_2.jpg | Picris hieracioides |  | 23.2 | X Reichardia picroides 0.81 | OK Picris hieracioides 1.00 |
| Pinus_sylvestris_1.jpg | Pinus sylvestris |  | 98.4 | OK Pinus sylvestris 0.76 | OK Pinus sylvestris 0.84 |
| Molinia_caerulea_1.jpg | Molinia caerulea |  | 0.0 | - | OK Molinia caerulea 0.99 |
| Anthriscus_sylvestris_1.jpg | Anthriscus sylvestris |  | 79.7 | OK Anthriscus sylvestris 0.94 | X Rubus fruticosus 0.51 |
| Capsella_bursa-pastoris_1.jpg | Capsella bursa-pastoris |  | 6.5 | X Hedera helix 0.65 | OK Capsella bursa-pastoris 1.00 |
| Bromus_hordeaceus_1.jpg | Bromus hordeaceus |  | 44.7 | OK Bromus hordeaceus 1.00 | OK Bromus hordeaceus 1.00 |
| Holcus_lanatus_1.jpg | Holcus lanatus |  | 0.0 | - | OK Holcus lanatus 0.98 |
| Carex_flacca_1.jpg | Carex flacca |  | 89.2 | OK Carex flacca 1.00 | OK Carex flacca 1.00 |
| Neottia_ovata_1.jpg | Neottia ovata |  | 79.7 | OK Neottia ovata 1.00 | OK Neottia ovata 1.00 |
| Galium_odoratum_1.jpg | Galium odoratum |  | 98.1 | OK Galium odoratum 1.00 | OK Galium odoratum 1.00 |
| Rubus_idaeus_1.jpg | Rubus idaeus |  | 2.1 | X Prunus laurocerasus 0.79 | OK Rubus idaeus 0.46 |
| Arabidopsis_thaliana_1.jpg | Arabidopsis thaliana |  | 94.4 | OK Arabidopsis thaliana 0.96 | OK Arabidopsis thaliana 0.94 |
| Melissa_officinalis_1.jpg | Melissa officinalis |  | 97.7 | OK Melissa officinalis 1.00 | OK Melissa officinalis 1.00 |
| Helleborus_foetidus_1.jpg | Helleborus foetidus |  | 90.4 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Petasites_hybridus_1.jpg | Petasites hybridus |  | 21.5 | OK Petasites hybridus 1.00 | OK Petasites hybridus 1.00 |

## Setting: catalog+truth
True species on the candidate list for 130/130 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 80/130 (62%) | 92/130 (71%) | 80/130 (62%) | 0.939 / 0.592 | 4 | 77/107 (72%) |
| full | 114/130 (88%) | 126/130 (97%) | 115/130 (88%) | 0.948 / 0.674 | 4 | 112/125 (90%) |
| hybrid>=2 | 98/130 (75%) | 107/130 (82%) | 98/130 (75%) | 0.942 / 0.587 | 2 | 95/115 (83%) |
| hybrid>=5 | 107/130 (82%) | 117/130 (90%) | 107/130 (82%) | 0.946 / 0.634 | 2 | 104/121 (86%) |
| hybrid>=10 | 110/130 (85%) | 120/130 (92%) | 110/130 (85%) | 0.948 / 0.643 | 2 | 108/123 (88%) |
| hybrid>=20 | 113/130 (87%) | 125/130 (96%) | 114/130 (88%) | 0.951 / 0.629 | 2 | 111/124 (90%) |
| hybrid>=40 | 114/130 (88%) | 125/130 (96%) | 115/130 (88%) | 0.954 / 0.618 | 2 | 112/124 (90%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 18 | 3 |
| 0.50-0.80 | 26 | 5 |
| 0.80-0.95 | 24 | 16 |
| 0.95-1.00 | 57 | 56 |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Pteridium aquilinum → Betula pendula ×1, Pteridium aquilinum → Dryopteris filix-mas ×1, Fagus sylvatica → Carex echinata ×1, Cornus sanguinea → Neottia ovata ×1, Prunus laurocerasus → Asplenium scolopendrium ×1, Ajuga reptans → Hedera helix ×1, Ajuga reptans → Corylus avellana ×1, Rabelera holostea → Bellis perennis ×1
- full: Asplenium scolopendrium → Struthiopteris spicant ×1, Orchis mascula → Anacamptis pyramidalis ×1, Prunus laurocerasus → Ligustrum vulgare ×1, Corylus avellana → Alnus alnobetula ×1, Ligustrum vulgare → Buxus sempervirens ×1, Ulex europaeus → Cytisus scoparius ×1, Plantago lanceolata → Scorzonera humilis ×1, Heracleum sphondylium → Bupleurum fruticosum ×1

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Asplenium_scolopendrium_1.jpg | Asplenium scolopendrium |  | 43.8 | OK Asplenium scolopendrium 0.64 | X Struthiopteris spicant 0.85 |
| Eupatorium_cannabinum_1.jpg | Eupatorium cannabinum |  | 26.8 | OK Eupatorium cannabinum 1.00 | OK Eupatorium cannabinum 1.00 |
| Ilex_aquifolium_1.jpg | Ilex aquifolium |  | 96.2 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Ilex_aquifolium_2.jpg | Ilex aquifolium |  | 98.1 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Orchis_mascula_1.jpg | Orchis mascula |  | 12.9 | OK Orchis mascula 0.92 | OK Orchis mascula 0.97 |
| Orchis_mascula_2.jpg | Orchis mascula |  | 10.8 | OK Orchis mascula 0.89 | X Anacamptis pyramidalis 0.66 |
| Pteridium_aquilinum_1.jpg | Pteridium aquilinum |  | 0.4 | X Betula pendula 0.19 | OK Pteridium aquilinum 1.00 |
| Pteridium_aquilinum_2.jpg | Pteridium aquilinum |  | 98.0 | X Dryopteris filix-mas 0.67 | OK Pteridium aquilinum 0.50 |
| Fagus_sylvatica_1.jpg | Fagus sylvatica |  | 3.3 | X Carex echinata 0.16 | OK Fagus sylvatica 1.00 |
| Fagus_sylvatica_2.jpg | Fagus sylvatica |  | 16.3 | OK Fagus sylvatica 1.00 | OK Fagus sylvatica 1.00 |
| Cornus_sanguinea_1.jpg | Cornus sanguinea |  | 3.9 | X Neottia ovata 0.70 | OK Cornus sanguinea 0.85 |
| Prunus_laurocerasus_1.jpg | Prunus laurocerasus |  | 1.2 | X Asplenium scolopendrium 0.86 | X Ligustrum vulgare 0.48 |
| Prunus_laurocerasus_2.jpg | Prunus laurocerasus |  | 11.6 | OK Prunus laurocerasus 1.00 | OK Prunus laurocerasus 1.00 |
| Ajuga_reptans_1.jpg | Ajuga reptans |  | 1.4 | X Hedera helix 1.00 | OK Ajuga reptans 0.99 |
| Ajuga_reptans_2.jpg | Ajuga reptans |  | 3.7 | X Corylus avellana 0.40 | OK Ajuga reptans 1.00 |
| Dryopteris_filix-mas_1.jpg | Dryopteris filix-mas |  | 78.8 | OK Dryopteris filix-mas 0.98 | OK Dryopteris filix-mas 0.98 |
| Rabelera_holostea_1.jpg | Rabelera holostea |  | 2.6 | X Bellis perennis 0.42 | OK Rabelera holostea 0.96 |
| Rabelera_holostea_2.jpg | Rabelera holostea |  | 21.6 | OK Rabelera holostea 0.97 | OK Rabelera holostea 0.99 |
| Corylus_avellana_1.jpg | Corylus avellana |  | 0.0 | - | OK Corylus avellana 1.00 |
| Corylus_avellana_2.jpg | Corylus avellana |  | 5.0 | OK Corylus avellana 1.00 | X Alnus alnobetula 0.96 |
| Ligustrum_vulgare_1.jpg | Ligustrum vulgare |  | 79.4 | X Ilex aquifolium 0.68 | X Buxus sempervirens 0.33 |
| Phragmites_australis_1.jpg | Phragmites australis |  | 78.3 | OK Phragmites australis 1.00 | OK Phragmites australis 0.98 |
| Prunus_spinosa_1.jpg | Prunus spinosa |  | 0.3 | X Salvia rosmarinus 0.20 | OK Prunus spinosa 0.96 |
| Digitalis_purpurea_1.jpg | Digitalis purpurea |  | 12.0 | X Melittis melissophyllum 0.69 | OK Digitalis purpurea 0.99 |
| Digitalis_purpurea_2.jpg | Digitalis purpurea |  | 58.4 | OK Digitalis purpurea 1.00 | OK Digitalis purpurea 1.00 |
| Urtica_dioica_1.jpg | Urtica dioica |  | 0.3 | X Prenanthes purpurea 0.90 | OK Urtica dioica 1.00 |
| Urtica_dioica_2.jpg | Urtica dioica |  | 2.8 | OK Urtica dioica 0.86 | OK Urtica dioica 1.00 |
| Solanum_dulcamara_1.jpg | Solanum dulcamara |  | 15.7 | OK Solanum dulcamara 1.00 | OK Solanum dulcamara 1.00 |
| Solanum_dulcamara_2.jpg | Solanum dulcamara |  | 2.8 | X Asplenium scolopendrium 0.33 | OK Solanum dulcamara 1.00 |
| Sedum_acre_1.jpg | Sedum acre |  | 66.7 | OK Sedum acre 1.00 | OK Sedum acre 0.99 |
| Quercus_robur_1.jpg | Quercus robur |  | 11.5 | OK Quercus robur 0.76 | OK Quercus robur 0.57 |
| Quercus_robur_2.jpg | Quercus robur |  | 22.4 | OK Quercus robur 0.83 | OK Quercus robur 0.49 |
| Ulex_europaeus_1.jpg | Ulex europaeus |  | 0.1 | X Capsella bursa-pastoris 0.76 | OK Ulex europaeus 0.75 |
| Ulex_europaeus_2.jpg | Ulex europaeus |  | 64.8 | X Cytisus scoparius 0.42 | X Cytisus scoparius 0.99 |
| Cirsium_vulgare_1.jpg | Cirsium vulgare |  | 46.0 | OK Cirsium vulgare 1.00 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_2.jpg | Cirsium vulgare |  | 97.6 | OK Cirsium vulgare 1.00 | OK Cirsium vulgare 1.00 |
| Hyacinthoides_non-scripta_1.jpg | Hyacinthoides non-scripta |  | 60.3 | OK Hyacinthoides non-scripta 1.00 | OK Hyacinthoides non-scripta 1.00 |
| Achillea_millefolium_1.jpg | Achillea millefolium |  | 55.7 | OK Achillea millefolium 1.00 | OK Achillea millefolium 1.00 |
| Trifolium_pratense_1.jpg | Trifolium pratense |  | 5.0 | OK Trifolium pratense 0.98 | OK Trifolium pratense 1.00 |
| Trifolium_pratense_2.jpg | Trifolium pratense |  | 39.9 | OK Trifolium pratense 1.00 | OK Trifolium pratense 1.00 |
| Castanea_sativa_1.jpg | Castanea sativa |  | 1.5 | X Betula pendula 0.38 | OK Castanea sativa 0.87 |
| Castanea_sativa_2.jpg | Castanea sativa |  | 3.9 | OK Castanea sativa 0.99 | OK Castanea sativa 1.00 |
| Plantago_lanceolata_1.jpg | Plantago lanceolata |  | 2.6 | OK Plantago lanceolata 0.40 | OK Plantago lanceolata 1.00 |
| Plantago_lanceolata_2.jpg | Plantago lanceolata |  | 3.2 | X Lotus pedunculatus 0.44 | X Scorzonera humilis 0.68 |
| Acer_pseudoplatanus_1.jpg | Acer pseudoplatanus |  | 13.0 | OK Acer pseudoplatanus 0.99 | OK Acer pseudoplatanus 0.99 |
| Acer_pseudoplatanus_2.jpg | Acer pseudoplatanus |  | 48.9 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Crataegus_monogyna_1.jpg | Crataegus monogyna |  | 72.1 | OK Crataegus monogyna 1.00 | OK Crataegus monogyna 1.00 |
| Crataegus_monogyna_2.jpg | Crataegus monogyna |  | 7.5 | X Bellis perennis 0.91 | OK Crataegus monogyna 1.00 |
| Sambucus_ebulus_1.jpg | Sambucus ebulus |  | 6.4 | OK Sambucus ebulus 0.49 | OK Sambucus ebulus 1.00 |
| Echium_vulgare_1.jpg | Echium vulgare |  | 67.0 | OK Echium vulgare 1.00 | OK Echium vulgare 1.00 |
| Teucrium_scorodonia_1.jpg | Teucrium scorodonia |  | 94.3 | OK Teucrium scorodonia 0.92 | OK Teucrium scorodonia 0.98 |
| Teucrium_scorodonia_2.jpg | Teucrium scorodonia |  | 98.2 | X Melittis melissophyllum 0.60 | OK Teucrium scorodonia 0.59 |
| Heracleum_sphondylium_1.jpg | Heracleum sphondylium |  | 98.1 | OK Heracleum sphondylium 1.00 | OK Heracleum sphondylium 1.00 |
| Heracleum_sphondylium_2.jpg | Heracleum sphondylium |  | 1.4 | X Acer pseudoplatanus 0.73 | X Bupleurum fruticosum 0.91 |
| Plantago_coronopus_1.jpg | Plantago coronopus |  | 0.1 | X Trifolium repens 0.52 | OK Plantago coronopus 1.00 |
| Plantago_coronopus_2.jpg | Plantago coronopus |  | 98.3 | OK Plantago coronopus 1.00 | OK Plantago coronopus 1.00 |
| Chelidonium_majus_1.jpg | Chelidonium majus |  | 94.4 | OK Chelidonium majus 1.00 | OK Chelidonium majus 1.00 |
| Chelidonium_majus_2.jpg | Chelidonium majus |  | 55.4 | OK Chelidonium majus 0.99 | OK Chelidonium majus 1.00 |
| Fraxinus_excelsior_1.jpg | Fraxinus excelsior |  | 98.1 | OK Fraxinus excelsior 0.92 | OK Fraxinus excelsior 0.82 |
| Trifolium_repens_1.jpg | Trifolium repens |  | 12.9 | OK Trifolium repens 0.99 | OK Trifolium repens 1.00 |
| Trifolium_repens_2.jpg | Trifolium repens |  | 7.5 | OK Trifolium repens 0.97 | OK Trifolium repens 0.69 |
| Geranium_dissectum_1.jpg | Geranium dissectum |  | 97.9 | OK Geranium dissectum 0.94 | OK Geranium dissectum 0.97 |
| Geranium_dissectum_2.jpg | Geranium dissectum |  | 15.3 | X Teucrium scorodonia 0.81 | X Geranium sylvaticum 0.50 |
| Vicia_sepium_1.jpg | Vicia sepium |  | 98.9 | OK Vicia sepium 1.00 | OK Vicia sepium 1.00 |
| Cytisus_scoparius_1.jpg | Cytisus scoparius |  | 98.7 | OK Cytisus scoparius 0.95 | OK Cytisus scoparius 0.63 |
| Asplenium_ceterach_1.jpg | Asplenium ceterach |  | 46.2 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Asplenium_ceterach_2.jpg | Asplenium ceterach |  | 94.0 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 1.00 |
| Anthoxanthum_odoratum_1.jpg | Anthoxanthum odoratum |  | 22.5 | OK Anthoxanthum odoratum 0.96 | OK Anthoxanthum odoratum 1.00 |
| Vicia_cracca_1.jpg | Vicia cracca |  | 3.7 | X Solanum dulcamara 0.70 | OK Vicia cracca 1.00 |
| Medicago_lupulina_1.jpg | Medicago lupulina |  | 1.7 | X Trifolium pratense 0.91 | OK Medicago lupulina 1.00 |
| Agrimonia_eupatoria_1.jpg | Agrimonia eupatoria |  | 14.4 | X Anthoxanthum odoratum 0.30 | OK Agrimonia eupatoria 1.00 |
| Catapodium_rigidum_1.jpg | Catapodium rigidum |  | 84.2 | OK Catapodium rigidum 0.94 | OK Catapodium rigidum 0.85 |
| Dactylis_glomerata_1.jpg | Dactylis glomerata |  | 0.0 | - | OK Dactylis glomerata 1.00 |
| Hypericum_perforatum_1.jpg | Hypericum perforatum |  | 69.5 | OK Hypericum perforatum 1.00 | OK Hypericum perforatum 1.00 |
| Erica_cinerea_1.jpg | Erica cinerea |  | 98.4 | OK Erica cinerea 1.00 | OK Erica cinerea 1.00 |
| Erica_cinerea_2.jpg | Erica cinerea |  | 26.1 | X Calluna vulgaris 0.67 | OK Erica cinerea 0.97 |
| Scorzonera_humilis_1.jpg | Scorzonera humilis |  | 60.3 | X Hyacinthoides non-scripta 0.25 | X Lactuca perennis 0.54 |
| Struthiopteris_spicant_1.jpg | Struthiopteris spicant |  | 0.4 | X Ligustrum vulgare 0.59 | OK Struthiopteris spicant 0.86 |
| Struthiopteris_spicant_2.jpg | Struthiopteris spicant |  | 59.9 | X Pteridium aquilinum 0.61 | X Polystichum lonchitis 0.81 |
| Phalaris_arundinacea_1.jpg | Phalaris arundinacea |  | 0.0 | - | X Arrhenatherum elatius 0.28 |
| Lotus_corniculatus_1.jpg | Lotus corniculatus |  | 98.7 | OK Lotus corniculatus 0.90 | OK Lotus corniculatus 0.92 |
| Argentina_anserina_1.jpg | Argentina anserina |  | 1.4 | X Urtica dioica 0.51 | OK Argentina anserina 1.00 |
| Anacamptis_pyramidalis_1.jpg | Anacamptis pyramidalis |  | 8.2 | X Gymnadenia conopsea 0.48 | X Dactylorhiza maculata 0.62 |
| Anacamptis_pyramidalis_2.jpg | Anacamptis pyramidalis |  | 30.4 | OK Anacamptis pyramidalis 0.89 | OK Anacamptis pyramidalis 0.98 |
| Calluna_vulgaris_1.jpg | Calluna vulgaris |  | 98.7 | OK Calluna vulgaris 1.00 | OK Calluna vulgaris 0.99 |
| Primula_veris_1.jpg | Primula veris |  | 10.5 | X Acer pseudoplatanus 0.69 | OK Primula veris 1.00 |
| Primula_veris_2.jpg | Primula veris |  | 13.2 | X Trifolium repens 0.84 | OK Primula veris 0.99 |
| Bellis_perennis_1.jpg | Bellis perennis |  | 1.2 | OK Bellis perennis 1.00 | OK Bellis perennis 1.00 |
| Bellis_perennis_2.jpg | Bellis perennis |  | 8.1 | OK Bellis perennis 0.97 | OK Bellis perennis 1.00 |
| Lathyrus_pratensis_1.jpg | Lathyrus pratensis |  | 5.0 | X Vincetoxicum hirundinaria 0.54 | OK Lathyrus pratensis 0.82 |
| Lathyrus_pratensis_2.jpg | Lathyrus pratensis |  | 7.0 | OK Lathyrus pratensis 0.75 | OK Lathyrus pratensis 0.71 |
| Dactylorhiza_maculata_1.jpg | Dactylorhiza maculata |  | 44.2 | OK Dactylorhiza maculata 0.91 | OK Dactylorhiza maculata 0.97 |
| Hedera_helix_1.jpg | Hedera helix |  | 3.7 | OK Hedera helix 0.99 | OK Hedera helix 0.98 |
| Hedera_helix_2.jpg | Hedera helix |  | 10.1 | OK Hedera helix 0.79 | OK Hedera helix 1.00 |
| Juncus_acutiflorus_1.jpg | Juncus acutiflorus |  | 98.7 | OK Juncus acutiflorus 0.85 | OK Juncus acutiflorus 0.88 |
| Juncus_acutiflorus_2.jpg | Juncus acutiflorus |  | 47.4 | X Luzula luzuloides 0.89 | X Luzula luzuloides 0.96 |
| Arrhenatherum_elatius_1.jpg | Arrhenatherum elatius |  | 98.9 | OK Arrhenatherum elatius 1.00 | OK Arrhenatherum elatius 1.00 |
| Impatiens_balfourii_1.jpg | Impatiens balfourii |  | 7.5 | OK Impatiens balfourii 0.83 | OK Impatiens balfourii 1.00 |
| Alopecurus_pratensis_1.jpg | Alopecurus pratensis |  | 7.7 | X Holcus lanatus 0.74 | OK Alopecurus pratensis 0.84 |
| Borago_officinalis_1.jpg | Borago officinalis |  | 98.9 | OK Borago officinalis 1.00 | OK Borago officinalis 1.00 |
| Teesdalia_nudicaulis_1.jpg | Teesdalia nudicaulis |  | 0.7 | X Hedera helix 0.70 | OK Teesdalia nudicaulis 0.80 |
| Teesdalia_nudicaulis_2.jpg | Teesdalia nudicaulis |  | 20.4 | OK Teesdalia nudicaulis 0.92 | OK Teesdalia nudicaulis 0.98 |
| Lotus_pedunculatus_1.jpg | Lotus pedunculatus |  | 98.5 | OK Lotus pedunculatus 0.99 | OK Lotus pedunculatus 0.99 |
| Potentilla_erecta_1.jpg | Potentilla erecta |  | 2.7 | X Carex echinata 0.44 | OK Potentilla erecta 1.00 |
| Potentilla_erecta_2.jpg | Potentilla erecta |  | 23.2 | OK Potentilla erecta 1.00 | OK Potentilla erecta 1.00 |
| Alliaria_petiolata_1.jpg | Alliaria petiolata |  | 98.2 | OK Alliaria petiolata 0.98 | OK Alliaria petiolata 0.99 |
| Galium_mollugo_1.jpg | Galium mollugo |  | 36.6 | OK Galium mollugo 0.49 | OK Galium mollugo 0.89 |
| Aulacomnium_palustre_1.jpg | Aulacomnium palustre |  | 1.1 | X Plantago lanceolata 0.71 | OK Aulacomnium palustre 1.00 |
| Carex_panicea_1.jpg | Carex panicea |  | 3.5 | X Holcus lanatus 0.50 | OK Carex panicea 0.94 |
| Carex_hirta_1.jpg | Carex hirta |  | 98.8 | OK Carex hirta 0.96 | OK Carex hirta 0.96 |
| Viburnum_lantana_1.jpg | Viburnum lantana |  | 12.8 | OK Viburnum lantana 0.98 | OK Viburnum lantana 1.00 |
| Fagopyrum_esculentum_1.jpg | Fagopyrum esculentum |  | 32.9 | OK Fagopyrum esculentum 0.97 | X Alliaria petiolata 0.68 |
| Buxus_sempervirens_1.jpg | Buxus sempervirens |  | 0.2 | X Carex echinata 0.28 | OK Buxus sempervirens 0.97 |
| Sorbus_aucuparia_1.jpg | Sorbus aucuparia |  | 1.3 | X Teucrium scorodonia 0.30 | OK Sorbus aucuparia 1.00 |
| Picris_hieracioides_1.jpg | Picris hieracioides |  | 35.3 | OK Picris hieracioides 1.00 | OK Picris hieracioides 1.00 |
| Picris_hieracioides_2.jpg | Picris hieracioides |  | 23.2 | X Reichardia picroides 0.81 | OK Picris hieracioides 1.00 |
| Pinus_sylvestris_1.jpg | Pinus sylvestris |  | 98.4 | OK Pinus sylvestris 0.76 | OK Pinus sylvestris 0.84 |
| Molinia_caerulea_1.jpg | Molinia caerulea |  | 0.0 | - | OK Molinia caerulea 0.99 |
| Anthriscus_sylvestris_1.jpg | Anthriscus sylvestris |  | 79.7 | OK Anthriscus sylvestris 0.94 | X Rubus fruticosus 0.51 |
| Capsella_bursa-pastoris_1.jpg | Capsella bursa-pastoris |  | 6.5 | X Hedera helix 0.65 | OK Capsella bursa-pastoris 1.00 |
| Bromus_hordeaceus_1.jpg | Bromus hordeaceus |  | 44.7 | OK Bromus hordeaceus 1.00 | OK Bromus hordeaceus 1.00 |
| Holcus_lanatus_1.jpg | Holcus lanatus |  | 0.0 | - | OK Holcus lanatus 0.98 |
| Carex_flacca_1.jpg | Carex flacca |  | 89.2 | OK Carex flacca 1.00 | OK Carex flacca 1.00 |
| Neottia_ovata_1.jpg | Neottia ovata |  | 79.7 | OK Neottia ovata 1.00 | OK Neottia ovata 1.00 |
| Galium_odoratum_1.jpg | Galium odoratum |  | 98.1 | OK Galium odoratum 1.00 | OK Galium odoratum 1.00 |
| Rubus_idaeus_1.jpg | Rubus idaeus |  | 2.1 | X Prunus laurocerasus 0.79 | OK Rubus idaeus 0.46 |
| Arabidopsis_thaliana_1.jpg | Arabidopsis thaliana |  | 94.4 | OK Arabidopsis thaliana 0.96 | OK Arabidopsis thaliana 0.94 |
| Melissa_officinalis_1.jpg | Melissa officinalis |  | 97.7 | OK Melissa officinalis 1.00 | OK Melissa officinalis 1.00 |
| Helleborus_foetidus_1.jpg | Helleborus foetidus |  | 90.4 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Petasites_hybridus_1.jpg | Petasites hybridus |  | 21.5 | OK Petasites hybridus 1.00 | OK Petasites hybridus 1.00 |

No previous report to compare with.
