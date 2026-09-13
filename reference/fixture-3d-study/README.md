# Mobilier 3D — première passe à examiner, 12 septembre 2026

Les cryopods endommagés, tables, bancs, consoles et rangements disposent maintenant de sources Blender et de banques d'essai couvrant les états existants. **Cette direction n'a pas encore été approuvée artistiquement par Ludovic. Les banques sont chargées explicitement pour l'essai ; aucune n'est installée dans les assets du jeu normal.** Les cryopods intacts et leur ouverture approuvée restent inchangés.

## Examiner les propositions

Depuis `TheEnd`, lancer `./tools/fixtures/open-fixture-study.ps1`. Le script détecte les trois exports dans le dépôt Art voisin ; les arguments permettent d'utiliser d'autres banques. Le banc utilise les renderers, la lumière, les ombres et la projection du client, sur son sol métallique. Il n'ouvre ni ne modifie une sauvegarde.

- `1` à `5` ou `Tab` : cryogénie, tables/bancs, consoles, stations, rangements.
- `Page précédente/suivante` : autres tailles et habillages.
- `R` : rotation ; `+`, `-` ou molette : zoom.
- `P` : occupation de démonstration des cryopods ; `O` : ouverture animée ; `Échap` : fermer.
- Ajouter `-InGame` pour tester les mêmes banques dans le vrai jeu en mode sprite. Les positions et états viennent alors du jeu.

Exemples de captures reproductibles, dans des chemins de sortie encore libres :

```powershell
./tools/fixtures/open-fixture-study.ps1 -NoBuild -Page table-bench -GroupOffset 0 -Capture C:/captures/tables-bancs.png
./tools/fixtures/open-fixture-study.ps1 -NoBuild -Page consoles -GroupOffset 2 -Rotation 1 -Capture C:/captures/consoles.png
```

Le suffixe JSON de chaque capture identifie les banques, leurs empreintes, les variantes effectivement montrées et l'orientation. Les aperçus de fabrication sous Art viennent de Blender ; les PNG dans ce dossier proviennent du client natif.

## Périmètre et états

| Famille | Formats et habillages | Variantes nouvelles |
| --- | --- | ---: |
| Cryopod | Coque d'origine, vitrage brisé, service arraché ou flanc affaissé | 2 états endommagés |
| Table et banc | Longueurs 2 et 3, proportions et fixations dédiées | 16 |
| Console | Longueurs 2 et 3, Dalle / Visière / Peigne | 24 |
| Poste de commande en alcôve | 3×2 et 4×3, Dalle / Peigne | 16 |
| Rangement | Longueurs 1, 2 et 3 | 12 |

Soit **70 variantes nouvelles**, plus le cryopod intact et ouvert déjà approuvé. `FixtureCondition.Sealed` signifie aujourd'hui intact et complet : il représente le meuble normal/fermé, pas une soudure universelle. `Open` montre un accès ou panneau relevé ; `Stripped` montre du matériel retiré ; `Collapsed` montre une rupture et un affaissement. La distinction supplémentaire normal/scellé n'est pas créée dans Core. Les variantes de mobilier sont statiques ; l'animation d'ouverture approuvée du cryopod est conservée.

Les stations réacteur, douche, cuisson, filtration et décontamination ne sont pas des consoles : elles conservent leur rendu spécifique actuel. Le banc de batteries reste aussi dans son rendu actuel. Les lits et équipements médicaux de type Bunk ne font pas partie de cette passe. Les différentes peintures des postes ne changent pas leur fonction.

## Sources et export

| Source dans TheEnd-Art | Banque d'étude |
| --- | --- |
| `objects/cryopod/cryopod-damaged.blend` | `exports/cryopod-damaged` |
| `objects/common-furniture/common-furniture.blend` | `exports/common-furniture` |
| `objects/utility-furniture/utility-furniture.blend` | `exports/utility-furniture` |

