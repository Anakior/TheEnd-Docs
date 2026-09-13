# Eau, cloisons et herbe en mode sprite — 12 septembre 2026

> Version intermédiaire : l'herbe V2 a ensuite été rejetée et l'animation de l'eau renforcée.
> Voir la [retouche suivante](../environment-refinement/README.md) pour la version actuelle,
> avec aussi la correction de projection des cônes lumineux.

Ludovic signale trois défauts dans le dôme : eau en aplats bleus, cloisons avec des carrés
de jonction et herbe en traits verts. Pendant la vérification, il demande également des
raccords de végétation moins carrés et des murs ayant davantage l'aspect de ruines.
Cette version remplace leur présentation dans le
renderer sprite. Les simulations, la topologie des murs et les passages restent identiques.
La direction est intégrée pour examen ; elle n'a pas encore reçu de validation artistique
de Ludovic.

## Rendu intégré

- **Eau** : nouvelle matière raster bleu-vert à rides fines, teinte progressive selon la
  distance à la rive et marge translucide sur le vrai terrain. Suppression du contour
  pointillé et des deux bandes de couleur. Dérive lente des UV liée au tick du jeu ; une
  pause fige l'eau. `SpriteWaterSkin` consomme les contours publiés de `LeakSkin`, y compris
  les îlots, et prépare son maillage sur worker. La géométrie vectorielle reste le repli
  tant qu'une surface de la même grille n'est pas prête, ou si la matière est absente.
- **Cloisons du dôme** : retrait des anciens carrés noirs avec point central et des
  pointillés superposés à la matière métallique. Matières de blindage, rails et canaux
  usés déjà disponibles dans le jeu, avec creux, facettes métalliques ternes, arêtes
  écaillées et extrémités arrachées. La retouche initiale avec contours bruns a été écartée
  après inspection native ; la corrosion est un accent discret, sans zigzags continus.
  Les changements de direction, ruptures, rails rétractés et
  passages restent ceux du jeu. Les rectangles sombres sous certains segments courts
  sont leurs façades verticales texturées, d'environ 20 px au zoom de ces captures.
- **Herbe** : matière de prairie basse, feuilles superposées et touffes irrégulières,
  échantillonnée à 96 pixels par cellule. Teinte atténuée RGB(205,211,195) pour s'accorder
  avec le reste du dôme. Les traits verts de l'ancien rendu sont désactivés seulement
  lorsque cette matière est chargée. Les transitions combinent maintenant les textures
  voisines avec des poids continus et une lisière irrégulière, au lieu de sélectionner
  une seule famille par petit carré. La végétation s'efface aussi progressivement sur
  les dalles adjacentes. Cette version de la végétation est statique.

Sources et prompts : `TheEnd-Art/sprite-render/environment-v2/README.md` et
`provenance.json`. Les deux PNG sources sont copiés sans retouche dans
`TheEnd.Client/Assets/sprites/materials`. Le renderer vectoriel garde son aspect précédent.
Les modèles et banques des portes, sas, rochers et débris n'ont pas été modifiés.

## Captures du vrai jeu

`TheEndGame`, seed 12345, grille 256 × 256, pont 3 (affiché 4/6), sprite avec murs en
volume, fenêtre 1920 × 1080, zoom 16 soit 48 px/cellule. L'hôte change uniquement le pont
et la caméra ; aucun terrain, état de porte ou DisplayFrame n'est mis en scène.

| Vue | Centre | Avant | Après |
| --- | --- | --- | --- |
| Rive du grand lac | (128,100) | [Avant](before-water.png) | [Après](after-water.png) |
| Cloisons, eau et herbe | (124,146) | [Avant](before-partitions-water.png) | [Après](after-partitions-water.png) |
| Prairie | (184,82) | [Avant](before-grass.png) | [Après](after-grass.png) |

Les JSON voisins des images conservent les cadrages et ticks réels. Les binaires avant
ont été copiés indépendamment avant modification : Client SHA256
`F4E1ED63EA103584414A0D32B7EB2A28095B6EE3CDB7350752AC130BBE626642`.
`environment-audit.json` décrit les cellules réelles des deux cadrages du dôme.
`validation.json` donne le résultat des captures finales et des tests.

## Vérification

Compilation Client Debug sans erreur ni avertissement ; **133 tests ciblés réussis,
zéro échec, zéro test ignoré**. Les trois captures après modification ont été produites
par le même binaire final et inspectées. Les images avant/après sont cadrées de façon
identique, sans collage ni retouche.

Les tests ciblés couvrent contours concaves, petits bassins, îlots secs, surface conservée,
annulation du worker, identité des grilles, continuité des mélanges de terrain et limites
des dégâts visuels sur les cloisons intactes/endommagées. Les preuves
portes/lampes précédemment bloquées par Windows sont également terminées : 610 tests
réussis et trois captures natives examinées dans `../door-lamp-fixes/README.md`.

Le premier découpage de l'eau propagait chaque bande de rive à travers tout le lac. Le
maillage final garde une grille régulière à l'intérieur et ne découpe finement que les
cases traversées par une berge : 98 043 sommets pour 5 663 cellules d'eau, contre 611 493
au premier essai. Audit local CPU : préparation sur worker 0,6–1,1 s, 14 118 sommets
visibles autour de (128,100), dérive UV 0,37–0,66 ms selon la vue. Ce sont des mesures
locales de ces étapes, pas une garantie de fréquence d'images globale. L'écart de surface
mesuré par rapport aux contours est inférieur à 0,00001 cellule².

`water-mesh-audit.json` conserve les mesures. Pas d'optimisation générale ni de nouvelle
dépendance. Aucun commit/push Code, Art ou Docs par l'assistant.

## Reproduction locale

Après compilation du Client, le probe temporaire existant peut refaire les trois cadrages :

```powershell
.\.artifacts\door-lamp-fix\native\run.ps1 -Name environment-release-water -DeckId 3 -X 128 -Y 100
.\.artifacts\door-lamp-fix\native\run.ps1 -Name environment-release-mixed -DeckId 3 -X 124 -Y 146 -NoBuild
.\.artifacts\door-lamp-fix\native\run.ps1 -Name environment-release-grass -DeckId 3 -X 184 -Y 82 -NoBuild
```

Sur une autre machine sans `.artifacts`, les images et leurs métadonnées suffisent pour
retrouver ces cadrages dans le jeu normal. Les matières installées ne dépendent d'aucun
chemin de cache Codex.
