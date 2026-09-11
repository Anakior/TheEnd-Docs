# Colons : portrait, modèle 3D et carré

Le mode sprite utilise une banque 3D commune pour les colons. Le mode vectoriel conserve
les carrés et leurs initiales. Les deux affichages lisent les mêmes personnages et les mêmes
positions ; changer de rendu ne change ni la simulation ni une sauvegarde.

Le mode sprite utilise aussi le cryopod 3D validé, avec sa vitre coulissante et sa
silhouette anonyme. Ce raccord n'ajoute pas de nouvelle mécanique, de nouvel écran
de création ou de gestionnaire de mods.

## Une seule apparence enregistrée

`AvatarComponent` reste la recette de référence : rig, cheveux, barbe, tenue, couleurs et
détails du portrait. `ColonistFactory` valide cette recette avec `AvatarCatalog` avant de
l'attacher au personnage. Le créateur et les sauvegardes emploient ce même contrat.

`ActorPresenter` transmet la recette sans nouveau tirage. `ActorAppearanceCatalog` traduit
ses identifiants en pièces de la banque. Les couleurs de peau, de cheveux et d'iris viennent
du catalogue et des opérations déjà utilisés par les portraits.

La banque couvre les deux silhouettes, les 24 coiffures, les huit barbes et les six tenues
adaptées à chaque silhouette. Les petites variations de visage, sourcils, bouche et cicatrices
restent portées par le portrait détaillé ; le modèle est destiné à la lecture de loin.
L'approbation artistique des nouvelles pièces reste à Ludovic.

## Où lire et modifier le code

Tous les chemins ci-dessous sont relatifs au dépôt TheEnd.

| Besoin | Point d'entrée |
| --- | --- |
| Choix de création et compatibilités | `TheEnd.Core/Resources/avatar.json`, `TheEnd.Core/Colonists/AvatarCatalog.cs` |
| Recette enregistrée | `TheEnd.Core/Components/AvatarComponent.cs` |
| Recette vers pièces 3D | `TheEnd.Client/Assets/models/colonist/appearance.json` |
| Résolution et couleurs | `TheEnd.Client/Renderer/Actors/ActorAppearanceCatalog.cs` |
| Présentation par personnage, retour au carré | `TheEnd.Client/Renderer/Actors/ActorPresentation.cs` |
| Direction et phase de marche | `TheEnd.Client/Renderer/Actors/ActorMotion.cs` |
| Projection sur la grille et dimensions | `ActorModelCamera.cs`, `ActorVisualMetrics.cs` dans le même dossier |
| Dessin des personnages | `TheEnd.Client/Renderer/Actors/ActorModelRenderer.cs` |
| Chargement et rendu communs aux modèles | `TheEnd.Client/Renderer/Models3D/` |
| Ordre des couches de la scène | `TheEnd.Client/Composition/GameFrameRenderer.cs`, `SpriteDeckBackend.cs` |

Les sources éditables restent dans `TheEnd-Art/characters/colonist/colonist.blend`.
Les exports intermédiaires restent dans `TheEnd-Art/exports/`, hors Git. La banque installée
dans `Assets/models/colonist` est utilisée à la fois par le jeu et par le laboratoire natif.

Les banques installées contiennent les manifestes, les buffers et les textures utilisés
par le client. Les rapports d'export et de validation restent dans `TheEnd-Art/exports/` ;
ils ne sont ni installés ni livrés avec le jeu. Le manifeste conserve les empreintes
de la source Blender et de l'exporteur pour retrouver leur provenance.
Les textures identiques sont partagées entre matériaux, sans fusionner leurs teintes
ou leurs propriétés de transparence.

## Retoucher ou ajouter une variante

Pour retoucher une pièce existante : ouvrir le `.blend`, modifier les formes, la peinture ou
l'animation, puis sauvegarder. L'export lit le fichier sauvegardé sans le reconstruire.

Depuis TheEnd-Art :

```powershell
.\tools\models\build-model.ps1 -Source characters/colonist/colonist.blend -InstallAs models/colonist
```

Pour ajouter un choix :

