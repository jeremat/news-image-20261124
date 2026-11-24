"""Draw the 24 November 2026 front page, v2 dense (1024x1024) with PIL.

Winner anatomy (from the 17-22 Nov leaderboards, win rates 85-87%):
masthead with story counts, UTC timeline strip, 3 big leads with
data-carrying drawn illustrations + CONFIRMED/REPORTED/CLAIM tags and
sources, a row of medium stories, an ALSO ON briefs list, a WHERE IT
HAPPENED map with numbered pins, a DATE CHECK footer and a DAY IN
NUMBERS box. Our v1 (6 stories, 57.7% on 18 Nov) was far too thin.

Deterministic: fixed text, fixed geometry, no time, no randomness, no
network. Run it here to produce entry.png; main.py only copies that file.

Story data lives in STORIES below (leads, mediums, briefs, timeline,
numbers, date check, map pins) and is filled from
~/workspace/makefun/research-20261124-v2.md.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 230)
INK = (20, 20, 20)
MUTED = (58, 58, 58)
WHITE = (255, 255, 255)
RED = (180, 35, 24)
BLUE = (29, 78, 216)
OCEAN = (191, 227, 240)
LAND = (232, 222, 196)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w, draw):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def trunc(text, fnt, max_w, draw):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=fnt) > max_w:
        text = text[:-1]
    return text + "…"


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    import math

    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def shield(draw, x, y, w, h, fill, outline):
    pts = [
        (x, y),
        (x + w, y),
        (x + w, y + h * 0.55),
        (x + w / 2, y + h),
        (x, y + h * 0.55),
    ]
    draw.polygon(pts, fill=fill, outline=outline, width=3)


# --- lead pictograms, drawn in fractions of their box --------------------

def picto_sea(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=OCEAN)
    sea_y = y0 + v * 0.55
    d.rectangle([x0, sea_y, x1, y1], fill=(31, 95, 139))
    for wx in range(0, int(u) - 20, 34):
        d.arc([x0 + wx, sea_y + 8, x0 + wx + 30, sea_y + 26], 180, 360,
              fill=WHITE, width=3)
    hull = [
        (x0 + u * 0.12, sea_y - v * 0.28), (x0 + u * 0.72, sea_y - v * 0.06),
        (x0 + u * 0.72, sea_y + v * 0.13), (x0 + u * 0.42, sea_y + v * 0.17),
        (x0 + u * 0.12, sea_y + v * 0.13),
    ]
    d.polygon(hull, fill=(30, 30, 34))
    d.rectangle([x0 + u * 0.25, sea_y - v * 0.48, x0 + u * 0.38, sea_y - v * 0.28],
                fill=(30, 30, 34))
    d.rectangle([x0 + u * 0.40, sea_y - v * 0.42, x0 + u * 0.44, sea_y - v * 0.28],
                fill=(30, 30, 34))
    starburst(d, x0 + u * 0.85, sea_y - 2, 26, 12, 8, (255, 122, 26))
    starburst(d, x0 + u * 0.85, sea_y - 2, 14, 7, 8, (255, 214, 64))
    for dx, dy in [(0.08, 0.12), (0.20, 0.06), (0.32, 0.14), (0.45, 0.08),
                   (0.58, 0.14), (0.70, 0.06), (0.82, 0.12)]:
        d.ellipse([x0 + u * dx, y0 + v * dy, x0 + u * dx + 7, y0 + v * dy + 7],
                  fill=INK)
        d.line([x0 + u * dx + 3, y0 + v * dy + 7, x0 + u * dx + 3,
                y0 + v * dy + 13], fill=INK, width=2)


def picto_satellite(d, x0, y0, x1, y1):
    import math
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(14, 27, 51))
    d.ellipse([x0 - u * 0.03, y1 - v * 0.60, x0 + u * 0.42, y1 + v * 1.15],
              fill=(46, 127, 194))
    d.ellipse([x0 + u * 0.07, y1 - v * 0.52, x0 + u * 0.21, y1 - v * 0.20],
              fill=(64, 160, 90))
    d.ellipse([x0 + u * 0.24, y1 - v * 0.42, x0 + u * 0.36, y1 - v * 0.11],
              fill=(64, 160, 90))
    for a in range(0, 360, 24):
        x = x0 + u * 0.75 + u * 0.45 * math.cos(math.radians(a))
        y = y0 + v * 0.45 + v * 0.30 * math.sin(math.radians(a))
        if x0 <= x <= x1 and y0 <= y <= y1:
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=WHITE)
    d.rectangle([x0 + u * 0.76, y0 + v * 0.28, x0 + u * 0.87, y0 + v * 0.52],
                fill=(200, 205, 212))
    d.rectangle([x0 + u * 0.65, y0 + v * 0.32, x0 + u * 0.75, y0 + v * 0.48],
                fill=(59, 110, 200))
    d.rectangle([x0 + u * 0.88, y0 + v * 0.32, x0 + u * 0.98, y0 + v * 0.48],
                fill=(59, 110, 200))
    starburst(d, x0 + u * 0.94, y0 + v * 0.20, 15, 7, 4, (255, 59, 48))


def picto_midterms(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(234, 240, 251))
    bar_y = y0 + v * 0.22
    bar_h = v * 0.36
    total_w = u - 24
    dem_w = total_w * 258 / 435
    rep_w = total_w * 173 / 435
    bx = x0 + 12
    d.rectangle([bx, bar_y, bx + dem_w, bar_y + bar_h], fill=BLUE)
    d.rectangle([bx + dem_w, bar_y, bx + dem_w + rep_w, bar_y + bar_h],
                fill=RED)
    d.rectangle([bx + dem_w + rep_w, bar_y, bx + total_w, bar_y + bar_h],
                fill=(148, 163, 184))
    f_big = font(SANS_B, max(18, int(v * 0.26)))
    d.text((bx + 12, bar_y + 5), "258", font=f_big, fill=WHITE)
    d.text((bx + dem_w + 12, bar_y + 5), "173", font=f_big, fill=WHITE)
    f_small = font(SANS_B, max(11, int(v * 0.15)))
    d.text((bx + 2, bar_y + bar_h + 8), "DEM 258", font=f_small, fill=BLUE)
    d.text((bx + total_w, bar_y + bar_h + 8), "REP 173", font=f_small,
           fill=RED, anchor="ra")


def picto_cyber(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(230, 244, 242))
    shield(d, x0 + u * 0.24, y0 + v * 0.08, u * 0.24, v * 0.72,
           BLUE, INK)
    shield(d, x0 + u * 0.55, y0 + v * 0.08, u * 0.24, v * 0.72,
           (15, 118, 110), INK)
    f_plus = font(SANS_B, max(22, int(v * 0.34)))
    d.text((x0 + u * 0.49, y0 + v * 0.22), "+", font=f_plus, fill=INK)
    f_check = font(SANS_B, max(20, int(v * 0.30)))
    d.text((x0 + u * 0.32, y0 + v * 0.28), "✓", font=f_check, fill=WHITE)
    d.text((x0 + u * 0.63, y0 + v * 0.28), "✓", font=f_check, fill=WHITE)
    for cx, cy in [(0.10, 0.20), (0.90, 0.20), (0.10, 0.62), (0.90, 0.62)]:
        d.ellipse([x0 + u * cx - 4, y0 + v * cy - 4, x0 + u * cx + 4,
                   y0 + v * cy + 4], fill=(15, 118, 110))


def picto_cop31(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(234, 245, 236))
    cx, cy, r = x0 + u * 0.32, y0 + v * 0.44, v * 0.40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 127, 194))
    d.ellipse([cx - r * 0.55, cy - r * 0.45, cx + r * 0.05, cy + r * 0.10],
              fill=(64, 160, 90))
    d.ellipse([cx + r * 0.20, cy + r * 0.15, cx + r * 0.70, cy + r * 0.65],
              fill=(64, 160, 90))
    d.line([x0 + u * 0.62, y0 + v * 0.08, x0 + u * 0.92, y0 + v * 0.82],
           fill=RED, width=10)
    d.line([x0 + u * 0.92, y0 + v * 0.08, x0 + u * 0.62, y0 + v * 0.82],
           fill=RED, width=10)


def picto_iran(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(251, 239, 234))
    sea_y = y0 + v * 0.6
    d.rectangle([x0, sea_y, x1, y1], fill=(31, 95, 139))
    d.polygon([(x0, y0), (x0 + u * 0.18, y0), (x0 + u * 0.12, sea_y),
               (x0, sea_y)], fill=(120, 90, 70))
    d.polygon([(x1, y0), (x1 - u * 0.18, y0), (x1 - u * 0.12, sea_y),
               (x1, sea_y)], fill=(120, 90, 70))
    d.rectangle([x0 + u * 0.28, sea_y - v * 0.15, x0 + u * 0.82, sea_y + v * 0.15],
                fill=(30, 30, 34))
    for i, col in enumerate([(200, 60, 40), (230, 180, 40), (40, 120, 90)]):
        d.rectangle([x0 + u * (0.32 + i * 0.15), sea_y - v * 0.36,
                     x0 + u * (0.44 + i * 0.15), sea_y - v * 0.15], fill=col)
    d.rectangle([x0 + u * 0.78, sea_y - v * 0.42, x0 + u * 0.82, sea_y - v * 0.15],
                fill=(230, 230, 230))
    for lx in range(int(x0 + u * 0.18), int(x1 - u * 0.18), 26):
        d.ellipse([lx, sea_y - v * 0.52, lx + 14, sea_y - v * 0.38],
                  outline=RED, width=4)

# --- small pictograms for the medium row (simple, flat) -------------------

def picto_chart(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(234, 240, 251))
    d.line([x0 + 10, y0 + v - 12, x1 - 8, y0 + v - 12], fill=INK, width=2)
    d.line([x0 + 10, y0 + 8, x0 + 10, y0 + v - 12], fill=INK, width=2)
    for i, (bh, col) in enumerate([(0.30, BLUE), (0.45, BLUE),
                                   (0.62, BLUE), (0.80, RED)]):
        bx = x0 + 22 + i * (u - 40) / 4
        bw = (u - 40) / 4 * 0.55
        d.rectangle([bx, y0 + v - 12 - v * bh, bx + bw, y0 + v - 12], fill=col)


def picto_quake(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(251, 241, 220))
    for i, bh in enumerate([0.45, 0.65, 0.55]):
        bx = x0 + 14 + i * (u - 28) / 3
        bw = (u - 28) / 3 * 0.7
        d.rectangle([bx, y0 + v - 10 - v * bh, bx + bw, y0 + v - 10],
                    fill=(90, 90, 96))
    d.line([x0 + u * 0.5, y0 + 6, x0 + u * 0.42, y0 + v * 0.5,
            x0 + u * 0.58, y0 + v * 0.75, x0 + u * 0.5, y0 + v - 10],
           fill=RED, width=3)


def picto_rocket(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(14, 27, 51))
    for sx, sy in [(0.15, 0.2), (0.85, 0.15), (0.75, 0.55), (0.2, 0.65)]:
        d.ellipse([x0 + u * sx - 2, y0 + v * sy - 2, x0 + u * sx + 2,
                   y0 + v * sy + 2], fill=WHITE)
    cx = x0 + u * 0.5
    d.polygon([(cx, y0 + v * 0.08), (cx + u * 0.10, y0 + v * 0.45),
               (cx - u * 0.10, y0 + v * 0.45)], fill=(230, 230, 230))
    d.rectangle([cx - u * 0.10, y0 + v * 0.45, cx + u * 0.10, y0 + v * 0.62],
                fill=RED)
    d.polygon([(cx - u * 0.10, y0 + v * 0.45), (cx - u * 0.20, y0 + v * 0.68),
               (cx - u * 0.10, y0 + v * 0.62)], fill=(200, 60, 40))
    d.polygon([(cx + u * 0.10, y0 + v * 0.45), (cx + u * 0.20, y0 + v * 0.68),
               (cx + u * 0.10, y0 + v * 0.62)], fill=(200, 60, 40))
    d.polygon([(cx - u * 0.06, y0 + v * 0.62), (cx + u * 0.06, y0 + v * 0.62),
               (cx, y0 + v * 0.88)], fill=(255, 180, 40))


def picto_storm(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(234, 240, 251))
    cx, cy = x0 + u * 0.5, y0 + v * 0.42
    for r in (v * 0.34, v * 0.24, v * 0.14):
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 120, fill=(31, 95, 139),
              width=4)
    for rx in (0.25, 0.45, 0.65):
        d.line([x0 + u * rx, y0 + v * 0.78, x0 + u * rx - 4, y0 + v * 0.92],
               fill=BLUE, width=3)


def picto_court(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(240, 238, 232))
    d.polygon([(x0 + u * 0.1, y0 + v * 0.30), (x0 + u * 0.9, y0 + v * 0.30),
               (x0 + u * 0.5, y0 + v * 0.08)], fill=(120, 110, 95))
    d.rectangle([x0 + u * 0.12, y0 + v * 0.30, x0 + u * 0.88, y0 + v * 0.38],
                fill=(120, 110, 95))
    for i in range(4):
        cx = x0 + u * (0.20 + i * 0.20)
        d.rectangle([cx - 4, y0 + v * 0.38, cx + 4, y0 + v * 0.82],
                    fill=(150, 142, 128))
    d.rectangle([x0 + u * 0.10, y0 + v * 0.82, x0 + u * 0.90, y0 + v * 0.90],
                fill=(120, 110, 95))


def picto_summit(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(234, 245, 236))
    for i, col in enumerate([BLUE, RED, (21, 128, 61)]):
        px = x0 + u * (0.20 + i * 0.30)
        d.line([px, y0 + v * 0.15, px, y0 + v * 0.85], fill=INK, width=3)
        d.polygon([(px, y0 + v * 0.15), (px + u * 0.22, y0 + v * 0.25),
                   (px, y0 + v * 0.35)], fill=col)


def picto_globe(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(234, 240, 251))
    cx, cy, r = x0 + u * 0.5, y0 + v * 0.5, min(u, v) * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 127, 194))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=WHITE,
              width=2)
    d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=2)


def picto_fire(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(251, 239, 234))
    cx, cy = x0 + u * 0.5, y0 + v * 0.55
    d.polygon([(cx, y0 + v * 0.10), (cx + u * 0.22, y0 + v * 0.50),
               (cx + u * 0.10, y0 + v * 0.50), (cx + u * 0.18, y0 + v * 0.85),
               (cx - u * 0.18, y0 + v * 0.85), (cx - u * 0.10, y0 + v * 0.50),
               (cx - u * 0.22, y0 + v * 0.50)], fill=(255, 122, 26))
    d.polygon([(cx, y0 + v * 0.45), (cx + u * 0.10, y0 + v * 0.70),
               (cx - u * 0.10, y0 + v * 0.70)], fill=(255, 214, 64))


def picto_markets(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(234, 245, 236))
    d.text((x0 + 12, y0 + 6), "+31.5%",
           font=font(SANS_B, max(26, int(v * 0.32))), fill=(21, 128, 61))
    base = y0 + v - 10
    top = y0 + v * 0.52
    for i, frac in enumerate([0.35, 0.50, 0.45, 0.70, 1.0]):
        bx = x0 + 14 + i * (u - 28) / 5
        bw = (u - 28) / 5 * 0.55
        bh = (base - top) * frac
        d.rectangle([bx, base - bh, bx + bw, base], fill=(21, 128, 61))


def picto_plane(d, x0, y0, x1, y1):
    u, v = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(234, 240, 251))
    d.polygon([(x0 + u * 0.15, y0 + v * 0.55), (x0 + u * 0.75, y0 + v * 0.30),
               (x0 + u * 0.90, y0 + v * 0.30), (x0 + u * 0.78, y0 + v * 0.48),
               (x0 + u * 0.85, y0 + v * 0.62), (x0 + u * 0.62, y0 + v * 0.58),
               (x0 + u * 0.45, y0 + v * 0.75), (x0 + u * 0.35, y0 + v * 0.60),
               (x0 + u * 0.15, y0 + v * 0.62)], fill=(27, 42, 74))
    d.ellipse([x0 + u * 0.08, y0 + v * 0.18, x0 + u * 0.13, y0 + v * 0.28],
              outline=RED, width=2)
    d.ellipse([x0 + u * 0.20, y0 + v * 0.12, x0 + u * 0.25, y0 + v * 0.22],
              outline=RED, width=2)


# --- world map (rough lon/lat polygons, equirectangular) ------------------

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 47), (-70, 42), (-80, 32), (-90, 20), (-105, 20),
     (-115, 30), (-125, 40), (-145, 60), (-168, 66)],
    [(-55, 60), (-45, 60), (-40, 70), (-55, 76), (-60, 70)],
    [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-55, -35),
     (-65, -45), (-70, -55), (-75, -40), (-80, -20), (-80, 10)],
    [(-10, 36), (0, 44), (-5, 48), (5, 58), (10, 58), (18, 56), (25, 60),
     (30, 70), (40, 68), (35, 60), (30, 50), (25, 45), (15, 40), (10, 38),
     (0, 36)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 12), (50, 10), (45, 0), (40, -10), (35, -25), (30, -35),
     (20, -35), (15, -25), (12, -10), (8, 4), (-8, 5), (-17, 15)],
    [(40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
     (160, 70), (170, 66), (160, 60), (140, 50), (130, 42), (120, 40),
     (110, 20), (105, 10), (100, 5), (95, 15), (90, 22), (80, 8),
     (75, 20), (65, 25), (55, 26), (50, 30), (45, 30), (40, 40), (40, 68)],
    [(113, -22), (125, -15), (135, -12), (142, -11), (150, -22), (153, -28),
     (150, -37), (140, -38), (130, -32), (120, -34), (113, -22)],
]


def project(lon, lat, x0, y0, x1, y1):
    fx = (lon + 170) / 360.0
    fy = (75 - lat) / 130.0
    return (x0 + fx * (x1 - x0), y0 + fy * (y1 - y0))


def draw_map(d, x0, y0, x1, y1, pins):
    d.rectangle([x0, y0, x1, y1], fill=(203, 226, 238))
    for poly in CONTINENTS:
        pts = [project(lon, lat, x0, y0, x1, y1) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(120, 110, 95))
    for num, lon, lat in pins:
        px, py = project(lon, lat, x0, y0, x1, y1)
        r = 10
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=WHITE, width=2)
        d.text((px, py - 1), str(num), font=font(SANS_B, 12), fill=WHITE,
               anchor="mm")

# --- story data (filled from research-20261124-v2.md) ---------------------

LEADS = [
    dict(num=1, region="Eastern Europe", field="Conflict",
         kicker="UKRAINE  •  LIBYA",
         color=RED, headline=["SUNK 1,700 KM", "FROM HOME"], picto=picto_sea,
         caption="7 sea drones sank the corvette Merkury off Benghazi; "
                 "the Angara was hit.",
         tag="CONFIRMED", source="Kyiv / AFP"),
    dict(num=2, region="North America", field="Markets",
         kicker="MARKETS  •  TECH",
         color=(21, 128, 61), headline=["NVIDIA SOARS", "31.5% IN A DAY"],
         picto=picto_markets,
         caption="Nvidia soars 31.5%, its best day in 23 years, and lifts "
                 "Asia on Tuesday.",
         tag="CONFIRMED", source="Reuters"),
    dict(num=3, region="Eastern Europe", field="Space",
         kicker="SPACE  •  RUSSIA",
         color=(27, 42, 74), headline=["A NUCLEAR", "SATELLITE?"],
         picto=picto_satellite,
         caption="Russia reportedly built a nuclear-capable satellite. "
                 "The Kremlin denies it.",
         tag="REPORTED", source="WDR / NDR / SZ"),
]

MEDIUMS = [
    dict(num=4, region="North America", field="Politics",
         kicker="USA  •  MIDTERMS",
         color=BLUE, headline="DEMOCRATS WIN 258 SEATS", picto=picto_midterms,
         caption="Democrats take 258 seats, most since 1992.",
         tag="CONFIRMED", source="AP"),
    dict(num=5, region="North America", field="Business",
         kicker="TECH  •  BUSINESS", color=(15, 118, 110),
         headline="$43.9 BILLION CYBER MEGADEAL", picto=picto_cyber,
         caption="CrowdStrike to buy Zscaler for $43.9bn.",
         tag="CONFIRMED", source="Reuters"),
    dict(num=6, region="Western Europe", field="Climate",
         kicker="CLIMATE  •  COP31",
         color=(21, 128, 61), headline="NO DEAL IN ANTALYA", picto=picto_cop31,
         caption="No deal at COP31 after the longest talks ever.",
         tag="CONFIRMED", source="AFP"),
    dict(num=7, region="Middle East", field="Conflict",
         kicker="IRAN  •  GULF",
         color=(127, 29, 29), headline="BLOCKADE STANDOFF", picto=picto_iran,
         caption="US blockade holds; Iran calls it aggression.",
         tag="CONFIRMED", source="Reuters"),
    dict(num=8, region="Asia-Pacific", field="Science",
         kicker="ASIA  •  NEPAL",
         color=(146, 64, 14), headline="QUAKE SHAKES NEPAL", picto=picto_quake,
         caption="M5.3 quake in Nepal; felt in five countries.",
         tag="CONFIRMED", source="Reuters"),
    dict(num=9, region="Asia-Pacific", field="Conflict",
         kicker="ASIA  •  KOREA",
         color=RED, headline="SEOUL SCRAMBLES JETS", picto=picto_plane,
         caption="Russian jets enter Seoul zone; jets scrambled.",
         tag="CONFIRMED", source="Reuters"),
]

# one line each, numbered 10-29 (20 briefs)
BRIEFS = [
    dict(num=10, region="North America", field="Crime",
         text="Mexico to try 'El Chapo Isidro' at home."),
    dict(num=11, region="North America", field="Conflict",
         text="Bukele names 3 soldiers killed in Haiti."),
    dict(num=12, region="North America", field="Health",
         text="Measles: ninth death in Pennsylvania."),
    dict(num=13, region="South America", field="Conflict",
         text="Car bomb hits Colombia governor's office."),
    dict(num=14, region="Western Europe", field="Politics",
         text="NATO: defence pledge now covers space."),
    dict(num=15, region="Eastern Europe", field="Conflict",
         text="Türkiye works on safe Black Sea passage."),
    dict(num=16, region="Eastern Europe", field="Conflict",
         text="Zaporizhzhia hit by new night attacks."),
    dict(num=17, region="Western Europe", field="Politics",
         text="Macron wants rare-earth reserves."),
    dict(num=18, region="Western Europe", field="Sport",
         text="Champions League returns tonight."),
    dict(num=19, region="Africa", field="Conflict",
         text="Libya demands answers from Kyiv."),
    dict(num=20, region="Africa", field="Conflict",
         text="Somalia, Uganda step up vs Al-Shabaab."),
    dict(num=21, region="Africa", field="Health",
         text="MSF suspends work in South Sudan's Yei."),
    dict(num=22, region="Africa", field="Disaster",
         text="Boat capsizes in Nigeria, at least 24 dead."),
    dict(num=23, region="Middle East", field="Humanitarian",
         text="Yemen: 360,000 displaced since August."),
    dict(num=24, region="Middle East", field="Conflict",
         text="Gaza strikes kill 3, incl. UNRWA worker."),
    dict(num=25, region="Middle East", field="Conflict",
         text="Houthis claim Saudi strike kills 17."),
    dict(num=26, region="Middle East", field="Culture",
         text="Iran lashes singer Parastoo Ahmadi."),
    dict(num=27, region="Middle East", field="Politics",
         text="Iran rules out talks until US meets 7 terms."),
    dict(num=28, region="Asia-Pacific", field="Politics",
         text="China sentences official to death for spying."),
    dict(num=29, region="Asia-Pacific", field="Science",
         text="China opens Tiangong to first foreign astronaut."),
]

# (UTC time, short label, max ~28 chars)
TIMELINE = [
    ("01:04", "Seoul reports Russian jets"),
    ("01:06", "Bukele names 3 dead in Haiti"),
    ("01:32", "M5.3 quake hits Nepal"),
    ("02:09", "US drone caught cartel boss"),
    ("02:15", "NATO: pledge covers space"),
    ("04:49", "Car bomb in Colombia"),
    ("07:04", "MSF halts work in S. Sudan"),
    ("20:00", "Arsenal v Dortmund"),
]

# (big figure, label)
NUMBERS = [
    ("+31.5%", "Nvidia in one day — best in 23 years"),
    ("+6.51%", "Nasdaq to 24,089.56"),
    ("360,000+", "displaced in Yemen since August"),
    ("M5.3", "Nepal quake, felt in 5 countries"),
]

# (what, real date) — 2 columns x 3 rows
DATECHECK = [
    ("GTA 6 launch", "19 Nov"),
    ("ICJ Myanmar ruling", "19 Nov"),
    ("Cyclone Akvan", "20 Nov"),
    ("Kane out for months", "20 Nov"),
    ("States sue SpaceX", "23 Nov"),
    ("EU sanctions plan", "23 Nov"),
]

MAP_PINS = [
    (1, 18.0, 30.0),    # Benghazi (nudged: avoids Antalya pin)
    (2, -121.9, 37.3),  # Santa Clara (Nvidia)
    (3, 40.0, 57.0),    # Moscow (nudged: avoids Antalya pin)
    (4, -77.0, 38.9),   # Washington
    (5, -97.7, 30.3),   # Austin (CrowdStrike)
    (6, 36.0, 41.0),    # Antalya (nudged: avoids Benghazi/Moscow pins)
    (7, 56.5, 26.5),    # Strait of Hormuz
    (8, 85.3, 27.7),    # Nepal
    (9, 127.0, 37.5),   # Seoul
]

TAG_COLORS = {"CONFIRMED": (21, 128, 61), "REPORTED": (180, 120, 0),
              "CLAIM": (180, 35, 24), "OFFICIAL": (29, 78, 216)}


def tag_line(d, x, y, tag, source, size):
    col = TAG_COLORS.get(tag, MUTED)
    d.ellipse([x, y + 3, x + 8, y + 11], fill=col)
    d.text((x + 12, y), tag, font=font(SANS_B, size), fill=col)
    w = d.textlength(tag, font=font(SANS_B, size))
    d.text((x + 12 + w + 6, y), "— " + source, font=font(SANS, size),
           fill=MUTED)


def draw_lead(img, d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 26], fill=s["color"])
    d.text((x + 10, y + 3), f"{s['num']}  {s['kicker']}",
           font=font(SANS_B, 15), fill=WHITE)
    hy = y + 34
    for line in s["headline"][:2]:
        d.text((x + 10, hy), line, font=font(SERIF_B, 29), fill=INK)
        hy += 34
    pw, ph = w - 20, 110
    layer = Image.new("RGB", (pw, ph), WHITE)
    ld = ImageDraw.Draw(layer)
    s["picto"](ld, 0, 0, pw, ph)
    img.paste(layer, (x + 10, y + 108))
    cap = wrap(s["caption"], font(SANS, 14), w - 20, d)
    if len(cap) > 2:
        print(f"WARNING: lead caption {len(cap)} lines: {s['kicker']}")
    cy = y + 226
    for line in cap[:2]:
        d.text((x + 10, cy), line, font=font(SANS, 14), fill=MUTED)
        cy += 18
    tag_line(d, x + 10, y + h - 24, s["tag"], s["source"], 12)


def draw_medium(img, d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    d.text((x + 8, y + 4), f"{s['num']}  {s['kicker']}",
           font=font(SANS_B, 10), fill=s["color"])
    pw, ph = w - 16, 58
    layer = Image.new("RGB", (pw, ph), WHITE)
    ld = ImageDraw.Draw(layer)
    s["picto"](ld, 0, 0, pw, ph)
    img.paste(layer, (x + 8, y + 22))
    lines = wrap(s["headline"], font(SERIF_B, 14), w - 16, d)
    hy = y + 86
    for line in lines[:3]:
        d.text((x + 8, hy), line, font=font(SERIF_B, 14), fill=INK)
        hy += 17
    cap = wrap(s["caption"], font(SANS, 11), w - 16, d)
    cy = hy + 2
    for line in cap[:2]:
        d.text((x + 8, cy), line, font=font(SANS, 11), fill=MUTED)
        cy += 13
    tag_line(d, x + 8, y + h - 16, s["tag"], s["source"], 10)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 8, H - 8], outline=INK, width=3)
    # masthead + counts
    d.text((W // 2, 12), "THE WORLD TODAY", font=font(SERIF_B, 54),
           fill=INK, anchor="ma")
    regions = {s["region"] for s in LEADS + MEDIUMS + BRIEFS}
    fields = {s["field"] for s in LEADS + MEDIUMS + BRIEFS}
    total = len(LEADS) + len(MEDIUMS) + len(BRIEFS)
    counts = (f"{total} STORIES  ·  {len(regions)} REGIONS  ·  "
              f"{len(fields)} FIELDS")
    d.text((W // 2, 70), counts, font=font(SANS_B, 17), fill=RED, anchor="ma")
    # date band
    d.rectangle([20, 94, W - 20, 126], fill=INK)
    d.text((W // 2, 99), "TUESDAY 24 NOVEMBER 2026",
           font=font(SANS_B, 26), fill=WHITE, anchor="ma")
    # UTC timeline strip
    d.line([20, 134, W - 20, 134], fill=INK, width=2)
    d.text((20, 140), "THE DAY IN UTC", font=font(SANS_B, 14), fill=INK)
    if TIMELINE:
        col_w = (W - 40 - 150) // len(TIMELINE)
        for i, (t, label) in enumerate(TIMELINE):
            tx = 180 + i * col_w
            d.text((tx, 140), t, font=font(SANS_B, 14), fill=RED)
            for j, line in enumerate(wrap(label, font(SANS, 12), col_w - 8, d)[:2]):
                d.text((tx, 158 + j * 14), line, font=font(SANS, 12),
                       fill=MUTED)
    d.line([20, 194, W - 20, 194], fill=INK, width=2)
    # leads
    lead_w, lead_h = 310, 298
    for i, s in enumerate(LEADS):
        draw_lead(img, d, s, 20 + i * (lead_w + 14), 202, lead_w, lead_h)
    # mediums (as many columns as stories)
    n_med = len(MEDIUMS)
    med_w = (W - 40 - (n_med - 1) * 10) // n_med if n_med else 0
    med_h = 184
    for i, s in enumerate(MEDIUMS):
        draw_medium(img, d, s, 20 + i * (med_w + 10), 508, med_w, med_h)
    # briefs (left) + map (right)
    d.text((20, 700), "ALSO ON 24 NOVEMBER", font=font(SANS_B, 15), fill=INK)
    d.line([20, 722, 660, 722], fill=INK, width=2)
    half = (len(BRIEFS) + 1) // 2
    for col in range(2):
        cx = 20 + col * 325
        for j, b in enumerate(BRIEFS[col * half:(col + 1) * half]):
            by = 728 + j * 16
            if by > 890:
                print(f"WARNING: brief overflows: {b['num']} {b['text'][:40]}")
                continue
            d.text((cx, by), f"{b['num']}.", font=font(SANS_B, 12), fill=RED)
            d.text((cx + 26, by),
                   trunc(b["text"], font(SANS, 12), 295, d),
                   font=font(SANS, 12), fill=INK)
    d.text((672, 700), "WHERE IT HAPPENED", font=font(SANS_B, 15), fill=INK)
    d.line([672, 722, W - 20, 722], fill=INK, width=2)
    draw_map(d, 672, 730, W - 20, 892, MAP_PINS)
    # numbers + date check
    d.line([20, 902, W - 20, 902], fill=INK, width=2)
    d.text((20, 910), "THE DAY IN NUMBERS", font=font(SANS_B, 14), fill=INK)
    if NUMBERS:
        nw = 540 // len(NUMBERS)
        for i, (big, label) in enumerate(NUMBERS):
            nx = 20 + i * nw
            d.text((nx, 930), big, font=font(SANS_B, 24), fill=RED)
            ly = 956
            for line in wrap(label, font(SANS, 11), nw - 8, d)[:2]:
                d.text((nx, ly), line, font=font(SANS, 11), fill=MUTED)
                ly += 13
    d.text((580, 910), "DATE CHECK — NOT FROM TODAY",
           font=font(SANS_B, 14), fill=INK)
    for i, (what, when) in enumerate(DATECHECK):
        dx = 580 + (i // 3) * 220
        dy = 930 + (i % 3) * 15
        d.text((dx, dy),
               f"✗  {what}  ({when})", font=font(SANS, 12), fill=MUTED)
    # footer
    d.line([20, 978, W - 20, 978], fill=INK, width=2)
    d.text((W // 2, 984),
           "Every story here happened, or was first reported, on Tuesday "
           "24 November 2026. Scenes are drawn illustrations, not photographs.",
           font=font(SANS, 11), fill=MUTED, anchor="ma")
    d.text((W // 2, 999),
           "REPORTED = outlets report it  ·  CLAIM = a party says so, "
           "unverified  ·  Sources: Reuters, AP, AFP, BBC, Bloomberg.",
           font=font(SANS, 11), fill=MUTED, anchor="ma")
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, optimize=True, compress_level=9)
    return out


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
