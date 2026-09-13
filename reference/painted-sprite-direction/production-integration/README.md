# Décor et mobilier peints dans le jeu normal — 12 septembre 2026

Ludovic demande explicitement de valider et d'intégrer l'ensemble de l'essai pour poursuivre les retouches dans le vrai jeu. La direction peinte est retenue, avec l'eau progressive animée et les anciennes dalles métalliques du jeu. Les défauts artistiques encore visibles pourront être repris sur cette base.

## Éléments embarqués

| Banque du Client | Source conservée dans Art | Contenu |
| --- | --- | --- |
| `Assets/models/common-furniture` | `objects/common-furniture/common-furniture-painted.blend` | 16 variantes de tables et bancs courts/longs, quatre états |
| `Assets/models/utility-furniture` | `objects/utility-furniture/utility-furniture-complete-painted.blend` | 52 consoles, rangements et stations selon formats/habillages/états |
| `Assets/models/cryopod-damaged` | `objects/cryopod/cryopod-damaged-painted.blend` | Cryopods dépouillé et cassé ; banque intacte existante conservée |
| `Assets/sprites/painted-world-v4` | `sprite-render/painted-world-materials-v4` | Huit PNG actifs : trois matières de murs, terre, herbe, sable, sol fongique et eau |

Les trois banques de modèles comportent 956 fichiers runtime au total, tous identiques aux exports approuvés. Les sources Blender, l'exporteur et l'ensemble des hashes des rapports de validation ont été contrôlés avant toute copie. Seules les dépendances déclarées sont installées, manifeste en dernier ; les rapports restent dans Art. Détails : [installation des modèles](model-installation.json).

Les 12 alias peints partagent huit textures. Aucun des six essais de dalles rejetés n'est installé ; les dix dalles d'origine sont préservées. La banque de matières conserve sa provenance et ses empreintes dans le Client.

## Fonctionnement normal

Le client utilise par défaut les banques embarquées. Aucune variable d'environnement, aucun dossier Art/exports et aucun lanceur d'étude ne sont requis. Le mode sprite est déjà le mode par défaut du jeu. Les overrides d'étude restent disponibles pour comparer de futures retouches.

Le chargeur de matières essaie l'override éventuel, puis la banque peinte embarquée, puis l'ancienne texture. Les peintures finales gardent leurs valeurs sans gain supplémentaire ; les murs sont importés en 256² une fois. Le profil d'eau est maintenant associé à une peinture effectivement chargée, embarquée ou externe : berge transparente sur une case, progression turquoise/profondeur sur quatre cases, mouvement de matière même en pause. Les captures gardent leur temps déterministe. Aucun changement de simulation, de collision ou des états du mobilier.

## Vérification

Client compilé sans erreur ni avertissement. **358 tests ciblés passent** : matières, eau, horloge, caches, présentation du mobilier et des cryopods. Voir [journal de compilation](build.log), [journal de tests](tests.log) et [résultats TRX](painted-integration.trx).

Les **huit vues installées sont strictement identiques pixel par pixel aux huit références V4**, à mêmes caméra, monde et tick visuel 12000 : cryopods dépouillé/cassé, table, banc cassé, console, rangement dépouillé, station et dôme. Le mode installé ne contient aucune variable de banque ou de matière externe ; la provenance des modèles effectivement chargés est vérifiée. Chaque matière peinte est chargée une fois, depuis `BundledPaint`.

Captures : `reference-v4` et `installed-game`. Voir notamment la [console dans le client installé](installed-game/game-4-Console-Sealed.png), le [cryopod dépouillé](installed-game/game-0-CryoPod-Stripped.png) et le [dôme](installed-game/game-7-Dome-Environment.png). La séquence `installed-water-motion` reprend sept instants de l'eau sur six secondes : **les sept images sont également identiques pixel par pixel à la séquence approuvée**, sans transformation d'image. Le [rapport final](integration-validation.json), validé, regroupe les quinze comparaisons, empreintes et contrôles de caches.

Client final : `1D42A4A2620900FFBEC518B959D974ECE74A112290E25B5F83596951DF4B956B`. Les dix dalles et les six banques installées auparavant conservent leurs empreintes. Aucun nouveau benchmark de performances globales : cette passe vérifie l'intégration, la fidélité visuelle et les caches.

## Continuer les retouches

Lancer normalement `TheEnd.Client.exe` depuis son dossier `C:/workspace/TheEnd/TheEnd.Client/bin/Debug/net9.0` après compilation. L'exécutable ordinaire a été lancé directement, sans argument ni aucune variable `THEEND_`, pour la revue : PID 38776, fenêtre « The End » et simulation prêts au contrôle de 20:20:10. Les huit matières embarquées ont été chargées. Ce processus n'est plus actif au contrôle de 20:23:14 ; la cause de sa fermeture n'est pas établie. Provenance et première tentative depuis la racine dans [normal-launch.json](normal-launch.json), fonctionnement dans [normal-game.log](normal-game.log).

Les sources `.blend` restent les sources de vérité ; ne pas reconstruire les modèles avec les anciennes recettes. Depuis Art, exporter la source sauvegardée avec `tools/models/build-model.ps1 -Source <source> -InstallAs models/<banque>` selon le tableau. Pour les matières, conserver la liste des 12 alias et actualiser les PNG/provenances de la banque peinte retenue.

Ludovic conserve les commits Code, Art et Docs. Cette intégration est autorisée et effectuée localement, sans commit/push de l'assistant.
