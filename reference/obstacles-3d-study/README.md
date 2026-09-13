# Rochers et débris — études 3D et intégration

Reprise du 11 septembre 2026, après l'intégration de la porte. Les formes de
rochers montrées sont appréciées et conservées : « Les rochers ça va ». La première
version des quatre familles de débris a été rejetée : « les débris par contre
c'est très moche pas du tout de la même qualité que le reste ».

**La direction visuelle v2 est approuvée : « Oui c'est bien cette direction ».
Elle est désormais transposée en quatre nouveaux modèles de débris et trois
fragments de composition.** Après examen natif, l'utilisateur autorise le
12 septembre 2026 l'intégration normale des rochers et des débris :
**« Bon écoutes ça a l'air pas mal donc on va l'intégrer comme ça et je regarderais »**.

Les banques sont installées dans `TheEnd.Client/Assets/models/rock` et
`TheEnd.Client/Assets/models/debris`. Le rendu ordinaire utilise ces modèles
pour tous les amas en mode sprite avec les murs en volume. Le repli existant est
conservé en mode vectoriel, avec les murs plats ou si la banque correspondante
est indisponible. L'intégration ne modifie ni les cellules ni les règles de
déblaiement, de construction ou de déplacement. Les contrôles d'intégration
passent ; l'utilisateur poursuivra son examen dans le jeu.
Les preuves de la version rejetée restent conservées comme historique.

- [Quatre formes de rochers appréciées dans le jeu](rock-variants.png).
- [Direction visuelle de débris approuvée](debris-art-direction-v2.png), image
  générée ; [progression, provenance et prompt](debris-art-direction-v2.md).
- Nouvelle passe native : [planche v3](debris-native-v3.png), créée et inspectée
  avec les captures [mobilier](debris-v3-furniture.png),
  [console](debris-v3-console.png), [armoire](debris-v3-rack.png) et
  [verrière](debris-v3-canopy.png). La [répartition naturelle](debris-v3-natural.png)
  est capturée séparément.
- [Quatre familles de débris rejetées dans le jeu — preuve historique](debris-variants.png).
- [Comparaison historique au rendu 2D](comparison.png) : rocher `rounded` mis en
  scène et anciens débris avec leur choix naturel (mobilier, armoire, armoire).
- Captures du jeu ordinaire : [débris intégrés](integration-debris.png) et
  [rochers intégrés](integration-rock.png), avec les [preuves de comparaison](integration-check.json).

## Sources éditables

| Famille | Source dans TheEnd-Art | Variantes `body` |
| --- | --- | --- |
| Rochers | `objects/rock/rock-study.blend` | `rounded`, `split`, `slab`, `jagged` |
| Débris | `objects/debris/debris-study.blend` | `furniture`, `console`, `rack`, `canopy` |

La source des débris contient aussi les variantes `scrap/beam`, `scrap/panel` et
`scrap/module`, dérivées de véritables éléments des équipements. Le mobilier
possède un plateau épais et des supports pliés ; la console un écran fissuré
encastré et un boîtier délogé ; l'armoire des profils épais et deux modules
déplacés ; la verrière des cadres, joints, fixations et éclats retenus.

Chaque banque utilise un seul os `Root` et une pose `idle`, sans boucle. Les images
de matière sont réutilisées, packées et documentées dans les dossiers Art. Les
sources sauvegardées, leurs UV et leurs matériaux sont éditables ; les scripts
locaux de construction ne doivent pas être rejoués sur une source retouchée.

Sources actuelles, exportées et validées avec une erreur de skinning nulle :

- Rocher : `a5a9320d7d61a2e7ab720408db8fdcd63aa49ec97959f32dbd38663ede62b12e`.
- Débris : `19561aa99c31cb35d26ea378871295c4752a9bec9d9d917a37f23463a909af12`.

Le hash `1adf04f36d1c8ca65c7b0ef78fd1f0aaa7e873b0142e22b1c5e0b4901523224b`
désigne les quatre débris rejetés de `debris-variants.png`, pas les modèles actuels.
La reconstruction a d'abord repris la peinture de la porte directement ; son
grain s'est révélé excessif en capture native. Le matériau ardoise utilise
maintenant directement `objects/cryopod/textures/hull-paint.png`. Cette correction
de matière conserve la géométrie, les UV, le rig et les clips. L'usure localisée
des arêtes et des ruptures reste portée par les pièces construites.

