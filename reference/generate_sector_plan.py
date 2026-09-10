#!/usr/bin/env python3
"""
Génère un secteur TheEnd déterministe. La référence fixe la forme ; le look est
gelé.

Règle de placement — Les pièces sont posées de la plus grande aux plus petites,
puis poussées vers la coque. Un emplacement est refusé à moins de quatre cases
de la coque ou d'une autre pièce, ou s'il coupe le passage large de six cases
vers un col. Après la dernière pièce, les plus courts chemins relient les cols
dans le reliquat ; la graine ne départage que des candidats valides.

Tassement : tailles grande/moyenne/petite 24–28/14–18/8–12,
ROOM_SPACING_CELLS 4 partout et PACKING_CHOICE_POOL 1–8.
La recherche garde PACKING_SCAN_STEP_CELLS à 1–2 et
PACKING_BACKTRACK_LIMIT à 64–1024.

PNG : mêmes arguments, mêmes octets.
"""

import argparse
import hashlib
import math
import random
from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageChops, ImageDraw


# =============================================================================
# GÉOMÉTRIE DU SECTEUR — toutes les distances de cette section sont en cases
# =============================================================================

# Source : dérivée de l'unité du monde ; toutes les fractions de distance partent de cette case.
ONE_CELL = Fraction(1, 1)

# Source : dérivée de ONE_CELL ; sert aux centres de cases et aux constructions symétriques.
HALF_CELL = ONE_CELL * Fraction(1, 2)

# Source : jugée à l'œil d'après le rapport largeur/hauteur du plan de référence.
SECTOR_WIDTH_CELLS = 104

# Source : jugée à l'œil d'après le rapport largeur/hauteur du plan de référence.
SECTOR_HEIGHT_CELLS = 76

# Source : lue sur la coque principale du plan ; deux pans successifs remplacent chaque angle.
SECTOR_PAN_COUNT = 12

# Source : jugée à l'œil d'après les larges angles coupés du plan, puis quantifiée en cases.
SECTOR_ANGLE_CUT_CELLS = 10

# Source : dérivée de SECTOR_ANGLE_CUT_CELLS ; le premier pan monte de la moitié de la coupe.
SECTOR_SHOULDER_RISE_CELLS = SECTOR_ANGLE_CUT_CELLS * Fraction(1, 2)

# Source : dérivée de SECTOR_ANGLE_CUT_CELLS ; le second pan atteint deux coupes sur le flanc.
SECTOR_CORNER_REACH_CELLS = SECTOR_ANGLE_CUT_CELLS * 2

# Source : lue sur le plan : « une dizaine ».
ROOM_COUNT = 10

# Source : jugée à l'œil : une grande pièce.
ROOM_LARGE_COUNT = 1

# Source : jugée à l'œil : six pièces moyennes.
ROOM_MEDIUM_COUNT = 6

# Source : dérivée des trois groupes : trois petites pièces.
ROOM_SMALL_COUNT = ROOM_COUNT - ROOM_LARGE_COUNT - ROOM_MEDIUM_COUNT

# Source : jugée à l'œil ; grande pièce, plage 24–28.
ROOM_LARGE_SIZE_MIN_CELLS = 24

# Source : jugée à l'œil ; grande pièce, plage 24–28.
ROOM_LARGE_SIZE_MAX_CELLS = 28

# Source : jugée à l'œil ; pièces moyennes, plage 14–18.
ROOM_MEDIUM_SIZE_MIN_CELLS = 14

# Source : jugée à l'œil ; pièces moyennes, plage 14–18.
ROOM_MEDIUM_SIZE_MAX_CELLS = 18

# Source : jugée à l'œil ; petites pièces, plage 8–12.
ROOM_SMALL_SIZE_MIN_CELLS = 8

# Source : jugée à l'œil ; petites pièces, plage 8–12.
ROOM_SMALL_SIZE_MAX_CELLS = 12

# Source : dérivée de la symétrie des pièces : pas pair.
ROOM_SIZE_STEP_CELLS = 2

# Source : lue sur le plan : coupe large, soit 1/4 du petit côté.
ROOM_CORNER_CUT_FRACTION = Fraction(1, 4)

# Source : lue sur le plan : même bande de quatre cases autour de chaque pièce.
ROOM_SPACING_CELLS = 4

# Source : jugée à l'œil sur le couloir du plan.
CORRIDOR_WIDTH_CELLS = 6

# Source : jugée à l'œil ; choix valide entre 1 et 8.
PACKING_CHOICE_POOL = 5

# Source : jugée par essais ; retours valides entre 64 et 1024.
PACKING_BACKTRACK_LIMIT = 1024

# Source : dérivée de la grille ; pas valide entre 1 et 2.
PACKING_SCAN_STEP_CELLS = 1

# Source : lue sur le plan : passage étroit.
DOOR_NECK_WIDTH_CELLS = 2

# Source : dérivée de ROOM_SPACING_CELLS.
DOOR_NECK_DEPTH_CELLS = ROOM_SPACING_CELLS

# Source : dérivée de DOOR_NECK_DEPTH_CELLS : moitié du col.
DOOR_LEAF_FROM_ROOM_CELLS = DOOR_NECK_DEPTH_CELLS * Fraction(1, 2)

# Source : dérivée de DOOR_NECK_WIDTH_CELLS.
DOOR_OPEN_WIDTH_CELLS = DOOR_NECK_WIDTH_CELLS


# =============================================================================
# GRAMMAIRE VISUELLE GELÉE — distances reprises du renderer, toujours en cases
# =============================================================================

# Source : dérivée du look gelé ; valeur HullGrammar.OuterLine du renderer actuel.
HULL_EDGE_LINE_WIDTH_CELLS = ONE_CELL * Fraction(3, 100)

# Source : dérivée du look gelé ; valeur HullGrammar.MidLine du renderer actuel.
HULL_NEAR_RAIL_WIDTH_CELLS = ONE_CELL * Fraction(17, 200)

# Source : dérivée du look gelé ; valeur HullGrammar.InnerLine du renderer actuel.
HULL_FAR_RAIL_WIDTH_CELLS = ONE_CELL * Fraction(3, 100)

# Source : dérivée du look gelé ; valeur HullGrammar.Gap du renderer actuel.
HULL_RAIL_CENTER_GAP_CELLS = ONE_CELL * Fraction(3, 10)

# Source : dérivée du look gelé ; valeur HullGrammar.Depth du renderer actuel.
HULL_RAIL_PAIR_DEPTH_CELLS = ONE_CELL * Fraction(1, 2)

# Source : dérivée des quatre constantes précédentes ; noir laissé entre le trait de bord et le premier rail.
HULL_BLACK_CHANNEL_WIDTH_CELLS = (
    HULL_RAIL_PAIR_DEPTH_CELLS
    - HULL_RAIL_CENTER_GAP_CELLS * Fraction(1, 2)
    - HULL_NEAR_RAIL_WIDTH_CELLS * Fraction(1, 2)
    - HULL_EDGE_LINE_WIDTH_CELLS
)

# Source : dérivée des épaisseurs et de HULL_RAIL_CENTER_GAP_CELLS ; vide net entre les deux rails.
HULL_RAIL_CLEAR_GAP_CELLS = (
    HULL_RAIL_CENTER_GAP_CELLS
    - HULL_NEAR_RAIL_WIDTH_CELLS * Fraction(1, 2)
    - HULL_FAR_RAIL_WIDTH_CELLS * Fraction(1, 2)
)

# Source : dérivée du rail le plus intérieur ; profondeur totale des trois traits de coque.
HULL_TOTAL_WALL_THICKNESS_CELLS = (
    HULL_RAIL_PAIR_DEPTH_CELLS
    + HULL_RAIL_CENTER_GAP_CELLS * Fraction(1, 2)
    + HULL_FAR_RAIL_WIDTH_CELLS * Fraction(1, 2)
)

# Source : dérivée de HULL_TOTAL_WALL_THICKNESS_CELLS ; marge MassSkin au-delà du dernier rail.
HULL_HATCH_SETBACK_CELLS = HULL_TOTAL_WALL_THICKNESS_CELLS + ONE_CELL * Fraction(1, 20)

# Source : dérivée du look gelé ; valeur WallGrammar.Rail du renderer actuel.
ROOM_WALL_RAIL_WIDTH_CELLS = ONE_CELL * Fraction(11, 200)

# Source : dérivée du look gelé ; valeur WallGrammar.Gap du renderer actuel.
ROOM_WALL_RAIL_CENTER_GAP_CELLS = ONE_CELL * Fraction(17, 100)

# Source : dérivée du look gelé ; valeur WallGrammar.Depth du renderer actuel.
ROOM_WALL_RAIL_PAIR_DEPTH_CELLS = ONE_CELL * Fraction(1, 2)

# Source : dérivée des rails intérieurs ; profondeur totale d'un mur de pièce.
ROOM_WALL_TOTAL_THICKNESS_CELLS = (
    ROOM_WALL_RAIL_PAIR_DEPTH_CELLS
    + ROOM_WALL_RAIL_CENTER_GAP_CELLS * Fraction(1, 2)
    + ROOM_WALL_RAIL_WIDTH_CELLS * Fraction(1, 2)
)

