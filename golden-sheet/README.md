# Golden sheet — banc de référence des murs

**État : RÉFÉRENCE DE TRAVAIL, NON VALIDÉE (8 août 2026).** Ludovic constate une nette amélioration des raccords mais doit encore remonter de petits défauts. Cette planche sert déjà à comparer les révisions ; elle ne devient un verrou de référence qu'après sa validation explicite.

## Ce que c'est

`golden_sheet.png` est un montage de 25 crops d'UNE capture réelle du jeu (`capture-brute-7680x4320.png`) :
le harnais `THEEND_GOLDEN` (`TheEnd.Client/Development/GoldenWallBench.cs`, délégué au frame 150 par
`FrameCaptureHarness`) pose 25 configurations canoniques de murs/portes via les vraies `PlaceWallsCommand`
(le trajet exact des outils D/C/P). `GoldenWallFixture` fournit un pont neutre dédié : aucune coque générée,
avarie, pièce ou histoire ne peut traverser un crop, tandis que les commandes, la simulation et le pipeline de
rendu restent ceux du jeu. La capture se fait frame 420 via `THEEND_SHOT`.

Depuis la racine `TheEnd-Docs`, capturer puis reconstruire une nouvelle planche dans `.cache` :

```bash
THEEND_SHOT="$(pwd)/.cache/golden-sheet/capture-brute-7680x4320.png" \
THEEND_GOLDEN=1 dotnet run --project ../TheEnd/TheEnd.Client
golden-sheet/build-sheet.sh .cache/golden-sheet/capture-brute-7680x4320.png
```

La fenêtre du client doit mesurer exactement **1920×1080** pendant la capture. Le render target 4× mesure alors
7680×4320, avec exactement 48 px/cellule et l'origine `(wx·48 − 2016, wy·48 − 6048)`, dérivée de
`CenterOn(122, 171)` dans le harnais. Le script refuse toute autre dimension et toute case qui sortirait de la capture.

La découpe n'est plus manuelle. Le manifeste versionné dans `build-sheet.sh` produit deux niveaux :

- `cases/01.png` à `cases/25.png` sont les crops 672×672 **sans redimensionnement ni cartouche**, destinés à la
  comparaison fidèle ;
- `golden_sheet.png` est l'aperçu 5×5, avec des vignettes ramenées à 480×480 et un libellé.

Le script nécessite Bash, un `awk` POSIX et ImageMagick 7 (commande `magick`). Il emploie directement la police
JetBrains Mono livrée avec le client, afin que les cartouches ne dépendent pas des polices installées sur la machine.
Le dépôt de code voisin `TheEnd` est utilisé par défaut ; `THEEND_CODE_ROOT` permet de choisir
un autre emplacement. Sans argument, le script relit la capture de référence et écrit sa planche
et ses cases dans `.cache/golden-sheet`, sans remplacer les témoins versionnés.
On peut lui passer d'autres destinations sans toucher à la référence suivie :

```bash
golden-sheet/build-sheet.sh /tmp/capture.png /tmp/planche.png /tmp/cases
```

Les coordonnées monde des 25 configurations sont le manifeste de `GoldenWallBench.cs`.

## Les cases

1-17 : familles de base sur sol métallique (droits, L/T/croix, diagonales déclarées, zigzag non déclaré, cercles
déclaré/déchiré/non déclaré, portes droite/diagonale/entre croisements, deux salles).
18-24 : la famille MASSE, construite depuis les screens de Ludovic du 7 août (croix sur masse, portes entre blocs,
couloir taillé, petite croix, logement+T+porte = sa référence, porte serrée à segments d'une cellule).
25 : une porte découpée dans un cercle déclaré sur une tangente diagonale, par les mêmes commandes que l'outil joueur.

## Où en est le code (pour reprendre)

La save complète : Atlas `wizishop/save-claude/chantier-golden-sheet-murs.md`.
Le plan et le journal d'exécution : Atlas `theend/meta/plan-moteur-murs.md` (section 6, entrées « 7 août suite 6→11 »).
Le pipeline actif compile désormais les sources déclarées en un `WallLayout` unique, puis
`WallLayoutSkin` peint ses rails et ses nœuds. L'ancien `WallSkin` et ses décisions concurrentes
(`Crossing`, `Piece`, `StrandRuns`, `NearestFaceRail`) ont été supprimés après migration de leurs invariants.
La planche reste volontairement indépendante des tests structurels : elle juge la somme réellement peinte
par tous les skins.
