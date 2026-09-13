# Glace, câbles, ascenseur, flaques et lits — 13 septembre 2026

**Passe historique** : Ludovic a ensuite rejeté le rendu des flaques, demandé des
lits plus peints et signalé les postes spécialisés ainsi que l'échelle manquants.
La [retouche V2](../interior-details-review-v2/README.md) suit ces retours ; les preuves
ci-dessous décrivent uniquement l'état V1, sans constituer son approbation artistique.

Ludovic repère cinq familles encore décalées du décor peint : glace, câbles d'infrastructure de la pièce gelée, ascenseur, petites fuites d'eau sur dalle et lits. Cette passe poursuit les retouches dans le jeu normal, après l'intégration approuvée du 12 septembre.

## Contenu du client

- **Glace** : matière givrée peinte peu saturée, fissures fines et inclusions laiteuses. Dépôt statique avec contour érodé et transparent ; triangles contenus dans les cellules de glace, UV continus entre cellules. Aucun aplat cyan ni lumière émise. Source PNG intacte dans `TheEnd-Art/sprite-render/interior-details-v1`, installée dans `TheEnd.Client/Assets/sprites/interior-details-v1`.
- **Câbles et conduits** : corps arrondis avec peinture de rail approuvée, colliers et raccords, brins exposés ou coupés selon les arêtes du graphe. Les ruptures restent vides et les extrémités intactes rejoignent leur fixation murale. Les familles restent indépendantes aux croisements. Les arcs d'énergie ne font pas partie de ce remplacement.
- **Ascenseur** : source sauvegardée `TheEnd-Art/objects/elevator/elevator.blend`, banque `Assets/models/elevator`. Plateforme basse 3 × 3, panneaux épais, guides et vérins latéraux, commandes discrètes. Les trois états `broken`, `unpowered`, `ready` suivent directement Working/Passable de la route ; la cage du dôme respecte sa règle actuelle. Seules les empreintes entièrement compatibles sont remplacées.
- **Lits** : source sauvegardée `TheEnd-Art/objects/bed/bed.blend`, banque `Assets/models/bed`. Couchette, lit médical et table d'examen, chacun dans les quatre états sealed/open/stripped/collapsed : **douze variantes**, matelas, textiles, oreillers et structures en volume. La table d'examen garde un matelas technique sans couverture ni oreiller. La tête suit les quatre orientations du mobilier.
- **Flaques** : les composantes d'eau entièrement sur Metal/BrokenMetal utilisent une pellicule transparente gris froid, des bords fins et des reflets très calmes. Elles n'échantillonnent plus le PNG à grandes vagues du lac. Le reste de l'eau conserve son shader et ses paramètres validés.

Les dix dalles métalliques d'origine restent préservées. Les modèles peints installés précédemment restent en place. Aucun état gameplay ou mécanisme de déplacement modifié.

## Cache et repli

Glace et infrastructure : géométrie et buffers GPU conservés, dessin limité aux régions visibles de 32 cases ; aucune construction ni upload dans Draw. Le stamp de visibilité des features sépare la glace des écritures d'atmosphère. Les raccords de câbles suivent aussi le stamp des murs. Quand le sprite remplace les lignes, leur cache vectoriel ne prépare plus de variantes de zoom cachées ; le retour vectoriel ou le manque de matière réactive ce chemin.

Les textures sont chargées au démarrage et partagées. Lits/ascenseur utilisent les banques de modèles communes au client avec culling et profondeur. Les cas non couverts restent sur leur dessin existant. Un changement réel du sol sous une eau visible invalide désormais sa préparation pour réévaluer flaque/lac. La classification des composantes est capturée avant le worker, sans lui transmettre le tableau de cellules mutable.

## Validation

Client final compilé avec **zéro avertissement et zéro erreur**, puis **517 tests ciblés réussis** : lits, ascenseur, eau, horloge, caches, grille, glace et infrastructure. Voir [compilation finale](build-final.log), [tests finaux](tests-final-r1.log) et [TRX](interior-details-final-r1.trx).

[Validation des fichiers](asset-validation.json) : 46 fichiers runtime pour les lits, 29 pour l'ascenseur, tous identiques entre export validé, Assets du Code et sortie exécutable. Sources Blender conformes aux rapports d'export ; aucune erreur de skinning mesurée par le validateur. La glace est identique dans Art/Code/bin. Les seize empreintes historiques (dix dalles et six banques) sont conservées.

