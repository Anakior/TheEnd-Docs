# Porte peinte : recherche et intégration

[Planche fermée / ouverte](door-painted-study.png).

Statut au **11 septembre 2026 : corps de porte validé visuellement par Ludovic, puis intégré au jeu à sa demande**. Son retour sur le GIF natif est : « oui là c'est bon cela fait porte etc », suivi de l'autorisation « Tu peux même l'intégrer dans le jeu hein ». La course de 0,48 conserve l'extrémité mobile visible à la bouche du carter. **La planche ci-dessus reste une image générée à partir de captures.** Sa réserve initiale portait sur les pieds du colon par rapport au mur ; la validation du corps du prototype vient du GIF natif présenté ensuite. Après examen de la première intégration, Ludovic trouve le sceau à traverses peu convaincant et demande une soudure directe. Cette retouche du sceau est exportée, intégrée et contrôlée en capture native ; le corps et le verrou sont conservés.

Le dessin a été transposé dans `C:\workspace\TheEnd-Art\objects\door\door-painted-study.blend`. La [vidéo native](door-motion.mp4) et son [aperçu GIF](door-motion.gif) montrent le corps retenu avec la caméra, l'échelle et la profondeur réelles ; les bottes sont naturellement masquées par le mur au retour. Cette validation visuelle concerne la baie et l'orientation montrées. Les positions sont mises en scène, simulation figée et sceau masqué : ce n'est pas un test de navigation ou de collision. [Source et reproduction](../../../TheEnd-Art/objects/door/README.md).

## Intégration du 11 septembre 2026

La banque installée est `TheEnd.Client/Assets/models/door/manifest.json`. Le jeu et `DoorModelStudy` utilisent désormais le même `DoorModelRenderer`, fondé sur le rendu 3D partagé, avec la caméra, la lumière, la profondeur et les ombres du moteur. `DoorModelPresentation` suit l'ouverture publiée par la simulation. Le remplacement concerne les portes `Ordinary` de span 1 dans le rendu sprite avec murs en volume ; le placement respecte les axes et donne priorité aux tangentes déclarées. Les traitements spéciaux, les autres spans et les autres modes de rendu conservent leurs présentations existantes.

Le corps `body/painted` garde la course validée de 0,48 et les clips `closed` / `open`, avec une ouverture en 1/3 de seconde. La retouche courante remplace les traverses par `seal/weld` : un cordon irrégulier de métal refroidi au joint X=0, en deux segments autour du verrou, accompagné de chauffe et de peinture brûlée bronze/bleutée. `lock/base` reste le verrou central indépendant. La porte de départ cumule réellement `DoorState.Locked` et `FeatureKind.WeldedSeal` ; le rendu affiche les deux ensembles. Le sceau 3D remplace son ancien dessin 2D sur les portes concernées. Le corps, le verrou, le rig et les règles de simulation sont conservés.

La source sauvegardée reste `objects/door/door-painted-study.blend`, SHA-256 `b26b3faf66221e25c9bea9e03ebf3aefcc5a0ce5feb8cf8a57beca668eb66286`. Les empreintes du corps, du verrou, des courbes, clips et os sont identiques à celles de l'intégration précédente ; la comparaison de la banque retrouve aussi 48 fichiers inchangés pour le corps, le verrou, les clips et les textures. L'export de la soudure est validé avec trois os et une erreur maximale de 3,72529 × 10⁻⁸ m ; les **53 tests ciblés Debug passent**, sans avertissement ni erreur de compilation. La **première intégration**, avec les traverses, avait aussi passé les **4 466 tests Release** ; ce total reste celui de cette intégration précédente.

La [capture de la soudure](door-welded.png) et la [planche des états intégrés](door-game-states.png) montrent cette retouche : cordon gris/bruni présent au joint, verrou conservé et traverses absentes. La planche distingue le vrai départ, avec sceau et verrou, des poses de diagnostic verrou seul, fermée et ouverte. Ces dernières modifient uniquement la présentation pour examiner chaque état. **Ludovic valide l'ensemble le 11 septembre : « Oui c'est nickel . On peut intégrer tout ça ».** Le corps, l'ouverture, le verrou et cette apparence soudée sont retenus et intégrés dans le périmètre décrit ci-dessus.

