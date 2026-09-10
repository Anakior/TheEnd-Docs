"""Planche de decision pour le sas, dessinee dans le langage du jeu.

Traits fins, plaques de jonction, rails doubles, hachure serree. Rien n'est un bloc plein :
tout est trace. Le dessin est fait a 3x puis reduit, pour que les obliques soient nettes.

Le sas fait 3 cases de large, c'est UN objet, et ferme il bloque comme un mur.
Les proportions du tube (3 cases de large, bordage de 2) sont mesurees dans le jeu, pas choisies.

    python3 reference/generate_sas_plan.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SS = 3                      # supersampling
CELL = 30
PLATING = 2                 # cases de coque de chaque cote du tube, mesurees dans le jeu
TUBE = 3

VOID = (9, 22, 40)
GRID = (22, 52, 84)
MASS = (13, 15, 20)
HATCH = (46, 52, 62)
HULL = (198, 208, 218)
WALL = (126, 138, 152)
FLOOR = (22, 26, 35)
CHAMBER = (30, 38, 54)
DOTS = (54, 62, 78)
STEEL = (150, 160, 172)
STEEL_DARK = (74, 82, 94)
ACCENT = (232, 158, 62)
SEAL = (188, 72, 60)
WELD = (198, 204, 212)
TEXT = (214, 222, 232)
SUBTLE = (124, 136, 150)
BG = (8, 13, 24)


def font(size):
    for path in (
        "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


F_TITLE = font(20)


class Sheet:
    """Un calque dessine a l'echelle SS. Toutes les coordonnees sont en pixels d'ecran."""

    def __init__(self, w, h, background=BG):
        self.img = Image.new("RGB", (w * SS, h * SS), background)
        self.d = ImageDraw.Draw(self.img)

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=1):
        self.d.rectangle(
            [x0 * SS, y0 * SS, x1 * SS, y1 * SS],
            fill=fill,
            outline=outline,
            width=max(1, round(width * SS)),
        )

    def line(self, x0, y0, x1, y1, fill, width=1):
        self.d.line(
            [x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=fill, width=max(1, round(width * SS))
        )

    def dot(self, x, y, r, fill):
        self.d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=fill)

    def flat(self):
        return self.img.resize((self.img.width // SS, self.img.height // SS), Image.LANCZOS)


def hatch(s, x0, y0, x1, y1):
    """La hachure de masse : fine, serree, a 45 degres."""
    s.rect(x0, y0, x1, y1, fill=MASS)
    step = 5
    start = int(x0 - (y1 - y0))
    x = start - (start % step)
    while x < x1 + 1:
        ax, ay = x, y1
        bx, by = x + (y1 - y0), y0
        if bx < x0 or ax > x1:
            x += step
            continue
        if ax < x0:
            ay = y1 - (x0 - ax)
            ax = x0
        if bx > x1:
            by = y0 + (bx - x1)
            bx = x1
        s.line(ax, ay, bx, by, HATCH, 0.6)
        x += step


def void(s, x0, y0, x1, y1):
    s.rect(x0, y0, x1, y1, fill=VOID)
    step = CELL * 4
    y = y0 - (y0 % step) + step
    while y < y1:
        s.line(x0, y, x1, y, GRID, 0.8)
        y += step
    x = x0 - (x0 % step) + step
    while x < x1:
        s.line(x, y0, x, y1, GRID, 0.8)
        x += step


def floor(s, x0, y0, x1, y1, colour=FLOOR):
    s.rect(x0, y0, x1, y1, fill=colour)
    y = y0 + CELL / 2
    while y < y1:
        x = x0 + CELL / 2
        while x < x1:
            s.dot(x, y, 0.45, DOTS)
            x += CELL
        y += CELL


def plate(s, x, y, size=3.4):
    """La plaque de jonction du jeu : un petit carre clair sur le trait."""
    s.rect(x - size / 2, y - size / 2, x + size / 2, y + size / 2, fill=HULL)


def rails(s, x, y0, y1):
    """Le double trait des murs, avec ses tirets."""
    s.line(x - 1.1, y0, x - 1.1, y1, WALL, 0.9)
    s.line(x + 1.1, y0, x + 1.1, y1, WALL, 0.9)
    y = y0 + 4
    while y < y1 - 3:
        s.line(x - 0.6, y, x + 0.6, y, STEEL_DARK, 0.7)
        y += 9


def tube(s, cx, cy, length, doors, chambers, treatment, state, caps=True):
    """Un tube vertical de `length` cases, avec ses nacelles aux deux bouts."""
    total_w = TUBE + 2 * PLATING
    x0, y0 = cx, cy
    x1, y1 = cx + total_w * CELL, cy + length * CELL

    tx0 = cx + PLATING * CELL
    tx1 = tx0 + TUBE * CELL

    if caps:
        for side in (-1, 1):
            ry0 = y0 - 2 * CELL if side < 0 else y1
            hatch(s, x0 - CELL, ry0, x1 + CELL, ry0 + 2 * CELL)
            floor(s, tx0, ry0, tx1, ry0 + 2 * CELL)
            edge_y = ry0 if side > 0 else ry0 + 2 * CELL
            s.line(x0 - CELL, edge_y, x1 + CELL, edge_y, HULL, 1.2)
            rails(s, tx0, ry0, ry0 + 2 * CELL)
            rails(s, tx1, ry0, ry0 + 2 * CELL)

    hatch(s, x0, y0, x1, y1)
    for a, b in chambers:
        floor(s, tx0, y0 + a * CELL, tx1, y0 + (b + 1) * CELL, CHAMBER)
    for y in range(length):
        if not any(a <= y <= b for a, b in chambers):
            floor(s, tx0, y0 + y * CELL, tx1, y0 + (y + 1) * CELL)

    # coque : un trait fin au bord, un plus marque en retrait
    for x in (x0, x1):
        s.line(x, y0, x, y1, HULL, 1.2)
        inner = x + 2.4 if x == x0 else x - 2.4
        s.line(inner, y0, inner, y1, STEEL_DARK, 0.7)

    rails(s, tx0, y0, y1)
    rails(s, tx1, y0, y1)

    for y in doors:
        sas(s, tx0, y0 + y * CELL, TUBE * CELL, CELL, treatment, state)


def sas(s, x, y, w, h, treatment, state):
    """Le sas : un mecanisme, pas une barre. x,y = coin de la case, w = 3 cases."""
    mid = x + w / 2

    if treatment == "fin":
        frame_out, depth = 2.0, h * 0.34
    elif treatment == "cadre":
        frame_out, depth = 4.5, h * 0.46
    else:  # blindee
        frame_out, depth = 6.5, h * 0.62

    top = y + (h - depth) / 2
    bot = top + depth

    # la niche : le mur s'epaissit autour du sas, sur deux cases
    if treatment == "blindee":
        s.rect(x - frame_out, y - 3, x + w + frame_out, y + h + 3, fill=MASS)
        s.line(x - frame_out, y - 3, x + w + frame_out, y - 3, HULL, 1.1)
        s.line(x - frame_out, y + h + 3, x + w + frame_out, y + h + 3, HULL, 1.1)

    # les jambages : deux montants de coque qui mordent dans le mur
    for jx in (x, x + w):
        s.rect(jx - frame_out, top - 2.5, jx + frame_out, bot + 2.5, fill=STEEL_DARK)
        s.rect(jx - frame_out, top - 2.5, jx + frame_out, bot + 2.5, outline=HULL, width=0.9)

    # le rail sur lequel courent les vantaux
    s.line(x, top - 1.2, x + w, top - 1.2, STEEL_DARK, 0.8)
    s.line(x, bot + 1.2, x + w, bot + 1.2, STEEL_DARK, 0.8)

    def leaf(a, b):
        """Un vantail, avec sa nervure et son lisere d'arete."""
        if b - a < 1.5:
            return
        s.rect(a, top, b, bot, fill=STEEL)
        s.rect(a, top, b, bot, outline=(232, 238, 244), width=0.8)
        if b - a > 9:
            s.line((a + b) / 2, top + 2.5, (a + b) / 2, bot - 2.5, STEEL_DARK, 0.7)

    if state == "ouvert":
        # les vantaux escamotes dans les jambages, le passage libre entre les deux
        s.rect(x + w * 0.16, top - 1, x + w * 0.84, bot + 1, fill=CHAMBER)
        px = x + w * 0.16 + CELL / 2
        while px < x + w * 0.84:
            s.dot(px, (top + bot) / 2, 0.45, DOTS)
            px += CELL
        leaf(x + 0.5, x + w * 0.16)
        leaf(x + w * 0.84, x + w - 0.5)
    elif state == "cycle":
        leaf(x + 0.5, mid - w * 0.20)
        leaf(mid + w * 0.20, x + w - 0.5)
        # les bords d'attaque, en avertissement
        s.line(mid - w * 0.20, top, mid - w * 0.20, bot, ACCENT, 1.4)
        s.line(mid + w * 0.20, top, mid + w * 0.20, bot, ACCENT, 1.4)
    else:
        leaf(x + 0.5, mid)
        leaf(mid, x + w - 0.5)
        s.line(mid, top + 0.5, mid, bot - 0.5, (18, 20, 26), 1.1)

    if state == "scelle":
        s.line(x + 1, top + depth / 2, x + w - 1, top + depth / 2, SEAL, 1.6)
        s.dot(mid, top + depth / 2, 2.6, SEAL)
    elif state == "soude":
        k = 0
        while k < w - 3:
            s.line(x + 2 + k, top + 1.5, x + 5 + k, bot - 1.5, WELD, 1.0)
            k += 5

    plate(s, x, top - 2.5)
    plate(s, x, bot + 2.5)
    plate(s, x + w, top - 2.5)
    plate(s, x + w, bot + 2.5)