Exporter chacune avec `tools/models/build-model.ps1 -Source <source>` depuis Art, sans `-InstallAs`. Les fichiers Blender sauvegardés sont la source de vérité ; l'exporteur ne rejoue pas les scripts de fabrication. La peinture de coque approuvée est réutilisée, UV et PNG packés. Les sources intactes, portes, sas, rochers et débris sont préservées.

## Raccordement et cache

`FixtureModelLayout` sélectionne les formats réellement construits, sans ajuster les bornes au rectangle logique ni grossir les fixations. Les bancs ont un axe de catalogue différent des tables, pris en compte dans leur placement. `DisplayObject.DefinitionId` conserve l'identité sémantique, nécessaire pour distinguer une console d'un réacteur.

`FixtureModelPresentation` conserve poses et bornes jusqu'à un changement pertinent. Les objets non pris en charge et les variantes absentes conservent leur ancien rendu. Les banques utilisent un seul ensemble de textures et buffers GPU par famille, chargé une fois. Les indices des sous-maillages d'une variante sont calculés au chargement ; dessiner un meuble ne parcourt pas toutes les variantes. Les listes visibles sont réutilisées et le culling tient compte du volume projeté. Les anciens corps/ombres vectoriels sont retirés seulement pour les objets effectivement remplacés. Les lumières d'environnement et les règles de jeu restent celles du client.

La banque cryopod endommagée est un compagnon optionnel, avec bornes propres à chacun de ses deux états. L'occupation suit toujours la présence réelle dans le pod en jeu, sans déduire un corps de son ancien occupant. En l'absence de banque compagnon, les états endommagés restent vectoriels.

Variables externes : `THEEND_COMMON_FURNITURE_BANK`, `THEEND_UTILITY_FURNITURE_BANK`, `THEEND_CRYOPOD_DAMAGED_BANK` ; chacune accepte le dossier d'export ou son manifeste. Elles sont locales au processus lancé par le script.

## Vérifications

Les trois exports passent le validateur commun : erreur maximale de skinning **0 m**. **1 810 tests Renderer et FixturePresenter réussissent, zéro échec et zéro ignoré.** Ils couvrent notamment les formats, les quatre orientations, les états, les marges physiques, les équipements exclus, les variantes manquantes, le retour vectoriel, la mutation des listes et la stabilité/allocation du cache après chauffe. Le TRX est conservé ici.

Sept captures sous `game/` viennent du vrai `TheEndGame`, avec les banques externes : deux cryopods endommagés, une table, un banc cassé, une console, un rangement dépouillé et un poste central. Seuls la pause, le pont et la caméra sont choisis par le helper ; aucune modification des fixtures, des états ou de la simulation. `game/native-game-validation.json` donne les identités, positions, états et tailles. Chaque cible est absente du rendu vectoriel et la révision du cache est stable pendant 25 images stationnaires. Ces captures vérifient le raccordement visuel ; ce n'est pas un benchmark FPS ni un test de trajet de colon.

Les propositions sont prêtes pour retour artistique avant installation. Aucun commit/push Code, Art ou Docs effectué par l'assistant.

Les 13 planches natives couvrent les 70 variantes nouvelles et le cryopod intact/ouvert, dont une comparaison vide/occupé et des vues Ouest. Les écrans des consoles sont nets après correction de faces coplanaires dans la source. Les trappes Open des consoles restent discrètes à petite échelle ; les cavités dépouillées pourront être approfondies selon le retour artistique.

Compilation finale sans erreur ni avertissement. Les tests, les sept captures en jeu et les douze premières planches utilisent la DLL `8780FD79CB12B26623DFEF2AEA452CCE317625CAE87C98623D517F9C00AA05D7`. La DLL finale `915D1B82BA14DD36D00B6E925566BF8938FC6EA1DED72B6223F4974042EA63DE` ajoute uniquement l'option d'occupation automatique et corrige un caractère du pied de page du banc ; `cryopods-occupied.png` a été contrôlée avec cette compilation. Aucun changement du rendu de production ni des banques entre ces deux compilations.