1. Définir son identifiant et ses compatibilités dans le catalogue de création et ses assets de portrait.
2. Ajouter les pièces Blender avec `model_part` et `model_variant` explicites. Plusieurs meshes
   peuvent appartenir à une même variante. Ils utilisent le rig commun et ses poids.
3. Ajouter le lien entre identifiant de création et variante dans `appearance.json`.
4. Exporter, valider, puis vérifier la variante dans le jeu aux zooms usuels et pendant la marche.

Il n'y a pas de branche de dessin C# à ajouter pour chaque coupe ou tenue. Une anatomie
supplémentaire demande une source liée à un squelette compatible : elle peut réutiliser ses
animations, comme les deux corps actuels. Un nouvel état animé demande son clip et son raccord.
Un choix sans correspondance ou une ancienne recette absente garde un carré et produit un
diagnostic. Une pièce référencée mais absente de la banque, ou un export invalide, échoue au
chargement avec une erreur explicite. Les tests vérifient la couverture de tous les choix actuels
du créateur ; ajouter un choix impose de compléter son raccord.

## Positions, animation et interactions

La position affichée vient de `ActorWorldPosition`, déjà utilisé par le clic et la simulation.
À **1×**, un colon parcourt **3 cases par seconde** sur un axe, en sprite comme en vectoriel.
`ColonistMoveSystem.TicksPerStep` vaut 20 à 60 ticks/s ; une diagonale prend 28 ticks.
Ce réglage réduit la vitesse de déplacement de 40 % par rapport aux 5 cases/s précédentes,
sans ralentir l'horloge du monde. Les portes conservent leur durée liée au pas : un pas
pour une porte ordinaire, deux pour une porte pressurisée.

Le cycle de marche avance selon la distance réellement parcourue et le `stride` du clip,
avec un coefficient visuel de **0,5** dans `ActorMotion`. Sur un déplacement horizontal
à 1×, le clip actuel décrit environ **1,16 cycle par seconde**. Ralentir le déplacement
ralentit donc les jambes dans la même proportion, sans modifier le fichier Blender.
La distance projetée tient compte de l'axe vertical. Ce réglage reste une calibration
visuelle à juger en jeu ; les appuis ne sont pas physiquement verrouillés au sol.
Redessiner la même position ou mettre en pause n'avance pas les jambes. La phase ne repart
pas à zéro à chaque case. Un changement de monde ou de pont réinitialise l'historique local.

La caméra orthographique place les pieds sur la grille 2D. Elle suit la zone visible pour
rester valide loin de l'origine. Le supersampling ne change pas l'échelle logique.

L'export calcule `clipBounds` pour chaque pièce et animation. Le client utilise les bornes des
pièces sélectionnées pour les clics, la sélection et les bulles, plutôt que la largeur des bras
dans la pose de référence du squelette. Un corps mort est posé au sol ; les teintes d'état partagent
la grammaire du carré. Les personnages encore contenus dans une capsule gardent son affichage.

## Cryopods dans le jeu

La source reste `TheEnd-Art/objects/cryopod/cryopod.blend`. Le jeu et l'onglet
**Cryopod** du laboratoire chargent la même banque canonique dans
`TheEnd.Client/Assets/models/cryopod`, avec les mêmes pièces, clips et matériaux.
Depuis TheEnd-Art, installer une retouche avec :

```powershell
.\tools\models\build-model.ps1 -Source objects/cryopod/cryopod.blend -InstallAs models/cryopod
```

Le remplacement s'applique en mode sprite aux capsules `Sealed` et `Open`, avec
une empreinte de 1 × 2 orientée nord/sud ou de 2 × 1 orientée est/ouest. Les états
détériorés, les empreintes non prises en charge et l'absence de banque conservent
le rendu 2D. Le mode vectoriel garde sa présentation existante.

La vitre coulisse vers les pieds ; son alpha de **0,65** laisse lire une silhouette
commune sans révéler le visage ni l'apparence du colon. La présence vient des
`BerthClaimComponent` dont `Contained` vaut vrai, transmis par `FixturePresenter`.
`OccupantSoul` garde l'historique de la cryogénie et ne prouve pas qu'un corps est
encore dans la capsule. L'ouverture suit `PodOpeningView`, calculé depuis le réveil
dans la simulation : le rendu ne possède pas de minuterie indépendante. Une capsule
`Open` sans ouverture en cours est entièrement ouverte.