def tile(title, subtitle, length, doors, chambers, treatment, state, caps=True):
    w_cells = TUBE + 2 * PLATING
    pad = CELL
    text_w = max(font(17).getbbox(title)[2], font(12).getbbox(subtitle or "")[2]) + 28
    width = max(w_cells * CELL + 2 * pad, text_w)
    top = 52
    height = top + (length + (4 if caps else 0)) * CELL + 14

    s = Sheet(int(width), int(height), BG)
    cx = (width - w_cells * CELL) / 2
    cy = top + (2 * CELL if caps else 0)
    void(s, 0, top, width, height)
    tube(s, cx, cy, length, doors, chambers, treatment, state, caps)

    # le texte est pose APRES la reduction, sinon le reechantillonnage le delave
    flat = s.flat()
    d = ImageDraw.Draw(flat)
    d.text((14, 10), title, fill=TEXT, font=font(17))
    if subtitle:
        d.text((14, 31), subtitle, fill=SUBTLE, font=font(12))
    return flat


def row(images, gap=12):
    width = sum(i.width for i in images) + gap * (len(images) - 1)
    height = max(i.height for i in images)
    strip = Image.new("RGB", (width, height), BG)
    x = 0
    for i in images:
        strip.paste(i, (x, 0))
        x += i.width + gap
    return strip


