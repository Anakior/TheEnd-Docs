# Architecture et budget de performance du renderer

Ce document fixe l'état de référence de la passe d'optimisation des 11 et 12 août 2026. Il explique les
coûts observés, les choix retenus, les invariants à préserver et la manière de refaire les mesures.
Il ne constitue pas une promesse de FPS absolue : les temps GPU dépendent de la machine et du
driver. Les rapports avant/après, le nombre de sommets et les budgets d'une frame sont les repères
durables.

## Objectifs

Le renderer doit respecter quatre contraintes :

1. tenir 60 Hz sans dette GPU sur un pont meublé de 256×256 ;
2. ne jamais bloquer une frame sur la tessellation complète d'un pont ;
3. ne jamais montrer un assemblage de couches provenant de deux révisions différentes ;
4. conserver exactement la même sémantique de monde, le même ordre déterministe et le même langage
   visuel.

La cible de frame est donc de 16,67 ms. Les uploads étagés et les commits du cache statique visent
moins de 4 ms par appel au thread de rendu. Les calculs plus longs doivent être annulables et
exécutés sur un worker borné. Le premier build lazy d'un chunk de meubles reste une limite distincte,
mesurée plus bas.

## Protocole de référence

Les mesures de cette page ont été faites avec :

- build `Release` ;
- seed `12345` ;
- monde de `256×256` cellules ;
- fenêtre `1920×1080` ;
- zoom de référence `24 px/cellule` ;
- SS3, sauf quand la ligne mentionne explicitement SS4 ou MSAA4 ;
- rendu non plafonné et VSync désactivée pour rendre visible la dette GPU ;
- 120 frames de chauffe, puis 360 frames mesurées ;
- même caméra et même famille de pont avant/après.

Le harnais détaillé utilisé pendant l'audit vit localement sous `TestResults/runtime-matrix`. Ce
dossier est volontairement ignoré par Git : les chiffres et le protocole ci-dessus sont la source
durable, pas les fichiers temporaires du probe.

## Résultats consolidés

| Mesure | Avant | Après | Gain observé |
|---|---:|---:|---:|
| Dôme, sommets soumis par frame | 4 646 000 | 781 956 | −83,2 % |
| Start, sommets soumis par frame | 3 895 000 | 449 016 | −88,5 % |
| Dôme SS3, coût steady du probe | 2,051 ms | 0,199 ms | environ 10,3× |
| Sol du dôme, pass `retained_base` | 1 864 605 sommets | 449 274 | −75,9 % |
| Meubles du dôme, géométrie complète | 2 402 088 sommets | 411 915 | −82,9 % |
| Meubles Start, géométrie complète | 3 110 262 sommets | 581 541 | −81,3 % |
| Installation GPU d'une révision dôme | 22,6–25,6 ms d'un coup | étapes ≤2,20 ms, commit ≤1,15 ms | hitch supprimé |
| Transition froide du dôme | 3,16 s | 2,37–2,56 s en fond | −19 à −25 % |
| Pic process de cette transition | 834,3 Mio | 741,6 Mio | −11,1 % |
| Mapping complet du dôme | médiane 1,1445 ms | cache idle 0,0010 ms | environ 1 145× |
| Cloisons du dôme, steady | 1,19 ms et 64,8 Kio/frame | 0,008 ms et 0 Kio | −99,3 % CPU |
| Écriture grille sans rapport, eau + meubles | 84,244 ms et 4,314 Mio | 0,067 ms et 3,7 Kio | invalidation évitée |
| Révision same-grid du dôme, commit | non étagé | 3,920 ms maximum | sous le budget de 4 ms |
| Révision same-grid Start, commit | non étagé | 3,792 ms maximum | sous le budget de 4 ms |
| Dôme MSAA4, VSync, 3 600 frames steady | nouveau mode | 59,4 FPS sans creux | 60 Hz tenu sur l'iGPU Intel |
| Pic process MSAA4 / SS3, même vue | — | 406,9 / 818–829,5 Mio | environ −50 % pour MSAA4 |

