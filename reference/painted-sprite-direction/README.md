# Un mode sprite à matière peinte

Retouche du 13 septembre 2026 : [coffrage fermé de la colonne d’ascenseur dans le
dôme](sealed-shaft-review/README.md), avec capot peint en volume. Cette traversée
du pont ne possède pas de palier ; elle est distincte de l’ascenseur accessible.

Navigation du 13 septembre 2026 : [ZQSD et correction du chargement à chaque
bascule vectoriel/sprite](navigation-backend-review/README.md). Les textures restent
en cache ; les sols et murs ne sont plus reconstruits au simple changement de mode.

## État actuel — draps calmes, échelle dans l'ombre et espace peint, 13 septembre 2026

La [retouche V3](interior-details-review-v3/README.md) simplifie les plis des draps,
fait disparaître l'échelle avec la profondeur et intègre un espace peint sombre
dans le client ordinaire. Dix-sept captures natives et 160 tests ciblés passent ;
le dôme, son eau et les anciens sols restent identiques. Les retours artistiques
de Ludovic sur cette nouvelle passe restent à recueillir.

## Historique — reprise postes, échelle, lits et flaques, 13 septembre 2026

La [retouche V2](interior-details-review-v2/README.md) répond aux retours sur les postes
spécialisés et l'échelle encore vectoriels, les lits trop peu peints et les flaques
grises. Elle poursuit l'intégration dans le client ordinaire ; le lac approuvé et
les anciennes dalles restent conservés. Ce nouveau lot attend le retour artistique
de Ludovic.

## Première passe intérieure

Les retouches continuent maintenant dans le jeu normal : [glace, câbles, ascenseur, flaques et lits](interior-details-v1/README.md). Douze variantes de couchage et trois états d'ascenseur complètent le mobilier intégré ; glace givrée, infrastructure peinte et eau sur dalle ont leurs rendus propres. Les anciens sols et l'eau du dôme validée sont conservés. Les captures natives et sources de cette nouvelle passe sont prêtes pour les prochains retours artistiques de Ludovic.

**L'ensemble validé est désormais intégré dans le jeu normal à la demande de Ludovic**, afin de poursuivre les retouches en situation réelle : [intégration du décor et du mobilier peints](production-integration/README.md). Les 70 variantes de mobilier et les huit matières V4 sont embarquées, avec les anciennes dalles métalliques. Aucun lanceur d'étude ni dossier Art n'est nécessaire à l'exécution.

Dernier choix : Ludovic préfère explicitement **les anciennes dalles du jeu**, avant leur passage au style peint. La [reprise dalles/eau](floor-water-review/README.md) restaure ces dix textures dans l'essai V4 et corrige la progression des berges ainsi que l'animation de l'eau peinte, y compris en pause. Les six nouvelles propositions de dalle sont rejetées et conservées hors du chargement actif.

La [reprise du contraste des murs](wall-contrast-review/README.md) reste conservée : trois matières peintes distinctes, avec les lumières du client d'origine. La V3 corrigeait les creux trop éclaircis de la V2 ; ces murs sont identiques dans la V4.