Les PNG de la première passe sont des captures natives. Leurs planches recadrent et agrandissent chaque paire
ou série de façon identique, sans retoucher les objets. Les JSON voisins indiquent
le hash du `.blend`, l'exporteur, les cellules et la variante naturelle ou forcée.
La nouvelle passe détaille les `Poses` de chaque patch : `Part`, `Style`, matrices
et bornes projetées de chaque corps ou fragment. `BodyVisualBounds` désigne
explicitement les bornes du corps principal. Chaque capture v3 possède son fichier
voisin `.png.obstacle-study.json`. Un aperçu Blender sert seulement à inspecter
la construction : son éclairage n'est pas celui du jeu.

La planche native v3 prélève le même rectangle de 220×180 pixels, de (865,390) à
(1085,570), puis l'agrandit entièrement ×2 sans retouche. Les anciennes planches
de variantes prélèvent une zone native de 180×155 pixels et
l'agrandissent entièrement ×2 : origine (950,410) pour les rochers et (885,395)
pour les débris. Le comparatif 2D/3D utilise respectivement (880,365) et (800,390),
sur 300×250 pixels agrandis ×2. Aucune forme n'est redimensionnée séparément.

## Répartition et échelle

`ObstacleModelLayout` fournit une répartition commune au rendu ordinaire et au
diagnostic : sélection des composantes cardinales, variantes, patches et poses.
`ObstacleModelPresentation` prépare tous les amas du pont et conserve ce résultat
en cache selon `Grid.StructureVersionStamp`. `ObstacleModelRenderer` est partagé
par les deux présentations. L'ancien dessin et ses détails préparés en cache ne
sont masqués que pour les composantes dont la banque est disponible.

Le diagnostic sélectionne une composante du type demandé et la remplace par la
banque d'essai. Cette composante est exclue du rendu de production pour éviter
un doublon. Les autres amas utilisent les banques installées, avec les mêmes
règles de repli que le rendu ordinaire.

Pour les rochers, une silhouette représente l'amas entier avec l'échelle uniforme
en XY `1.6 × (0.42 + 0.19 × sqrt(nombre de cellules))` ; l'échelle de Z est
plafonnée à 2. Leur source et cette présentation sont conservées. Le choix de forme
et l'orientation proviennent de l'ancrage spatial, afin de rester stables pendant
le cadrage.

Pour les débris, la partition connexe existante en patches de 3×3 au maximum est
réutilisée. Le choix conserve les quatre familles du dessin existant : mobilier,
console, armoire et verrière. Chaque patch reçoit un corps principal à l'échelle
uniforme XYZ `s = min(2, min(largeur, hauteur)) × PlanarFit`. L'axe X long du modèle
suit l'axe long du patch ; le facteur d'ajustement de la rotation agit aussi sur Z
et conserve les proportions de l'équipement. La projection habituelle de la grille
multiplie ensuite Y par `sqrt(2)`.

Les patches grands ou longs sont composés d'un corps et de deux fragments au
maximum, choisis parmi panneau, traverse et module. Les fragments sont ancrés
sur des cellules occupées et gardent une échelle uniforme de 1 avant la projection
de grille. Leurs formes, placements et rotations restent stables. Les cellules
irrégulières demeurent l'empreinte logique : les modèles n'ajoutent pas de collision.

Le cadrage natif de référence utilise une grille 256×256, pont d'index 0. Le rocher
est l'amas de huit cellules ancré en (92,71), dans un rectangle 4×3. Les débris sont
l'amas de neuf cellules ancré en (203,191), dans un rectangle 4×4, réparti en trois
patches. Ces coordonnées décrivent ces captures ; les JSON font foi si la carte
ou sa génération change.

## Refaire un essai

Pour ouvrir le banc interactif, depuis `TheEnd` :

```powershell
.\scripts\run-obstacle-study.ps1
```