Le chiffre `0,199 ms` est le coût CPU/driver vu par le probe non plafonné, pas un « FPS jeu ». Sur la
machine, la vue et le scénario mesurés, il montre une marge très supérieure au budget de 16,67 ms ;
ce n'est pas une garantie générale de temps GPU sur un autre matériel.

### Contrôle ciblé du backend sprite — 17 août 2026

Une régression distincte a été mesurée en Debug sur Start, seed `12345`, fenêtre 1920×1080 et plan
post-révision de 60 contours / 2 099 points. Le choix de décalque était refait à chaque frame et les
surcouches vectorielles de mur (`WallSkinSkin` + rythme de tirets) étaient entièrement retessellées.

| Mesure steady | État signalé | Catalogue indexé seul | Catalogue + cache retenu |
|---|---:|---:|---:|
| Draw | ~56 ms | 53–55 ms | 15,5–16,1 ms |
| Allocations | ~7,05 Mio/frame | ~3,66 Mio/frame | 743–774 Kio/frame |
| Sommets soumis | ~824 k | ~824 k | ~824 k |

Le catalogue indexé enlève à lui seul environ 3,4 Mio d'allocations par frame. Le cache de surcouche
retient ensuite la tessellation par identité de scène/layout et par bucket visuel, avec deux variantes
LRU ; son chemin steady n'alloue rien. Le premier build d'une nouvelle variante reste synchrone : sur
le plan lourd, planification, tessellation et upload prennent environ 41,2 ms une fois, dont seulement
0,33 ms d'upload GPU. Le déplacer sur le worker de préparation, avec publication atomique, reste donc
une optimisation froide à faire ; ce coût ponctuel n'est pas présenté comme respectant le budget
d'upload de 4 ms.

À 1080p, les seules surfaces RGBA de la chaîne de supersampling représentent environ 158,2 Mio en
SS4, 89,0 Mio en SS3 et 31,6 Mio en SS2. Dans la comparaison historique du chemin supersamplé, passer
de SS4 à SS3 économisait donc environ 69,2 Mio de render targets avant même les allocations internes
du driver. Le défaut actuel est le MSAA4 natif décrit ci-dessous.

## Pourquoi le coût était anormal

Le problème ne venait pas d'une fatalité du vectoriel, mais d'une accumulation de travaux inutiles :

- SS4 rendait la scène en 7680×4320 et saturait le fill-rate sur les grandes surfaces ;
- les batches retenus du sol et des meubles couvraient tout le pont et étaient soumis même hors
  écran ;
- un trait arrondi ajoutait un disque complet de 16 triangles à chaque point interne ; ces disques
  représentaient 87 à 89 % des sommets des meubles ;
- le cœur profond de l'eau était peint une première fois en rive puis repeint ;
- les grains de sable et d'herbe étaient tessellés sous l'eau alors qu'ils étaient invisibles ;
- des caches d'eau et de meubles dépendaient de la révision globale de la grille ;
- les cloisons du dôme et les 65 536 `DisplayCell` étaient reconstruits à chaque frame ;
- la propagation de corruption scannait tous les ponts même avec une seule cellule active ;
- des buffers temporaires et des dumps synchrones alimentaient inutilement le GC et la console.

## Architecture finale

### 1. Antialiasing et composition

Le défaut est MSAA4 à résolution native. Si le driver n'accorde aucun multisampling, le runtime
revient en SS2. Les chemins historiques SS2, SS3 et SS4 restent disponibles comme overrides ; SS4
reste le mode Ultra :

```powershell
$env:THEEND_SS = '4'
dotnet run --project TheEnd.Client -c Release
```

Les valeurs `THEEND_SS` acceptées sont `2`, `3` et `4`. Une valeur absente ou invalide conserve le
défaut MSAA4. `THEEND_AA=msaa4` prend priorité lorsqu'il est défini en même temps qu'un override SS.

MSAA4 rend directement à la résolution de la fenêtre et demande quatre échantillons de couverture au
render target. La variable suivante permet de le forcer explicitement dans un script ou benchmark :

```powershell
$env:THEEND_AA = 'msaa4'
$env:THEEND_SS = $null
dotnet run --project TheEnd.Client -c Release
```

