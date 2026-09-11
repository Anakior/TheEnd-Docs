# Recherche de porte dans le vaisseau

## Dessin peint approuvé, contrôle natif en mouvement à juger

Ludovic a **approuvé le dessin de la [planche peinte fermée / ouverte](door-painted-study.png)**,
avec une réserve sur les pieds du colon par rapport au mur dans l'image générée.
Il demande de voir le mouvement. La nouvelle source éditable est
`C:\workspace\TheEnd-Art\objects\door\door-painted-study.blend` ; son export
`body/painted` est validé et reste chargé uniquement par le diagnostic.
Le modèle et son rendu natif attendent le retour utilisateur.

Le premier mouvement a révélé deux défauts signalés par Ludovic : du seuil gris
restait visible de chaque côté des vantaux trop étroits, et le joint de pleine
hauteur produisait une grande face noire mobile. La vidéo actuelle reprend des
vantaux élargis à 0,94, sans cette plaque noire, avec une fente de rangement et
un retrait suffisant pour que le mur les masque une fois ouverts. Il s'agit de
corrections du modèle Blender ; le moteur et la cadence sont inchangés.

Ludovic trouve ensuite l'ouverture meilleure, mais repère un rectangle en haut
et demande plus de détails. La version actuelle retire les seuils clairs des
logements et la répétition de dalles à rivets dans le passage ; leurs chants
reprennent le métal sombre du mur. Les vantaux reçoivent des panneaux
chanfreinés, des fixations et des raidisseurs, dans la même silhouette et avec
la même course. Ces détails restent éditables dans le `.blend`. La vidéo
ci-dessous montre la reprise décrite ci-après, qui attend son appréciation.

Ludovic précise ensuite que le logement doit être un élément mécanique dans
lequel rentre la porte, et que l'ensemble manque de volume. La version actuelle
donne à chaque entrée un carter avec capot saillant, joues épaisses et guides
visibles. Le graphite du mécanisme remplace le sol dans les poches ; le passage
piéton reste distinct. Les accessoires du carter montent à 0,825, les murs
restant à 0,6. Les vantaux détaillés, leur largeur et leur mouvement sont conservés.

Cette base est jugée meilleure. Ludovic demande ensuite que le bord lu sur le
mur appartienne visuellement au vantail mobile : le liseré clair du nez du
carter est rendu plus discret, et le chant plié déjà lié au vantail est
renforcé. La vidéo actuelle contrôle cette distinction entre pièce mobile et
logement fixe, sans ajouter de composant ni modifier la course.

La [vidéo native](door-motion.mp4) et son [aperçu GIF](door-motion.gif) montrent
six secondes à 30 images/s : deux passages à trois cases/s, aller au centre puis
retour décalé de 0,15 case vers le mur bas après un pas latéral visible. L'animation
du colon, sa taille, la caméra, la lumière et la profondeur sont celles du jeu.
Les captures confirment que les bottes sont naturellement masquées au retour.
La scène entière est recadrée puis agrandie ×2 dans la vidéo et le GIF ; le
personnage n'est pas redimensionné séparément.