Ludovic a approuvé la reprise de profondeur (« C'est mieux comme ça oui »), puis précisé que **le côté peint doit guider tous les éléments du mode sprite**. Les quatre modèles intacts deviennent les références conservées. Le travail suivant prépare leurs tailles et états, et un premier essai cohérent du décor dans le moteur.

La [passe complète](complete/README.md) documente les 70 variantes de mobilier, 15 planches natives, les captures du vrai vaisseau et les matières peintes du décor. Le métal, les terrains, l'herbe et l'eau sont traités avec des peintures propres à leur matière. Les sources, prompts et concepts restent dans `TheEnd-Art/sprite-render/painted-world-*`.

Les autres familles du jeu restent à décliner : la direction générale est retenue, sans prétendre que tous les détails sont terminés. Le lanceur `TheEnd/tools/fixtures/open-painted-world-study.ps1` reste disponible pour les comparaisons externes ; le client ordinaire charge maintenant les éléments intégrés par défaut. Aucun commit/push de l'assistant.

## Historique — premiers échantillons

Le 12 septembre 2026, Ludovic rejette la première passe de mobilier pour sa qualité artistique et précise la direction : **l'effet peinture des personnages donne de la vie aux concepts et doit guider le mode sprite dans son ensemble**. La réponse porte donc sur la peinture, les valeurs et le rapport aux volumes, au lieu d'une accumulation de petits détails mécaniques.

Retour suivant : **« Le style peint est bien meilleur »**, mais les éléments manquent de détails et de profondeur, en particulier la console jugée trop simple. La peinture est conservée ; la [reprise des volumes](depth/README.md) compare les formes peintes ci-dessous aux nouvelles propositions. Ce retour apprécie la direction de matière, sans valider les modèles comme terminés.

## Première lecture dans le moteur

Quatre modèles intacts servent d'échantillons : table courte, banc court, console Dalle de deux cases et rangement de deux cases. Les nouvelles sources dérivent des fichiers sauvegardés ; la V1 rejetée reste préservée. Ces échantillons ne constituent ni une installation définitive ni une déclinaison terminée de tous les états.

- [Table et banc : matière isolée sur la même géométrie](common-paint-comparison.png).
- [Console et rangement : avant / nouvelle peinture](utility-paint-comparison.png).
- [Console et rangement tournés vers l'ouest](utility-paint-comparison-west.png).

Les planches viennent de MonoGame avec les renderers, la projection, la lumière et le sol du jeu. Chaque paire conserve cadrage et échelle communs ; la rangée du bas montre **48 pixels par case**. Les JSON voisins donnent les manifestes chargés et les variantes réellement dessinées. La comparaison table/banc utilise une banque témoin avec la géométrie dérivée identique et l'ancienne peinture ; la comparaison console/rangement comprend aussi quelques retouches de cadre, de joint et de montant.

Lancer depuis TheEnd :

```powershell
./tools/fixtures/open-fixture-study.ps1 -ComparePaint -Page table-bench -CommonFurnitureReferenceBank C:/workspace/TheEnd-Art/exports/common-furniture-detail-v1-paint -NoBuild
./tools/fixtures/open-fixture-study.ps1 -ComparePaint -Page consoles -NoBuild
```

`2` montre table/banc ; `3` ou `5` montre console/rangement. `R` tourne, `+/-` et la molette changent le zoom. Pour isoler strictement la peinture de table/banc, ajouter `-CommonFurnitureReferenceBank C:/workspace/TheEnd-Art/exports/common-furniture-detail-v1-paint`.

## Ce qui fait le rendu peint

Le colon et le mobilier utilisent déjà le même éclairage diffus, sans reflets spéculaires. Sur les personnages, les grandes ombres, les nuances et les rehauts sont présents dans les peintures UV des vêtements et suivent leurs formes. Le contour très fin des acteurs aide aussi la silhouette ; il n'a pas été ajouté globalement au décor pendant cet essai.

Références sources : `TheEnd-Art/characters/colonist/textures/shirt-colour.png`, `trousers-colour.png`, `face-colour.png`. La veste réellement utilisée par le client, `Assets/models/colonist/textures/clothing-a02-slate-technical-jacket.png`, montre particulièrement bien les grandes plages calmes et les touches peintes. Le rendu des portraits et celui des corps 3D restent distincts ; cette étude utilise directement les peintures des modèles 3D disponibles.

Le nouvel atlas conserve quatre familles de valeurs : ardoise éclairée, bleu-gris intermédiaire, graphite aux ombres colorées, quelques rehauts d'étain chaud. Les plans reçoivent de grandes touches peintes et des zones calmes. Les joints, cavités et petits accents soutiennent la lecture. La première version était trop striée ; la seconde réduit cet effet et le banc utilise une peinture continue à travers ses lattes.

## Fil conducteur pour l'ensemble du décor

| Famille | Intention de peinture |
| --- | --- |
| Mobilier et portes | Valeurs peintes attachées aux panneaux et aux assemblages, creux colorés, quelques arêtes rehaussées ; silhouettes et accès lisibles |
| Murs et ruines | Grandes masses calmes, changements de plans marqués par la peinture, éclats localisés et cassures structurées |
| Rochers et débris | Faces et ruptures modelées par les valeurs, variations colorées adaptées à la matière, accents sur les pièces utiles à la lecture |
| Terre et herbe | Masses peintes à plusieurs tailles, transitions organiques, groupes de touches plutôt qu'un tapis uniforme de traits |
| Eau | Grandes zones de profondeur et reflets peints animés, mouvement perceptible avec des berges stables |

Ce tableau définit une direction générale à décliner. **Les murs, terrains, eau, portes, débris et personnages ne sont pas repeints ni remplacés par cette passe.** Une même texture métallique ne convient pas à tous les matériaux. Les décisions artistiques seront évaluées sur une zone cohérente du jeu et aux zooms usuels, avant d'étendre la méthode à toutes les variantes intactes, ouvertes, dépouillées et cassées.

## Fabrication, sources et vérifications

La peinture est créée avec le skill imagegen et l'outil intégré, avec la chemise du colon comme référence stylistique. Aucun filtre de grain global n'est ajouté à l'écran. Sources, deux prompts complets et contrat des régions UV : `TheEnd-Art/sprite-render/painted-materials-v1/README.md`. Image actuelle : `painted-metal-atlas-v2.png`, SHA256 `6350270192F5130366F647A3199B9CE2B278A20C1A6D30E0412B540FF7F14733`.

- `objects/common-furniture/common-furniture-detail.blend` → `exports/common-furniture-detail`.
- `objects/utility-furniture/utility-furniture-detail.blend` → `exports/utility-furniture-detail`.
- Témoin de peinture table/banc : `objects/common-furniture/common-furniture-detail-v1-paint.blend` → export homonyme.

Le pipeline commun lit les `.blend` sauvegardés ; il ne rejoue pas les scripts historiques. Les deux banques de propositions passent la validation d'export, erreur de skinning maximale **0 m**. Les images sont packées et leurs copies conservées dans Art. Chaque banque réutilise ses textures et buffers GPU ; aucune peinture n'est recalculée par image.

Un défaut de la première passe a aussi été identifié : certaines UV sortaient de l'image alors que le client utilise LinearClamp, étirant les pixels du bord. Audit des sommets texturés : 14 934 sur 43 076 hors [0,1] pour la banque commune V1, 8 286 sur 45 698 pour l'utilitaire V1 ; **zéro** sur les quatre nouveaux échantillons. L'atlas reçoit désormais des UV attribuées aux pièces, avec marges entre régions et orientation cohérente. Les îlots ne sont pas recadrés à une fraction minuscule de la peinture.

Le client et le helper de capture compilent sans erreur ni avertissement. Cette passe change le banc d'étude et des assets externes ; le rendu de production et le Core ne sont pas modifiés. La suite de 1 810 tests de la passe précédente n'est pas présentée comme nouvellement exécutée ici. Les vérifications de cette passe sont les exports et les captures natives comparatives.

La vérification dans le vrai `TheEndGame` a également réussi pour les quatre exemples intacts : [table](game/game-0-Table-Sealed.png), [banc](game/game-1-Bench-Sealed.png), [console](game/game-2-Console-Sealed.png), [rangement](game/game-3-Rack-Sealed.png). Le helper sélectionne uniquement la pause, le pont et la caméra, sans changer les objets ni leurs états. Chaque cible est bien retirée du rendu vectoriel et la révision du cache reste stable pendant les 25 images contrôlées après préparation. Il s'agit d'un contrôle fonctionnel, pas d'une mesure de performances. Résultat détaillé : [preuve native](game/native-game-validation.json) et [provenance des fichiers vérifiés](validation.json).

Les premiers modèles peints restent des propositions. Les autres formats/états et le traitement général du décor attendent le retour sur cette direction. Aucun commit/push Code, Art ou Docs de l'assistant.
