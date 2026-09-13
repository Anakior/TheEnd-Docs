# Colonne scellée traversant le dôme — cible native

La cible `SealedShaft` du helper local `.artifacts/fixture-complete/native/run.ps1` retrouve le dôme dans le plan réel du vaisseau, puis une route `Elevator` dont les paliers sont alignés en XY, encadrent la profondeur du dôme et n'y ont aucun palier. Elle vérifie la grille actuelle : huit murs sur support métal et un cœur de terrain `Mass`, sans case franchissable. Elle ne relance pas le planificateur, ne crée pas de `VerticalCrossing` et ne modifie pas le monde. `DomeCage` n'est pas une cible de substitution.

La cible est ajoutée après les vues existantes. Tous leurs centres, échelles et noms restent inchangés. Son nom propre est `game-SealedShaft.png` ; le filtre `-DetailTarget SealedShaft` ne capture qu'elle. Le zoom 96 utilise la caméra native, sans agrandissement de l'image après capture.

## Avant remplacement

Commande exécutée depuis `C:/workspace/TheEnd` après compilation du seul helper (0 erreur, 0 avertissement) :

```powershell
& .artifacts/fixture-complete/native/run.ps1 -NoBuild -InteriorDetails -DetailTarget SealedShaft -DetailCellSize 96 -Output C:/workspace/TheEnd-Docs/reference/painted-sprite-direction/sealed-shaft-review/native-before
```

- [Image native avant](native-before/game-SealedShaft.png), 1920×1080, réellement inspectée : carré fermé hachuré de 3×3 cases, cœur sombre et habillage de mur actuel.
- [Rapport natif](native-before/native-game-validation.json) : `Passed=true`, simulation et présentation fixées à 12000, caches contrôlés stables pendant 35 images. Matériaux et modèles installés, aucun override d'étude.
- Client chargé : `F5DF1BFAC16528FF97CA36C1A08ED14D8070EC50A36532164CF2BE5785836EC0`. Aucun build du Client, aucune modification Code/Art/assets pendant cette capture.
- Dôme : id/profondeur 3, grille 256×256, révision 110125. Origine (158,42), côté 3, centre caméra (159.5,43.5), 96 pixels/case.
- Route réelle : id 0, `Elevator`, hors service et non alimentée. Paliers 0,1,2,4,5 à (158,42) ; aucun palier au dôme. Les neuf cases actuelles et leurs couches sont listées dans `SubjectEvidence`.
- Capture PID 28620, terminée avec code 0 avant la reprise du build coordonné par l'agent parent.

Pour une comparaison après remplacement, conserver le filtre, le centre issu de la route, les actifs installés et le tick 12000 ; choisir un nouveau dossier. Une seconde vue à 48 pixels/case peut compléter la vue d'inspection 96. La sélection exige volontairement une colonne encore fermée ; si ses murs ont été modifiés en jeu, elle ne fabriquera pas de sujet équivalent.

## Premier après — intermédiaire, défaut repéré

[Image native 96](native-after96/game-SealedShaft.png) et [rapport](native-after96/native-game-validation.json), Client `8A6CC5AB77AE0C2B5C344FF8745FF084F317DDCAF013F25A2F3DBF06D0385C22`. Même sujet, centre, UI, échelle et tick que la vue avant. Le helper seul a été recompilé (0 erreur, 0 avertissement) ; capture PID 47944 terminée avec code 0.

Le volume peint est présent. **Cette vue n'est pas une validation visuelle finale** : l'ancien cadre noir avec liseré clair et quatre nœuds reste visible autour du nouveau modèle, particulièrement à gauche, à droite et à la base. La capture 48 a été suspendue avant lancement et l'agent parent corrige le masquage du rendu antérieur. Cette preuve intermédiaire est conservée.

Le contrôle supplémentaire `SealedShaftCache` est optionnel pour les anciens DLL, où le champ de renderer n'existe pas ; il n'affecte pas les vérifications avant ni les autres cibles. Pour ce DLL après, il exige exactement un modèle et un modèle visible à chaque observation des images 10 à 45 incluses. Les 36 observations couvrent 35 intervalles : révision 1 constante, et `ReferenceEquals` vrai pour le renderer, la banque GPU `FixtureModelRenderer`, la présentation, la liste des modèles et celle des modèles visibles. Les identités numériques du rapport servent seulement à la traçabilité dans ce processus. La banque installée est identifiée par le manifeste SHA256 `42558820CA7CFCD99C3964D6DDFE5938CBF2D216DB878A7D742FBBEA56519067` ; aucun override d'étude n'est chargé.

Le `Passed=true` du rapport atteste les assertions de sujet et de cache, pas l'absence d'un défaut artistique. L'inspection visuelle a bien trouvé le cadre résiduel décrit ci-dessus.

## Après correction du décor — preuves finales

- [Vue native 96](native-final96/game-SealedShaft.png) et [rapport 96](native-final96/native-game-validation.json).
- [Vue native 48](native-final48/game-SealedShaft.png) et [rapport 48](native-final48/native-game-validation.json).

Les deux images ont été inspectées : les anciennes hachures, les quatre nœuds clairs et le cadre noir extérieur ont disparu. Le volume conserve sa base peinte et son ombre propre ; il reste lisible à l'échelle normale de 48 pixels/case. Le contexte, le vrai sujet et le tick 12000 restent identiques. Les deux rapports ont `Passed=true` et aucun override de banque ou matière.

Client final chargé : `67A137411218D9478BA47CE876DCFEBFEB6066D7BFA870EB00F358DC68CF72F3`. Seul le helper a été recompilé par cet agent, avec 0 erreur et 0 avertissement. Les captures se sont exécutées successivement : PID 39828 à 96, puis PID 43728 à 48 ; les deux sont terminées avec code 0.

La preuve `SealedShaftCache` donne, pour chacune des deux vues : un modèle, un modèle visible, révision 1, 36 observations et 35 intervalles stables. Les objets renderer, banque GPU, présentation et listes restent identiques. Le nouveau cache `_sealedShaftDecor` et son `Batch` gardent aussi exactement leurs instances ; `RetainedVariantCount=1` est stable et inférieur à la borne 2. Cette instrumentation additionnelle demeure optionnelle lorsqu'un ancien Client n'a pas le champ de cache. La banque de modèle reste celle du manifeste `42558820CA7CFCD99C3964D6DDFE5938CBF2D216DB878A7D742FBBEA56519067`.

Commandes finales :

```powershell
& .artifacts/fixture-complete/native/run.ps1 -NoBuild -InteriorDetails -DetailTarget SealedShaft -DetailCellSize 96 -Output C:/workspace/TheEnd-Docs/reference/painted-sprite-direction/sealed-shaft-review/native-final96
& .artifacts/fixture-complete/native/run.ps1 -NoBuild -InteriorDetails -DetailTarget SealedShaft -DetailCellSize 48 -Output C:/workspace/TheEnd-Docs/reference/painted-sprite-direction/sealed-shaft-review/native-final48
```

La première vue après, incorrecte visuellement, ainsi que la vue avant restent conservées dans leurs dossiers d'origine. Les vérifications de cette note portent sur le vrai sujet montré et la stabilité de cette vue ; les tests de gameplay, d'allocation et de repli sont conduits séparément par l'agent parent.