La fenêtre se cadre sur un amas réel de débris, prépare une capture initiale,
puis reste ouverte avec les commandes du jeu. Molette : zoom ; clic-molette
maintenu : déplacer la caméra ; Espace : pause ; Échap : fermer.
`-Variant console` (ou `furniture`, `rack`, `canopy`) force une famille pour
la comparaison. `-Feature Rubble` ouvre l'essai des rochers ; `-NoBuild`
réutilise le client déjà compilé. Le diagnostic remplace seulement la composante
sélectionnée, avec ses fragments, et exclut son doublon de production. Les autres
amas utilisent leur banque installée lorsque le mode et sa disponibilité le
permettent.
Le maintien ouvert utilise `THEEND_SHOT_KEEP_OPEN=1` ; une capture sans ce
paramètre se ferme toujours automatiquement. Les variables restent limitées
au processus enfant.

Depuis `TheEnd-Art`, exporter, valider et installer les sources sauvegardées :

```powershell
.\tools\models\build-model.ps1 -Source objects/rock/rock-study.blend -InstallAs models/rock
.\tools\models\build-model.ps1 -Source objects/debris/debris-study.blend -InstallAs models/debris
```

Omettre `-InstallAs` pour produire seulement une banque externe d'essai. Le
diagnostic ci-dessous peut toujours charger cette banque sans la réinstaller.

Depuis `TheEnd`, compiler le client :

```powershell
dotnet build TheEnd.Client/TheEnd.Client.csproj -c Debug
```

Ce bloc PowerShell crée une capture dans un dossier unique. Adapter `$workspace`,
`$feature`, `$model` et éventuellement `$variant`. Laisser `$variant` à `$null`
pour le choix naturel. Une variante explicite met en scène ce corps sur tous les
patches du sujet, en conservant le choix naturel des fragments ; elle sert à
comparer le dessin, pas sa répartition.

```powershell
$workspace = 'C:\workspace'
$feature = 'Rubble' # ou HeavyDebris
$model = 'rock-study' # ou debris-study
$variant = $null # rounded/split/slab/jagged ou furniture/console/rack/canopy
$gameRoot = Join-Path $workspace 'TheEnd'
$bank = Join-Path $workspace ('TheEnd-Art/exports/' + $model)
$captureRoot = Join-Path $gameRoot ('.artifacts/obstacles-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $captureRoot | Out-Null
$shot = Join-Path $captureRoot 'final.png'
$start = [Diagnostics.ProcessStartInfo]::new()
$start.FileName = Join-Path $gameRoot 'TheEnd.Client/bin/Debug/net9.0/TheEnd.Client.exe'
$start.WorkingDirectory = $gameRoot
$start.UseShellExecute = $false
$start.WindowStyle = [Diagnostics.ProcessWindowStyle]::Hidden
foreach ($key in @($start.Environment.Keys)) {
    if ($key.StartsWith('THEEND_')) { $start.Environment.Remove($key) | Out-Null }
}
$settings = @{
    THEEND_BACKEND = 'sprite'
    THEEND_WIDTH = '1920'
    THEEND_HEIGHT = '1080'
    THEEND_LANGUAGE = 'fr'
    THEEND_UI_SCALE = '1'
    THEEND_SHOT_ZOOM = '16'
    THEEND_WALL_VOLUME = '1'
    THEEND_SHOT_FEATURE = $feature
    THEEND_SHOT = $shot
    THEEND_OBSTACLE_STUDY = $feature
    THEEND_OBSTACLE_STUDY_BANK = $bank
}
if ($null -ne $variant) { $settings.THEEND_OBSTACLE_VARIANT = $variant }
foreach ($entry in $settings.GetEnumerator()) { $start.Environment[$entry.Key] = $entry.Value }
$start.RedirectStandardOutput = $true
$start.RedirectStandardError = $true
$capture = [Diagnostics.Process]::Start($start)
$stdout = $capture.StandardOutput.ReadToEndAsync()
$stderr = $capture.StandardError.ReadToEndAsync()
$deadline = [DateTime]::UtcNow.AddMinutes(10)
while (-not $capture.WaitForExit(1000)) {
    if ([DateTime]::UtcNow -gt $deadline) {
        throw "Capture encore active, PID $($capture.Id). L'inspecter avant de relancer."
    }
}
($stdout.GetAwaiter().GetResult() + $stderr.GetAwaiter().GetResult()) |
    Set-Content -LiteralPath (Join-Path $captureRoot 'capture.log') -Encoding utf8
if ($capture.ExitCode -ne 0) { throw "Capture échouée : $captureRoot/capture.log" }
if (-not (Test-Path -LiteralPath $shot)) { throw 'Capture finale absente.' }
Write-Output $captureRoot
```