La simulation est figée pendant l'enregistrement ; le sceau est masqué et les
positions sont mises en scène dans des copies de la présentation. Ce n'est pas
une validation du pathfinding ou des collisions. Aucun modèle n'est installé
dans les assets ordinaires.
[Source, export et reproduction du diagnostic](../../../TheEnd-Art/objects/door/README.md).
[Provenance de l'image approuvée et prompts](door-painted-study.md).

## Essai rejeté : silhouette dans la coupe du mur

**Retour de Ludovic : « Non mais ça ressemble à rien surtout encore ».**
La planche et sa source Blender sont rejetées à leur tour. Aucun dessin ni
convention de coupe de cet essai n'est validé. Elles restent ci-dessous pour
documenter l'historique ; elles ne constituent pas une base acceptée à habiller.

[Trois vues natives de la porte simplifiée](door-silhouette.png).
Source : `C:\workspace\TheEnd-Art\objects\door\door-silhouette-study.blend`.

Après le rejet du cadre entier, Ludovic demande de retenter. Cet essai repart
de la silhouette : deux vantaux d'épaisseur 0,24, coupés à 0,59 comme les murs à
0,6, et entièrement rentrés dans les extrémités du mur lorsqu'ils sont ouverts.
Pas de cadre haut ni de cassettes ajoutées au-dessus des murs. Les matériaux sont
unis ; aucune nouvelle texture n'est produite.

Le personnage conserve sa taille, sa caméra et son rendu usuels. Le torse reste
visible dans le passage ; les murs proches peuvent encore masquer les pieds.
La coupe du modèle n'est pas une décision de hauteur physique : il ne contient
que la partie visible, alors que le colon reste entier. Le risque de percevoir
une petite barrière avait été relevé ; la proposition a depuis été rejetée.

Le premier seuil était trop étroit et rappelait le contour des vantaux fermés.
Il est maintenant presque affleurant, large comme le passage et proche du sol en
valeur. Les joues sont minces et couvrent les extrémités du mur dans leur largeur.
Les hachures visibles au début appartenaient au décor vectoriel de la cellule de
porte, classée hors du sol. Le seuil couvre cette surface dans l'essai ; le cache
de décor du jeu n'a pas été modifié. Course conservée de 0,48, largeur libre entre joues
0,962 ; vérification indépendante des bornes exportées. Le contrôle de la source
et de son export passe, avec une erreur maximale ≈2,98×10⁻⁸.

La planche montre fermé, ouvert avec le colon au milieu, puis ouvert avec le
colon de l'autre côté. Les captures entières sont recadrées et agrandies ×2,
sans retoucher la taille du personnage. **Poses fixes, une orientation, aucun
test de navigation ou de collision.** Le sceau est masqué pour l'étude ; la
simulation reste verrouillée. Aucun nouveau modèle installé en production.

Reproduction : mêmes réglages de capture ci-dessous, avec
`THEEND_DOOR_STUDY=low` et
`THEEND_DOOR_STUDY_BANK=C:\workspace\TheEnd-Art\exports\door-silhouette-study`.
Le script local `TheEnd/.artifacts/door-clearance/capture.ps1` accepte `-Bank`.

## Retour sur la porte entière rejetée

Essai précédent **rejeté** : [porte entière retravaillée](door-refined.png).
La source éditable est `C:\workspace\TheEnd-Art\objects\door\door-cutaway-study.blend`.
Aucun dessin n'est validé pour la production. Retour de Ludovic sur cette dernière
planche : « ça ressemble vraiment à rien et c'est chelou ». Ne pas poursuivre
l'habillage de ce cadre en le considérant comme une base acceptée.

Constat de la revue : la vue du jeu fait surtout lire le dessus et les profils
superposés d'une porte haute au milieu de murs coupés. La matière seule ne résout
pas sa silhouette. Piste de travail proposée, sans décision produit acquise :
juger d'abord une géométrie simple fermée et ouverte avec la caméra du jeu, les
vrais murs et le colon, avant de détailler à nouveau le modèle.

## Reprise du cadre et de la matière

Ludovic a rejeté les trois dessins de la [comparaison précédente](cutaway-native.png).
Il considère seulement la porte entière comme la proposition de volume la plus
crédible, et demande de poursuivre. `frame` est donc retravaillée dans le même
`.blend` ; l'ancienne planche conserve sa géométrie précédente.

Le modèle possède désormais deux profils chanfreinés dans l'épaisseur réelle du
mur, des cassettes centrales plus fines, un seuil et un capot supérieur continu.
Une matière d'acier peint est appliquée par UV et packée dans Blender. Sa
[provenance et son prompt](../../../TheEnd-Art/objects/door/textures/provenance.md)
documentent l'usage de l'outil imagegen intégré pour la matière seule.

La nouvelle planche distingue la vue d'inspection Blender à gauche (caméra et
éclairage propres) des deux captures natives à droite (murs, colon, échelle et
éclairage du jeu). Les recadrages natifs sont agrandis ×2 dans leur ensemble.
Les détails du modèle et le rendu dans le jeu sont donc évaluables séparément.

