# Cache du terrain et de l’eau, raccords des murs — 12 septembre 2026

Ludovic valide l’aspect de l’herbe rase, de l’eau et des spots (« Oui c’est bon »), puis
signale un ralentissement général, l’arrivée tardive de l’eau texturée et des triangles
vides sous les murs ruinés. Les corrections conservent cette direction artistique.

## Causes et corrections

- **Lisières du terrain** : les mélanges sable/herbe/terre étaient recalculés par
  sous-échantillon à chaque image. Leurs couches alternaient les textures dans le
  SpriteBatch, provoquant des milliers d’appels de dessin. `SpriteFloorSkin` conserve
  désormais les commandes de chaque voisinage de terrain et les regroupe par matière
  sur l’ensemble de la passe de sol. Les listes de commandes visibles sont réutilisées.
  L’ordre des couches à chaque point, les coordonnées, teintes et opacités sont conservés.
  Le cache suit les neuf types de terrain voisins ; un changement de terrain invalide
  la zone concernée, tandis que le curseur, l’atmosphère et les fuites ne changent pas
  ces commandes. Un autre plan de pont réinitialise le cache.
- **Animation de l’eau** : sa géométrie était déjà conservée, mais ses sommets UV/couleur
  étaient modifiés sur le processeur et renvoyés au GPU à chaque image. Les buffers GPU
  sont maintenant immuables ; un shader applique les mêmes ondes et reflets en recevant
  seulement l’horloge commune. Berges, profondeur, opacité et comportement en pause
  restent inchangés. Voir [mesures de l’eau](water-gpu.md).
- **Arrivée et retour sur un pont** : les contours et la matière d’eau sont préparés dès
  le début de la préparation du plan, en parallèle du cache statique. La première image
  jouable en sprite attend leur publication, au même titre que les murs et meubles.
  Les caches `LeakSkin` et `SpriteWaterSkin` gardent trois publications (active et deux
  ponts récents), avec réutilisation des contours et des buffers. Une nouvelle révision
  remplace l’ancienne du même pont ; un autre monde ne peut pas emprunter une ancienne
  surface. Les erreurs de préparation froide sont remontées à l’écran de chargement.
- **Triangles sous les cloisons** : le dessus utilisait des raccords d’angle continus,
  mais les façades étaient extrudées à partir de rectangles indépendants. Les façades
  partagent maintenant les mêmes sommets d’angle ; les vraies extrémités restent fermées
  et les passages ne sont pas comblés. L’usure et la topologie du dôme restent inchangées.

## Validation

### Scène complète

Même `TheEndGame`, pont 3, centre (124,146), 1920×1080, 32 pixels/cellule,
supersampling 1, simulation en pause : 120 images de préparation puis 240 mesurées.
Les deux mesures retenues ont été réalisées séparément, sans autre hôte natif ou test
lourd concurrent, sans capture d’image pendant la mesure.

| Mesure | Avant | Après |
| --- | ---: | ---: |
| Temps moyen du dessin | 163,30 ms | 21,88 ms |
| Temps médian du dessin | 164,45 ms | 21,74 ms |
| Appels GPU par image | 23 145 | 363 |
| Cadence observée | 6,02 images/s | 40,00 images/s |
| Primitives par image | 631 821 | 631 629 |

Les références des caches de scène statique, murs, meubles, cloisons et état des portes
pour la lumière n’ont changé sur aucune des 240 images. La scène mesurée n’a pas de
spot visible. Cela confirme la régression du sol et de l’eau sans attribuer le résultat
aux spots ni à une reconstruction continuelle des murs.

La première correction du terrain avait déjà ramené le dessin à 22,21 ms et 923 appels.
Le regroupement global réduit encore les appels à 363, mais n’apporte pas de gain de
cadence significatif dans cette scène. Il n’est pas présenté comme une nouvelle hausse
de FPS. Ces mesures Debug locales ne garantissent pas la même cadence sur toutes les
vues ou pendant une simulation chargée.

Rapports : [avant](scene-before.json), [étape par cellule](scene-cell-batching.json),
[version finale](scene-after.json). Le premier essai avant avec chevauchement de
processus est exclu des temps comparés.

### Chargement, géométrie et régressions

Le parcours 0 → 3 → 0 → 3 confirme **zéro image jouable sans l’eau sprite** après
correction, contre deux puis trois images au premier accès/retour dans la preuve avant.
Le nombre de constructions des contours passe de quatre à deux ; les identités des
contours et surfaces sprite sont les mêmes lors du retour sur chaque pont.
Rapports [avant](water-loading-before.json) / [après](water-loading-after.json),
[première image jouable du dôme](first-playable-dome.png) et
[retour sur le dôme](revisited-dome.png).

Ce dernier contrôle fonctionnel a tourné pendant la suite de tests et des captures
de comparaison raster : ses durées de chargement ne sont pas comparées à celles de
l’avant. La disponibilité dès la première image et la réutilisation des publications
sont les invariants vérifiés. La mesure de performance de la scène, ci-dessus, a bien
été effectuée séparément.

Le [contrôle natif du sol](floor-batching.md) obtient zéro pixel différent sur quatre
vues 1920×1080 après le regroupement global : lisière à 32 px/cellule, lisière à 48
avec déplacement fractionnaire de caméra, herbe et courbe de séparation du dôme.
La [preuve des raccords de murs](ruin-joints.md) confirme la fermeture des triangles,
avec le sol, l’herbe, les passages et le dessus patiné inchangés dans les zones comparées.

Les rapports de mesures, tests et captures finales sont conservés dans ce dossier.
**1 503 tests Renderer réussissent, zéro échec et zéro ignoré**, sur le Client Debug
final compilé sans erreur ni avertissement. Le TRX `environment-performance.trx` et
`validation.json` conservent le résultat. La DLL des tests, du parcours de chargement,
du benchmark final et du jeu installé est identique : empreintes dans
`final-binaries.json`. Tous les processus de capture et de test sont terminés.

Les hôtes temporaires se trouvent dans `TheEnd/.artifacts/water-loading`,
`water-performance`, `render-performance` et `partition-volume-gap`.
Les mesures du composant eau et les mesures de la scène complète sont distinguées :
une économie de soumission CPU ne constitue pas, à elle seule, une garantie de FPS.

Le test de chargement utilise le vrai `TheEndGame` et les visites 0 → 3 → 0 → 3.
Il ne choisit que le pont et la caméra, sans modifier la simulation. Les captures PNG
du premier affichage et de l’état stabilisé servent à vérifier la publication ; ce
parcours avec lectures d’image n’est pas un benchmark de cadence.

La direction artistique validée est documentée dans
[`environment-refinement`](../environment-refinement/README.md).
Les textures PNG, les banques de modèles et Core ne sont pas modifiés par cette passe.
Aucun commit/push Code, Art ou Docs par l’assistant.
