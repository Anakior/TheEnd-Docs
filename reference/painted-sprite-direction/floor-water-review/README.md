# Dalles d'origine et eau progressive — 12 septembre 2026

**Suite : intégration effectuée dans le jeu normal.** Ludovic a demandé de conserver l'ensemble pour continuer les retouches directement en jeu. Voir la [preuve d'intégration](../production-integration/README.md) ; les captures de cette page restent la référence approuvée avant installation.

**Retour après la revue jouable : validé.** Ludovic : « C'est vraiment bien comme ça. Pour l'eau notamment ! Cela rend vraiment bien. » Cette eau progressive et animée, associée aux dalles d'origine, devient la référence artistique retenue pour la suite du décor peint.

Ludovic signale la répétition de la dalle peinte et une eau qui paraît uniformément profonde et immobile. Les six variantes de dalle proposées ensuite sont rejetées : il préfère explicitement **l'ancienne dalle du jeu, avant le passage au style peint**.

L'étude active `TheEnd-Art/sprite-render/painted-world-materials-v4` conserve les huit matières du décor V3 et revient aux dix dalles standard/usées installées, via le fallback normal du chargeur. Les six propositions rejetées sont préservées sous `rejected-floor-variants`, hors des alias actifs. Les 70 modèles de mobilier peints restent identiques. Le [rapport de matières](material-validation.json) distingue les mesures historiques des propositions rejetées et le choix actif.

L'eau conserve le PNG peint V3. La correction vise une berge transparente plus large, une zone turquoise peu profonde puis une transition vers le large, avec une animation du matériau indépendante de la pause du monde. L'origine du défaut était double : le shader multipliait une texture déjà sombre par une teinte inférieure à un, et l'essai en pause figeait le tick utilisé par les vagues.

## Rendu et contrôle natifs

- [Salle avec dalles d'origine](game-room-original-floor/game-2-Table-Sealed.png) : pont 0, centre (95.5,89), 48 px/case, tick 12000. La matière du sol installée retrouve sa place parmi le mobilier et les murs peints. Le chargeur ne trouve aucun remplacement externe des dix dalles ; les alias actifs chargent seulement huit matières, une fois chacune.
- [Eau au début de la séquence finale](game-dome-motion-final/game-7-Dome-Environment-t0000ms.png) et [après trois secondes visuelles](game-dome-motion-final/game-7-Dome-Environment-t3000ms.png) : pont 3, centre (124,146), 48 px/case. Le rivage est plus transparent sur une case, puis la teinte turquoise rejoint la profondeur sur quatre cases. Ce sont des captures du jeu, sans retouche d'image.
- [Séquence native finale](game-dome-motion-final/native-game-validation.json) : sept instants visuels exacts de 12000 à 12360, sur six secondes ; tick du monde constant à 12000, mêmes surface et buffers, une publication d'eau et révision du mobilier stable. Le [contrôle des pixels](water-motion-validation.json) confirme que les zones sèches de sable, herbe et murs sont strictement identiques sur les sept images et à V3, tandis que 99,30 à 99,50 % des pixels de la région d'eau mesurée changent entre chaque seconde. Il s'agit de sept instants, pas d'une mesure de fluidité continue.

Le premier essai `game-dome-motion` avait reçu une interaction avec le panneau de personnage : quatre captures avaient une zone de vue décalée. Il ne valide donc pas sept cadrages identiques malgré ses métadonnées de temps/cache correctes. Le helper utilise maintenant la garde de saisie existante du jeu, via `CaptureInputSuppressed`, uniquement pendant ses captures. La revue interactive garde toutes les commandes normales. La séquence finale est la preuve de référence.

## Code et vérification

Le profil s'active seulement après le chargement réussi du PNG d'eau externe. La branche du matériau installé conserve ses teintes et son horloge de simulation. Les vagues croisées, leur période spatiale de neuf cases et les contours existants sont conservés. La distance au rivage, déjà calculée pour les couleurs, est également conservée dans les buffers ; le shader interpole cette distance pour la transparence et les gains de couleur.

L'horloge de présentation suit `GameTime.TotalGameTime` à 60 unités/s, indépendamment de la pause et de la vitesse du monde. Les captures du harness natif suivent leur tick de simulation déterministe ; le helper peut imposer explicitement son propre tick visuel. La correction ajoute quatre octets par sommet GPU et un tableau CPU de distances, sans chargement de texture, calcul de contour ni transfert de sommets par image. Ce contrôle n'est pas un benchmark FPS.

Shader recompilé, Client et helper compilés sans erreur ni avertissement. La suite ciblée eau/géométrie/cache/horloge/chargement de matières passe **46 tests**, puis **4 tests d'horloge** sont rejoués après le raccord du harness natif. Il ne faut pas additionner ces deux nombres, car ils se recouvrent. Voir `validation-transcript.txt` et `water-clock-final.trx`. Le dernier raccord de saisie du helper a ensuite été compilé et vérifié par la séquence native finale.

La capture de salle et la première séquence utilisent le Client `62EEED2D42A7672AF92841410F630CBFD9BC9C6367150389BC748D842447EF5C`. La séquence finale et la revue utilisent `F690B05A849F8BD8ECDDAAEFCF6691EB318AAFD8C58CE11BCDCE7A9D047312B6` : seuls le raccord de l'horloge du harness et la garde de saisie de capture ont changé entre les deux. Shader identique `856EABBCA36457DA58B68D55B88567F9BF109C5BD2B8BF12F088D7CE353360DD`. Core, lumières et banques de mobilier inchangés pendant cette reprise.

## Reprise

Jeu normal avec l'étude externe : `TheEnd/tools/fixtures/open-painted-world-study.ps1 -NoBuild`. Le lanceur pointe désormais sur V4. Pour reprendre directement sur le dôme en pause, depuis TheEnd :

```powershell
.\.artifacts\fixture-complete\native\run.ps1 -NoBuild -InteractiveDome -SpriteMaterialsDirectory C:/workspace/TheEnd-Art/sprite-render/painted-world-materials-v4
```

`-InteractiveRoom` donne le même accès libre depuis la salle. Le placement ne s'effectue qu'une fois ; aucune sortie automatique. Les modes de capture sont `-RoomOnly` ou `-DomeOnly -WaterMotion -FixedVisualTick 12000`, avec `-Output` vers un nouveau dossier.

Revue lancée le 12 septembre 2026, processus local 38752, fenêtre « The End » prête au dernier contrôle. Ce PID est historique et doit être revérifié à toute reprise.

Cette passe était une étude externe. Les anciennes dalles et l'eau corrigée ont été retenues après la revue jouable, puis Ludovic a demandé l'intégration de l'ensemble. Les éléments sont désormais embarqués dans le client ordinaire ; les références ci-dessus restent conservées. Aucun commit/push Code, Art ou Docs de l'assistant.