La baie droite de ce cadre mesure 0,94 jusqu'à Z=1,785, puis 0,71 sous le sommet
chanfreiné à Z=1,925. L'enveloppe atteint Z=2,045 et reste dans la profondeur
réelle du mur (±0,5). La course rigide des vantaux est toujours de 0,48.
Un défaut d'orientation des faces avant biseau a été corrigé : les vantaux fermés
ne se chevauchent plus. Relecture indépendante des bornes exportées effectuée.

Export et comparaison avec Blender réussis (erreur maximale ≈3,73×10⁻⁸), puis
captures natives fermée, ouverte avec colon au milieu et ouverte avec colon après
la porte. Les poses restent fixes. L'étude n'est pas installée dans les assets
de production. Le modèle demeure presque de profil dans ce passage : les montants
et les logements masquent encore une partie du colon, et la lecture du raccord
aux murs coupés reste à améliorer. Le détail de la vue Blender ne résout pas à
lui seul cette limite du rendu en jeu.

## Historique de la proposition générée

Statut : **propositions écartées pour leur orientation et leurs proportions**, après retour de Ludovic. Les trois précédents modèles Blender avaient déjà été rejetés, ainsi que leur décor de murs simplifié. Cette recherche produite avec l'outil imagegen intégré ne constitue ni un modèle 3D ni une capture de modification du jeu. Elle ne doit pas servir de référence dimensionnelle.

Image : [direction-dans-vaisseau.png](direction-dans-vaisseau.png).

Références : la capture native `TheEnd/.artifacts/obstacle-sprites/WeldedSeal-sprite-48-bars.png` et la matière `TheEnd-Art/sprite-render/poc/input/wall-skin-selected-v1.png`. La composition est générée à partir de ces références : les murs ne sont pas une reproduction garantie pixel par pixel. Les profils fins superposés, l'acier sombre, les canaux en retrait et le cuivre localisé servent de base. Les traverses soudées restent le choix acquis ; aucun habillage A/B n'est validé.

Le premier résultat avait inversé le sens mécanique des vantaux et des traverses. Une seconde passe a demandé un joint horizontal et des traverses verticales, puisque les vantaux coulissent nord/sud dans ce passage orienté est/ouest. Cette consigne n'a pas suffi : la porte reste représentée comme une face posée à plat au lieu d'un volume vu presque de profil dans ce mur. Les prompts ci-dessous conservent la provenance, pas une correction validée.

## Contrôle de l'orientation et du passage

[Planche de contrôle native](controle-passage.png) : comparaison avant/après de la découpe du dessus du mur, avec le même colon dans la même pose fixe. Le dessin de porte reste celui du rendu courant ; ce n'est pas une proposition de nouvelle porte. Les recadrages sont agrandis ×2 sans retouche, décor et personnage ensemble.

**L'échelle du colon est celle du jeu**, sans modification dans la capture : `ActorVisualMetrics` conserve `Scale = 1`, puis la caméra normale projette le modèle. Le zoom de capture atteint le plafond habituel de 48 pixels par case. Sa hauteur coiffée en marche (environ 1,74–1,76 unité modèle) représente environ 59–60 pixels de hauteur projetée, puis 118–120 pixels sur la planche agrandie. La coupe des murs à 0,6 et la projection oblique empêchent de comparer directement la hauteur apparente du colon à la largeur du passage au sol.

**La première planche ne validait pas le passage.** Ludovic a repéré un mur visible sous la porte, qui cachait aussi une partie du colon. Le défaut était dans le rendu sprite : les faces latérales étaient déjà découpées autour de la baie, mais le dessus reprenait les peintures continues du mur. Une fois surélevé, ce dessus écrivait une profondeur opaque dans le passage. Ce n'était ni un agrandissement du colon ni un changement des collisions par l'outil de capture.

