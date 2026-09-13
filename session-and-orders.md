# Accueil, menu de session et premiers ordres

Passe du 13 septembre 2026, intégrée au client ordinaire pour la clôture d’usage de M2.4. La première passe sprite est considérée comme réalisée ; cette livraison ne prononce pas à elle seule la clôture artistique et fonctionnelle de M2.4.

## Parcours joueur

- Au lancement : Continuer, Nouvelle partie, Réglages, Quitter. Continuer est indisponible sans sauvegarde. Le monde est préparé après le choix du joueur.
- En jeu : Échap ferme d’abord la fenêtre HUD courante, puis ouvre le menu de session. Celui-ci propose Reprendre, Sauvegarder, Charger, Réglages, Accueil et Quitter.
- Le menu de session suspend la simulation sans changer la vitesse ni la pause choisies. Les réglages partagent la langue, l’échelle et la préférence de mouvement réduit du HUD.
- Charger, revenir à l’accueil ou quitter depuis une session demandent confirmation. Les opérations de fichier donnent un retour lisible ; un échec de chargement préserve la session en cours.
- Cliquer un personnage dans le monde ou le roster, puis faire un clic droit à destination. Le menu contextuel porte uniquement le prénom et le nom en tête, puis propose « Aller ici ». Pas de titre « Ordres », de préfixe « Avec » ni de croix, conformément au dernier retour de Ludovic. L’ouverture seule ne donne aucun ordre. La commande d’ouverture d’un cryopod occupé reste disponible dans ce même menu.
- Une destination inaccessible ou déjà atteinte présente une action grisée et sa raison. Échap ou un clic extérieur ferment le menu. Une sélection morte, en rupture, contenue, en réveil cryogénique ou située sur un autre pont ne reçoit pas cet ordre.

## Points de reprise

`OrderContextMenu` conserve l’auteur, le pont et la destination au moment du clic droit. Le chemin est vérifié à l’ouverture puis lors de la confirmation, sans recherche à chaque image. `GameInput` et `HudPanelPolicy` assurent le routage UI-first et empêchent un clic dans le menu d’agir sur le monde derrière.

`SessionMenuState` porte la navigation et les confirmations ; `SessionMenuScreen` utilise les matériaux peints et la typographie du HUD. `TheEndGame` déclenche le bootstrap sur choix explicite et suspend les mises à jour de simulation pendant le menu. Pour Continuer, le chargement intervient dans `GameRuntime.Start` après l’initialisation et avant la préparation des portraits et la première image du monde.

La sauvegarde reste `world.json` dans le répertoire de travail ; aucun nouveau format ni migration. `GameInput.SaveWorld` et `LoadWorld` partagent le stockage et le nettoyage des interactions avec les raccourcis existants Ctrl+S et L. Les bancs natifs qui activent le harnais intégré ou `CaptureInputSuppressed` conservent leur démarrage direct.

## Validation

La suite complète Release compte **5 403 tests réussis, zéro échec et zéro ignoré** avant la simplification finale du menu contextuel. Après cette retouche, la suite ciblée UI, entrées, localisation et pathfinding a été repassée : **702 tests réussis en Debug et 700 en Release** (deux cas réservés à Debug). Les compilations Debug et Release passent sans avertissement ni erreur. Les 19 fichiers C# modifiés ou créés ont été vérifiés avec CSharpier.

Les preuves sont dans `reference/session-order-menu` : résultats TRX, `test-summary.json`, captures PNG natives et observations du parcours dans `session-menu-validation.json`. Les sauvegardes des captures utilisent des répertoires isolés sous `.artifacts/session-menu/worlds` ; aucune sauvegarde du joueur n’a été lue ni modifiée.

Le premier run `native-100` est intermédiaire : son override de backend forçait le sprite sur les deux vues d’ordres. Ses contrôles du menu et de restauration restent valides, mais seule la capture finale sans cet override sert à comparer les deux rendus.

`native-100-final` valide les quatre vues à 100 % avant épuration du contexte ; `native-200` valide l’accueil et le menu de session avec la préférence agrandie. **`native-context-refined` est la référence finale**, avec le nom seul et sans croix. Ses deux vues d’ordres sont bien prises dans les backends sprite et vectoriel respectifs. Le même parcours vérifie : 40 images sans avancer au tick 12402 dans le menu malgré vitesse 3 ; reprise puis restauration au tick 12405 des 36 identités/cellules et 1 284 fixtures ; clic droit sans commande, action unique, et arrivée de Sophie sur le pont 0 en (53,47) au tick 12526.

Limites du premier accueil : il propose une nouvelle partie avec la configuration de développement existante, sans créateur de famille ni choix d’arche. Continuer effectue le bootstrap avant restauration et peut donc prendre le temps d’un chargement initial. La vitesse et la pause sont conservées par Reprendre et Charger dans la session ; après Accueil puis Continuer, elles reviennent aux valeurs initiales, car `world.json` ne les sérialise pas.
