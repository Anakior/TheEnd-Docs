# Cryopod : validation du banc 3D

Les quatre états utilisent le renderer natif du jeu et ses matériaux. Le banc est
une scène indépendante : il ne charge ni ne modifie de sauvegarde de colonie. La
banque approuvée fournit `Sealed` et `Open`; la banque compagnon externe fournit
`Stripped` (dépouillé) et `Collapsed` (cassé).

## Captures retenues

- [Quatre états vides, nord](cryopods-north-final.png).
- [Quatre états occupés, nord](cryopods-north-occupied.png).
- [Quatre états occupés, ouest](cryopods-west-occupied.png).
- [Quatre états vides, ouest](cryopods-west.png).

Chaque capture présente une ligne de détail et une ligne à **48 px/cellule**.
Toutes les variantes d’une même ligne utilisent la même échelle et le même centre
de caméra : le cadrage ne grossit pas une épave pour compenser son affaissement.
Les variantes sont séparées, sans chevauchement ou découpe du modèle. Les silhouettes
et le vitrage restent lisibles dans les deux orientations vérifiées.

La source approuvée `cryopod.blend`, ses peintures et les clips fermé/ouvert sont
conservés. Les empreintes du manifeste et des deux clips sont contrôlées dans
[cryopod-occupancy-validation.json](cryopod-occupancy-validation.json).

La comparaison pixel à pixel des captures nord vide/occupée vérifie une modification
dans la chambre de chaque état et **zéro pixel modifié** dans les rectangles de coque
comparés. L’occupation est indépendante de l’état et ne change pas le matériau du
meuble. La silhouette anonyme demeure celle du modèle approuvé.

Le modèle dépouillé possède des panneaux de vitrage réellement manquants et un
mécanisme déboîté. Le modèle cassé ajoute un affaissement asymétrique du flanc, un
rail interrompu et des fragments au fond. Ces pièces sont sauvegardées dans
`TheEnd-Art/objects/cryopod/cryopod-damaged.blend`, décrites dans
`TheEnd-Art/objects/cryopod/damaged-study.md`. L’export Art est validé avec une erreur
maximale de skinning de 0 mètre. Aucune banque compagnon n’est installée par le banc.

## Reproduire

Depuis TheEnd :

```powershell
.\tools\fixtures\open-fixture-study.ps1 -Page cryopods
.\tools\fixtures\open-fixture-study.ps1 -Page cryopods -Occupied -Rotation 1
```

Le lanceur trouve les exports dans Art voisin. `-CryopodDamagedBank` permet de donner
explicitement un dossier ou un manifeste, sans copie dans les assets.
`-Capture chemin.png` produit une capture cachée et son JSON de provenance puis
ferme le banc. `-NoBuild` réutilise le Client déjà compilé. `-InGame` lance la partie
normale en mode sprite avec les mêmes chemins de banques, sous responsabilité du
renderer de jeu ; ce mode est distinct de la présente preuve hors simulation.

Dans le banc : 1–5/Tab changent de page, R tourne, +/− ou la molette règlent le zoom,
P change vide/occupé et O anime la capsule ouverte. Pg. préc./suiv. donnent les autres
formes du mobilier ; `-GroupOffset` sélectionne un groupe pour la capture.

Les tests ajoutés dans `CryopodDamagePresentationTests` couvrent l’absence de banque,
une variante manquante, les quatre orientations, les bornes propres aux dommages,
les ouvertures obsolètes, l’occupation réelle et le retour au mode vectoriel. Ils
complètent les tests existants sur les capsules intactes et leurs interactions.

## Autres pages déjà examinées

[Tables et bancs longs](table-bench-long.png) et [courts](table-bench-short.png)
présentent chacun leurs quatre états sur deux rangées. Les groupes de forme sont
conservés : les formats longs ne sont pas remplacés par une simple mise à l’échelle
des formats courts. Les premières captures portent encore un astérisque à la place
du signe moins dans l’aide ; ce caractère a été corrigé dans le build final du banc.

Le JSON adjacent à chaque PNG enregistre les banques effectivement chargées et leurs
hashes. Les trois captures cryo finales utilisent le Client SHA-256
`915D1B82BA14DD36D00B6E925566BF8938FC6EA1DED72B6223F4974042EA63DE`.
