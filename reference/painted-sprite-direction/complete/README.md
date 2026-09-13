# Peinture du mobilier et du décor

Le retour « C'est mieux comme ça oui » valide la reprise des quatre modèles intacts. Ludovic insiste ensuite : le côté peint doit se retrouver sur tous les éléments, à la manière des personnages. Cette passe conserve les volumes approuvés, décline le mobilier et vérifie une première zone avec des matières peintes dans le vrai jeu.

## Première zone dans le moteur

Les nouvelles peintures portent sur la dalle métallique, les murs, la terre, l'herbe courte et l'eau. Le premier dôme montrait encore une rupture avec le sable et le sol fongique ; deux peintures supplémentaires complètent ces matières dans la V2.

- [Salle avec mobilier et matières peintes](game-with-world-paint/game-2-Table-Sealed.png).
- [Même salle, anciennes matières du décor](game-before-world-paint/game-2-Table-Sealed.png).
- [Dôme avec les sept matières de l'étude](game-dome-final-paint/game-7-Dome-Environment.png).
- [Même dôme, anciennes matières](game-before-world-paint/game-7-Dome-Environment.png).
- [Premier essai à cinq matières](game-with-world-paint/game-7-Dome-Environment.png), conservé pour expliquer la reprise du sable/fongique.

Les captures viennent du vrai `TheEndGame`, avec ses lumières, sa géométrie et son interface. Les deux images sous `TheEnd-Art/sprite-render/painted-world-direction-v1` sont des **concepts générés**, distincts de ces preuves natives.

Sources matérielles : `TheEnd-Art/sprite-render/painted-world-materials-v2/README.md`, sept PNG natifs, `aliases.json`, prompts et provenance ImageGen. La V1 est préservée. Les cinq images initiales sont identiques dans V2 ; seuls le sable et le sol fongique s'ajoutent. La peinture remplace le grain photographique par des masses colorées et des touches visibles, adaptées à chaque matière.

**Limites de cette étude :** les dix dalles standard/vieillies partagent encore une première peinture ; leurs usures restent à décliner. La pierre, les fracturations de sol, la frange de coque et les peintures propres aux portes, rochers et débris n'ont pas reçu cette reprise. Les cryopods intacts conservent leur source approuvée. Ces éléments devront suivre la direction peinte avec leurs propres variantes ; le jeu entier n'est pas encore repeint.

## Mobilier : 70 variantes préparées

| Famille | Formats et habillages | États | Nombre |
| --- | --- | --- | ---: |
| Tables/bancs | Courts et longs | Fermé, ouvert, dépouillé, cassé | 16 |
| Consoles | Deux/trois places ; Dalle, Visière, Peigne | Les quatre états | 24 |
| Rangements | Une/deux/trois travées | Les quatre états | 12 |
| Alcôves de commande | 3 × 2 et 4 × 3 ; Dalle, Peigne | Les quatre états | 16 |
| Cryopods endommagés | Coque, intérieur, restes du couvercle, occupant selon l'état réel | Dépouillé, cassé | 2 |

`sealed` est le vocabulaire existant pour intact/fermé ; il n'ajoute aucune soudure universelle ou nouvelle règle de gameplay. Les panneaux ouverts, niches dépouillées et assemblages cassés sont des volumes distincts. La console garde l'écran incliné, le pupitre en retrait et le module de service. Les formats plus grands assemblent les composants à leur taille réelle.

Sources sauvegardées et autoritaires :

- `TheEnd-Art/objects/common-furniture/common-furniture-painted.blend` ; documentation `PAINTED.md`.
- `TheEnd-Art/objects/utility-furniture/utility-furniture-complete-painted.blend` ; `complete-painted-study.md`. Cette source conserve les 36 consoles/rangements de `utility-furniture-painted.blend` et ajoute les 16 stations.
- `TheEnd-Art/objects/cryopod/cryopod-damaged-painted.blend` ; `damaged-painted-study.md`.

Les `.blend` de profondeur approuvés et l'atlas V2 restent inchangés. Les exports homonymes sont externes. [Audit des banques](bank-validation.json) : 70 variantes, provenance et empreintes concordantes, aucune UV texturée hors [0,1], erreur de skinning maximale 0 m.

[Couverture native](native-validation.json) : 15 planches, 116 cartes disponibles, 70 variantes distinctes, manifestes utiles vérifiés. Les planches communes et cryopods précèdent le chargeur de matières ; les dernières planches utilitaires utilisent la DLL finale. Le rapport distingue ces cohortes.

## Chargement, cache et contrôles

`SpriteMaterialResolver` et `THEEND_SPRITE_MATERIALS_DIR` permettent l'essai externe, avec repli sur le matériau installé s'il manque. Un objet `aliases.json` associe les noms existants à des fichiers PNG du dossier. Le cache utilise le chemin physique et la taille d'import : plusieurs alias partagent la même texture, détenue et libérée une seule fois.

Les murs passent une seule fois à 256 × 256 pour respecter leurs UV à 48 texels par case. Les peintures externes ne subissent pas les gains d'éclaircissement de l'ancien matériau. La frange oblique garde sa copie indépendante. Le chargement et la publication différée des assets restent hors de la boucle de dessin.

Build Client et helper : 0 erreur, 0 avertissement. Les 10 tests ciblés du resolver passent. La suite de 1810 tests de la passe initiale n'a pas été relancée ni revendiquée comme nouveau résultat. `git diff --check` passe.

Les huit vues avant/après utilisent les mêmes objets, états, caméras à 48 px/case et tick 12000, sans modifier le monde : les sept cibles sont sorties du rendu vectoriel et la révision du cache mobilier reste stable pendant 25 images après préparation. Le contrôle du dôme est répété seul après les deux peintures supplémentaires. Ces observations sont fonctionnelles et visuelles ; elles ne constituent pas un benchmark FPS global.

Les JSON voisins des captures conservent les banques, le binaire, le cadrage et les empreintes des matières. Le binaire final est `FBAA2C887F44B744A677BED8BE3A5ABF890C82CCF85E25A2B9CB14E897CF8E2E`.

Le [contrôle de comparaison](world-validation.json) confirme les huit cadrages/objets identiques, les cinq peintures V1 conservées dans V2 et les sept événements de chargement uniques pour 22 alias. Aucune erreur de chargement de texture dans le journal final. La stabilité du cache observée reste celle du mobilier ; aucun chiffre de FPS global n'en est déduit.

## Relancer

Depuis TheEnd, pour le vrai jeu avec cette étude :

```powershell
./tools/fixtures/open-painted-world-study.ps1 -NoBuild
```

Pour les états isolés :

```powershell
./tools/fixtures/open-fixture-study.ps1 -Page consoles -CommonFurnitureBank C:/workspace/TheEnd-Art/exports/common-furniture-painted -UtilityFurnitureBank C:/workspace/TheEnd-Art/exports/utility-furniture-complete-painted -CryopodDamagedBank C:/workspace/TheEnd-Art/exports/cryopod-damaged-painted -NoBuild
```

Touches 1–5 pour la famille, Page précédente/suivante pour les formats, R pour tourner, +/- pour le zoom. Les sources et captures restent disponibles pour la revue artistique. Aucune copie dans les assets installés ; aucun commit/push Code/Art/Docs par l'assistant.
