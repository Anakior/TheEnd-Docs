# Postes, échelle et reprise des lits/flaques — 13 septembre 2026

Historique : les retours suivants jugent les draps trop texturés et l'échelle
trop éclairée en profondeur. La [V3](../interior-details-review-v3/README.md)
reprend ces deux points et ajoute l'espace peint demandé ensuite.

Ludovic signale les postes spécialisés et l'échelle encore vectoriels, les lits
insuffisamment peints et les flaques ressemblant à des taches grises. Cette passe
répond à ces retours dans le jeu normal. La direction peinte générale reste celle
déjà retenue ; ce nouveau lot attend son prochain retour artistique.

## Changements

| Famille | Rendu installé |
| --- | --- |
| Postes spécialisés | Cinq équipements distincts : cuisson 2 × 2, douche 1 × 2, cœur de fusion 4 × 3, filtre de vestibule 1 × 1 et décontamination 1 × 1 ; chacun sealed/open/stripped/collapsed. Banque dédiée, sélection par définition et dimensions réelles. |
| Échelle de service | Trémie peinte, vrai cuvelage en profondeur, rails/barreaux et poignées en volume. Intact ou cassé selon la route manuelle ; l'électricité n'intervient pas. |
| Lits | Nouvelle peinture du textile : plis en masses colorées et touches visibles, assortis au métal peint. Douze variantes et toute la géométrie/UV conservées exactement. |
| Flaques sur dalle | Film humide sombre et transparent, silhouette pincée/irrégulière, ménisque interrompu et trois petits reflets localisés. Le voile gris uniforme et les stries régulières sont abandonnés. |

Le lac du dôme, les dix dalles métalliques d'origine, les banques de mobilier
approuvées, la glace, les câbles et l'ascenseur ne sont pas retouchés dans cette passe.
Les états et emprises de la simulation sont préservés ; les variantes absentes ou
incompatibles conservent leur présentation existante.

Les nouvelles banques utilisent le renderer et les caches de modèles communs.
Le masque des accès verticaux est reconstruit seulement à un changement de révision.
Les coordonnées locales des flaques sont calculées à leur préparation et utilisent
deux attributs déjà présents : sommets GPU de 44 octets, sans upload par frame.

## Sources et fabrication

- `TheEnd-Art/objects/station-equipment/station-equipment.blend` → `Assets/models/station-equipment`.
- `TheEnd-Art/objects/service-ladder/service-ladder.blend` → `Assets/models/service-ladder`.
- `TheEnd-Art/objects/bed/bed.blend` → `Assets/models/bed`.
- [Détail de la flaque et preuves](puddles.md).
- [Rapport de l'échelle](service-ladder-validation.json).

Les sources Blender sauvegardées restent la vérité ; les anciens générateurs ne
sont pas rejoués pour exporter. Le textile V2 vient d'ImageGen intégré, sans API
externe ni retouche raster par script. PNG et prompt exact avec références :
`TheEnd-Art/objects/bed/textures/bed-textile-painted-v2.png` et
`bed-textile-painted-v2-prompt.txt`. La validation `textile-v2-validation.json`
confirme la conservation des sommets, faces, UV et transformations.

## Contrôles natifs préliminaires

Ces vues utilisent le vrai TheEndGame, les assets installés, sans override de
banque/matière ni changement du monde. Le helper sélectionne uniquement le pont,
la caméra et une pause au tick 12000. Le zoom 96 est réservé à l'inspection native,
sans redimensionnement des PNG ni changement du zoom maximal normal.

- [Flaque corrigée](puddle-second-retry/game-02-FloorPuddle.png), rapport voisin Passed=true.
- [Échelle](ladder-inspection/game-06-ServiceLadder.png), masque de neuf cases vérifié.
- [Lits en salle](bed-inspection-retry/game-03-Bunk-Sealed.png), les trois états réellement
  présents sont capturés, sans inventer un état ouvert dans la simulation.

Les captures `puddle-first` montrent le premier réglage rayé abandonné. Deux premiers
lancements du helper (`puddle-second` et `bed-inspection`) se sont fermés avant
l'initialisation, sans diagnostic et sans image. Les relances ont réussi ; ces
dossiers ne constituent pas une preuve de validation. Aucun diagnostic Windows
nouveau n'est établi à partir de ces sorties précoces.

## Validation finale

Client compilé avec **0 avertissement et 0 erreur**, puis **704 tests ciblés réussis**,
dont 170 postes, 103 lits, 15 échelle et 14 flaques. [Compilation](build-final.log),
[tests](tests-final-r2.log), [TRX](interior-review-final-r2.trx).
Le premier passage avait 703 réussites et une borne de test trop basse pour la
trappe relevée du cœur de fusion : sa hauteur voulue est 1,721818 m, vérifiée dans
la source et l'aperçu Ouest. Le test utilise désormais cette enveloppe distincte.
Aucune géométrie n'a été modifiée pour masquer cet échec.

[Validation des assets](asset-validation.json) : 46 fichiers lits, 29 ascenseur,
65 postes et 31 échelle, chacun identique entre export validé, Code et sortie du
client. Les sources correspondent aux rapports Blender ; les seize empreintes
historiques, dont les dix dalles, sont préservées.

Les [douze captures finales à 48 px/case](game-final/native-game-validation.json)
chargent les sept banques attendues depuis le client, sans override. Les objets
ciblés ne sont plus dans la liste vectorielle ; le masque de l'échelle couvre bien
les neuf cases. Les caches de présentation restent stables pendant 35 frames.
Quatre postes sont réellement présents dans ce monde : cuisson, douche, fusion
et filtre. Le module de décontamination est validé par son modèle et ses tests,
sans être présenté comme capturé dans le monde. Il en va de même des états absents
des salles sélectionnées : les variantes sont contrôlées en atelier et dans les tests.

- [Poste de cuisson dans la salle de la capture utilisateur](game-final/game-10-Station-poste-cuisson.png).
- [Douche](game-final/game-09-Station-module-douche.png).
- [Cœur de fusion](game-final/game-07-Station-coeur-fusion.png).
- [Filtre](game-final/game-08-Station-filtre-vestibule.png).
- [Lits](game-final/game-03-Bunk-Sealed.png).
- [Échelle](game-final/game-06-ServiceLadder.png).
- [Flaque](game-final/game-02-FloorPuddle.png).

L'[inspection rapprochée des quatre postes](station-inspection/native-game-validation.json)
à 96 px/case passe également, avec les mêmes banques et la même DLL. Les quatre
images ont été relues : peinture, volumes, placement et occultation des murs cohérents.

**Dôme complet identique à la référence approuvée : 0 pixel différent sur
2 073 600**, ainsi que les régions eau, berge et profondeur. Le shader de lac et
ses attributs de vagues restent inchangés ; son horloge et sa stabilité sont aussi
couverts par les tests. Ce contrôle n'est pas un benchmark FPS global.

DLL finale : `544B258FD0E28F2F43C67A6CDA43FFFCD5EB800180381E8CFD0FE5E42454B88F`.
Shader : `DF5011EE7B24E90325A2A05FAEECFAD60F6660EEF12F34328CAB7E1B6DEC5BED`.
Aucun commit/push Code, Art ou Docs ; Ludovic conserve les commits.