# Source : dérivée de ROOM_WALL_TOTAL_THICKNESS_CELLS ; marge MassSkin au-delà du dernier rail.
ROOM_HATCH_SETBACK_CELLS = ROOM_WALL_TOTAL_THICKNESS_CELLS + ONE_CELL * Fraction(1, 20)

# Source : dérivée du look gelé ; valeur WallGrammar.PlateSide du renderer actuel.
JUNCTION_PLATE_SIDE_CELLS = ONE_CELL * Fraction(17, 50)

# Source : dérivée du look gelé ; valeur WallGrammar.PlateBorder du renderer actuel.
JUNCTION_PLATE_BORDER_CELLS = ONE_CELL * Fraction(3, 100)

# Source : dérivée du look gelé ; demi-côté WallGrammar.PlateCore du renderer actuel.
JUNCTION_PLATE_CORE_HALF_SIDE_CELLS = ONE_CELL * Fraction(9, 200)

# Source : dérivée du look gelé ; valeur TrimGrammar.FieldInset du renderer actuel.
TRIM_FIELD_INSET_CELLS = ONE_CELL * Fraction(4, 25)

# Source : dérivée du look gelé ; valeur TrimGrammar.SeparationInset du renderer actuel.
TRIM_SEPARATION_INSET_CELLS = ONE_CELL * Fraction(17, 200)

# Source : dérivée du look gelé ; épaisseur de séparation de TrimSkin.
TRIM_SEPARATION_WIDTH_CELLS = ONE_CELL * Fraction(7, 500)

# Source : dérivée du look gelé ; bord extérieur de la bande de hachures de TrimGrammar.
TRIM_BAND_OUTER_CELLS = -ONE_CELL * Fraction(53, 200)

# Source : dérivée du look gelé ; bord intérieur de la bande de hachures de TrimGrammar.
TRIM_BAND_INNER_CELLS = -ONE_CELL * Fraction(1, 40)

# Source : dérivée de TRIM_BAND_OUTER_CELLS et TRIM_BAND_INNER_CELLS.
TRIM_BAND_MIDLINE_CELLS = (TRIM_BAND_OUTER_CELLS + TRIM_BAND_INNER_CELLS) * Fraction(1, 2)

# Source : dérivée du look gelé ; valeur TrimGrammar.TickSpacing du renderer actuel.
TRIM_TICK_SPACING_CELLS = ONE_CELL * Fraction(7, 25)

# Source : dérivée de TRIM_TICK_SPACING_CELLS comme dans TrimGrammar.EndMargin.
TRIM_TICK_END_MARGIN_CELLS = TRIM_TICK_SPACING_CELLS * Fraction(2, 5)

# Source : dérivée de la largeur de la bande de liseré ; un trait la traverse sans en sortir.
TRIM_TICK_REACH_CELLS = (TRIM_BAND_INNER_CELLS - TRIM_BAND_OUTER_CELLS) * Fraction(1, 2)

# Source : dérivée du look gelé ; épaisseur des hachures de TrimSkin.
TRIM_TICK_WIDTH_CELLS = ONE_CELL * Fraction(11, 500)

# Source : dérivée du look gelé ; demi-côté des petits nœuds de liseré de TrimSkin.
TRIM_NODE_HALF_SIDE_CELLS = ONE_CELL * Fraction(3, 100)

# Source : dérivée du look gelé ; inclinaison de TrimSkin, sans influence sur les distances.
TRIM_TICK_LEAN_DEGREES = 62

# Source : dérivée du look gelé ; seuil de reconnaissance d'un pan droit dans TrimSkin.
TRIM_STRAIGHT_THRESHOLD = Fraction(3, 100)

# Source : dérivée du look gelé ; espacement MassSkin.HatchSpacing du renderer actuel.
MASS_HATCH_SPACING_CELLS = ONE_CELL * Fraction(11, 20)

# Source : dérivée du look gelé ; épaisseur MassSkin.HatchWidth du renderer actuel.
MASS_HATCH_LINE_WIDTH_CELLS = ONE_CELL * Fraction(13, 500)

# Source : dérivée de MASS_HATCH_SPACING_CELLS ; même léger décalage que MassSkin.Nudge.
MASS_HATCH_NUDGE_CELLS = MASS_HATCH_SPACING_CELLS * Fraction(1, 100)

# Source : dérivée du look gelé ; épaisseur du tireté entre les rails de DashedRail.
RAIL_DASH_WIDTH_CELLS = ONE_CELL * Fraction(1, 50)

# Source : dérivée du look gelé ; retrait aux extrémités d'un pan dans DashedRail.
RAIL_DASH_END_MARGIN_CELLS = ONE_CELL * Fraction(8, 25)

# Source : dérivée du look gelé ; minimum DashPattern.Long du renderer actuel.
RAIL_DASH_MIN_CELLS = ONE_CELL * Fraction(11, 50)

# Source : dérivée du look gelé ; maximum DashPattern.Long du renderer actuel.
RAIL_DASH_MAX_CELLS = ONE_CELL * Fraction(41, 50)

# Source : dérivée du look gelé ; minimum d'espace DashPattern.Long du renderer actuel.
RAIL_DASH_GAP_MIN_CELLS = ONE_CELL * Fraction(7, 25)

# Source : dérivée du look gelé ; maximum d'espace DashPattern.Long du renderer actuel.
RAIL_DASH_GAP_MAX_CELLS = ONE_CELL * Fraction(103, 100)

# Source : dérivée du look gelé ; DoorSkin.FrameWidth du renderer actuel.
DOOR_FRAME_LINE_WIDTH_CELLS = ONE_CELL * Fraction(7, 250)

# Source : dérivée de ROOM_WALL_RAIL_WIDTH_CELLS comme DoorSkin.JambWidth.
DOOR_JAMB_WIDTH_CELLS = ROOM_WALL_RAIL_WIDTH_CELLS * Fraction(7, 5)

# Source : dérivée de ROOM_WALL_RAIL_CENTER_GAP_CELLS ; le jambage traverse les deux rails latéraux.
DOOR_JAMB_REACH_CELLS = (
    ROOM_WALL_RAIL_CENTER_GAP_CELLS * Fraction(1, 2) + ROOM_WALL_RAIL_WIDTH_CELLS
)

# Source : dérivée du look gelé ; le vantail garde l'épaisseur d'un rail de mur.
DOOR_LEAF_WIDTH_CELLS = ROOM_WALL_RAIL_WIDTH_CELLS

# Source : dérivée du look gelé ; longueur DoorSkin.LeafDash du renderer actuel.
DOOR_LEAF_DASH_CELLS = ONE_CELL * Fraction(17, 200)

# Source : dérivée du look gelé ; vide DoorSkin.LeafGap du renderer actuel.
DOOR_LEAF_DASH_GAP_CELLS = ONE_CELL * Fraction(7, 100)

# Source : dérivée du look gelé ; retrait DoorSkin.LeafInset à chaque jambage.
DOOR_LEAF_INSET_CELLS = ONE_CELL * Fraction(1, 20)

# Source : dérivée de ROOM_WALL_RAIL_CENTER_GAP_CELLS ; réserve noire autour du cadre.
DOOR_RECESS_HALF_DEPTH_CELLS = ROOM_WALL_RAIL_CENTER_GAP_CELLS * Fraction(5, 4)


# =============================================================================
# DÉTAIL DES SIX SOLS — mesures gelées du renderer, en cases
# =============================================================================

# Source : dérivée du look gelé ; FloorSkin.GridWidth du renderer actuel.
FLOOR_GRID_LINE_WIDTH_CELLS = ONE_CELL * Fraction(3, 250)

# Source : dérivée du look gelé ; FloorSkin.CourseWidth du renderer actuel.
STONE_COURSE_WIDTH_CELLS = ONE_CELL * Fraction(3, 200)

# Source : dérivée du look gelé ; FloorSkin.TornEdgeWidth du renderer actuel.
BROKEN_EDGE_WIDTH_CELLS = ONE_CELL * Fraction(11, 1000)

# Source : dérivée du look gelé ; FloorSkin.CrackWidth du renderer actuel.
DIRT_CRACK_WIDTH_CELLS = ONE_CELL * Fraction(7, 500)

# Source : dérivée du look gelé ; FloorSkin.BladeWidth du renderer actuel.
GRASS_BLADE_WIDTH_CELLS = ONE_CELL * Fraction(2, 125)

# Source : dérivée du look gelé ; FloorSkin.RivetRadius du renderer actuel.
METAL_RIVET_RADIUS_CELLS = ONE_CELL * Fraction(3, 125)

# Source : dérivée du look gelé ; premier alignement de rivets à 0,22 case.
METAL_RIVET_INSET_CELLS = ONE_CELL * Fraction(11, 50)

# Source : dérivée de ONE_CELL et METAL_RIVET_INSET_CELLS ; second alignement symétrique.
METAL_RIVET_FAR_INSET_CELLS = ONE_CELL - METAL_RIVET_INSET_CELLS

# Source : dérivée du look gelé ; nombre de grains de sable par case dans FloorSkin.
SAND_GRAINS_PER_CELL = 14

# Source : dérivée du look gelé ; nombre de grains de terre par case dans FloorSkin.
DIRT_GRAINS_PER_CELL = 11

