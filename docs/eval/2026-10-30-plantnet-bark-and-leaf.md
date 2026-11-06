# Eval report — 2026-10-30 — plantnet-bark-and-leaf

- Photos: 574 (labels from labels.csv)
- Candidate list: `data/species_lists/catalog.txt` (214 species)
- Confidence threshold for abstaining: 0.5 (placeholder)
- Device: cuda
- Labels are PlantNet suggestions given by the team, not expert-verified: treat the second word of each name as uncertain (genus-level is more reliable).

## Setting: catalog
True species on the candidate list for 574/574 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 169/574 (29%) | 225/574 (39%) | 179/574 (31%) | 0.892 / 0.509 | 16 | 160/276 (58%) |
| full | 370/574 (64%) | 470/574 (82%) | 398/574 (69%) | 0.904 / 0.586 | 26 | 360/481 (75%) |
| hybrid>=2 | 305/574 (53%) | 400/574 (70%) | 329/574 (57%) | 0.895 / 0.559 | 28 | 295/442 (67%) |
| hybrid>=5 | 333/574 (58%) | 426/574 (74%) | 357/574 (62%) | 0.901 / 0.572 | 27 | 324/463 (70%) |
| hybrid>=10 | 346/574 (60%) | 444/574 (77%) | 372/574 (65%) | 0.903 / 0.588 | 28 | 337/477 (71%) |
| hybrid>=20 | 358/574 (62%) | 452/574 (79%) | 384/574 (67%) | 0.91 / 0.587 | 29 | 349/478 (73%) |
| hybrid>=40 | 362/574 (63%) | 463/574 (81%) | 389/574 (68%) | 0.908 / 0.586 | 29 | 354/479 (74%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 138 | 9 |
| 0.50-0.80 | 110 | 27 |
| 0.80-0.95 | 52 | 30 |
| 0.95-1.00 | 114 | 103 |

Could BioCLIP have seen these photos? Split by iNaturalist upload date (cutoff 2024-01-01: its training data predates Nov 2023):

| subset | photos | full top-1 | full top-3 | crop top-1 | crop top-3 |
|---|---|---|---|---|---|
| uploaded on/after 2024-01-01 (cannot be in training data) | 574 | 370/574 (64%) | 470/574 (82%) | 169/574 (29%) | 225/574 (39%) |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Alnus alnobetula → Corylus avellana ×2, Dactylorhiza maculata → Carex echinata ×2, Ligustrum vulgare → Acacia dealbata ×2, Melittis melissophyllum → Melissa officinalis ×2, Orchis purpurea → Himantoglossum robertianum ×2, Ostrya carpinifolia → Asplenium scolopendrium ×2, Pistacia lentiscus → Acer pseudoplatanus ×2, Vicia cracca → Holcus lanatus ×2
- full: Arundo donax → Phragmites australis ×3, Abies alba → Acer pseudoplatanus ×2, Brachypodium pinnatum → Phalaris arundinacea ×2, Coronilla juncea → Crithmum maritimum ×2, Fraxinus angustifolia → Fraxinus excelsior ×2, Fraxinus ornus → Fraxinus angustifolia ×2, Geranium sylvaticum → Urtica dioica ×2, Hyacinthoides non-scripta → Plantago lanceolata ×2

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Abies_alba_leaf_1.jpg | Abies alba | leaf | 0.0 | - | OK Abies alba 1.00 |
| Abies_alba_leaf_2.jpg | Abies alba | leaf | 0.0 | - | OK Abies alba 1.00 |
| Abies_alba_bark_1.jpg | Abies alba | bark | 0.8 | X Bellis perennis 0.60 | X Acer pseudoplatanus 0.22 |
| Abies_alba_bark_2.jpg | Abies alba | bark | 0.0 | - | X Acer pseudoplatanus 0.88 |
| Acacia_dealbata_leaf_1.jpg | Acacia dealbata | leaf | 97.7 | OK Acacia dealbata 1.00 | OK Acacia dealbata 1.00 |
| Acacia_dealbata_leaf_2.jpg | Acacia dealbata | leaf | 0.2 | OK Acacia dealbata 0.13 | OK Acacia dealbata 1.00 |
| Acacia_dealbata_bark_1.jpg | Acacia dealbata | bark | 18.5 | X Cytisus scoparius 0.59 | OK Acacia dealbata 1.00 |
| Acacia_dealbata_bark_2.jpg | Acacia dealbata | bark | 0.0 | - | OK Acacia dealbata 0.85 |
| Acer_pseudoplatanus_bark_1.jpg | Acer pseudoplatanus | bark | 0.0 | - | OK Acer pseudoplatanus 0.54 |
| Acer_pseudoplatanus_bark_2.jpg | Acer pseudoplatanus | bark | 0.0 | - | OK Acer pseudoplatanus 0.99 |
| Acer_pseudoplatanus_leaf_1.jpg | Acer pseudoplatanus | leaf | 37.8 | OK Acer pseudoplatanus 0.96 | OK Acer pseudoplatanus 1.00 |
| Acer_pseudoplatanus_leaf_2.jpg | Acer pseudoplatanus | leaf | 81.8 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Achillea_millefolium_leaf_1.jpg | Achillea millefolium | leaf | 0.9 | X Teucrium scorodonia 0.25 | X Agrimonia eupatoria 0.55 |
| Achillea_millefolium_leaf_2.jpg | Achillea millefolium | leaf | 0.0 | - | X Meum athamanticum 0.93 |
| Adenostyles_alpina_leaf_1.jpg | Adenostyles alpina | leaf | 0.6 | X Asplenium scolopendrium 0.80 | X Alliaria petiolata 0.46 |
| Adenostyles_alpina_leaf_2.jpg | Adenostyles alpina | leaf | 72.0 | X Petasites hybridus 1.00 | X Petasites hybridus 0.92 |
| Adiantum_capillus-veneris_leaf_1.jpg | Adiantum capillus-veneris | leaf | 98.0 | OK Adiantum capillus-veneris 1.00 | OK Adiantum capillus-veneris 1.00 |
| Adiantum_capillus-veneris_leaf_2.jpg | Adiantum capillus-veneris | leaf | 0.7 | X Asplenium scolopendrium 0.67 | OK Adiantum capillus-veneris 1.00 |
| Adiantum_capillus-veneris_bark_1.jpg | Adiantum capillus-veneris | bark | 0.0 | - | OK Adiantum capillus-veneris 0.85 |
| Agrimonia_eupatoria_leaf_1.jpg | Agrimonia eupatoria | leaf | 86.0 | OK Agrimonia eupatoria 0.63 | OK Agrimonia eupatoria 0.91 |
| Agrimonia_eupatoria_leaf_2.jpg | Agrimonia eupatoria | leaf | 8.6 | X Urtica dioica 0.25 | X Argentina anserina 0.94 |
| Agrimonia_eupatoria_bark_1.jpg | Agrimonia eupatoria | bark | 3.5 | X Medicago lupulina 0.58 | OK Agrimonia eupatoria 1.00 |
| Agrostis_stolonifera_leaf_1.jpg | Agrostis stolonifera | leaf | 0.0 | - | X Agrostis canina 0.46 |
| Agrostis_stolonifera_leaf_2.jpg | Agrostis stolonifera | leaf | 77.2 | X Arrhenatherum elatius 0.38 | X Phragmites australis 0.32 |
| Ajuga_reptans_leaf_1.jpg | Ajuga reptans | leaf | 38.4 | OK Ajuga reptans 0.79 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_leaf_2.jpg | Ajuga reptans | leaf | 97.5 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_bark_1.jpg | Ajuga reptans | bark | 12.5 | OK Ajuga reptans 0.93 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_bark_2.jpg | Ajuga reptans | bark | 23.1 | X Bellis perennis 0.47 | OK Ajuga reptans 0.99 |
| Alliaria_petiolata_leaf_1.jpg | Alliaria petiolata | leaf | 19.7 | OK Alliaria petiolata 0.58 | OK Alliaria petiolata 0.98 |
| Alliaria_petiolata_leaf_2.jpg | Alliaria petiolata | leaf | 24.4 | OK Alliaria petiolata 0.94 | OK Alliaria petiolata 0.99 |
| Alliaria_petiolata_bark_1.jpg | Alliaria petiolata | bark | 0.0 | - | OK Alliaria petiolata 1.00 |
| Allium_victorialis_leaf_1.jpg | Allium victorialis | leaf | 22.2 | OK Allium victorialis 0.98 | OK Allium victorialis 1.00 |
| Allium_victorialis_leaf_2.jpg | Allium victorialis | leaf | 9.8 | OK Allium victorialis 0.76 | OK Allium victorialis 1.00 |
| Alnus_alnobetula_leaf_1.jpg | Alnus alnobetula | leaf | 22.2 | X Corylus avellana 0.72 | X Corylus avellana 0.41 |
| Alnus_alnobetula_leaf_2.jpg | Alnus alnobetula | leaf | 56.0 | X Corylus avellana 0.48 | OK Alnus alnobetula 0.38 |
| Alnus_alnobetula_bark_1.jpg | Alnus alnobetula | bark | 0.9 | X Trifolium repens 0.94 | X Quercus robur 0.65 |
| Alnus_alnobetula_bark_2.jpg | Alnus alnobetula | bark | 13.7 | X Betula pendula 0.58 | OK Alnus alnobetula 1.00 |
| Alopecurus_pratensis_leaf_1.jpg | Alopecurus pratensis | leaf | 0.0 | - | X Holcus lanatus 0.25 |
| Alopecurus_pratensis_leaf_2.jpg | Alopecurus pratensis | leaf | 0.0 | - | X Brachypodium pinnatum 0.25 |
| Anacamptis_pyramidalis_leaf_1.jpg | Anacamptis pyramidalis | leaf | 64.0 | OK Anacamptis pyramidalis 0.99 | OK Anacamptis pyramidalis 1.00 |
| Anacamptis_pyramidalis_leaf_2.jpg | Anacamptis pyramidalis | leaf | 97.5 | OK Anacamptis pyramidalis 0.45 | X Cephalanthera longifolia 0.45 |
| Anthoxanthum_odoratum_leaf_1.jpg | Anthoxanthum odoratum | leaf | 10.8 | X Phragmites australis 0.32 | OK Anthoxanthum odoratum 0.73 |
| Anthoxanthum_odoratum_leaf_2.jpg | Anthoxanthum odoratum | leaf | 0.3 | X Dactylorhiza maculata 0.51 | OK Anthoxanthum odoratum 0.98 |
| Anthoxanthum_odoratum_bark_1.jpg | Anthoxanthum odoratum | bark | 97.8 | X Arrhenatherum elatius 0.52 | X Arrhenatherum elatius 0.62 |
| Anthoxanthum_odoratum_bark_2.jpg | Anthoxanthum odoratum | bark | 64.4 | X Holcus lanatus 0.36 | X Holcus lanatus 0.77 |
| Anthriscus_sylvestris_leaf_1.jpg | Anthriscus sylvestris | leaf | 0.0 | - | OK Anthriscus sylvestris 0.98 |
| Anthriscus_sylvestris_leaf_2.jpg | Anthriscus sylvestris | leaf | 0.0 | - | OK Anthriscus sylvestris 1.00 |
| Anthriscus_sylvestris_bark_1.jpg | Anthriscus sylvestris | bark | 97.6 | OK Anthriscus sylvestris 0.66 | OK Anthriscus sylvestris 0.76 |
| Anthriscus_sylvestris_bark_2.jpg | Anthriscus sylvestris | bark | 1.4 | X Carex echinata 0.30 | OK Anthriscus sylvestris 1.00 |
| Anthyllis_vulneraria_leaf_1.jpg | Anthyllis vulneraria | leaf | 10.2 | X Arundo donax 0.50 | X Lotus pedunculatus 0.39 |
| Anthyllis_vulneraria_leaf_2.jpg | Anthyllis vulneraria | leaf | 97.4 | OK Anthyllis vulneraria 0.99 | OK Anthyllis vulneraria 0.99 |
| Aphyllanthes_monspeliensis_leaf_1.jpg | Aphyllanthes monspeliensis | leaf | 2.9 | OK Aphyllanthes monspeliensis 1.00 | OK Aphyllanthes monspeliensis 1.00 |
| Aphyllanthes_monspeliensis_leaf_2.jpg | Aphyllanthes monspeliensis | leaf | 0.0 | - | X Avenella flexuosa 0.70 |
| Aphyllanthes_monspeliensis_bark_1.jpg | Aphyllanthes monspeliensis | bark | 0.0 | - | OK Aphyllanthes monspeliensis 0.98 |
| Aphyllanthes_monspeliensis_bark_2.jpg | Aphyllanthes monspeliensis | bark | 0.0 | - | OK Aphyllanthes monspeliensis 1.00 |
| Aquilegia_atrata_leaf_1.jpg | Aquilegia atrata | leaf | 83.9 | OK Aquilegia atrata 1.00 | OK Aquilegia atrata 1.00 |
| Aquilegia_atrata_leaf_2.jpg | Aquilegia atrata | leaf | 64.8 | OK Aquilegia atrata 0.90 | OK Aquilegia atrata 0.74 |
| Arabidopsis_thaliana_leaf_1.jpg | Arabidopsis thaliana | leaf | 3.4 | X Medicago lupulina 0.21 | X Cerastium holosteoides 0.97 |
| Arabidopsis_thaliana_leaf_2.jpg | Arabidopsis thaliana | leaf | 80.0 | X Borago officinalis 0.71 | X Borago officinalis 0.37 |
| Arabidopsis_thaliana_bark_1.jpg | Arabidopsis thaliana | bark | 12.9 | X Hypericum perforatum 0.24 | X Impatiens balfourii 0.56 |
| Argentina_anserina_leaf_1.jpg | Argentina anserina | leaf | 37.8 | OK Argentina anserina 1.00 | OK Argentina anserina 1.00 |
| Argentina_anserina_leaf_2.jpg | Argentina anserina | leaf | 0.0 | - | X Prunus spinosa 0.75 |
| Argentina_anserina_bark_1.jpg | Argentina anserina | bark | 7.4 | X Trollius europaeus 0.29 | OK Argentina anserina 0.97 |
| Argentina_anserina_bark_2.jpg | Argentina anserina | bark | 0.0 | - | X Trifolium pratense 0.50 |
| Aristolochia_clematitis_leaf_1.jpg | Aristolochia clematitis | leaf | 97.4 | OK Aristolochia clematitis 1.00 | OK Aristolochia clematitis 1.00 |
| Aristolochia_clematitis_leaf_2.jpg | Aristolochia clematitis | leaf | 3.2 | X Fagopyrum esculentum 0.84 | OK Aristolochia clematitis 0.99 |
| Aristolochia_rotunda_leaf_1.jpg | Aristolochia rotunda | leaf | 50.8 | OK Aristolochia rotunda 0.96 | OK Aristolochia rotunda 0.55 |
| Aristolochia_rotunda_leaf_2.jpg | Aristolochia rotunda | leaf | 11.5 | X Medicago lupulina 0.78 | OK Aristolochia rotunda 0.97 |
| Aristolochia_rotunda_bark_1.jpg | Aristolochia rotunda | bark | 98.2 | OK Aristolochia rotunda 1.00 | OK Aristolochia rotunda 1.00 |
| Arrhenatherum_elatius_leaf_1.jpg | Arrhenatherum elatius | leaf | 0.0 | - | OK Arrhenatherum elatius 0.98 |
| Arrhenatherum_elatius_leaf_2.jpg | Arrhenatherum elatius | leaf | 0.0 | - | OK Arrhenatherum elatius 0.96 |
| Aruncus_dioicus_leaf_1.jpg | Aruncus dioicus | leaf | 3.3 | X Hedera helix 0.87 | OK Aruncus dioicus 0.97 |
| Aruncus_dioicus_leaf_2.jpg | Aruncus dioicus | leaf | 80.7 | X Rubus idaeus 1.00 | X Rubus fruticosus 0.80 |
| Arundo_donax_leaf_1.jpg | Arundo donax | leaf | 22.5 | OK Arundo donax 0.99 | X Phragmites australis 0.86 |
| Arundo_donax_leaf_2.jpg | Arundo donax | leaf | 0.0 | - | X Phragmites australis 0.53 |
| Arundo_donax_bark_1.jpg | Arundo donax | bark | 0.8 | X Ligustrum vulgare 0.29 | X Phragmites australis 0.65 |
| Arundo_donax_bark_2.jpg | Arundo donax | bark | 0.0 | - | X Fraxinus excelsior 0.62 |
| Asplenium_ceterach_leaf_1.jpg | Asplenium ceterach | leaf | 98.1 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 0.99 |
| Asplenium_ceterach_leaf_2.jpg | Asplenium ceterach | leaf | 1.0 | X Acacia dealbata 0.42 | OK Asplenium ceterach 1.00 |
| Asplenium_scolopendrium_leaf_1.jpg | Asplenium scolopendrium | leaf | 59.7 | OK Asplenium scolopendrium 1.00 | OK Asplenium scolopendrium 1.00 |
| Asplenium_scolopendrium_leaf_2.jpg | Asplenium scolopendrium | leaf | 96.7 | OK Asplenium scolopendrium 1.00 | OK Asplenium scolopendrium 1.00 |
| Astrantia_major_leaf_1.jpg | Astrantia major | leaf | 80.0 | X Heracleum sphondylium 0.46 | OK Astrantia major 0.76 |
| Astrantia_major_leaf_2.jpg | Astrantia major | leaf | 85.7 | OK Astrantia major 0.98 | OK Astrantia major 0.98 |
| Avenella_flexuosa_leaf_1.jpg | Avenella flexuosa | leaf | 0.0 | - | X Agrostis stolonifera 0.69 |
| Avenella_flexuosa_leaf_2.jpg | Avenella flexuosa | leaf | 0.0 | - | X Aphyllanthes monspeliensis 0.97 |
| Bellis_perennis_leaf_1.jpg | Bellis perennis | leaf | 66.5 | OK Bellis perennis 0.94 | OK Bellis perennis 0.99 |
| Bellis_perennis_leaf_2.jpg | Bellis perennis | leaf | 0.0 | - | OK Bellis perennis 1.00 |
| Bellis_perennis_bark_1.jpg | Bellis perennis | bark | 26.7 | OK Bellis perennis 0.89 | OK Bellis perennis 1.00 |
| Berberis_aetnensis_leaf_1.jpg | Berberis aetnensis | leaf | 97.3 | OK Berberis aetnensis 1.00 | OK Berberis aetnensis 1.00 |
| Berberis_aetnensis_bark_1.jpg | Berberis aetnensis | bark | 4.8 | X Holcus lanatus 0.75 | OK Berberis aetnensis 1.00 |
| Berberis_aetnensis_leaf_2.jpg | Berberis aetnensis | leaf | 0.0 | - | OK Berberis aetnensis 1.00 |
| Betula_pendula_bark_1.jpg | Betula pendula | bark | 0.0 | - | OK Betula pendula 0.84 |
| Betula_pendula_bark_2.jpg | Betula pendula | bark | 0.0 | - | OK Betula pendula 1.00 |
| Betula_pendula_leaf_1.jpg | Betula pendula | leaf | 13.3 | OK Betula pendula 1.00 | OK Betula pendula 1.00 |
| Betula_pendula_leaf_2.jpg | Betula pendula | leaf | 96.3 | OK Betula pendula 1.00 | OK Betula pendula 1.00 |
| Bituminaria_bituminosa_leaf_1.jpg | Bituminaria bituminosa | leaf | 0.7 | X Trifolium repens 0.41 | OK Bituminaria bituminosa 0.93 |
| Bituminaria_bituminosa_leaf_2.jpg | Bituminaria bituminosa | leaf | 97.9 | OK Bituminaria bituminosa 1.00 | OK Bituminaria bituminosa 1.00 |
| Bituminaria_bituminosa_bark_1.jpg | Bituminaria bituminosa | bark | 7.9 | X Ophioglossum vulgatum 0.44 | X Cytisus scoparius 0.79 |
| Blackstonia_perfoliata_leaf_1.jpg | Blackstonia perfoliata | leaf | 51.2 | X Fagus sylvatica 0.45 | X Crocus vernus 0.47 |
| Blackstonia_perfoliata_leaf_2.jpg | Blackstonia perfoliata | leaf | 67.2 | OK Blackstonia perfoliata 1.00 | OK Blackstonia perfoliata 0.99 |
| Borago_officinalis_leaf_1.jpg | Borago officinalis | leaf | 50.9 | X Digitalis purpurea 0.48 | OK Borago officinalis 0.65 |
| Borago_officinalis_leaf_2.jpg | Borago officinalis | leaf | 11.8 | OK Borago officinalis 0.77 | OK Borago officinalis 0.60 |
| Brachypodium_pinnatum_leaf_1.jpg | Brachypodium pinnatum | leaf | 0.0 | - | X Phalaris arundinacea 0.82 |
| Brachypodium_pinnatum_leaf_2.jpg | Brachypodium pinnatum | leaf | 0.0 | - | X Phalaris arundinacea 0.48 |
| Brachypodium_retusum_leaf_1.jpg | Brachypodium retusum | leaf | 0.0 | - | OK Brachypodium retusum 1.00 |
| Brachypodium_retusum_leaf_2.jpg | Brachypodium retusum | leaf | 0.0 | - | OK Brachypodium retusum 1.00 |
| Bromus_hordeaceus_leaf_1.jpg | Bromus hordeaceus | leaf | 46.1 | OK Bromus hordeaceus 0.95 | OK Bromus hordeaceus 1.00 |
| Bromus_hordeaceus_leaf_2.jpg | Bromus hordeaceus | leaf | 0.0 | - | OK Bromus hordeaceus 0.80 |
| Bupleurum_baldense_leaf_1.jpg | Bupleurum baldense | leaf | 46.6 | X Brachypodium retusum 0.87 | OK Bupleurum baldense 1.00 |
| Bupleurum_fruticosum_leaf_1.jpg | Bupleurum fruticosum | leaf | 6.2 | X Ligustrum vulgare 0.80 | X Phillyrea latifolia 0.27 |
| Bupleurum_fruticosum_leaf_2.jpg | Bupleurum fruticosum | leaf | 93.6 | OK Bupleurum fruticosum 1.00 | OK Bupleurum fruticosum 0.99 |
| Bupleurum_fruticosum_bark_1.jpg | Bupleurum fruticosum | bark | 0.0 | - | X Ilex aquifolium 0.26 |
| Bupleurum_fruticosum_bark_2.jpg | Bupleurum fruticosum | bark | 6.1 | X Bellis perennis 0.34 | X Cornus mas 0.45 |
| Buxus_sempervirens_leaf_1.jpg | Buxus sempervirens | leaf | 0.1 | X Hypochaeris robertia 0.79 | OK Buxus sempervirens 0.99 |
| Buxus_sempervirens_leaf_2.jpg | Buxus sempervirens | leaf | 23.9 | OK Buxus sempervirens 1.00 | OK Buxus sempervirens 1.00 |
| Buxus_sempervirens_bark_1.jpg | Buxus sempervirens | bark | 0.0 | - | OK Buxus sempervirens 0.39 |
| Buxus_sempervirens_bark_2.jpg | Buxus sempervirens | bark | 2.3 | X Bellis perennis 0.71 | OK Buxus sempervirens 0.97 |
| Calluna_vulgaris_leaf_1.jpg | Calluna vulgaris | leaf | 1.7 | X Neottia ovata 0.21 | OK Calluna vulgaris 0.80 |
| Calluna_vulgaris_leaf_2.jpg | Calluna vulgaris | leaf | 95.0 | OK Calluna vulgaris 0.99 | OK Calluna vulgaris 0.98 |
| Calluna_vulgaris_bark_1.jpg | Calluna vulgaris | bark | 0.0 | - | X Genista salzmannii 0.34 |
| Calluna_vulgaris_bark_2.jpg | Calluna vulgaris | bark | 0.0 | - | OK Calluna vulgaris 0.98 |
| Capsella_bursa-pastoris_leaf_1.jpg | Capsella bursa-pastoris | leaf | 96.9 | OK Capsella bursa-pastoris 0.87 | X Hypochaeris robertia 0.50 |
| Capsella_bursa-pastoris_leaf_2.jpg | Capsella bursa-pastoris | leaf | 2.6 | X Urtica dioica 0.30 | OK Capsella bursa-pastoris 0.98 |
| Capsella_bursa-pastoris_bark_1.jpg | Capsella bursa-pastoris | bark | 94.5 | X Cerastium holosteoides 0.79 | OK Capsella bursa-pastoris 0.55 |
| Cardamine_pentaphyllos_leaf_1.jpg | Cardamine pentaphyllos | leaf | 79.3 | OK Cardamine pentaphyllos 1.00 | OK Cardamine pentaphyllos 1.00 |
| Carex_flacca_leaf_1.jpg | Carex flacca | leaf | 3.7 | X Anthoxanthum odoratum 0.34 | X Festuca altissima 0.89 |
| Carex_flacca_leaf_2.jpg | Carex flacca | leaf | 1.5 | X Plantago lanceolata 0.29 | OK Carex flacca 0.93 |
| Carex_hirta_leaf_1.jpg | Carex hirta | leaf | 45.7 | X Arrhenatherum elatius 0.46 | X Dactylis glomerata 0.22 |
| Carex_hirta_leaf_2.jpg | Carex hirta | leaf | 0.4 | X Viola biflora 0.47 | OK Carex hirta 0.97 |
| Carex_hirta_bark_1.jpg | Carex hirta | bark | 0.0 | - | OK Carex hirta 0.85 |
| Carex_hirta_bark_2.jpg | Carex hirta | bark | 6.1 | X Holcus lanatus 0.22 | X Carex flacca 0.42 |
| Carex_nigra_leaf_1.jpg | Carex nigra | leaf | 0.0 | - | X Dactylis glomerata 0.83 |
| Carex_nigra_leaf_2.jpg | Carex nigra | leaf | 97.0 | X Carex flacca 0.62 | X Carex flacca 0.90 |
| Carex_panicea_leaf_1.jpg | Carex panicea | leaf | 0.0 | - | X Carex flacca 0.27 |
| Castanea_sativa_bark_1.jpg | Castanea sativa | bark | 0.0 | - | X Quercus petraea 0.58 |
| Castanea_sativa_bark_2.jpg | Castanea sativa | bark | 1.6 | X Arabidopsis thaliana 0.79 | X Cornus mas 0.74 |
| Castanea_sativa_leaf_1.jpg | Castanea sativa | leaf | 53.9 | OK Castanea sativa 0.99 | OK Castanea sativa 1.00 |
| Castanea_sativa_leaf_2.jpg | Castanea sativa | leaf | 95.0 | OK Castanea sativa 1.00 | OK Castanea sativa 1.00 |
| Castroviejoa_frigida_leaf_1.jpg | Castroviejoa frigida | leaf | 0.0 | - | X Juniperus communis 0.47 |
| Catapodium_rigidum_leaf_1.jpg | Catapodium rigidum | leaf | 0.5 | X Asplenium scolopendrium 0.44 | OK Catapodium rigidum 0.98 |
| Catapodium_rigidum_leaf_2.jpg | Catapodium rigidum | leaf | 0.0 | - | OK Catapodium rigidum 1.00 |
| Catapodium_rigidum_bark_1.jpg | Catapodium rigidum | bark | 1.2 | X Digitalis purpurea 0.32 | OK Catapodium rigidum 0.94 |
| Centaurea_calcitrapa_leaf_1.jpg | Centaurea calcitrapa | leaf | 1.0 | X Petasites hybridus 0.28 | X Echium vulgare 0.38 |
| Centaurea_calcitrapa_leaf_2.jpg | Centaurea calcitrapa | leaf | 0.0 | - | X Cirsium vulgare 1.00 |
| Cephalanthera_longifolia_leaf_1.jpg | Cephalanthera longifolia | leaf | 0.8 | X Quercus ilex 0.62 | OK Cephalanthera longifolia 1.00 |
| Cephalanthera_longifolia_leaf_2.jpg | Cephalanthera longifolia | leaf | 1.9 | X Castanea sativa 0.76 | OK Cephalanthera longifolia 1.00 |
| Cephalanthera_longifolia_bark_1.jpg | Cephalanthera longifolia | bark | 50.6 | OK Cephalanthera longifolia 0.99 | OK Cephalanthera longifolia 1.00 |
| Cerastium_soleirolii_leaf_1.jpg | Cerastium soleirolii | leaf | 6.0 | X Anthoxanthum odoratum 0.49 | X Anthyllis vulneraria 0.52 |
| Cerastium_soleirolii_bark_1.jpg | Cerastium soleirolii | bark | 3.0 | X Cistus salviifolius 0.46 | X Rabelera holostea 0.63 |
| Chelidonium_majus_leaf_1.jpg | Chelidonium majus | leaf | 32.7 | OK Chelidonium majus 0.99 | X Fraxinus excelsior 0.32 |
| Chelidonium_majus_leaf_2.jpg | Chelidonium majus | leaf | 0.0 | - | OK Chelidonium majus 1.00 |
| Chelidonium_majus_bark_1.jpg | Chelidonium majus | bark | 97.8 | OK Chelidonium majus 0.87 | OK Chelidonium majus 0.90 |
| Cirsium_oleraceum_leaf_1.jpg | Cirsium oleraceum | leaf | 76.3 | OK Cirsium oleraceum 1.00 | OK Cirsium oleraceum 1.00 |
| Cirsium_oleraceum_leaf_2.jpg | Cirsium oleraceum | leaf | 0.5 | X Asplenium ceterach 0.22 | OK Cirsium oleraceum 0.73 |
| Cirsium_oleraceum_bark_1.jpg | Cirsium oleraceum | bark | 37.9 | X Urtica dioica 0.61 | OK Cirsium oleraceum 0.60 |
| Cirsium_oleraceum_bark_2.jpg | Cirsium oleraceum | bark | 67.6 | OK Cirsium oleraceum 0.95 | OK Cirsium oleraceum 0.90 |
| Cirsium_vulgare_leaf_1.jpg | Cirsium vulgare | leaf | 75.3 | OK Cirsium vulgare 1.00 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_leaf_2.jpg | Cirsium vulgare | leaf | 0.5 | X Quercus ilex 0.29 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_bark_1.jpg | Cirsium vulgare | bark | 97.9 | OK Cirsium vulgare 0.89 | OK Cirsium vulgare 0.93 |
| Cirsium_vulgare_bark_2.jpg | Cirsium vulgare | bark | 15.4 | OK Cirsium vulgare 0.99 | OK Cirsium vulgare 0.98 |
| Cistus_albidus_leaf_1.jpg | Cistus albidus | leaf | 0.9 | OK Cistus albidus 0.98 | OK Cistus albidus 1.00 |
| Cistus_albidus_leaf_2.jpg | Cistus albidus | leaf | 0.7 | X Bellis perennis 0.29 | OK Cistus albidus 1.00 |
| Cistus_albidus_bark_1.jpg | Cistus albidus | bark | 22.4 | X Arundo donax 0.57 | OK Cistus albidus 0.97 |
| Cistus_albidus_bark_2.jpg | Cistus albidus | bark | 1.5 | X Trifolium pratense 0.83 | X Bupleurum baldense 0.23 |
| Cistus_salviifolius_leaf_1.jpg | Cistus salviifolius | leaf | 1.2 | X Digitalis purpurea 0.81 | OK Cistus salviifolius 0.99 |
| Cistus_salviifolius_leaf_2.jpg | Cistus salviifolius | leaf | 0.0 | - | OK Cistus salviifolius 0.54 |
| Cistus_salviifolius_bark_1.jpg | Cistus salviifolius | bark | 0.0 | - | X Alnus alnobetula 0.47 |
| Coris_monspeliensis_leaf_1.jpg | Coris monspeliensis | leaf | 0.0 | - | OK Coris monspeliensis 1.00 |
| Coris_monspeliensis_leaf_2.jpg | Coris monspeliensis | leaf | 97.8 | OK Coris monspeliensis 0.98 | OK Coris monspeliensis 0.98 |
| Coris_monspeliensis_bark_1.jpg | Coris monspeliensis | bark | 98.1 | OK Coris monspeliensis 0.88 | OK Coris monspeliensis 0.88 |
| Cornus_mas_bark_1.jpg | Cornus mas | bark | 0.0 | - | OK Cornus mas 0.97 |
| Cornus_mas_bark_2.jpg | Cornus mas | bark | 0.0 | - | OK Cornus mas 0.77 |
| Cornus_mas_leaf_1.jpg | Cornus mas | leaf | 0.0 | - | OK Cornus mas 1.00 |
| Cornus_mas_leaf_2.jpg | Cornus mas | leaf | 50.4 | OK Cornus mas 1.00 | OK Cornus mas 1.00 |
| Cornus_sanguinea_bark_1.jpg | Cornus sanguinea | bark | 28.8 | X Gentiana lutea 0.15 | OK Cornus sanguinea 0.56 |
| Cornus_sanguinea_leaf_1.jpg | Cornus sanguinea | leaf | 1.1 | X Pteridium aquilinum 0.21 | OK Cornus sanguinea 1.00 |
| Cornus_sanguinea_bark_2.jpg | Cornus sanguinea | bark | 0.0 | - | OK Cornus sanguinea 1.00 |
| Cornus_sanguinea_leaf_2.jpg | Cornus sanguinea | leaf | 2.6 | OK Cornus sanguinea 0.78 | OK Cornus sanguinea 0.93 |
| Coronilla_juncea_leaf_1.jpg | Coronilla juncea | leaf | 2.7 | X Trifolium repens 0.42 | X Crithmum maritimum 0.87 |
| Coronilla_juncea_leaf_2.jpg | Coronilla juncea | leaf | 0.0 | - | X Ruta corsica 0.96 |
| Coronilla_juncea_bark_1.jpg | Coronilla juncea | bark | 55.3 | X Euphorbia spinosa 0.48 | X Crithmum maritimum 0.48 |
| Coronilla_juncea_bark_2.jpg | Coronilla juncea | bark | 0.9 | X Hypochaeris robertia 0.51 | X Impatiens balfourii 0.61 |
| Corylus_avellana_bark_1.jpg | Corylus avellana | bark | 0.0 | - | X Fraxinus excelsior 0.39 |
| Corylus_avellana_bark_2.jpg | Corylus avellana | bark | 22.0 | X Viburnum lantana 0.59 | OK Corylus avellana 0.81 |
| Corylus_avellana_leaf_1.jpg | Corylus avellana | leaf | 7.2 | X Anacamptis pyramidalis 0.46 | OK Corylus avellana 1.00 |
| Corylus_avellana_leaf_2.jpg | Corylus avellana | leaf | 29.0 | OK Corylus avellana 1.00 | OK Corylus avellana 1.00 |
| Crataegus_monogyna_bark_1.jpg | Crataegus monogyna | bark | 0.0 | - | X Sorbus aucuparia 0.56 |
| Crataegus_monogyna_bark_2.jpg | Crataegus monogyna | bark | 1.5 | X Silybum marianum 0.23 | X Anthoxanthum odoratum 0.15 |
| Crataegus_monogyna_leaf_1.jpg | Crataegus monogyna | leaf | 1.6 | X Plantago lanceolata 0.26 | OK Crataegus monogyna 0.93 |
| Crataegus_monogyna_leaf_2.jpg | Crataegus monogyna | leaf | 0.9 | X Acacia dealbata 0.66 | OK Crataegus monogyna 0.99 |
| Crithmum_maritimum_leaf_1.jpg | Crithmum maritimum | leaf | 0.0 | - | OK Crithmum maritimum 0.95 |
| Crithmum_maritimum_leaf_2.jpg | Crithmum maritimum | leaf | 97.9 | OK Crithmum maritimum 1.00 | OK Crithmum maritimum 1.00 |
| Crithmum_maritimum_bark_1.jpg | Crithmum maritimum | bark | 97.9 | OK Crithmum maritimum 1.00 | OK Crithmum maritimum 1.00 |
| Crithmum_maritimum_bark_2.jpg | Crithmum maritimum | bark | 48.3 | X Anacamptis pyramidalis 0.34 | X Scorzonera humilis 0.31 |
| Crocus_vernus_leaf_1.jpg | Crocus vernus | leaf | 56.3 | X Carex panicea 0.21 | OK Crocus vernus 0.54 |
| Crocus_vernus_leaf_2.jpg | Crocus vernus | leaf | 23.4 | X Fagus sylvatica 1.00 | OK Crocus vernus 0.87 |
| Cytisus_scoparius_bark_1.jpg | Cytisus scoparius | bark | 0.9 | X Trifolium repens 0.33 | X Picris hieracioides 0.39 |
| Cytisus_scoparius_leaf_1.jpg | Cytisus scoparius | leaf | 0.0 | - | OK Cytisus scoparius 0.96 |
| Cytisus_scoparius_leaf_2.jpg | Cytisus scoparius | leaf | 0.0 | - | OK Cytisus scoparius 1.00 |
| Cytisus_scoparius_bark_2.jpg | Cytisus scoparius | bark | 0.7 | X Bellis perennis 0.38 | X Cornus sanguinea 0.41 |
| Dactylis_glomerata_leaf_1.jpg | Dactylis glomerata | leaf | 0.7 | X Acacia dealbata 0.16 | OK Dactylis glomerata 0.64 |
| Dactylis_glomerata_leaf_2.jpg | Dactylis glomerata | leaf | 0.0 | - | OK Dactylis glomerata 0.66 |
| Dactylorhiza_maculata_leaf_1.jpg | Dactylorhiza maculata | leaf | 4.2 | X Carex echinata 0.99 | OK Dactylorhiza maculata 0.97 |
| Dactylorhiza_maculata_leaf_2.jpg | Dactylorhiza maculata | leaf | 23.6 | X Carex echinata 0.88 | X Orchis mascula 0.39 |
| Dactylorhiza_sambucina_leaf_1.jpg | Dactylorhiza sambucina | leaf | 14.2 | X Phalaris arundinacea 0.58 | X Allium victorialis 0.41 |
| Dactylorhiza_sambucina_leaf_2.jpg | Dactylorhiza sambucina | leaf | 17.0 | X Ophioglossum vulgatum 0.78 | X Gymnadenia conopsea 0.36 |
| Digitalis_purpurea_leaf_1.jpg | Digitalis purpurea | leaf | 66.5 | OK Digitalis purpurea 0.99 | OK Digitalis purpurea 0.99 |
| Digitalis_purpurea_leaf_2.jpg | Digitalis purpurea | leaf | 79.5 | OK Digitalis purpurea 1.00 | OK Digitalis purpurea 1.00 |
| Dryopteris_filix-mas_leaf_1.jpg | Dryopteris filix-mas | leaf | 4.4 | X Asplenium scolopendrium 0.73 | OK Dryopteris filix-mas 1.00 |
| Dryopteris_filix-mas_leaf_2.jpg | Dryopteris filix-mas | leaf | 43.7 | OK Dryopteris filix-mas 1.00 | OK Dryopteris filix-mas 0.99 |
| Dryopteris_filix-mas_bark_1.jpg | Dryopteris filix-mas | bark | 11.4 | X Polystichum lonchitis 0.78 | OK Dryopteris filix-mas 0.93 |
| Ecballium_elaterium_leaf_1.jpg | Ecballium elaterium | leaf | 0.6 | X Asplenium scolopendrium 0.45 | OK Ecballium elaterium 1.00 |
| Ecballium_elaterium_leaf_2.jpg | Ecballium elaterium | leaf | 67.7 | X Aristolochia clematitis 0.97 | X Aristolochia rotunda 0.61 |
| Echium_vulgare_leaf_1.jpg | Echium vulgare | leaf | 97.8 | OK Echium vulgare 0.96 | OK Echium vulgare 0.96 |
| Echium_vulgare_leaf_2.jpg | Echium vulgare | leaf | 98.1 | OK Echium vulgare 0.99 | OK Echium vulgare 0.99 |
| Echium_vulgare_bark_1.jpg | Echium vulgare | bark | 10.2 | OK Echium vulgare 0.55 | OK Echium vulgare 1.00 |
| Echium_vulgare_bark_2.jpg | Echium vulgare | bark | 97.2 | OK Echium vulgare 1.00 | OK Echium vulgare 1.00 |
| Erica_cinerea_leaf_1.jpg | Erica cinerea | leaf | 0.0 | - | OK Erica cinerea 0.73 |
| Erica_cinerea_leaf_2.jpg | Erica cinerea | leaf | 0.3 | X Vicia cracca 0.20 | X Calluna vulgaris 0.99 |
| Eryngium_campestre_leaf_1.jpg | Eryngium campestre | leaf | 29.6 | OK Eryngium campestre 1.00 | X Polygonatum verticillatum 0.44 |
| Eryngium_campestre_leaf_2.jpg | Eryngium campestre | leaf | 25.2 | X Primula veris 0.58 | X Cirsium oleraceum 0.49 |
| Eryngium_campestre_bark_1.jpg | Eryngium campestre | bark | 97.8 | X Scorzonera humilis 0.50 | X Scorzonera humilis 0.69 |
| Eryngium_campestre_bark_2.jpg | Eryngium campestre | bark | 1.3 | X Medicago lupulina 0.72 | X Heracleum sphondylium 0.50 |
| Eupatorium_cannabinum_leaf_1.jpg | Eupatorium cannabinum | leaf | 65.2 | OK Eupatorium cannabinum 0.67 | OK Eupatorium cannabinum 0.33 |
| Eupatorium_cannabinum_leaf_2.jpg | Eupatorium cannabinum | leaf | 55.0 | OK Eupatorium cannabinum 0.99 | OK Eupatorium cannabinum 0.95 |
| Eupatorium_cannabinum_bark_1.jpg | Eupatorium cannabinum | bark | 97.7 | OK Eupatorium cannabinum 0.40 | OK Eupatorium cannabinum 0.49 |
| Eupatorium_cannabinum_bark_2.jpg | Eupatorium cannabinum | bark | 47.2 | OK Eupatorium cannabinum 0.59 | X Sambucus ebulus 0.47 |
| Euphorbia_cyparissias_leaf_1.jpg | Euphorbia cyparissias | leaf | 0.2 | X Medicago lupulina 0.12 | X Plantago lanceolata 0.21 |
| Euphorbia_cyparissias_leaf_2.jpg | Euphorbia cyparissias | leaf | 5.7 | X Asplenium scolopendrium 0.39 | OK Euphorbia cyparissias 0.97 |
| Euphorbia_cyparissias_bark_1.jpg | Euphorbia cyparissias | bark | 97.4 | OK Euphorbia cyparissias 0.98 | OK Euphorbia cyparissias 0.97 |
| Euphorbia_palustris_leaf_1.jpg | Euphorbia palustris | leaf | 52.8 | OK Euphorbia palustris 1.00 | OK Euphorbia palustris 0.98 |
| Euphorbia_palustris_leaf_2.jpg | Euphorbia palustris | leaf | 94.2 | X Helleborus foetidus 0.41 | OK Euphorbia palustris 0.43 |
| Euphorbia_palustris_bark_1.jpg | Euphorbia palustris | bark | 9.6 | X Arundo donax 0.79 | OK Euphorbia palustris 0.99 |
| Euphorbia_spinosa_leaf_1.jpg | Euphorbia spinosa | leaf | 13.0 | X Carex flacca 0.53 | X Bupleurum fruticosum 1.00 |
| Euphorbia_spinosa_leaf_2.jpg | Euphorbia spinosa | leaf | 6.3 | X Holcus lanatus 0.81 | OK Euphorbia spinosa 0.98 |
| Euphorbia_spinosa_bark_1.jpg | Euphorbia spinosa | bark | 7.2 | X Ribes rubrum 0.24 | X Alliaria petiolata 0.56 |
| Euphorbia_spinosa_bark_2.jpg | Euphorbia spinosa | bark | 2.8 | X Holcus mollis 0.19 | OK Euphorbia spinosa 1.00 |
| Fagopyrum_esculentum_leaf_1.jpg | Fagopyrum esculentum | leaf | 39.9 | X Impatiens balfourii 0.75 | X Hedera helix 0.29 |
| Fagopyrum_esculentum_leaf_2.jpg | Fagopyrum esculentum | leaf | 79.6 | OK Fagopyrum esculentum 1.00 | OK Fagopyrum esculentum 1.00 |
| Fagopyrum_esculentum_bark_1.jpg | Fagopyrum esculentum | bark | 0.0 | - | OK Fagopyrum esculentum 0.74 |
| Fagus_sylvatica_bark_1.jpg | Fagus sylvatica | bark | 0.0 | - | X Ostrya carpinifolia 0.32 |
| Fagus_sylvatica_leaf_1.jpg | Fagus sylvatica | leaf | 15.3 | OK Fagus sylvatica 0.87 | OK Fagus sylvatica 0.99 |
| Fagus_sylvatica_leaf_2.jpg | Fagus sylvatica | leaf | 75.0 | OK Fagus sylvatica 0.52 | X Quercus petraea 0.45 |
| Fagus_sylvatica_bark_2.jpg | Fagus sylvatica | bark | 0.0 | - | OK Fagus sylvatica 0.63 |
| Festuca_rubra_leaf_1.jpg | Festuca rubra | leaf | 0.0 | - | X Anthoxanthum odoratum 0.26 |
| Fraxinus_angustifolia_bark_1.jpg | Fraxinus angustifolia | bark | 0.0 | - | X Ligustrum vulgare 0.22 |
| Fraxinus_angustifolia_bark_2.jpg | Fraxinus angustifolia | bark | 0.0 | - | X Cornus mas 0.77 |
| Fraxinus_angustifolia_leaf_1.jpg | Fraxinus angustifolia | leaf | 66.4 | X Fraxinus excelsior 0.92 | X Fraxinus excelsior 0.83 |
| Fraxinus_angustifolia_leaf_2.jpg | Fraxinus angustifolia | leaf | 0.0 | - | X Fraxinus excelsior 0.77 |
| Fraxinus_excelsior_bark_1.jpg | Fraxinus excelsior | bark | 0.0 | - | OK Fraxinus excelsior 0.98 |
| Fraxinus_excelsior_leaf_1.jpg | Fraxinus excelsior | leaf | 0.0 | - | OK Fraxinus excelsior 0.82 |
| Fraxinus_excelsior_bark_2.jpg | Fraxinus excelsior | bark | 0.0 | - | X Acacia dealbata 0.97 |
| Fraxinus_excelsior_leaf_2.jpg | Fraxinus excelsior | leaf | 1.0 | X Trifolium repens 0.76 | OK Fraxinus excelsior 0.71 |
| Fraxinus_ornus_bark_1.jpg | Fraxinus ornus | bark | 0.0 | - | X Crataegus monogyna 0.62 |
| Fraxinus_ornus_bark_2.jpg | Fraxinus ornus | bark | 0.0 | - | X Ilex aquifolium 0.56 |
| Fraxinus_ornus_leaf_1.jpg | Fraxinus ornus | leaf | 64.8 | X Fraxinus excelsior 0.91 | X Fraxinus angustifolia 0.59 |
| Fraxinus_ornus_leaf_2.jpg | Fraxinus ornus | leaf | 0.0 | - | X Fraxinus angustifolia 0.73 |
| Galium_mollugo_leaf_1.jpg | Galium mollugo | leaf | 1.0 | X Urtica dioica 0.47 | OK Galium mollugo 1.00 |
| Galium_mollugo_leaf_2.jpg | Galium mollugo | leaf | 42.2 | OK Galium mollugo 0.99 | OK Galium mollugo 0.99 |
| Galium_odoratum_leaf_1.jpg | Galium odoratum | leaf | 20.9 | OK Galium odoratum 1.00 | OK Galium odoratum 1.00 |
| Galium_odoratum_leaf_2.jpg | Galium odoratum | leaf | 0.8 | X Acer pseudoplatanus 0.19 | X Bupleurum fruticosum 0.51 |
| Genista_cinerea_leaf_1.jpg | Genista cinerea | leaf | 0.0 | - | OK Genista cinerea 0.56 |
| Genista_cinerea_leaf_2.jpg | Genista cinerea | leaf | 0.0 | - | X Cytisus scoparius 1.00 |
| Gentiana_lutea_leaf_1.jpg | Gentiana lutea | leaf | 97.6 | OK Gentiana lutea 0.84 | OK Gentiana lutea 0.79 |
| Gentiana_lutea_leaf_2.jpg | Gentiana lutea | leaf | 4.3 | OK Gentiana lutea 0.48 | OK Gentiana lutea 0.99 |
| Gentiana_lutea_bark_1.jpg | Gentiana lutea | bark | 20.6 | X Medicago lupulina 0.87 | X Sambucus ebulus 0.54 |
| Gentiana_lutea_bark_2.jpg | Gentiana lutea | bark | 3.4 | X Digitalis purpurea 0.41 | X Hypericum perforatum 0.25 |
| Geranium_dissectum_leaf_1.jpg | Geranium dissectum | leaf | 97.9 | X Aconitum lycoctonum 0.62 | X Aconitum lycoctonum 0.69 |
| Geranium_dissectum_leaf_2.jpg | Geranium dissectum | leaf | 9.1 | X Bellis perennis 0.65 | OK Geranium dissectum 1.00 |
| Geranium_dissectum_bark_1.jpg | Geranium dissectum | bark | 0.0 | - | OK Geranium dissectum 0.66 |
| Geranium_dissectum_bark_2.jpg | Geranium dissectum | bark | 0.0 | - | OK Geranium dissectum 0.69 |
| Geranium_sylvaticum_leaf_1.jpg | Geranium sylvaticum | leaf | 23.5 | X Trollius europaeus 0.53 | OK Geranium sylvaticum 0.89 |
| Geranium_sylvaticum_leaf_2.jpg | Geranium sylvaticum | leaf | 78.7 | X Aconitum lycoctonum 0.58 | OK Geranium sylvaticum 0.90 |
| Geranium_sylvaticum_bark_1.jpg | Geranium sylvaticum | bark | 37.9 | X Melissa officinalis 0.39 | X Urtica dioica 0.25 |
| Geranium_sylvaticum_bark_2.jpg | Geranium sylvaticum | bark | 9.6 | X Holcus lanatus 0.56 | X Urtica dioica 0.50 |
| Globularia_bisnagarica_leaf_1.jpg | Globularia bisnagarica | leaf | 94.3 | X Anthyllis vulneraria 0.89 | X Ruta corsica 0.59 |
| Globularia_bisnagarica_leaf_2.jpg | Globularia bisnagarica | leaf | 6.5 | X Medicago lupulina 0.26 | X Bellis perennis 0.46 |
| Globularia_bisnagarica_bark_1.jpg | Globularia bisnagarica | bark | 11.0 | X Asplenium scolopendrium 0.23 | OK Globularia bisnagarica 0.97 |
| Gymnadenia_conopsea_leaf_1.jpg | Gymnadenia conopsea | leaf | 22.8 | X Globularia bisnagarica 0.85 | OK Gymnadenia conopsea 0.97 |
| Gymnadenia_conopsea_leaf_2.jpg | Gymnadenia conopsea | leaf | 33.9 | X Allium victorialis 0.92 | X Orchis purpurea 0.80 |
| Gymnadenia_conopsea_bark_1.jpg | Gymnadenia conopsea | bark | 26.2 | OK Gymnadenia conopsea 0.87 | OK Gymnadenia conopsea 0.99 |
| Gymnocarpium_robertianum_leaf_1.jpg | Gymnocarpium robertianum | leaf | 0.0 | - | OK Gymnocarpium robertianum 0.61 |
| Gymnocarpium_robertianum_leaf_2.jpg | Gymnocarpium robertianum | leaf | 10.5 | X Prenanthes purpurea 0.60 | OK Gymnocarpium robertianum 1.00 |
| Hedera_helix_leaf_1.jpg | Hedera helix | leaf | 0.2 | X Trifolium repens 0.50 | OK Hedera helix 1.00 |
| Hedera_helix_leaf_2.jpg | Hedera helix | leaf | 0.8 | X Teucrium scorodonia 0.17 | OK Hedera helix 1.00 |
| Hedera_helix_bark_1.jpg | Hedera helix | bark | 0.4 | X Bellis perennis 0.60 | X Buxus sempervirens 0.49 |
| Hedera_helix_bark_2.jpg | Hedera helix | bark | 0.0 | - | OK Hedera helix 1.00 |
| Helleborus_foetidus_leaf_1.jpg | Helleborus foetidus | leaf | 73.8 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Helleborus_foetidus_leaf_2.jpg | Helleborus foetidus | leaf | 98.0 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Helleborus_foetidus_bark_1.jpg | Helleborus foetidus | bark | 1.2 | X Medicago lupulina 0.21 | X Bupleurum fruticosum 0.76 |
| Helleborus_foetidus_bark_2.jpg | Helleborus foetidus | bark | 11.8 | X Bupleurum fruticosum 0.73 | OK Helleborus foetidus 1.00 |
| Heracleum_sphondylium_leaf_1.jpg | Heracleum sphondylium | leaf | 39.0 | OK Heracleum sphondylium 0.87 | OK Heracleum sphondylium 1.00 |
| Heracleum_sphondylium_leaf_2.jpg | Heracleum sphondylium | leaf | 0.1 | X Petasites hybridus 0.28 | OK Heracleum sphondylium 0.97 |
| Heracleum_sphondylium_bark_1.jpg | Heracleum sphondylium | bark | 41.4 | X Urtica dioica 0.82 | OK Heracleum sphondylium 0.97 |
| Heracleum_sphondylium_bark_2.jpg | Heracleum sphondylium | bark | 0.0 | - | OK Heracleum sphondylium 0.96 |
| Himantoglossum_robertianum_leaf_1.jpg | Himantoglossum robertianum | leaf | 64.5 | OK Himantoglossum robertianum 0.99 | OK Himantoglossum robertianum 0.98 |
| Himantoglossum_robertianum_leaf_2.jpg | Himantoglossum robertianum | leaf | 18.6 | X Allium victorialis 0.68 | X Allium victorialis 0.89 |
| Himantoglossum_robertianum_bark_1.jpg | Himantoglossum robertianum | bark | 44.4 | OK Himantoglossum robertianum 1.00 | OK Himantoglossum robertianum 0.99 |
| Himantoglossum_robertianum_bark_2.jpg | Himantoglossum robertianum | bark | 98.1 | OK Himantoglossum robertianum 0.77 | OK Himantoglossum robertianum 0.89 |
| Holcus_lanatus_leaf_1.jpg | Holcus lanatus | leaf | 85.4 | X Bromus hordeaceus 0.61 | X Carex flacca 0.67 |
| Holcus_lanatus_leaf_2.jpg | Holcus lanatus | leaf | 0.0 | - | X Dactylis glomerata 0.86 |
| Holcus_lanatus_bark_1.jpg | Holcus lanatus | bark | 0.0 | - | X Alopecurus pratensis 0.83 |
| Holcus_lanatus_bark_2.jpg | Holcus lanatus | bark | 8.7 | X Phragmites australis 0.33 | OK Holcus lanatus 0.85 |
| Hyacinthoides_non-scripta_leaf_1.jpg | Hyacinthoides non-scripta | leaf | 7.3 | X Quercus robur 0.31 | X Plantago lanceolata 0.55 |
| Hyacinthoides_non-scripta_leaf_2.jpg | Hyacinthoides non-scripta | leaf | 81.4 | OK Hyacinthoides non-scripta 0.88 | X Plantago lanceolata 0.45 |
| Hyacinthoides_non-scripta_bark_1.jpg | Hyacinthoides non-scripta | bark | 53.9 | OK Hyacinthoides non-scripta 0.42 | X Gymnadenia conopsea 0.38 |
| Hypericum_perforatum_bark_1.jpg | Hypericum perforatum | bark | 0.0 | - | X Phragmites australis 0.82 |
| Hypericum_perforatum_leaf_1.jpg | Hypericum perforatum | leaf | 0.0 | - | X Anthriscus sylvestris 0.28 |
| Hypericum_perforatum_leaf_2.jpg | Hypericum perforatum | leaf | 0.0 | - | X Lathyrus pratensis 0.68 |
| Hypericum_perforatum_bark_2.jpg | Hypericum perforatum | bark | 2.9 | X Ophioglossum vulgatum 0.42 | OK Hypericum perforatum 0.89 |
| Ilex_aquifolium_leaf_1.jpg | Ilex aquifolium | leaf | 71.2 | OK Ilex aquifolium 0.77 | OK Ilex aquifolium 0.58 |
| Ilex_aquifolium_leaf_2.jpg | Ilex aquifolium | leaf | 45.7 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Ilex_aquifolium_bark_1.jpg | Ilex aquifolium | bark | 1.4 | X Bellis perennis 0.57 | OK Ilex aquifolium 0.61 |
| Ilex_aquifolium_bark_2.jpg | Ilex aquifolium | bark | 0.0 | - | X Betula pendula 0.46 |
| Impatiens_balfourii_leaf_1.jpg | Impatiens balfourii | leaf | 58.6 | OK Impatiens balfourii 1.00 | OK Impatiens balfourii 1.00 |
| Impatiens_balfourii_leaf_2.jpg | Impatiens balfourii | leaf | 97.7 | OK Impatiens balfourii 0.76 | OK Impatiens balfourii 0.82 |
| Iris_lutescens_leaf_1.jpg | Iris lutescens | leaf | 0.3 | X Digitalis purpurea 0.13 | OK Iris lutescens 0.96 |
| Iris_lutescens_leaf_2.jpg | Iris lutescens | leaf | 1.8 | X Scorzonera humilis 0.40 | X Allium victorialis 0.88 |
| Juncus_acutiflorus_leaf_1.jpg | Juncus acutiflorus | leaf | 70.8 | OK Juncus acutiflorus 0.69 | OK Juncus acutiflorus 0.99 |
| Juncus_acutiflorus_leaf_2.jpg | Juncus acutiflorus | leaf | 4.2 | X Holcus lanatus 0.81 | X Medicago lupulina 0.26 |
| Juncus_acutus_leaf_1.jpg | Juncus acutus | leaf | 0.0 | - | OK Juncus acutus 0.97 |
| Juncus_acutus_leaf_2.jpg | Juncus acutus | leaf | 0.0 | - | OK Juncus acutus 1.00 |
| Juncus_acutus_bark_1.jpg | Juncus acutus | bark | 0.0 | - | X Carex flacca 0.98 |
| Juniperus_communis_leaf_1.jpg | Juniperus communis | leaf | 0.0 | - | X Juniperus oxycedrus 0.86 |
| Juniperus_communis_leaf_2.jpg | Juniperus communis | leaf | 1.5 | X Castanea sativa 0.13 | OK Juniperus communis 1.00 |
| Juniperus_communis_bark_1.jpg | Juniperus communis | bark | 0.0 | - | OK Juniperus communis 0.73 |
| Juniperus_communis_bark_2.jpg | Juniperus communis | bark | 1.1 | X Pteridium aquilinum 0.15 | OK Juniperus communis 1.00 |
| Juniperus_oxycedrus_leaf_1.jpg | Juniperus oxycedrus | leaf | 0.0 | - | OK Juniperus oxycedrus 1.00 |
| Juniperus_oxycedrus_leaf_2.jpg | Juniperus oxycedrus | leaf | 0.0 | - | X Juniperus communis 0.68 |
| Juniperus_oxycedrus_bark_1.jpg | Juniperus oxycedrus | bark | 0.0 | - | X Buxus sempervirens 0.61 |
| Juniperus_oxycedrus_bark_2.jpg | Juniperus oxycedrus | bark | 0.0 | - | OK Juniperus oxycedrus 0.53 |
| Juniperus_phoenicea_leaf_1.jpg | Juniperus phoenicea | leaf | 0.2 | X Digitalis purpurea 0.52 | OK Juniperus phoenicea 1.00 |
| Juniperus_phoenicea_leaf_2.jpg | Juniperus phoenicea | leaf | 0.0 | - | OK Juniperus phoenicea 1.00 |
| Juniperus_phoenicea_bark_1.jpg | Juniperus phoenicea | bark | 37.1 | OK Juniperus phoenicea 0.91 | X Genista salzmannii 0.70 |
| Juniperus_phoenicea_bark_2.jpg | Juniperus phoenicea | bark | 0.0 | - | OK Juniperus phoenicea 0.78 |
| Lactuca_perennis_leaf_1.jpg | Lactuca perennis | leaf | 78.8 | OK Lactuca perennis 0.98 | OK Lactuca perennis 0.97 |
| Lactuca_perennis_leaf_2.jpg | Lactuca perennis | leaf | 86.5 | OK Lactuca perennis 0.79 | OK Lactuca perennis 0.73 |
| Lactuca_perennis_bark_1.jpg | Lactuca perennis | bark | 3.1 | X Bupleurum fruticosum 0.68 | X Reichardia picroides 0.70 |
| Lathyrus_pratensis_leaf_1.jpg | Lathyrus pratensis | leaf | 0.0 | - | X Vicia sepium 0.25 |
| Lathyrus_pratensis_leaf_2.jpg | Lathyrus pratensis | leaf | 3.0 | X Carex echinata 0.24 | X Phillyrea latifolia 0.30 |
| Ligustrum_vulgare_leaf_1.jpg | Ligustrum vulgare | leaf | 0.9 | X Acacia dealbata 0.55 | X Cytisus scoparius 0.68 |
| Ligustrum_vulgare_leaf_2.jpg | Ligustrum vulgare | leaf | 4.0 | X Acacia dealbata 0.57 | OK Ligustrum vulgare 0.98 |
| Ligustrum_vulgare_bark_1.jpg | Ligustrum vulgare | bark | 0.0 | - | OK Ligustrum vulgare 0.99 |
| Ligustrum_vulgare_bark_2.jpg | Ligustrum vulgare | bark | 18.6 | X Senecio ovatus 0.86 | OK Ligustrum vulgare 0.99 |
| Lotus_corniculatus_leaf_1.jpg | Lotus corniculatus | leaf | 14.5 | X Ophioglossum vulgatum 0.99 | X Lotus maritimus 0.98 |
| Lotus_corniculatus_leaf_2.jpg | Lotus corniculatus | leaf | 95.3 | X Lotus maritimus 0.68 | X Lotus maritimus 0.54 |
| Lotus_maritimus_leaf_1.jpg | Lotus maritimus | leaf | 1.2 | X Plantago lanceolata 0.20 | X Lotus pedunculatus 0.52 |
| Lotus_maritimus_leaf_2.jpg | Lotus maritimus | leaf | 14.5 | X Lotus corniculatus 0.69 | OK Lotus maritimus 0.97 |
| Lotus_maritimus_bark_1.jpg | Lotus maritimus | bark | 97.5 | OK Lotus maritimus 0.97 | OK Lotus maritimus 0.97 |
| Lotus_maritimus_bark_2.jpg | Lotus maritimus | bark | 0.0 | - | OK Lotus maritimus 0.99 |
| Luzula_luzuloides_leaf_1.jpg | Luzula luzuloides | leaf | 97.3 | X Phalaris arundinacea 0.37 | X Scorzonera humilis 0.46 |
| Luzula_luzuloides_leaf_2.jpg | Luzula luzuloides | leaf | 0.0 | - | X Brachypodium pinnatum 0.50 |
| Medicago_lupulina_leaf_1.jpg | Medicago lupulina | leaf | 97.9 | OK Medicago lupulina 0.40 | X Trifolium repens 0.44 |
| Medicago_lupulina_leaf_2.jpg | Medicago lupulina | leaf | 97.7 | OK Medicago lupulina 0.98 | OK Medicago lupulina 0.98 |
| Medicago_lupulina_bark_1.jpg | Medicago lupulina | bark | 4.3 | X Trifolium pratense 0.38 | OK Medicago lupulina 0.97 |
| Melissa_officinalis_leaf_1.jpg | Melissa officinalis | leaf | 15.4 | X Betula pendula 0.63 | X Alliaria petiolata 0.44 |
| Melissa_officinalis_leaf_2.jpg | Melissa officinalis | leaf | 0.0 | - | OK Melissa officinalis 0.94 |
| Melissa_officinalis_bark_1.jpg | Melissa officinalis | bark | 16.8 | OK Melissa officinalis 0.54 | X Alliaria petiolata 0.82 |
| Melittis_melissophyllum_leaf_1.jpg | Melittis melissophyllum | leaf | 47.3 | X Melissa officinalis 0.64 | OK Melittis melissophyllum 0.88 |
| Melittis_melissophyllum_leaf_2.jpg | Melittis melissophyllum | leaf | 61.0 | X Melissa officinalis 0.66 | OK Melittis melissophyllum 0.66 |
| Meum_athamanticum_leaf_1.jpg | Meum athamanticum | leaf | 2.8 | X Ophioglossum vulgatum 0.19 | OK Meum athamanticum 0.99 |
| Meum_athamanticum_leaf_2.jpg | Meum athamanticum | leaf | 30.4 | OK Meum athamanticum 0.46 | OK Meum athamanticum 0.62 |
| Meum_athamanticum_bark_1.jpg | Meum athamanticum | bark | 91.3 | X Fagopyrum esculentum 0.37 | OK Meum athamanticum 0.33 |
| Meum_athamanticum_bark_2.jpg | Meum athamanticum | bark | 97.4 | OK Meum athamanticum 1.00 | OK Meum athamanticum 1.00 |
| Molinia_caerulea_leaf_1.jpg | Molinia caerulea | leaf | 0.0 | - | X Agrostis canina 0.71 |
| Molinia_caerulea_leaf_2.jpg | Molinia caerulea | leaf | 0.0 | - | X Dactylis glomerata 0.99 |
| Narcissus_dubius_leaf_1.jpg | Narcissus dubius | leaf | 50.9 | OK Narcissus dubius 1.00 | OK Narcissus dubius 1.00 |
| Narcissus_dubius_bark_1.jpg | Narcissus dubius | bark | 77.9 | OK Narcissus dubius 0.90 | OK Narcissus dubius 0.97 |
| Narcissus_dubius_leaf_2.jpg | Narcissus dubius | leaf | 0.0 | - | X Carex flacca 0.64 |
| Narcissus_dubius_bark_2.jpg | Narcissus dubius | bark | 97.9 | OK Narcissus dubius 0.89 | OK Narcissus dubius 0.96 |
| Narthecium_reverchonii_leaf_1.jpg | Narthecium reverchonii | leaf | 0.0 | - | OK Narthecium reverchonii 1.00 |
| Neottia_ovata_leaf_1.jpg | Neottia ovata | leaf | 59.4 | OK Neottia ovata 0.91 | OK Neottia ovata 0.97 |
| Neottia_ovata_leaf_2.jpg | Neottia ovata | leaf | 13.5 | OK Neottia ovata 0.98 | OK Neottia ovata 1.00 |
| Ophioglossum_vulgatum_leaf_1.jpg | Ophioglossum vulgatum | leaf | 27.8 | OK Ophioglossum vulgatum 0.99 | OK Ophioglossum vulgatum 0.58 |
| Ophioglossum_vulgatum_leaf_2.jpg | Ophioglossum vulgatum | leaf | 23.1 | OK Ophioglossum vulgatum 1.00 | OK Ophioglossum vulgatum 1.00 |
| Orchis_anthropophora_leaf_1.jpg | Orchis anthropophora | leaf | 16.1 | X Phalaris arundinacea 0.49 | X Gymnadenia conopsea 0.82 |
| Orchis_anthropophora_leaf_2.jpg | Orchis anthropophora | leaf | 8.2 | X Carex hirta 0.92 | X Dactylorhiza sambucina 0.41 |
| Orchis_mascula_leaf_1.jpg | Orchis mascula | leaf | 6.0 | X Hedera helix 0.88 | OK Orchis mascula 0.97 |
| Orchis_mascula_leaf_2.jpg | Orchis mascula | leaf | 85.0 | OK Orchis mascula 0.85 | OK Orchis mascula 0.57 |
| Orchis_purpurea_leaf_1.jpg | Orchis purpurea | leaf | 69.4 | X Himantoglossum robertianum 0.37 | OK Orchis purpurea 0.60 |
| Orchis_purpurea_leaf_2.jpg | Orchis purpurea | leaf | 17.0 | X Himantoglossum robertianum 0.45 | X Himantoglossum robertianum 0.45 |
| Ostrya_carpinifolia_leaf_1.jpg | Ostrya carpinifolia | leaf | 1.7 | X Asplenium scolopendrium 0.99 | OK Ostrya carpinifolia 0.78 |
| Ostrya_carpinifolia_leaf_2.jpg | Ostrya carpinifolia | leaf | 2.0 | X Asplenium scolopendrium 0.99 | OK Ostrya carpinifolia 0.82 |
| Ostrya_carpinifolia_bark_1.jpg | Ostrya carpinifolia | bark | 0.0 | - | X Castanea sativa 0.47 |
| Ostrya_carpinifolia_bark_2.jpg | Ostrya carpinifolia | bark | 0.0 | - | X Sorbus aucuparia 0.35 |
| Paris_quadrifolia_leaf_1.jpg | Paris quadrifolia | leaf | 97.1 | OK Paris quadrifolia 1.00 | OK Paris quadrifolia 1.00 |
| Paris_quadrifolia_leaf_2.jpg | Paris quadrifolia | leaf | 54.9 | OK Paris quadrifolia 1.00 | OK Paris quadrifolia 1.00 |
| Petasites_hybridus_bark_1.jpg | Petasites hybridus | bark | 6.4 | X Hedera helix 0.29 | X Himantoglossum robertianum 0.54 |
| Petasites_hybridus_leaf_1.jpg | Petasites hybridus | leaf | 53.9 | X Solanum dulcamara 0.48 | OK Petasites hybridus 0.96 |
| Petasites_hybridus_leaf_2.jpg | Petasites hybridus | leaf | 34.9 | OK Petasites hybridus 0.97 | OK Petasites hybridus 0.98 |
| Petasites_hybridus_bark_2.jpg | Petasites hybridus | bark | 37.7 | X Carex echinata 0.51 | X Urtica dioica 0.69 |
| Phalaris_arundinacea_leaf_1.jpg | Phalaris arundinacea | leaf | 19.8 | X Arundo donax 0.59 | X Arundo donax 0.69 |
| Phalaris_arundinacea_leaf_2.jpg | Phalaris arundinacea | leaf | 0.0 | - | OK Phalaris arundinacea 0.50 |
| Phillyrea_latifolia_leaf_1.jpg | Phillyrea latifolia | leaf | 5.4 | X Acer pseudoplatanus 0.47 | X Quercus coccifera 0.35 |
| Phillyrea_latifolia_leaf_2.jpg | Phillyrea latifolia | leaf | 3.1 | X Prunus laurocerasus 0.60 | OK Phillyrea latifolia 0.99 |
| Phillyrea_latifolia_bark_1.jpg | Phillyrea latifolia | bark | 0.3 | X Bellis perennis 0.23 | X Ilex aquifolium 0.35 |
| Phillyrea_latifolia_bark_2.jpg | Phillyrea latifolia | bark | 0.4 | X Plantago coronopus 0.28 | X Fraxinus angustifolia 0.46 |
| Phragmites_australis_leaf_1.jpg | Phragmites australis | leaf | 0.5 | X Holcus mollis 0.97 | OK Phragmites australis 1.00 |
| Phragmites_australis_leaf_2.jpg | Phragmites australis | leaf | 0.0 | - | OK Phragmites australis 1.00 |
| Phragmites_australis_bark_1.jpg | Phragmites australis | bark | 0.0 | - | OK Phragmites australis 0.84 |
| Phragmites_australis_bark_2.jpg | Phragmites australis | bark | 0.0 | - | OK Phragmites australis 1.00 |
| Picris_hieracioides_leaf_1.jpg | Picris hieracioides | leaf | 36.6 | OK Picris hieracioides 0.91 | X Arabidopsis thaliana 0.67 |
| Picris_hieracioides_leaf_2.jpg | Picris hieracioides | leaf | 97.3 | X Lactuca perennis 0.35 | X Hypochaeris robertia 0.36 |
| Picris_hieracioides_bark_1.jpg | Picris hieracioides | bark | 18.4 | X Holcus lanatus 0.74 | X Achillea millefolium 0.51 |
| Picris_hieracioides_bark_2.jpg | Picris hieracioides | bark | 60.8 | X Saxifraga granulata 0.14 | OK Picris hieracioides 0.88 |
| Pinguicula_corsica_leaf_1.jpg | Pinguicula corsica | leaf | 92.5 | X Neottia ovata 0.50 | X Lotus pedunculatus 0.46 |
| Pinus_nigra_leaf_1.jpg | Pinus nigra | leaf | 1.2 | X Trifolium repens 0.71 | X Pinus pinaster 0.91 |
| Pinus_nigra_bark_1.jpg | Pinus nigra | bark | 0.0 | - | X Cornus mas 0.46 |
| Pinus_nigra_bark_2.jpg | Pinus nigra | bark | 0.0 | - | X Pinus sylvestris 0.47 |
| Pinus_nigra_leaf_2.jpg | Pinus nigra | leaf | 65.2 | OK Pinus nigra 0.96 | OK Pinus nigra 0.97 |
| Pinus_pinaster_bark_1.jpg | Pinus pinaster | bark | 0.0 | - | X Pinus sylvestris 0.92 |
| Pinus_pinaster_bark_2.jpg | Pinus pinaster | bark | 0.0 | - | X Castanea sativa 0.95 |
| Pinus_pinaster_leaf_1.jpg | Pinus pinaster | leaf | 0.0 | - | OK Pinus pinaster 0.90 |
| Pinus_pinaster_leaf_2.jpg | Pinus pinaster | leaf | 0.0 | - | X Pinus nigra 0.98 |
| Pinus_sylvestris_leaf_1.jpg | Pinus sylvestris | leaf | 0.0 | - | OK Pinus sylvestris 0.82 |
| Pinus_sylvestris_leaf_2.jpg | Pinus sylvestris | leaf | 0.0 | - | OK Pinus sylvestris 0.96 |
| Pinus_sylvestris_bark_1.jpg | Pinus sylvestris | bark | 0.0 | - | X Crataegus monogyna 0.60 |
| Pinus_sylvestris_bark_2.jpg | Pinus sylvestris | bark | 0.0 | - | X Juniperus phoenicea 0.56 |
| Pistacia_lentiscus_leaf_1.jpg | Pistacia lentiscus | leaf | 0.0 | - | OK Pistacia lentiscus 1.00 |
| Pistacia_lentiscus_leaf_2.jpg | Pistacia lentiscus | leaf | 0.9 | X Acer pseudoplatanus 0.24 | OK Pistacia lentiscus 1.00 |
| Pistacia_lentiscus_bark_1.jpg | Pistacia lentiscus | bark | 8.8 | X Trifolium repens 0.21 | X Cornus mas 0.54 |
| Pistacia_lentiscus_bark_2.jpg | Pistacia lentiscus | bark | 2.6 | X Acer pseudoplatanus 0.37 | OK Pistacia lentiscus 0.93 |
| Plantago_coronopus_leaf_1.jpg | Plantago coronopus | leaf | 95.7 | OK Plantago coronopus 0.99 | OK Plantago coronopus 1.00 |
| Plantago_coronopus_leaf_2.jpg | Plantago coronopus | leaf | 1.6 | X Plantago lanceolata 0.60 | OK Plantago coronopus 0.94 |
| Plantago_coronopus_bark_1.jpg | Plantago coronopus | bark | 97.9 | OK Plantago coronopus 0.99 | OK Plantago coronopus 1.00 |
| Plantago_lanceolata_leaf_1.jpg | Plantago lanceolata | leaf | 97.6 | OK Plantago lanceolata 0.81 | OK Plantago lanceolata 0.90 |
| Plantago_lanceolata_leaf_2.jpg | Plantago lanceolata | leaf | 6.6 | X Arundo donax 0.30 | X Scorzonera humilis 0.55 |
| Polygonatum_verticillatum_leaf_1.jpg | Polygonatum verticillatum | leaf | 97.2 | OK Polygonatum verticillatum 1.00 | OK Polygonatum verticillatum 1.00 |
| Polygonatum_verticillatum_leaf_2.jpg | Polygonatum verticillatum | leaf | 73.8 | OK Polygonatum verticillatum 0.99 | OK Polygonatum verticillatum 0.86 |
| Polystichum_lonchitis_leaf_1.jpg | Polystichum lonchitis | leaf | 4.9 | X Bellis perennis 0.16 | OK Polystichum lonchitis 1.00 |
| Polystichum_lonchitis_leaf_2.jpg | Polystichum lonchitis | leaf | 82.4 | OK Polystichum lonchitis 0.97 | OK Polystichum lonchitis 0.99 |
| Potentilla_erecta_leaf_1.jpg | Potentilla erecta | leaf | 0.3 | X Gentiana lutea 0.19 | OK Potentilla erecta 0.93 |
| Potentilla_erecta_leaf_2.jpg | Potentilla erecta | leaf | 97.2 | OK Potentilla erecta 1.00 | OK Potentilla erecta 1.00 |
| Potentilla_erecta_bark_1.jpg | Potentilla erecta | bark | 0.8 | X Trifolium repens 0.69 | OK Potentilla erecta 1.00 |
| Potentilla_micrantha_leaf_1.jpg | Potentilla micrantha | leaf | 2.2 | X Acacia dealbata 0.27 | OK Potentilla micrantha 0.69 |
| Potentilla_micrantha_bark_1.jpg | Potentilla micrantha | bark | 7.7 | X Corylus avellana 0.27 | OK Potentilla micrantha 0.99 |
| Potentilla_micrantha_leaf_2.jpg | Potentilla micrantha | leaf | 98.0 | OK Potentilla micrantha 1.00 | OK Potentilla micrantha 1.00 |
| Prenanthes_purpurea_leaf_1.jpg | Prenanthes purpurea | leaf | 0.0 | - | X Impatiens balfourii 0.22 |
| Prenanthes_purpurea_leaf_2.jpg | Prenanthes purpurea | leaf | 2.1 | X Medicago lupulina 0.44 | OK Prenanthes purpurea 0.99 |
| Primula_veris_leaf_1.jpg | Primula veris | leaf | 4.8 | X Senecio ovatus 0.27 | OK Primula veris 1.00 |
| Primula_veris_leaf_2.jpg | Primula veris | leaf | 72.9 | OK Primula veris 0.72 | X Silybum marianum 0.69 |
| Prunus_laurocerasus_leaf_1.jpg | Prunus laurocerasus | leaf | 34.1 | OK Prunus laurocerasus 0.99 | OK Prunus laurocerasus 1.00 |
| Prunus_laurocerasus_leaf_2.jpg | Prunus laurocerasus | leaf | 16.5 | X Acacia dealbata 0.42 | OK Prunus laurocerasus 0.96 |
| Prunus_laurocerasus_bark_1.jpg | Prunus laurocerasus | bark | 97.9 | X Quercus robur 0.36 | OK Prunus laurocerasus 0.44 |
| Prunus_laurocerasus_bark_2.jpg | Prunus laurocerasus | bark | 17.5 | X Bupleurum fruticosum 0.56 | OK Prunus laurocerasus 0.98 |
| Prunus_spinosa_bark_1.jpg | Prunus spinosa | bark | 0.0 | - | X Cornus mas 0.88 |
| Prunus_spinosa_bark_2.jpg | Prunus spinosa | bark | 0.0 | - | OK Prunus spinosa 0.58 |
| Prunus_spinosa_leaf_1.jpg | Prunus spinosa | leaf | 56.3 | OK Prunus spinosa 1.00 | OK Prunus spinosa 1.00 |
| Prunus_spinosa_leaf_2.jpg | Prunus spinosa | leaf | 97.4 | OK Prunus spinosa 0.93 | OK Prunus spinosa 0.91 |
| Pteridium_aquilinum_leaf_1.jpg | Pteridium aquilinum | leaf | 0.2 | X Vicia cracca 0.33 | OK Pteridium aquilinum 1.00 |
| Pteridium_aquilinum_leaf_2.jpg | Pteridium aquilinum | leaf | 0.0 | - | OK Pteridium aquilinum 1.00 |
| Pteridium_aquilinum_bark_1.jpg | Pteridium aquilinum | bark | 0.8 | X Ligustrum vulgare 0.26 | OK Pteridium aquilinum 0.40 |
| Quercus_coccifera_leaf_1.jpg | Quercus coccifera | leaf | 0.0 | - | OK Quercus coccifera 0.91 |
| Quercus_coccifera_leaf_2.jpg | Quercus coccifera | leaf | 0.2 | X Quercus petraea 0.37 | OK Quercus coccifera 0.71 |
| Quercus_coccifera_bark_1.jpg | Quercus coccifera | bark | 0.0 | - | X Crataegus monogyna 0.34 |
| Quercus_coccifera_bark_2.jpg | Quercus coccifera | bark | 4.3 | X Trifolium repens 0.37 | OK Quercus coccifera 0.50 |
| Quercus_ilex_leaf_1.jpg | Quercus ilex | leaf | 95.0 | OK Quercus ilex 0.58 | OK Quercus ilex 0.56 |
| Quercus_ilex_leaf_2.jpg | Quercus ilex | leaf | 12.6 | X Fraxinus ornus 0.64 | OK Quercus ilex 1.00 |
| Quercus_ilex_bark_1.jpg | Quercus ilex | bark | 4.9 | X Acacia dealbata 0.47 | OK Quercus ilex 0.95 |
| Quercus_ilex_bark_2.jpg | Quercus ilex | bark | 0.0 | - | OK Quercus ilex 0.57 |
| Quercus_petraea_bark_1.jpg | Quercus petraea | bark | 1.3 | X Pteridium aquilinum 0.16 | X Cornus mas 0.37 |
| Quercus_petraea_leaf_1.jpg | Quercus petraea | leaf | 35.7 | X Quercus robur 0.69 | X Quercus pubescens 0.91 |
| Quercus_petraea_leaf_2.jpg | Quercus petraea | leaf | 27.7 | OK Quercus petraea 0.64 | OK Quercus petraea 0.53 |
| Quercus_petraea_bark_2.jpg | Quercus petraea | bark | 0.0 | - | OK Quercus petraea 0.96 |
| Quercus_pubescens_leaf_1.jpg | Quercus pubescens | leaf | 25.9 | OK Quercus pubescens 0.79 | X Quercus petraea 0.96 |
| Quercus_pubescens_leaf_2.jpg | Quercus pubescens | leaf | 0.0 | - | X Quercus coccifera 0.70 |
| Quercus_pubescens_bark_1.jpg | Quercus pubescens | bark | 0.0 | - | X Pinus nigra 0.22 |
| Quercus_pubescens_bark_2.jpg | Quercus pubescens | bark | 0.0 | - | X Acacia dealbata 0.37 |
| Quercus_robur_bark_1.jpg | Quercus robur | bark | 0.0 | - | X Quercus ilex 0.54 |
| Quercus_robur_leaf_1.jpg | Quercus robur | leaf | 0.0 | - | X Quercus petraea 0.53 |
| Quercus_robur_leaf_2.jpg | Quercus robur | leaf | 56.0 | OK Quercus robur 0.98 | OK Quercus robur 0.94 |
| Quercus_robur_bark_2.jpg | Quercus robur | bark | 0.0 | - | X Crataegus monogyna 0.29 |
| Reichardia_picroides_leaf_1.jpg | Reichardia picroides | leaf | 12.9 | X Lactuca perennis 0.76 | OK Reichardia picroides 0.82 |
| Reichardia_picroides_leaf_2.jpg | Reichardia picroides | leaf | 97.5 | OK Reichardia picroides 0.99 | OK Reichardia picroides 1.00 |
| Ribes_rubrum_leaf_1.jpg | Ribes rubrum | leaf | 8.7 | OK Ribes rubrum 0.97 | OK Ribes rubrum 1.00 |
| Ribes_rubrum_leaf_2.jpg | Ribes rubrum | leaf | 11.7 | OK Ribes rubrum 1.00 | OK Ribes rubrum 0.99 |
| Rubus_fruticosus_leaf_1.jpg | Rubus fruticosus | leaf | 6.9 | X Hedera helix 0.39 | X Agrimonia eupatoria 0.43 |
| Rubus_fruticosus_leaf_2.jpg | Rubus fruticosus | leaf | 97.7 | X Corylus avellana 0.56 | X Corylus avellana 0.80 |
| Rubus_fruticosus_bark_1.jpg | Rubus fruticosus | bark | 1.5 | X Trifolium repens 0.15 | X Rubus idaeus 0.65 |
| Rubus_idaeus_leaf_1.jpg | Rubus idaeus | leaf | 87.7 | OK Rubus idaeus 0.99 | OK Rubus idaeus 1.00 |
| Rubus_idaeus_leaf_2.jpg | Rubus idaeus | leaf | 89.7 | OK Rubus idaeus 1.00 | OK Rubus idaeus 0.88 |
| Rubus_idaeus_bark_1.jpg | Rubus idaeus | bark | 9.2 | X Bellis perennis 0.76 | OK Rubus idaeus 0.78 |
| Ruta_corsica_leaf_1.jpg | Ruta corsica | leaf | 1.4 | X Phillyrea latifolia 0.23 | OK Ruta corsica 1.00 |
| Salix_retusa_leaf_1.jpg | Salix retusa | leaf | 0.0 | - | OK Salix retusa 0.91 |
| Salix_retusa_leaf_2.jpg | Salix retusa | leaf | 93.5 | OK Salix retusa 1.00 | OK Salix retusa 1.00 |
| Salvia_rosmarinus_leaf_1.jpg | Salvia rosmarinus | leaf | 0.0 | - | OK Salvia rosmarinus 1.00 |
| Salvia_rosmarinus_leaf_2.jpg | Salvia rosmarinus | leaf | 0.0 | - | OK Salvia rosmarinus 1.00 |
| Salvia_rosmarinus_bark_1.jpg | Salvia rosmarinus | bark | 11.6 | X Adiantum capillus-veneris 0.68 | X Cornus mas 0.38 |
| Sambucus_ebulus_leaf_1.jpg | Sambucus ebulus | leaf | 73.5 | OK Sambucus ebulus 0.94 | OK Sambucus ebulus 0.86 |
| Sambucus_ebulus_leaf_2.jpg | Sambucus ebulus | leaf | 45.8 | OK Sambucus ebulus 0.98 | OK Sambucus ebulus 0.98 |
| Saxifraga_aizoides_leaf_1.jpg | Saxifraga aizoides | leaf | 0.0 | - | OK Saxifraga aizoides 0.78 |
| Saxifraga_aizoides_leaf_2.jpg | Saxifraga aizoides | leaf | 15.5 | OK Saxifraga aizoides 0.97 | OK Saxifraga aizoides 1.00 |
| Saxifraga_callosa_leaf_1.jpg | Saxifraga callosa | leaf | 97.7 | X Saxifraga paniculata 1.00 | X Saxifraga paniculata 1.00 |
| Saxifraga_callosa_leaf_2.jpg | Saxifraga callosa | leaf | 88.4 | OK Saxifraga callosa 0.88 | OK Saxifraga callosa 0.98 |
| Saxifraga_granulata_leaf_1.jpg | Saxifraga granulata | leaf | 35.7 | X Anthoxanthum odoratum 0.44 | X Scorzonera humilis 0.70 |
| Saxifraga_granulata_leaf_2.jpg | Saxifraga granulata | leaf | 54.0 | OK Saxifraga granulata 1.00 | OK Saxifraga granulata 1.00 |
| Saxifraga_granulata_bark_1.jpg | Saxifraga granulata | bark | 4.8 | X Alopecurus pratensis 0.70 | OK Saxifraga granulata 1.00 |
| Saxifraga_paniculata_leaf_1.jpg | Saxifraga paniculata | leaf | 97.3 | OK Saxifraga paniculata 0.81 | OK Saxifraga paniculata 0.79 |
| Saxifraga_paniculata_leaf_2.jpg | Saxifraga paniculata | leaf | 2.1 | X Digitalis purpurea 0.80 | OK Saxifraga paniculata 1.00 |
| Scorzonera_humilis_leaf_1.jpg | Scorzonera humilis | leaf | 7.2 | X Carex panicea 0.65 | X Anacamptis pyramidalis 0.23 |
| Scorzonera_humilis_leaf_2.jpg | Scorzonera humilis | leaf | 4.0 | X Impatiens balfourii 0.46 | X Lactuca perennis 0.86 |
| Sedum_acre_leaf_1.jpg | Sedum acre | leaf | 97.7 | OK Sedum acre 1.00 | OK Sedum acre 1.00 |
| Sedum_acre_leaf_2.jpg | Sedum acre | leaf | 98.0 | OK Sedum acre 1.00 | OK Sedum acre 1.00 |
| Sedum_acre_bark_1.jpg | Sedum acre | bark | 0.0 | - | OK Sedum acre 0.98 |
| Senecio_ovatus_leaf_1.jpg | Senecio ovatus | leaf | 91.2 | OK Senecio ovatus 0.98 | OK Senecio ovatus 0.99 |
| Senecio_ovatus_leaf_2.jpg | Senecio ovatus | leaf | 48.0 | OK Senecio ovatus 0.66 | X Prenanthes purpurea 0.94 |
| Silaum_silaus_leaf_1.jpg | Silaum silaus | leaf | 0.0 | - | OK Silaum silaus 0.98 |
| Silaum_silaus_leaf_2.jpg | Silaum silaus | leaf | 1.0 | X Trifolium pratense 0.51 | OK Silaum silaus 0.80 |
| Silybum_marianum_leaf_1.jpg | Silybum marianum | leaf | 2.6 | X Pteridium aquilinum 0.31 | OK Silybum marianum 1.00 |
| Silybum_marianum_leaf_2.jpg | Silybum marianum | leaf | 63.7 | OK Silybum marianum 1.00 | OK Silybum marianum 1.00 |
| Silybum_marianum_bark_1.jpg | Silybum marianum | bark | 0.0 | - | OK Silybum marianum 0.85 |
| Solanum_dulcamara_leaf_1.jpg | Solanum dulcamara | leaf | 17.8 | OK Solanum dulcamara 0.69 | OK Solanum dulcamara 0.49 |
| Solanum_dulcamara_leaf_2.jpg | Solanum dulcamara | leaf | 97.4 | OK Solanum dulcamara 0.68 | OK Solanum dulcamara 0.52 |
| Solanum_dulcamara_bark_1.jpg | Solanum dulcamara | bark | 4.2 | X Ophioglossum vulgatum 0.77 | X Hyacinthoides non-scripta 0.61 |
| Sorbus_aucuparia_leaf_1.jpg | Sorbus aucuparia | leaf | 95.5 | OK Sorbus aucuparia 0.92 | OK Sorbus aucuparia 0.97 |
| Sorbus_aucuparia_leaf_2.jpg | Sorbus aucuparia | leaf | 0.0 | - | OK Sorbus aucuparia 1.00 |
| Sorbus_aucuparia_bark_1.jpg | Sorbus aucuparia | bark | 0.0 | - | OK Sorbus aucuparia 0.90 |
| Sorbus_aucuparia_bark_2.jpg | Sorbus aucuparia | bark | 0.0 | - | OK Sorbus aucuparia 0.82 |
| Stachys_corsica_bark_1.jpg | Stachys corsica | bark | 1.6 | X Neottia ovata 0.63 | OK Stachys corsica 0.80 |
| Stachys_corsica_leaf_1.jpg | Stachys corsica | leaf | 2.2 | X Himantoglossum robertianum 0.56 | X Melissa officinalis 0.75 |
| Struthiopteris_spicant_leaf_1.jpg | Struthiopteris spicant | leaf | 82.5 | OK Struthiopteris spicant 1.00 | OK Struthiopteris spicant 1.00 |
| Struthiopteris_spicant_leaf_2.jpg | Struthiopteris spicant | leaf | 93.9 | OK Struthiopteris spicant 0.98 | OK Struthiopteris spicant 0.99 |
| Tanacetum_corymbosum_leaf_1.jpg | Tanacetum corymbosum | leaf | 1.0 | X Coris monspeliensis 0.62 | X Anthriscus sylvestris 0.27 |
| Tanacetum_corymbosum_leaf_2.jpg | Tanacetum corymbosum | leaf | 94.3 | X Argentina anserina 0.89 | X Argentina anserina 0.46 |
| Teucrium_scorodonia_leaf_1.jpg | Teucrium scorodonia | leaf | 1.4 | X Bellis perennis 0.76 | OK Teucrium scorodonia 1.00 |
| Teucrium_scorodonia_leaf_2.jpg | Teucrium scorodonia | leaf | 23.0 | OK Teucrium scorodonia 0.84 | OK Teucrium scorodonia 0.85 |
| Teucrium_scorodonia_bark_1.jpg | Teucrium scorodonia | bark | 97.6 | OK Teucrium scorodonia 0.87 | OK Teucrium scorodonia 0.84 |
| Teucrium_scorodonia_bark_2.jpg | Teucrium scorodonia | bark | 44.6 | X Chelidonium majus 0.28 | X Melittis melissophyllum 0.40 |
| Thymus_praecox_leaf_1.jpg | Thymus praecox | leaf | 0.0 | - | X Cistus salviifolius 0.66 |
| Thymus_praecox_leaf_2.jpg | Thymus praecox | leaf | 0.0 | - | OK Thymus praecox 0.98 |
| Thymus_vulgaris_leaf_1.jpg | Thymus vulgaris | leaf | 0.2 | X Digitalis purpurea 0.67 | OK Thymus vulgaris 0.69 |
| Thymus_vulgaris_leaf_2.jpg | Thymus vulgaris | leaf | 0.0 | - | OK Thymus vulgaris 1.00 |
| Thymus_vulgaris_bark_1.jpg | Thymus vulgaris | bark | 8.0 | X Coris monspeliensis 0.54 | X Carex flacca 0.83 |
| Trifolium_pratense_leaf_1.jpg | Trifolium pratense | leaf | 6.6 | X Bromus hordeaceus 0.28 | OK Trifolium pratense 1.00 |
| Trifolium_pratense_leaf_2.jpg | Trifolium pratense | leaf | 48.9 | X Cardamine pentaphyllos 0.65 | X Trifolium repens 0.59 |
| Trifolium_repens_leaf_1.jpg | Trifolium repens | leaf | 97.9 | X Trifolium pratense 0.62 | X Trifolium pratense 0.65 |
| Trifolium_repens_leaf_2.jpg | Trifolium repens | leaf | 5.3 | X Neottia ovata 0.98 | OK Trifolium repens 0.97 |
| Trocdaris_verticillatum_leaf_1.jpg | Trocdaris verticillatum | leaf | 0.0 | - | OK Trocdaris verticillatum 0.92 |
| Trocdaris_verticillatum_leaf_2.jpg | Trocdaris verticillatum | leaf | 90.9 | OK Trocdaris verticillatum 0.67 | OK Trocdaris verticillatum 0.80 |
| Trocdaris_verticillatum_bark_1.jpg | Trocdaris verticillatum | bark | 8.6 | X Arabidopsis thaliana 0.29 | X Impatiens balfourii 0.58 |
| Trollius_europaeus_leaf_1.jpg | Trollius europaeus | leaf | 97.5 | OK Trollius europaeus 0.80 | OK Trollius europaeus 0.78 |
| Trollius_europaeus_leaf_2.jpg | Trollius europaeus | leaf | 18.3 | OK Trollius europaeus 0.82 | X Aconitum lycoctonum 0.56 |
| Ulex_europaeus_leaf_1.jpg | Ulex europaeus | leaf | 11.2 | OK Ulex europaeus 0.45 | OK Ulex europaeus 0.94 |
| Ulex_europaeus_leaf_2.jpg | Ulex europaeus | leaf | 0.0 | - | OK Ulex europaeus 1.00 |
| Ulex_europaeus_bark_1.jpg | Ulex europaeus | bark | 0.0 | - | X Juniperus communis 0.92 |
| Ulex_europaeus_bark_2.jpg | Ulex europaeus | bark | 0.0 | - | OK Ulex europaeus 0.72 |
| Ulex_parviflorus_leaf_1.jpg | Ulex parviflorus | leaf | 0.0 | - | X Ulex europaeus 0.99 |
| Ulex_parviflorus_leaf_2.jpg | Ulex parviflorus | leaf | 5.7 | X Phalaris arundinacea 0.35 | X Agrostis canina 0.86 |
| Ulex_parviflorus_bark_1.jpg | Ulex parviflorus | bark | 0.0 | - | X Brachypodium retusum 0.24 |
| Ulex_parviflorus_bark_2.jpg | Ulex parviflorus | bark | 0.0 | - | X Crithmum maritimum 0.55 |
| Urtica_dioica_leaf_1.jpg | Urtica dioica | leaf | 1.0 | X Pteridium aquilinum 0.48 | OK Urtica dioica 1.00 |
| Urtica_dioica_leaf_2.jpg | Urtica dioica | leaf | 97.4 | OK Urtica dioica 1.00 | OK Urtica dioica 1.00 |
| Urtica_dioica_bark_1.jpg | Urtica dioica | bark | 21.0 | X Corylus avellana 0.30 | X Melissa officinalis 0.51 |
| Urtica_dioica_bark_2.jpg | Urtica dioica | bark | 34.6 | OK Urtica dioica 0.34 | OK Urtica dioica 1.00 |
| Viburnum_lantana_bark_1.jpg | Viburnum lantana | bark | 0.0 | - | OK Viburnum lantana 0.52 |
| Viburnum_lantana_bark_2.jpg | Viburnum lantana | bark | 0.3 | X Arabidopsis thaliana 0.33 | OK Viburnum lantana 0.64 |
| Viburnum_lantana_leaf_1.jpg | Viburnum lantana | leaf | 2.0 | X Bellis perennis 0.41 | OK Viburnum lantana 0.88 |
| Viburnum_lantana_leaf_2.jpg | Viburnum lantana | leaf | 0.1 | X Silybum marianum 0.42 | X Ilex aquifolium 0.63 |
| Vicia_cracca_leaf_1.jpg | Vicia cracca | leaf | 4.9 | X Gymnadenia conopsea 0.19 | OK Vicia cracca 0.98 |
| Vicia_cracca_leaf_2.jpg | Vicia cracca | leaf | 7.9 | X Holcus lanatus 0.21 | X Lathyrus pratensis 0.96 |
| Vicia_cracca_bark_1.jpg | Vicia cracca | bark | 6.7 | X Holcus lanatus 0.33 | OK Vicia cracca 0.74 |
| Vicia_cracca_bark_2.jpg | Vicia cracca | bark | 0.0 | - | OK Vicia cracca 1.00 |
| Vicia_sepium_leaf_1.jpg | Vicia sepium | leaf | 2.1 | X Viola biflora 0.33 | OK Vicia sepium 1.00 |
| Vicia_sepium_leaf_2.jpg | Vicia sepium | leaf | 1.0 | X Trifolium repens 0.19 | OK Vicia sepium 0.99 |
| Vicia_sepium_bark_1.jpg | Vicia sepium | bark | 98.1 | X Lotus pedunculatus 0.18 | X Bituminaria bituminosa 0.15 |
| Vicia_sepium_bark_2.jpg | Vicia sepium | bark | 21.0 | X Ophioglossum vulgatum 0.40 | OK Vicia sepium 0.45 |
| Vincetoxicum_hirundinaria_leaf_1.jpg | Vincetoxicum hirundinaria | leaf | 11.1 | OK Vincetoxicum hirundinaria 0.99 | OK Vincetoxicum hirundinaria 1.00 |
| Vincetoxicum_hirundinaria_leaf_2.jpg | Vincetoxicum hirundinaria | leaf | 83.2 | OK Vincetoxicum hirundinaria 0.99 | OK Vincetoxicum hirundinaria 0.99 |
| Vincetoxicum_hirundinaria_bark_1.jpg | Vincetoxicum hirundinaria | bark | 43.1 | X Hypericum perforatum 0.26 | OK Vincetoxicum hirundinaria 0.98 |
| Vincetoxicum_hirundinaria_bark_2.jpg | Vincetoxicum hirundinaria | bark | 23.2 | X Prunus laurocerasus 0.25 | OK Vincetoxicum hirundinaria 0.50 |
| Viola_biflora_leaf_1.jpg | Viola biflora | leaf | 91.2 | OK Viola biflora 1.00 | OK Viola biflora 1.00 |
| Viola_biflora_leaf_2.jpg | Viola biflora | leaf | 72.0 | OK Viola biflora 0.61 | OK Viola biflora 0.68 |
| Viola_palustris_leaf_1.jpg | Viola palustris | leaf | 6.8 | X Ophioglossum vulgatum 0.68 | X Viola biflora 0.91 |
| Viola_palustris_leaf_2.jpg | Viola palustris | leaf | 92.9 | OK Viola palustris 0.99 | OK Viola palustris 0.99 |

## Setting: catalog+truth
True species on the candidate list for 574/574 (100%) of the photos.

| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |
|---|---|---|---|---|---|---|
| crop | 169/574 (29%) | 225/574 (39%) | 179/574 (31%) | 0.892 / 0.509 | 16 | 160/276 (58%) |
| full | 370/574 (64%) | 470/574 (82%) | 398/574 (69%) | 0.904 / 0.586 | 26 | 360/481 (75%) |
| hybrid>=2 | 305/574 (53%) | 400/574 (70%) | 329/574 (57%) | 0.895 / 0.559 | 28 | 295/442 (67%) |
| hybrid>=5 | 333/574 (58%) | 426/574 (74%) | 357/574 (62%) | 0.901 / 0.572 | 27 | 324/463 (70%) |
| hybrid>=10 | 346/574 (60%) | 444/574 (77%) | 372/574 (65%) | 0.903 / 0.588 | 28 | 337/477 (71%) |
| hybrid>=20 | 358/574 (62%) | 452/574 (79%) | 384/574 (67%) | 0.91 / 0.587 | 29 | 349/478 (73%) |
| hybrid>=40 | 362/574 (63%) | 463/574 (81%) | 389/574 (68%) | 0.908 / 0.586 | 29 | 354/479 (74%) |

Calibration (detector crop): of the answers in each confidence range, how many were right

| confidence | answers | correct |
|---|---|---|
| 0.00-0.50 | 138 | 9 |
| 0.50-0.80 | 110 | 27 |
| 0.80-0.95 | 52 | 30 |
| 0.95-1.00 | 114 | 103 |

Could BioCLIP have seen these photos? Split by iNaturalist upload date (cutoff 2024-01-01: its training data predates Nov 2023):

| subset | photos | full top-1 | full top-3 | crop top-1 | crop top-3 |
|---|---|---|---|---|---|
| uploaded on/after 2024-01-01 (cannot be in training data) | 574 | 370/574 (64%) | 470/574 (82%) | 169/574 (29%) | 225/574 (39%) |

Most frequent confusions (truth → predicted, count), detector crop / full photo:
- crop: Alnus alnobetula → Corylus avellana ×2, Dactylorhiza maculata → Carex echinata ×2, Ligustrum vulgare → Acacia dealbata ×2, Melittis melissophyllum → Melissa officinalis ×2, Orchis purpurea → Himantoglossum robertianum ×2, Ostrya carpinifolia → Asplenium scolopendrium ×2, Pistacia lentiscus → Acer pseudoplatanus ×2, Vicia cracca → Holcus lanatus ×2
- full: Arundo donax → Phragmites australis ×3, Abies alba → Acer pseudoplatanus ×2, Brachypodium pinnatum → Phalaris arundinacea ×2, Coronilla juncea → Crithmum maritimum ×2, Fraxinus angustifolia → Fraxinus excelsior ×2, Fraxinus ornus → Fraxinus angustifolia ×2, Geranium sylvaticum → Urtica dioica ×2, Hyacinthoides non-scripta → Plantago lanceolata ×2

| photo | truth | organ | box % | crop: top-1 | full: top-1 |
|---|---|---|---|---|---|
| Abies_alba_leaf_1.jpg | Abies alba | leaf | 0.0 | - | OK Abies alba 1.00 |
| Abies_alba_leaf_2.jpg | Abies alba | leaf | 0.0 | - | OK Abies alba 1.00 |
| Abies_alba_bark_1.jpg | Abies alba | bark | 0.8 | X Bellis perennis 0.60 | X Acer pseudoplatanus 0.22 |
| Abies_alba_bark_2.jpg | Abies alba | bark | 0.0 | - | X Acer pseudoplatanus 0.88 |
| Acacia_dealbata_leaf_1.jpg | Acacia dealbata | leaf | 97.7 | OK Acacia dealbata 1.00 | OK Acacia dealbata 1.00 |
| Acacia_dealbata_leaf_2.jpg | Acacia dealbata | leaf | 0.2 | OK Acacia dealbata 0.13 | OK Acacia dealbata 1.00 |
| Acacia_dealbata_bark_1.jpg | Acacia dealbata | bark | 18.5 | X Cytisus scoparius 0.59 | OK Acacia dealbata 1.00 |
| Acacia_dealbata_bark_2.jpg | Acacia dealbata | bark | 0.0 | - | OK Acacia dealbata 0.85 |
| Acer_pseudoplatanus_bark_1.jpg | Acer pseudoplatanus | bark | 0.0 | - | OK Acer pseudoplatanus 0.54 |
| Acer_pseudoplatanus_bark_2.jpg | Acer pseudoplatanus | bark | 0.0 | - | OK Acer pseudoplatanus 0.99 |
| Acer_pseudoplatanus_leaf_1.jpg | Acer pseudoplatanus | leaf | 37.8 | OK Acer pseudoplatanus 0.96 | OK Acer pseudoplatanus 1.00 |
| Acer_pseudoplatanus_leaf_2.jpg | Acer pseudoplatanus | leaf | 81.8 | OK Acer pseudoplatanus 1.00 | OK Acer pseudoplatanus 1.00 |
| Achillea_millefolium_leaf_1.jpg | Achillea millefolium | leaf | 0.9 | X Teucrium scorodonia 0.25 | X Agrimonia eupatoria 0.55 |
| Achillea_millefolium_leaf_2.jpg | Achillea millefolium | leaf | 0.0 | - | X Meum athamanticum 0.93 |
| Adenostyles_alpina_leaf_1.jpg | Adenostyles alpina | leaf | 0.6 | X Asplenium scolopendrium 0.80 | X Alliaria petiolata 0.46 |
| Adenostyles_alpina_leaf_2.jpg | Adenostyles alpina | leaf | 72.0 | X Petasites hybridus 1.00 | X Petasites hybridus 0.92 |
| Adiantum_capillus-veneris_leaf_1.jpg | Adiantum capillus-veneris | leaf | 98.0 | OK Adiantum capillus-veneris 1.00 | OK Adiantum capillus-veneris 1.00 |
| Adiantum_capillus-veneris_leaf_2.jpg | Adiantum capillus-veneris | leaf | 0.7 | X Asplenium scolopendrium 0.67 | OK Adiantum capillus-veneris 1.00 |
| Adiantum_capillus-veneris_bark_1.jpg | Adiantum capillus-veneris | bark | 0.0 | - | OK Adiantum capillus-veneris 0.85 |
| Agrimonia_eupatoria_leaf_1.jpg | Agrimonia eupatoria | leaf | 86.0 | OK Agrimonia eupatoria 0.63 | OK Agrimonia eupatoria 0.91 |
| Agrimonia_eupatoria_leaf_2.jpg | Agrimonia eupatoria | leaf | 8.6 | X Urtica dioica 0.25 | X Argentina anserina 0.94 |
| Agrimonia_eupatoria_bark_1.jpg | Agrimonia eupatoria | bark | 3.5 | X Medicago lupulina 0.58 | OK Agrimonia eupatoria 1.00 |
| Agrostis_stolonifera_leaf_1.jpg | Agrostis stolonifera | leaf | 0.0 | - | X Agrostis canina 0.46 |
| Agrostis_stolonifera_leaf_2.jpg | Agrostis stolonifera | leaf | 77.2 | X Arrhenatherum elatius 0.38 | X Phragmites australis 0.32 |
| Ajuga_reptans_leaf_1.jpg | Ajuga reptans | leaf | 38.4 | OK Ajuga reptans 0.79 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_leaf_2.jpg | Ajuga reptans | leaf | 97.5 | OK Ajuga reptans 1.00 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_bark_1.jpg | Ajuga reptans | bark | 12.5 | OK Ajuga reptans 0.93 | OK Ajuga reptans 1.00 |
| Ajuga_reptans_bark_2.jpg | Ajuga reptans | bark | 23.1 | X Bellis perennis 0.47 | OK Ajuga reptans 0.99 |
| Alliaria_petiolata_leaf_1.jpg | Alliaria petiolata | leaf | 19.7 | OK Alliaria petiolata 0.58 | OK Alliaria petiolata 0.98 |
| Alliaria_petiolata_leaf_2.jpg | Alliaria petiolata | leaf | 24.4 | OK Alliaria petiolata 0.94 | OK Alliaria petiolata 0.99 |
| Alliaria_petiolata_bark_1.jpg | Alliaria petiolata | bark | 0.0 | - | OK Alliaria petiolata 1.00 |
| Allium_victorialis_leaf_1.jpg | Allium victorialis | leaf | 22.2 | OK Allium victorialis 0.98 | OK Allium victorialis 1.00 |
| Allium_victorialis_leaf_2.jpg | Allium victorialis | leaf | 9.8 | OK Allium victorialis 0.76 | OK Allium victorialis 1.00 |
| Alnus_alnobetula_leaf_1.jpg | Alnus alnobetula | leaf | 22.2 | X Corylus avellana 0.72 | X Corylus avellana 0.41 |
| Alnus_alnobetula_leaf_2.jpg | Alnus alnobetula | leaf | 56.0 | X Corylus avellana 0.48 | OK Alnus alnobetula 0.38 |
| Alnus_alnobetula_bark_1.jpg | Alnus alnobetula | bark | 0.9 | X Trifolium repens 0.94 | X Quercus robur 0.65 |
| Alnus_alnobetula_bark_2.jpg | Alnus alnobetula | bark | 13.7 | X Betula pendula 0.58 | OK Alnus alnobetula 1.00 |
| Alopecurus_pratensis_leaf_1.jpg | Alopecurus pratensis | leaf | 0.0 | - | X Holcus lanatus 0.25 |
| Alopecurus_pratensis_leaf_2.jpg | Alopecurus pratensis | leaf | 0.0 | - | X Brachypodium pinnatum 0.25 |
| Anacamptis_pyramidalis_leaf_1.jpg | Anacamptis pyramidalis | leaf | 64.0 | OK Anacamptis pyramidalis 0.99 | OK Anacamptis pyramidalis 1.00 |
| Anacamptis_pyramidalis_leaf_2.jpg | Anacamptis pyramidalis | leaf | 97.5 | OK Anacamptis pyramidalis 0.45 | X Cephalanthera longifolia 0.45 |
| Anthoxanthum_odoratum_leaf_1.jpg | Anthoxanthum odoratum | leaf | 10.8 | X Phragmites australis 0.32 | OK Anthoxanthum odoratum 0.73 |
| Anthoxanthum_odoratum_leaf_2.jpg | Anthoxanthum odoratum | leaf | 0.3 | X Dactylorhiza maculata 0.51 | OK Anthoxanthum odoratum 0.98 |
| Anthoxanthum_odoratum_bark_1.jpg | Anthoxanthum odoratum | bark | 97.8 | X Arrhenatherum elatius 0.52 | X Arrhenatherum elatius 0.62 |
| Anthoxanthum_odoratum_bark_2.jpg | Anthoxanthum odoratum | bark | 64.4 | X Holcus lanatus 0.36 | X Holcus lanatus 0.77 |
| Anthriscus_sylvestris_leaf_1.jpg | Anthriscus sylvestris | leaf | 0.0 | - | OK Anthriscus sylvestris 0.98 |
| Anthriscus_sylvestris_leaf_2.jpg | Anthriscus sylvestris | leaf | 0.0 | - | OK Anthriscus sylvestris 1.00 |
| Anthriscus_sylvestris_bark_1.jpg | Anthriscus sylvestris | bark | 97.6 | OK Anthriscus sylvestris 0.66 | OK Anthriscus sylvestris 0.76 |
| Anthriscus_sylvestris_bark_2.jpg | Anthriscus sylvestris | bark | 1.4 | X Carex echinata 0.30 | OK Anthriscus sylvestris 1.00 |
| Anthyllis_vulneraria_leaf_1.jpg | Anthyllis vulneraria | leaf | 10.2 | X Arundo donax 0.50 | X Lotus pedunculatus 0.39 |
| Anthyllis_vulneraria_leaf_2.jpg | Anthyllis vulneraria | leaf | 97.4 | OK Anthyllis vulneraria 0.99 | OK Anthyllis vulneraria 0.99 |
| Aphyllanthes_monspeliensis_leaf_1.jpg | Aphyllanthes monspeliensis | leaf | 2.9 | OK Aphyllanthes monspeliensis 1.00 | OK Aphyllanthes monspeliensis 1.00 |
| Aphyllanthes_monspeliensis_leaf_2.jpg | Aphyllanthes monspeliensis | leaf | 0.0 | - | X Avenella flexuosa 0.70 |
| Aphyllanthes_monspeliensis_bark_1.jpg | Aphyllanthes monspeliensis | bark | 0.0 | - | OK Aphyllanthes monspeliensis 0.98 |
| Aphyllanthes_monspeliensis_bark_2.jpg | Aphyllanthes monspeliensis | bark | 0.0 | - | OK Aphyllanthes monspeliensis 1.00 |
| Aquilegia_atrata_leaf_1.jpg | Aquilegia atrata | leaf | 83.9 | OK Aquilegia atrata 1.00 | OK Aquilegia atrata 1.00 |
| Aquilegia_atrata_leaf_2.jpg | Aquilegia atrata | leaf | 64.8 | OK Aquilegia atrata 0.90 | OK Aquilegia atrata 0.74 |
| Arabidopsis_thaliana_leaf_1.jpg | Arabidopsis thaliana | leaf | 3.4 | X Medicago lupulina 0.21 | X Cerastium holosteoides 0.97 |
| Arabidopsis_thaliana_leaf_2.jpg | Arabidopsis thaliana | leaf | 80.0 | X Borago officinalis 0.71 | X Borago officinalis 0.37 |
| Arabidopsis_thaliana_bark_1.jpg | Arabidopsis thaliana | bark | 12.9 | X Hypericum perforatum 0.24 | X Impatiens balfourii 0.56 |
| Argentina_anserina_leaf_1.jpg | Argentina anserina | leaf | 37.8 | OK Argentina anserina 1.00 | OK Argentina anserina 1.00 |
| Argentina_anserina_leaf_2.jpg | Argentina anserina | leaf | 0.0 | - | X Prunus spinosa 0.75 |
| Argentina_anserina_bark_1.jpg | Argentina anserina | bark | 7.4 | X Trollius europaeus 0.29 | OK Argentina anserina 0.97 |
| Argentina_anserina_bark_2.jpg | Argentina anserina | bark | 0.0 | - | X Trifolium pratense 0.50 |
| Aristolochia_clematitis_leaf_1.jpg | Aristolochia clematitis | leaf | 97.4 | OK Aristolochia clematitis 1.00 | OK Aristolochia clematitis 1.00 |
| Aristolochia_clematitis_leaf_2.jpg | Aristolochia clematitis | leaf | 3.2 | X Fagopyrum esculentum 0.84 | OK Aristolochia clematitis 0.99 |
| Aristolochia_rotunda_leaf_1.jpg | Aristolochia rotunda | leaf | 50.8 | OK Aristolochia rotunda 0.96 | OK Aristolochia rotunda 0.55 |
| Aristolochia_rotunda_leaf_2.jpg | Aristolochia rotunda | leaf | 11.5 | X Medicago lupulina 0.78 | OK Aristolochia rotunda 0.97 |
| Aristolochia_rotunda_bark_1.jpg | Aristolochia rotunda | bark | 98.2 | OK Aristolochia rotunda 1.00 | OK Aristolochia rotunda 1.00 |
| Arrhenatherum_elatius_leaf_1.jpg | Arrhenatherum elatius | leaf | 0.0 | - | OK Arrhenatherum elatius 0.98 |
| Arrhenatherum_elatius_leaf_2.jpg | Arrhenatherum elatius | leaf | 0.0 | - | OK Arrhenatherum elatius 0.96 |
| Aruncus_dioicus_leaf_1.jpg | Aruncus dioicus | leaf | 3.3 | X Hedera helix 0.87 | OK Aruncus dioicus 0.97 |
| Aruncus_dioicus_leaf_2.jpg | Aruncus dioicus | leaf | 80.7 | X Rubus idaeus 1.00 | X Rubus fruticosus 0.80 |
| Arundo_donax_leaf_1.jpg | Arundo donax | leaf | 22.5 | OK Arundo donax 0.99 | X Phragmites australis 0.86 |
| Arundo_donax_leaf_2.jpg | Arundo donax | leaf | 0.0 | - | X Phragmites australis 0.53 |
| Arundo_donax_bark_1.jpg | Arundo donax | bark | 0.8 | X Ligustrum vulgare 0.29 | X Phragmites australis 0.65 |
| Arundo_donax_bark_2.jpg | Arundo donax | bark | 0.0 | - | X Fraxinus excelsior 0.62 |
| Asplenium_ceterach_leaf_1.jpg | Asplenium ceterach | leaf | 98.1 | OK Asplenium ceterach 1.00 | OK Asplenium ceterach 0.99 |
| Asplenium_ceterach_leaf_2.jpg | Asplenium ceterach | leaf | 1.0 | X Acacia dealbata 0.42 | OK Asplenium ceterach 1.00 |
| Asplenium_scolopendrium_leaf_1.jpg | Asplenium scolopendrium | leaf | 59.7 | OK Asplenium scolopendrium 1.00 | OK Asplenium scolopendrium 1.00 |
| Asplenium_scolopendrium_leaf_2.jpg | Asplenium scolopendrium | leaf | 96.7 | OK Asplenium scolopendrium 1.00 | OK Asplenium scolopendrium 1.00 |
| Astrantia_major_leaf_1.jpg | Astrantia major | leaf | 80.0 | X Heracleum sphondylium 0.46 | OK Astrantia major 0.76 |
| Astrantia_major_leaf_2.jpg | Astrantia major | leaf | 85.7 | OK Astrantia major 0.98 | OK Astrantia major 0.98 |
| Avenella_flexuosa_leaf_1.jpg | Avenella flexuosa | leaf | 0.0 | - | X Agrostis stolonifera 0.69 |
| Avenella_flexuosa_leaf_2.jpg | Avenella flexuosa | leaf | 0.0 | - | X Aphyllanthes monspeliensis 0.97 |
| Bellis_perennis_leaf_1.jpg | Bellis perennis | leaf | 66.5 | OK Bellis perennis 0.94 | OK Bellis perennis 0.99 |
| Bellis_perennis_leaf_2.jpg | Bellis perennis | leaf | 0.0 | - | OK Bellis perennis 1.00 |
| Bellis_perennis_bark_1.jpg | Bellis perennis | bark | 26.7 | OK Bellis perennis 0.89 | OK Bellis perennis 1.00 |
| Berberis_aetnensis_leaf_1.jpg | Berberis aetnensis | leaf | 97.3 | OK Berberis aetnensis 1.00 | OK Berberis aetnensis 1.00 |
| Berberis_aetnensis_bark_1.jpg | Berberis aetnensis | bark | 4.8 | X Holcus lanatus 0.75 | OK Berberis aetnensis 1.00 |
| Berberis_aetnensis_leaf_2.jpg | Berberis aetnensis | leaf | 0.0 | - | OK Berberis aetnensis 1.00 |
| Betula_pendula_bark_1.jpg | Betula pendula | bark | 0.0 | - | OK Betula pendula 0.84 |
| Betula_pendula_bark_2.jpg | Betula pendula | bark | 0.0 | - | OK Betula pendula 1.00 |
| Betula_pendula_leaf_1.jpg | Betula pendula | leaf | 13.3 | OK Betula pendula 1.00 | OK Betula pendula 1.00 |
| Betula_pendula_leaf_2.jpg | Betula pendula | leaf | 96.3 | OK Betula pendula 1.00 | OK Betula pendula 1.00 |
| Bituminaria_bituminosa_leaf_1.jpg | Bituminaria bituminosa | leaf | 0.7 | X Trifolium repens 0.41 | OK Bituminaria bituminosa 0.93 |
| Bituminaria_bituminosa_leaf_2.jpg | Bituminaria bituminosa | leaf | 97.9 | OK Bituminaria bituminosa 1.00 | OK Bituminaria bituminosa 1.00 |
| Bituminaria_bituminosa_bark_1.jpg | Bituminaria bituminosa | bark | 7.9 | X Ophioglossum vulgatum 0.44 | X Cytisus scoparius 0.79 |
| Blackstonia_perfoliata_leaf_1.jpg | Blackstonia perfoliata | leaf | 51.2 | X Fagus sylvatica 0.45 | X Crocus vernus 0.47 |
| Blackstonia_perfoliata_leaf_2.jpg | Blackstonia perfoliata | leaf | 67.2 | OK Blackstonia perfoliata 1.00 | OK Blackstonia perfoliata 0.99 |
| Borago_officinalis_leaf_1.jpg | Borago officinalis | leaf | 50.9 | X Digitalis purpurea 0.48 | OK Borago officinalis 0.65 |
| Borago_officinalis_leaf_2.jpg | Borago officinalis | leaf | 11.8 | OK Borago officinalis 0.77 | OK Borago officinalis 0.60 |
| Brachypodium_pinnatum_leaf_1.jpg | Brachypodium pinnatum | leaf | 0.0 | - | X Phalaris arundinacea 0.82 |
| Brachypodium_pinnatum_leaf_2.jpg | Brachypodium pinnatum | leaf | 0.0 | - | X Phalaris arundinacea 0.48 |
| Brachypodium_retusum_leaf_1.jpg | Brachypodium retusum | leaf | 0.0 | - | OK Brachypodium retusum 1.00 |
| Brachypodium_retusum_leaf_2.jpg | Brachypodium retusum | leaf | 0.0 | - | OK Brachypodium retusum 1.00 |
| Bromus_hordeaceus_leaf_1.jpg | Bromus hordeaceus | leaf | 46.1 | OK Bromus hordeaceus 0.95 | OK Bromus hordeaceus 1.00 |
| Bromus_hordeaceus_leaf_2.jpg | Bromus hordeaceus | leaf | 0.0 | - | OK Bromus hordeaceus 0.80 |
| Bupleurum_baldense_leaf_1.jpg | Bupleurum baldense | leaf | 46.6 | X Brachypodium retusum 0.87 | OK Bupleurum baldense 1.00 |
| Bupleurum_fruticosum_leaf_1.jpg | Bupleurum fruticosum | leaf | 6.2 | X Ligustrum vulgare 0.80 | X Phillyrea latifolia 0.27 |
| Bupleurum_fruticosum_leaf_2.jpg | Bupleurum fruticosum | leaf | 93.6 | OK Bupleurum fruticosum 1.00 | OK Bupleurum fruticosum 0.99 |
| Bupleurum_fruticosum_bark_1.jpg | Bupleurum fruticosum | bark | 0.0 | - | X Ilex aquifolium 0.26 |
| Bupleurum_fruticosum_bark_2.jpg | Bupleurum fruticosum | bark | 6.1 | X Bellis perennis 0.34 | X Cornus mas 0.45 |
| Buxus_sempervirens_leaf_1.jpg | Buxus sempervirens | leaf | 0.1 | X Hypochaeris robertia 0.79 | OK Buxus sempervirens 0.99 |
| Buxus_sempervirens_leaf_2.jpg | Buxus sempervirens | leaf | 23.9 | OK Buxus sempervirens 1.00 | OK Buxus sempervirens 1.00 |
| Buxus_sempervirens_bark_1.jpg | Buxus sempervirens | bark | 0.0 | - | OK Buxus sempervirens 0.39 |
| Buxus_sempervirens_bark_2.jpg | Buxus sempervirens | bark | 2.3 | X Bellis perennis 0.71 | OK Buxus sempervirens 0.97 |
| Calluna_vulgaris_leaf_1.jpg | Calluna vulgaris | leaf | 1.7 | X Neottia ovata 0.21 | OK Calluna vulgaris 0.80 |
| Calluna_vulgaris_leaf_2.jpg | Calluna vulgaris | leaf | 95.0 | OK Calluna vulgaris 0.99 | OK Calluna vulgaris 0.98 |
| Calluna_vulgaris_bark_1.jpg | Calluna vulgaris | bark | 0.0 | - | X Genista salzmannii 0.34 |
| Calluna_vulgaris_bark_2.jpg | Calluna vulgaris | bark | 0.0 | - | OK Calluna vulgaris 0.98 |
| Capsella_bursa-pastoris_leaf_1.jpg | Capsella bursa-pastoris | leaf | 96.9 | OK Capsella bursa-pastoris 0.87 | X Hypochaeris robertia 0.50 |
| Capsella_bursa-pastoris_leaf_2.jpg | Capsella bursa-pastoris | leaf | 2.6 | X Urtica dioica 0.30 | OK Capsella bursa-pastoris 0.98 |
| Capsella_bursa-pastoris_bark_1.jpg | Capsella bursa-pastoris | bark | 94.5 | X Cerastium holosteoides 0.79 | OK Capsella bursa-pastoris 0.55 |
| Cardamine_pentaphyllos_leaf_1.jpg | Cardamine pentaphyllos | leaf | 79.3 | OK Cardamine pentaphyllos 1.00 | OK Cardamine pentaphyllos 1.00 |
| Carex_flacca_leaf_1.jpg | Carex flacca | leaf | 3.7 | X Anthoxanthum odoratum 0.34 | X Festuca altissima 0.89 |
| Carex_flacca_leaf_2.jpg | Carex flacca | leaf | 1.5 | X Plantago lanceolata 0.29 | OK Carex flacca 0.93 |
| Carex_hirta_leaf_1.jpg | Carex hirta | leaf | 45.7 | X Arrhenatherum elatius 0.46 | X Dactylis glomerata 0.22 |
| Carex_hirta_leaf_2.jpg | Carex hirta | leaf | 0.4 | X Viola biflora 0.47 | OK Carex hirta 0.97 |
| Carex_hirta_bark_1.jpg | Carex hirta | bark | 0.0 | - | OK Carex hirta 0.85 |
| Carex_hirta_bark_2.jpg | Carex hirta | bark | 6.1 | X Holcus lanatus 0.22 | X Carex flacca 0.42 |
| Carex_nigra_leaf_1.jpg | Carex nigra | leaf | 0.0 | - | X Dactylis glomerata 0.83 |
| Carex_nigra_leaf_2.jpg | Carex nigra | leaf | 97.0 | X Carex flacca 0.62 | X Carex flacca 0.90 |
| Carex_panicea_leaf_1.jpg | Carex panicea | leaf | 0.0 | - | X Carex flacca 0.27 |
| Castanea_sativa_bark_1.jpg | Castanea sativa | bark | 0.0 | - | X Quercus petraea 0.58 |
| Castanea_sativa_bark_2.jpg | Castanea sativa | bark | 1.6 | X Arabidopsis thaliana 0.79 | X Cornus mas 0.74 |
| Castanea_sativa_leaf_1.jpg | Castanea sativa | leaf | 53.9 | OK Castanea sativa 0.99 | OK Castanea sativa 1.00 |
| Castanea_sativa_leaf_2.jpg | Castanea sativa | leaf | 95.0 | OK Castanea sativa 1.00 | OK Castanea sativa 1.00 |
| Castroviejoa_frigida_leaf_1.jpg | Castroviejoa frigida | leaf | 0.0 | - | X Juniperus communis 0.47 |
| Catapodium_rigidum_leaf_1.jpg | Catapodium rigidum | leaf | 0.5 | X Asplenium scolopendrium 0.44 | OK Catapodium rigidum 0.98 |
| Catapodium_rigidum_leaf_2.jpg | Catapodium rigidum | leaf | 0.0 | - | OK Catapodium rigidum 1.00 |
| Catapodium_rigidum_bark_1.jpg | Catapodium rigidum | bark | 1.2 | X Digitalis purpurea 0.32 | OK Catapodium rigidum 0.94 |
| Centaurea_calcitrapa_leaf_1.jpg | Centaurea calcitrapa | leaf | 1.0 | X Petasites hybridus 0.28 | X Echium vulgare 0.38 |
| Centaurea_calcitrapa_leaf_2.jpg | Centaurea calcitrapa | leaf | 0.0 | - | X Cirsium vulgare 1.00 |
| Cephalanthera_longifolia_leaf_1.jpg | Cephalanthera longifolia | leaf | 0.8 | X Quercus ilex 0.62 | OK Cephalanthera longifolia 1.00 |
| Cephalanthera_longifolia_leaf_2.jpg | Cephalanthera longifolia | leaf | 1.9 | X Castanea sativa 0.76 | OK Cephalanthera longifolia 1.00 |
| Cephalanthera_longifolia_bark_1.jpg | Cephalanthera longifolia | bark | 50.6 | OK Cephalanthera longifolia 0.99 | OK Cephalanthera longifolia 1.00 |
| Cerastium_soleirolii_leaf_1.jpg | Cerastium soleirolii | leaf | 6.0 | X Anthoxanthum odoratum 0.49 | X Anthyllis vulneraria 0.52 |
| Cerastium_soleirolii_bark_1.jpg | Cerastium soleirolii | bark | 3.0 | X Cistus salviifolius 0.46 | X Rabelera holostea 0.63 |
| Chelidonium_majus_leaf_1.jpg | Chelidonium majus | leaf | 32.7 | OK Chelidonium majus 0.99 | X Fraxinus excelsior 0.32 |
| Chelidonium_majus_leaf_2.jpg | Chelidonium majus | leaf | 0.0 | - | OK Chelidonium majus 1.00 |
| Chelidonium_majus_bark_1.jpg | Chelidonium majus | bark | 97.8 | OK Chelidonium majus 0.87 | OK Chelidonium majus 0.90 |
| Cirsium_oleraceum_leaf_1.jpg | Cirsium oleraceum | leaf | 76.3 | OK Cirsium oleraceum 1.00 | OK Cirsium oleraceum 1.00 |
| Cirsium_oleraceum_leaf_2.jpg | Cirsium oleraceum | leaf | 0.5 | X Asplenium ceterach 0.22 | OK Cirsium oleraceum 0.73 |
| Cirsium_oleraceum_bark_1.jpg | Cirsium oleraceum | bark | 37.9 | X Urtica dioica 0.61 | OK Cirsium oleraceum 0.60 |
| Cirsium_oleraceum_bark_2.jpg | Cirsium oleraceum | bark | 67.6 | OK Cirsium oleraceum 0.95 | OK Cirsium oleraceum 0.90 |
| Cirsium_vulgare_leaf_1.jpg | Cirsium vulgare | leaf | 75.3 | OK Cirsium vulgare 1.00 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_leaf_2.jpg | Cirsium vulgare | leaf | 0.5 | X Quercus ilex 0.29 | OK Cirsium vulgare 1.00 |
| Cirsium_vulgare_bark_1.jpg | Cirsium vulgare | bark | 97.9 | OK Cirsium vulgare 0.89 | OK Cirsium vulgare 0.93 |
| Cirsium_vulgare_bark_2.jpg | Cirsium vulgare | bark | 15.4 | OK Cirsium vulgare 0.99 | OK Cirsium vulgare 0.98 |
| Cistus_albidus_leaf_1.jpg | Cistus albidus | leaf | 0.9 | OK Cistus albidus 0.98 | OK Cistus albidus 1.00 |
| Cistus_albidus_leaf_2.jpg | Cistus albidus | leaf | 0.7 | X Bellis perennis 0.29 | OK Cistus albidus 1.00 |
| Cistus_albidus_bark_1.jpg | Cistus albidus | bark | 22.4 | X Arundo donax 0.57 | OK Cistus albidus 0.97 |
| Cistus_albidus_bark_2.jpg | Cistus albidus | bark | 1.5 | X Trifolium pratense 0.83 | X Bupleurum baldense 0.23 |
| Cistus_salviifolius_leaf_1.jpg | Cistus salviifolius | leaf | 1.2 | X Digitalis purpurea 0.81 | OK Cistus salviifolius 0.99 |
| Cistus_salviifolius_leaf_2.jpg | Cistus salviifolius | leaf | 0.0 | - | OK Cistus salviifolius 0.54 |
| Cistus_salviifolius_bark_1.jpg | Cistus salviifolius | bark | 0.0 | - | X Alnus alnobetula 0.47 |
| Coris_monspeliensis_leaf_1.jpg | Coris monspeliensis | leaf | 0.0 | - | OK Coris monspeliensis 1.00 |
| Coris_monspeliensis_leaf_2.jpg | Coris monspeliensis | leaf | 97.8 | OK Coris monspeliensis 0.98 | OK Coris monspeliensis 0.98 |
| Coris_monspeliensis_bark_1.jpg | Coris monspeliensis | bark | 98.1 | OK Coris monspeliensis 0.88 | OK Coris monspeliensis 0.88 |
| Cornus_mas_bark_1.jpg | Cornus mas | bark | 0.0 | - | OK Cornus mas 0.97 |
| Cornus_mas_bark_2.jpg | Cornus mas | bark | 0.0 | - | OK Cornus mas 0.77 |
| Cornus_mas_leaf_1.jpg | Cornus mas | leaf | 0.0 | - | OK Cornus mas 1.00 |
| Cornus_mas_leaf_2.jpg | Cornus mas | leaf | 50.4 | OK Cornus mas 1.00 | OK Cornus mas 1.00 |
| Cornus_sanguinea_bark_1.jpg | Cornus sanguinea | bark | 28.8 | X Gentiana lutea 0.15 | OK Cornus sanguinea 0.56 |
| Cornus_sanguinea_leaf_1.jpg | Cornus sanguinea | leaf | 1.1 | X Pteridium aquilinum 0.21 | OK Cornus sanguinea 1.00 |
| Cornus_sanguinea_bark_2.jpg | Cornus sanguinea | bark | 0.0 | - | OK Cornus sanguinea 1.00 |
| Cornus_sanguinea_leaf_2.jpg | Cornus sanguinea | leaf | 2.6 | OK Cornus sanguinea 0.78 | OK Cornus sanguinea 0.93 |
| Coronilla_juncea_leaf_1.jpg | Coronilla juncea | leaf | 2.7 | X Trifolium repens 0.42 | X Crithmum maritimum 0.87 |
| Coronilla_juncea_leaf_2.jpg | Coronilla juncea | leaf | 0.0 | - | X Ruta corsica 0.96 |
| Coronilla_juncea_bark_1.jpg | Coronilla juncea | bark | 55.3 | X Euphorbia spinosa 0.48 | X Crithmum maritimum 0.48 |
| Coronilla_juncea_bark_2.jpg | Coronilla juncea | bark | 0.9 | X Hypochaeris robertia 0.51 | X Impatiens balfourii 0.61 |
| Corylus_avellana_bark_1.jpg | Corylus avellana | bark | 0.0 | - | X Fraxinus excelsior 0.39 |
| Corylus_avellana_bark_2.jpg | Corylus avellana | bark | 22.0 | X Viburnum lantana 0.59 | OK Corylus avellana 0.81 |
| Corylus_avellana_leaf_1.jpg | Corylus avellana | leaf | 7.2 | X Anacamptis pyramidalis 0.46 | OK Corylus avellana 1.00 |
| Corylus_avellana_leaf_2.jpg | Corylus avellana | leaf | 29.0 | OK Corylus avellana 1.00 | OK Corylus avellana 1.00 |
| Crataegus_monogyna_bark_1.jpg | Crataegus monogyna | bark | 0.0 | - | X Sorbus aucuparia 0.56 |
| Crataegus_monogyna_bark_2.jpg | Crataegus monogyna | bark | 1.5 | X Silybum marianum 0.23 | X Anthoxanthum odoratum 0.15 |
| Crataegus_monogyna_leaf_1.jpg | Crataegus monogyna | leaf | 1.6 | X Plantago lanceolata 0.26 | OK Crataegus monogyna 0.93 |
| Crataegus_monogyna_leaf_2.jpg | Crataegus monogyna | leaf | 0.9 | X Acacia dealbata 0.66 | OK Crataegus monogyna 0.99 |
| Crithmum_maritimum_leaf_1.jpg | Crithmum maritimum | leaf | 0.0 | - | OK Crithmum maritimum 0.95 |
| Crithmum_maritimum_leaf_2.jpg | Crithmum maritimum | leaf | 97.9 | OK Crithmum maritimum 1.00 | OK Crithmum maritimum 1.00 |
| Crithmum_maritimum_bark_1.jpg | Crithmum maritimum | bark | 97.9 | OK Crithmum maritimum 1.00 | OK Crithmum maritimum 1.00 |
| Crithmum_maritimum_bark_2.jpg | Crithmum maritimum | bark | 48.3 | X Anacamptis pyramidalis 0.34 | X Scorzonera humilis 0.31 |
| Crocus_vernus_leaf_1.jpg | Crocus vernus | leaf | 56.3 | X Carex panicea 0.21 | OK Crocus vernus 0.54 |
| Crocus_vernus_leaf_2.jpg | Crocus vernus | leaf | 23.4 | X Fagus sylvatica 1.00 | OK Crocus vernus 0.87 |
| Cytisus_scoparius_bark_1.jpg | Cytisus scoparius | bark | 0.9 | X Trifolium repens 0.33 | X Picris hieracioides 0.39 |
| Cytisus_scoparius_leaf_1.jpg | Cytisus scoparius | leaf | 0.0 | - | OK Cytisus scoparius 0.96 |
| Cytisus_scoparius_leaf_2.jpg | Cytisus scoparius | leaf | 0.0 | - | OK Cytisus scoparius 1.00 |
| Cytisus_scoparius_bark_2.jpg | Cytisus scoparius | bark | 0.7 | X Bellis perennis 0.38 | X Cornus sanguinea 0.41 |
| Dactylis_glomerata_leaf_1.jpg | Dactylis glomerata | leaf | 0.7 | X Acacia dealbata 0.16 | OK Dactylis glomerata 0.64 |
| Dactylis_glomerata_leaf_2.jpg | Dactylis glomerata | leaf | 0.0 | - | OK Dactylis glomerata 0.66 |
| Dactylorhiza_maculata_leaf_1.jpg | Dactylorhiza maculata | leaf | 4.2 | X Carex echinata 0.99 | OK Dactylorhiza maculata 0.97 |
| Dactylorhiza_maculata_leaf_2.jpg | Dactylorhiza maculata | leaf | 23.6 | X Carex echinata 0.88 | X Orchis mascula 0.39 |
| Dactylorhiza_sambucina_leaf_1.jpg | Dactylorhiza sambucina | leaf | 14.2 | X Phalaris arundinacea 0.58 | X Allium victorialis 0.41 |
| Dactylorhiza_sambucina_leaf_2.jpg | Dactylorhiza sambucina | leaf | 17.0 | X Ophioglossum vulgatum 0.78 | X Gymnadenia conopsea 0.36 |
| Digitalis_purpurea_leaf_1.jpg | Digitalis purpurea | leaf | 66.5 | OK Digitalis purpurea 0.99 | OK Digitalis purpurea 0.99 |
| Digitalis_purpurea_leaf_2.jpg | Digitalis purpurea | leaf | 79.5 | OK Digitalis purpurea 1.00 | OK Digitalis purpurea 1.00 |
| Dryopteris_filix-mas_leaf_1.jpg | Dryopteris filix-mas | leaf | 4.4 | X Asplenium scolopendrium 0.73 | OK Dryopteris filix-mas 1.00 |
| Dryopteris_filix-mas_leaf_2.jpg | Dryopteris filix-mas | leaf | 43.7 | OK Dryopteris filix-mas 1.00 | OK Dryopteris filix-mas 0.99 |
| Dryopteris_filix-mas_bark_1.jpg | Dryopteris filix-mas | bark | 11.4 | X Polystichum lonchitis 0.78 | OK Dryopteris filix-mas 0.93 |
| Ecballium_elaterium_leaf_1.jpg | Ecballium elaterium | leaf | 0.6 | X Asplenium scolopendrium 0.45 | OK Ecballium elaterium 1.00 |
| Ecballium_elaterium_leaf_2.jpg | Ecballium elaterium | leaf | 67.7 | X Aristolochia clematitis 0.97 | X Aristolochia rotunda 0.61 |
| Echium_vulgare_leaf_1.jpg | Echium vulgare | leaf | 97.8 | OK Echium vulgare 0.96 | OK Echium vulgare 0.96 |
| Echium_vulgare_leaf_2.jpg | Echium vulgare | leaf | 98.1 | OK Echium vulgare 0.99 | OK Echium vulgare 0.99 |
| Echium_vulgare_bark_1.jpg | Echium vulgare | bark | 10.2 | OK Echium vulgare 0.55 | OK Echium vulgare 1.00 |
| Echium_vulgare_bark_2.jpg | Echium vulgare | bark | 97.2 | OK Echium vulgare 1.00 | OK Echium vulgare 1.00 |
| Erica_cinerea_leaf_1.jpg | Erica cinerea | leaf | 0.0 | - | OK Erica cinerea 0.73 |
| Erica_cinerea_leaf_2.jpg | Erica cinerea | leaf | 0.3 | X Vicia cracca 0.20 | X Calluna vulgaris 0.99 |
| Eryngium_campestre_leaf_1.jpg | Eryngium campestre | leaf | 29.6 | OK Eryngium campestre 1.00 | X Polygonatum verticillatum 0.44 |
| Eryngium_campestre_leaf_2.jpg | Eryngium campestre | leaf | 25.2 | X Primula veris 0.58 | X Cirsium oleraceum 0.49 |
| Eryngium_campestre_bark_1.jpg | Eryngium campestre | bark | 97.8 | X Scorzonera humilis 0.50 | X Scorzonera humilis 0.69 |
| Eryngium_campestre_bark_2.jpg | Eryngium campestre | bark | 1.3 | X Medicago lupulina 0.72 | X Heracleum sphondylium 0.50 |
| Eupatorium_cannabinum_leaf_1.jpg | Eupatorium cannabinum | leaf | 65.2 | OK Eupatorium cannabinum 0.67 | OK Eupatorium cannabinum 0.33 |
| Eupatorium_cannabinum_leaf_2.jpg | Eupatorium cannabinum | leaf | 55.0 | OK Eupatorium cannabinum 0.99 | OK Eupatorium cannabinum 0.95 |
| Eupatorium_cannabinum_bark_1.jpg | Eupatorium cannabinum | bark | 97.7 | OK Eupatorium cannabinum 0.40 | OK Eupatorium cannabinum 0.49 |
| Eupatorium_cannabinum_bark_2.jpg | Eupatorium cannabinum | bark | 47.2 | OK Eupatorium cannabinum 0.59 | X Sambucus ebulus 0.47 |
| Euphorbia_cyparissias_leaf_1.jpg | Euphorbia cyparissias | leaf | 0.2 | X Medicago lupulina 0.12 | X Plantago lanceolata 0.21 |
| Euphorbia_cyparissias_leaf_2.jpg | Euphorbia cyparissias | leaf | 5.7 | X Asplenium scolopendrium 0.39 | OK Euphorbia cyparissias 0.97 |
| Euphorbia_cyparissias_bark_1.jpg | Euphorbia cyparissias | bark | 97.4 | OK Euphorbia cyparissias 0.98 | OK Euphorbia cyparissias 0.97 |
| Euphorbia_palustris_leaf_1.jpg | Euphorbia palustris | leaf | 52.8 | OK Euphorbia palustris 1.00 | OK Euphorbia palustris 0.98 |
| Euphorbia_palustris_leaf_2.jpg | Euphorbia palustris | leaf | 94.2 | X Helleborus foetidus 0.41 | OK Euphorbia palustris 0.43 |
| Euphorbia_palustris_bark_1.jpg | Euphorbia palustris | bark | 9.6 | X Arundo donax 0.79 | OK Euphorbia palustris 0.99 |
| Euphorbia_spinosa_leaf_1.jpg | Euphorbia spinosa | leaf | 13.0 | X Carex flacca 0.53 | X Bupleurum fruticosum 1.00 |
| Euphorbia_spinosa_leaf_2.jpg | Euphorbia spinosa | leaf | 6.3 | X Holcus lanatus 0.81 | OK Euphorbia spinosa 0.98 |
| Euphorbia_spinosa_bark_1.jpg | Euphorbia spinosa | bark | 7.2 | X Ribes rubrum 0.24 | X Alliaria petiolata 0.56 |
| Euphorbia_spinosa_bark_2.jpg | Euphorbia spinosa | bark | 2.8 | X Holcus mollis 0.19 | OK Euphorbia spinosa 1.00 |
| Fagopyrum_esculentum_leaf_1.jpg | Fagopyrum esculentum | leaf | 39.9 | X Impatiens balfourii 0.75 | X Hedera helix 0.29 |
| Fagopyrum_esculentum_leaf_2.jpg | Fagopyrum esculentum | leaf | 79.6 | OK Fagopyrum esculentum 1.00 | OK Fagopyrum esculentum 1.00 |
| Fagopyrum_esculentum_bark_1.jpg | Fagopyrum esculentum | bark | 0.0 | - | OK Fagopyrum esculentum 0.74 |
| Fagus_sylvatica_bark_1.jpg | Fagus sylvatica | bark | 0.0 | - | X Ostrya carpinifolia 0.32 |
| Fagus_sylvatica_leaf_1.jpg | Fagus sylvatica | leaf | 15.3 | OK Fagus sylvatica 0.87 | OK Fagus sylvatica 0.99 |
| Fagus_sylvatica_leaf_2.jpg | Fagus sylvatica | leaf | 75.0 | OK Fagus sylvatica 0.52 | X Quercus petraea 0.45 |
| Fagus_sylvatica_bark_2.jpg | Fagus sylvatica | bark | 0.0 | - | OK Fagus sylvatica 0.63 |
| Festuca_rubra_leaf_1.jpg | Festuca rubra | leaf | 0.0 | - | X Anthoxanthum odoratum 0.26 |
| Fraxinus_angustifolia_bark_1.jpg | Fraxinus angustifolia | bark | 0.0 | - | X Ligustrum vulgare 0.22 |
| Fraxinus_angustifolia_bark_2.jpg | Fraxinus angustifolia | bark | 0.0 | - | X Cornus mas 0.77 |
| Fraxinus_angustifolia_leaf_1.jpg | Fraxinus angustifolia | leaf | 66.4 | X Fraxinus excelsior 0.92 | X Fraxinus excelsior 0.83 |
| Fraxinus_angustifolia_leaf_2.jpg | Fraxinus angustifolia | leaf | 0.0 | - | X Fraxinus excelsior 0.77 |
| Fraxinus_excelsior_bark_1.jpg | Fraxinus excelsior | bark | 0.0 | - | OK Fraxinus excelsior 0.98 |
| Fraxinus_excelsior_leaf_1.jpg | Fraxinus excelsior | leaf | 0.0 | - | OK Fraxinus excelsior 0.82 |
| Fraxinus_excelsior_bark_2.jpg | Fraxinus excelsior | bark | 0.0 | - | X Acacia dealbata 0.97 |
| Fraxinus_excelsior_leaf_2.jpg | Fraxinus excelsior | leaf | 1.0 | X Trifolium repens 0.76 | OK Fraxinus excelsior 0.71 |
| Fraxinus_ornus_bark_1.jpg | Fraxinus ornus | bark | 0.0 | - | X Crataegus monogyna 0.62 |
| Fraxinus_ornus_bark_2.jpg | Fraxinus ornus | bark | 0.0 | - | X Ilex aquifolium 0.56 |
| Fraxinus_ornus_leaf_1.jpg | Fraxinus ornus | leaf | 64.8 | X Fraxinus excelsior 0.91 | X Fraxinus angustifolia 0.59 |
| Fraxinus_ornus_leaf_2.jpg | Fraxinus ornus | leaf | 0.0 | - | X Fraxinus angustifolia 0.73 |
| Galium_mollugo_leaf_1.jpg | Galium mollugo | leaf | 1.0 | X Urtica dioica 0.47 | OK Galium mollugo 1.00 |
| Galium_mollugo_leaf_2.jpg | Galium mollugo | leaf | 42.2 | OK Galium mollugo 0.99 | OK Galium mollugo 0.99 |
| Galium_odoratum_leaf_1.jpg | Galium odoratum | leaf | 20.9 | OK Galium odoratum 1.00 | OK Galium odoratum 1.00 |
| Galium_odoratum_leaf_2.jpg | Galium odoratum | leaf | 0.8 | X Acer pseudoplatanus 0.19 | X Bupleurum fruticosum 0.51 |
| Genista_cinerea_leaf_1.jpg | Genista cinerea | leaf | 0.0 | - | OK Genista cinerea 0.56 |
| Genista_cinerea_leaf_2.jpg | Genista cinerea | leaf | 0.0 | - | X Cytisus scoparius 1.00 |
| Gentiana_lutea_leaf_1.jpg | Gentiana lutea | leaf | 97.6 | OK Gentiana lutea 0.84 | OK Gentiana lutea 0.79 |
| Gentiana_lutea_leaf_2.jpg | Gentiana lutea | leaf | 4.3 | OK Gentiana lutea 0.48 | OK Gentiana lutea 0.99 |
| Gentiana_lutea_bark_1.jpg | Gentiana lutea | bark | 20.6 | X Medicago lupulina 0.87 | X Sambucus ebulus 0.54 |
| Gentiana_lutea_bark_2.jpg | Gentiana lutea | bark | 3.4 | X Digitalis purpurea 0.41 | X Hypericum perforatum 0.25 |
| Geranium_dissectum_leaf_1.jpg | Geranium dissectum | leaf | 97.9 | X Aconitum lycoctonum 0.62 | X Aconitum lycoctonum 0.69 |
| Geranium_dissectum_leaf_2.jpg | Geranium dissectum | leaf | 9.1 | X Bellis perennis 0.65 | OK Geranium dissectum 1.00 |
| Geranium_dissectum_bark_1.jpg | Geranium dissectum | bark | 0.0 | - | OK Geranium dissectum 0.66 |
| Geranium_dissectum_bark_2.jpg | Geranium dissectum | bark | 0.0 | - | OK Geranium dissectum 0.69 |
| Geranium_sylvaticum_leaf_1.jpg | Geranium sylvaticum | leaf | 23.5 | X Trollius europaeus 0.53 | OK Geranium sylvaticum 0.89 |
| Geranium_sylvaticum_leaf_2.jpg | Geranium sylvaticum | leaf | 78.7 | X Aconitum lycoctonum 0.58 | OK Geranium sylvaticum 0.90 |
| Geranium_sylvaticum_bark_1.jpg | Geranium sylvaticum | bark | 37.9 | X Melissa officinalis 0.39 | X Urtica dioica 0.25 |
| Geranium_sylvaticum_bark_2.jpg | Geranium sylvaticum | bark | 9.6 | X Holcus lanatus 0.56 | X Urtica dioica 0.50 |
| Globularia_bisnagarica_leaf_1.jpg | Globularia bisnagarica | leaf | 94.3 | X Anthyllis vulneraria 0.89 | X Ruta corsica 0.59 |
| Globularia_bisnagarica_leaf_2.jpg | Globularia bisnagarica | leaf | 6.5 | X Medicago lupulina 0.26 | X Bellis perennis 0.46 |
| Globularia_bisnagarica_bark_1.jpg | Globularia bisnagarica | bark | 11.0 | X Asplenium scolopendrium 0.23 | OK Globularia bisnagarica 0.97 |
| Gymnadenia_conopsea_leaf_1.jpg | Gymnadenia conopsea | leaf | 22.8 | X Globularia bisnagarica 0.85 | OK Gymnadenia conopsea 0.97 |
| Gymnadenia_conopsea_leaf_2.jpg | Gymnadenia conopsea | leaf | 33.9 | X Allium victorialis 0.92 | X Orchis purpurea 0.80 |
| Gymnadenia_conopsea_bark_1.jpg | Gymnadenia conopsea | bark | 26.2 | OK Gymnadenia conopsea 0.87 | OK Gymnadenia conopsea 0.99 |
| Gymnocarpium_robertianum_leaf_1.jpg | Gymnocarpium robertianum | leaf | 0.0 | - | OK Gymnocarpium robertianum 0.61 |
| Gymnocarpium_robertianum_leaf_2.jpg | Gymnocarpium robertianum | leaf | 10.5 | X Prenanthes purpurea 0.60 | OK Gymnocarpium robertianum 1.00 |
| Hedera_helix_leaf_1.jpg | Hedera helix | leaf | 0.2 | X Trifolium repens 0.50 | OK Hedera helix 1.00 |
| Hedera_helix_leaf_2.jpg | Hedera helix | leaf | 0.8 | X Teucrium scorodonia 0.17 | OK Hedera helix 1.00 |
| Hedera_helix_bark_1.jpg | Hedera helix | bark | 0.4 | X Bellis perennis 0.60 | X Buxus sempervirens 0.49 |
| Hedera_helix_bark_2.jpg | Hedera helix | bark | 0.0 | - | OK Hedera helix 1.00 |
| Helleborus_foetidus_leaf_1.jpg | Helleborus foetidus | leaf | 73.8 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Helleborus_foetidus_leaf_2.jpg | Helleborus foetidus | leaf | 98.0 | OK Helleborus foetidus 1.00 | OK Helleborus foetidus 1.00 |
| Helleborus_foetidus_bark_1.jpg | Helleborus foetidus | bark | 1.2 | X Medicago lupulina 0.21 | X Bupleurum fruticosum 0.76 |
| Helleborus_foetidus_bark_2.jpg | Helleborus foetidus | bark | 11.8 | X Bupleurum fruticosum 0.73 | OK Helleborus foetidus 1.00 |
| Heracleum_sphondylium_leaf_1.jpg | Heracleum sphondylium | leaf | 39.0 | OK Heracleum sphondylium 0.87 | OK Heracleum sphondylium 1.00 |
| Heracleum_sphondylium_leaf_2.jpg | Heracleum sphondylium | leaf | 0.1 | X Petasites hybridus 0.28 | OK Heracleum sphondylium 0.97 |
| Heracleum_sphondylium_bark_1.jpg | Heracleum sphondylium | bark | 41.4 | X Urtica dioica 0.82 | OK Heracleum sphondylium 0.97 |
| Heracleum_sphondylium_bark_2.jpg | Heracleum sphondylium | bark | 0.0 | - | OK Heracleum sphondylium 0.96 |
| Himantoglossum_robertianum_leaf_1.jpg | Himantoglossum robertianum | leaf | 64.5 | OK Himantoglossum robertianum 0.99 | OK Himantoglossum robertianum 0.98 |
| Himantoglossum_robertianum_leaf_2.jpg | Himantoglossum robertianum | leaf | 18.6 | X Allium victorialis 0.68 | X Allium victorialis 0.89 |
| Himantoglossum_robertianum_bark_1.jpg | Himantoglossum robertianum | bark | 44.4 | OK Himantoglossum robertianum 1.00 | OK Himantoglossum robertianum 0.99 |
| Himantoglossum_robertianum_bark_2.jpg | Himantoglossum robertianum | bark | 98.1 | OK Himantoglossum robertianum 0.77 | OK Himantoglossum robertianum 0.89 |
| Holcus_lanatus_leaf_1.jpg | Holcus lanatus | leaf | 85.4 | X Bromus hordeaceus 0.61 | X Carex flacca 0.67 |
| Holcus_lanatus_leaf_2.jpg | Holcus lanatus | leaf | 0.0 | - | X Dactylis glomerata 0.86 |
| Holcus_lanatus_bark_1.jpg | Holcus lanatus | bark | 0.0 | - | X Alopecurus pratensis 0.83 |
| Holcus_lanatus_bark_2.jpg | Holcus lanatus | bark | 8.7 | X Phragmites australis 0.33 | OK Holcus lanatus 0.85 |
| Hyacinthoides_non-scripta_leaf_1.jpg | Hyacinthoides non-scripta | leaf | 7.3 | X Quercus robur 0.31 | X Plantago lanceolata 0.55 |
| Hyacinthoides_non-scripta_leaf_2.jpg | Hyacinthoides non-scripta | leaf | 81.4 | OK Hyacinthoides non-scripta 0.88 | X Plantago lanceolata 0.45 |
| Hyacinthoides_non-scripta_bark_1.jpg | Hyacinthoides non-scripta | bark | 53.9 | OK Hyacinthoides non-scripta 0.42 | X Gymnadenia conopsea 0.38 |
| Hypericum_perforatum_bark_1.jpg | Hypericum perforatum | bark | 0.0 | - | X Phragmites australis 0.82 |
| Hypericum_perforatum_leaf_1.jpg | Hypericum perforatum | leaf | 0.0 | - | X Anthriscus sylvestris 0.28 |
| Hypericum_perforatum_leaf_2.jpg | Hypericum perforatum | leaf | 0.0 | - | X Lathyrus pratensis 0.68 |
| Hypericum_perforatum_bark_2.jpg | Hypericum perforatum | bark | 2.9 | X Ophioglossum vulgatum 0.42 | OK Hypericum perforatum 0.89 |
| Ilex_aquifolium_leaf_1.jpg | Ilex aquifolium | leaf | 71.2 | OK Ilex aquifolium 0.77 | OK Ilex aquifolium 0.58 |
| Ilex_aquifolium_leaf_2.jpg | Ilex aquifolium | leaf | 45.7 | OK Ilex aquifolium 1.00 | OK Ilex aquifolium 1.00 |
| Ilex_aquifolium_bark_1.jpg | Ilex aquifolium | bark | 1.4 | X Bellis perennis 0.57 | OK Ilex aquifolium 0.61 |
| Ilex_aquifolium_bark_2.jpg | Ilex aquifolium | bark | 0.0 | - | X Betula pendula 0.46 |
| Impatiens_balfourii_leaf_1.jpg | Impatiens balfourii | leaf | 58.6 | OK Impatiens balfourii 1.00 | OK Impatiens balfourii 1.00 |
| Impatiens_balfourii_leaf_2.jpg | Impatiens balfourii | leaf | 97.7 | OK Impatiens balfourii 0.76 | OK Impatiens balfourii 0.82 |
| Iris_lutescens_leaf_1.jpg | Iris lutescens | leaf | 0.3 | X Digitalis purpurea 0.13 | OK Iris lutescens 0.96 |
| Iris_lutescens_leaf_2.jpg | Iris lutescens | leaf | 1.8 | X Scorzonera humilis 0.40 | X Allium victorialis 0.88 |
| Juncus_acutiflorus_leaf_1.jpg | Juncus acutiflorus | leaf | 70.8 | OK Juncus acutiflorus 0.69 | OK Juncus acutiflorus 0.99 |
| Juncus_acutiflorus_leaf_2.jpg | Juncus acutiflorus | leaf | 4.2 | X Holcus lanatus 0.81 | X Medicago lupulina 0.26 |
| Juncus_acutus_leaf_1.jpg | Juncus acutus | leaf | 0.0 | - | OK Juncus acutus 0.97 |
| Juncus_acutus_leaf_2.jpg | Juncus acutus | leaf | 0.0 | - | OK Juncus acutus 1.00 |
| Juncus_acutus_bark_1.jpg | Juncus acutus | bark | 0.0 | - | X Carex flacca 0.98 |
| Juniperus_communis_leaf_1.jpg | Juniperus communis | leaf | 0.0 | - | X Juniperus oxycedrus 0.86 |
| Juniperus_communis_leaf_2.jpg | Juniperus communis | leaf | 1.5 | X Castanea sativa 0.13 | OK Juniperus communis 1.00 |
| Juniperus_communis_bark_1.jpg | Juniperus communis | bark | 0.0 | - | OK Juniperus communis 0.73 |
| Juniperus_communis_bark_2.jpg | Juniperus communis | bark | 1.1 | X Pteridium aquilinum 0.15 | OK Juniperus communis 1.00 |
| Juniperus_oxycedrus_leaf_1.jpg | Juniperus oxycedrus | leaf | 0.0 | - | OK Juniperus oxycedrus 1.00 |
| Juniperus_oxycedrus_leaf_2.jpg | Juniperus oxycedrus | leaf | 0.0 | - | X Juniperus communis 0.68 |
| Juniperus_oxycedrus_bark_1.jpg | Juniperus oxycedrus | bark | 0.0 | - | X Buxus sempervirens 0.61 |
| Juniperus_oxycedrus_bark_2.jpg | Juniperus oxycedrus | bark | 0.0 | - | OK Juniperus oxycedrus 0.53 |
| Juniperus_phoenicea_leaf_1.jpg | Juniperus phoenicea | leaf | 0.2 | X Digitalis purpurea 0.52 | OK Juniperus phoenicea 1.00 |
| Juniperus_phoenicea_leaf_2.jpg | Juniperus phoenicea | leaf | 0.0 | - | OK Juniperus phoenicea 1.00 |
| Juniperus_phoenicea_bark_1.jpg | Juniperus phoenicea | bark | 37.1 | OK Juniperus phoenicea 0.91 | X Genista salzmannii 0.70 |
| Juniperus_phoenicea_bark_2.jpg | Juniperus phoenicea | bark | 0.0 | - | OK Juniperus phoenicea 0.78 |
| Lactuca_perennis_leaf_1.jpg | Lactuca perennis | leaf | 78.8 | OK Lactuca perennis 0.98 | OK Lactuca perennis 0.97 |
| Lactuca_perennis_leaf_2.jpg | Lactuca perennis | leaf | 86.5 | OK Lactuca perennis 0.79 | OK Lactuca perennis 0.73 |
| Lactuca_perennis_bark_1.jpg | Lactuca perennis | bark | 3.1 | X Bupleurum fruticosum 0.68 | X Reichardia picroides 0.70 |
| Lathyrus_pratensis_leaf_1.jpg | Lathyrus pratensis | leaf | 0.0 | - | X Vicia sepium 0.25 |
| Lathyrus_pratensis_leaf_2.jpg | Lathyrus pratensis | leaf | 3.0 | X Carex echinata 0.24 | X Phillyrea latifolia 0.30 |
| Ligustrum_vulgare_leaf_1.jpg | Ligustrum vulgare | leaf | 0.9 | X Acacia dealbata 0.55 | X Cytisus scoparius 0.68 |
| Ligustrum_vulgare_leaf_2.jpg | Ligustrum vulgare | leaf | 4.0 | X Acacia dealbata 0.57 | OK Ligustrum vulgare 0.98 |
| Ligustrum_vulgare_bark_1.jpg | Ligustrum vulgare | bark | 0.0 | - | OK Ligustrum vulgare 0.99 |
| Ligustrum_vulgare_bark_2.jpg | Ligustrum vulgare | bark | 18.6 | X Senecio ovatus 0.86 | OK Ligustrum vulgare 0.99 |
| Lotus_corniculatus_leaf_1.jpg | Lotus corniculatus | leaf | 14.5 | X Ophioglossum vulgatum 0.99 | X Lotus maritimus 0.98 |
| Lotus_corniculatus_leaf_2.jpg | Lotus corniculatus | leaf | 95.3 | X Lotus maritimus 0.68 | X Lotus maritimus 0.54 |
| Lotus_maritimus_leaf_1.jpg | Lotus maritimus | leaf | 1.2 | X Plantago lanceolata 0.20 | X Lotus pedunculatus 0.52 |
| Lotus_maritimus_leaf_2.jpg | Lotus maritimus | leaf | 14.5 | X Lotus corniculatus 0.69 | OK Lotus maritimus 0.97 |
| Lotus_maritimus_bark_1.jpg | Lotus maritimus | bark | 97.5 | OK Lotus maritimus 0.97 | OK Lotus maritimus 0.97 |
| Lotus_maritimus_bark_2.jpg | Lotus maritimus | bark | 0.0 | - | OK Lotus maritimus 0.99 |
| Luzula_luzuloides_leaf_1.jpg | Luzula luzuloides | leaf | 97.3 | X Phalaris arundinacea 0.37 | X Scorzonera humilis 0.46 |
| Luzula_luzuloides_leaf_2.jpg | Luzula luzuloides | leaf | 0.0 | - | X Brachypodium pinnatum 0.50 |
| Medicago_lupulina_leaf_1.jpg | Medicago lupulina | leaf | 97.9 | OK Medicago lupulina 0.40 | X Trifolium repens 0.44 |
| Medicago_lupulina_leaf_2.jpg | Medicago lupulina | leaf | 97.7 | OK Medicago lupulina 0.98 | OK Medicago lupulina 0.98 |
| Medicago_lupulina_bark_1.jpg | Medicago lupulina | bark | 4.3 | X Trifolium pratense 0.38 | OK Medicago lupulina 0.97 |
| Melissa_officinalis_leaf_1.jpg | Melissa officinalis | leaf | 15.4 | X Betula pendula 0.63 | X Alliaria petiolata 0.44 |
| Melissa_officinalis_leaf_2.jpg | Melissa officinalis | leaf | 0.0 | - | OK Melissa officinalis 0.94 |
| Melissa_officinalis_bark_1.jpg | Melissa officinalis | bark | 16.8 | OK Melissa officinalis 0.54 | X Alliaria petiolata 0.82 |
| Melittis_melissophyllum_leaf_1.jpg | Melittis melissophyllum | leaf | 47.3 | X Melissa officinalis 0.64 | OK Melittis melissophyllum 0.88 |
| Melittis_melissophyllum_leaf_2.jpg | Melittis melissophyllum | leaf | 61.0 | X Melissa officinalis 0.66 | OK Melittis melissophyllum 0.66 |
| Meum_athamanticum_leaf_1.jpg | Meum athamanticum | leaf | 2.8 | X Ophioglossum vulgatum 0.19 | OK Meum athamanticum 0.99 |
| Meum_athamanticum_leaf_2.jpg | Meum athamanticum | leaf | 30.4 | OK Meum athamanticum 0.46 | OK Meum athamanticum 0.62 |
| Meum_athamanticum_bark_1.jpg | Meum athamanticum | bark | 91.3 | X Fagopyrum esculentum 0.37 | OK Meum athamanticum 0.33 |
| Meum_athamanticum_bark_2.jpg | Meum athamanticum | bark | 97.4 | OK Meum athamanticum 1.00 | OK Meum athamanticum 1.00 |
| Molinia_caerulea_leaf_1.jpg | Molinia caerulea | leaf | 0.0 | - | X Agrostis canina 0.71 |
| Molinia_caerulea_leaf_2.jpg | Molinia caerulea | leaf | 0.0 | - | X Dactylis glomerata 0.99 |
| Narcissus_dubius_leaf_1.jpg | Narcissus dubius | leaf | 50.9 | OK Narcissus dubius 1.00 | OK Narcissus dubius 1.00 |
| Narcissus_dubius_bark_1.jpg | Narcissus dubius | bark | 77.9 | OK Narcissus dubius 0.90 | OK Narcissus dubius 0.97 |
| Narcissus_dubius_leaf_2.jpg | Narcissus dubius | leaf | 0.0 | - | X Carex flacca 0.64 |
| Narcissus_dubius_bark_2.jpg | Narcissus dubius | bark | 97.9 | OK Narcissus dubius 0.89 | OK Narcissus dubius 0.96 |
| Narthecium_reverchonii_leaf_1.jpg | Narthecium reverchonii | leaf | 0.0 | - | OK Narthecium reverchonii 1.00 |
| Neottia_ovata_leaf_1.jpg | Neottia ovata | leaf | 59.4 | OK Neottia ovata 0.91 | OK Neottia ovata 0.97 |
| Neottia_ovata_leaf_2.jpg | Neottia ovata | leaf | 13.5 | OK Neottia ovata 0.98 | OK Neottia ovata 1.00 |
| Ophioglossum_vulgatum_leaf_1.jpg | Ophioglossum vulgatum | leaf | 27.8 | OK Ophioglossum vulgatum 0.99 | OK Ophioglossum vulgatum 0.58 |
| Ophioglossum_vulgatum_leaf_2.jpg | Ophioglossum vulgatum | leaf | 23.1 | OK Ophioglossum vulgatum 1.00 | OK Ophioglossum vulgatum 1.00 |
| Orchis_anthropophora_leaf_1.jpg | Orchis anthropophora | leaf | 16.1 | X Phalaris arundinacea 0.49 | X Gymnadenia conopsea 0.82 |
| Orchis_anthropophora_leaf_2.jpg | Orchis anthropophora | leaf | 8.2 | X Carex hirta 0.92 | X Dactylorhiza sambucina 0.41 |
| Orchis_mascula_leaf_1.jpg | Orchis mascula | leaf | 6.0 | X Hedera helix 0.88 | OK Orchis mascula 0.97 |
| Orchis_mascula_leaf_2.jpg | Orchis mascula | leaf | 85.0 | OK Orchis mascula 0.85 | OK Orchis mascula 0.57 |
| Orchis_purpurea_leaf_1.jpg | Orchis purpurea | leaf | 69.4 | X Himantoglossum robertianum 0.37 | OK Orchis purpurea 0.60 |
| Orchis_purpurea_leaf_2.jpg | Orchis purpurea | leaf | 17.0 | X Himantoglossum robertianum 0.45 | X Himantoglossum robertianum 0.45 |
| Ostrya_carpinifolia_leaf_1.jpg | Ostrya carpinifolia | leaf | 1.7 | X Asplenium scolopendrium 0.99 | OK Ostrya carpinifolia 0.78 |
| Ostrya_carpinifolia_leaf_2.jpg | Ostrya carpinifolia | leaf | 2.0 | X Asplenium scolopendrium 0.99 | OK Ostrya carpinifolia 0.82 |
| Ostrya_carpinifolia_bark_1.jpg | Ostrya carpinifolia | bark | 0.0 | - | X Castanea sativa 0.47 |
| Ostrya_carpinifolia_bark_2.jpg | Ostrya carpinifolia | bark | 0.0 | - | X Sorbus aucuparia 0.35 |
| Paris_quadrifolia_leaf_1.jpg | Paris quadrifolia | leaf | 97.1 | OK Paris quadrifolia 1.00 | OK Paris quadrifolia 1.00 |
| Paris_quadrifolia_leaf_2.jpg | Paris quadrifolia | leaf | 54.9 | OK Paris quadrifolia 1.00 | OK Paris quadrifolia 1.00 |
| Petasites_hybridus_bark_1.jpg | Petasites hybridus | bark | 6.4 | X Hedera helix 0.29 | X Himantoglossum robertianum 0.54 |
| Petasites_hybridus_leaf_1.jpg | Petasites hybridus | leaf | 53.9 | X Solanum dulcamara 0.48 | OK Petasites hybridus 0.96 |
| Petasites_hybridus_leaf_2.jpg | Petasites hybridus | leaf | 34.9 | OK Petasites hybridus 0.97 | OK Petasites hybridus 0.98 |
| Petasites_hybridus_bark_2.jpg | Petasites hybridus | bark | 37.7 | X Carex echinata 0.51 | X Urtica dioica 0.69 |
| Phalaris_arundinacea_leaf_1.jpg | Phalaris arundinacea | leaf | 19.8 | X Arundo donax 0.59 | X Arundo donax 0.69 |
| Phalaris_arundinacea_leaf_2.jpg | Phalaris arundinacea | leaf | 0.0 | - | OK Phalaris arundinacea 0.50 |
| Phillyrea_latifolia_leaf_1.jpg | Phillyrea latifolia | leaf | 5.4 | X Acer pseudoplatanus 0.47 | X Quercus coccifera 0.35 |
| Phillyrea_latifolia_leaf_2.jpg | Phillyrea latifolia | leaf | 3.1 | X Prunus laurocerasus 0.60 | OK Phillyrea latifolia 0.99 |
| Phillyrea_latifolia_bark_1.jpg | Phillyrea latifolia | bark | 0.3 | X Bellis perennis 0.23 | X Ilex aquifolium 0.35 |
| Phillyrea_latifolia_bark_2.jpg | Phillyrea latifolia | bark | 0.4 | X Plantago coronopus 0.28 | X Fraxinus angustifolia 0.46 |
| Phragmites_australis_leaf_1.jpg | Phragmites australis | leaf | 0.5 | X Holcus mollis 0.97 | OK Phragmites australis 1.00 |
| Phragmites_australis_leaf_2.jpg | Phragmites australis | leaf | 0.0 | - | OK Phragmites australis 1.00 |
| Phragmites_australis_bark_1.jpg | Phragmites australis | bark | 0.0 | - | OK Phragmites australis 0.84 |
| Phragmites_australis_bark_2.jpg | Phragmites australis | bark | 0.0 | - | OK Phragmites australis 1.00 |
| Picris_hieracioides_leaf_1.jpg | Picris hieracioides | leaf | 36.6 | OK Picris hieracioides 0.91 | X Arabidopsis thaliana 0.67 |
| Picris_hieracioides_leaf_2.jpg | Picris hieracioides | leaf | 97.3 | X Lactuca perennis 0.35 | X Hypochaeris robertia 0.36 |
| Picris_hieracioides_bark_1.jpg | Picris hieracioides | bark | 18.4 | X Holcus lanatus 0.74 | X Achillea millefolium 0.51 |
| Picris_hieracioides_bark_2.jpg | Picris hieracioides | bark | 60.8 | X Saxifraga granulata 0.14 | OK Picris hieracioides 0.88 |
| Pinguicula_corsica_leaf_1.jpg | Pinguicula corsica | leaf | 92.5 | X Neottia ovata 0.50 | X Lotus pedunculatus 0.46 |
| Pinus_nigra_leaf_1.jpg | Pinus nigra | leaf | 1.2 | X Trifolium repens 0.71 | X Pinus pinaster 0.91 |
| Pinus_nigra_bark_1.jpg | Pinus nigra | bark | 0.0 | - | X Cornus mas 0.46 |
| Pinus_nigra_bark_2.jpg | Pinus nigra | bark | 0.0 | - | X Pinus sylvestris 0.47 |
| Pinus_nigra_leaf_2.jpg | Pinus nigra | leaf | 65.2 | OK Pinus nigra 0.96 | OK Pinus nigra 0.97 |
| Pinus_pinaster_bark_1.jpg | Pinus pinaster | bark | 0.0 | - | X Pinus sylvestris 0.92 |
| Pinus_pinaster_bark_2.jpg | Pinus pinaster | bark | 0.0 | - | X Castanea sativa 0.95 |
| Pinus_pinaster_leaf_1.jpg | Pinus pinaster | leaf | 0.0 | - | OK Pinus pinaster 0.90 |
| Pinus_pinaster_leaf_2.jpg | Pinus pinaster | leaf | 0.0 | - | X Pinus nigra 0.98 |
| Pinus_sylvestris_leaf_1.jpg | Pinus sylvestris | leaf | 0.0 | - | OK Pinus sylvestris 0.82 |
| Pinus_sylvestris_leaf_2.jpg | Pinus sylvestris | leaf | 0.0 | - | OK Pinus sylvestris 0.96 |
| Pinus_sylvestris_bark_1.jpg | Pinus sylvestris | bark | 0.0 | - | X Crataegus monogyna 0.60 |
| Pinus_sylvestris_bark_2.jpg | Pinus sylvestris | bark | 0.0 | - | X Juniperus phoenicea 0.56 |
| Pistacia_lentiscus_leaf_1.jpg | Pistacia lentiscus | leaf | 0.0 | - | OK Pistacia lentiscus 1.00 |
| Pistacia_lentiscus_leaf_2.jpg | Pistacia lentiscus | leaf | 0.9 | X Acer pseudoplatanus 0.24 | OK Pistacia lentiscus 1.00 |
| Pistacia_lentiscus_bark_1.jpg | Pistacia lentiscus | bark | 8.8 | X Trifolium repens 0.21 | X Cornus mas 0.54 |
| Pistacia_lentiscus_bark_2.jpg | Pistacia lentiscus | bark | 2.6 | X Acer pseudoplatanus 0.37 | OK Pistacia lentiscus 0.93 |
| Plantago_coronopus_leaf_1.jpg | Plantago coronopus | leaf | 95.7 | OK Plantago coronopus 0.99 | OK Plantago coronopus 1.00 |
| Plantago_coronopus_leaf_2.jpg | Plantago coronopus | leaf | 1.6 | X Plantago lanceolata 0.60 | OK Plantago coronopus 0.94 |
| Plantago_coronopus_bark_1.jpg | Plantago coronopus | bark | 97.9 | OK Plantago coronopus 0.99 | OK Plantago coronopus 1.00 |
| Plantago_lanceolata_leaf_1.jpg | Plantago lanceolata | leaf | 97.6 | OK Plantago lanceolata 0.81 | OK Plantago lanceolata 0.90 |
| Plantago_lanceolata_leaf_2.jpg | Plantago lanceolata | leaf | 6.6 | X Arundo donax 0.30 | X Scorzonera humilis 0.55 |
| Polygonatum_verticillatum_leaf_1.jpg | Polygonatum verticillatum | leaf | 97.2 | OK Polygonatum verticillatum 1.00 | OK Polygonatum verticillatum 1.00 |
| Polygonatum_verticillatum_leaf_2.jpg | Polygonatum verticillatum | leaf | 73.8 | OK Polygonatum verticillatum 0.99 | OK Polygonatum verticillatum 0.86 |
| Polystichum_lonchitis_leaf_1.jpg | Polystichum lonchitis | leaf | 4.9 | X Bellis perennis 0.16 | OK Polystichum lonchitis 1.00 |
| Polystichum_lonchitis_leaf_2.jpg | Polystichum lonchitis | leaf | 82.4 | OK Polystichum lonchitis 0.97 | OK Polystichum lonchitis 0.99 |
| Potentilla_erecta_leaf_1.jpg | Potentilla erecta | leaf | 0.3 | X Gentiana lutea 0.19 | OK Potentilla erecta 0.93 |
| Potentilla_erecta_leaf_2.jpg | Potentilla erecta | leaf | 97.2 | OK Potentilla erecta 1.00 | OK Potentilla erecta 1.00 |
| Potentilla_erecta_bark_1.jpg | Potentilla erecta | bark | 0.8 | X Trifolium repens 0.69 | OK Potentilla erecta 1.00 |
| Potentilla_micrantha_leaf_1.jpg | Potentilla micrantha | leaf | 2.2 | X Acacia dealbata 0.27 | OK Potentilla micrantha 0.69 |
| Potentilla_micrantha_bark_1.jpg | Potentilla micrantha | bark | 7.7 | X Corylus avellana 0.27 | OK Potentilla micrantha 0.99 |
| Potentilla_micrantha_leaf_2.jpg | Potentilla micrantha | leaf | 98.0 | OK Potentilla micrantha 1.00 | OK Potentilla micrantha 1.00 |
| Prenanthes_purpurea_leaf_1.jpg | Prenanthes purpurea | leaf | 0.0 | - | X Impatiens balfourii 0.22 |
| Prenanthes_purpurea_leaf_2.jpg | Prenanthes purpurea | leaf | 2.1 | X Medicago lupulina 0.44 | OK Prenanthes purpurea 0.99 |
| Primula_veris_leaf_1.jpg | Primula veris | leaf | 4.8 | X Senecio ovatus 0.27 | OK Primula veris 1.00 |
| Primula_veris_leaf_2.jpg | Primula veris | leaf | 72.9 | OK Primula veris 0.72 | X Silybum marianum 0.69 |
| Prunus_laurocerasus_leaf_1.jpg | Prunus laurocerasus | leaf | 34.1 | OK Prunus laurocerasus 0.99 | OK Prunus laurocerasus 1.00 |
| Prunus_laurocerasus_leaf_2.jpg | Prunus laurocerasus | leaf | 16.5 | X Acacia dealbata 0.42 | OK Prunus laurocerasus 0.96 |
| Prunus_laurocerasus_bark_1.jpg | Prunus laurocerasus | bark | 97.9 | X Quercus robur 0.36 | OK Prunus laurocerasus 0.44 |
| Prunus_laurocerasus_bark_2.jpg | Prunus laurocerasus | bark | 17.5 | X Bupleurum fruticosum 0.56 | OK Prunus laurocerasus 0.98 |
| Prunus_spinosa_bark_1.jpg | Prunus spinosa | bark | 0.0 | - | X Cornus mas 0.88 |
| Prunus_spinosa_bark_2.jpg | Prunus spinosa | bark | 0.0 | - | OK Prunus spinosa 0.58 |
| Prunus_spinosa_leaf_1.jpg | Prunus spinosa | leaf | 56.3 | OK Prunus spinosa 1.00 | OK Prunus spinosa 1.00 |
| Prunus_spinosa_leaf_2.jpg | Prunus spinosa | leaf | 97.4 | OK Prunus spinosa 0.93 | OK Prunus spinosa 0.91 |
| Pteridium_aquilinum_leaf_1.jpg | Pteridium aquilinum | leaf | 0.2 | X Vicia cracca 0.33 | OK Pteridium aquilinum 1.00 |
| Pteridium_aquilinum_leaf_2.jpg | Pteridium aquilinum | leaf | 0.0 | - | OK Pteridium aquilinum 1.00 |
| Pteridium_aquilinum_bark_1.jpg | Pteridium aquilinum | bark | 0.8 | X Ligustrum vulgare 0.26 | OK Pteridium aquilinum 0.40 |
| Quercus_coccifera_leaf_1.jpg | Quercus coccifera | leaf | 0.0 | - | OK Quercus coccifera 0.91 |
| Quercus_coccifera_leaf_2.jpg | Quercus coccifera | leaf | 0.2 | X Quercus petraea 0.37 | OK Quercus coccifera 0.71 |
| Quercus_coccifera_bark_1.jpg | Quercus coccifera | bark | 0.0 | - | X Crataegus monogyna 0.34 |
| Quercus_coccifera_bark_2.jpg | Quercus coccifera | bark | 4.3 | X Trifolium repens 0.37 | OK Quercus coccifera 0.50 |
| Quercus_ilex_leaf_1.jpg | Quercus ilex | leaf | 95.0 | OK Quercus ilex 0.58 | OK Quercus ilex 0.56 |
| Quercus_ilex_leaf_2.jpg | Quercus ilex | leaf | 12.6 | X Fraxinus ornus 0.64 | OK Quercus ilex 1.00 |
| Quercus_ilex_bark_1.jpg | Quercus ilex | bark | 4.9 | X Acacia dealbata 0.47 | OK Quercus ilex 0.95 |
| Quercus_ilex_bark_2.jpg | Quercus ilex | bark | 0.0 | - | OK Quercus ilex 0.57 |
| Quercus_petraea_bark_1.jpg | Quercus petraea | bark | 1.3 | X Pteridium aquilinum 0.16 | X Cornus mas 0.37 |
| Quercus_petraea_leaf_1.jpg | Quercus petraea | leaf | 35.7 | X Quercus robur 0.69 | X Quercus pubescens 0.91 |
| Quercus_petraea_leaf_2.jpg | Quercus petraea | leaf | 27.7 | OK Quercus petraea 0.64 | OK Quercus petraea 0.53 |
| Quercus_petraea_bark_2.jpg | Quercus petraea | bark | 0.0 | - | OK Quercus petraea 0.96 |
| Quercus_pubescens_leaf_1.jpg | Quercus pubescens | leaf | 25.9 | OK Quercus pubescens 0.79 | X Quercus petraea 0.96 |
| Quercus_pubescens_leaf_2.jpg | Quercus pubescens | leaf | 0.0 | - | X Quercus coccifera 0.70 |
| Quercus_pubescens_bark_1.jpg | Quercus pubescens | bark | 0.0 | - | X Pinus nigra 0.22 |
| Quercus_pubescens_bark_2.jpg | Quercus pubescens | bark | 0.0 | - | X Acacia dealbata 0.37 |
| Quercus_robur_bark_1.jpg | Quercus robur | bark | 0.0 | - | X Quercus ilex 0.54 |
| Quercus_robur_leaf_1.jpg | Quercus robur | leaf | 0.0 | - | X Quercus petraea 0.53 |
| Quercus_robur_leaf_2.jpg | Quercus robur | leaf | 56.0 | OK Quercus robur 0.98 | OK Quercus robur 0.94 |
| Quercus_robur_bark_2.jpg | Quercus robur | bark | 0.0 | - | X Crataegus monogyna 0.29 |
| Reichardia_picroides_leaf_1.jpg | Reichardia picroides | leaf | 12.9 | X Lactuca perennis 0.76 | OK Reichardia picroides 0.82 |
| Reichardia_picroides_leaf_2.jpg | Reichardia picroides | leaf | 97.5 | OK Reichardia picroides 0.99 | OK Reichardia picroides 1.00 |
| Ribes_rubrum_leaf_1.jpg | Ribes rubrum | leaf | 8.7 | OK Ribes rubrum 0.97 | OK Ribes rubrum 1.00 |
| Ribes_rubrum_leaf_2.jpg | Ribes rubrum | leaf | 11.7 | OK Ribes rubrum 1.00 | OK Ribes rubrum 0.99 |
| Rubus_fruticosus_leaf_1.jpg | Rubus fruticosus | leaf | 6.9 | X Hedera helix 0.39 | X Agrimonia eupatoria 0.43 |
| Rubus_fruticosus_leaf_2.jpg | Rubus fruticosus | leaf | 97.7 | X Corylus avellana 0.56 | X Corylus avellana 0.80 |
| Rubus_fruticosus_bark_1.jpg | Rubus fruticosus | bark | 1.5 | X Trifolium repens 0.15 | X Rubus idaeus 0.65 |
| Rubus_idaeus_leaf_1.jpg | Rubus idaeus | leaf | 87.7 | OK Rubus idaeus 0.99 | OK Rubus idaeus 1.00 |
| Rubus_idaeus_leaf_2.jpg | Rubus idaeus | leaf | 89.7 | OK Rubus idaeus 1.00 | OK Rubus idaeus 0.88 |
| Rubus_idaeus_bark_1.jpg | Rubus idaeus | bark | 9.2 | X Bellis perennis 0.76 | OK Rubus idaeus 0.78 |
| Ruta_corsica_leaf_1.jpg | Ruta corsica | leaf | 1.4 | X Phillyrea latifolia 0.23 | OK Ruta corsica 1.00 |
| Salix_retusa_leaf_1.jpg | Salix retusa | leaf | 0.0 | - | OK Salix retusa 0.91 |
| Salix_retusa_leaf_2.jpg | Salix retusa | leaf | 93.5 | OK Salix retusa 1.00 | OK Salix retusa 1.00 |
| Salvia_rosmarinus_leaf_1.jpg | Salvia rosmarinus | leaf | 0.0 | - | OK Salvia rosmarinus 1.00 |
| Salvia_rosmarinus_leaf_2.jpg | Salvia rosmarinus | leaf | 0.0 | - | OK Salvia rosmarinus 1.00 |
| Salvia_rosmarinus_bark_1.jpg | Salvia rosmarinus | bark | 11.6 | X Adiantum capillus-veneris 0.68 | X Cornus mas 0.38 |
| Sambucus_ebulus_leaf_1.jpg | Sambucus ebulus | leaf | 73.5 | OK Sambucus ebulus 0.94 | OK Sambucus ebulus 0.86 |
| Sambucus_ebulus_leaf_2.jpg | Sambucus ebulus | leaf | 45.8 | OK Sambucus ebulus 0.98 | OK Sambucus ebulus 0.98 |
| Saxifraga_aizoides_leaf_1.jpg | Saxifraga aizoides | leaf | 0.0 | - | OK Saxifraga aizoides 0.78 |
| Saxifraga_aizoides_leaf_2.jpg | Saxifraga aizoides | leaf | 15.5 | OK Saxifraga aizoides 0.97 | OK Saxifraga aizoides 1.00 |
| Saxifraga_callosa_leaf_1.jpg | Saxifraga callosa | leaf | 97.7 | X Saxifraga paniculata 1.00 | X Saxifraga paniculata 1.00 |
| Saxifraga_callosa_leaf_2.jpg | Saxifraga callosa | leaf | 88.4 | OK Saxifraga callosa 0.88 | OK Saxifraga callosa 0.98 |
| Saxifraga_granulata_leaf_1.jpg | Saxifraga granulata | leaf | 35.7 | X Anthoxanthum odoratum 0.44 | X Scorzonera humilis 0.70 |
| Saxifraga_granulata_leaf_2.jpg | Saxifraga granulata | leaf | 54.0 | OK Saxifraga granulata 1.00 | OK Saxifraga granulata 1.00 |
| Saxifraga_granulata_bark_1.jpg | Saxifraga granulata | bark | 4.8 | X Alopecurus pratensis 0.70 | OK Saxifraga granulata 1.00 |
| Saxifraga_paniculata_leaf_1.jpg | Saxifraga paniculata | leaf | 97.3 | OK Saxifraga paniculata 0.81 | OK Saxifraga paniculata 0.79 |
| Saxifraga_paniculata_leaf_2.jpg | Saxifraga paniculata | leaf | 2.1 | X Digitalis purpurea 0.80 | OK Saxifraga paniculata 1.00 |
| Scorzonera_humilis_leaf_1.jpg | Scorzonera humilis | leaf | 7.2 | X Carex panicea 0.65 | X Anacamptis pyramidalis 0.23 |
| Scorzonera_humilis_leaf_2.jpg | Scorzonera humilis | leaf | 4.0 | X Impatiens balfourii 0.46 | X Lactuca perennis 0.86 |
| Sedum_acre_leaf_1.jpg | Sedum acre | leaf | 97.7 | OK Sedum acre 1.00 | OK Sedum acre 1.00 |
| Sedum_acre_leaf_2.jpg | Sedum acre | leaf | 98.0 | OK Sedum acre 1.00 | OK Sedum acre 1.00 |
| Sedum_acre_bark_1.jpg | Sedum acre | bark | 0.0 | - | OK Sedum acre 0.98 |
| Senecio_ovatus_leaf_1.jpg | Senecio ovatus | leaf | 91.2 | OK Senecio ovatus 0.98 | OK Senecio ovatus 0.99 |
| Senecio_ovatus_leaf_2.jpg | Senecio ovatus | leaf | 48.0 | OK Senecio ovatus 0.66 | X Prenanthes purpurea 0.94 |
| Silaum_silaus_leaf_1.jpg | Silaum silaus | leaf | 0.0 | - | OK Silaum silaus 0.98 |
| Silaum_silaus_leaf_2.jpg | Silaum silaus | leaf | 1.0 | X Trifolium pratense 0.51 | OK Silaum silaus 0.80 |
| Silybum_marianum_leaf_1.jpg | Silybum marianum | leaf | 2.6 | X Pteridium aquilinum 0.31 | OK Silybum marianum 1.00 |
| Silybum_marianum_leaf_2.jpg | Silybum marianum | leaf | 63.7 | OK Silybum marianum 1.00 | OK Silybum marianum 1.00 |
| Silybum_marianum_bark_1.jpg | Silybum marianum | bark | 0.0 | - | OK Silybum marianum 0.85 |
| Solanum_dulcamara_leaf_1.jpg | Solanum dulcamara | leaf | 17.8 | OK Solanum dulcamara 0.69 | OK Solanum dulcamara 0.49 |
| Solanum_dulcamara_leaf_2.jpg | Solanum dulcamara | leaf | 97.4 | OK Solanum dulcamara 0.68 | OK Solanum dulcamara 0.52 |
| Solanum_dulcamara_bark_1.jpg | Solanum dulcamara | bark | 4.2 | X Ophioglossum vulgatum 0.77 | X Hyacinthoides non-scripta 0.61 |
| Sorbus_aucuparia_leaf_1.jpg | Sorbus aucuparia | leaf | 95.5 | OK Sorbus aucuparia 0.92 | OK Sorbus aucuparia 0.97 |
| Sorbus_aucuparia_leaf_2.jpg | Sorbus aucuparia | leaf | 0.0 | - | OK Sorbus aucuparia 1.00 |
| Sorbus_aucuparia_bark_1.jpg | Sorbus aucuparia | bark | 0.0 | - | OK Sorbus aucuparia 0.90 |
| Sorbus_aucuparia_bark_2.jpg | Sorbus aucuparia | bark | 0.0 | - | OK Sorbus aucuparia 0.82 |
| Stachys_corsica_bark_1.jpg | Stachys corsica | bark | 1.6 | X Neottia ovata 0.63 | OK Stachys corsica 0.80 |
| Stachys_corsica_leaf_1.jpg | Stachys corsica | leaf | 2.2 | X Himantoglossum robertianum 0.56 | X Melissa officinalis 0.75 |
| Struthiopteris_spicant_leaf_1.jpg | Struthiopteris spicant | leaf | 82.5 | OK Struthiopteris spicant 1.00 | OK Struthiopteris spicant 1.00 |
| Struthiopteris_spicant_leaf_2.jpg | Struthiopteris spicant | leaf | 93.9 | OK Struthiopteris spicant 0.98 | OK Struthiopteris spicant 0.99 |
| Tanacetum_corymbosum_leaf_1.jpg | Tanacetum corymbosum | leaf | 1.0 | X Coris monspeliensis 0.62 | X Anthriscus sylvestris 0.27 |
| Tanacetum_corymbosum_leaf_2.jpg | Tanacetum corymbosum | leaf | 94.3 | X Argentina anserina 0.89 | X Argentina anserina 0.46 |
| Teucrium_scorodonia_leaf_1.jpg | Teucrium scorodonia | leaf | 1.4 | X Bellis perennis 0.76 | OK Teucrium scorodonia 1.00 |
| Teucrium_scorodonia_leaf_2.jpg | Teucrium scorodonia | leaf | 23.0 | OK Teucrium scorodonia 0.84 | OK Teucrium scorodonia 0.85 |
| Teucrium_scorodonia_bark_1.jpg | Teucrium scorodonia | bark | 97.6 | OK Teucrium scorodonia 0.87 | OK Teucrium scorodonia 0.84 |
| Teucrium_scorodonia_bark_2.jpg | Teucrium scorodonia | bark | 44.6 | X Chelidonium majus 0.28 | X Melittis melissophyllum 0.40 |
| Thymus_praecox_leaf_1.jpg | Thymus praecox | leaf | 0.0 | - | X Cistus salviifolius 0.66 |
| Thymus_praecox_leaf_2.jpg | Thymus praecox | leaf | 0.0 | - | OK Thymus praecox 0.98 |
| Thymus_vulgaris_leaf_1.jpg | Thymus vulgaris | leaf | 0.2 | X Digitalis purpurea 0.67 | OK Thymus vulgaris 0.69 |
| Thymus_vulgaris_leaf_2.jpg | Thymus vulgaris | leaf | 0.0 | - | OK Thymus vulgaris 1.00 |
| Thymus_vulgaris_bark_1.jpg | Thymus vulgaris | bark | 8.0 | X Coris monspeliensis 0.54 | X Carex flacca 0.83 |
| Trifolium_pratense_leaf_1.jpg | Trifolium pratense | leaf | 6.6 | X Bromus hordeaceus 0.28 | OK Trifolium pratense 1.00 |
| Trifolium_pratense_leaf_2.jpg | Trifolium pratense | leaf | 48.9 | X Cardamine pentaphyllos 0.65 | X Trifolium repens 0.59 |
| Trifolium_repens_leaf_1.jpg | Trifolium repens | leaf | 97.9 | X Trifolium pratense 0.62 | X Trifolium pratense 0.65 |
| Trifolium_repens_leaf_2.jpg | Trifolium repens | leaf | 5.3 | X Neottia ovata 0.98 | OK Trifolium repens 0.97 |
| Trocdaris_verticillatum_leaf_1.jpg | Trocdaris verticillatum | leaf | 0.0 | - | OK Trocdaris verticillatum 0.92 |
| Trocdaris_verticillatum_leaf_2.jpg | Trocdaris verticillatum | leaf | 90.9 | OK Trocdaris verticillatum 0.67 | OK Trocdaris verticillatum 0.80 |
| Trocdaris_verticillatum_bark_1.jpg | Trocdaris verticillatum | bark | 8.6 | X Arabidopsis thaliana 0.29 | X Impatiens balfourii 0.58 |
| Trollius_europaeus_leaf_1.jpg | Trollius europaeus | leaf | 97.5 | OK Trollius europaeus 0.80 | OK Trollius europaeus 0.78 |
| Trollius_europaeus_leaf_2.jpg | Trollius europaeus | leaf | 18.3 | OK Trollius europaeus 0.82 | X Aconitum lycoctonum 0.56 |
| Ulex_europaeus_leaf_1.jpg | Ulex europaeus | leaf | 11.2 | OK Ulex europaeus 0.45 | OK Ulex europaeus 0.94 |
| Ulex_europaeus_leaf_2.jpg | Ulex europaeus | leaf | 0.0 | - | OK Ulex europaeus 1.00 |
| Ulex_europaeus_bark_1.jpg | Ulex europaeus | bark | 0.0 | - | X Juniperus communis 0.92 |
| Ulex_europaeus_bark_2.jpg | Ulex europaeus | bark | 0.0 | - | OK Ulex europaeus 0.72 |
| Ulex_parviflorus_leaf_1.jpg | Ulex parviflorus | leaf | 0.0 | - | X Ulex europaeus 0.99 |
| Ulex_parviflorus_leaf_2.jpg | Ulex parviflorus | leaf | 5.7 | X Phalaris arundinacea 0.35 | X Agrostis canina 0.86 |
| Ulex_parviflorus_bark_1.jpg | Ulex parviflorus | bark | 0.0 | - | X Brachypodium retusum 0.24 |
| Ulex_parviflorus_bark_2.jpg | Ulex parviflorus | bark | 0.0 | - | X Crithmum maritimum 0.55 |
| Urtica_dioica_leaf_1.jpg | Urtica dioica | leaf | 1.0 | X Pteridium aquilinum 0.48 | OK Urtica dioica 1.00 |
| Urtica_dioica_leaf_2.jpg | Urtica dioica | leaf | 97.4 | OK Urtica dioica 1.00 | OK Urtica dioica 1.00 |
| Urtica_dioica_bark_1.jpg | Urtica dioica | bark | 21.0 | X Corylus avellana 0.30 | X Melissa officinalis 0.51 |
| Urtica_dioica_bark_2.jpg | Urtica dioica | bark | 34.6 | OK Urtica dioica 0.34 | OK Urtica dioica 1.00 |
| Viburnum_lantana_bark_1.jpg | Viburnum lantana | bark | 0.0 | - | OK Viburnum lantana 0.52 |
| Viburnum_lantana_bark_2.jpg | Viburnum lantana | bark | 0.3 | X Arabidopsis thaliana 0.33 | OK Viburnum lantana 0.64 |
| Viburnum_lantana_leaf_1.jpg | Viburnum lantana | leaf | 2.0 | X Bellis perennis 0.41 | OK Viburnum lantana 0.88 |
| Viburnum_lantana_leaf_2.jpg | Viburnum lantana | leaf | 0.1 | X Silybum marianum 0.42 | X Ilex aquifolium 0.63 |
| Vicia_cracca_leaf_1.jpg | Vicia cracca | leaf | 4.9 | X Gymnadenia conopsea 0.19 | OK Vicia cracca 0.98 |
| Vicia_cracca_leaf_2.jpg | Vicia cracca | leaf | 7.9 | X Holcus lanatus 0.21 | X Lathyrus pratensis 0.96 |
| Vicia_cracca_bark_1.jpg | Vicia cracca | bark | 6.7 | X Holcus lanatus 0.33 | OK Vicia cracca 0.74 |
| Vicia_cracca_bark_2.jpg | Vicia cracca | bark | 0.0 | - | OK Vicia cracca 1.00 |
| Vicia_sepium_leaf_1.jpg | Vicia sepium | leaf | 2.1 | X Viola biflora 0.33 | OK Vicia sepium 1.00 |
| Vicia_sepium_leaf_2.jpg | Vicia sepium | leaf | 1.0 | X Trifolium repens 0.19 | OK Vicia sepium 0.99 |
| Vicia_sepium_bark_1.jpg | Vicia sepium | bark | 98.1 | X Lotus pedunculatus 0.18 | X Bituminaria bituminosa 0.15 |
| Vicia_sepium_bark_2.jpg | Vicia sepium | bark | 21.0 | X Ophioglossum vulgatum 0.40 | OK Vicia sepium 0.45 |
| Vincetoxicum_hirundinaria_leaf_1.jpg | Vincetoxicum hirundinaria | leaf | 11.1 | OK Vincetoxicum hirundinaria 0.99 | OK Vincetoxicum hirundinaria 1.00 |
| Vincetoxicum_hirundinaria_leaf_2.jpg | Vincetoxicum hirundinaria | leaf | 83.2 | OK Vincetoxicum hirundinaria 0.99 | OK Vincetoxicum hirundinaria 0.99 |
| Vincetoxicum_hirundinaria_bark_1.jpg | Vincetoxicum hirundinaria | bark | 43.1 | X Hypericum perforatum 0.26 | OK Vincetoxicum hirundinaria 0.98 |
| Vincetoxicum_hirundinaria_bark_2.jpg | Vincetoxicum hirundinaria | bark | 23.2 | X Prunus laurocerasus 0.25 | OK Vincetoxicum hirundinaria 0.50 |
| Viola_biflora_leaf_1.jpg | Viola biflora | leaf | 91.2 | OK Viola biflora 1.00 | OK Viola biflora 1.00 |
| Viola_biflora_leaf_2.jpg | Viola biflora | leaf | 72.0 | OK Viola biflora 0.61 | OK Viola biflora 0.68 |
| Viola_palustris_leaf_1.jpg | Viola palustris | leaf | 6.8 | X Ophioglossum vulgatum 0.68 | X Viola biflora 0.91 |
| Viola_palustris_leaf_2.jpg | Viola palustris | leaf | 92.9 | OK Viola palustris 0.99 | OK Viola palustris 0.99 |

No previous report to compare with.