La porte de départ est centrée en `(66,5 ; 56,5)`, avec une tangente nord/sud et un passage est/ouest. Les vantaux se retirent vers le nord et le sud dans le mur. La projection doit venir de cette géométrie 3D ; dessiner une façade carrée directement dans l'image ne respecte pas sa profondeur.

| Mesure dans la grille du jeu | Valeur | Portée |
| --- | ---: | --- |
| Baie nominale commune | 0,94 case | Distance entre les axes des jambages ; ce n'est pas la largeur libre |
| Entre les bords intérieurs des jambages vectoriels | 0,863 case | Après leur épaisseur de trait |
| Entre les matières des jambages du sprite actuel | ≈ 0,684 case | Après quantification de leur texture |
| Largeur instantanée maximale du colon en marche est/ouest | ≈ 0,46 case | Modèles et variantes disponibles, contour compris |
| Largeur instantanée maximale en marche nord/sud | ≈ 0,65 case | Même mesure, rotation et projection comprises |
| Ouverture centrée minimale couvrant le cycle nord/sud | ≈ 0,779 case | Inclut le déport du corps, mais aucune marge supplémentaire |

Ces mesures proviennent de la géométrie de porte et des sommets déformés par les 32 poses de marche de la banque actuelle, avec son échelle et son contour de rendu. Elles ne garantissent pas les tailles de futurs modèles ou mods. La largeur mesurée au sol est compatible avec la silhouette est/ouest, mais cela ne valide pas le rendu ni un trajet ; le montant peut recouvrir une partie du corps en orientation nord/sud. La future porte doit donc réutiliser la baie commune et conserver une marge dans les deux orientations, avec la coupe murale à 0,6. Les poches de retrait et les raccords restent à construire.

Le contrôle de capture se lance avec `THEEND_DOOR_CLEARANCE=closed|open|after` et `THEEND_SHOT=<chemin.png>`. Pour reproduire cette planche : `THEEND_BACKEND=sprite`, `THEEND_SHOT_HOME=1`, `THEEND_SHOT_FEATURE=WeldedSeal`, `THEEND_SHOT_ZOOM=16`, fenêtre 1920×1080, langue française et échelle UI 1. `DoorClearanceCapture` copie uniquement la présentation, masque le sceau et place le même colon devant, au centre ou après la porte ; il écrit les coordonnées dans `<chemin.png>.door-clearance.json`. La simulation reste verrouillée et scellée. Les poses sont fixes : **ce n'est pas un test de déplacement ni de collision**. Le pathfinding actuel raisonne par cases et état de porte, sans mesurer la largeur du modèle.

La correction du rendu en volume découpe le dessus après les peintures structurelles et avant les montants, vantaux et sceaux. `WallVolumeGeometry.DoorOpening` fournit les mêmes quatre coins aux côtés et au dessus. `SpriteWallVolume.ClearDoorOpenings` efface réellement la couleur et l'alpha de la surface dédiée ; il ne rend pas le mur semi-transparent. L'ouverture est permanente dans le mur, tandis que les vantaux restent animés indépendamment. Aucun cache de géométrie n'est invalidé à chaque mouvement de porte. Le mode vectoriel et le comparatif sprite à plat ne sont pas modifiés.

Vérification : compilation Debug et **46 tests ciblés réussis** (volume mural, occlusion, caméra des acteurs et présentation de la porte de départ), puis captures natives ouverte et fermée contrôlées visuellement. Les fichiers bruts et les scripts restent dans `TheEnd/.artifacts/door-clearance/`, ignoré par Git. Aucun nouveau modèle de porte n'est installé ; la modification de production porte sur la découpe du mur.

## Essai natif précédent : hauteur de la porte