# Source : dérivée du look gelé ; nombre de grains d'herbe par case dans FloorSkin.
GRASS_GRAINS_PER_CELL = 5

# Source : dérivée du look gelé ; FloorSkin.GrainRadius du renderer actuel.
GRAIN_RADIUS_CELLS = ONE_CELL * Fraction(3, 100)

# Source : dérivée du look gelé ; FloorSkin.GrainRadiusSpan du renderer actuel.
GRAIN_RADIUS_SPAN_CELLS = ONE_CELL * Fraction(13, 500)

# Source : dérivée du look gelé ; FloorSkin.ClodRadius du renderer actuel.
DIRT_CLOD_RADIUS_CELLS = ONE_CELL * Fraction(9, 125)

# Source : dérivée du look gelé ; rayon de grain spécifique à l'herbe.
GRASS_GRAIN_RADIUS_CELLS = ONE_CELL * Fraction(2, 125)

# Source : dérivée du look gelé ; variation du rayon de grain spécifique à l'herbe.
GRASS_GRAIN_RADIUS_SPAN_CELLS = ONE_CELL * Fraction(7, 500)

# Source : dérivée du look gelé ; nombre de sommets d'une déchirure de métal.
BROKEN_HOLE_SEGMENTS = 8

# Source : dérivée du look gelé ; FloorSkin.HoleRadius du renderer actuel.
BROKEN_HOLE_RADIUS_CELLS = ONE_CELL * Fraction(6, 25)

# Source : dérivée du look gelé ; FloorSkin.HoleRadiusSpan du renderer actuel.
BROKEN_HOLE_RADIUS_SPAN_CELLS = ONE_CELL * Fraction(1, 5)

# Source : dérivée du look gelé ; une plaque sur cinq est déchirée.
BROKEN_HOLE_EVERY_CELLS = 5

# Source : dérivée du look gelé ; une case de terre sur vingt-trois porte une fissure.
DIRT_CRACK_EVERY_CELLS = 23

# Source : dérivée du look gelé ; une motte revient tous les quatre grains de terre.
DIRT_CLOD_EVERY_GRAINS = 4

# Source : dérivée du look gelé ; départ horizontal de la fissure de terre dans FloorSkin.
DIRT_CRACK_START_X_CELLS = ONE_CELL * Fraction(1, 5)

# Source : dérivée du look gelé ; départ vertical de la fissure de terre dans FloorSkin.
DIRT_CRACK_START_Y_CELLS = ONE_CELL * Fraction(2, 5)

# Source : dérivée du look gelé ; arrivée horizontale de la fissure de terre dans FloorSkin.
DIRT_CRACK_END_X_CELLS = ONE_CELL * Fraction(3, 4)

# Source : dérivée du look gelé ; arrivée verticale de la fissure de terre dans FloorSkin.
DIRT_CRACK_END_Y_CELLS = ONE_CELL * Fraction(31, 50)

# Source : dérivée du look gelé ; luminosité minimale d'un grain dans FloorSkin.
GRAIN_BRIGHTNESS_MIN = Fraction(11, 20)

# Source : dérivée de GRAIN_BRIGHTNESS_MIN ; variation restante jusqu'à la pleine luminosité.
GRAIN_BRIGHTNESS_SPAN = 1 - GRAIN_BRIGHTNESS_MIN

# Source : dérivée du look gelé ; échelle minimale d'une motte dans FloorSkin.
DIRT_CLOD_SCALE_MIN = Fraction(7, 10)

# Source : dérivée du look gelé ; variation d'échelle d'une motte dans FloorSkin.
DIRT_CLOD_SCALE_SPAN = Fraction(3, 5)

# Source : dérivée du look gelé ; maximum de brins tentés par case dans FloorSkin.
GRASS_MAX_BLADES_PER_CELL = 7

# Source : dérivée du look gelé ; probabilité statique de présence d'un brin.
GRASS_BLADE_CHANCE = Fraction(18, 25)

# Source : dérivée du look gelé ; longueur minimale d'un brin dans FloorSkin.
GRASS_BLADE_LENGTH_CELLS = ONE_CELL * Fraction(17, 100)

# Source : dérivée du look gelé ; variation de longueur d'un brin dans FloorSkin.
GRASS_BLADE_LENGTH_SPAN_CELLS = ONE_CELL * Fraction(21, 100)

# Source : dérivée du look gelé ; angle minimal statique d'un brin, en radians.
GRASS_BLADE_ANGLE_MIN_RADIANS = Fraction(-19, 10)

# Source : dérivée du look gelé ; amplitude angulaire statique d'un brin, en radians.
GRASS_BLADE_ANGLE_SPAN_RADIANS = Fraction(13, 10)

# Source : dérivée du look gelé ; la racine d'un brin reste dans cette marge horizontale.
GRASS_ROOT_X_INSET_CELLS = ONE_CELL * Fraction(3, 20)

# Source : dérivée du look gelé ; largeur disponible à la racine d'un brin.
GRASS_ROOT_X_SPAN_CELLS = ONE_CELL * Fraction(7, 10)

# Source : dérivée du look gelé ; hauteur minimale de la racine d'un brin.
GRASS_ROOT_Y_INSET_CELLS = ONE_CELL * Fraction(3, 10)

# Source : dérivée du look gelé ; hauteur disponible à la racine d'un brin.
GRASS_ROOT_Y_SPAN_CELLS = ONE_CELL * Fraction(11, 20)


# =============================================================================
# RENDU — échelle de sortie (pixels) et couleurs, sans influence sur la forme
# =============================================================================

# Source : jugée à l'œil ; 14 px rendent le quadrillage lisible sans produire un PNG démesuré.
CELL_PIXELS = 14

# Source : jugée à l'œil ; trois passes internes suffisent aux traits subpixel du look gelé.
SUPERSAMPLE = 3

# Source : jugée à l'œil ; quatre cases laissent respirer la feuille autour de la coque.
CANVAS_MARGIN_CELLS = 4

# Source : dérivée du besoin de vérification demandé ; active la grille d'une case par défaut.
SHOW_CELL_GRID_DEFAULT = True

# Source : dérivée du quadrillage actuel PaperGrammar ; une règle forte toutes les huit cases.
PAPER_MAJOR_EVERY_CELLS = 8

# Source : dérivée du look gelé ; PaperGrammar.MinorWeightPixels, en pixels finaux.
PAPER_MINOR_WIDTH_PIXELS = Fraction(3, 4)

# Source : dérivée du look gelé ; PaperGrammar.MajorWeightPixels, en pixels finaux.
PAPER_MAJOR_WIDTH_PIXELS = Fraction(7, 5)

# Source : jugée à l'œil ; un pixel final garde la surcouche de contrôle discrète et nette.
VERIFY_GRID_WIDTH_PIXELS = 1

# Source : jugée à l'œil ; graine lisible et stable pour l'exécution sans argument.
DEFAULT_SEED = 7

# Source : dérivée du format PNG ; niveau maximal, déterministe et sans perte.
PNG_COMPRESSION_LEVEL = 9

# Source : dérivée de ScenePalette.Backdrop du renderer actuel.
COLOR_BACKDROP = (1, 33, 62)

# Source : dérivée de ScenePalette.PaperMinor du renderer actuel.
COLOR_PAPER_MINOR = (12, 47, 79)

# Source : dérivée de ScenePalette.PaperMajor du renderer actuel.
COLOR_PAPER_MAJOR = (21, 60, 95)

# Source : dérivée de ScenePalette.Silhouette du renderer actuel.
COLOR_SHIP_BODY = (0, 0, 0)

# Source : dérivée de ScenePalette.Hull du renderer actuel.
COLOR_HULL = (170, 180, 194)

# Source : dérivée de ScenePalette.Node du renderer actuel.
COLOR_NODE = (218, 228, 240)

# Source : dérivée de ScenePalette.Dash du renderer actuel.
COLOR_DASH = (120, 129, 143)

# Source : dérivée de ScenePalette.Hatch du renderer actuel.
COLOR_MASS_HATCH = (68, 78, 92)

# Source : dérivée de ScenePalette.TrimLine du renderer actuel.
COLOR_TRIM_LINE = (96, 106, 120)

# Source : dérivée de ScenePalette.TrimNode du renderer actuel.
COLOR_TRIM_NODE = (150, 160, 176)

# Source : dérivée de ScenePalette.TrimTick du renderer actuel.
COLOR_TRIM_TICK = (120, 129, 143)

# Source : dérivée de DoorSkin.LeafA du renderer actuel.
COLOR_DOOR_A = (56, 189, 248)

# Source : dérivée de DoorSkin.LeafB du renderer actuel.
COLOR_DOOR_B = (52, 211, 153)

# Source : jugée à l'œil à partir de la grille blueprint ; alpha bas pour une surcouche discrète.
COLOR_VERIFY_GRID = (96, 190, 255, 34)

# Source : dérivée de FloorPalette.WashFor du renderer actuel, sans changement des six matières.
FLOOR_WASH_COLORS = {
    "metal": (12, 16, 22),
    "stone": (17, 18, 21),
    "dirt": (48, 38, 23),
    "sand": (62, 55, 34),
    "grass": (20, 36, 23),
    "broken_metal": (12, 16, 22),
}