`THEEND_AA=msaa4` prend volontairement priorité sur une ancienne valeur `THEEND_SS`. Le driver peut
accorder 4 ou 2 échantillons ; le diagnostic Debug affiche la valeur réelle. S'il n'en accorde aucun,
la chaîne revient en SS2 au lieu de prétendre que MSAA est actif. Les captures golden ignorent ces
overrides et restent forcées en SS4, car leur feuille de crops dépend exactement d'une scène
7680×4320.

Sur l'iGPU Intel RaptorLake-S de la machine de mesure, le driver a accordé une scène
`1920×1080@4`, sans cible intermédiaire et avec `vectorScale=1`. Un run VSync de 600 frames de chauffe
puis 3 600 frames steady est resté entre 59,4 et 60,3 FPS dans chacune des 30 fenêtres de mesure,
avec un pic process de 406,9 Mio. Une répétition après les runs lourds a tenu 58,5 FPS de moyenne,
57,7 FPS dans sa pire fenêtre de 120 frames et 463,8 Mio de pic, sans gel. Dans le même protocole,
SS3 utilise une scène 5760×3240 et un intermédiaire 2880×1620 ; deux répétitions ont subi un gel de
53,7 à 61,0 s autour de la 2 040e frame steady, puis ont repris à 59,5 FPS, avec 818–829,5 Mio de pic.
Cela décrit ce backend/iGPU précis et doit être revalidé sur un autre driver.

MSAA4 couvre très bien les bords des triangles vectoriels, mais n'a que quatre niveaux de couverture.
Les traits nettement subpixel, les glyphes et les textures peuvent donc rester plus secs qu'en SS4.
La capture de contrôle `TestResults/msaa4-dome.png` valide le resolve DesktopGL et l'absence d'image
noire ; ce fichier est un artefact local ignoré par Git.

Les packages MonoGame sont épinglés en `3.8.5` pour rendre ce chemin de resolve reproductible. Toute
mise à jour doit refaire au minimum la capture MSAA, le resize et le run VSync soutenu avant de changer
cette version.

Les render targets utilisent `DiscardContents`, car chaque cible est entièrement réécrite avant
d'être lue. La scène est toujours initialisée par `GraphicsDevice.Clear`. En revanche, le blit opaque
plein écran tient lieu de clear pour la cible intermédiaire puis le backbuffer ; faire clear puis
blit doublait une part importante de la bande passante.

Les couches dont toutes les couleurs ont un alpha de 255 utilisent `VectorBlendMode.Opaque` : sol
retenu, structure statique, eau, meubles, cloisons, portes retenues et papier. Une couche contenant
de la glace, une prévisualisation translucide ou un autre alpha variable doit rester en
`AlphaBlend`. Ne jamais rendre `Opaque` globalement.

### 2. Révisions ciblées de la grille

`Grid` expose trois notions distinctes :

- `IdentityStamp` : identité stable de l'instance de grille ;
- `VersionStamp` : identité + toute écriture de contenu ;
- `WaterVersionStamp` : identité + changements de topologie de l'eau visible uniquement.

Le cache de meubles utilise l'identité de grille et la valeur des objets. Une écriture de mur,
d'atmosphère ou d'eau sans changement de mobilier ne le reconstruit plus. Le cache d'eau utilise
`WaterVersionStamp`; un mur ordinaire ne l'invalide pas, mais des débris qui masquent ou révèlent une
cellule d'eau l'invalident.

Une nouvelle donnée dérivée doit dépendre de la révision minimale qui décrit réellement son entrée.
Utiliser `VersionStamp` « par sécurité » sur un cache indépendant est une régression de performance.

### 3. Présentation incrémentale

`WorldPresentationCache` conserve le tableau `DisplayCell[,]` :

- les changements de terrain/structure/feature/atmosphère sont rejoués depuis le journal borné de
  `Grid` ;
- la corruption possède son propre journal ;
- seules les portes vivantes et les anciennes cellules de porte sont remappées ;
- seul l'ancien et le nouveau curseur changent ;
- remplacement de source, changement de dimensions ou overflow d'un journal déclenchent un remap
  complet sûr.