`Renderer/Fixtures/CryopodPresentation.cs` sépare les capsules 3D du mobilier 2D
et projette leurs bornes. Ces mêmes bornes servent au clic dans `Input/WorldHitTester.cs`,
à l'encadrement dans `UI/GameHudRenderer.cs` et au filtrage des capsules hors champ
dans `Composition/SpriteDeckBackend.cs`.

`Renderer/Fixtures/CryopodModelRenderer.cs` partage les meshes, textures et buffers GPU
chargés une fois pour toutes les capsules. Chaque instance fournit sa position,
son ouverture et sa présence. `GameFrameRenderer` exclut les capsules remplacées du
cache 2D et leur vitre de la passe 2D. La révision de `CryopodPresentation` invalide
`FixtureFrameCache` quand l'ensemble remplacé change, notamment lors d'une bascule
sprite/vectoriel ; la progression de l'ouverture seule ne reconstruit pas ce cache.

## Occlusion et cache

Le mode sprite utilise par défaut les murs en volume avec la coupe validée de 0,6 unité.
Leur profondeur vient des façades et du dessus réellement dessinés, décrits plus bas.

Dans le mode sprite plat conservé pour comparaison, les murs et les portes 2D fournissent
au masque de profondeur les triangles et quads qu'ils dessinent réellement. Les ouvertures
restent ouvertes. Le masque n'extrude pas des cases de
collision dans du vide qui ne serait pas peint. Chaque bande forme une faible façade ancrée
sur son bord côté écran : sa profondeur vient de son épaisseur peinte, jamais de sa longueur.
Les coins obliques restent bornés. Cela évite qu'un mur arrière coupe la tête d'un colon devant
lui. C'est une convention de présentation pour le décor 2D, pas une reconstruction physique
des murs en 3D.

Le mobilier prête ses buffers déjà mis en cache pendant la frame. La hauteur visuelle est
stockée dans `Z` : les corps de meubles utilisent une hauteur commune de 0,65 ; leurs ombres
de contact restent à zéro. `MarkHeightScope` identifie ces ombres dans les skins. Le dessin
couleur ignore cette hauteur et conserve les mêmes pixels. Cette valeur ne définit aucune
hauteur physique dans la simulation.

Pas de nouveau cache de pont : les plans publiés et les buffers visibles restent les sources.
La collecte des masques réutilise sa mémoire ; le prêt ne copie pas les buffers et ne change
pas leur propriétaire. Seule la cible de scène possède profondeur et stencil. Les cibles
intermédiaires et l'interface gardent leur fonctionnement 2D.

Les meshes et textures 3D sont chargés une fois et partagés. Chaque personnage ne conserve
que son apparence résolue et sa pose. L'éclairage est celui du client, avec une ombre projetée
simplifiée ; ce raccord ne reproduit pas tous les matériaux ni les lumières de Blender.

## Vérifier une modification

Les tests de `Renderer/Actor*`, `FixtureOcclusionTests`, `Display/ActorPresenterTests` et
`Input` couvrent les recettes, la phase de marche, la projection, les états, les clics et les
bulles. L'export vérifie aussi les bornes animées et compare le skinning à Blender.

Une retouche graphique exige une vérification dans le jeu : femme et homme, coiffure longue,
barbe, marche puis pause, bord de meuble, porte ouverte et fermée, changement de pont, zoom,
sélection et bulles. En développement, **R** conserve la bascule sprite/vectoriel existante.
Les captures automatiques utilisent `THEEND_BACKEND=sprite` ou `vector`.

Le relevé conservé pour l'intégration des colons compte 4 357 tests réussis, dont la cadence
sur une seconde au rythme réel de la simulation. Les captures conservées montrent
la [sélection en mode sprite](reference/colonist-integration/mode-sprite.png), le
[mode carré](reference/colonist-integration/mode-carre.png) et une
[conversation réelle](reference/colonist-integration/conversation.png). Elles décrivent l'état
testé ; elles ne constituent pas une nouvelle référence artistique approuvée.

