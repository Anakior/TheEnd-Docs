# Débris — direction visuelle et intégration

[Planche de recherche](debris-art-direction-v2.png).

**Direction visuelle validée le 11 septembre 2026 : « Oui c'est bien cette direction ».** La planche reste une image générée, ni une capture du moteur ni un export Blender. Sa transposition est maintenant construite en quatre modèles 3D et trois fragments de composition. Après examen natif, l'utilisateur autorise leur intégration avec les rochers le 12 septembre : **« Bon écoutes ça a l'air pas mal donc on va l'intégrer comme ça et je regarderais »**. L'examen dans le jeu se poursuit. Les quatre modèles précédents restent rejetés artistiquement : « les débris par contre c'est très moche pas du tout de la même qualité que le reste ». Les rochers sont conservés sur la base montrée : « Les rochers ça va ».

## Transposition réalisée

La source `TheEnd-Art/objects/debris/debris-study.blend` contient les corps
`body/furniture`, `body/console`, `body/rack` et `body/canopy`, ainsi que
`scrap/beam`, `scrap/panel` et `scrap/module`. Les nouveaux équipements possèdent
des profils épais, des panneaux encastrés, des mécanismes reconnaissables, des
sections déformées et une usure placée sur les ruptures. Les fragments sont
dérivés de leurs véritables pièces. La source finale porte le SHA-256
`19561aa99c31cb35d26ea378871295c4752a9bec9d9d917a37f23463a909af12`.

La peinture de porte utilisée lors de la reconstruction avait un grain trop
présent dans le moteur. La matière ardoise a donc été réaffectée directement à
`objects/cryopod/textures/hull-paint.png`, en conservant les meshes, les UV, le rig
et les clips. Les cavités graphite, les fixations discrètes et l'usure géométrique
des arêtes restent présentes.

La présentation conserve les proportions XYZ des débris :
`s = min(2, min(largeur, hauteur)) × PlanarFit`, puis projection de grille avec Y
multiplié par `sqrt(2)`. Un patch reçoit un corps et jusqu'à deux fragments sur
ses cellules occupées ; familles et rotations sont stables. L'export conserve
un seul `Root` et la pose `idle` et passe la comparaison avec une erreur de
skinning nulle. Lors de cette reconstruction, avant l'intégration normale,
**77 tests ciblés passaient**, avec une compilation Debug sans avertissement ni
erreur. Ces résultats concernent cette étape historique du diagnostic.