Les listes d'acteurs, de meubles, de mécanismes et de stocks sont également réutilisées. Le résultat
incrémental est testé contre `WorldPresenter.Map` sur des centaines de mutations aléatoires.

### 4. Eau

La géométrie d'un bassin respecte ces invariants :

- `shallow = shore XOR heart` ;
- `deep = heart` ;
- les deux bandes ne se recouvrent pas ;
- les cellules `FeatureKind.Water` ne dessinent ni grain, ni plaque, ni touffe de sol ;
- le wash de fond reste présent pour éviter un trou sous la rive ;
- le batch d'eau retenu est opaque ;
- une écriture de grille sans changement eau/non-eau ne rebake rien.

La vue centrée sur le grand lac et la vue dôme automatique terminent toutes deux autour de 0,20 ms
dans le probe SS3 final. Le surcoût de l'eau n'est plus le goulet observé auparavant.

### 5. Chunks du sol

Le sol statique est découpé en chunks monde de 32×32 cellules. Les sommets restent exprimés en
coordonnées monde : déplacer la caméra ne rebake rien. `VisibleCells` choisit les chunks soumis, avec
une marge qui couvre les détails dépassant leur cellule.

Les surfaces sont une passe distincte des brins d'herbe figés. Toutes les surfaces sont soumises
avant les brins, afin qu'une touffe inclinée au-delà d'une frontière de chunk ne soit pas recouverte
par le chunk voisin.

Le bake CPU est déterministe et utilise au maximum deux workers, ou `CPU - 1` sur une petite machine.
Quatre workers ont été mesurés plus lents et plus gourmands à cause de la pression mémoire ; ne pas
augmenter ce nombre sans nouvelle mesure.

### 6. Uploads étagés et publication atomique

Une révision terminée sur le worker n'est pas publiée immédiatement :

1. les chunks sont uploadés par groupes de 16 au maximum, avec un budget visé de 4 ms ;
2. les buffers monolithiques sont uploadés un par appel de `Prepare` ;
3. l'ancien pont complet, ou l'écran de chargement, reste affiché ;
4. seulement lorsque toutes les couches sont prêtes, leurs références sont échangées atomiquement ;
5. les anciens buffers sont ensuite libérés.

Une couche arbitrairement partielle reste interdite. L'unique exception est l'atome de structure
d'un clic mur pur sur le même pont : terrain et topologie des portes doivent être inchangés, et au
moins un mur doit avoir changé. Le worker construit d'abord sa `SceneGeometry`, son `WallLayout` et
le batch de structure exacts, puis les publie ensemble. L'ancien sol et les anciens décors restent
installés jusqu'au swap complet ; le feedback local est dessiné avant le nouvel atome afin qu'une
démolition découvre immédiatement son patch de sol. Le build complet adopte le même batch GPU, sans
second upload ni second propriétaire.

Une annulation, une demande plus récente ou une erreur rétracte cet atome emprunté et libère les
données CPU, les buffers GPU partiels et le snapshot, sans altérer la dernière révision complète.

Une variante LOD devenue obsolète est comparée à la demande courante avant tout nouvel upload. Si
elle n'est plus utile, elle est annulée immédiatement.

### 7. Annulation sans exception

Changer rapidement de zoom ou de pont annule normalement un bake. Ce n'est pas une erreur.

Les workers du renderer doivent observer `CancellationToken.IsCancellationRequested`, arrêter leur
boucle et retourner `null`. Ils ne doivent pas utiliser `ThrowIfCancellationRequested`, construire
une `OperationCanceledException`, ni passer le token à `ParallelOptions.CancellationToken` : Visual
Studio s'arrête sur l'exception de premier niveau avant que le wrapper puisse la traduire.

Les vraies erreurs continuent d'être capturées dans `WorkerResult.Error`, journalisées, puis la
dernière révision complète reste active.

### 8. Meubles : chunks, lazy build et LRU

Les meubles sont groupés par chunk d'ancre de 16 cellules. Le bound de culling est l'union des
empreintes réelles, élargie d'une cellule. Cela évite les trous lorsqu'un meuble dépasse son chunk
d'ancrage.

