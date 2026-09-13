# Murs peints : retrouver le contraste

Ludovic trouve le résultat réel convaincant, mais juge les murs différents et la luminosité moins bonne. La comparaison montre surtout une modification de palette : les creux sont devenus trop clairs dans la V2, alors que l'éclairage des modèles est conservé.

La V3 sépare la peinture de l'armure, des rails et des canaux. Le creux central retrouve une luminance proche de l'ancien rendu (18,94 contre 17,23 ; V2 était à 36,09). Le contraste local du dessus revient de 12,97 à 15,19, pour 15,44 dans l'ancien rendu. Ces mesures servent à expliquer la lecture du mur, sans prétendre remplacer le jugement artistique.

- [Capture native V3](game-dome/game-7-Dome-Environment.png).
- [V2 précédente, même scène](../complete/game-dome-final-paint/game-7-Dome-Environment.png).
- [Anciennes matières, même scène](../complete/game-before-world-paint/game-7-Dome-Environment.png).
- [Diagnostic des matières et des régions](diagnosis.json), [contrôle après correction](result.json).

Les trois nouvelles peintures, les prompts et leur provenance sont dans `TheEnd-Art/sprite-render/painted-world-materials-v3`. Les six autres textures V2 et les 70 modèles sont conservés. Aucun changement du renderer, des lumières, du Core ou des assets installés. Le lanceur `tools/fixtures/open-painted-world-study.ps1` pointe sur V3.

Le contrôle natif du dôme passe : même scène au tick 12000, caméra (124,146), pont 4/6, 48 px/case ; cache mobilier stable entre les images préparées 10 et 35. Le JSON de la capture identifie les banques, les textures et la DLL Client inchangée `FBAA2C887F44B744A677BED8BE3A5ABF890C82CCF85E25A2B9CB14E897CF8E2E`. Ce n'est pas une mesure de performances globale. Aucun test du Client n'a été relancé pour ces seules matières.

Le helper local `.artifacts/fixture-complete/native/run.ps1` a été recompilé seul (0 erreur, 0 avertissement) pour ajouter `-InteractiveDome`. Il ouvre le vrai jeu sur le dôme en pause, puis retire son composant de placement une fois la scène prête : aucun recentrage continu, timeout ou arrêt automatique. Les commandes normales restent disponibles. Ce mode ne capture rien et ne change pas les états du monde.

```powershell
./.artifacts/fixture-complete/native/run.ps1 -NoBuild -InteractiveDome -SpriteMaterialsDirectory C:/workspace/TheEnd-Art/sprite-render/painted-world-materials-v3
```

Les trois versions de matières et leurs captures restent conservées. Aucun commit/push Code/Art/Docs de l'assistant.