Pour les cryopods, vérifier aussi les quatre orientations, les états vide/occupé,
l'ouverture puis la pause, la sélection près des débords, l'occultation par les murs,
le bord de l'écran et la bascule sprite/vectoriel. Le relevé ci-dessus concerne les
colons et ne constitue pas un résultat de validation de ce raccord des cryopods.

Le catalogue prépare l'ajout de contenu ; la découverte, la priorité et le chargement de
packs de mods restent un chantier distinct. Ne pas les confondre avec ce raccord de rendu.

## Mesure du laboratoire natif

Sur la RTX 4080 SUPER de la machine d'essai, avec la banque complète, ombres et MSAA4,
le laboratoire 1360 × 900 donne les mesures suivantes. Le détail est dans le
[rapport de mesure](reference/colonist-integration/render-benchmark.json).

| Colons dessinés | Durée moyenne d'une frame | 95e percentile | FPS moyens |
| --- | --- | --- | --- |
| 25 | 1,69 ms | 2,42 ms | 592 |
| 100 | 4,93 ms | 5,59 ms | 203 |
| 250 | 12,32 ms | 14,07 ms | 81 |

Ce sont des cadences observées sur trois secondes après échauffement, hors encodage des images.
Elles incluent le rendu du laboratoire et l'attente du pilote, mais pas la simulation, les
chemins, ni le vaisseau du jeu. Le contour encré y est désactivé, contrairement au jeu.
Elles ne démontrent donc pas 60 FPS en partie avec 250 colons, ni sur un GPU plus modeste.

## Essai isolé de murs en volume

Depuis TheEnd, lancer `scripts/run-actor3d-prototype.ps1 -Walls`. Le même laboratoire natif
propose les onglets **Colons**, **Cryopod** et **Murs**. Le mode Murs montre un pan de cinq
cases, avec son épaisseur réelle, ses plaques, joints et rails. Il reprend `WallArmor`,
`WallRail` et `WallChannel`, ainsi que l'éclairage des colons et leurs ombres projetées.

Les boutons **Coupe basse**, **Mi-hauteur** et **Mur haut** comparent des hauteurs de 0,6,
1,2 et 2 unités. Le clic au sol déplace le colon, le bouton de parcours lui fait contourner
le mur, et **Placer le colon derrière** permet de juger l'occultation. Molette : zoom ;
clic droit : déplacer la vue ; Espace : pause. Ludovic a validé la coupe basse de 0,6 unité
après comparaison dans le jeu. Les deux autres hauteurs restent des variantes de laboratoire.

`Development/Actor3D/WallVolumePrototype.cs` construit cette petite géométrie en code.
Il réutilise quatre buffers, reconstruits uniquement lors d'un changement de hauteur.
Les textures appartiennent à `ActorPrototypeScene`. Le détour utilise la même fonction
d'intersection et de contournement rectangulaire que la capsule. Ce pan procédural n'est
pas un nouvel asset Blender et n'ajoute aucun export à la banque de personnages.

`-Walls -Capture` produit huit captures et un rapport dans `.artifacts/actor3d-prototype/wall-captures` :
devant/derrière aux trois hauteurs, parcours autour du mur, passage oblique près d'un coin.
Pendant les parcours, toute traversée de l'emprise visible fait échouer la capture.
Deux aperçus sont conservés : [devant](reference/colonist-integration/wall-front.png) et
[derrière](reference/colonist-integration/wall-behind.png).

Ce premier laboratoire reste disponible. L'essai suivant utilise les plans du vrai vaisseau.

## Comparer le volume dans le jeu

Depuis TheEnd :

```powershell
.\scripts\run-wall-volume-study.ps1
```

La **coupe de mur à 0,6 unité est validée par Ludovic** et utilisée par défaut en mode sprite,
y compris au lancement ordinaire. Cette hauteur est une coupe visuelle, pas une hauteur de
collision dans la simulation. Le script ouvre ce même rendu en session de développement.
**R** bascule entre sprite et vectoriel ; le changement de pont et les autres commandes
restent ceux du jeu. `THEEND_WALL_VOLUME=0` conserve le rendu sprite plat pour diagnostic ;
`-Mode sprite` dans le script de capture applique cette exception explicitement. La valeur
`1` reste acceptée, mais n'est plus nécessaire. Si la texture d'armure manque, le repli
existant du décor reste disponible avec son diagnostic de chargement.