Un chunk n'est tessellé et uploadé qu'à sa première apparition. Un pan vers une zone inconnue crée
uniquement les nouveaux chunks ; revenir en arrière ne reconstruit rien. Les variantes de zoom sont
limitées par une LRU de taille 2.

Les buckets de zoom doivent contenir tous les seuils de branche des skins. Les seuils actuels sont
notamment 20, 24, 28, `>40` pour les couchettes et 48. Le bucket 41–47 utilise donc 42 ; fusionner ce
bucket avec 32 réintroduirait une régression visuelle.

Après un pan de mesure :

- dôme : 8 buffers, 87 774 sommets retenus, environ 1,34 Mio GPU ;
- Start : 22 buffers, 290 853 sommets retenus, environ 4,44 Mio GPU ;
- retour caméra : 0,003 à 0,013 ms, aucune allocation.

### 9. Tessellation des traits

`StrokeTessellator` est commun au renderer live et au builder retained. Pour un trait demandé avec
`roundCaps: true`, il produit :

- un quad par segment non nul ;
- seulement le wedge extérieur nécessaire à un joint ;
- deux demi-caps pour une polyligne ouverte ;
- aucun cap d'extrémité pour une boucle fermée ;
- 6 à 16 segments d'arc selon le rayon final à l'écran ;
- aucune allocation de tableau intermédiaire.

Avec `roundCaps: false`, seuls les quads des segments sont émis. Les doublons et segments nuls sont
ignorés. Les deux voies doivent produire une géométrie bit pour bit identique à `CellSize` ou bucket
identique. Un cache retained contenant des traits arrondis doit inclure le bucket d'arc dans sa clé,
ou prouver par test que sa résolution reste constante sur toute sa plage de zoom. Remettre un disque
complet à chaque point est interdit : c'était 87 à 89 % des sommets des meubles.

### 10. Cloisons du dôme

`DomePartitionSkin` retient son batch. Il l'invalide seulement lorsque changent :

- le design ou le pont ;
- l'état narratif pertinent ;
- l'empreinte de présence des seuls carriers publiés par `DomePartitionGesturePlan` dans le nouveau
  snapshot `WallWeb` ;
- une cellule sondée qui influence réellement une cloison ou son raccord à l'enveloppe.

L'identité brute du snapshot n'est pas une clé : une modification de mur sans rapport republie un
`WallWeb`, mais conserve le batch si la présence de ses cellules de cloison est identique. La
géométrie, elle, vient du plan de gestes H/V/45° publié par Core, jamais des coudes du raster de
collision. Le chemin chaud teste d'abord l'identité déjà vue, puis ne calcule l'empreinte qu'à
l'arrivée d'un nouveau snapshot.

Le régime stable ne doit ni retesseller, ni allouer. Un rebuild mesuré coûte environ 0,62 ms ; le
steady est à 0,008 ms.

### 11. Corruption

`CorruptionField` maintient une frontière compacte des cellules actives et un journal de
changements. `CorruptionSpreadSystem` choisit :

- la voie sparse sous un sixième du pont actif ;
- la voie dense au-delà.

La voie sparse trie les sources et les cellules touchées afin de préserver exactement l'ordre
y-major historique, les additions flottantes et la séquence des événements `RoomCorruptedEvent`.
Sur le dôme Release :

- 1 cellule : 0,0005 ms contre 0,1664 ms dense ;
- 1 % actif : 0,0384 ms contre 0,1754 ms ;
- 10 % actif : 0,2537 ms contre 0,2770 ms ;
- front dense : environ 0,81 ms.

Après chauffe, les deux voies n'allouent rien.

### 12. Allocations et diagnostics

Les buffers temporaires du papier, des acteurs et des features sont réutilisés quand leur durée de
vie est celle du renderer. `LeakSkin` réutilise notamment ses quatre ensembles de cellules déjà
dessinées.

En Debug, `F1` active/désactive le rendu non plafonné. Le titre de la fenêtre affiche FPS, temps
draw/update, sommets, Kio/frame et niveau de supersampling.

Les dumps complets de relations et d'esprits font des écritures console synchrones et sont désactivés
par défaut, même en Debug. Pour les activer explicitement :

