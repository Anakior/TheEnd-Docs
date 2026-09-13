# Sas A — modèle 3D et essai natif

**Historique du premier modèle natif rejeté le 12 septembre 2026.**

**La version actuelle, sa nouvelle vidéo et ses contrôles sont dans [Raccord aux murs et stabilité de l'ouverture](retouche-murs-ouverture.md).** Les données ci-dessous sont celles du modèle précédent.

Retour de Ludovic après la vidéo : « c'est moche pas du tout ressemblant avec le reste du design des murs » et « ouverture cela tremblote ». Les preuves et mesures ci-dessous décrivent la version rejetée (`ac9619…`) ; leurs contrôles de matrices et de course ne prouvaient pas l'absence de clignotement des surfaces. Le concept A reste retenu. La reprise porte sur la construction des raccords, les matières du décor et les recouvrements de faces visibles pendant le mouvement.

Après avoir retenu [A « Monobloc facetté »](direction-v2-a-monobloc.png), Ludovic demande : « Go pour le modèle 3D du coup ».

- Source éditable : [sas-door-a.blend](../../../TheEnd-Art/objects/sas-door/sas-door-a.blend).
- Construction, cotes et matières : [README Art](../../../TheEnd-Art/objects/sas-door/README.md).
- Banque externe validée : `TheEnd-Art/exports/sas-door-a/manifest.json`, variante `body/faceted`.
- **Aucune banque sas installée dans le rendu normal.** Le banc charge cette source exportée pour une seule bande réelle. Les portes ordinaires, rochers et débris intégrés restent conservés.

## Examiner le résultat

[Animation native : ouverture puis fermeture](sas-a-motion-native.mp4).

Le film vient de **120 captures du vrai moteur à 30 images/s**, sur quatre secondes. Il montre un recadrage de 400 × 400 pixels à l'origine (760,220), agrandi ×3 par voisin le plus proche en 1200 × 1200, puis encodé H.264. Aucun dessin ni matière n'est retouché dans les captures. Les vues intégrales ci-dessous restent la preuve à l'échelle du jeu.

| Bande | Fermée | Ouverte |
| --- | --- | --- |
| Verticale, passage gauche/droite | [Capture native](sas-a-closed-native.png) | [Capture native](sas-a-open-native.png) |
| Horizontale, passage haut/bas | [Capture native](sas-a-horizontal-closed-native.png) | [Capture native](sas-a-horizontal-open-native.png) |

Les JSON voisins enregistrent source, bande, identifiants, pose, matrice et bornes projetées. Réglages : monde de développement 256 × 256, graine 12345, rendu sprite, murs en volume, caméra native, 1920 × 1080, cellule au zoom maximal de 48 pixels.

La bande verticale est le sas 1 / bande A du pont 0, porte médiane (119,74), ids 32/33/34. L'autre orientation cible la première vraie bande horizontale du pont 0. Le cadrage consulte `SasMap` : `THEEND_SHOT_GATE` reste réservé à la porte ordinaire du dôme.

## Modèle et corrections après le premier essai

Deux vantaux à larges chanfreins, face centrale ardoise, pans latéraux sombres et chants acier. Les carters graphite contiennent un plancher, des guides bas, des joues, un fond et un capot ; leurs récepteurs en laiton sont encastrés. Les panneaux et les accessoires centraux restent liés aux os mobiles.

Le premier essai natif montrait des capots trop clairs et des hachures au sol à l'ouverture. La retouche assombrit les carters, calme la peinture et sépare les valeurs des facettes. Un seuil de métal existant, à Z=0,010, couvre les hachures sans créer d'obstacle haut. Les quatre captures ci-dessus et le film montrent cette version retouchée.

La course, le rig et les 41 poses restent identiques après cette retouche. La source précédente et les scripts d'initialisation sont historiques dans `TheEnd-Art/.cache/sas-door-study` ; **modifier le .blend sauvegardé**, puis exporter, sans le reconstruire depuis une recette initiale.

| Contrat | Valeur |
| --- | --- |
| Baie nominale | 3 cases suivant X local |
| Repère | X le long de la bande, Y à travers, Z vertical |
| Os | Root, LeafLeft, LeafRight ; poids rigides |
| Clips | closed (pose 0), open (0..40 à 60 images/s, non bouclé) |
| Ouverture / fermeture | 2/3 de seconde chacune, course ±1,480 |
| Nez acier à pleine ouverture | X ±1,490 ; passage 2,980 |
| Joints inclus | passage 2,976 |
| Bas / haut des vantaux | Z=0,018 / 0,588 |
| Seuil / jeu sous les vantaux | Z=0,010 / 0,008 |
| Carters | X ±3,042 ; Y ±0,658 ; détails jusqu'à Z=0,638 |
| Taille source | 3 478 sommets, 6 062 triangles |
| Export | 26 sous-maillages, 12 matériaux, 12 230 sommets séparés |

Les poches dépassent la petite niche décorative historique. L'inspection du monde de capture retrouve 40 bandes, vingt par axe : les cellules au centre de leurs poches, aux offsets ±2 et ±3, sont toutes en Terrain Mass. Le raccord a été examiné dans les deux orientations représentées ici. Ce constat ne crée pas une règle universelle de placement pour de futurs sas construits par le joueur.

## Contrôles

Source SHA-256 : `ac9619d3b8c567571bc7f498e6b259bfa6ac8170c6ef5082ccda94577edc89dc`.

- Export commun et comparaison à Blender réussis : erreur maximale 1,78814 × 10⁻⁷ m.
- [Audit indépendant des buffers](sas-a-model-audit.json) réussi : 41 poses, poids rigides, bornes de clips, course, seuil et absence de face fixe dans le volume balayé des vantaux.
- **1 739 tests Debug réussis, zéro échec/ignoré**, en 2 min 35 s : Renderer, Development, Display et Sas. Le ciblage initial de 44 tests passe aussi. La suite complète précédente de 4 564 tests concernait l'intégration des obstacles ; elle n'est pas présentée comme relancée ici.
- Compilation Client : zéro erreur/avertissement. Formatage C# et `git diff --check` conformes.
- La capture du jeu normal sans diagnostic est **identique octet par octet** à la preuve précédente `obstacles-3d-study/integration-debris.png` (SHA `548e3efdae00d5e279bbd1bf2694a3fc7971a6d1aa95d879627a8ec2709715f7`).
- Les frames 0 et 119 du film sont identiques à la capture fermée ; la frame 45 est identique à la capture ouverte.
- Les trois sources et manifestes installés de porte ordinaire, rocher et débris conservent leurs empreintes.

Le banc pose une **présentation diagnostique** d'une vraie bande de sas. Il ne simule pas le trajet d'un colon, les collisions, l'équilibrage de pression ou l'interverrouillage des deux bandes. Le modèle animé n'a pas encore reçu l'appréciation artistique de Ludovic en jeu.

## Refaire l'essai sur une autre machine

Depuis `TheEnd-Art`, exporter la source sauvegardée avec l'outil commun :

```powershell
.\tools\models\build-model.ps1 -Source objects/sas-door/sas-door-a.blend
```

Depuis `TheEnd`, compiler et capturer :

```powershell
.\scripts\run-sas-study.ps1 -Mode closed -Axis vertical
.\scripts\run-sas-study.ps1 -Mode open -Axis vertical -NoBuild
.\scripts\run-sas-study.ps1 -Mode motion -Axis vertical -NoBuild
.\scripts\run-sas-study.ps1 -Mode closed -Axis horizontal -NoBuild
.\scripts\run-sas-study.ps1 -Mode open -Axis horizontal -NoBuild
```

Le script localise Art à côté de Code. `-Bank` permet de désigner un autre manifeste ou dossier exporté ; `-OutputDirectory` choisit le dossier de preuves. La capture est cachée et se ferme par défaut ; `-KeepOpen` sert seulement lorsqu'un banc interactif est demandé. Il garde la pose diagnostique choisie et rend ensuite les commandes du jeu.

Variables : `THEEND_SAS_STUDY=closed|open|motion`, `THEEND_SAS_STUDY_BANK` absolu, `THEEND_SAS_STUDY_AXIS=vertical|horizontal|any`, `THEEND_SHOT` ; pour motion, `THEEND_SAS_MOTION_FRAMES` absolu. Le moteur de dessin est `DoorModelRenderer`, déjà partagé avec la porte ordinaire. La source de trois cases ne reçoit aucune échelle ×3. L'ancien corps, ses ferrures et ses vantaux sont masqués uniquement sur la bande sélectionnée, tout en conservant sa topologie murale.

Les sources sont dans Art, les références/proofs dans Docs, le banc dans Code. Aucun commit/push de ces trois dépôts par l'assistant.
