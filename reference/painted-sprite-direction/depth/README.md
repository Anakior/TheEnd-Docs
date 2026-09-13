# Mobilier peint : profondeur et fonction

**Retour reçu : « C'est mieux comme ça oui ».** Ces quatre formes servent désormais de référence à la [déclinaison des formats/états et au premier décor peint](../complete/README.md). La présente note conserve le détail de la comparaison qui a conduit à cette approbation.

Le retour de Ludovic est clair : le style peint est bien meilleur, mais les objets manquent encore de détails et de profondeur, surtout la console. La peinture V2 devient la référence conservée pour cette reprise ; le travail porte sur la géométrie et les fonctions visibles.

La console doit se lire en trois masses : un bloc d'écran incliné avec un véritable encastrement, un pupitre de commandes en avant et un socle en retrait. Les joues, joints et panneaux secondaires donnent l'épaisseur. À 48 pixels par case, les niveaux et les ombres de contact doivent rester visibles ; les boutons et fixations soutiennent cette structure.

Cette séparation prépare aussi une lecture cohérente des futurs états : le bloc d'écran, le pupitre et les panneaux d'accès sont des éléments identifiables à ouvrir, dépouiller ou casser. Les états supplémentaires ne sont pas fabriqués dans cet essai ; il faut d'abord juger la forme intacte. Les vues de comparaison doivent conserver les mêmes dimensions, le même cadrage par paire et le même éclairage, y compris lorsque l'objet est tourné.

Les tables et bancs reçoivent une reprise plus mesurée de leurs panneaux, chants et appuis. Les modèles peints précédents restent les témoins de comparaison. La peinture n'est pas régénérée et le rendu de production ne change pas.

## Sources et revue

- Source table/banc : `TheEnd-Art/objects/common-furniture/common-furniture-depth.blend`.
- Source utilitaire : `TheEnd-Art/objects/utility-furniture/utility-furniture-depth.blend`.
- Témoins peints : banques `common-furniture-detail` et `utility-furniture-detail`.
- Les nouveaux exports restent des banques externes. Les états et tailles supplémentaires ne font pas partie de cette revue.

## Table et banc

La table conserve son emprise et sa hauteur de 0,614 m. Son bord porteur passe à 0,10 m d'épaisseur ; les panneaux et leur insert descendent de 0,06 m. Les pieds, la traverse basse et les platines sont renforcés. Le banc conserve son gabarit de 0,405 m de haut, avec une épaisseur réelle des lattes, des appuis renforcés et un léger décalage entre les bandes d'assise. Les touches peintes restent celles des sources précédentes.

- [Comparatif de face, détail et 48 px/case](table-bench-rotation-0.png).
- [Comparatif tourné vers l'ouest](table-bench-rotation-1.png).

Chaque planche comporte huit cartes disponibles. Les JSON voisins identifient les banques exactes et les légendes « Forme actuelle / Relief retravaillé ». Le changement est surtout visible dans les chants et les appuis ; il reste mesuré à 48 pixels par case. Export commun validé, erreur maximale de skinning 0 m. Source SHA256 : `782536448013144ade76cb7e43a49bd3899c03df03f999c714236aaf4e3b91c9`.

## Console et rangement

L'écran de la console est relevé à 38° depuis l'horizontale et encastré dans un logement avec joues épaisses. Son centre se trouve à 0,79 m, au-dessus du pupitre à 0,613 m. Le clavier dans sa cavité, le module latéral, la trappe et la grille distinguent les fonctions ; le socle en retrait donne l'assise. La console monte désormais à 1,018 m, toujours dans une emprise de 2 × 1 m. La source peinte fournit les cadres, le verre et leurs UV conservés. Les niches du rangement sont réellement dégagées, ses deux caissons supérieurs reculés et posés plus bas sur leurs tablettes.

Comparatifs natifs, tous avec huit cartes disponibles et une rangée à 48 pixels par case : [Nord](consoles-rotation-0.png), [Ouest](consoles-rotation-1.png), [Sud](consoles-rotation-2.png), [Est](consoles-rotation-3.png). Les vues latérales montrent particulièrement le décroché écran/pupitre. En vue arrière Sud, le dos du logement masque naturellement une partie de l'écran incliné. Les captures sont des rendus réels du moteur, sans retouche d'image.

Source utilitaire SHA256 : `95593b1d5cc296f57b387010c7ce51ae17800fc5d15cbafa2e7a2f7fd8f1a9a9`. Les deux exports passent la validation avec une erreur maximale de skinning de 0 m. L'audit vérifie les fichiers exportés, leurs empreintes et toutes les UV texturées : aucun dépassement de [0,1]. Les sources peintes témoins et l'atlas V2 restent identiques : [rapport de banque](bank-validation.json).

## Vérification dans le jeu et reprise

Les quatre exemples intacts ont aussi été chargés et capturés dans le vrai vaisseau : [table](game/game-0-Table-Sealed.png), [banc](game/game-1-Bench-Sealed.png), [console contre son mur](game/game-2-Console-Sealed.png), [rangement](game/game-3-Rack-Sealed.png). Le helper sélectionne uniquement pause, pont et caméra, sans modifier le monde ni les états. Chaque cible passe bien du rendu vectoriel au modèle et sa révision de cache reste stable pendant les 25 images contrôlées après préparation : [résultat natif](game/native-game-validation.json). Ce contrôle n'est pas un benchmark FPS.

Le client et le helper compilent avec 0 erreur et 0 avertissement. La seule modification Code de cette reprise concerne les libellés optionnels du banc (`-ReferenceLabel`, `-CandidateLabel`, défauts « Avant / Peint » conservés), afin de comparer deux modèles déjà peints. Le Core, les renderers de production et les assets installés ne sont pas modifiés. Les tests de la passe précédente ne sont pas revendiqués comme nouvellement exécutés.

Depuis TheEnd, avec le client compilé :

```powershell
./tools/fixtures/open-fixture-study.ps1 -ComparePaint -Page consoles `
  -CommonFurnitureBank C:/workspace/TheEnd-Art/exports/common-furniture-depth `
  -CommonFurnitureReferenceBank C:/workspace/TheEnd-Art/exports/common-furniture-detail `
  -UtilityFurnitureBank C:/workspace/TheEnd-Art/exports/utility-furniture-depth `
  -UtilityFurnitureReferenceBank C:/workspace/TheEnd-Art/exports/utility-furniture-detail `
  -ReferenceLabel 'Forme actuelle' -CandidateLabel 'Relief retravaillé' -NoBuild
```

`2` affiche tables/bancs ; `3` ou `5` affiche console/rangement ; `R` tourne ; `+/-` et la molette changent le zoom. Les quatre prototypes restent des propositions à apprécier artistiquement, sans installation. Aucun commit/push Code, Art ou Docs de l'assistant.