```powershell
$env:THEEND_DEV_DUMPS = '1'
```

## Ownership et invariants de sûreté

Tout changement de cache doit préserver les règles suivantes :

1. `VectorBatchData` possède son tableau loué jusqu'à `Upload` ou `Dispose` ; les deux chemins rendent
   exactement une fois le tableau à l'`ArrayPool`.
2. Un `StaticVectorBatch` appartient à un cache, à une variante LRU ou à un upload partiel, jamais à
   deux propriétaires simultanément.
3. Le propriétaire dispose le buffer lors d'une éviction, mutation, annulation, erreur ou destruction
   du runtime.
4. Les presets partagés `BlendState` ne sont jamais possédés ni disposés par un batch.
5. Un worker ne touche jamais au `GraphicsDevice`.
6. Un snapshot lu par un worker n'est jamais recyclé avant la fin réelle de sa tâche.
7. Une révision complète n'est installée que lorsque toutes ses couches sont prêtes. L'atome anticipé
   `SceneGeometry`/`WallLayout`/cellules/structure d'un changement mur pur est la seule publication
   intermédiaire autorisée ; ses quatre éléments ont la même révision, sont annulés ensemble et
   restent limités aux 64 cellules que le feedback de démolition peut recouvrir exactement.
8. Un pan ne doit jamais invalider une géométrie exprimée en coordonnées monde.
9. Une optimisation sparse doit rester exactement équivalente à sa référence dense, y compris ordre
   d'événements et bits des flottants.

## Comment refaire une mesure

### Mesure interactive intégrée

```powershell
dotnet build TheEnd.sln -c Debug --no-restore
$env:THEEND_SS = '3'
dotnet run --project TheEnd.Client -c Debug --no-build
```

Appuyer sur `F1`, cadrer la zone à mesurer, attendre la chauffe des caches, puis relever plusieurs
fenêtres de 0,5 s dans le titre. Comparer toujours le même seed, le même pont, le même zoom et la même
caméra. C'est cette mesure intégrée qu'une autre machine peut reproduire ; la matrice exhaustive du
probe temporaire n'est pas versionnée.

### Capture déterministe

```powershell
dotnet build TheEnd.Client\TheEnd.Client.csproj -c Release --no-restore
$env:THEEND_AA = 'msaa4'
$env:THEEND_SS = $null
$env:THEEND_SHOT = "$PWD\TestResults\renderer-check.png"
dotnet run --project TheEnd.Client -c Release --no-build
```

Ajouter `$env:THEEND_SHOT_HOME = '1'` pour cadrer Start. Vérifier au minimum : contours du dôme,
frontières de chunks, eau, racks, cryopods, coins arrondis et ordre des couches. Cette capture contient
`Targets.Scene` ; elle ne valide pas le blit vers le backbuffer final. En mode supersampling, elle ne
valide pas non plus l'intermédiaire de downsample. Un contrôle de la fenêtre reste nécessaire pour ces
étapes.

En MSAA4, `Present` délie d'abord la scène et déclenche son resolve avant que le harnais appelle
`SaveAsPng`; la capture obtenue fait donc 1920×1080. Pour reconstruire la feuille golden, définir
`THEEND_GOLDEN=1` : ce mode force SS4 et produit toujours les 7680×4320 attendus, quels que soient les
overrides AA/SS hérités du shell.

### Validation automatisée

```powershell
$changedCs = @(
    git diff --name-only --diff-filter=ACMRTUXB -- '*.cs'
    git ls-files --others --exclude-standard -- '*.cs'
) | Where-Object { $_ } | Sort-Object -Unique
if ($changedCs.Count -gt 0) {
    dotnet format TheEnd.sln --no-restore --verify-no-changes --include $changedCs
}
dotnet build TheEnd.sln -c Release --no-restore
dotnet test TheEnd.Tests\TheEnd.Tests.csproj -c Release --no-build
dotnet build TheEnd.sln -c Debug --no-restore
dotnet test TheEnd.Tests\TheEnd.Tests.csproj -c Debug --no-build
```

