# Raccord des spots et de leur lumière — 12 septembre 2026

Le [signalement](reported-light-alignment.png) montre un spot sur un mur vertical
dont le cône lumineux démarre trop bas. La première correction avait placé le
support à 0,35 m et projeté son dessin vers le haut, tandis que le cône conservait
une origine au sol. Le décalage était de 0,35 / √2 case, soit environ 12 pixels
avec des cases de 48 pixels.

En mode sprite avec murs en volume, la source lumineuse part maintenant de la
même ancre physique et de la même hauteur que le support. Le cône descend jusqu'au
sol sur ses premières 0,8 case, puis sa projection reste sur le sol. Ses
intersections avec les murs et les portes sont toujours calculées avant projection,
dans les coordonnées physiques du plan.

Les triangles de ces seuls spots passent par la même caméra 3D que les murs et
lisent leur tampon de profondeur. La lumière d'un support caché ne peut donc pas
être peinte par-dessus le sommet du mur. Le passage est additif, ne modifie pas
la profondeur et restaure les états graphiques. Les lumières de consoles et de
capsules, ainsi que les modes plat et vectoriel, conservent leur passage existant.
Le dessin et l'ancre des supports North/South n'ont pas été déplacés.

## Preuves natives

L'hôte utilise `TheEndGame` sur le vrai vaisseau de départ (seed 12345, pont 0),
en ne sélectionnant que le pont et la caméra. Aucun objet, état ou DisplayFrame
n'est fabriqué pour les captures.

| Vue | Caméra | Observation |
| --- | --- | --- |
| [Paroi verticale avant](before-lamp-light-vertical.png) / [après](after-lamp-light-vertical.png) | (105.5,87.5), 48 px/case | Lampe East, seed 194, cône bleu désormais raccordé à sa hauteur ; une lampe horizontale ambre est également visible dans la vue. |
| [East avant](before-lamp-light-east.png) / [après](after-lamp-light-east.png) | (67.5,80.5), 48 px/case | Lampe East, seed 187 ; les meubles voisins peuvent désormais masquer le flux. |
| [North après](after-lamp-light-north.png) | (61.5,48.5), 48 px/case | Support visible sur la diagonale, raccord de la lumière conservé. |
| [South après](after-lamp-light-south.png) | (47.5,88.5), 48 px/case | Support caché derrière la diagonale ; aucun cône ajouté sur le sommet du mur. |

Le premier avant/après vertical utilise pour l'avant la DLL isolée
`F4E1ED63EA103584414A0D32B7EB2A28095B6EE3CDB7350752AC130BBE626642`, conservée avant
la correction du cône. Les métadonnées JSON voisines conservent les caméras et
identités ; [la preuve](light-alignment-check.json) conserve les empreintes.

## Vérification

Compilation du Client et de l'hôte natif réussie. **68 tests ciblés réussissent,
zéro échec et zéro test ignoré** (`WallLamp`, `Glow`, `ActorOcclusion`). Les nouveaux
cas couvrent les quatre orientations, les deux côtés d'une diagonale, l'origine
montée, l'arrivée au sol, les intersections physiques inchangées, le cache et le
maintien du passage actuel pour les autres types de lumières.

TRX : `TheEnd/.artifacts/door-lamp-fix/light-projection-tests/lamp-light-projection.trx`.
Les captures natives après se sont terminées avec le code 0 et ont été inspectées.
Aucun asset ou comportement Core n'a été modifié pour ce raccord.
