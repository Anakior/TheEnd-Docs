# Références visuelles : ce que chacune fait foi, et sur quoi

Les commandes partent de la racine `TheEnd-Docs`. Les générateurs écrivent désormais dans
`.cache/reference` et conservent les images de référence de ce dossier. L'outillage artistique
est dans le dépôt voisin `TheEnd-Art` ; le code du jeu est dans `TheEnd`.

> ⚠️ **À lire avant de tirer quoi que ce soit d'une image de ce dossier.** Chaque référence ne fait
> autorité que sur **une** chose. Le silence d'une référence n'est **jamais** un motif de suppression :
> il veut dire que la question ne lui a pas été posée.

---

## `secteur-forme.png` : la FORME d'un secteur, et rien d'autre

`ARCHE STELLAIRE / SECTEUR D'HABITAT 07`, plan d'un secteur à l'échelle 1:250.

### Ce qu'il spécifie ✅

| Élément | Ce qu'on y lit |
|---|---|
| **Silhouette du secteur** | une coque convexe à pans coupés, pas un rectangle |
| **Mur extérieur** | **trois traits** : un fin au bord, un canal noir, puis la paire de rails |
| **Forme des pièces** | octogonale, **tous** les coins largement coupés, pas des rectangles à petits chanfreins |
| **Espacement des pièces** | de larges bandes de masse hachurée entre elles, comparables à l'épaisseur d'un mur |
| **Portes** | ⭐ un **col** : un passage étroit qui **sort** de la pièce, avec ses deux jambages, le vantail au milieu. Pas un trou dans un mur |
| **Couloir** | une circulation centrale large dont les pièces pendent |
| **Nombre de pièces** | une dizaine par secteur, de tailles très inégales |

### Ce qu'il ne spécifie PAS ⛔

Et c'est la partie qui compte, parce que c'est un **plan technique** : il dessine ce qui porte, pas ce
qu'on voit en jeu.

- ⛔ **Les sols.** Les pièces y sont noires **parce qu'un plan d'architecte ne peint pas ses sols**.
  Ce n'est pas une demande de les supprimer. Les six terrains sont gelés, et c'est **le code actuel**
  qui fait foi sur eux, pas le POC et encore moins ce plan.
- ⛔ **Le liseré des salles.** Absent d'un plan technique, présent dans le jeu, **et il y reste**.
- ⛔ **Les plaques de jonction aux coins.** Idem : ce plan ne les dessine pas, ça ne veut pas dire
  qu'elles sont de trop.
- ⛔ **Les couleurs, les matières, l'usure, la corruption, les colons, l'eau, l'énergie.**
- ⛔ **Toute cote chiffrée.** Il donne des **rapports**, comme un col qui fait environ un septième de
  la largeur d'une pièce, jamais des cases. Mesurer au pixel sur cette image, c'est la même erreur que mesurer
  sur les PNG du POC, où cinq constantes sont sorties fausses dans le même sens parce qu'un halo
  d'anticrénelage se lit comme du plein.

### D'où vient la vérité, quand deux sources se croisent