**Retour sur le sceau de la première intégration, le 11 septembre :** « Scellé je ne suis pas convaincu. Faudrait plus quelque chose comme si cela avait été soudé ». Les deux traverses fixes `seal/bars` présentées dans cette passe sont donc écartées au profit d'une soudure directement sur la rencontre des vantaux. Ce retour concerne le sceau de cette intégration, pas le corps de porte validé ni les statuts consignés dans les anciennes études.

## Historique du dessin, consigné au 11 septembre 2026

Deux générations avec l'outil imagegen intégré, sans CLI. La première avait encore inversé les récepteurs et le joint ; elle est écartée. La correction approuvée place les raccords aux extrémités nord/sud et un joint transversal. Elle retient des profils gris, de l'acier peint, une usure légère et de petites touches de laiton.

Le premier mouvement 3D a été critiqué pour les bandes de seuil gris laissées sur les côtés et la face noire dévoilée par un joint trop grand. Une première reprise a élargi les vantaux et corrigé leur retrait dans les logements. Le dessin de référence demeurait approuvé ; la correction animée attendait alors le retour de Ludovic.

La reprise a été jugée meilleure. Ludovic relevait encore un rectangle dans le logement supérieur et demandait plus de détail. La passe suivante a assombri le contour fixe, retiré le seuil saillant, prolongé le sol sans bord de dalle et ajouté des panneaux chanfreinés avec fixations et raidisseurs. Elle conservait la course et la caméra, et restait alors à apprécier artistiquement.

Ludovic a précisé que ce logement devait se lire comme un élément qui reçoit la porte, avec du volume, et non comme du sol sur le mur. La reprise a ajouté des carters avec capots saillants, joues épaisses et guides internes ; leurs fonds ont été traités en graphite mécanique. Ces volumes 3D constituaient alors une proposition supplémentaire à examiner.

Ludovic a trouvé cette base meilleure et demandé de clarifier le bord mobile : la retouche a atténué le liseré du nez fixe du carter et renforcé le chant solidaire de chaque vantail. Le volume des carters et les détails retenus ont été conservés ; cette retouche animée attendait alors son appréciation.

**Reprise et validation du 11 septembre :** Ludovic a désigné précisément le rectangle aux deux traits sous le récepteur, qui montrait le fond et les guides du logement après disparition du vantail. Cette correction ramène la course de 0,94 à 0,48 : l'extrémité mobile s'arrête à la bouche du carter et reste visible sous le capot. La géométrie, les peintures et les pièces fixes sont conservées, ainsi que la durée d'ouverture de 1/3 de seconde. Export validé ; Ludovic confirme ensuite sur le GIF natif : « oui là c'est bon cela fait porte etc ». Le prototype était encore isolé au moment de ce retour ; son intégration a ensuite été autorisée et réalisée comme décrit ci-dessus.

L'image ne garantit pas les proportions, les pixels du décor ou le personnage à l'identique : ils ont été redessinés. Ne pas déduire les dimensions, l'occlusion ou les collisions du modèle depuis cette planche ; les mesures et la caméra du jeu restent les contraintes du modèle.

Sources envoyées :

- `C:/workspace/TheEnd/.artifacts/door-clearance/sprite-closed-silhouette.png`
- `C:/workspace/TheEnd/.artifacts/door-clearance/sprite-after-silhouette.png`

Original initial : `C:/Users/anaki/.codex/generated_images/01a07a2b-a578-7de2-a8ec-aad665656fb2/exec-113f837e-2e71-4f18-bd1f-737c3beb9369.png`.
Original corrigé, copié sans retouche dans Docs : `C:/Users/anaki/.codex/generated_images/01a07a2b-a578-7de2-a8ec-aad665656fb2/exec-0ddc8bca-6b23-4818-99b2-3805c0588f2a.png`.

## Prompt initial