# Source : dérivée de FloorPalette.Sand du renderer actuel.
SAND_PALETTE = (
    (224, 204, 142),
    (196, 174, 116),
    (168, 146, 98),
    (234, 218, 168),
    (148, 124, 82),
    (208, 186, 126),
    (182, 158, 104),
)

# Source : dérivée de FloorPalette.Grass du renderer actuel.
GRASS_PALETTE = (
    (120, 164, 96),
    (92, 138, 78),
    (146, 178, 100),
    (74, 116, 68),
    (108, 152, 86),
    (132, 168, 92),
    (86, 130, 80),
)

# Source : dérivée de FloorPalette.Dirt du renderer actuel.
DIRT_PALETTE = (
    (158, 124, 82),
    (132, 102, 66),
    (176, 142, 92),
    (112, 86, 56),
    (146, 114, 74),
    (120, 96, 62),
    (166, 130, 84),
)

# Source : dérivée des six matières gelées énumérées dans TheEnd-Art/archive/ascii-render/README.md.
FLOOR_MATERIALS = ("metal", "stone", "dirt", "sand", "grass", "broken_metal")

# Source : dérivée de FloorPalette.MetalGrid du renderer actuel.
COLOR_METAL_GRID = (48, 56, 66)

# Source : dérivée de FloorPalette.Rivet du renderer actuel.
COLOR_METAL_RIVET = (116, 128, 144)

# Source : dérivée de FloorPalette.StoneCourse du renderer actuel.
COLOR_STONE_COURSE = (62, 66, 74)

# Source : dérivée de FloorPalette.DirtCrack du renderer actuel.
COLOR_DIRT_CRACK = (120, 94, 60)

# Source : dérivée de FloorPalette.HoleFill du renderer actuel.
COLOR_BROKEN_HOLE = (7, 8, 10)

# Source : dérivée de FloorPalette.TornMetal du renderer actuel.
COLOR_BROKEN_EDGE = (72, 82, 94)

# Source : dérivée du vert construit par FloorSkin pour les brins d'herbe.
COLOR_GRASS_BLADE_RED_BLUE = (86, 80)

# Source : dérivée du vert minimal construit par FloorSkin pour les brins d'herbe.
COLOR_GRASS_BLADE_GREEN_MIN = 150

# Source : dérivée de FloorSkin ; variation du canal vert d'un brin d'herbe.
COLOR_GRASS_BLADE_GREEN_SPAN = 40


Point = tuple[float, float]


@dataclass(frozen=True)
class RoomSpec:
    """Une pièce et son col ; toutes les coordonnées restent en cases."""
    index: int
    hull_side: str
    x: int
    y: int
    width: int
    depth: int
    material: str

    @property
    def right(self): return self.x + self.width

    @property
    def bottom(self): return self.y + self.depth

    @property
    def door_direction(self): return {
        "north": (0, 1), "south": (0, -1), "west": (1, 0), "east": (-1, 0)
    }[self.hull_side]

    @property
    def door_port(self):
        cx, cy = (self.x + self.right) // 2, (self.y + self.bottom) // 2
        return {"north": (cx, self.bottom), "south": (cx, self.y),
                "west": (self.right, cy), "east": (self.x, cy)}[self.hull_side]

    @property
    def corner_cut(self):
        fraction = ROOM_CORNER_CUT_FRACTION
        return min(self.width, self.depth) * fraction.numerator // fraction.denominator


@dataclass(frozen=True)
class Layout:
    sector: tuple[Point, ...]
    corridor: tuple[Point, ...]
    floor: tuple[Point, ...]
    rooms: tuple[RoomSpec, ...]


class Canvas:
    """Dessin supersamplé dont l'API reçoit uniquement des coordonnées en cases."""

    def __init__(self) -> None:
        self.world_width = SECTOR_WIDTH_CELLS + 2 * CANVAS_MARGIN_CELLS
        self.world_height = SECTOR_HEIGHT_CELLS + 2 * CANVAS_MARGIN_CELLS
        self.scale = CELL_PIXELS * SUPERSAMPLE
        self.size = (self.world_width * self.scale, self.world_height * self.scale)
        self.image = Image.new("RGBA", self.size, COLOR_BACKDROP + (255,))
        self.draw = ImageDraw.Draw(self.image)

    def px(self, point: Point) -> tuple[int, int]:
        x = (float(point[0]) + CANVAS_MARGIN_CELLS) * self.scale
        y = (float(point[1]) + CANVAS_MARGIN_CELLS) * self.scale
        return round(x), round(y)

    def length(self, cells: int | float | Fraction) -> int:
        return max(1, round(float(cells) * self.scale))

    def final_pixels(self, pixels: int | float | Fraction) -> int:
        return max(1, round(float(pixels) * SUPERSAMPLE))

    def polygon(self, points: Sequence[Point], fill: tuple[int, ...]) -> None:
        self.draw.polygon([self.px(point) for point in points], fill=fill)

    def line(
        self,
        a: Point,
        b: Point,
        fill: tuple[int, ...],
        width_cells: int | float | Fraction,
    ) -> None:
        self.draw.line(
            [self.px(a), self.px(b)],
            fill=fill,
            width=self.length(width_cells),
        )

    def polyline(
        self,
        points: Sequence[Point],
        fill: tuple[int, ...],
        width_cells: int | float | Fraction,
        *,
        closed: bool = True,
    ) -> None:
        sequence = list(points)
        if closed:
            sequence.append(points[0])
        self.draw.line(
            [self.px(point) for point in sequence],
            fill=fill,
            width=self.length(width_cells),
            joint="curve",
        )

    def rectangle(
        self,
        centre: Point,
        half_width: int | float | Fraction,
        half_height: int | float | Fraction,
        fill: tuple[int, ...],
        *,
        outline: tuple[int, ...] | None = None,
        outline_width: int | float | Fraction = ONE_CELL,
    ) -> None:
        cx, cy = centre
        box = [
            self.px((cx - float(half_width), cy - float(half_height))),
            self.px((cx + float(half_width), cy + float(half_height))),
        ]
        self.draw.rectangle(
            box,
            fill=fill,
            outline=outline,
            width=self.length(outline_width) if outline is not None else 1,
        )

    def dot(
        self,
        centre: Point,
        radius: int | float | Fraction,
        fill: tuple[int, ...],
    ) -> None:
        cx, cy = centre
        r = float(radius)
        self.draw.rectangle(
            [self.px((cx - r, cy - r)), self.px((cx + r, cy + r))],
            fill=fill,
        )

    def mask_for(self, points: Sequence[Point]) -> Image.Image:
        mask = Image.new("L", self.size, 0)
        ImageDraw.Draw(mask).polygon([self.px(point) for point in points], fill=255)
        return mask

    def finish(self) -> Image.Image:
        final_size = (
            self.world_width * CELL_PIXELS,
            self.world_height * CELL_PIXELS,
        )
        return self.image.resize(final_size, Image.Resampling.LANCZOS).convert("RGB")


def as_point(point):
    return float(point[0]), float(point[1])


def sector_polygon():
    """Douze pans : horizontal, deux coupes, flanc, deux coupes, puis symétrie."""
    w, h, cut = SECTOR_WIDTH_CELLS, SECTOR_HEIGHT_CELLS, SECTOR_ANGLE_CUT_CELLS
    shoulder, reach = SECTOR_SHOULDER_RISE_CELLS, SECTOR_CORNER_REACH_CELLS
    points = (
        (reach, 0), (w - reach, 0), (w - cut, shoulder), (w, reach),
        (w, h - reach), (w - cut, h - shoulder), (w - reach, h),
        (reach, h), (cut, h - shoulder), (0, h - reach), (0, reach),
        (cut, shoulder),
    )
    if len(points) != SECTOR_PAN_COUNT:
        raise ValueError("nombre de pans incohérent")
    return tuple(as_point(point) for point in points)


def room_polygon(room):
    x, y, r, b, cut = room.x, room.y, room.right, room.bottom, room.corner_cut
    points = (
        (x + cut, y), (r - cut, y), (r, y + cut), (r, b - cut),
        (r - cut, b), (x + cut, b), (x, b - cut), (x, y + cut),
    )
    return tuple(as_point(point) for point in points)


def neck_polygon(room):
    (px, py), (dx, dy) = room.door_port, room.door_direction
    tx, ty, half = -dy, dx, Fraction(DOOR_NECK_WIDTH_CELLS, 2)
    ex, ey = px + dx * DOOR_NECK_DEPTH_CELLS, py + dy * DOOR_NECK_DEPTH_CELLS
    points = (
        (px - tx * half, py - ty * half), (px + tx * half, py + ty * half),
        (ex + tx * half, ey + ty * half), (ex - tx * half, ey - ty * half),
    )
    return tuple(as_point(point) for point in points)


def polygon_cells(polygon):
    xs, ys = [point[0] for point in polygon], [point[1] for point in polygon]
    return {
        (x, y)
        for y in range(math.floor(min(ys)), math.ceil(max(ys)))
        for x in range(math.floor(min(xs)), math.ceil(max(xs)))
        if point_in_polygon((x + 0.5, y + 0.5), polygon)
    }


def expand(cells, radius):
    return {(x + dx, y + dy) for x, y in cells
            for dy in range(-radius, radius + 1) for dx in range(-radius, radius + 1)}