Le dessus reprend le dessin complet déjà utilisé : matières, rails, encrage et portes
animées. Il est projeté sur un plan surélevé. Les côtés descendent de ce plan jusqu'au sol,
à partir des bords déjà préparés ; le relief ne remplace pas les contours par des blocs de
cellules. La position projetée du dessus se relève naturellement à l'écran, tandis que
les positions de jeu et les empreintes au sol restent identiques.

Points d'entrée dans le dépôt Code :

| Responsabilité | Fichier |
| --- | --- |
| Essai et ordre des passes | `TheEnd.Client/Composition/SpriteDeckBackend.cs` |
| Projection du dessus et façades | `TheEnd.Client/Composition/SpriteWallVolume.cs` |
| Bords des corps préparés, raccords et découpes des passages | `TheEnd.Client/Composition/WallVolumeGeometry.cs` |
| Publication commune de l'encre et des débris | `TheEnd.Client/Renderer/Walls/Skin/SpriteWallOverlayCache.cs` |

La géométrie des côtés est reconstruite lors d'un changement de présentation installée.
Les buffers du volume sont préparés lorsque le mode sprite est affiché ; démarrer en
vectoriel n'alloue pas sa cible de rendu supplémentaire.
Un seul jeu de buffers est conservé, sans deuxième cache de pont. Le dessus utilise une
cible de rendu réutilisée, à la résolution d'anticrénelage courante, avec une marge sous
l'écran. Le dessin mural existant y est exécuté une fois par frame ; il contient les portes
vivantes et n'est pas un nouveau bake permanent par pont. L'encre et les débris partagent
la même publication atomique du cache ; seule l'encre est relevée. Les débris restent au sol.

Le cache de contours du sol ne prolonge une dalle que dans les cellules réellement
traversées par une diagonale. Un simple contact avec un sommet ne compte pas : il ajoutait
une dalle hors du mur, dont seul le bord restait visible comme un trait isolé. Ce calcul
reste commun au sol et à la masse structurelle, en sprite plat comme en volume.

Les passages sont découpés depuis la géométrie déclarée des portes, indépendamment de leur
ouverture courante. Les marques transparentes contribuent à la couleur ; seules les zones
presque opaques du dessus écrivent une profondeur pleine. Les couleurs et le masque du
mobilier précèdent le volume pour permettre son occultation par une façade.

Captures reproductibles, avec le même monde, le même tick et le même cadrage :

```powershell
.\scripts\run-wall-volume-study.ps1 -Capture -Scene home -Mode volume
.\scripts\run-wall-volume-study.ps1 -Capture -Scene home -Mode sprite -NoBuild
.\scripts\run-wall-volume-study.ps1 -Capture -Scene home -Mode vector -NoBuild
.\scripts\run-wall-volume-study.ps1 -Capture -Scene gate -Mode volume -NoBuild
```

`-Scene` accepte aussi `door`, `dome` et `wreck`. `-Zoom` règle le rapprochement des captures
(16 par défaut). Les sorties restent dans `.artifacts/wall-in-game/captures/`.
Les aperçus retenus montrent le [volume en jeu](reference/colonist-integration/wall-in-game.png),
le [même cadrage vectoriel](reference/colonist-integration/wall-vector.png) et
la [serre du dôme](reference/colonist-integration/wall-dome.png).

Le rendu des murs est intégré au mode sprite ; le reste du monde n'est pas entièrement
en 3D. La hauteur uniforme de 0,6 est validée ; les éventuelles transparences et coupes
automatiques restent à décider. Hormis les cryopods pris en charge, le mobilier et les lampes
gardent leur présentation 2D avec une profondeur approchée. Le verre n'est pas une vitre
physique et les portes n'ont pas encore de vantaux
volumétriques. Le coût de la cible supplémentaire reste à mesurer sur les configurations visées.

Les 13 cas de géométrie ajoutés vérifient coordonnées, diagonales, raccords, ouvertures et
découpes de portes. Trois cas supplémentaires vérifient la séparation encre/sol, l'échec
du second upload et les annulations ; les deux couches restent publiées ensemble.