def stack(rows, headers, gap=22):
    width = max(r.width for r in rows) + 44
    height = sum(r.height + 30 for r in rows) + gap * (len(rows) + 1)
    sheet = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(sheet)
    y = gap
    for r, head in zip(rows, headers):
        d.text((22, y), head, fill=TEXT, font=F_TITLE)
        y += 30
        sheet.paste(r, (22, y))
        y += r.height + gap
    return sheet


disposition = [
    tile("A.  chambre unique", "le tube EST la chambre : 2 portes, 12 cases entre elles",
         12, [0, 11], [(1, 10)], "cadre", "ferme"),
    tile("B.  chambre compacte", "2 portes, chambre de 3 cases, couloir de part et d'autre",
         12, [4, 8], [(5, 7)], "cadre", "ferme"),
    tile("C.  double chambre", "la reference : 3 portes, 2 chambres de 3 cases",
         12, [1, 5, 9], [(2, 4), (6, 8)], "cadre", "ferme"),
]

lisibilite = [
    tile("1.  fin", "jambages discrets, vantaux minces",
         7, [3], [(4, 6)], "fin", "ferme", caps=False),
    tile("2.  cadre", "montants marques, rail visible",
         7, [3], [(4, 6)], "cadre", "ferme", caps=False),
    tile("3.  blindee", "le mur s'epaissit autour, emprise de 2 cases",
         7, [3], [(4, 6)], "blindee", "ferme", caps=False),
]

etats = [
    tile("ouvert", "vantaux escamotes dans les jambages",
         7, [3], [(4, 6)], "cadre", "ouvert", caps=False),
    tile("en cycle", "les deux vantaux courent, bords en avertissement",
         7, [3], [(4, 6)], "cadre", "cycle", caps=False),
    tile("ferme", "bloque comme un mur, ouvrable",
         7, [3], [(4, 6)], "cadre", "ferme", caps=False),
    tile("scelle", "ferme sur ordre, verrouille",
         7, [3], [(4, 6)], "cadre", "scelle", caps=False),
    tile("soude", "definitif : la nacelle est retranchee",
         7, [3], [(4, 6)], "cadre", "soude", caps=False),
]

sheet = stack(
    [row(disposition), row(lisibilite), row(etats)],
    [
        "DISPOSITION   quelle forme prend le sas dans le tube",
        "LISIBILITE   le sas est un objet de 3 cases, il doit se voir",
        "ETATS   ferme bloque comme un mur",
    ],
)

out = Path(__file__).resolve().parents[1] / ".cache" / "reference" / "sas-planche.png"
out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out)
print(f"{out} : {sheet.width}x{sheet.height}")
