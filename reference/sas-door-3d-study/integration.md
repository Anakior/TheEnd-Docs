# Sas A — intégration au jeu

**12 septembre 2026 — intégration demandée par Ludovic après validation de l'apparence et de l'ouverture : « Implémentes du coup ».**

La banque [sas-door](../../../TheEnd/TheEnd.Client/Assets/models/sas-door/manifest.json) est installée et reliée au rendu normal sprite avec murs en volume. Toutes les bandes de sas de trois cases utilisent le modèle retenu, sur les deux axes. Les vantaux suivent l'ouverture publiée par `DoorPresenter` depuis les trois portes synchronisées de chaque bande ; aucun déplacement d'essai n'est injecté dans le rendu de production.

## Source conservée

Le fichier [sas-door-a.blend](../../../TheEnd-Art/objects/sas-door/sas-door-a.blend) conserve le SHA `84012115713aa568cb6f888b56c98d648574da4bf0b4d86f5cf1d97e280cc535`. La réexportation et l'installation par le pipeline commun n'ont changé ni sa forme, ni ses matières, ni ses 41 poses. Les 72 fichiers installés sont identiques à la banque approuvée : 4 963 460 octets, 31 sous-maillages, 15 matériaux, deux clips et trois os. Aucun rapport de validation n'est installé avec les assets. [Audit d'installation](sas-a-installation-audit.json).

Le manifeste installé porte le SHA `b2273f1483be9000b660481ca8af1ef2043276af26dc4bfb8806346a55e1dd87`. Le contenu du modèle est copié automatiquement dans les sorties de compilation et de publication par la règle existante du client.

## Branchement

`SasModelPresentation` sélectionne les mécanismes `ArmouredSas` de portée 3, avec leur axe cardinal. La source contient déjà la longueur complète : aucun facteur ×3 n'est appliqué. Le même `DoorModelRenderer` que la porte ordinaire anime les vantaux et dessine les ombres, avec les mêmes règles de profondeur et de visibilité à l'écran.

Le cache garde toutes les déclarations de portes pour construire la topologie des murs. Il retire seulement le corps et les accessoires 2D des bandes remplacées. L'ensemble des identifiants est copié pour chaque tâche de préparation ; un changement de mode invalide les anciens buffers et rétablit le dessin vectoriel. L'ouverture seule ne reconstruit pas le cache. Les portes ordinaires conservent leur banque, et les portes Pressure isolées d'une case gardent leur dessin existant. Le mode vectoriel, le rendu à plat et le repli si la banque manque restent disponibles.

Le banc externe reste utilisable pour les futures retouches. Sa bande choisie est exclue du modèle installé pour éviter un double dessin ; les autres bandes continuent d'utiliser le rendu normal.

## Captures du rendu installé

| Bande | Fermée | Ouverte |
| --- | --- | --- |
| Verticale | [Capture](sas-a-integrated-closed.png) | [Capture](sas-a-integrated-open.png) |
| Horizontale | [Capture](sas-a-integrated-horizontal-closed.png) | [Capture](sas-a-integrated-horizontal-open.png) |

Ces quatre images sont **identiques octet par octet** aux quatre vues correspondantes de la version approuvée. Elles sont produites par le rendu normal avec la banque installée, sans `THEEND_SAS_STUDY`, sans banque externe et sans substitution du `DisplayFrame`. Pour examiner précisément les deux extrémités de l'animation, le diagnostic pose les trois entrées réelles de `DoorMap` en état fermé ou ouvert avant la capture. Les JSON voisins enregistrent cette mise en pose, la source, les trois identifiants, leurs ticks et leur ouverture ; ce n'est pas un trajet de colon mis en scène.

Depuis Code, reproduire avec :

```powershell
.\scripts\run-sas-study.ps1 -Installed -Mode closed -Axis vertical
.\scripts\run-sas-study.ps1 -Installed -Mode open -Axis horizontal -NoBuild
```

`THEEND_SHOT_SAS=vertical|horizontal` seul permet aussi de cadrer un sas dans son état actuel. `THEEND_SHOT_SAS_POSE=closed|open` active la mise en pose diagnostique. Ces réglages sont propres aux captures ; le jeu ordinaire lit ses états de simulation.

Le modèle et la vidéo retenus restent documentés dans [la retouche validée](retouche-murs-ouverture.md). Le fichier Blender sauvegardé demeure la source de travail. Aucun commit ou push Code, Art ou Docs par l'assistant.

## Vérification terminée

**1 755 tests Debug réussis, aucun échec ni test ignoré**, en 3 min 21 s : Renderer, Development, Display et Sas. Compilation Client sans erreur ni avertissement. Les nouveaux tests font parcourir un cycle au vrai `DoorSystem`, puis vérifient l'ouverture publiée et la pose du modèle, les deux axes et la distinction avec les autres portes. Ils couvrent également les changements de masque du cache à révision de grille identique, sa stabilité pendant l'ouverture, ainsi que le rig et les surfaces de la banque installée.

Les quatre captures installées sont identiques aux vues approuvées. La capture de régression du jeu normal sur les débris est également identique à la référence antérieure ; les six empreintes des sources et manifestes de porte ordinaire, rocher et débris sont conservées. Les règles Core n'ont pas été modifiées. [Rapport final d'intégration](sas-a-integration-check.json).

Commande de contrôle utilisée :

```powershell
dotnet test TheEnd.Tests/TheEnd.Tests.csproj -c Debug --no-restore --filter 'FullyQualifiedName~TheEnd.Tests.Renderer|FullyQualifiedName~TheEnd.Tests.Development|FullyQualifiedName~TheEnd.Tests.Display|FullyQualifiedName~Sas'
```
