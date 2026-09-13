# Composition du fond spatial — contrôle natif

Même caméra, pont 0, centre (159,5 ; 43,5), 48 px/case, tick 12000. Images 1920 × 1080. Résultat : **réussi**.

Sur **816 219 pixels intérieurs distincts**, 0 diffèrent : RGBA identiques, écart maximal 0/255. Les zones comprennent sol de droite, ascenseur/porte, sol central, masse sombre et rails muraux.

| Région | Pixels modifiés | Pixels examinés | Écart maximal |
| --- | ---: | ---: | ---: |
| right-room-floor | 0 | 157950 | 0/255 |
| elevator-platform-and-door | 0 | 32800 | 0/255 |
| lower-centre-room-floor | 0 | 46116 | 0/255 |
| interior-wall-shadow-mass | 0 | 66000 | 0/255 |
| upper-opaque-hull-rail | 0 | 14750 | 0/255 |
| left-opaque-hull-rail | 0 | 8043 | 0/255 |
| exterior-space | 289458 | 289800 | 239/255 |

Le rapport natif référence `space/painted-space-v1.png` avec SHA256 `fda0cd21cfc0c7c64301117cc86c54b14b20172ded417bad1ead69ab80fdda2a` ; le fichier installé porte la même empreinte.

Les coordonnées et justifications des régions sont dans [le JSON](space-compositing-validation.json). Les images n’ont été ni alignées, ni redimensionnées, ni retouchées.

Le total de 816 219 pixels est l'union des régions intérieures ci-dessus et de
trois zones intérieures plus larges (`widerInteriorCoverage` dans le JSON), avec
suppression des recouvrements. Il ne correspond pas à la seule somme du tableau.

**Limites :** preuve de cette vue uniquement, régions conservatrices hors silhouettes anticrénelées et interface translucide. Aucun lac naturel dans ces mesures ; aucune conclusion sur ses berges ou son eau. Les surfaces opaques sont identifiées visuellement, sans buffer d’identification des matériaux.
