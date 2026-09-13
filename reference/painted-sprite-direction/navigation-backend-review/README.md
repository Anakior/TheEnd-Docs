# Navigation ZQSD et bascule vectoriel/sprite — 13 septembre 2026

Ludovic demande le déplacement de caméra avec ZQSD et signale un chargement
à chaque retour du vectoriel vers le mode sprite. Les corrections sont intégrées
dans le client ordinaire. Les textures et modèles artistiques sont conservés.

## Commandes

Maintenir Z/Q/S/D déplace la vue vers le haut/la gauche/le bas/la droite,
y compris en pause. Vitesse constante dans le temps, diagonales normalisées,
fractions de pixel conservées ; molette et clic-molette gardent leur rôle.
Ctrl+S sauvegarde désormais, puisque S sert au déplacement. Dans le mode
d'édition de murs F2, D conserve l'outil ligne et le pan clavier est suspendu.
Les raccourcis R, C, P et L gardent leur routage existant.

Le focus clavier de l'interface, un panneau modal, une capture de pointeur,
le clic-molette ou un modificateur suspendent le déplacement au clavier.
[Commandes détaillées](../../../camera-keyboard.md).

## Cause et correction

Le changement de masque des sas appelait `ClearBuffers` et remettait le pont,
sa géométrie et ses sols à zéro, malgré une révision du monde inchangée.
Par ailleurs, le mobilier ne conservait qu'une présentation : le changement
de mode modifiait la révision des objets remplacés et chassait les lots précédents.
La garde de première image complète attendait donc une nouvelle préparation.

Le cache du pont garde maintenant sa structure vectorielle complète. Les
sprites utilisent déjà leurs propres surfaces murales ; leur petite couche
de quincaillerie de sas de secours est préparée et conservée séparément.
Changer le masque ne détruit plus les sols, murs et détails du pont.

Le cache du mobilier conserve deux présentations, chacune avec au maximum
deux niveaux de détail. Seule la présentation active prépare ou envoie des
données au GPU ; les révisions de remplacement dépendent des modèles disponibles,
sans varier lors d'un simple changement de moteur. Les erreurs et gardes de
cohérence restent propres à chaque présentation.

Le premier affichage d'un mode peut encore préparer son mobilier. Un retour
vers ce mode déjà préparé réutilise ses lots ; un vrai changement de pont,
d'objets ou de géométrie murale peut naturellement demander une nouvelle préparation.

## Vérifications

Client Debug compilé sans avertissement ni erreur : [journal](build.log).
**784 tests ciblés passent** : navigation, focus HUD, caches du mobilier,
publication des ponts, sas et infrastructure ; [résultats](navigation-backend.trx).
Un avertissement de nullabilité dans un nouveau test a ensuite été corrigé,
puis les quatre tests de la couche de secours SAS ont repassé sans avertissement :
[vérification finale](sas-hardware-final.trx).

DLL testée : `F5DF1BFAC16528FF97CA36C1A08ED14D8070EC50A36532164CF2BE5785836EC0`.
Les [mesures avant](native-before/backend-switch-validation.json) et
[après](native-after/backend-switch-validation.json) viennent du même vrai jeu,
au tick 12000, en pause, avec caméra fixe et sans override de moteur.

| Bascule | Avant : images indisponibles / délai | Après : images indisponibles / délai |
| --- | ---: | ---: |
| Premier sprite → vectoriel | 91 / 1 549 ms | 8 / 139 ms |
| Retour vectoriel → sprite | 78 / 1 410 ms | 0 / 13 ms |
| Deuxième sprite → vectoriel | 81 / 1 418 ms | 0 / 4 ms |
| Dernier vectoriel → sprite | 77 / 1 415 ms | 0 / 15 ms |

Le délai se mesure de la demande au premier Draw prêt, y compris le temps
normal d'une image. Zéro image indisponible signifie que l'écran de chargement
n'a pas été montré ; cela ne prétend pas à une exécution de durée nulle.
Le premier passage froid prépare encore le mobilier vectoriel, mais ne reconstruit
plus les sols et les murs. Les 47 textures et 11 banques restent les mêmes
instances GPU pendant toutes les bascules.

Ces mesures sont bornées à cette scène et à cette machine ; ce n'est pas un
benchmark FPS général. La première tentative d'instrumentation avant les bascules
avait échoué lors de l'énumération des textures : seul le helper a été corrigé,
puis les preuves ci-dessus ont été exécutées. La tentative initiale reste hors
des mesures. Aucune garde de readiness du jeu n'a été contournée.

La [comparaison finale](backend-switch-comparison.json) passe : les cinq paires
de captures avant/après sont strictement identiques en octets et SHA256. Les
références du pont restent identiques sur les quatre bascules. Les lots du
mobilier sprite sont conservés ; ceux du vectoriel sont créés au premier
passage puis réutilisés. Aucun processus de jeu ou de capture ne reste actif.

La relecture indépendante n'a pas trouvé de problème dans ce parcours du jeu
ordinaire. Elle relève un cas préexistant réservé au banc SAS : `studyAnchor`
continue d'exclure la quincaillerie 2D en vectoriel alors que le modèle d'étude
ne se dessine qu'en sprite. Ce mode de développement, hors de ces mesures,
reste à traiter si les essais SAS sont repris.

Aucun commit/push Code, Art ou Docs ; Ludovic conserve les commits.
