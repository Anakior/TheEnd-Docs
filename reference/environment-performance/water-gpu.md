# Eau sprite : animation retenue sur le GPU

Le passage de l’eau au vertex shader réduit son coût de soumission CPU de **3,44–4,41 ms à 0,08–0,18 ms par image** sur la vue mesurée. Les ondulations validées sont conservées : même texture, mêmes phases spatiales, mêmes périodes et même horloge de simulation. Les positions de berge, les couleurs de profondeur au repos et l’opacité ne sont pas animées.

## Mesure native

La preuve [water-gpu-benchmark.json](water-gpu-benchmark.json) compare deux chemins dans le même processus MonoGame, sur l’eau du vrai dôme généré avec la graine `12345`, pont `3`, caméra `(128,100)`, 48 pixels par cellule :

- Référence : fonction CPU `SpriteWaterSkin.Animate` précédemment validée, puis `DrawPreparedTexturedTriangles` et son envoi des sommets à chaque image.
- Nouveau chemin : mêmes positions, couleurs et phases précalculées dans des `VertexBuffer` immuables ; seuls trois paramètres de l’horloge sont actualisés par image.

La vue contient 21 chunks et 14 118 sommets visibles. Chaque mesure comprend 12 images de préparation, puis 120 images ; trois paires de mesures sont réalisées. Les deux chemins allouent zéro octet par image pendant la soumission mesurée.

| Passe | Référence CPU | GPU retenu |
| --- | ---: | ---: |
| 1 | 3,448 ms | 0,111 ms |
| 2 | 4,406 ms | 0,182 ms |
| 3 | 3,437 ms | 0,082 ms |

Il s’agit du coût de soumission du matériau eau, appels de dessin inclus, et non du temps total d’une image du jeu ou d’une mesure isolée du temps GPU.

Les captures natives aux ticks `12000`, `12060` et `12127` sont comparées pixel par pixel à caméra, cible et texture identiques. L’écart moyen maximal par canal reste entre **0,0856 et 0,0882 sur 255** ; l’écart maximal ponctuel est de **2 à 3 sur 255**. Les écarts proviennent des arrondis entre calculs CPU et shader. Les deux images ont également été inspectées visuellement.

Captures et helper reproductible : `C:\workspace\TheEnd\.artifacts\water-performance\gpu-compare` et `C:\workspace\TheEnd\.artifacts\water-performance\native\run.ps1`. Le helper isole le matériau eau sur un fond uni afin de comparer précisément son rendu ; les preuves de chargement et de jeu complet sont distinctes.

## Cache et chargement

`SpriteWaterSkin` conserve trois publications CPU/GPU : le pont actif et deux ponts récents. Il réutilise l’instance exacte du contour publiée par `LeakSkin`. Une nouvelle révision de l’eau remplace la publication précédente de la même grille ; l’éviction ou la destruction du cache libère ses buffers GPU.

Le chemin courant vérifie directement si la publication active est déjà la bonne : il ne recherche pas dans le cache à chaque image. Le dessin ne réécrit plus les sommets et ne renvoie plus leur contenu au GPU.

`RequestedViewportReady` reste faux à l’arrivée sur une grille froide tant que contours, matériau et buffers ne sont pas prêts. Une ancienne publication compatible reste utilisable pendant une nouvelle révision de la même grille. `RequestedViewportFailure` transmet les erreurs de contour, préparation, shader ou upload lorsque aucune publication compatible ne peut être affichée. Sans texture d’eau disponible, le mode de remplacement n’attend pas et le rendu vectoriel demeure disponible.

La vérification native du maintien de l’écran de chargement et du retour sur un pont est suivie séparément dans cette référence de performance.

## Source et compilation du shader

- Source : `C:\workspace\TheEnd\TheEnd.Client\Assets\shaders\sprite-water.fx`.
- Binaire livré : `C:\workspace\TheEnd\TheEnd.Client\Assets\shaders\sprite-water.mgfxo`.
- Gestion des buffers : `SpriteWaterGpu.cs` ; préparation/cache : `SpriteWaterSkin.cs` ; caméra partagée : `VectorRenderer.DrawPreparedEffectTriangles`.

Le shader est compilé avant livraison. Il n’est pas compilé pendant le chargement du jeu. La commande utilisée, depuis `C:\workspace\TheEnd`, est :

```powershell
.\scripts\build-water-shader.ps1 -MgfxCompiler 'C:\Users\anaki\.nuget\packages\dotnet-mgcb\3.8.4.1\tools\net8.0\any\mgfxc.dll'
```

Ce compilateur MonoGame `3.8.4.1`, déjà installé, produit le profil `OpenGL`. Le binaire résultant a été chargé et mesuré avec le runtime du jeu `3.8.5`. Les fichiers du dossier `Assets` sont copiés par le projet Client dans les sorties de compilation et de publication.

## Provenance et validation

SHA-256 :

| Élément | Empreinte |
| --- | --- |
| DLL avant modification, conservée dans `.artifacts/water-performance/before-binary` | `0FEA6C06A4D2ACE92B7CC6F7B21D7AD3CE72E89B6F138F16A4FF12531FBAE98B` |
| DLL utilisée par le helper comparatif | `D26FA70428F02FD7F4554384DCAD8EDCF300E9C68094F878600D22EE6FD5E854` |
| `sprite-water.fx` | `A91FC094B367DE2D86D52CEB7DE2E913BBF89D1D855725510627DD63A5BC64A2` |
| `sprite-water.mgfxo` | `23939295AF11B1EC3E7DD1EF2809BD3573194011C072BC1AC9C2D09FDEEA3CB3` |

Le filtre `WaterSkinTests|SpriteWater*` a exécuté **32 tests réussis, zéro ignoré** : contours et îlots, animation/pause/reprise, raccords UV, cache des contours, réutilisation des buffers, éviction au quatrième pont, remplacement d’une révision et disposition mémoire des attributs GPU. Le raccourci de préparation sur publication active a été ajouté après cette compilation ; il est inclus dans la validation globale suivante. La DLL du tableau identifie donc précisément le helper mesuré, et non une future compilation globale.

Aucun commit ni push effectué dans Code ou Docs.
