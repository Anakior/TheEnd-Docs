# Flaques : surface mouillée et reflets localisés

Le retour utilisateur porte sur une flaque ressemblant à un disque gris. Cette reprise retire le reflet uniforme : le sol reste visible, assombri par l'humidité, avec un contour pincé, un ménisque interrompu et trois petits fragments de luminaires sur un côté. Les reflets combinent une partie nette et une frange diffuse. La matière et les grandes ondulations du lac ne sont pas utilisées.

La [seconde capture native à 96 pixels/case](puddle-second-retry/game-02-FloorPuddle.png) a été retenue pour les contrôles finaux et la prochaine revue utilisateur. Elle remplace le [premier candidat](puddle-first/game-02-FloorPuddle.png), dont les stries étaient trop régulières. Ce choix interne ne vaut pas approbation de Ludovic.

## Mise en œuvre

`SpriteWaterSkin.Build` calcule une fois la position locale et la demi-taille de la composante pour chaque sommet de flaque. Les composantes déconnectées gardent leurs propres coordonnées, même lorsqu'elles partagent un lot GPU. Seuls les lots de flaques possèdent ce tableau CPU supplémentaire.

`SpriteWaterGpu` transporte ces quatre valeurs dans les deux attributs de vagues inutilisés par `Puddle`. La taille du sommet GPU reste **44 octets**. Le chemin `Water` garde ses sinus/cosinus, sa texture, ses paramètres et son shader. Ni la classification Metal/BrokenMetal, ni les contours de simulation, ni les positions de sommets, ni les caches/publications ne changent. Aucun nouveau chargement, calcul de géométrie ou upload par frame.

Le pixel shader érode le bord uniquement vers l'intérieur, avec des variations statiques et une amplitude limitée selon la taille de la flaque. Le film humide conserve environ 65 à 76 % du sol avant les reflets. Le ménisque capte seulement une direction et certains segments. Les trois reflets ont des dimensions propres de l'ordre de 5 à 12 pixels à 48 pixels/case ; ils ne s'étirent pas sur toute la surface. Leur déplacement est très faible, avec l'horloge de présentation existante, tandis que la silhouette reste fixe.

Le mélange optique est prémultiplié, pour le `AlphaBlend` existant. Le reflet est composé sur le ménisque puis sur le film humide. Une relecture indépendante a confirmé les bornes d'alpha, l'ordre des coordonnées par sommet, la conservation des attributs naturels et l'immobilité du bord. Voir [preuve de la seconde révision](puddle-shader-second-review.json).

## Vérifications à ce stade

- Shader compilé avec `scripts/build-water-shader.ps1`, profil OpenGL, sortie 0.
- Préfixe complet du shader naturel strictement identique au fichier précédant cette reprise. L'empreinte de ce préfixe est conservée dans [le premier audit](puddle-shader-first-review.json).
- [Build coordonné du Client](build-first.log) : zéro erreur et zéro avertissement.
- [Capture native 96](puddle-second-retry/native-game-validation.json) : `Passed=true`, monde et temps visuel rendu au tick 12000, assets installés, aucun override de banque/matière. Cible réelle de quatorze cellules d'eau métallique, pont d'index 0, centre (73.21429, 209). Les caches d'intérieur surveillés sont stables pendant les 35 frames du contrôle.
- Deux tests supplémentaires dans `SpriteWaterPuddleTests` vérifient les domaines indépendants de flaques partageant un lot et la conservation exacte des attributs GPU du lac. La classe contient quatorze cas ; leur exécution appartient au cycle final coordonné, consigné séparément dans le dossier de cette revue.

La validation d'ensemble est terminée : les 14 tests de flaques passent dans le lot
de 704 tests, `interior-review-final-r2.trx`. La capture 48 dans `game-final` passe,
et le dôme complet reste identique à la référence approuvée (0 pixel différent sur
2 073 600). Les deux nouveaux tests ont bien été exécutés dans cette passe.

## Empreintes de la seconde révision

Les sources ci-dessous sont relevées après le formatage effectué avant le build coordonné.

| Fichier | SHA-256 |
| --- | --- |
| `SpriteWaterSkin.cs` | `9C02AB968A1A7FBC2F3F2626DE4CF31D4610E8C92C9FEB82D553AC3F2AAF272C` |
| `SpriteWaterGpu.cs` | `7F3A4CBA91CCD10A0115B2DEB94DBBE41BA53619884D746E76085616C468C10C` |
| `SpriteWaterPuddleTests.cs` | `EE5D1674A38C1335D9C8B3FFF8E7E311DB442AABC7DE8AE326DE5D186610C7E5` |
| `sprite-water.fx` | `E461DE44D2A94BD7A8BCDD1703AB4B1CF97D56FFF45F41911A9AD761BB13AEF0` |
| `sprite-water.mgfxo` | `DF5011EE7B24E90325A2A05FAEECFAD60F6660EEF12F34328CAB7E1B6DEC5BED` |
| Client de la capture 96 | `9A73AF4FA2A839095195421029A4881857484C0379EF8335A5712E5A66FAB79E` |

Le hash de shader chargé dans le rapport natif correspond à celui de cette table. Aucun PNG de dalle ou d'eau n'a été modifié. Le shader de flaque ne représente pas de vrais luminaires réfléchis par traçage : ce sont des fragments graphiques locaux, cohérents avec une direction d'éclairage. Une composante très étroite ou creuse peut masquer certains fragments, car ils restent découpés par sa surface réelle. Aucun benchmark FPS global ni nouvelle vidéo d'animation dans cette sous-tâche. Aucun commit/push.
