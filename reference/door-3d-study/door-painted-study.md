# Recherche peinte de porte

[Planche fermée / ouverte](door-painted-study.png).

Statut : **dessin approuvé par Ludovic**, après le rejet de l'étude de silhouette 3D. Sa réserve porte sur les pieds du colon par rapport au mur dans l'image générée ; il demande maintenant de voir la porte en mouvement. **Cette planche reste une image générée à partir de captures.** Son approbation ne vaut pas validation du nouveau modèle ou de son rendu dans le jeu.

Le dessin a depuis été transposé dans `C:\workspace\TheEnd-Art\objects\door\door-painted-study.blend`, exporté et validé sans installation dans les assets ordinaires. La [vidéo native](door-motion.mp4) et son [aperçu GIF](door-motion.gif) servent à juger le mouvement avec la caméra, l'échelle et la profondeur réelles ; les bottes sont naturellement masquées par le mur au retour. Les positions sont mises en scène, simulation figée et sceau masqué : ce n'est pas un test de navigation ou de collision. [Source et reproduction](../../../TheEnd-Art/objects/door/README.md).

Deux générations avec l'outil imagegen intégré, sans CLI. La première avait encore inversé les récepteurs et le joint ; elle est écartée. La correction approuvée place les raccords aux extrémités nord/sud et un joint transversal. Elle retient des profils gris, de l'acier peint, une usure légère et de petites touches de laiton.

Le premier mouvement 3D a été critiqué pour les bandes de seuil gris laissées sur les côtés et la face noire dévoilée par un joint trop grand. La vidéo liée ci-dessus est la reprise corrigée du modèle, avec des vantaux plus larges et un retrait dans leurs logements. Le dessin de référence demeure approuvé ; la correction animée attend le retour de Ludovic.

La reprise est jugée meilleure. Ludovic relève encore un rectangle dans le logement supérieur et demande plus de détail. Les médias actuels montrent sa correction (contour fixe assombri, seuil saillant retiré, sol continu sans bord de dalle) et des panneaux chanfreinés avec fixations et raidisseurs. Cette passe ne modifie ni la course ni la caméra et reste à apprécier artistiquement.

Précision de Ludovic : ce logement doit se lire comme un élément qui reçoit la porte, avec du volume, et non comme du sol sur le mur. Les médias actuels ajoutent donc des carters avec capots saillants, joues épaisses et guides internes ; leurs fonds sont traités en graphite mécanique. Ces volumes 3D constituent une proposition supplémentaire, pas une validation acquise du dessin de référence.

Ludovic trouve cette base meilleure et demande de clarifier le bord mobile : les médias actuels atténuent le liseré du nez fixe du carter et renforcent le chant solidaire de chaque vantail. Le volume des carters et les détails retenus sont conservés ; cette retouche animée reste à apprécier.

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
