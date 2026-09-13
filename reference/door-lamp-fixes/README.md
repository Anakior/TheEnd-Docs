# Porte pointillée et spots muraux — 12 septembre 2026

Ludovic signale une [porte étrange](reported-door.png) et des
[spots qui semblent flotter au-dessus des murs](reported-lamps.png).

**État : correctifs implémentés et validation terminée le 12 septembre 2026.
Les 610 tests ciblés ont été exécutés et réussissent, sans échec ni test ignoré.
Les trois captures natives après correction ont été obtenues et inspectées.
Le blocage Windows rencontré lors de la première vérification ne se reproduit plus.**

Le signalement ultérieur du décalage entre spot et lumière est traité dans
[le raccord des sources lumineuses](light-alignment.md), avec un passage spatial
limité aux spots en sprite volume et ses preuves avant/après.

## Porte

Le trait jaune est une porte pressurisée d'une case restée avec son rendu
vectoriel. `DoorPresenter` la publie depuis le vrai `DoorMap` ; la sélection
du modèle 3D ne prenait que les portes `Ordinary`. La géométrie des pointillés
provient de `DoorLeafSkin`, avec le cadre historique.

L'audit du départ réel (seed 12345, grille 256²) trouve 341 portes vivantes,
34 portes `Pressure` hors sas et aucune porte orpheline. La
[capture native avant](before-pressure-vertical.png) reproduit le défaut sur
le pont 0, porte 4, cellule (72,161), fermée, hors `SasMap`. Les autres
informations sont dans [l'audit](pressure-audit.json).

`DoorModelPresentation` accepte désormais `Ordinary` et `Pressure` de span 1
avec la banque de porte déjà approuvée. L'ouverture reste pilotée par les
ticks du type réel ; les portes pressurisées conservent leur durée et leurs
règles. Les sas de trois cases gardent leur modèle propre. Aucun asset ni
comportement Core n'a été modifié. Les tests de sélection, sceaux, replis et
cycle de présentation ont été adaptés aux deux types.

La [capture native après](after-pressure-vertical.png) montre désormais cette
porte fermée avec le modèle 3D approuvé ; le trait jaune a disparu. Les
[métadonnées](after-pressure-vertical.json) confirment la même porte `Pressure`
4, hors sas, et le même cadrage que la capture avant.

## Spots

Le cache leur attribuait la hauteur des meubles (0,65 m), supérieure aux murs
(0,60 m), alors que le dessin restait au sol. L'ancre issue du tracé mural
était également située dans l'épaisseur du mur.

En mode sprite avec volume, `WallLampAnchor` place le spot sur la face donnant
dans la pièce. `WallLampSkin` utilise une hauteur de montage de 0,35 m, avec
la même projection pour sa couleur et sa profondeur. Le mur peut donc masquer
les supports sur sa face cachée. `GlowSkin` reprend l'ancre physique au sol
pour conserver la projection lumineuse. Aucun masquage arbitraire par orientation.

Le booléen de mode traverse le cache des équipements et ses workers ; changer
de mode invalide l'ancienne présentation. Les rendus plat et vectoriel restent
inchangés. Tests ajoutés : quatre orientations, diagonale, profondeur,
projection, lumière dans une pièce réelle normale/étroite et changement de mode.

Les captures avant [North](before-lamp-north.png) et
[South](before-lamp-south.png) montrent des lampes sur des diagonales : le Facing
est quantifié et ne décrit pas exactement leur tangente visuelle. Leurs
métadonnées voisines identifient les vrais objets. L'aperçu porte montre aussi
des supports horizontaux et verticaux à comparer après correction.

Les captures après [North](after-lamp-north.png) et [South](after-lamp-south.png)
retrouvent les mêmes lampes réelles, le même pont et la même caméra :
North en (61,48), seed 190, et South en (47,88), seed 186. Sur la face visible,
le support est désormais placé plus bas, contre la paroi intérieure ; les
lampes horizontales voisines suivent également cette hauteur. Sur la diagonale
South, la barre qui flottait sur l'extérieur du mur est maintenant masquée par
celui-ci. Les supports ne passent plus visuellement au-dessus du sommet du mur
dans ces trois vues. Les [métadonnées North](after-lamp-north.json) et
[South](after-lamp-south.json) conservent l'identité des objets observés.

## Validation

Client Debug et hôte natif : zéro avertissement, zéro erreur. Le rapport xUnit
contient **610 tests exécutés, 610 réussis, zéro échec, zéro test non exécuté**.
Le TRX est conservé dans
`TheEnd/.artifacts/door-lamp-fix/tests/door-lamp-fixes.trx` ; les compteurs,
empreintes des PNG et métadonnées de scène sont repris dans
[la preuve de validation](native-validation.json).

Les trois lancements de l'hôte natif se sont terminés avec le code 0. Celui-ci
appelle `TheEndGame` et ne change que le pont/la caméra. Il ne crée pas de porte,
ne force pas son état et ne remplace pas le `DisplayFrame`. L'inspection couvre
les scènes capturées ; les tests complètent les orientations, la profondeur,
la projection lumineuse et le changement de mode. Aucun code ni asset n'a été
modifié pendant cette reprise de validation.

Pour reproduire depuis Code :

```powershell
dotnet test TheEnd.Tests/TheEnd.Tests.csproj -c Debug --no-restore --filter 'FullyQualifiedName~Door|FullyQualifiedName~Sas|FullyQualifiedName~WallLamp|FullyQualifiedName~FixtureFrame|FullyQualifiedName~FixtureSkin|FullyQualifiedName~Glow|FullyQualifiedName~ActorOcclusion|FullyQualifiedName~WallVolume'
.\.artifacts\door-lamp-fix\native\run.ps1 -Name after-pressure-vertical -DeckId 0 -DoorId 4
.\.artifacts\door-lamp-fix\native\run.ps1 -Name after-lamp-north -DeckId 0 -DoorId -2 -NoBuild
.\.artifacts\door-lamp-fix\native\run.ps1 -Name after-lamp-south -DeckId 0 -DoorId -3 -NoBuild
```

## Blocage initial conservé pour l'historique

La première vérification compilait les assemblies, mais Windows refusait le
chargement de `TheEnd.Client.dll` (`0x800711C7`, événements CodeIntegrity
3033/3077). La découverte xUnit était interrompue : zéro test avait alors pu
s'exécuter et aucune capture après correction n'avait été produite. Les
empreintes `before-binary-provenance.json` / `after-binary-provenance.json`
correspondent à cette étape. Après le signalement de Ludovic que le lancement
fonctionne, les commandes normales ci-dessus ont réussi. Aucun contournement
ni changement de protection Windows n'a été effectué par l'assistant.

Aucun commit/push Code, Art ou Docs par l'assistant.