| Sujet | Qui fait foi |
|---|---|
| Forme d'un secteur, des pièces, des cols, espacements | ⭐ **ce plan** |
| Terrains (les six matières, le fondu, l'herbe) | ⭐ **le code actuel**, peaufiné après le POC : la divergence est voulue |
| Liseré, murs intérieurs, plaques, portes | le POC **et** le code, qui sont d'accord |
| Coque, hachure de masse, feuille blueprint | **aucune source écrite** : ce sont des décisions, à juger à l'écran |

Voir `theend/meta/plan-rendu-architecture.md` §0 et §0.1 dans l'Atlas, qui posent la même règle et
racontent ce qu'a coûté de l'oublier.

---

## `generate_sector_plan.py` + `secteur-forme-mockup.png` : une interprétation, pas une source

Un générateur déterministe écrit par Codex à partir de `secteur-forme.png` et d'une capture du jeu.
Toute sa géométrie sort de constantes nommées **en cases**, chacune étiquetée de sa provenance.

```
python3 reference/generate_sector_plan.py --seed 7
```

### ⚠️ Ce que l'étiquetage révèle, et c'est pour ça qu'il a été demandé

Sur **152** constantes : **4 lues** sur le plan, **16 jugées à l'œil**, **132 dérivées** des
précédentes. Le mockup ne mesure donc pas la référence, il repose sur **vingt décisions** et de
l'arithmétique par-dessus. Ses **rapports** sont informatifs ; ses valeurs ne font autorité sur rien.

### ⛔ Son look n'a aucune autorité

Il a redessiné le liseré, les rails, les plaques, les six sols et les portes, ce qui lui avait été
interdit. Il les a **transcrits** depuis le code plutôt qu'inventés, donc le mal est limité, mais
c'est désormais une **seconde copie qui va diverger** : elle porte déjà un `TRIM_TICK_LEAN_DEGREES`
alors que le liseré du jeu pose un `/` global sur mur droit.

⛔ **Ne jamais corriger le renderer pour lui ressembler.** Sur le look, le code fait foi.

### Ce qu'il apporte vraiment : cinq nombres

| | jeu | mockup |
|---|---|---|
| espacement salle ↔ salle | `RoomPacker.Seam` = 1 | **4** |
| espacement salle ↔ couloir | 1 | **4** |
| largeur du couloir | `SectorMetrics.SectorGap` = 4 | 6 |
| coupe des coins | 0,15 à 0,40 du petit côté, sur 55 % des coins | **1/4, sur tous les coins** |
| col de porte | n'existe pas, la porte est une case dans le mur | **2 cases de large**, profond de toute la bande, vantail au milieu |

Les tailles de pièces, elles, tombent déjà juste : 10-18 sur 12-20 contre 8-18 sur 9-20 dans le jeu.

### ⛔ Ce qu'il ne faut PAS en prendre

- **Sa disposition.** Deux rangées alignées de part et d'autre d'un couloir droit, des pièces de
  tailles voisines, une marge vide contre la coque. La référence tasse des pièces très inégales
  jusqu'à la coque. C'est une limite d'algorithme, la même que `RoomPacker`, qui fait pendre des
  colonnes de pièces à un couloir décidé avant elles.
- **Sa coque**, un polygone régulier là où celle de la référence épouse les pièces.

---

## `etage-assemblage.png` : comment les secteurs s'ASSEMBLENT

`ARCHE STELLAIRE / ÉTAGE MULTI-SECTEUR`, révision 2. Six nacelles sur un étage.

`secteur-forme.png` dit la forme d'**une** nacelle ; celui-ci dit ce qu'il y a **entre** elles. Les
deux ne se contredisent pas, ils ne sont pas au même niveau de lecture.

### Ce qu'il spécifie ✅

| Élément | Ce qu'on y lit |
|---|---|
| **Un secteur est une nacelle** | il a **sa propre coque** et sa ceinture hachurée, pas une région dans un plastron commun |
| **Entre deux nacelles** | du **vide**, pas de la masse |
| **Le lien** | ⭐ un `SAS INTER-SECTEUR`, et **rien d'autre**. Pas de couloir central : la note du plan en fait une règle |
| **Le graphe** | une grille 2x3, chaque nacelle touche ses voisines. Perdre une nacelle ne coupe jamais l'étage |
| **La circulation interne** | ⭐ ce n'est pas « des couloirs entre les pièces » : c'est le réseau qui relie **chaque porte de pièce aux sas** de sa nacelle |
| **La disposition** | une **dominante au centre**, les satellites en couronne autour |
| **La forme des pièces** | des rectangles à coins coupés, aux proportions très variées. Pas des octogones réguliers |

⭐ L'invariant qui en découle, et qui est testable : **depuis la porte de n'importe quelle pièce on
atteint un sas sans traverser une autre pièce.** ⚠️ Il rougirait aujourd'hui, et volontairement :
`RoomPacker.BackRoomChance = 0.22` pose des pièces en seconde rangée, atteignables uniquement en
traversant leur voisine. C'est un arbitrage, pas un oubli.

### Ce qu'il ne spécifie PAS ⛔

- ⛔ **L'ÉCHELLE. Elle est fausse, et deux fois.** Les graduations de la barre ne sont pas régulières,
  c'est un objet décoratif. Et même régulière, elle donnerait des `LOGEMENTS` de 9 x 4 m et des
  `SANITAIRES` de 12 x 3 : crédible pour de l'architecture, **injouable** ici, où `RoomMetrics.MinRoom`
  vaut 9 cases. Une case n'est pas un mètre, c'est une unité de jeu.
  **Ne jamais convertir ce plan en cases.** Il donne des rapports, pas des cotes.
- ⛔ **Le taux de remplissage.** Il est à 80-90 %, parce qu'un vrai vaisseau ne gaspille rien. Un
  colony-sim, si : le joueur doit pouvoir s'approprier l'espace, poser, réaménager, agrandir. La masse
  libre à l'intérieur d'une nacelle n'est pas de la place perdue, c'est **de la place à prendre**, et
  la coque est la limite dure que Core refuse de franchir. Viser plutôt **50 à 60 %**.
- ⛔ **Le look**, comme toujours. Le code fait foi.

### D'où viennent les tailles absolues

Pas d'ici. On les ancre sur les valeurs du jeu, déjà validées par la pratique
(`RoomMetrics.MinRoom` 9, `MaxRoom` 20), et la taille de nacelle en découle : onze pièces à ces
tailles, remplies à 50-60 %, donnent une nacelle d'environ **70 x 45**. `SectorMetrics` est déjà à
58-88, donc dans la bande.

---

## `generate_sas_plan.py` + `sas-planche.png` : une DÉCISION, pas une observation

```
python3 reference/generate_sas_plan.py
```

⚠️ **Cette planche n'est pas de la même nature que les deux plans ci-dessus.** Eux sont des dessins
qu'on lit ; celle-ci est un dessin qu'on a fait pour **trancher**. Elle n'observe rien, elle
enregistre trois choix pris devant l'écran, en comparant les options côte à côte.

Tout y est à l'échelle de la case, dans le langage du jeu : hachure de masse, liseré de coque, rails
doublés, plaques de jonction, sol pointillé.

### Ce qu'elle fait foi ✅

| Sujet | Décision |
|---|---|
| **Nature** | ⭐ un sas est **UN objet**, pas trois cases voisines qui s'ignorent |
| **Largeur** | 3 cases |
| **Fermé** | bloque **exactement comme un mur** |
| **Disposition** | ⭐ **A** : le tube EST la chambre, une porte à chaque extrémité |
| **Lisibilité** | ⭐ **3, blindée** : emprise de 2 cases dans l'axe, le mur s'épaissit autour |
| **États** | ouvert, en cycle, fermé, scellé, soudé |

Les proportions dessinées ne sont pas choisies, elles sont **mesurées dans le jeu** : tube de 3 cases,
bordage de 2 de chaque côté. Mesure sur 10 ponts et 35 164 murs et portes, la distance minimale entre
un mur et le vide est de 2 cases, jamais moins.

### ⚠️ Elle diverge volontairement de `etage-assemblage.png`

Le plan d'assemblage dessine **deux chambres accolées** entre chaque paire de secteurs, étiquetées
« SAS SAS », et sa légende fait de `SAS INTER-SECTEUR` un objet distinct de `PORTE / TRAPPE`. La
planche pose l'option C sur cette base, et **Ludovic a retenu A**.

⛔ **Ne pas « corriger » vers la référence.** C'est un arbitrage assumé : A se lit immédiatement,
coûte deux portes au lieu de trois, et la géométrie garde la marge pour passer à C plus tard sans
toucher au générateur (2 + 3 + 2 + 3 + 2 = 12 cases, exactement la traversée disponible).

### Ce qu'elle ne spécifie PAS ⛔

- ⛔ **Les épaisseurs de trait et les couleurs.** La planche est dessinée à la main en Python, pas par
  le renderer. Ce qui est validé est la **forme**, jamais les valeurs. Le code fera foi, comme partout
  ailleurs dans ce dossier.
- ⛔ **La mécanique.** Est-ce que le sas tient la pression ? La nacelle devient-elle l'unité de
  dépressurisation ? Qui ordonne sa fermeture, et quel colon nommé va la faire ? Est-ce qu'il s'use ?
  Est-ce qu'il retient une trace de ce qu'il a enfermé ? **Aucune de ces questions n'est tranchée**, et
  la planche n'y répond pas.
- ⛔ **Le calendrier des états.** `ouvert` et `fermé` sont mécaniques et implémentables. `scellé` et
  `soudé` supposent qu'un ordre du joueur puisse devenir un travail confié à un colon : ils entrent le
  jour où le système d'ordres sait le porter, pas avant. Les cinq membres existent dès maintenant dans
  l'énumération, pour qu'un état ajouté plus tard ne finisse pas dans un `default` — le trou que
  `CS8509` traite en erreur ici.

---

## `concept-element.png` : le VOCABULAIRE d'un élément posé au sol, vu de dessus

Une planche de concept, huit familles vues de dessus : `ASCENSEUR`, `ÉCHELLE`, `GLACE`,
`TROUS DANS LE SOL`, `EAU`, `ROCHERS`, `FISSURES DANS LES MURS`, `ARCS ÉLECTRIQUES`.

Les trois planches précédentes parlent du **bâti** — la forme d'une nacelle, ce qu'il y a entre elles,
comment on passe de l'une à l'autre. Celle-ci parle de ce qui **traîne dessus** : elle ne dit ni où ces
éléments apparaissent, ni ce qu'ils font, elle dit **à quoi on les reconnaît**.

### Ce qu'elle spécifie ✅

| Sujet | Ce qu'on y lit |
|---|---|
| **La vue** | ⭐ strictement de dessus, comme le reste du jeu. Une échelle est un **puits** vu d'en haut, pas des barreaux de profil |
| **Progression par paliers** | ⭐ chaque famille se lit en **quatre crans** de la même chose : petit / moyen / grand / structurel. Ce n'est pas quatre objets, c'est un objet et son intensité |
| **Ligne du bas = variante d'état** | en mouvement pour l'ascenseur, profondeur pour l'échelle, glissant pour la glace, débris pour les trous, courant pour l'eau, envahissement pour les rochers |
| **Encadrement** | ⭐ les éléments **construits** (ascenseur, échelle) sont tenus par un cadre de structure avec ses plaques de coin ; les éléments **naturels ou subis** (eau, glace, rochers, trous) n'ont pas de cadre et débordent librement |
| **Silhouette du naturel** | des contours **irréguliers et fermés**, jamais alignés sur la grille. Une flaque n'est pas un carré bleu |
| **Sens de lecture** | ⭐ quatre codes, et seulement quatre : trait plein = structure, hachure = dégâts/usure, aplat bleu = accumulation, trait cyan = **élément actif** |
| **Le cyan est rare** | il ne sert qu'à dire « ça bouge, ça marche, ça a du courant ». Un ascenseur en panne le perd |

⭐ L'invariant qui en découle : **un élément mort et le même élément vivant ne diffèrent que par le
cyan.** C'est ce qui permet de lire un pont d'un coup d'œil sans lire d'étiquette.

### Ce qu'elle ne spécifie PAS ⛔

- ⛔ **Ce qui existe dans le jeu.** `FeatureType` connaît aujourd'hui `Water`, `Energy`, `Ice`,
  `Elevator`, `ServiceLadder` ; les **trous**, les **rochers** et les **fissures de mur** n'ont aucun
  équivalent, et les `ARCS ÉLECTRIQUES` sont vraisemblablement la forme visuelle d'`Energy`, pas une
  neuvième famille. **Cette planche n'est pas une liste de features à implémenter.** Elle dessine un
  vocabulaire ; ce qui entre dans l'énumération se décide ailleurs, sur des critères de jeu.
- ⛔ **Les tailles.** Aucun cran n'est chiffré en cases. « Petit / moyen / grand » sont des **rapports
  entre eux**, exactement comme les cotes de `secteur-forme.png`. Mesurer au pixel ici referait la même
  erreur.
- ⛔ **Les couleurs, les épaisseurs de trait, l'anticrénelage.** Comme partout dans ce dossier :
  **le code fait foi sur le look.** La planche valide une **forme** et une **grammaire**, jamais des
  valeurs. `IceSkin`, `LeakSkin` et `FloorPalette` ne se corrigent pas pour ressembler à une image.
- ⛔ **La mécanique.** Est-ce qu'un trou se traverse, se comble, tue ? Est-ce que la glace fait glisser
  ou seulement ralentit ? Est-ce qu'un rocher se mine ? Une fissure fuit-elle ? **Rien de tout ça n'est
  tranché**, et `FeatureRules` reste seul juge de ce qui bloque.
- ⛔ **La fréquence.** Une planche montre les quatre crans côte à côte parce que c'est un catalogue.
  Un pont couvert de gros trous et de flaques profondes serait illisible et injouable : la
  distribution se règle à l'écran, pas ici.

---

## `cryo-pod-direction-a-concept.png` : cible de MATIÈRE pour le cryopod

Concept exploratoire généré pour isoler la direction A : un sarcophage longitudinal vu strictement
du dessus, montré fonctionnel, brisé et ouvert. Il sert de cible de richesse industrielle — coque
multicouche, joints, verrous, verrière et machinerie — et montre comment le token carré `KA` peut
rester l'identité du colon sans introduire de silhouette humaine.

### Ce qu'il spécifie ✅

- la famille de forme longitudinale et blindée ;
- la hiérarchie coque / joint / verrière / berceau / machinerie ;
- les trois lectures d'état : cyan actif, verre mort et fissuré, cavité ouverte ;
- l'ambre réservé au nom du colon, petit et intégré au berceau.

### Ce qu'il ne spécifie PAS ⛔

- ⛔ **Le rendu du jeu.** Ce PNG n'est pas produit par l'ASCII renderer. Le POC déterministe
  `../TheEnd-Art/archive/ascii-render/poc/cryo_pods.py`, puis le futur skin C#, font foi sur les traits et les détails.
- ⛔ **Les dimensions en pixels.** Le concept ne tranche pas l'emprise. Le POC teste actuellement
  une variante 2×1 (64×32 px à la caméra par défaut), avec le précédent 3×1 conservé pour comparaison.
- ⛔ **La mécanique.** Il ne décide ni énergie, ni température, ni interaction, ni devenir du colon.

---

## `rack-concept.png` : grammaire de FORME du rack modulaire

Planche historique fournie pour explorer un rack vu de dessus : cadre industriel, tablettes,
face d'accès, orientations et répétition le long d'un mur. Ses objets dessinés et ses libellés
plein / entamé / vide ne sont plus normatifs : le sujet retenu est désormais la structure et ce
que les siècles lui ont fait. Le générateur déterministe montre **scellé**, **dépouillé** et
**effondré**, sans aucun contenu.

### Ce qu'il spécifie ✅

- une famille industrielle faite de rails imbriqués, plaques d'angle, verrous et marques, sans
  aplat ;
- trois lectures matérielles : fermeture intacte et sanglée, ossature ouverte et nue, puis coque
  rompue avec tablettes affaissées ;
- une face d'accès portée par un double rail plus lumineux et une encoche centrale ;
- des empreintes 1×1, 2×1 et 3×1 comme variantes exploratoires de la même grammaire ;
- le test décisif d'une rangée de quinze racks contre un mur, avec un effondré au centre ;
- une palette d'acier froide ; l'ambre `#C69660` reste réservé à l'identité d'un colon.

### Ce qu'il ne spécifie PAS ⛔

- ⛔ **Un contenu ou une quantité.** Aucun objet, type, stock, capacité, chiffre, jauge ou opacité
  variable n'est défini. Les plans entre le fond gravé et les lèvres avant restent libres pour une
  future mécanique de portage.
- ⛔ **Une promesse de récupération.** `Scellé` décrit uniquement l'intégrité de la fermeture ; il
  n'affirme pas qu'un butin existe derrière elle.
- ⛔ **Une empreinte de gameplay.** Le `FoodStore` réel est aujourd'hui une entité mono-case,
  passable et sans orientation. Les formats 1×1 à 3×1 restent des explorations de présentation.
- ⛔ **Une case d'interaction.** Le double rail désigne une face visuelle. Le jeu ne possède encore
  ni orientation de rack ni cellule d'accès adjacente.
- ⛔ **Les anciens objets du concept.** Bidons, caisses et états de remplissage de l'image source
  ne sont conservés que comme historique de composition.
- ⛔ **Le rendu final du jeu.** Le générateur `../TheEnd-Art/archive/ascii-render/poc/racks.py` produit une grammaire
  vectorielle prévisualisée en PNG ; un futur skin C# devra encore la porter dans MonoGame.

---

## `bunk-direction-a-concept.png` : grammaire de FORME de la couchette

Concept exploratoire fourni pour une bannette navale ouverte vue du dessus. Il donne une direction
de matière et de silhouette, pas un système de sommeil. Le POC déterministe conserve le vrai token
carré du colon comme une couche d'acteur séparée et refuse la silhouette humaine.

### Ce qu'il spécifie ✅

- un berceau longitudinal ouvert, avec une tête dense et protectrice puis des pieds légers ;
- un rail côté mur continu et une face visuelle interrompue côté couloir ;
- une literie entièrement décrite par des contours, coutures, tension et hachures, sans aplat ;
- trois lectures matérielles proposées : **intacte**, **dépouillée** et **ruinée** ; la présence du
  colon reste un axe séparé, jamais un quatrième état du meuble ;
- une proposition 2×1 au zoom nominal de 32 px/case, une variante longue 3×1 et plusieurs poses
  orientées comme explorations visuelles ;
- le test anti-papier-peint de quinze couchettes indépendantes, parallèles au mur, avec une ruinée
  au centre ;
- l'ambre `#C69660` réservé au token du colon.

### Ce qu'il ne spécifie PAS ⛔

- ⛔ **Une mécanique de lit.** Le sommeil actuel est une activité abstraite déclenchée sur la case
  où se trouve le colon. Il ne cherche, ne cible, n'occupe et ne réserve aucun meuble.
- ⛔ **Une affectation ou une capacité.** Le token placé sur la case de tête est une composition de
  présentation proposée, pas la preuve d'un lit attribué ni occupé.
- ⛔ **Une empreinte, une orientation ou une collision de gameplay.** Le modèle ne possède encore
  aucun objet couchette, face d'accès, cellule d'interaction ou règle de circulation associée.
- ⛔ **Une taxonomie arrêtée.** Le 2×1 et la variante médicale 3×1 sont des hypothèses de forme ; le
  1×1 est simplement hors de cette étude de couchette adulte.
- ⛔ **L'état “détournée”.** Il a été retiré du POC pour ne pas dessiner un rangement ou un contenu
  sans mécanique de portage.
- ⛔ **Le rendu final du jeu.** `../TheEnd-Art/archive/ascii-render/poc/bunks.py` produit une grammaire vectorielle
  prévisualisée en PNG ; un futur objet et son skin C# restent à modéliser.

---

## Grammaire « LA LIGNE » : infrastructure linéaire

Brief de forme destiné à unifier les tracés techniques déjà suggérés au-dessus des caissons cryo et
des couchettes. Le générateur `../TheEnd-Art/archive/ascii-render/poc/infrastructure_lines.py` transforme un graphe
cardinal de dessin en conduite ou chemin de câbles, puis produit
`../TheEnd-Art/archive/ascii-render/poc/output/infrastructure-lines.png`. Il s'agit d'une infrastructure visuellement
inerte, pas d'un réseau de simulation.

### Ce qu'il spécifie ✅

- la distinction prioritaire avec le mur : le mur reste une bande vide entre deux rails égaux,
  scandée par des plaques carrées ; la conduite possède un corps axial sombre, des lèvres, des
  bagues perpendiculaires et des collecteurs ronds ; le câble reste un faisceau de brins avec
  colliers ;
- une grammaire paramétrique de raccords cardinaux : segments, coudes courbes, T, croix et trois
  fins visuelles — bouchon scellé, fin contre mur et coupe franche ;
- deux familles de matière partageant le même tracé : conduite et chemin de câbles ; le rail ou
  garde-corps est volontairement reporté tant qu'il ne possède pas une silhouette assez distincte
  du mur ;
- trois lectures matérielles proposées : intacte, conduite percée ou gaine lésée, puis sectionnée ;
- le danger coloré comme une surcouche rare : acier neutre lorsque la ligne est inerte, évocation
  d'eau ou d'arc seulement au point endommagé ;
- une validation de lecture par composition de pièce au zoom nominal, puis rerendu paramétrique à
  32, 24, 16 et 12 px/case.

### Ce qu'il ne spécifie PAS ⛔

- ⛔ **Un réseau de gameplay.** Aucun composant, port, identifiant de réseau, source, puits, flux,
  capacité, pression, tension, température, alimentation, transport ou réparation n'existe encore.
  Le graphe Python ne sert qu'à produire les raccords visuels du POC.
- ⛔ **Une relation entre les lignes et les meubles.** Rack et couchette ne sont que des repères
  d'échelle dans la composition ; ils ne consomment rien et ne possèdent aucun port.
- ⛔ **Le tracé des dangers actuels.** Les `FeatureType.Water` et `FeatureType.Energy` restent des
  dangers par case, impassables et non raccordés. Les marques de fuite de la planche évoquent un
  futur raccord visuel ; elles ne reproduisent ni une topologie ni un point de rupture connu du
  `LeakSkin`.
- ⛔ **Une couche de rendu ou une collision.** Passage mural, sous-plancher, superposition de
  familles et règles d'occlusion restent à décider.
- ⛔ **Le rendu final du jeu.** Le PNG est la prévisualisation d'une grammaire vectorielle ; un futur
  modèle et son skin C#/MonoGame devront encore porter cette infrastructure.

---

## `console-four-directions-concept.png` : source de FORME pour console et poste

Planche comparative historique fournie pour explorer quatre directions graphiques. La décision de
conception les normalise en **deux archétypes seulement** : A, B et C deviennent trois matières
intérieures d'une même **console** ; D devient le **poste** en alcôve. Le générateur déterministe
`../TheEnd-Art/archive/ascii-render/poc/consoles.py` applique cette décision et produit
`../TheEnd-Art/archive/ascii-render/poc/output/consoles.png`.

### Ce qu'il spécifie ✅

- une coque commune de console, faite de rails imbriqués, joues de service, plaques, verrous et
  tablette opérateur ; seule la matière intérieure change ;
- trois habillages déclarés par le type de pièce : **visière** pour un système protégé, **dalle**
  pour un plan horizontal et **peigne** pour plusieurs lectures ; ces marques restent de la matière
  abstraite, jamais une carte, un texte ou une donnée lisible ;
- un second archétype en U : le **poste**, dont le vide central et les ailes enveloppantes portent
  la lecture ;
- les empreintes de présentation retenues : console 2×1 ou 3×1, poste 3×2 ou 4×3 ; le 1×1 est
  abandonné dans cette étude ;
- trois états visuels proposés : **morte**, **vivante** et **brisée**, avec le cyan `#48A8E0`
  limité aux plans d'affichage actifs et l'ambre absent ;
- une orientation strictement vue du dessus, une face opérateur marquée sur l'objet, une variation
  déterministe par objet et un test de répétition sur le peigne ;
- une validation paramétrique au zoom nominal de 32 px/case, puis à 24, 16 et 12 px/case.

### Ce qu'il ne spécifie PAS ⛔

- ⛔ **Quatre objets distincts.** Les anciennes directions A/B/C ne sont plus trois formes de
  mobilier. Les petites vues en biais de la planche source ne sont pas normatives non plus : le POC
  ne produit que des rotations top-down.
- ⛔ **Le 1×1, le mur ou la hachure verte de la source.** Le POC refuse la console 1×1, ne redessine
  aucun mur d'appui et corrige la hachure en gris `#78818F`.
- ⛔ **Une information consultable.** Les segments de dalle, dents du peigne et marques cyan ne
  codent aucun écran, texte, carte, chiffre, jauge ou commande lisible par le joueur.
- ⛔ **Une mécanique d'énergie.** `Morte` et `vivante` sont des lectures d'affichage proposées ; le
  jeu ne possède aujourd'hui aucun objet console, état d'alimentation, port, réseau ou réparation.
- ⛔ **Un opérateur ou une interaction.** Empreinte, orientation, face visuelle, collision, capacité,
  réservation et case d'usage ne sont pas modélisées. Le vide du poste n'est ni un siège ni une
  cellule d'interaction.
- ⛔ **Le rendu final du jeu.** La grammaire est vectorielle mais le livrable actuel reste un PNG de
  prévisualisation ; un futur modèle et son skin C#/MonoGame devront encore l'intégrer.

---

## `ui-jeu-etude-b.png` : cible d'interface (M2.4) — bulles de Fusion

**Arbitrage de reprise M2.4 : `ui-jeu-etude-b.png` est la cible finale de composition et de matière
de l'interface. Les bulles s'inspirent de `ui-jeu-fusion.png`.** Cette instruction de Ludovic
remplace l'ancienne priorité générale donnée à Fusion, encore citée dans le plan M2.4 sur l'Atlas.
L'étude B guide le roster bas, l'inspecteur à droite, les panneaux charbon et les cadres métalliques
fins ; Fusion guide la parole encadrée avec queue et la pensée en italique sans cadre avec une
traînée de points. L'étude A reste une référence historique.

Aucune des trois images n'est une spécification fonctionnelle, une capture du jeu, ou la promesse
d'un système. Les champs affichés viennent exclusivement du modèle existant. Les portraits validés
restent les assets du jeu et la sélection des personnages utilise désormais un cadre carré.

### Ce que les références spécifient ✅

- **La densité et le registre** : peu de panneaux, beaucoup de vide, aucune icône bavarde. Le jeu est
  lent et sombre, l'interface doit l'être aussi.
- **La matière de l'UI** : cadres métalliques fins, filets d'un pixel, panneaux sombres
  semi-transparents qui laissent voir le monde. Elle appartient au vaisseau, pas à une application.
- ⭐ **La séparation provenance / occupation, lisible d'un coup d'œil** — deux inspecteurs côte à
  côte : `CP-05 · STATE SEALED · OCCUPANT MARA VALE — CONTAINED · PROVENANCE —` face à
  `CP-03 · STATE OPEN · OCCUPANT NONE · PROVENANCE ADRIEN VALE EMERGED HERE`. C'est exactement le
  modèle du code (`FixtureCondition` + `BerthClaimComponent` d'un côté, `OccupantSoul` de l'autre),
  et la preuve qu'il se raconte sans notice. **L'acquis principal de tout l'exercice.**
- ⭐ **L'ambre distingue une présence d'une trace** : `OCCUPANT: MARA VALE — CONTAINED` est en ambre,
  `PROVENANCE: ADRIEN VALE EMERGED HERE` est en gris. Une identité vivante et présente porte la
  couleur des colons ; un nom qui n'est plus qu'un enregistrement ne l'a pas. Règle à tenir partout.
- ⭐ **Le roster est une FAMILLE** — Mara, Simon, Adrien, Lena, Noah **Vale**, avec le crochet de
  parenté dessous. C'est la prémisse du jeu (`FamilyLoader.FoundingFamily`, `family.json`) : un
  joueur qui lit ce roster comprend en une seconde pourquoi la chute fera mal. C'est aussi
  « percevoir sans lire » résolu pour trois pixels.
- **Les quatre jauges nommées** `HLT` / `HNG` / `RST` / `MND` — santé, faim, repos et **esprit**
  (`MentalHealthComponent`, la jauge centrale du jeu).
- **Les bulles, deux registres distincts** : parole en cadre fin avec queue, pensée en italique sans
  cadre, reliée à son porteur par une traînée de points. **Chaque bulle appartient à un colon
  visible.** Toutes deux purement typographiques, donc capables de mentir plus tard (M2.5).
- **Le ton des répliques** : sobre, humain, inquiet — `THE OTHERS ARE STILL UNDER.`, jamais un bon
  mot ni un relevé d'état.
- **Le journal nomme ses locuteurs** (`SIMON VALE: I DON'T LIKE THIS PLACE.`) : la forme que produit
  réellement le `VoiceDirector`.
- **L'alerte de rupture est priorisée**, en ambre et détachée de la pile — c'est la garantie
  anti-injustice de M1.3, elle ne doit pas se noyer.
- **Le panneau est réduit à ses lignes vraies** : quatre, pas une de plus.
- **L'absence de grille de priorités et de barre d'actions**, qui est **normative** : le joueur
  ordonne, un colon nommé exécute (systeme-colons §3.4 sur l'Atlas).
- ⭐ **Le budget lumineux : le monde est la lecture principale, l'UI est secondaire.** On
  n'assombrit **jamais** le vaisseau pour faire ressortir les panneaux — une interface plus
  contrastée que le monde fait lire les panneaux au lieu du vaisseau, et c'est le point faible de
  RimWorld que M2.4 existe pour corriger. Deux corollaires de palette, distincts et à ne plus
  confondre : **l'ambre marque une personne vivante, ce n'est pas un état de sélection** — tous les
  colons le portent, la sélection étant le cadre carré et non la couleur ; et **le cyan a deux portées,
  toutes deux justes** — sur une machine il veut dire « elle tourne » (un caisson scellé et occupé
  garde donc sa lueur, toujours), dans l'interface il veut dire « sélectionné ou interactif ».
  Rationner l'un ne doit jamais éteindre l'autre.
- ⭐ **La lisibilité vient de la lumière LOCALE, pas de l'exposition globale.** Règle née d'un
  aller-retour complet le 12 août 2026 : une première passe avait assombri le monde pour faire
  ressortir l'UI (*« on lit moins le jeu lui-même »*), la correction a éclairci **tout le pont**
  uniformément (*« trop lumineux maintenant »*). La cible est entre les deux, et ce n'est pas un
  réglage de curseur : **le sol reste noir et froid, ce sont les machines alimentées qui font des
  flaques de lumière autour d'elles**. Éclaircir globalement achète la lisibilité en tuant
  l'ambiance ; éclairer localement donne les deux. C'est aussi ce que dit la planche sprite plus
  bas — l'éclairage est le système absent qui ferait le plus pour les deux moteurs.

### Ce qu'elles ne spécifient PAS ⛔

- ⛔ **Les systèmes que le jeu n'a pas.** L'étude A affichait `CONDITION: 78 %`, `CORE TEMP` et
  `LAST CHECK` ; l'étude B, `CONDITION: GOOD` et `POWER: ONLINE`. **Aucun de ces champs n'existe et
  aucun ne doit exister à cause de ces images** — ils ont été retirés pour cette raison, et la fusion
  est la preuve que le panneau se tient sans eux. `FixtureCondition` est un enum à quatre états —
  `Sealed`, `Open`, `Stripped`, `Collapsed` — et pas une usure graduée (plan-objets sur l'Atlas :
  « aucun champ d'usure, l'état se projette depuis le ledger ») ; l'énergie est un système de M2.11.
- ⚠️ **Défauts restants de la planche, à ne pas recopier :**
  - **le pont est éclairé trop uniformément.** C'est le second dépassement de l'aller-retour
    ci-dessus : on lit le vaisseau, mais l'arche a perdu son froid. La cible est **entre les deux
    passes** — sol sombre, lumière **locale**. Constat de Ludovic : *« trop lumineux maintenant,
    mais comme base ça ira » * ;
  - **`HULL INTEGRITY CRITICAL / CATASTROPHIC FAILURE IMMINENT` sur-corrige.** Remplacer le
    non-événement était juste, mais l'effroi de ce jeu est **lent** : une alerte qui promet la
    destruction dans les secondes qui suivent ment sur son rythme, et suppose un système de coque
    qui n'existe pas ;
  - **`POWER ROUTING OPTIMIZED` dans le journal** : un message système dans un journal qui doit
    rester humain.
- ⛔ **Les libellés, unités et valeurs.** Noms, numéros d'unité, heures, secondes et jours sont du
  remplissage d'ambiance. La ligne de journal `POWER ROUTING OPTIMIZED` est du même ordre : un
  message système dans un journal qui doit rester humain.
- ⛔ **Le rendu du monde.** Le décor sous l'UI est la planche sprite ci-dessous, pas le renderer.

---

## `rendu-sprite-concept.png` : cible d'AMBIANCE pour le second moteur (M2.3)

Rendu sprite de la même baie cryo, généré le 12 août 2026 « juste pour la curiosité de ce que ça
pourrait être ». **Aucune décision n'est prise sur le style du jeu** : l'axe ASCII vectoriel reste
l'identité, le sprite est le second skin optionnel du double moteur.

### Ce qu'elle spécifie ✅

- **L'ambiance à atteindre**, quel que soit le moteur : froid, abandonné, gel dans les angles,
  plaques de sol fêlées, noir qui avale tout au-delà des murs.
- ⭐ **Ce qui fait le travail, et ce n'est pas le sprite : la LUMIÈRE.** La flaque cyan sous les
  caissons, le dégradé sur les grandes surfaces, le noir au-delà. Le jeu n'a aujourd'hui **aucun
  système d'éclairage**, et cette passe embellirait autant l'ASCII que le sprite — c'est
  l'enseignement principal de la planche.
- **La confirmation que la couche sémantique suffit** : nacelle octogonale, caissons 1×2
  perpendiculaires adossés, murs à épaisseur, conduits à bagues, rack, console, sas. Rien dans
  l'image ne demande une donnée que `DisplayCell` / `DisplayObject` / `DisplayActor` ne portent déjà.

### Ce qu'elle ne spécifie PAS ⛔

- ⛔ **Le choix du moteur.** Voir cette image ne tranche pas le double moteur ; M2.3 ne livre que
  **la couture** (un second consommateur de `DisplayFrame`, avec des placeholders), pas des assets.
- ⛔ **Un tileset.** C'est **une frame composée à la main**, pas une grammaire : elle ne dit rien des
  raccords de murs, des autres formes de salles, ni des rotations.
- ⛔ **Le niveau de finition des assets.** Le garde-fou reste ~1 h par asset.
- ⛔ **La densité de mobilier.** La salle y est vide, et le sprite rend ce vide **pire** que l'ASCII.
  C'est un constat sur le mobilier, pas une cible de composition.
