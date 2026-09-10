# Prompt — `tileset-sols-murs-pilote.png`

Mode : génération intégrée, avec `rendu-sprite-concept.png` comme référence de style et de matière uniquement.

```text
Use case: stylized-concept
Asset type: pilot game environment tileset board for a top-down 2D spaceship game

Input images:
- Image 1 is a STYLE AND MATERIAL REFERENCE ONLY. Preserve its cold abandoned industrial spaceship mood, dark steel palette, worn metal, frost traces, restrained cyan accents, and realistic painted-sprite finish. Do not reproduce its room composition.

Primary request:
Create one clean, production-oriented concept sheet containing exactly sixteen isolated square environment modules arranged in a precise 4 by 4 grid. The sheet explores only floors and walls for the same spaceship.

Tile content, left to right:
Row 1 — four seamless floor modules: quiet intact dark steel plates; subtly worn plates; cracked plates; plates with restrained frost gathered near seams.
Row 2 — four wall modules using one identical wall cross-section and thickness: horizontal straight; vertical straight; 90-degree outer corner; 90-degree inner corner.
Row 3 — four modules: 45-degree diagonal rising left-to-right; 45-degree diagonal falling left-to-right; diagonal-to-horizontal corner; diagonal-to-vertical corner.
Row 4 — four modules: closed wall end-cap; T junction; cross junction; centered doorway frame without a door leaf.

Style/medium:
High-quality painted raster game sprites, realistic but restrained, matching Image 1. Strong readable silhouettes at game scale. Consistent steel construction vocabulary: outer hull lip, structural metal frame, narrow inset service channel, occasional tiny muted rust accents. Floors must remain visually quieter than walls.

Composition/framing:
Exact orthographic 90-degree top-down view, never isometric and no perspective. Every module has identical square dimensions, camera scale, orientation rules, padding, and centered registration. Clear even gutters separate modules. No overlaps. No cropped modules. Plain uniform charcoal presentation background outside the modules.

Lighting:
Neutral soft overhead reference lighting only. No dramatic room lighting, no cyan pools, no long cast shadows, no baked directional lighting crossing tile boundaries. Materials and edges remain readable.

Constraints:
All floor edges should plausibly repeat without a visible focal seam. Every wall connection must meet the exact midpoint of the relevant tile edge and use the same width and cross-section. Diagonal pieces must connect geometrically to straight pieces. Keep frost and damage away from tile borders unless they form a repeatable seam. No furniture, cryopods, consoles, actors, UI, labels, numbers, legends, logos, watermark, decorative frame, or room scene. Exactly sixteen modules and no extras.

Output intent:
A practical first-pass tileset grammar board suitable for evaluating consistency and deciding what to regenerate before mechanical slicing and integration.
```
