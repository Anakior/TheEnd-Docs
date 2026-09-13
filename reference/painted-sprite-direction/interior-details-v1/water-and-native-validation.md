# Flaques sur dalle — preuve finale r2

La flaque réelle de quatorze cellules sur le pont 1 est maintenant lisible par un reflet gris froid et un bord doux. Les joints et la texture de dalle restent visibles dessous, sans turquoise ni grande vague. La silhouette arrondie provient du contour existant, conservé dans cette correction. Les captures sont une revue technique et artistique interne, pas une approbation visuelle de Ludovic.

## Résultats natifs

| Preuve | Résultat |
| --- | --- |
| [Flaque à 48 pixels/case](game-water-final-r2/game-02-FloorPuddle.png) | Voile de reflet visible dans la pièce sombre ; sol traversant. |
| [Flaque à 96 pixels/case](game-water-inspection/game-02-FloorPuddle.png) | Inspection native rapprochée, contour fin et absence de texture de lac confirmés. |
| [Dôme à 48 pixels/case](game-water-final-r2/game-7-Dome-Environment.png) | Identique à la capture de production approuvée : **0 pixel différent sur 2 073 600**. |
| Régions eau, berge et profondeur | Respectivement 0/36 000, 0/13 500 et 0/10 500 pixels différents ; écart maximal par canal nul. |
| [Rapport 48](game-water-final-r2/native-game-validation.json) | Sept cibles réelles, toutes validées ; inclut le dôme et la comparaison RGBA. |
| [Rapport 96](game-water-inspection/native-game-validation.json) | Une cible réelle, `FloorPuddle`, validée. |

Les captures viennent du composite de `TheEndGame`, en 1920 × 1080, avec les assets installés, sans override de banque ou de matière. Le monde et l'horloge visuelle restent au tick 12000. La flaque est située au pont d'index 0, centre (73.21429, 209) ; les quatorze cellules Metal/Water sont consignées dans les rapports. Aucun état de fixture ou de monde n'a été créé pour la preuve.

Le zoom 96 est appliqué à la caméra du helper uniquement ; les PNG ne sont ni redimensionnés ni retouchés. Le jeu normal garde ses bornes de zoom. Les caches glace, infrastructure, ascenseur et mobilier restent stables pendant les 35 frames contrôlées de chaque vue. Les rapports relèvent aussi les identités de surface et de buffers d'eau au moment du rendu ; cette séquence d'images fixes n'est pas une mesure de FPS ni une vidéo du mouvement.

La comparaison du dôme utilise les pixels RGBA, sans alignement ni transformation d'image, avec [la référence de production](../production-integration/installed-game/game-7-Dome-Environment.png). L'identité de l'image entière confirme également la préservation du lac dans ce cadrage.

## Correction et périmètre

- Une composante d'eau utilise le profil flaque si toutes ses cellules reposent sur Metal ou BrokenMetal. Une composante mixte ou naturelle conserve le profil du lac. Aucun seuil de taille ne fait basculer l'apparence.
- La classification est capturée avant le travail asynchrone. Un changement réel de terrain sous l'eau visible invalide sa préparation. Les contours, distances à la berge, sommets et buffers retenus conservent leur fonctionnement ; aucune lecture de texture ni reconstruction par frame n'est ajoutée.
- Une technique `Puddle` distincte ne lit pas le PNG du lac. Le reflet oscille très faiblement avec une période de quatorze secondes ; l'horloge de présentation et son override déterministe sont réutilisés. La berge de la flaque reste immobile.
- Le réglage final r2 garantit un reflet minimum : alpha humide .24, liseré .11, reflet `.13 + .11 * reflection` modulé entre .96 et 1. La couleur de reflet est (.42, .49, .52). Le résultat est prémultiplié pour `AlphaBlend` ; au moins 41 % du sol subsiste dans le mélange. Aucun mécanisme d'émission lumineuse n'est ajouté.
- `WaterVertex`, `WaterPixel` et la technique `Water` approuvés n'ont pas été modifiés. La preuve native confirme leur résultat dans le dôme de référence.

Fichiers de production concernés : `TheEnd.Client/Composition/SpriteWaterSkin.cs`, `SpriteWaterGpu.cs`, `TheEnd.Client/Assets/shaders/sprite-water.fx` et `.mgfxo`, avec `TheEnd.Tests/Renderer/SpriteWaterPuddleTests.cs`. L'invalidation du terrain sous l'eau dans Core a été intégrée et testée dans le cycle commun. Aucun PNG de sol ni d'eau n'a été modifié par ce correctif.

Les douze cas dédiés couvrent les types de sol, la composante mixte, l'absence de seuil de taille, les lots distincts dans une même région spatiale, la conservation de géométrie, la capture de classification avant mutation du tableau et l'horloge périodique déterministe. Le cycle commun a réussi **517 tests**, zéro échec et zéro test ignoré : [journal](tests-final-r1.log), [TRX](interior-details-final-r1.trx). Après ces tests, seule la technique shader de flaque a reçu l'ajustement r2 de valeurs ; sa compilation, sa copie runtime et la validation des assets ont réussi. La DLL n'a pas changé.

## Empreintes finales

| Fichier | SHA-256 |
| --- | --- |
| Client utilisé par les deux runs | `7FA4240178BA51A63D13B446AD7FCF09B9283FC6EDC39E4744434A05C4FCA27D` |
| `sprite-water.mgfxo`, source et runtime | `566DEC43486A157BE07B8F234D3EBF91E450B706BA0F28DB421D20B92514817B` |
| `sprite-water.fx`, source et runtime | `7A74297B22EDF323A460DF2AC27432BA9FF5B974770F4C6CC7F49745DBCEB879` |

Compilation shader : `scripts/build-water-shader.ps1`. Les deux JSON natifs consignent directement l'empreinte du shader réellement chargé par leur sortie exécutable. [Validation globale des assets](asset-validation.json).

## Reproduction et incident conservé

Depuis `C:/workspace/TheEnd`, avec la DLL finale et le helper déjà compilés, utiliser un nouveau dossier vide à chaque lancement :

```powershell
.artifacts/fixture-complete/native/run.ps1 -InteriorDetails -InstalledAssets -NoBuild -DetailCellSize 48 -Output 'C:/workspace/TheEnd-Docs/reference/painted-sprite-direction/interior-details-v1/game-water-final-r2'
.artifacts/fixture-complete/native/run.ps1 -InteriorDetails -InstalledAssets -NoBuild -DetailTarget FloorPuddle -DetailCellSize 96 -Output 'C:/workspace/TheEnd-Docs/reference/painted-sprite-direction/interior-details-v1/game-water-inspection'
```

Ces commandes ont été lancées successivement, sans processus natifs concurrents. Le premier essai ciblé 48, conservé dans `game-water-final`, s'est fermé avant la première capture : processus natif terminé sans rapport, sortie standard vide, puis erreur du lanceur à la lecture du JSON absent. La cause n'est pas établie. Aucun correctif de helper ou de renderer n'a été fait après cet incident. La relance All 48 puis la cible unique 96 ont réussi, ce qui ne permet pas d'attribuer l'incident au filtre.

`game-r0`, `game-final` et `game-inspection` restent des preuves antérieures ; leurs flaques ne représentent pas le réglage final r2. La classification par composante conserve volontairement le profil lac sur une étendue mêlant métal et terrain naturel. La discrétion du mouvement est vérifiée par le code et les tests d'horloge ; les deux images fixes ne prétendent pas démontrer sa perception en vidéo. Aucun benchmark global ni commit/push dans cette sous-tâche.
