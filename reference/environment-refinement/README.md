# Herbe fine, eau animée et alignement des spots — 12 septembre 2026

Après la première retouche du dôme, Ludovic trouve l'eau presque immobile et rejette
l'herbe V2 : ses grandes feuilles ressemblent trop à de la végétation haute. Il montre
aussi un cône lumineux décalé par rapport à un spot sur une paroi verticale.

## Version intégrée

- **Herbe courte V3** : nouvelle texture de gazon fin, sans grosses feuilles ni touffes
  hautes. Les lisières progressives de la retouche précédente sont conservées. Échelle
  fixe de 96 pixels/cellule, teinte RGB(174,187,165). Elle reste statique.
  [Capture du jeu](grass-short-v3.png), pont 3, centre (124,146), 48 px/cellule.
- **Eau** : deux petites ondes croisées déforment localement les reflets, avec une variation
  de luminosité douce. Périodes 3,8 s et 5,2 s, reflet 3,1 s ; excursion maximale de
  0,18 cellule. Le mouvement utilise les vrais ticks du jeu, reste stable en pause et
  conserve les coordonnées de rive, la profondeur et l'opacité. Les phases spatiales
  sont préparées une fois ; leur interpolation garde les raccords entre berge et intérieur.
  [Vidéo native, six secondes](water-motion.mp4).
- **Spots** : la lampe était projetée à 0,35 m de hauteur, mais le cône commençait au sol :
  environ 12 px de décalage vertical au zoom 48. Le cône part désormais à la hauteur du
  spot et rejoint le sol sur les 0,8 premières cellules. Les intersections avec les
  obstacles restent calculées dans les coordonnées physiques. Une file réservée aux
  lumières surélevées utilise la caméra des murs et leur profondeur en lecture seule ;
  un mur ou un objet peut donc masquer le flux. Les autres sources lumineuses et le mode
  vectoriel/plat gardent leur passage existant.

Les matières de murs usés et les éclats de la précédente retouche sont conservés.
Ludovic valide ensuite cet aspect (« Oui c’est bon »), puis signale un ralentissement,
une arrivée tardive de l’eau et des trous sous les raccords de murs. La
[passe de correction suivante](../environment-performance/README.md) conserve cette
direction artistique et remplace le calcul CPU de l’animation par son équivalent GPU.

## Preuves

La vidéo est enregistrée dans le vrai `TheEndGame`, seed 12345, pont 3, centre (128,100),
fenêtre 1920×1080, zoom 16. L'hôte ne dirige que le pont et la caméra. Après l'amorçage,
la simulation avance normalement : 80 images sur six secondes, ticks 12420→12780,
une seule position de caméra et une seule version d'eau. Les 80 zones d'eau sont
différentes, la zone de berge sèche est identique sur toutes les images. Les horodatages
réels sont respectés, y compris le premier intervalle de 0,48 s ; cette capture n'est pas
une mesure de la fréquence d'images du jeu.

`water-motion.json` et `water-motion-validation.json` contiennent les mesures. Le helper
temporaire est `.artifacts/environment-motion/native/run.ps1 -Name water-motion-reviewed
-Duration 6`. Il capture le composite final, sans DisplayFrame ni horloge artificiels.

Le [spot vertical avant](../door-lamp-fixes/before-lamp-light-vertical.png) et
[après](../door-lamp-fixes/after-lamp-light-vertical.png) utilisent le même cadrage :
pont 0, centre (105.5,87.5), lampe East seed 194. Les captures East, North et South
contrôlent aussi les meubles voisins et les lampes visibles/cachées sur les diagonales.
Les métadonnées et la provenance des DLL sont conservées dans la
[note de raccord des spots](../door-lamp-fixes/light-alignment.md).

Les tests ciblés et la suite Renderer couvrent l'animation, les raccords UV, la pause,
la hauteur/projection des faisceaux, leur clipping physique et les replis du renderer.
**1 483 tests Renderer réussissent, zéro échec et zéro test ignoré**, après compilation
du Client sans erreur ni avertissement. Le résultat est conservé dans `validation.json`
et `environment-motion-lamps.trx`. Les captures natives sont terminées et inspectées.

L'animation d'eau ajoute un coût CPU à profiler lors de la phase d'optimisation :
la mise à jour locale UV/couleur prend environ 3,4–4,0 ms dans deux vues en Debug,
contre 0,4–0,7 ms pour l'ancien glissement uniforme. La géométrie reste à 98 043 sommets
pour 5 663 cases d'eau. Ces mesures locales ne décrivent pas le FPS global.

## Sources

- `TheEnd-Art/sprite-render/environment-v2/grass-short-v3.png`, prompt complet dans son
  `README.md`, empreintes dans `grass-short-v3-provenance.json`. Création avec l'outil
  Imagegen intégré, copie PNG identique dans `TheEnd.Client/Assets/sprites/materials`.
- `grass-meadow-v2.png` reste uniquement comme historique dans l'atelier Art ; elle a
  été retirée des sources de la banque runtime après le rejet de Ludovic.
- La texture `water-surface-v1.png` n'a pas changé ; l'animation vient de `SpriteWaterSkin`.
- Projection des lampes : `SpriteGlowPlan`, `GlowSkin`, `ISpatialLightSink`,
  `VectorRenderer.FlushSpatialLights` et son appel dans `GameFrameRenderer`.

Pas de modification de Core, des modèles Blender ou des banques de portes/sas/obstacles.
Aucun commit/push Code, Art ou Docs par l'assistant.
