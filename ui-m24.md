# Interface M2.4 — état de reprise

L'[inventaire de l'interface globale dans Atlas](https://github.com/Anakior/knowledge-base/blob/main/content/theend/meta/plan-interface-globale.md) décrit les besoins futurs du jeu,
leur place proposée dans ce châssis et les arbitrages à mener avec chaque système. Il distingue
les surfaces déjà présentes des évolutions conçues ; il ne modifie pas le scope livré ci-dessous.

## Direction visuelle

L'arbitrage de reprise de Ludovic prend **`reference/ui-jeu-etude-b.png` comme cible finale de
composition et de matière de l'UI**. Pour les bulles, la référence est **`reference/ui-jeu-fusion.png`** :
parole en cadre fin avec queue, pensée en italique sans cadre avec une traînée de points.
Cette instruction remplace l'ancienne priorité générale donnée à Fusion dans le plan de l'Atlas.
La fiche détaillée est dans [les références](reference/README.md).

Le contrôle artistique de P10 est **rouvert** après comparaison avec la référence : la première
version jouable avait des aplats trop lisses et des contours trop propres. Le matériau attendu est
un métal charbon patiné, avec un grain discret et des cadres fins usés portant des touches de
rouille. La validation des comportements et de la géométrie ne vaut pas validation de cette matière.

Le HUD utilise désormais une matière commune : fond charbon mat et cadre métallique fin,
bruni et localement écaillé. `HudMaterial` réemploie les champs peints `wall-armor-quiet.png`
et `floor-metal-oxidized.png` du renderer, sans modifier leurs sources. Il prépare deux textures
au chargement : grain de fond et profil de bord patiné. Les coins gardent leur taille ; les
filets et les fonds sont tuilés à l'échelle de l'interface, sans étirer le grain sur les grands
panneaux. La matière reste ancrée au panneau et ne dépend ni du temps ni de la caméra.

Roster, inspecteurs, dossier, journaux, réglages, alertes, menu d'ouverture, boutons et cadres
des portraits partagent cette finition. Les repères de sélection restent cyan. Les paroles
conservent environ 70 % d'opacité et leur placement existant ; les alertes et le menu d'ouverture
gardent leur fond opaque pour masquer les textes inférieurs.

Les portraits finalisés restent les assets du jeu. L'ambre indique une personne vivante, le cyan
la sélection ou l'interaction ; les personnages sélectionnés et survolés ont un cadre carré.
Le monde garde sa lumière : aucun voile global ne sert à faire ressortir les panneaux.
Les valeurs fictives des images, comme l'alimentation ou une usure de caisson, ne deviennent pas
des champs du jeu.

Les initiales des tokens suivent leur position continue, sans arrondi au pixel. Leur atlas dédié
est préparé au chargement avec des marges transparentes et des versions réduites filtrées : les
traits restent stables pendant les déplacements, y compris au dézoom maximal. L'atlas des glyphes
de grille et l'anticrénelage global conservent leur réglage.

## P5 — roster, inspecteurs et dossier

La version jouable expose le roster des personnes révélées, les liens de famille, les portraits,
les états et les jauges HLT/HNG/RST/MND. Le filtre « Vivants seulement » est désactivé par défaut.
Les cartes sont paginées lorsque l'espace ne suffit plus. Une Soul disparue du monde reste
inspectable dans la mémoire ; un mort ou un tourné ne reçoit jamais d'ordre.

- Un clic sur une carte sélectionne la personne ; un double clic centre son porteur actuel,
  en changeant de pont si nécessaire.
  Sélection, désélection et ouverture/fermeture des panneaux ne déplacent pas la caméra.
- La fiche compacte ouvre le dossier. Celui-ci présente identité, besoins, esprit, personnalité,
  phobies, relations qualitatives et faits connus récents. Les données absentes restent absentes.
- La molette, Page précédente/suivante et les boutons du dossier défilent son contenu ; Échap
  ferme d'abord le dossier puis l'inspecteur. Le focus clavier reste visible.
- Les inspecteurs adaptent leurs champs au type d'objet : occupant pour les cryopods et couchettes,
  provenance historique pour les cryopods, contenu pour les rangements. Le contenu d'un rangement
  reste « Inconnu » tant qu'aucun inventaire simulé ne permet de le décrire ; il n'est pas déclaré
  vide à partir de l'absence d'occupant. Les autres équipements n'affichent que leur état.
- Le dossier n'est pas omniscient : un fait pré-jeu doit être découvert par la colonie et connu
  de la personne inspectée avant d'être présenté. La politique de visibilité est celle du journal.

Le registre durable de personnes existant dans Voice conserve maintenant Avatar et dernier pont.
Les projections UI sont reconstructibles. **WorldSave v22** valide ces données avant toute mutation ;
les versions précédentes sont refusées, conformément à la politique du projet, sans migration.
Le profil de portrait `memorial` désature le résultat pour les morts, sans modifier leur recette.
Les portraits sont préparés sur le worker existant puis transférés sur le thread graphique.
Au démarrage, les recettes des fondateurs sont préparées dans les deux formats réellement consommés :
128 px pour le roster et l'inspecteur, 256 px pour le dossier. Le premier écran jouable attend leur
publication complète, en parallèle de la préparation du plan, avant tout tick de simulation.
Un échec de portrait est journalisé et laisse les initiales visibles ; il ne bloque pas le chargement.
Les portraits qui deviennent nécessaires en cours de partie restent préparés en arrière-plan.
La santé d'un cadavre reste absente : son ancienne intégrité ne devient pas une jauge de vie.
L'intégrité actuelle des tournés reste lisible. Les jauges HLT et MND utilisent la même échelle
de 0 à 100 sur les cartes et dans le dossier ; les numéros de pont commencent à 1 partout dans l'UI.

La disposition et les rectangles de clic sont communs aux backends vectoriel et sprite. Le texte
du dossier est mesuré avec les vraies polices ; les lignes hors de la zone visible ne sont pas
dessinées et le contenu est découpé par un scissor.
Le dossier masque les autres panneaux pendant sa lecture et conserve le monde visible autour.
Les projections réutilisent leurs références quand les valeurs visibles restent identiques ; une
variation réelle est publiée au tick suivant. Le dossier conserve les paragraphes déjà mesurés :
changer une jauge ne reformate pas les 64 faits récents.

## P6 — paroles et pensées dans le monde

Les nouveaux événements Voice du ledger alimentent maintenant les bulles du HUD commun aux deux
backends. Leur texte vient de l'événement écrit ; leur ancrage suit la Soul de la personne dans
la frame du monde. Seule une personne visible et dégagée des panneaux peut porter une bulle.

- La discussion reprend le cadre charbon discret, le filet fin et la queue de Fusion. Son fond
  et sa queue sont semi-transparents (environ 70 % d'opacité), le texte reste lisible. La pensée
  utilise la vraie police italique, **sans cadre ni capsule**, avec trois points vers son porteur
  et une ombre locale des caractères. Aucun nom ni relevé d'état n'est ajouté à la réplique.
- Trois bulles au maximum sont présentées, avec une seule réplique par personne. Les nouvelles
  discussions choisissent leur place avant les nouvelles pensées, en respectant les bulles
  déjà en lecture. Une pensée ne coupe pas
  une discussion. Une nouvelle réplique remplace la précédente du même locuteur, sous réserve
  de cette priorité. Quand le budget est plein, une discussion peut remplacer une pensée ;
  à priorité égale, les lignes déjà en lecture conservent leur place.
- La durée est calculée depuis le tick de parole : `120 + 3 × longueur du texte`, bornée de
  180 à 600 ticks. À 60 ticks par seconde de simulation, cela représente 3 à 10 secondes.
  La pause suspend donc aussi leur expiration. Les deux tours les plus récents d'une même
  conversation peuvent coexister ; le précédent reste au plus 90 ticks après la réponse,
  sans dépasser son expiration initiale.
- Chaque texte est mesuré avec la police réellement dessinée et l'échelle UI demandée, de
  100 à 200 %. Il occupe au plus trois lignes. Les retours explicites comptent ; un mot trop
  large ou une quatrième ligne renvoie l'événement à l'historique seul, sans réduction de
  police, troncature ni points de suspension.
- Chaque bulle conserve l'ancrage choisi à son apparition et suit le déplacement de son locuteur.
  Les autres colons peuvent passer sous son fond transparent : leur mouvement ne déplace pas
  la bulle. La sélection et le survol ne changent pas non plus son ancrage.
  Les autres bulles interviennent seulement dans le choix initial, sans déplacer celles déjà
  en lecture. Les limites de l'écran et les panneaux restent respectés ; si la bulle ne peut
  plus être présentée à cet endroit, la ligne reste dans l'historique.
  Les bulles n'ont aucune zone de clic : le monde reste interactif à travers elles.

Le dossier laisse les bulles des personnes visibles dans le monde s'afficher à côté de sa fiche.
Seul son rectangle est alors un obstacle : le roster, l'inspecteur et l'horloge masqués ne réservent
plus d'espace. Ouvrir ou fermer le dossier ne retire pas une réplique dont le locuteur et l'ancrage
restent visibles. Une ligne hors écran,
écartée par le budget, expirée ou impossible à placer n'attend pas un prochain cadrage : elle
ne rejoue pas après un déplacement de caméra, un changement de pont ou la fermeture d'un panneau.
Le chargement d'une partie et le rattachement à un nouveau ledger ne rejouent pas non plus les
événements déjà écrits. Cette présentation temporaire ne supprime aucun événement du ledger ;
le journal complet permet maintenant de retrouver ces lignes.

Les trois caches de texte sont conservés entre les frames. Ils ne refont leurs mesures que
si le contenu, la largeur, l'échelle ou la police change ; le placement réutilise ses buffers.

## P7 — journal complet et attention critique

`J` ouvre le journal de la colonie, également accessible au-dessus du roster. Ses huit filtres
séparent les paroles, pensées, relations, découvertes, ruptures, faits de colonie et passé connu.
La page visible est mesurée et défilée ; les pages précédentes conservent toute l'histoire sans
plafond de 128 faits. Les liens Personne, Lieu et Fait d'origine ouvrent les vraies projections,
en changeant de pont si nécessaire. Les événements techniques ne deviennent pas des lignes humaines.
Un fait pré-jeu reste invisible tant que la colonie ne l'a pas découvert.

Une personne qui vacille dispose de 300 ticks de grâce avant le premier tirage de rupture. Le
runner cède à l'entrée de l'épisode et abandonne le retard accumulé à l'ancienne vitesse ; une
alerte doit atteindre le rendu avant que la simulation reprenne. La vitesse demandée revient à
1×, la pause reste telle que le joueur l'a choisie. La vitesse précédente n'est jamais restaurée
automatiquement. L'alerte reste jusqu'au bouton VU ; le roster conserve ensuite l'indication tant
que l'état persiste. Les urgences simultanées sont regroupées avec accès aux personnes concernées.
Une rupture actualise l'alerte ; une récupération, une mort ou une transformation retire l'état
périmé. Le chargement reconstruit l'attention depuis les composants actuels.

## P8 — liens perceptibles et épithètes

Une proximité nouvelle entre deux personnes liées par une relation Strong peut laisser un signe
bref ; seuls les vrais événements
de formation ou de dégradation d'un lien produisent une floraison. Ces signes cèdent devant les
paroles et les urgences. Un changement de caméra ou un chargement ne les rejoue pas. Le modèle
relationnel existant, ses nombres et son rythme restent la vérité mécanique.

Six épithètes sobres sont attribuées à partir de faits connus et réels : Ouvre-chemin, Mémoire
des absents, Présence familière, Confiance blessée, Fidèle aux absents et De retour. Chaque gain
est unique pour une personne et un titre, annoncé dans le journal avec sa cause. Le nom reste
affiché ; une seule épithète l'accompagne. Le dossier conserve tous les titres gagnés, leurs
causes et le choix d'un titre épinglé ou automatique. Les choix et les gains survivent au
chargement dans le ledger. Voice peut évoquer une réputation lorsqu'elle connaît son origine.

## P9 — les dormants existent avant leur réveil

La génération peuple certains cryopods scellés avec des personnes complètes. Avant la fin de
leur réveil, elles sont absentes du roster, de la mémoire publique et des portraits. Le caisson
ne révèle que la présence vivante et le nom ; aucun trait, besoin ou niveau de corruption ne fuit.

Sélectionner un colon disponible puis faire un clic droit sur un caisson dormant propose
**OUVRIR LE CRYOPOD**. Le colon doit rejoindre un accès praticable puis accomplir l'action pendant
180 ticks. Le caisson reste fermé jusque-là. Un nouvel ordre, une interruption ou la perte de
l'accès annule l'ouverture. La personne déjà présente se réveille ensuite selon les phases
physiques du caisson ; aucune arrivée automatique ne crée un nouveau colon. Le journal relie
le réveil à l'ouverture et à son auteur.

WorldSave v22 conserve dormants, action d'ouverture et échéances de vacillement. Le chargement
valide leurs références et leur cohérence avec le ledger avant de remplacer la partie active.
Les anciens formats sont refusés, sans migration, conformément à la politique du projet.

## P10 — affichage et vérifications finales

Le bouton **AFFICHAGE**, ou `F10`, ouvre les préférences : 100, 125, 150 ou 200 %, et mouvements
réduits. Elles sont enregistrées sur cet appareil, en dehors des parties. Les paramètres de
capture ne remplacent pas les préférences du joueur. Tab et Maj+Tab déplacent le focus, Entrée
active le contrôle, Échap ferme d'abord le panneau courant. Un changement d'échelle conserve
le point observé dans le monde. Les outils de construction, de diagnostic et l'atelier de
portraits restent accessibles uniquement en DEBUG.

La validation finale confronte le chemin normal du jeu aux huit tailles prévues, aux deux
backends et aux échelles d'accessibilité. Le journal, le dossier, les alertes et le menu d'un
dormant sont capturés à partir de leur état réel, avec les mêmes rectangles de dessin et de clic.

## Capturer le chemin réel

Le harnais existant `scripts/capture-ui.sh` couvre les huit tailles du plan sur les deux backends.
Les captures de cas ciblés utilisent les mêmes widgets et les mêmes projections que la partie :

- `THEEND_SHOT` : fichier PNG de destination ; par défaut, capture du composite à la frame 420
  puis sortie ;
- `THEEND_SHOT_INITIAL=1` : capture du premier composite jouable, avant tout tick de simulation ;
- `THEEND_SHOT_HOME=1` : cadrage de la baie de réveil ;
- `THEEND_SHOT_SELECT=1` : sélection d'une personne visible ;
- `THEEND_SHOT_DOSSIER=1` : ouverture du vrai dossier, avec centrage si le personnage est hors cadre ;
- `THEEND_SHOT_FIXTURE=1` : sélection d'un objet réel via le hit-test du monde ;
- `THEEND_SHOT_JOURNAL=1` et `THEEND_SHOT_SETTINGS=1` : ouverture du journal ou des préférences ;
- `THEEND_SHOT_DORMANT_MENU=1` : menu d'un caisson réellement occupé, avec un ouvreur réveillé ;
- `THEEND_SHOT_DOSSIER_END=1` : dernière partie défilée du dossier ;
- `THEEND_SHOT_ALERT=single|group` : passage réel de 1 ou 4 fondateurs sous le seuil critique,
  avec preuve de la première frame d'alerte, du retour à 1× et de la grâce complète ;
- `THEEND_SHOT_EPITHET=1` : rupture, réconfort et récupération réels, puis défilement du dossier
  jusqu'aux boutons Épingler et Voir le fait du titre gagné ;
- `THEEND_SHOT_REDUCED_MOTION=1` avec la capture Affichage : mouvement réduit activé en mémoire,
  sans écrire les préférences de l'appareil ;
- `THEEND_SHOT_VOICE=any|discussion|thought|conversation` : attend une bulle réellement dessinée
  du type demandé ; `conversation` attend deux locuteurs distincts de la même conversation
  simultanément dessinés. Le PNG est accompagné de `<fichier PNG>.voice.json`, qui consigne le
  tick capturé et les événements exacts du ledger correspondant aux bulles dessinées.
  Le scénario `conversation` attend la première ouverture réelle, puis donne deux ordres de
  déplacement aux partenaires pour les garder à portée jusqu'à la réponse ; le cadrage suit
  leur milieu. Les personnes et destinations viennent du monde courant. La réplique reste
  entièrement choisie et écrite par Voice. Cette chorégraphie est limitée à ce scénario de capture ;
- `THEEND_WIDTH`, `THEEND_HEIGHT`, `THEEND_UI_SCALE`, `THEEND_BACKEND` : résolution, échelle et backend.

Les scénarios de sélection restent inactifs sans `THEEND_SHOT`. Aucun widget factice ni donnée de
démonstration n'est injecté dans le HUD.

## Validation P5

- Compilation Debug des tests et Release du client : zéro avertissement, zéro erreur.
- 49 nouveaux cas portent la suite à 3 804 tests, sans test ignoré. La première passe complète a
  relevé une seule attente obsolète (« version 20 ») dans le test de rejet d'une sauvegarde future.
  Après correction et recompilation, les 81 cas ciblés de persistance, projections, input,
  texte du dossier et portraits mémoriels passent tous. Le cas initialement en échec est inclus.
- La stabilité des projections est vérifiée sur 60 ticks, avec un budget de 4 Ko après chauffe ;
  celle du texte sur 100 nouveaux snapshots équivalents. Un changement visible n'invalide que
  les paragraphes concernés, sans reformater les 64 faits.
- 21 captures natives Release : huit résolutions × deux backends, plus dossier à 100 et 200 %,
  objet à 200 %, inspecteur à 125 et 150 %. Dimensions vérifiées et aucun stderr.
  Les captures représentatives ont été inspectées aux tailles minimales, desktop et larges.
- Trois captures finales après harmonisation des libellés : dossier 1920×1080, dossier
  1280×720 à 200 %, équipage et inspecteur sprite 1920×1080.

Preuves locales ignorées par Git : `.artifacts/p5-tests/` pour les résultats TRX,
`.artifacts/p5-ui/validated/` pour la matrice et `.artifacts/p5-ui/final/` pour les vues finales.
Ce palier livre les surfaces P5 ; l'ensemble du rendu M2.4 reste à terminer avec les paliers suivants.

## Validation P6 et correctifs de reprise

- Compilation Release du client et Debug des tests : zéro avertissement, zéro erreur.
- Suite complète : **3 889 tests réussis**, aucun échec ni test ignoré. Après l'ajustement de
  l'emprise des tokens carrés et du scénario de capture, les **183 cas ciblés** passent aussi :
  projection Voice, texte, placement, visibilité, captures, input personnages et portraits.
- Le test d'intégration fait tourner deux simulations réelles pendant 3 000 ticks avec et sans
  présentation des bulles. Les sauvegardes complètes sont identiques, Voice et RNG compris ;
  les lignes montrées correspondent exactement aux événements émis et conservés au journal.
- La pause, la vitesse ×5, les conversations, le plafond de trois, la priorité Discussion,
  les changements de pont/cadrage, les chevauchements et les textes impossibles sont couverts.
  Le placement réserve le token carré du locuteur ainsi que son cadre de sélection ou de survol.
  Les autres colons ne sont pas des obstacles aux bulles.
- 24 captures natives vérifiées : huit résolutions de 1280×720 à 3840×2160 sur les deux backends,
  deux vues à 125/150 %, puis six captures finales couvrant les cadres corrigés au format minimal,
  paroles et pensées à 200 %, et un véritable échange à deux sur chaque backend. Les PNG ont les
  dimensions attendues, les événements annoncés sont effectivement dessinés, et aucun stderr
  n'est produit. L'échange capturé réunit les événements 333 et 334, conversation 1, au tick 14131.
- La première frame jouable a été capturée sur les deux backends avant tout tick de simulation :
  les quatre portraits sont déjà présents. Les clics de sélection et de désélection, y compris
  l'ouverture et la fermeture des panneaux, sont vérifiés sans déplacement de caméra.

Preuves locales ignorées par Git : `.artifacts/p6-tests/`, `.artifacts/p6-ui/` et
`.artifacts/portrait-warmup/`. Les captures Voice comportent un manifeste des événements réellement
dessinés. La pensée est vérifiée en italique, sans cadre, avec trois points, conformément à Fusion.

Après retour en jeu sur les changements incessants de position, l'évitement des autres colons a
été retiré et chaque réplique conserve son ancrage. **169 tests ciblés** passent, dont les suites
de déplacements, les mouvements sous-pixel, les voisins traversant la bulle, la disparition d'une
bulle voisine et la réutilisation d'un cache par une nouvelle réplique. Le fond des paroles et la
queue ont une opacité uniforme d'environ 70 %. Deux captures natives contrôlent le rendu vectoriel
et sprite ; preuves dans `.artifacts/voice-stability/`.

La suppression globale des bulles lors de l'ouverture du dossier a également été retirée :
la visibilité et le placement partagent les rectangles des seuls panneaux réellement dessinés.
**173 tests ciblés** passent, dont l'ouverture/fermeture du dossier pendant une réplique ; les
captures natives avec dossier ouvert montrent une parole en 1280×720 et une pensée en 1920×1080.
Preuves : `.artifacts/dossier-voice/`. Le plafond de trois et les durées en ticks restent inchangés.

## Validation fonctionnelle P7–P10

- **4 050 tests Release réussis, aucun ignoré.** Les contrôles ciblés passent également en DEBUG
  (110 cas d'interface). Les builds Release et DEBUG terminent sans avertissement ni erreur.
- Les huit résolutions du plan sont contrôlées à l'œil sur chacun des deux backends. Roster,
  portraits, noms, jauges, journal récent et horloge restent contenus. À hauteur égale, l'ultrawide
  conserve la densité et laisse davantage de place au monde.
- **51 captures natives contrôlées pour leur comportement et leur géométrie** : la matrice et les
  états ciblés totalisent 48 images, auxquelles s'ajoutent les deux conversations et le mouvement
  réduit. Les captures ciblées montrent journal
  complet, préférences 100/125/150/200 %, fin de dossier,
  menu d'un dormant, alerte unique, groupe de quatre et épithète gagnée avec ses deux actions
  entièrement visibles. Les overlays d'alerte et d'ouverture possèdent un fond local opaque
  pour que les textes des panneaux inférieurs ne traversent pas leurs messages.
- Les épisodes simultanés observés commencent au tick 12540, sont dessinés au tick 12541 et
  gardent leur premier tirage à 12840. L'urgence contraint 5× à 1× sans mettre en pause.
  Le titre « De retour » capturé provient du rétablissement réel au tick 15960, relié dans le ledger.
- Une conversation réelle à deux est de nouveau capturée sur chaque backend, événements 333/334
  au tick 14131, avec le journal récent présent. Le mode mouvements réduits est aussi capturé activé.
- Les caches d'alertes, de signaux sociaux, d'épithètes et de journal réutilisent leur mémoire.
  Le chemin de mesure SpriteFont du journal est testé explicitement : zéro allocation sur les
  frames inchangées, en plus des cas de reflow et de longue histoire.
- La revue indépendante du routage n'a conservé aucun blocage. L'épinglage en pause reste sur le
  chemin de commande existant, traité sans avancer le tick. Aucun nouveau fichier partiel de
  `GameInput` n'est conservé : l'interaction narrative vit dans `NarrativeHudInput`.

Preuves locales ignorées par Git : `.artifacts/m24/native-approved/` (matrice et états ciblés),
`.artifacts/m24/menu-approved/` (dernière version du menu) et `.artifacts/m24/extras/`
(conversation et mouvements réduits). Les fichiers `.ui.json` et `.voice.json` conservent les
états et événements réellement dessinés ; les captures réussies ne produisent aucun stderr.
Cette campagne ne clôt pas le contrôle artistique : la matière des panneaux doit encore être
comparée aux références après correction du rendu.

## Reprise de la matière des panneaux

- Client Release compilé sans avertissement ni erreur ; **501 tests d'interface réussis**,
  aucun échec ni test ignoré. La revue technique vérifie aussi la prémultiplication de l'alpha,
  la libération des textures et l'absence de création de ressources pendant le dessin.
- Neuf captures natives de la nouvelle matière : inspecteur d'objet, dossier, conversation à
  deux, alerte groupée, menu dormant, journal complet et réglages, avec les deux backends,
  de 1280×720 à 3840×2160 et aux échelles 100/125/150/200 %.
- La comparaison avec Étude B et Fusion porte sur la matière : fonds mats, cadres brunis,
  accidents des filets, grain et lisibilité. Les alertes et le menu masquent correctement les
  panneaux sous-jacents ; les paroles restent translucides. Les rectangles d'interaction,
  l'ancrage des bulles, la caméra et la simulation ne changent pas.

Preuves locales : `.artifacts/ui-patina/before/` pour l'ancien rendu et
`.artifacts/ui-patina/final/` pour la correction, avec dimensions et contrôles consignés dans
`.artifacts/ui-patina/validation.json`. Cette correction est disponible à comparer en jeu ;
la validation artistique finale de M2.4 reste ouverte.

## Suite du plan

Les fonctions de P7–P10 sont implémentées ; **M2.4 reste en cours pour la finition artistique de
P10**. La priorité est la matière des panneaux, boutons, cadres de portraits et paroles, suivie
d'une comparaison visuelle native avec Étude B et Fusion. La fenêtre d'histoire récente du dossier
reste bornée à 64 faits ; le journal complet et les causes d'épithètes donnent accès aux faits plus
anciens du ledger.
Après cette validation visuelle, la suite prévue est M2.5, la corruption de la présentation.
Elle devra notamment résoudre les glyphes de déformation absents de Source Sans 3 avant d'altérer
les noms affichés. Les réglages
actuels restent ceux de M2.4 ; aucune corruption de l'interface n'est anticipée ici.