La validation consolidée avant le mode MSAA comptait 2 171 tests réussis et 1 test historique ignoré
dans chacune des configurations `Release` et `Debug`. La première validation complète du contrat
MSAA4 a ensuite compté 2 185 réussites et le même test ignoré dans les deux configurations. Après sa
promotion comme défaut et l'intégration des derniers contrats de rendu, la suite `Release` du
12 août 2026 compte 2 211 réussites, 1 test historique ignoré et aucun échec. Les tests d'annulation
écoutent aussi les exceptions de premier niveau afin de reproduire le comportement du débogueur, pas
seulement l'exception finale vue par l'appelant.

## Checklist avant d'ajouter un skin ou un cache

- La géométrie est-elle statique, animée ou dépendante du zoom ?
- Peut-elle être exprimée en coordonnées monde et retenue ?
- Son cache dépend-il d'une identité, d'une révision ciblée ou réellement de toute la grille ?
- Le pan peut-il se limiter à un culling par bounds ?
- Toutes ses couleurs ont-elles un alpha de 255 avant de choisir `Opaque` ?
- Les seuils visuels exacts figurent-ils dans la clé/bucket LOD ?
- Le premier build visible respecte-t-il 4 ms, sinon peut-il être lazy ou étagé ?
- L'annulation retourne-t-elle silencieusement sans exception de contrôle ?
- Chaque buffer CPU/GPU possède-t-il un propriétaire unique et un chemin de disposal pour succès,
  annulation, erreur et éviction ?
- Un test compare-t-il le cache à une voie de référence complète ?
- Une capture vérifie-t-elle les seams, l'ordre des couches et les changements de zoom ?
- Le benchmark compare-t-il le même seed, zoom, viewport et état de chauffe ?

## Limites connues et assumées

- Le bake froid du dôme reste à environ 2,4–2,6 s sur la machine de mesure. Il est en arrière-plan et
  n'interrompt plus la frame, mais il n'est pas instantané.
- Le premier build lazy des meubles d'un viewport/bucket inconnu reste synchrone : environ 16,6 ms
  sur le dôme et 5,0 ms sur Start dans le probe final. Le retour dans une variante LRU chaude tombe à
  0,003–0,013 ms. Si ce coût redevient visible avec davantage de mobilier, le prochain chantier est
  un staging ou un worker par chunk, pas la suppression du culling.
- SS4 reste coûteux en fill-rate et en mémoire. Il s'agit d'un mode Ultra explicite, pas du défaut.
- Le sol est entièrement tessellé sur le worker avant publication ; les chunks réduisent surtout la
  soumission GPU. Un futur bake réellement visible-first serait plus complexe et n'est justifié que
  par une nouvelle mesure.
- La frame Release finale alloue encore environ 7,6 Kio dans le probe dôme/eau. Ce résidu est très
  inférieur au budget et ne justifie pas à lui seul une complexité de cache supplémentaire.
- Les temps absolus doivent être rebaselinés après un changement de matériel, de driver, de version
  MonoGame, de résolution ou de densité de mobilier.

## Fichiers pivots

- `TheEnd.Client/Renderer/Runtime/StaticDeckCache.*` : workers, variantes, staging et publication ;
- `TheEnd.Client/Renderer/Runtime/FloorChunks.cs` : layout, bake parallèle, culling et upload
  incrémental ;
- `TheEnd.Client/Renderer/Fixtures/FixtureFrameCache.cs` : chunks lazy et buckets de zoom ;
- `TheEnd.Client/Renderer/Vector/StrokeTessellator.cs` : grammaire commune des traits ;
- `TheEnd.Client/Display/WorldPresentationCache.cs` : mapping incrémental ;
- `TheEnd.Client/Renderer/Structures/DomePartitionSkin.cs` : cache des cloisons ;
- `TheEnd.Client/Renderer/Environment/LeakSkin.Water.cs` : géométrie et cache d'eau ;
- `TheEnd.Core/World/Grid.cs` : identités et journaux de changements ;
- `TheEnd.Core/Corruption/CorruptionField.cs` et
  `TheEnd.Core/Systems/CorruptionSpreadSystem.cs` : frontière active et propagation hybride.