Pour retrouver le rendu ordinaire installé dans le même cadrage, retirer les
paramètres `THEEND_OBSTACLE_*` du bloc. Cela conserve les modèles 3D installés
en mode sprite avec les murs en volume. Le repli reste celui du mode vectoriel,
des murs plats ou d'une banque indisponible. Les variables restent limitées au
processus enfant.
La capture refuse un sujet absent, une famille manquante, un mode incompatible ou
un modèle qui n'a pas effectivement été dessiné.

## Contrôles et suite

Lors de la reconstruction et de la composition des débris, avant leur
intégration normale, la compilation Debug passait sans avertissement ni erreur
et les **77 tests ciblés passaient**. Les cinq captures natives v3 et leur planche
ont été produites et inspectées. Le contrôle natif du rocher conservé était
identique pixel à pixel, sur l'image complète, à `rock-rounded.png`. Ces résultats
décrivent cette étape historique du diagnostic.

Les deux banques installées le 12 septembre sont exportées et validées avec un
os `Root`, une pose `idle` et une erreur de skinning nulle. Leurs fichiers runtime
correspondent aux exports validés ; les sources et leurs hashes sont inchangés.
La compilation Debug passe sans avertissement ni erreur et la suite complète
réussit : **4 564 tests, aucun échec ni test ignoré**, en 9 min 32 s.
Les contrôles ajoutés couvrent toutes les composantes, le déblaiement, les
changements de pont/grille, les banques absentes, les exclusions du diagnostic,
les enveloppes des assets et l'absence d'allocation sur une préparation inchangée.

Les captures `integration-debris.png` et `integration-rock.png` utilisent les
banques installées, sans `THEEND_OBSTACLE_*`. Leurs zones de sujet sont identiques
pixel à pixel aux références retenues : (840,415)–(1035,605) pour les débris et
(950,410)–(1130,565) pour le rocher. L'image complète de débris est aussi identique
à [la capture avec diagnostic](integration-debris-study.png), confirmant le
rendu partagé et l'absence de doublon. `integration-check.json` conserve les
hashes des images/manifests, la provenance, le cadrage et ces comparaisons.

Pour relancer la suite complète :

```powershell
dotnet test TheEnd.Tests/TheEnd.Tests.csproj -c Debug --no-restore
```

La commande utilisée à l'étape du diagnostic ciblait la stabilité des familles
et orientations, les composantes entières, les patches étroits, le masque du
cache et le repli sans diagnostic :

```powershell
dotnet test TheEnd.Tests/TheEnd.Tests.csproj -c Debug --filter 'FullyQualifiedName~ObstacleStudy|FullyQualifiedName~StaticLeakPreparationTests|FullyQualifiedName~HeavyDebrisSkinTests|FullyQualifiedName~FrameCapture|FullyQualifiedName~DoorClearanceCaptureTests'
```

La direction ImageGen approuvée est conservée dans `debris-art-direction-v2.png`.
Sa transposition 3D est désormais intégrée à la demande de l'utilisateur ; les
captures natives v3 documentent la proposition examinée avant cette intégration.
Les preuves précédentes restent historiques. Les formes de rochers appréciées
sont conservées. L'examen en jeu se poursuit sur plusieurs lieux et sur les
occultations avec les personnages, au fil des retours de l'utilisateur.
La porte approuvée conserve sa source, ses états et son intégration.

Références Atlas : `theend/meta/process-fabrication-modeles-3d.md` et
`wizishop/save-Codex/chantier-theend-fabrication-3d-portes.md`.