```text
Use case: precise-object-edit.
Asset type: painted art-direction proposal for a sliding door in an existing top-down colony game. This is concept art, not a claim of a working 3D implementation.
Inputs: image 1 is the real game scene with a rejected plain gray placeholder in the closed state; image 2 is the same real scene open. These images are authoritative for the walls, floor, human scale, camera angle and the orientation of the passage.

Create one polished landscape comparison, two panels labeled only "FERMÉE" and "OUVERTE", showing the SAME new door design in both states. Take a close crop around the doorway centered at (960,420) in the 1920x1080 references, approximately x=830..1100 y=320..540. Enlarge the whole crop equally, including the human. Preserve the distinctive existing layered gray wall profiles, worn steel floor, dark structural sides and the existing colonist, without redesigning the surrounding room.

Replace the crude untextured gray masses in the passage with an attractive carefully designed weathered metal sliding bulkhead door that belongs to these precise walls. Work like a skilled game environment concept artist: coherent nested metal sections, substantial but restrained folded steel leaves, a clean mating seam, small recessed slide guides continuous with the existing wall profiles, discreet worn brass mechanical catches, painterly edge wear, muted charcoal blue gray steel, believable contact shadows. Give it an authored purposeful silhouette rather than a simple rectangular bar or a box. All visible construction must serve the sliding closure. The floor through the open doorway must look continuous with the adjacent floor, not like a floating slab or vertical panel.

CRITICAL GEOMETRY: The human walks LEFT TO RIGHT in the image. The wall containing the door runs UP AND DOWN. The two leaves slide UP and DOWN into the ends of that wall. The door plane is vertical in real space and is seen EDGE ON by this camera. Show a deliberate cutaway cross-section at the height of the existing cut walls, with the thickness of the sliding leaves and layered receiving channels readable from above. The two leaves meet midway across this north-south span; the visible top cross-section has a short transverse mating seam. Do NOT turn the door to face the viewer or rotate its mechanism 90 degrees. Do NOT paint a face-up square hatch flat on the floor. Do NOT invent a tall tower, lintel box, freestanding posts or exposed storage cassettes sticking above the cut walls. The artist must make the actual orientation readable and attractive.

Closed panel: a credible substantial metal closure seated into both ends of the existing wall; colonist stays just left of the passage, as in image 1.
Open panel: the same two leaves have retracted along the wall, leaving a clear left-right floor passage; colonist is to the right as in image 2. The stationary receivers stay in exactly the same place and must not resemble a closed barrier.
Material style: mature restrained painted industrial science fiction matching the game, fine layered profiles and quiet wear, not cartoon, not plastic, not whitebox. No decorative glow, giant hazard stripes, giant bolts, control tower, garbled text, new UI, new characters, or unrelated machinery. Keep the existing camera and real human scale. Only the door and its immediate end fittings are redesigned.
```

## Prompt de correction

```text
Edit this exact two-panel comparison, preserving the entire walls, floor, colonists, lighting, crop and labels. Correct ONLY the mechanical orientation of the small door inside the two central openings. It currently has its receivers on LEFT and RIGHT and a VERTICAL central seam, which is wrong.

The character travels LEFT TO RIGHT. The door lies in the UP-DOWN wall. The two door halves must meet at a HORIZONTAL seam, and retract UP and DOWN, not left/right. This is the same cutaway view as the surrounding low walls: show the top cut section and thickness, NOT a door facade lying face-up on the floor.

CLOSED PANEL (left): remove the two brass cylinders from the left/right sides of the opening. Put compact transverse brass slide fittings at the TOP and BOTTOM ends of the opening, embedded into the existing up/down wall ends. Redraw the metal closure as an UPPER leaf and LOWER leaf meeting at a short HORIZONTAL dark seam near the middle. Overall closure is a narrow NORTH-SOUTH metal section running vertically in the image, approximately the width of one colonist's torso (around 55 pixels in this enlarged image), not a broad face-on cabinet. Shape its cross-section with small stepped steel lips and chamfers, restrained painted wear. The character and floor corridor stay unchanged.

OPEN PANEL (right): remove both lateral cylinders likewise. Put exactly the same fixed compact fittings at the TOP and BOTTOM of the opening. The upper leaf has retracted UP under the top wall; the lower leaf has retracted DOWN under the bottom wall. Show their ends tucked inside the wall and a clear LEFT-RIGHT floor connection through the center. No cabinets flank the character on the left or right. No closed-looking plate stays on the floor.

Preserve the wall profiles and the room exactly. Do not rotate the whole scene, the camera, the human or the labels. Do not invent a tall frame or enlarge the doorway. The only correction is the two leaves' north-south mechanics and their compact receivers; maintain the painted worn steel and brass aesthetic.
```