La [planche native v3](debris-native-v3.png) est créée et inspectée à partir
des captures `debris-v3-furniture.png`, `debris-v3-console.png`,
`debris-v3-rack.png` et `debris-v3-canopy.png`. La capture `debris-v3-natural.png`
complète cette comparaison par la répartition naturelle ; chaque PNG possède son
JSON. Le recadrage commun prélève (865,390)–(1085,570), soit 220×180 pixels
agrandis ×2 sans retouche. Les preuves décrivent chaque `Pose` par part, style,
matrice et bornes ; `BodyVisualBounds` identifie le corps principal. Les
[commandes autonomes](README.md#refaire-un-essai) permettent de refaire l'export,
l'installation ou une capture avec une banque externe d'essai.

À cette étape du diagnostic, un contrôle natif du rocher conservé reproduisait
`rock-rounded.png` à l'identique, pixel à pixel sur l'image complète. Sa source,
ses variantes et ses règles de pose sont conservées pour l'intégration.

## Intégration du 12 septembre

Les banques sont installées dans `TheEnd.Client/Assets/models/rock` et
`TheEnd.Client/Assets/models/debris`, depuis les sources sauvegardées inchangées.
Le rendu ordinaire les utilise pour tous les amas en mode sprite avec les murs
en volume. `ObstacleModelLayout` partage les variantes et poses entre production
et diagnostic ; `ObstacleModelPresentation` prépare les amas et les conserve en
cache selon `Grid.StructureVersionStamp`. `ObstacleModelRenderer` assure leur
rendu commun.

L'ancien dessin est masqué seulement si la banque correspondante est disponible.
Le repli existant reste actif en mode vectoriel, avec les murs plats ou en
l'absence de banque. Le diagnostic remplace une seule composante et exclut son
doublon de production ; les autres amas utilisent les assets installés. Le
lanceur `scripts/run-obstacle-study.ps1` et les banques externes d'essai restent
disponibles. Les cellules et les règles de jeu ne changent pas.

Les exports installés sont validés avec une erreur de skinning nulle et leurs
fichiers runtime correspondent aux exports. Les 4 564 tests Debug passent.
Les captures du jeu ordinaire [débris](integration-debris.png) et
[rocher](integration-rock.png) retrouvent exactement les pixels des sujets retenus.
La comparaison de l'image complète avec le diagnostic confirme l'absence de
doublon ; détails et hashes dans [integration-check.json](integration-check.json).

## Direction proposée

La recherche reprend la qualité des profils, de la peinture et de l'usure de la porte approuvée. Elle garde les quatre familles et remplace les grandes plaques plates par des équipements dont la construction reste reconnaissable : mobilier à structure épaisse, console à cadre et modules, armoire ouverte avec casiers déplacés, verrière à joints et fixations. Les dégâts se placent aux assemblages et dans l'épaisseur, avec tôles pliées, arêtes déchirées et pièces imbriquées. La matière associe acier peint gris ardoise, cavités graphite, usure ponctuelle et accents de laiton discrets.

Le dessin, le relief, l'usure, la quantité de petits débris et la caméra de cette image sont approximatifs. Ils ne fixent pas l'empreinte de collision, les dimensions ni les occultations du jeu. La transposition doit être appréciée avec les vrais modèles, les UV et le rendu natif ; le rendu généré ne garantit pas la fidélité de l'export.

Au moment de la génération de cette référence, les sources Blender, les banques externes et le code du diagnostic n'avaient pas été modifiés. Leur reprise a suivi la validation de la direction. Les captures antérieures restent les preuves des modèles rejetés, associés au hash `1adf04f36d1c8ca65c7b0ef78fd1f0aaa7e873b0142e22b1c5e0b4901523224b`. Les rochers et la porte approuvés sont conservés.

## Audit ayant guidé la reconstruction

L'audit des modèles rejetés relève un étirement XY×3 avec Z×1 dans le grand patch,
qui aplatissait les équipements. La nouvelle composition conserve les proportions
des pièces. Les anciennes UV projetées et la peinture mélangée à 70 % de couleur
constante ne plaçaient pas l'usure sur les ruptures ; la reconstruction porte les
épaisseurs, les recouvrements et les variations locales dans les vrais modèles.

La source réussie du cryopod fournit des conventions et pièces réutilisables :
carénage, boîtier de service, panneau de commande, cadre et joint de verrière,
guides et fixations. Le moteur conserve l'albédo et les normales géométriques,
mais pas les normal maps, la rugosité ou les ombres de cavité du studio Blender.
Le diagnostic impose des matériaux opaques ; la verrière reconstruite emploie des
éclats bleu-gris opaques, des fissures et des chants géométriques pour rester dans
ce contrat.

## Provenance

- Outil intégré `image_gen.imagegen`, une génération avec références, sans CLI.
- Original : `C:/Users/anaki/.codex/generated_images/01a0915e-83fb-73d2-8ed5-4be654015111/exec-2e40b7c2-fdb7-44c4-a802-6c75402c542c.png`.
- Copie sans retouche : `debris-art-direction-v2.png`, PNG RGB de 1 254 × 1 254 pixels.
- SHA-256 : `71ca5d3351ced7f5584406c082a32fa2848c821b19e1aeebe7e056410611c824`.
- Référence de qualité : `TheEnd-Docs/reference/door-3d-study/door-welded.png`, capture native approuvée.
- Référence du décor et de la caméra : `TheEnd-Docs/reference/obstacles-3d-study/debris-3d.png`, capture native antérieure.
- Contre-exemple et familles à conserver : `TheEnd-Docs/reference/obstacles-3d-study/debris-variants.png`, quatre modèles rejetés.

## Prompt final

```text
Use case: stylized-concept.
Asset type: ONE polished game environment art-direction contact sheet, four panels in a 2 by 2 layout, for redesigning destroyed spaceship equipment. This is a painted VISUAL PROPOSAL for future editable 3D models, not a working game screenshot.

Input references:
Image 1 is the APPROVED game's door and wall close-up: use its mature painted industrial construction, thick layered dark steel profiles, restrained edge wear, tiny brass details and integrated materials as the QUALITY AND STYLE reference. Do not copy the door as debris.
Image 2 is the actual game: use the same overhead orthographic camera and dark worn steel floor, human-scale furniture and subdued sci-fi palette.
Image 3 is the REJECTED debris prototype. It conveys only the four equipment families. Its flat gray cardboard surfaces, broad zigzag splits, uniform tubular rails and low-detail finish are exactly what must be replaced.

Create a substantially better and coherent design in the SAME restrained painterly industrial science-fiction world as the approved walls and door. Each of the four panels shows a different compact heap of recognizable damaged ship equipment resting convincingly on a small patch of the game's worn floor. Top-down near-orthographic view matching the game, visible top surfaces and a little front thickness, no horizon and no dramatic isometric studio perspective. Identical scale and camera in all four panels. A little surrounding floor allows contact shadows to be read.

Four subjects:
1. Collapsed ship furniture: a recognizable industrial workstation or mess-table fragment, substantial layered steel top now warped and partly torn, inset surface sections and a small exposed honeycomb/structural underside, one bent leg still caught beneath it, a detached support lying in the same heap. A physically authored damaged manufactured object, not a flat rectangle sawn in half.
2. Destroyed control console: an asymmetrical low crushed chassis retaining one cracked dark inset display at an angle, segmented protective bezels, recessed control strip, buckled service panel partly peeled back to expose a small bundle of cables and one convincing circuit/mechanical assembly. Several nested solid volumes and a strong readable silhouette.
3. Fallen equipment rack: an open armored cabinet partly on its side with bent thick edge members, two displaced shelf/module units, recessed service slots and an exposed dark cavity. Torn sheet-metal skin wraps around part of the carcass. Clearly a cabinet and different from the console.
4. Broken cryopod canopy fragment: a substantial pale gray/slate armored rim with gasket channels and hinge fittings, a few large dark blue smoked-glass shards still caught inside, one displaced curved rib and a torn end fitting. Clearly a piece of a manufactured canopy, never a loose bicycle-frame outline.

Quality and materials:
Build a hierarchy of big, medium and sparse small forms: designed nested profiles, real folded sheet thickness, deep recesses, chamfered frames, localized small fasteners and welded seams where construction calls for them. Wear follows exposed edges; torn zones reveal brighter bare metal with darker scorched recesses. Painted blue charcoal and muted gray-green steel with hand-painted tonal variety, graphite cavities, restrained silver edge accents, very sparse muted brass or brown oxidation. A little ingrained dirt/contact occlusion under overlapping pieces. Preserve quiet areas between the detailed structural edges. Coherent believable damage: bends, crushed overlaps, irregular short tears, displaced modules and broken attachment points. Strong separation between tops, cut edges and interiors so each object reads at small in-game scale. Painterly realism with clean authored forms, not faceted cardboard and not photographic noise.

Composition and finish:
One attractive finished 2x2 concept sheet, approximately square, all objects fully visible with breathing room, no overlap across panels. Floor tiles remain visible but subordinate. No UI, no characters, no robots, no landscape, no unrelated props. Small accurate labels underneath the panels only: "MOBILIER", "CONSOLE", "ARMOIRE", "VERRIÈRE". A discreet main title at top: "DÉBRIS — RECHERCHE VISUELLE". All label text must be spelled exactly.
Avoid giant flat gray polygon plates, puzzle-piece zigzag fractures, thin uniform noodles, generic greeble piles, pristine working equipment, emissive lights, orange sci-fi glow, neon, warning stripes everywhere, oversized bolts, shiny plastic, blurry mottled noise, cartoon low-poly rendering, photorealistic scrap heaps or heavy cinematic lighting. Preserve the established game's mature painted identity.
```