Client : `7FA4240178BA51A63D13B446AD7FCF09B9283FC6EDC39E4744434A05C4FCA27D`.
Shader final : `566DEC43486A157BE07B8F234D3EBF91E450B706BA0F28DB421D20B92514817B`. Après les 517 tests, seule la valeur du reflet et du liseré de la technique de flaque a été ajustée et le shader recompilé ; la DLL et la technique du lac sont inchangées.

Les captures natives utilisent le vrai TheEndGame, ses assets installés et aucun override de banque/matière. Elles sélectionnent des cibles réellement présentes sans modifier le monde : glace et câbles au pont 2, ascenseur et flaque au pont 1, puis les états de lits disponibles et le dôme. Monde et temps visuel figés au tick 12000. Le premier passage `game-r0` est conservé comme diagnostic avant la correction finale des raccords de câbles ; son dôme est strictement identique pixel par pixel à la référence approuvée sur les 2 073 600 pixels.

Captures finales : `game-final` à 48 pixels/case. L'inspection `game-inspection` utilise 96 pixels/case, appliqués directement à la caméra du helper ; elle ne redimensionne ni ne retouche les PNG. Le dôme reste à 48 pour la comparaison. Le zoom 96 est un outil de revue, pas une modification des bornes de zoom du jeu. Les rapports natifs consignent provenance, monde, caméra et stabilité des caches.

La revue rapprochée a montré une flaque trop peu lisible dans cette salle sombre. Le dernier réglage garantit un léger reflet gris bleu même lorsque la grande zone de reflet s'annule ; le liseré passe à .11, et au moins 41 % de la dalle reste visible. Aucun PNG de vague échantillonné. Les captures de flaque dans `game-final` et `game-inspection` documentent donc ce réglage antérieur ; la flaque finale est dans `game-water-final-r2` et `game-water-inspection`, avec l'empreinte du shader dans les rapports. Le dossier `game-water-final` conserve une tentative arrêtée avant initialisation, sans PNG ni erreur stdout ; cause non établie, remplacée par la relance r2.

Aperçus natifs : [glace et câbles](game-inspection/game-00-IceAndCables.png), [ascenseur](game-inspection/game-01-Elevator.png), [lits](game-inspection/game-03-Bunk-Sealed.png), [lits cassés](game-inspection/game-05-Bunk-Collapsed.png), [flaque finale](game-water-final-r2/game-02-FloorPuddle.png).

**Dernière validation native réussie** : sept vues à 48 dans [game-water-final-r2](game-water-final-r2/native-game-validation.json), puis [flaque à 96](game-water-inspection/native-game-validation.json). Même DLL et shader final vérifiés, aucun override ; caches stables sur 35 frames pour chaque cible. Le dôme complet reste identique pixel par pixel à la référence approuvée, **0 pixel différent sur 2 073 600**, ainsi que les trois régions eau/berge/profondeur. La flaque finale est relue aux deux échelles : pellicule gris froid, dalle et joints visibles ; contour arrondi hérité de la géométrie existante.

## Reprise

Lancer normalement `C:/workspace/TheEnd/TheEnd.Client/bin/Debug/net9.0/TheEnd.Client.exe` depuis son dossier après compilation. Aucun lanceur d'étude ni accès à Art n'est requis. Les cibles peuvent se retrouver dans le vrai vaisseau avec les coordonnées des rapports de capture.

Pour les modèles, partir des `.blend` sauvegardés et utiliser le pipeline `TheEnd-Art/tools/models/build-model.ps1 -Source objects/<famille>/<famille>.blend -InstallAs models/<famille>`. Les nouvelles matières ont été générées avec l'outil imagegen intégré : [prompt glace](../../../../TheEnd-Art/sprite-render/interior-details-v1/ice-frost-painted-prompt.txt) et prompt textile dans `TheEnd-Art/objects/bed/textures/bed-textile-painted-prompt.txt`. Les deux sorties originales restent conservées ; pas d'API externe ni de retouche d'image par script.

Ces ajouts sont implémentés pour la revue artistique de Ludovic ; leur intégration technique ne vaut pas son approbation visuelle. Aucun benchmark FPS global dans cette passe. Aucun commit/push Code, Art ou Docs de l'assistant ; sauvegarde Atlas ciblée en fin de travail.