def corridor_brush(centre):
    x, y = centre
    low = -(CORRIDOR_WIDTH_CELLS // 2)
    return {(x + dx, y + dy) for dy in range(low, low + CORRIDOR_WIDTH_CELLS)
            for dx in range(low, low + CORRIDOR_WIDTH_CELLS)}


def corridor_target(room):
    (x, y), (dx, dy) = room.door_port, room.door_direction
    reach = DOOR_NECK_DEPTH_CELLS + CORRIDOR_WIDTH_CELLS // 2
    return x + dx * reach, y + dy * reach


def grid_search(starts, goals, valid, directions, find_all=False):
    prev = {cell: None for cell in sorted(starts)}
    todo = deque(prev)
    pending = set(goals)
    while todo:
        at = todo.popleft()
        if at in pending:
            pending.remove(at)
            if not find_all or not pending:
                return at, prev
        for dx, dy in directions:
            near = at[0] + dx, at[1] + dy
            if near in valid and near not in prev:
                prev[near] = at
                todo.append(near)
    return None, prev


def size_plan(rng):
    bands = (
        (ROOM_LARGE_COUNT, ROOM_LARGE_SIZE_MIN_CELLS, ROOM_LARGE_SIZE_MAX_CELLS),
        (ROOM_MEDIUM_COUNT, ROOM_MEDIUM_SIZE_MIN_CELLS, ROOM_MEDIUM_SIZE_MAX_CELLS),
        (ROOM_SMALL_COUNT, ROOM_SMALL_SIZE_MIN_CELLS, ROOM_SMALL_SIZE_MAX_CELLS),
    )
    sizes = []
    for count, low, high in bands:
        choices = (high - low) // ROOM_SIZE_STEP_CELLS + 1
        for _ in range(count):
            sizes.append(tuple(low + ROOM_SIZE_STEP_CELLS * rng.randrange(choices)
                               for _ in range(2)))
    return sizes


def anchored_candidates(width, depth, allowed):
    candidates = []
    shape = polygon_cells(room_polygon(RoomSpec(0, "north", 0, 0, width, depth, "metal")))
    xmax, ymax, step = (SECTOR_WIDTH_CELLS - width,
                         SECTOR_HEIGHT_CELLS - depth, PACKING_SCAN_STEP_CELLS)
    xs, ys = range(0, xmax + 1, step), range(0, ymax + 1, step)
    axes = (
        ("north", xs, range(ymax + 1)), ("south", xs, range(ymax, -1, -1)),
        ("west", ys, range(xmax + 1)), ("east", ys, range(xmax, -1, -1)),
    )
    for side, along, outward in axes:
        for position in along:
            for pushed in outward:
                x, y = ((position, pushed) if side in ("north", "south")
                        else (pushed, position))
                cells = {(x + sx, y + sy) for sx, sy in shape}
                if cells and cells <= allowed:
                    candidates.append((side, x, y, cells))
                    break
    return candidates


def blocked_centres(cells):
    low = -(CORRIDOR_WIDTH_CELLS // 2)
    lo = -ROOM_SPACING_CELLS - (low + CORRIDOR_WIDTH_CELLS - 1)
    hi = ROOM_SPACING_CELLS - low
    return {(x + dx, y + dy) for x, y in cells
            for dy in range(lo, hi + 1) for dx in range(lo, hi + 1)}


def corridor_space(blocked, targets, centres):
    valid = centres - blocked
    if not targets or any(target not in valid for target in targets):
        return None
    if len(targets) == 1:
        return valid
    goal, _ = grid_search({targets[0]}, targets[1:], valid,
                          ((1, 0), (0, 1), (-1, 0), (0, -1)), True)
    return valid if goal is not None else None


def box_gap(a, b):
    return math.hypot(max(a.x - b.right, b.x - a.right, 0),
                      max(a.y - b.bottom, b.y - a.bottom, 0))

def pack_rooms(seed, sector_cells):
    if not 1 <= PACKING_CHOICE_POOL <= 8:
        raise ValueError("tassement hors plage")
    allowed = {cell for cell in sector_cells
               if expand({cell}, ROOM_SPACING_CELLS) <= sector_cells}
    centres = {(x, y) for y in range(SECTOR_HEIGHT_CELLS + 1)
               for x in range(SECTOR_WIDTH_CELLS + 1)
               if corridor_brush((x, y)) <= sector_cells}
    rng = random.Random(stable_variant(seed, 991))
    sizes = size_plan(rng)
    skins = list(FLOOR_MATERIALS)
    while len(skins) < ROOM_COUNT:
        skins.append(FLOOR_MATERIALS[rng.randrange(len(FLOOR_MATERIALS))])
    rng.shuffle(skins)

    cache, orders = {}, []
    for index, (width, depth) in enumerate(sizes):
        key = width, depth
        if key not in cache:
            cache[key] = anchored_candidates(width, depth, allowed)
        choices = []
        for side, x, y, cells in cache[key]:
            room = RoomSpec(index, side, x, y, width, depth, skins[index])
            choices.append((room, cells, expand(cells, ROOM_SPACING_CELLS),
                            polygon_cells(neck_polygon(room))))
        rng.shuffle(choices)
        orders.append(choices)

    visited, blocks = 0, {}

    def place(i, rooms, bodies, guards, necks, blocked, ports, space):
        nonlocal visited
        visited += 1
        if visited > PACKING_BACKTRACK_LIMIT: return None
        if i == ROOM_COUNT:
            corridor = route_corridor(space, ports, seed)
            floor = cell_contour(corridor | bodies | set().union(*necks), True)
            if polygon_cells(cell_contour(corridor)) & bodies: return None
            if not bodies <= polygon_cells(floor): return None
            return rooms, space, ports
        counts = {side: sum(room.hull_side == side for room in rooms)
                  for side in ("north", "south", "west", "east")}
        ranked = [
            (counts[room.hull_side],
             min((box_gap(room, other) for other in rooms), default=0),
             room, cells, guard, neck)
            for room, cells, guard, neck in orders[i] if not guard & bodies
        ]
        ranked.sort(key=lambda choice: choice[:2])
        tried = 0
        for _, _, room, cells, guard, neck in ranked:
            if (any(neck & other for other in guards)
                    or any(other & guard for other in necks)):
                continue
            new_ports = (*ports, corridor_target(room))
            if room not in blocks: blocks[room] = blocked_centres(cells)
            new_block = blocked | blocks[room]
            free = corridor_space(new_block, new_ports, centres)
            if free is None: continue
            result = place(i + 1, (*rooms, room), bodies | cells,
                           (*guards, guard), (*necks, neck), new_block,
                           new_ports, free)
            if result is not None: return result
            tried += 1
            if tried == PACKING_CHOICE_POOL: break
        return None

    result = place(0, (), set(), (), (), set(), (), None)
    if result is None: raise RuntimeError("tassement introuvable")
    return result

def route_corridor(valid, targets, seed):
    network, remaining = {targets[0]}, set(targets[1:])
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    random.Random(stable_variant(seed, 1771)).shuffle(directions)
    while remaining:
        goal, previous = grid_search(network, remaining, valid, directions)
        if goal is None:
            raise RuntimeError("cols non reliés")
        remaining.remove(goal)
        while goal is not None:
            network.add(goal)
            goal = previous[goal]
    return set().union(*(corridor_brush(cell) for cell in network))

def _step(loop, index):
    a, b = loop[index % len(loop)], loop[(index + 1) % len(loop)]
    return b[0] - a[0], b[1] - a[1]

def simplify_cell_loop(loop, safe, must):
    n = len(loop)
    start = next((i + 1 for i in range(n) if _step(loop, i - 1) == _step(loop, i)), 0)
    ring = [loop[(start + i) % n] for i in range(n)]

    def stairs(i):
        a, b = _step(ring, i), _step(ring, i + 1)
        if (safe and _step(ring, i - 1) == a) or a == b:
            return 0
        run = 0
        while (run < n and _step(ring, i + run) == (a if run % 2 == 0 else b)
               and _step(ring, i + run) != _step(ring, i + run + 1)):
            run += 1
        return run

    runs, i = [], 0
    while i < n:
        run = stairs(i) & ~1
        if run >= 4 and i + run < n:
            runs.append((i, run)); i += run
        else:
            i += 1

    def fold(skips):
        path, i = [], 0
        while i < n:
            path.append(ring[i]); i += skips.get(i, 1)

        def bend(points, at):
            a, b, c = points[at - 1], points[at], points[(at + 1) % len(points)]
            return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])

        kept = [point for i, point in enumerate(path) if bend(path, i)]
        if safe:
            kept = [point for i, point in enumerate(kept)
                    if bend(kept, i) > 0 or math.dist(point, kept[i - 1]) > 1
                    or math.dist(point, kept[(i + 1) % len(kept)]) > 1]
        return tuple(kept if len(kept) >= 3 else path)

    if not safe:
        return fold(dict(runs))
    ok = {}
    for i, run in runs:
        trial = {**ok, i: run}
        if must <= polygon_cells(fold(trial)):
            ok = trial
    return fold(ok)

