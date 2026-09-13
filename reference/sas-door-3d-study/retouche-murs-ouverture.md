# Sas A — raccord aux murs et stabilité de l'ouverture

**12 septembre 2026 — apparence et ouverture de cette version validées par Ludovic : « C'est bon ! ».**

Cette validation suit la présentation de `sas-a-v2-motion-native.mp4` et concerne
la source SHA `84012115713aa568cb6f888b56c98d648574da4bf0b4d86f5cf1d97e280cc535`.
Ludovic demande ensuite « Implémentes du coup » : [le modèle est désormais intégré
au rendu normal](integration.md). Les preuves de retouche ci-dessous conservent
le contexte du banc externe qui a servi à sa validation.

Ludovic conserve la direction [A « Monobloc facetté »](direction-v2-a-monobloc.png), mais rejette le modèle présenté dans [la première vidéo native](sas-a-motion-native.mp4) : « c'est moche pas du tout ressemblant avec le reste du design des murs » et « ouverture cela tremblote ».

Les gros capots plats et leur trappe arrière se lisaient comme des boîtiers rapportés. Les feuilles perdaient les chanfreins, l'usure et les matières du décor qui faisaient la qualité du concept retenu. La reprise s'appuie sur les peintures existantes du mur et de la porte ordinaire, avec une bouche construite dans la continuité de la couronne et un fond de poche dissimulé sous celle-ci.

## Nouveau résultat natif

[Ouverture et fermeture dans le moteur](sas-a-v2-motion-native.mp4).

| Bande | Fermée | Ouverte |
| --- | --- | --- |
| Verticale, traversée gauche/droite | [Vue native](sas-a-v2-closed-native.png) | [Vue native](sas-a-v2-open-native.png) |
| Horizontale, traversée haut/bas | [Vue native](sas-a-v2-horizontal-closed-native.png) | [Vue native](sas-a-v2-horizontal-open-native.png) |

Les captures intégrales viennent du banc, en 1920 × 1080. La vidéo conserve 120 images à 30 images/s sur quatre secondes, avec le même cadrage que l'essai rejeté : recadrage technique de 400 × 400 à (760,220), agrandi ×3 par voisin le plus proche, encodage H.264. Aucun dessin, texture ou objet n'est retouché dans ces preuves. La vue verticale fermée est l'image 0 de cette séquence ; son JSON de capture décrit cette pose finale également fermée et contient la trajectoire complète.

### Construction retenue pour ce nouvel essai

- Les grandes trappes arrière sont retirées. Les bouches sont compactes ; les couvercles profonds culminent à Z=0,596 sous la couronne du mur à 0,600.
- Les peintures de la porte ordinaire approuvée et les matières existantes `wall-armor-quiet`, `wall-rail-quiet` et `wall-channel-quiet` remplacent le mélange de peinture de cryopod trop uniforme du premier modèle.
- Les grandes facettes sont plus sombres que la face centrale. Le contour comporte des biseaux de 25 à 35 mm, en acier exposé avec des interruptions peintes, intégrés au maillage. Les UV agrandissent les plages d'usure de la peinture existante.
- Le petit contact en laiton est au fond d'un puits à deux niveaux, avec des parois graphite sombres.
- Le nez est un seul solide entre X=0,010 et 0,049 ; la coque commence à 0,050. Les anciens doublons et contours superposés sont retirés. Les solides des caissons profonds sont également réunis pour retirer leurs interfaces enterrées.

Source sauvegardée : `TheEnd-Art/objects/sas-door/sas-door-a.blend`, SHA **`84012115713aa568cb6f888b56c98d648574da4bf0b4d86f5cf1d97e280cc535`**. Trois os, variante `body/faceted`, deux vantaux rigides, course ±1,480 en 2/3 s. Leur enveloppe reste X=±0,008..1,486, Y=±0,470, Z=0,018..0,588. Le nez acier ouvert reste visible à ±1,490. La source compte 2 317 sommets / 4 450 triangles ; l'export compte 31 sous-maillages et 15 matériaux. Les caissons ont pour limites X=±3,042 et Y=±0,6395 ; le sommet du récepteur atteint Z=0,658.

L'export commun est validé contre Blender : trois os, erreur maximale 1,78814 × 10⁻⁷ m. Les captures et contrôles finaux sont répertoriés dans [le rapport natif](sas-a-v2-native-check.json). Aucun correctif C# de cadence, de caméra ou de profondeur n'est nécessaire ; le code du banc et du rendu n'a pas changé pendant cette retouche. La suite de 1 739 tests C# de la livraison précédente reste son résultat historique et n'est pas présentée comme relancée pour les seules retouches du `.blend`.