La planche `cutaway-native.png` compare trois variantes du même modèle et du même
mécanisme, fermées puis ouvertes. Les vrais murs restent en place, le colon garde
son échelle, la caméra et la lumière viennent du moteur. Couleurs, ombres projetées
et masquage par profondeur utilisent le rendu 3D partagé. Le dessin 2D de la seule
porte étudiée est retiré. Toute l'image est recadrée et agrandie ×2 ensemble.

| Variante | Géométrie visible | Question de lecture |
| --- | --- | --- |
| A — `low` | Coupe basse à 0,6 ; vantaux à environ 0,55 | La coupe commune aux murs suffit-elle à lire la porte ? |
| B — `posts` | Montant arrière à 1,96, avant et vantaux coupés bas | Un repère de hauteur suffit-il sans masquer le colon ? |
| C — `frame` | Porte entière à environ 2,06, avec linteau et cassettes | L'occultation d'une porte complète reste-t-elle acceptable ? |

La première version B conservait les deux montants hauts ; celui de devant cachait
une partie importante du colon. L'essai final coupe ce montant avant. Cette coupe
asymétrique est dessinée pour l'orientation de la porte de départ : elle ne définit
pas encore une règle générale de coupe qui s'adapterait à tous les murs et placements.
La variante entière garde ses volumes complets pour rendre son occultation visible
dans la comparaison, sans déplacer artificiellement le colon ou la caméra.

Lors de cette comparaison, le modèle contenait neuf objets mesh rigides, trois os communs et deux textures
du kit mural packées. Les variantes se choisissent par `body/low`, `body/posts` et
`body/frame`. Une animation commune translate chaque feuille de 0,48 unité locale
vers son logement ; les UV restent attachées au modèle. Baie nominale 0,94, minimum
au rebord environ 0,932, étudiée uniquement pour un span de 1.

La source Blender reste dans Art ; `exports/door-cutaway-study` est une banque
ignorée par Git que le diagnostic charge directement. Le jeu ordinaire ne charge
pas cette banque et conserve sa porte. `DoorModelStudy` réutilise le lecteur, les
clips et le renderer des autres modèles, sans nouveau pipeline d'assets.

Pour reproduire les captures depuis TheEnd, utiliser les paramètres du contrôle
précédent et ajouter `THEEND_DOOR_STUDY=low|posts|frame` ainsi que
`THEEND_DOOR_STUDY_BANK=C:\workspace\TheEnd-Art\exports\door-cutaway-study`.
Le diagnostic exige `THEEND_DOOR_CLEARANCE` et `THEEND_SHOT`, et refuse un span autre
que 1. Retirer ces variables pour retrouver le lancement normal. Le script local
`.artifacts/door-clearance/capture.ps1` accepte `-Study`, `-Pose` et `-Suffix`.

Validation : source sauvegardée, export et comparaison avec Blender réussis
(erreur maximale de déformation environ 3,73×10⁻⁸), client Debug compilé sans
avertissement ni erreur. Captures natives fermée/ouverte de chaque variante à
examiner dans la planche. Les poses restent fixes et ne constituent pas un test
de navigation, de collisions, de construction ou de modding.

## Prompt initial de la proposition générée écartée