def cell_contour(cells, protect=False):
    steps = ((1, 0), (0, 1), (-1, 0), (0, -1))
    edges, exits = [], {}

    def add(point, way):
        exits.setdefault(point, []).append(len(edges)); edges.append((point, way))

    for x, y in sorted(cells, key=lambda cell: (cell[1], cell[0])):
        if (x, y - 1) not in cells: add((x, y), 0)
        if (x + 1, y) not in cells: add((x + 1, y), 1)
        if (x, y + 1) not in cells: add((x + 1, y + 1), 2)
        if (x - 1, y) not in cells: add((x, y + 1), 3)

    used, loops = set(), []
    for seed in range(len(edges)):
        if seed in used:
            continue
        loop, edge = [], seed
        while edge not in used:
            used.add(edge)
            point, way = edges[edge]
            loop.append(as_point(point))
            dx, dy = steps[way]
            choices = [choice for choice in exits.get((point[0] + dx, point[1] + dy), ())
                       if choice not in used]
            if not choices:
                break
            edge = min(choices, key=lambda choice: (edges[choice][1] - way + 3) & 3)
        if len(loop) >= 3:
            loops.append(tuple(loop))
    if not loops:
        raise RuntimeError("contour absent")
    return simplify_cell_loop(max(loops, key=polygon_area), protect, cells)


def build_layout(seed):
    sector = sector_polygon()
    sector_cells = polygon_cells(sector)
    rooms, valid, targets = pack_rooms(seed, sector_cells)
    corridor_cells = route_corridor(valid, targets, seed)
    floor_cells = corridor_cells | set().union(*(
        polygon_cells(room_polygon(room)) | polygon_cells(neck_polygon(room))
        for room in rooms
    ))
    return Layout(sector, cell_contour(corridor_cells),
                  cell_contour(floor_cells, True), rooms)


def polygon_area(points: Sequence[Point]) -> float:
    area = 0.0
    for a, b in zip(points, points[1:] + points[:1]):
        area += a[0] * b[1] - b[0] * a[1]
    return area / 2.0


def line_intersection(
    p1: Point,
    direction1: Point,
    p2: Point,
    direction2: Point,
) -> Point:
    denominator = direction1[0] * direction2[1] - direction1[1] * direction2[0]
    if abs(denominator) < 1e-12:
        return p2
    distance = (
        (p2[0] - p1[0]) * direction2[1] - (p2[1] - p1[1]) * direction2[0]
    ) / denominator
    return (
        p1[0] + direction1[0] * distance,
        p1[1] + direction1[1] * distance,
    )


def offset_polygon(points: Sequence[Point], distance: int | float | Fraction) -> tuple[Point, ...]:
    """Décale un polygone simple ; distance positive = vers son intérieur."""

    signed_area = polygon_area(points)
    inward_sign = 1.0 if signed_area > 0 else -1.0
    shifted_lines: list[tuple[Point, Point]] = []
    amount = float(distance)

    for a, b in zip(points, points[1:] + points[:1]):
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        length = math.hypot(dx, dy)
        if length == 0:
            raise ValueError("un contour contient deux sommets identiques")
        ux, uy = dx / length, dy / length
        nx, ny = inward_sign * -uy, inward_sign * ux
        shifted_lines.append(((a[0] + nx * amount, a[1] + ny * amount), (ux, uy)))

    result: list[Point] = []
    for index in range(len(points)):
        previous_point, previous_direction = shifted_lines[index - 1]
        current_point, current_direction = shifted_lines[index]
        result.append(
            line_intersection(
                previous_point,
                previous_direction,
                current_point,
                current_direction,
            )
        )
    return tuple(result)


def point_in_polygon(point: Point, polygon: Sequence[Point]) -> bool:
    x, y = point
    inside = False
    previous = polygon[-1]
    for current in polygon:
        if (current[1] > y) != (previous[1] > y):
            crossing = (
                (previous[0] - current[0])
                * (y - current[1])
                / (previous[1] - current[1])
                + current[0]
            )
            if x < crossing:
                inside = not inside
        previous = current
    return inside


def stable_unit(seed: int, *channels: int) -> float:
    """Valeur [0, 1) stable, indépendante du hash aléatoire de Python."""

    payload = ":".join(str(value) for value in (seed, *channels)).encode("ascii")
    value = int.from_bytes(hashlib.blake2b(payload, digest_size=8).digest(), "big")
    return value / float(1 << 64)


def stable_variant(seed: int, *channels: int) -> int:
    payload = ":".join(str(value) for value in (seed, *channels)).encode("ascii")
    return int.from_bytes(hashlib.blake2b(payload, digest_size=8).digest(), "big")


def dim_color(color: tuple[int, int, int], brightness: float) -> tuple[int, int, int]:
    return tuple(round(channel * brightness) for channel in color)


def draw_paper(canvas: Canvas) -> None:
    x_min = -CANVAS_MARGIN_CELLS
    x_max = SECTOR_WIDTH_CELLS + CANVAS_MARGIN_CELLS
    y_min = -CANVAS_MARGIN_CELLS
    y_max = SECTOR_HEIGHT_CELLS + CANVAS_MARGIN_CELLS

    for x in range(x_min, x_max + 1):
        major = x % PAPER_MAJOR_EVERY_CELLS == 0
        canvas.draw.line(
            [canvas.px((x, y_min)), canvas.px((x, y_max))],
            fill=COLOR_PAPER_MAJOR if major else COLOR_PAPER_MINOR,
            width=canvas.final_pixels(
                PAPER_MAJOR_WIDTH_PIXELS if major else PAPER_MINOR_WIDTH_PIXELS
            ),
        )
    for y in range(y_min, y_max + 1):
        major = y % PAPER_MAJOR_EVERY_CELLS == 0
        canvas.draw.line(
            [canvas.px((x_min, y)), canvas.px((x_max, y))],
            fill=COLOR_PAPER_MAJOR if major else COLOR_PAPER_MINOR,
            width=canvas.final_pixels(
                PAPER_MAJOR_WIDTH_PIXELS if major else PAPER_MINOR_WIDTH_PIXELS
            ),
        )


def draw_mass_hatching(
    canvas: Canvas,
    silhouette_mask: Image.Image,
    floor_mask: Image.Image,
) -> None:
    mass_mask = ImageChops.subtract(silhouette_mask, floor_mask)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    spacing = canvas.length(MASS_HATCH_SPACING_CELLS)
    nudge = canvas.length(MASS_HATCH_NUDGE_CELLS)
    width = canvas.length(MASS_HATCH_LINE_WIDTH_CELLS)
    image_width, image_height = canvas.size

    for start_x in range(-image_height + nudge, image_width + nudge, spacing):
        draw.line(
            [(start_x, image_height), (start_x + image_height, 0)],
            fill=COLOR_MASS_HATCH + (255,),
            width=width,
        )

    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), mass_mask))
    canvas.image.alpha_composite(layer)


def cells_touched_by(polygon: Sequence[Point]) -> Iterable[tuple[int, int]]:
    min_x = math.floor(min(point[0] for point in polygon))
    max_x = math.ceil(max(point[0] for point in polygon))
    min_y = math.floor(min(point[1] for point in polygon))
    max_y = math.ceil(max(point[1] for point in polygon))
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            centre = (x + float(HALF_CELL), y + float(HALF_CELL))
            if point_in_polygon(centre, polygon):
                yield x, y


def draw_metal_cell(canvas: Canvas, x: int, y: int, *, broken: bool, seed: int, salt: int) -> None:
    canvas.line((x, y), (x + 1, y), COLOR_METAL_GRID, FLOOR_GRID_LINE_WIDTH_CELLS)
    canvas.line((x, y), (x, y + 1), COLOR_METAL_GRID, FLOOR_GRID_LINE_WIDTH_CELLS)

    if broken and stable_variant(seed, salt, x, y, 0) % BROKEN_HOLE_EVERY_CELLS == 0:
        centre = (x + float(HALF_CELL), y + float(HALF_CELL))
        ring: list[Point] = []
        for index in range(BROKEN_HOLE_SEGMENTS):
            angle = math.tau * index / BROKEN_HOLE_SEGMENTS
            radius = float(BROKEN_HOLE_RADIUS_CELLS) + float(
                BROKEN_HOLE_RADIUS_SPAN_CELLS
            ) * stable_unit(seed, salt, x, y, 10 + index)
            ring.append(
                (
                    centre[0] + math.cos(angle) * radius,
                    centre[1] + math.sin(angle) * radius,
                )
            )
        canvas.polygon(ring, COLOR_BROKEN_HOLE)
        for a, b in zip(ring, ring[1:] + ring[:1]):
            canvas.line(a, b, COLOR_BROKEN_EDGE, BROKEN_EDGE_WIDTH_CELLS)
        return

    for inset_x in (METAL_RIVET_INSET_CELLS, METAL_RIVET_FAR_INSET_CELLS):
        for inset_y in (METAL_RIVET_INSET_CELLS, METAL_RIVET_FAR_INSET_CELLS):
            canvas.dot(
                (x + float(inset_x), y + float(inset_y)),
                METAL_RIVET_RADIUS_CELLS,
                COLOR_METAL_RIVET,
            )


