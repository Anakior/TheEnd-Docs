# Draps plus calmes, échelle dans l'ombre et espace peint

Retours du 13 septembre 2026 : Ludovic juge les draps trop texturés pour lire
nettement des lits, souhaite que l'échelle disparaisse davantage dans l'ombre et
demande un espace stylisé accordé au décor peint. Cette passe poursuit ces trois
points dans le client ordinaire.

## Draps V3

La couverture perd les grands zigzags contrastés de la V2. Des surfaces beaucoup
plus calmes et quelques plis doux rendent distincts l'oreiller clair, le drap et
la couverture bleu ardoise. Les douze états/familles, positions, faces, UV et
transformations sont conservés exactement, preuve `textile-v3-validation.json`
dans `TheEnd-Art/objects/bed`.

Nouvelle peinture via ImageGen intégré : `TheEnd-Art/objects/bed/textures/bed-textile-painted-v3.png`,
[prompt exact et provenance](../../../../TheEnd-Art/objects/bed/textures/bed-textile-painted-v3-prompt.txt).
La référence était la V2 rejetée ; les anciennes images restent conservées.
Le fichier enregistré `bed.blend` est retouché par remplacement du datablock image,
repacké puis réexporté/validé/installé avec `tools/models/build-model.ps1`.

L'inspection native sélectionne maintenant chaque couple de famille et d'état
réellement présent (`bunk`, `bunk-medical`, `table-examen`) ; un lit médical ne
représente plus à lui seul toutes les couchettes. Aucun objet ou état du monde
n'est créé pour les captures.

## Échelle dans l'ombre

La source sauvegardée `TheEnd-Art/objects/service-ladder/service-ladder.blend`
conserve sa géométrie. La matière des barreaux et du cuvelage suit maintenant
la profondeur réelle : l'entrée reste lisible puis les détails s'effacent
progressivement jusqu'au noir. Le gradient est cuit par l'export canonique ;
aucun calcul de pixels ne s'ajoute au rendu. Deux textures partagées, parties
`rim`/`descent` et variantes `ready`/`broken` conservées.

[Capture native à 48 px/case](game-final/game-11-ServiceLadder.png) et
[audit source/export](service-ladder-depth-validation.json).
Une [inspection à 96 px/case](ladder-inspection/game-11-ServiceLadder.png)
confirme le fondu : seul le zoom de la caméra de diagnostic change, sans
retouche du PNG ni modification du zoom normal. Sa
[preuve native](ladder-inspection/native-game-validation.json) passe également.

## Espace peint

Un fond peint bleu ardoise et violet désaturé, avec des masses sombres et des
étoiles irrégulières, remplace le fond noir ponctué du mode sprite. L'image est
créée avec ImageGen intégré, conservée sans retouche puis installée dans
`TheEnd.Client/Assets/sprites/space/painted-space-v1.png`.

[Source et provenance](../../../../TheEnd-Art/sprite-render/painted-space-v1/README.md),
[prompt exact](../../../../TheEnd-Art/sprite-render/painted-space-v1/prompt.txt).
PNG RGB opaque 1672 × 941, SHA256
`FDA0CD21CFC0C7C64301117CC86C54B14B20172DED417BAD1EAD69AB80FDDA2A`.

`SpriteAssets` charge et conserve cette image avec les autres assets.
`SpriteSpaceSkin` soumet un seul quad avant les surfaces du vaisseau ; le fond
reste à l'infini pendant le déplacement et le zoom. Le recadrage couvre la
fenêtre sans étirer l'image. Pas d'animation, de chargement ou de création de
texture par frame. L'ancien `SpaceSkin` reste le secours si le PNG est absent.

[Espace et vaisseau dans le jeu](game-final/game-01-Elevator.png).
La [comparaison des surfaces intérieures](space-compositing-validation.md)
mesure 816 219 pixels intérieurs distincts identiques entre V2 et V3, tandis
que la région témoin extérieure change bien avec le nouveau fond.

## Validation terminée

- Client compilé : **0 avertissement, 0 erreur** ; [journal](build-final.log).
- **160 tests ciblés réussis**, couvrant lits, échelle, espace et résolution
  des matières : [TRX](interior-review-v3.trx), [journal](tests-final.log).
- **17 captures natives** du vrai `TheEndGame`, assets installés, sans override
  de banque ni modification du monde, tick visuel 12000, 48 px/case :
  [preuve du jeu](game-final/native-game-validation.json). Les sept banques
  sont effectivement chargées et les caches contrôlés sont stables 35 frames.
- Les huit couples famille/état de couchage présents dans ce monde sont
  inspectés, dont la [couchette ordinaire avec draps](game-final/game-03-Bunk-bunk-Sealed.png).
  Les états absents restent couverts par les douze variantes et leurs tests ;
  aucune capture d'un état absent n'est revendiquée.
- Dôme complet **identique à la référence validée : 0 pixel différent sur
  2 073 600**, y compris les régions d'eau et de berge. Cette vue ne montre
  pas d'espace extérieur, contrairement aux vues du vaisseau.
- [Audit des assets](asset-validation.json) : 164 fichiers des quatre banques
  identiques entre export validé, Code et runtime ; les 16 assets historiques
  sont inchangés. L'image d'espace est également identique entre Art, Code et
  runtime. Shader d'eau inchangé. Aucun benchmark FPS global effectué.

DLL contrôlée : `558222C90043ED03AEE2614AC2E2CCC7A30A782F25C099B3E153A131BEBB57C5`.
Sources `.blend` : lit `C959D0E53308323316E6D9EA466D12F447CF5216F6F09991C914EC9845223E5F`,
échelle `8C3A5394B4E34BBEECD899BC11463A0B1C0E6FEAD4ED52073FAB6F8426AD195F`.

Les variantes, dimensions et mécanismes de la simulation restent inchangés.
Cette retouche est intégrée pour poursuivre les retours artistiques en jeu ; elle
ne constitue pas encore une approbation de Ludovic. Aucun commit/push Code, Art ou Docs.