L'[audit final des surfaces](sas-a-v2-surface-audit.json) ne retrouve aucun doublon coplanaire à aire positive, dans les vantaux comme dans les caissons. Les 41 poses et le volume balayé restent conformes. Dans les [120 images finales](sas-a-v2-motion-review.json), les deux bouches sont strictement identiques pixel par pixel ; la variation moyenne du nez suivi sur les poses 19 à 35 reste inférieure à 0,572/255. Les 24 paires de poses égales à l'aller et au retour sont identiques. La [planche de contrôle](sas-a-v2-motion-review.png) montre les images 19 à 22. Ces mesures concernent le flash signalé, sans prétendre supprimer toute variation normale des pixels d'un objet texturé en déplacement.

## Cause du clignotement

Dans la banque rejetée, source SHA `ac9619d3b8c567571bc7f498e6b259bfa6ac8170c6ef5082ccda94577edc89dc`, la coque graphite et le nez peint avaient chacun une grande face terminale exactement sur le même plan X=±0,010. L'audit indépendant des triangles exportés mesure **0,38472 unité² de recouvrement par vantail, avec un écart nul**. Le dessus acier et le nez se doublaient aussi à Z=0,588.

Ces faces de couleurs différentes se disputent le même pixel et la même profondeur. Pendant le déplacement, la face terminale alterne entre clair et sombre, ce qui donne l'impression de tremblement. Les images natives 19 à 22 rendent le défaut manifeste.

La caméra et la cadence ne sont pas la cause de cette alternance : les poses fermées répétées, les poses ouvertes répétées et les 19 paires ouverture/fermeture à ouverture égale donnent des captures identiques pixel par pixel. La correction appartient à la géométrie du modèle. Changer la vitesse ou les réglages globaux du moteur masquerait le diagnostic.

L'ancien audit de 41 poses vérifiait le rig, la course et le dégagement dans les poches. Il ne cherchait pas les surfaces mobiles coplanaires entre elles ; il ne validait donc pas l'absence de clignotement visuel. Les anciens tests C# restent un résultat technique historique, pas une approbation du rendu.

### Essai causal dans le moteur

Une copie diagnostique de la banque rejetée retire exactement quatre triangles : une face graphite cachée sous le nez de chaque vantail. Sommets, UV, matières, textures et animations restent identiques octet par octet ; seuls deux buffers d'indices et leurs compteurs changent. Les vues natives 19 à 22 perdent alors les grandes bandes sombres alternées.

[Comparaison native avant/après retrait des quatre triangles](sas-a-v2-cause-comparison.png) · [rapport causal](sas-a-v2-cause.json).

Dans une même zone suivie sur la face mobile, la moyenne RGB de la frame 21 passe de (30,28 ; 38,26 ; 42,99) à (73,52 ; 81,19 ; 82,57), retrouvant la teinte de la frame 20 (73,55 ; 81,16 ; 82,58). Les frames 19/20 de cette zone restent inchangées par l'essai. Le défaut est donc bien lié au recouvrement, pas à une recoloration générale ou à une nouvelle trajectoire. La copie diagnostique reste dans le cache ; la correction livrée doit venir du `.blend` sauvegardé, puis de l'export commun.

## Reprise et conservation

La source de travail reste `TheEnd-Art/objects/sas-door/sas-door-a.blend`. Retoucher ce fichier sauvegardé, puis utiliser l'export commun ; ne pas relancer le générateur initial. Les preuves de la version rejetée restent conservées sous leurs noms originaux. Les nouvelles preuves sont nommées `sas-a-v2-*` pour distinguer cette retouche de l'historique.

Le banc externe reste `TheEnd/scripts/run-sas-study.ps1`. Exporter depuis Art avec `tools/models/build-model.ps1 -Source objects/sas-door/sas-door-a.blend`, puis depuis Code lancer `scripts/run-sas-study.ps1 -Mode motion -Axis vertical -NoBuild`. Les modes `closed` / `open` et l'axe `horizontal` donnent les autres vues. L'installation autorisée ensuite est décrite dans [le compte rendu d'intégration](integration.md). Les sources et banques approuvées de porte ordinaire, rocher et débris conservent leurs empreintes. Aucun commit ou push Code, Art ou Docs par l'assistant.