def draw_stone_cell(canvas: Canvas, x: int, y: int) -> None:
    canvas.line((x, y), (x + 1, y), COLOR_STONE_COURSE, STONE_COURSE_WIDTH_CELLS)
    joint = 0 if y % 2 == 0 else float(HALF_CELL)
    canvas.line(
        (x + joint, y),
        (x + joint, y + 1),
        COLOR_STONE_COURSE,
        STONE_COURSE_WIDTH_CELLS,
    )


def draw_grains(
    canvas: Canvas,
    x: int,
    y: int,
    count: int,
    palette: Sequence[tuple[int, int, int]],
    radius: Fraction,
    radius_span: Fraction,
    seed: int,
    salt: int,
    *,
    clod_every: int | None = None,
) -> None:
    for index in range(count):
        centre = (
            x + stable_unit(seed, salt, x, y, 10 + index),
            y + stable_unit(seed, salt, x, y, 40 + index),
        )
        tone_index = int(stable_unit(seed, salt, x, y, 70 + index) * len(palette))
        tone = palette[min(tone_index, len(palette) - 1)]
        brightness = float(GRAIN_BRIGHTNESS_MIN) + float(
            GRAIN_BRIGHTNESS_SPAN
        ) * stable_unit(seed, salt, x, y, 100 + index)

        if clod_every is not None and index % clod_every == 0:
            dot_radius = float(DIRT_CLOD_RADIUS_CELLS) * (
                float(DIRT_CLOD_SCALE_MIN)
                + float(DIRT_CLOD_SCALE_SPAN) * stable_unit(seed, salt, x, y, 130 + index)
            )
        else:
            dot_radius = float(radius) + float(radius_span) * stable_unit(
                seed, salt, x, y, 160 + index
            )
        canvas.dot(centre, dot_radius, dim_color(tone, brightness))


def draw_dirt_cell(canvas: Canvas, x: int, y: int, seed: int, salt: int) -> None:
    draw_grains(
        canvas,
        x,
        y,
        DIRT_GRAINS_PER_CELL,
        DIRT_PALETTE,
        GRAIN_RADIUS_CELLS,
        GRAIN_RADIUS_SPAN_CELLS,
        seed,
        salt,
        clod_every=DIRT_CLOD_EVERY_GRAINS,
    )
    if stable_variant(seed, salt, x, y, 220) % DIRT_CRACK_EVERY_CELLS == 0:
        canvas.line(
            (x + float(DIRT_CRACK_START_X_CELLS), y + float(DIRT_CRACK_START_Y_CELLS)),
            (x + float(DIRT_CRACK_END_X_CELLS), y + float(DIRT_CRACK_END_Y_CELLS)),
            COLOR_DIRT_CRACK,
            DIRT_CRACK_WIDTH_CELLS,
        )


def draw_grass_cell(canvas: Canvas, x: int, y: int, seed: int, salt: int) -> None:
    draw_grains(
        canvas,
        x,
        y,
        GRASS_GRAINS_PER_CELL,
        GRASS_PALETTE,
        GRASS_GRAIN_RADIUS_CELLS,
        GRASS_GRAIN_RADIUS_SPAN_CELLS,
        seed,
        salt,
    )

    for blade in range(GRASS_MAX_BLADES_PER_CELL):
        channel = 300 + blade * 20
        if stable_unit(seed, salt, x, y, channel) >= float(GRASS_BLADE_CHANCE):
            continue
        root = (
            x
            + float(GRASS_ROOT_X_INSET_CELLS)
            + float(GRASS_ROOT_X_SPAN_CELLS) * stable_unit(seed, salt, x, y, channel + 1),
            y
            + float(GRASS_ROOT_Y_INSET_CELLS)
            + float(GRASS_ROOT_Y_SPAN_CELLS) * stable_unit(seed, salt, x, y, channel + 2),
        )
        length = float(GRASS_BLADE_LENGTH_CELLS) + float(
            GRASS_BLADE_LENGTH_SPAN_CELLS
        ) * stable_unit(seed, salt, x, y, channel + 4)
        angle = float(GRASS_BLADE_ANGLE_MIN_RADIANS) + float(
            GRASS_BLADE_ANGLE_SPAN_RADIANS
        ) * stable_unit(seed, salt, x, y, channel + 3)
        tip = (root[0] + length * math.cos(angle), root[1] + length * math.sin(angle))
        green = round(
            COLOR_GRASS_BLADE_GREEN_MIN
            + COLOR_GRASS_BLADE_GREEN_SPAN * stable_unit(seed, salt, x, y, channel + 5)
        )
        canvas.line(
            root,
            tip,
            (COLOR_GRASS_BLADE_RED_BLUE[0], green, COLOR_GRASS_BLADE_RED_BLUE[1]),
            GRASS_BLADE_WIDTH_CELLS,
        )


def draw_floor_material(
    canvas: Canvas,
    polygon: Sequence[Point],
    material: str,
    seed: int,
    salt: int,
) -> None:
    canvas.polygon(polygon, FLOOR_WASH_COLORS[material])

    for x, y in cells_touched_by(polygon):
        if material == "metal":
            draw_metal_cell(canvas, x, y, broken=False, seed=seed, salt=salt)
        elif material == "broken_metal":
            draw_metal_cell(canvas, x, y, broken=True, seed=seed, salt=salt)
        elif material == "stone":
            draw_stone_cell(canvas, x, y)
        elif material == "sand":
            draw_grains(
                canvas,
                x,
                y,
                SAND_GRAINS_PER_CELL,
                SAND_PALETTE,
                GRAIN_RADIUS_CELLS,
                GRAIN_RADIUS_SPAN_CELLS,
                seed,
                salt,
            )
        elif material == "dirt":
            draw_dirt_cell(canvas, x, y, seed, salt)
        elif material == "grass":
            draw_grass_cell(canvas, x, y, seed, salt)
        else:
            raise ValueError(f"matière inconnue : {material}")


def draw_dashed_loop(
    canvas: Canvas,
    points: Sequence[Point],
    seed: int,
    salt: int,
) -> None:
    margin = float(RAIL_DASH_END_MARGIN_CELLS)
    for edge_index, (a, b) in enumerate(zip(points, points[1:] + points[:1])):
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        length = math.hypot(dx, dy)
        if length <= margin * 2:
            continue
        ux, uy = dx / length, dy / length
        position = margin
        dash_index = 0
        while position < length - margin:
            dash = float(RAIL_DASH_MIN_CELLS) + (
                float(RAIL_DASH_MAX_CELLS) - float(RAIL_DASH_MIN_CELLS)
            ) * stable_unit(seed, salt, edge_index, dash_index, 0)
            gap = float(RAIL_DASH_GAP_MIN_CELLS) + (
                float(RAIL_DASH_GAP_MAX_CELLS) - float(RAIL_DASH_GAP_MIN_CELLS)
            ) * stable_unit(seed, salt, edge_index, dash_index, 1)
            end = min(position + dash, length - margin)
            if end > position:
                canvas.line(
                    (a[0] + ux * position, a[1] + uy * position),
                    (a[0] + ux * end, a[1] + uy * end),
                    COLOR_DASH,
                    RAIL_DASH_WIDTH_CELLS,
                )
            position = end + gap
            dash_index += 1


def draw_plate(canvas: Canvas, centre: Point) -> None:
    half_side = float(JUNCTION_PLATE_SIDE_CELLS) / 2
    canvas.rectangle(
        centre,
        half_side,
        half_side,
        COLOR_SHIP_BODY,
        outline=COLOR_HULL,
        outline_width=JUNCTION_PLATE_BORDER_CELLS,
    )
    canvas.rectangle(
        centre,
        JUNCTION_PLATE_CORE_HALF_SIDE_CELLS,
        JUNCTION_PLATE_CORE_HALF_SIDE_CELLS,
        COLOR_NODE,
    )


def draw_trim_ticks(canvas: Canvas, outline: Sequence[Point]) -> None:
    ring = offset_polygon(outline, TRIM_BAND_MIDLINE_CELLS)
    spacing = float(TRIM_TICK_SPACING_CELLS)
    margin = float(TRIM_TICK_END_MARGIN_CELLS)
    reach = float(TRIM_TICK_REACH_CELLS)
    phase = 0.0
    lean_angle = math.radians(TRIM_TICK_LEAN_DEGREES)

    for a, b in zip(ring, ring[1:] + ring[:1]):
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        length = math.hypot(dx, dy)
        if length == 0:
            continue
        ux, uy = dx / length, dy / length

        if abs(ux) < float(TRIM_STRAIGHT_THRESHOLD) or abs(uy) < float(
            TRIM_STRAIGHT_THRESHOLD
        ):
            lean = (reach, -reach)
        else:
            cosine = math.cos(lean_angle)
            sine = math.sin(lean_angle)
            lean = (
                (ux * cosine + uy * sine) * reach / sine,
                (uy * cosine - ux * sine) * reach / sine,
            )

        position = phase
        while position <= length - margin:
            if position >= margin:
                centre = (a[0] + ux * position, a[1] + uy * position)
                canvas.line(
                    (centre[0] - lean[0], centre[1] - lean[1]),
                    (centre[0] + lean[0], centre[1] + lean[1]),
                    COLOR_TRIM_TICK,
                    TRIM_TICK_WIDTH_CELLS,
                )
            position += spacing
        phase = (spacing - (length - phase) % spacing) % spacing