```text
Use case: precise-object-edit / stylized-concept.
Create a careful two-option art-direction comparison for a small sliding spacecraft door in this specific colony game. This is a concept paint-over for later Blender modeling, NOT a new wall kit.

INPUTS:
Image 1 is the real game screenshot. It is authoritative for the CAMERA, exact wall profiles, floor tiles, door footprint, existing wall junctions, scale, and restrained dark palette. The existing sealed door is centered near pixel (960,420) in this 1920x1080 image, between the large room on the left and a short corridor on the right. The door lies in a NORTH-SOUTH wall, the passage runs EAST-WEST, and the two leaves slide north/south within the wall.
Image 2 is the selected WALL MATERIAL REFERENCE. It supplies fine worn steel details, layered thin profiles, recessed channels, localized edge abrasion, sparse aged copper and rivets. It must NOT override the layout or shape of the real game walls.

OUTPUT:
One landscape comparison image, two equally sized side-by-side closeups, labeled only "A" and "B". Each panel is a tight enlarged crop of the SAME actual passage around (960,420), roughly the original screenshot rectangle x=845..1095, y=315..515. Preserve the actual surroundings and wall construction in both panels. Retain several real floor tiles around the door so scale is obvious. Remove the surrounding game UI by cropping, not by inventing a new room. Do not rotate the scene to a cinematic angle. Match the game's overhead cutaway projection exactly.

CHANGE ONLY the small door body and its receiving jambs, including the already chosen two welded crossbars. Make the door feel like a purpose-built component of the EXISTING wall system, materially richer and more carefully designed than the crude current ladder of strokes.

A — folded steel leaves, compact machined receivers. Two broad solid weathered steel leaf masses with quiet asymmetrical pressed geometry, restrained tapering bevels and one central meeting seam. Layered end receivers terminate the existing narrow wall profiles naturally. Quiet charcoal blue-gray steel with soft hand-painted wear and edge-lighting, small exposed mechanism only inside the receiver.
B — heavier but equally compact overlapping armor skins over two rigid sliding leaves. A slightly stepped inner meeting joint, small inset reinforcement plates, recessed catches at the ends, mild corner chamfers. Stronger silhouette and material depth while keeping exactly the same footprint and wall profile. NOT a vault, iris, rolling shutter, grill or giant pressure airlock.

BOTH keep the approved welded crossbars: exactly two short straight weathered steel straps across the moving leaves, anchored to the fixed receivers with localized dull weld scars. Their axes follow the original door mechanics: they bridge the seam in the sliding direction. No X-shaped brace, no glowing welds, no reddish ornamental frame.
Maintain the existing cut height and implied volume. Do not add a tall lintel, large square portal, full-height front elevation, white caps, chunky concrete cubes, pebbled surfaces, futuristic neon, UI glyphs, ornate warning stripes, windows, colored outline boxes, dense greebles, illustrative lighting or atmospheric fog. Metal plates dominate; mechanisms and rivets support their construction.
The viewer must immediately recognize the REAL GAME WALLS. Preserve their thin layered metal rims, narrow light scratches, channels, copper runs, and floor junctions. Do not replace them with generic slab walls. Detail only the door and its immediate receiver connection.
Polished dark hand-painted industrial science fiction matching the supplied references, readable material planes, modest contrast.
```

## Correction de l'axe

```text
Edit this exact comparison image. Preserve ALL surrounding game walls, floors, debris, lighting, crop, labels A/B and overall art style exactly. Correct ONLY the MECHANICAL AXIS inside each small door footprint; it currently has the wrong direction for the actual game passage.

The walkable passage goes LEFT to RIGHT across the picture. The structural wall containing the door runs NORTH to SOUTH (up/down). Therefore fixed receivers belong at the NORTH and SOUTH ends of the small door footprint, NOT on its west/east sides. There are two solid sliding leaves: the upper leaf retracts UP into the northern wall, and the lower leaf retracts DOWN into the southern wall.

In BOTH panels:
- relocate the compact fixed receiving jambs to the TOP and BOTTOM of the small square door footprint, naturally terminating the existing north/south thin layered wall profiles;
- the seam dividing the two closed leaves is HORIZONTAL across the middle of the footprint; A has a simple horizontal meeting seam, B a shallow stepped horizontal meeting seam;
- the two chosen WELDED CROSSBARS must now be VERTICAL strips, one to the left and one to the right of the center, each extending up/down from the north receiver to the south receiver. They bridge the horizontal seam. Keep dull steel, subtle rust and welded rather than merely bolted attachment;
- retain the A versus B distinction of broad quiet folded steel versus subtly reinforced overlapping armor;
- keep the door's original small footprint, elevation and proportions. Do not add a complete portal, head-on elevation, extra components or new wall sections.
The rest of the image is locked. This is just an orientation correction, no style change.
```