def draw_floor_boundary(canvas: Canvas, outline: Sequence[Point], seed: int) -> None:
    # La masse est effacée seulement du côté masse du contour.
    mass_clear_path = offset_polygon(outline, -ROOM_HATCH_SETBACK_CELLS * Fraction(1, 2))
    canvas.polyline(
        mass_clear_path,
        COLOR_SHIP_BODY,
        ROOM_HATCH_SETBACK_CELLS,
    )

    # Le champ noir du liseré repousse le sol vers l'intérieur, sans le supprimer.
    field_path = offset_polygon(outline, TRIM_FIELD_INSET_CELLS * Fraction(1, 2))
    canvas.polyline(field_path, COLOR_SHIP_BODY, TRIM_FIELD_INSET_CELLS)

    near_distance = -(
        ROOM_WALL_RAIL_PAIR_DEPTH_CELLS
        - ROOM_WALL_RAIL_CENTER_GAP_CELLS * Fraction(1, 2)
    )
    far_distance = -(
        ROOM_WALL_RAIL_PAIR_DEPTH_CELLS
        + ROOM_WALL_RAIL_CENTER_GAP_CELLS * Fraction(1, 2)
    )
    mid_distance = -ROOM_WALL_RAIL_PAIR_DEPTH_CELLS
    near = offset_polygon(outline, near_distance)
    far = offset_polygon(outline, far_distance)
    mid = offset_polygon(outline, mid_distance)

    canvas.polyline(near, COLOR_HULL, ROOM_WALL_RAIL_WIDTH_CELLS)
    canvas.polyline(far, COLOR_HULL, ROOM_WALL_RAIL_WIDTH_CELLS)
    draw_dashed_loop(canvas, mid, seed, 1000)

    separation = offset_polygon(outline, TRIM_SEPARATION_INSET_CELLS)
    canvas.polyline(separation, COLOR_TRIM_LINE, TRIM_SEPARATION_WIDTH_CELLS)
    draw_trim_ticks(canvas, outline)

    for point in separation:
        canvas.rectangle(
            point,
            TRIM_NODE_HALF_SIDE_CELLS,
            TRIM_NODE_HALF_SIDE_CELLS,
            COLOR_TRIM_NODE,
        )
    for point in mid:
        draw_plate(canvas, point)


def draw_hull(canvas: Canvas, sector: Sequence[Point], seed: int) -> None:
    clear_path = offset_polygon(sector, HULL_HATCH_SETBACK_CELLS * Fraction(1, 2))
    canvas.polyline(clear_path, COLOR_SHIP_BODY, HULL_HATCH_SETBACK_CELLS)

    edge = offset_polygon(sector, HULL_EDGE_LINE_WIDTH_CELLS * Fraction(1, 2))
    near = offset_polygon(
        sector,
        HULL_RAIL_PAIR_DEPTH_CELLS - HULL_RAIL_CENTER_GAP_CELLS * Fraction(1, 2),
    )
    far = offset_polygon(
        sector,
        HULL_RAIL_PAIR_DEPTH_CELLS + HULL_RAIL_CENTER_GAP_CELLS * Fraction(1, 2),
    )
    mid = offset_polygon(sector, HULL_RAIL_PAIR_DEPTH_CELLS)

    canvas.polyline(edge, COLOR_HULL, HULL_EDGE_LINE_WIDTH_CELLS)
    canvas.polyline(near, COLOR_HULL, HULL_NEAR_RAIL_WIDTH_CELLS)
    canvas.polyline(far, COLOR_HULL, HULL_FAR_RAIL_WIDTH_CELLS)
    draw_dashed_loop(canvas, mid, seed, 2000)


def draw_door(canvas: Canvas, room: RoomSpec) -> None:
    px, py = room.door_port
    dx, dy = room.door_direction
    tx, ty = -dy, dx
    centre = (
        px + dx * float(DOOR_LEAF_FROM_ROOM_CELLS),
        py + dy * float(DOOR_LEAF_FROM_ROOM_CELLS),
    )
    half_open = float(DOOR_OPEN_WIDTH_CELLS) / 2
    canvas.rectangle(
        centre,
        half_open if dx == 0 else DOOR_RECESS_HALF_DEPTH_CELLS,
        DOOR_RECESS_HALF_DEPTH_CELLS if dx == 0 else half_open,
        COLOR_SHIP_BODY,
    )

    frame_offset = float(ROOM_WALL_RAIL_CENTER_GAP_CELLS) / 2
    for offset in (-frame_offset, frame_offset):
        canvas.line(
            (
                centre[0] - tx * half_open + dx * offset,
                centre[1] - ty * half_open + dy * offset,
            ),
            (
                centre[0] + tx * half_open + dx * offset,
                centre[1] + ty * half_open + dy * offset,
            ),
            COLOR_DASH,
            DOOR_FRAME_LINE_WIDTH_CELLS,
        )

    jamb_reach = float(DOOR_JAMB_REACH_CELLS)
    for side in (-half_open, half_open):
        jamb = centre[0] + tx * side, centre[1] + ty * side
        canvas.line(
            (jamb[0] - dx * jamb_reach, jamb[1] - dy * jamb_reach),
            (jamb[0] + dx * jamb_reach, jamb[1] + dy * jamb_reach),
            COLOR_NODE,
            DOOR_JAMB_WIDTH_CELLS,
        )

    start = -half_open + float(DOOR_LEAF_INSET_CELLS)
    end = half_open - float(DOOR_LEAF_INSET_CELLS)
    position = start
    index = 0
    while position < end:
        dash_end = min(position + float(DOOR_LEAF_DASH_CELLS), end)
        canvas.line(
            (centre[0] + tx * position, centre[1] + ty * position),
            (centre[0] + tx * dash_end, centre[1] + ty * dash_end),
            COLOR_DOOR_A if index % 2 == 0 else COLOR_DOOR_B,
            DOOR_LEAF_WIDTH_CELLS,
        )
        position = dash_end + float(DOOR_LEAF_DASH_GAP_CELLS)
        index += 1


def draw_verification_grid(
    canvas: Canvas,
    silhouette_mask: Image.Image,
) -> None:
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    width = canvas.final_pixels(VERIFY_GRID_WIDTH_PIXELS)

    for x in range(SECTOR_WIDTH_CELLS + 1):
        draw.line(
            [canvas.px((x, 0)), canvas.px((x, SECTOR_HEIGHT_CELLS))],
            fill=COLOR_VERIFY_GRID,
            width=width,
        )
    for y in range(SECTOR_HEIGHT_CELLS + 1):
        draw.line(
            [canvas.px((0, y)), canvas.px((SECTOR_WIDTH_CELLS, y))],
            fill=COLOR_VERIFY_GRID,
            width=width,
        )

    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), silhouette_mask))
    canvas.image.alpha_composite(layer)


def render(seed: int, show_grid: bool) -> Image.Image:
    layout = build_layout(seed)
    canvas = Canvas()
    draw_paper(canvas)

    silhouette_mask = canvas.mask_for(layout.sector)
    floor_mask = canvas.mask_for(layout.floor)
    canvas.polygon(layout.sector, COLOR_SHIP_BODY)
    draw_mass_hatching(canvas, silhouette_mask, floor_mask)

    # Le couloir reste du métal ; les dix pièces montrent les six matières gelées.
    draw_floor_material(canvas, layout.corridor, "metal", seed, -1)
    for room in layout.rooms:
        draw_floor_material(canvas, room_polygon(room), room.material, seed, room.index)
        draw_floor_material(canvas, neck_polygon(room), room.material, seed, room.index)

    draw_floor_boundary(canvas, layout.floor, seed)
    for room in layout.rooms:
        draw_door(canvas, room)
    draw_hull(canvas, layout.sector, seed)

    if show_grid:
        draw_verification_grid(canvas, silhouette_mask)

    return canvas.finish()


def format_constant(value: object) -> str:
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return f"{value.numerator}"
        return f"{value.numerator}/{value.denominator} (= {float(value):.4f})"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def print_constants() -> None:
    print("[CONSTANTES]")
    for name, value in globals().items():
        if name.isupper() and not name.startswith("_"):
            print(f"{name} = {format_constant(value)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dessine un secteur TheEnd déterministe à partir de constantes en cases."
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="graine déterministe")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / ".cache" / "reference" / "secteur-forme-mockup.png",
        help="PNG à écrire (défaut : TheEnd-Docs/.cache/reference/secteur-forme-mockup.png)",
    )
    grid = parser.add_mutually_exclusive_group()
    grid.add_argument("--grid", dest="show_grid", action="store_true", help="affiche la grille de contrôle")
    grid.add_argument(
        "--no-grid",
        dest="show_grid",
        action="store_false",
        help="masque la grille de contrôle",
    )
    parser.set_defaults(show_grid=SHOW_CELL_GRID_DEFAULT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image = render(args.seed, args.show_grid)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(
        args.output,
        format="PNG",
        compress_level=PNG_COMPRESSION_LEVEL,
        optimize=False,
    )

    print_constants()
    print("[EXECUTION]")
    print(f"seed = {args.seed}")
    print(f"show_grid = {str(args.show_grid).lower()}")
    print(f"png = {args.output.resolve()}")
    print(f"size = {image.width}x{image.height}")


if __name__ == "__main__":
    main()
