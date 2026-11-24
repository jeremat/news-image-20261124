"""Draw the 24 November 2026 front page (1024x1024) with PIL.

Deterministic: fixed text, fixed geometry, no time, no randomness, no
network. Run it here to produce entry.png; main.py only copies that file.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 230)
INK = (20, 20, 20)
MUTED = (58, 58, 58)
WHITE = (255, 255, 255)

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


def picto_sea(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(191, 227, 240))
    sea_y = y0 + (y1 - y0) * 0.55
    d.rectangle([x0, sea_y, x1, y1], fill=(31, 95, 139))
    for wx in range(x0 + 8, x1 - 20, 34):
        d.arc([wx, sea_y + 8, wx + 30, sea_y + 26], 180, 360, fill=WHITE, width=3)
    # sinking hull: bow up left, stern down right into the water
    hull = [
        (x0 + 55, sea_y - 26), (x0 + 250, sea_y - 6),
        (x0 + 250, sea_y + 12), (x0 + 150, sea_y + 16),
        (x0 + 55, sea_y + 12),
    ]
    d.polygon(hull, fill=(30, 30, 34))
    d.rectangle([x0 + 95, sea_y - 44, x0 + 130, sea_y - 26], fill=(30, 30, 34))
    d.rectangle([x0 + 140, sea_y - 38, x0 + 152, sea_y - 26], fill=(30, 30, 34))
    starburst(d, x0 + 285, sea_y - 2, 26, 12, 8, (255, 122, 26))
    starburst(d, x0 + 285, sea_y - 2, 14, 7, 8, (255, 214, 64))
    # seven sea drones in the sky
    for i, (dx, dy) in enumerate([(30, 12), (70, 6), (115, 14), (160, 8),
                                  (205, 14), (250, 6), (300, 12)]):
        d.ellipse([x0 + dx, y0 + dy, x0 + dx + 7, y0 + dy + 7], fill=(20, 20, 20))
        d.line([x0 + dx + 3, y0 + dy + 7, x0 + dx + 3, y0 + dy + 13],
               fill=(20, 20, 20), width=2)


def picto_satellite(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(14, 27, 51))
    # earth: a large blue disc rising from the bottom-left corner
    d.ellipse([x0 - 10, y1 - 55, x0 + 150, y1 + 105], fill=(46, 127, 194))
    d.ellipse([x0 + 25, y1 - 48, x0 + 75, y1 - 18], fill=(64, 160, 90))
    d.ellipse([x0 + 88, y1 - 38, x0 + 132, y1 - 10], fill=(64, 160, 90))
    # dashed orbit across the upper half
    for a in range(0, 360, 24):
        import math
        x = x0 + 270 + 165 * math.cos(math.radians(a))
        y = y0 + 46 + 30 * math.sin(math.radians(a))
        if x0 <= x <= x1 and y0 <= y <= y1:
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 255, 255))
    # satellite body + panels
    d.rectangle([x0 + 275, y0 + 28, x0 + 315, y0 + 52], fill=(200, 205, 212))
    d.rectangle([x0 + 235, y0 + 32, x0 + 273, y0 + 48], fill=(59, 110, 200))
    d.rectangle([x0 + 317, y0 + 32, x0 + 355, y0 + 48], fill=(59, 110, 200))
    d.line([x0 + 295, y0 + 52, x0 + 295, y0 + 60], fill=(200, 205, 212), width=3)
    # warning star
    starburst(d, x0 + 425, y0 + 22, 16, 7, 4, (255, 59, 48))


def picto_midterms(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(234, 240, 251))
    bar_y = y0 + 22
    bar_h = 36
    total_w = x1 - x0 - 24
    dem_w = int(total_w * 258 / 435)
    rep_w = int(total_w * 173 / 435)
    bx = x0 + 12
    d.rectangle([bx, bar_y, bx + dem_w, bar_y + bar_h], fill=(29, 78, 216))
    d.rectangle([bx + dem_w, bar_y, bx + dem_w + rep_w, bar_y + bar_h],
                fill=(180, 35, 24))
    d.rectangle([bx + dem_w + rep_w, bar_y, bx + total_w, bar_y + bar_h],
                fill=(148, 163, 184))
    f_big = font(SANS_B, 26)
    d.text((bx + 12, bar_y + 5), "258", font=f_big, fill=WHITE)
    d.text((bx + dem_w + 12, bar_y + 5), "173", font=f_big, fill=WHITE)
    f_small = font(SANS_B, 17)
    d.text((bx + 4, bar_y + bar_h + 8), "DEMOCRATS 258", font=f_small,
           fill=(29, 78, 216))
    d.text((bx + 200, bar_y + bar_h + 8), "REPUBLICANS 173", font=f_small,
           fill=(180, 35, 24))


def picto_cyber(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(230, 244, 242))
    shield(d, x0 + 110, y0 + 8, 110, 72, (29, 78, 216), (20, 20, 20))
    shield(d, x0 + 250, y0 + 8, 110, 72, (15, 118, 110), (20, 20, 20))
    f_plus = font(SANS_B, 34)
    d.text((x0 + 224, y0 + 22), "+", font=f_plus, fill=INK)
    f_check = font(SANS_B, 30)
    d.text((x0 + 148, y0 + 28), "✓", font=f_check, fill=WHITE)
    d.text((x0 + 288, y0 + 28), "✓", font=f_check, fill=WHITE)
    for cx, cy in [(x0 + 40, y0 + 20), (x0 + 400, y0 + 20),
                   (x0 + 40, y0 + 62), (x0 + 400, y0 + 62)]:
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(15, 118, 110))


def picto_cop31(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(234, 245, 236))
    cx, cy, r = x0 + 150, y0 + 44, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 127, 194))
    d.ellipse([cx - 22, cy - 18, cx + 2, cy + 4], fill=(64, 160, 90))
    d.ellipse([cx + 8, cy + 6, cx + 28, cy + 26], fill=(64, 160, 90))
    # red X over the deal: two thick bars
    d.line([x0 + 250, y0 + 8, x0 + 340, y0 + 78], fill=(180, 35, 24), width=10)
    d.line([x0 + 340, y0 + 8, x0 + 250, y0 + 78], fill=(180, 35, 24), width=10)
    f_small = font(SANS_B, 17)
    d.text((x0 + 380, y0 + 30), "NO", font=f_small, fill=(180, 35, 24))


def picto_iran(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(251, 239, 234))
    sea_y = y0 + (y1 - y0) * 0.6
    d.rectangle([x0, sea_y, x1, y1], fill=(31, 95, 139))
    # cliffs left and right, strait in the middle
    d.polygon([(x0, y0), (x0 + 70, y0), (x0 + 45, sea_y), (x0, sea_y)],
              fill=(120, 90, 70))
    d.polygon([(x1, y0), (x1 - 70, y0), (x1 - 45, sea_y), (x1, sea_y)],
              fill=(120, 90, 70))
    # tanker in the strait
    d.rectangle([x0 + 120, sea_y - 14, x0 + 350, sea_y + 14], fill=(30, 30, 34))
    for i, col in enumerate([(200, 60, 40), (230, 180, 40), (40, 120, 90)]):
        d.rectangle([x0 + 140 + i * 62, sea_y - 34, x0 + 194 + i * 62, sea_y - 14],
                    fill=col)
    d.rectangle([x0 + 330, sea_y - 40, x0 + 350, sea_y - 14], fill=(230, 230, 230))
    # blockade chain across the strait
    for lx in range(x0 + 80, x1 - 80, 26):
        d.ellipse([lx, sea_y - 52, lx + 14, sea_y - 38], outline=(180, 35, 24),
                  width=4)


PANELS = [
    dict(kicker="UKRAINE  •  LIBYA", color=(180, 35, 24),
         headline=[("SUNK 1,700 KM", 34, INK), ("FROM HOME", 34, INK)],
         picto=picto_sea,
         caption="Ukraine says 7 sea drones sank the corvette Merkury off "
                 "Benghazi and hit the Angara."),
    dict(kicker="SPACE  •  RUSSIA", color=(27, 42, 74),
         headline=[("A NUCLEAR", 34, INK), ("SATELLITE?", 34, INK)],
         picto=picto_satellite,
         caption="Reports say Russia built Sputnik-S, a nuclear-capable "
                 "satellite. The Kremlin denies it."),
    dict(kicker="USA  •  MIDTERMS", color=(29, 78, 216),
         headline=[("DEMOCRATS WIN", 34, INK), ("258 SEATS", 40, (29, 78, 216))],
         picto=picto_midterms,
         caption="Democrats take 258 House seats — their biggest majority "
                 "since 1992 — and 56 in the Senate."),
    dict(kicker="TECH  •  BUSINESS", color=(15, 118, 110),
         headline=[("$43.9 BILLION", 36, (15, 118, 110)),
                   ("CYBER MEGADEAL", 34, INK)],
         picto=picto_cyber,
         caption="CrowdStrike agrees to buy Zscaler in an all-stock deal, "
                 "the biggest cybersecurity buyout on record."),
    dict(kicker="CLIMATE  •  COP31", color=(21, 128, 61),
         headline=[("NO DEAL", 34, INK), ("IN ANTALYA", 34, INK)],
         picto=picto_cop31,
         caption="COP31 ends with no overall agreement after the longest "
                 "climate talks ever, two days over time."),
    dict(kicker="IRAN  •  GULF", color=(127, 29, 29),
         headline=[("BLOCKADE", 34, INK), ("STANDOFF", 34, INK)],
         picto=picto_iran,
         caption="The US naval blockade holds; Iran calls it an act of "
                 "aggression. Tehran says Hormuz could reopen."),
]


def draw_panel(img, d, panel, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 30], fill=panel["color"])
    d.text((x + 12, y + 4), panel["kicker"], font=font(SANS_B, 19), fill=WHITE)
    hy = y + 38
    for text, size, color in panel["headline"]:
        d.text((x + 12, hy), text, font=font(SERIF_B, size), fill=color)
        hy += size + 6
    # pictogram on its own layer so nothing can spill over the caption
    pw, ph = w - 20, 92
    layer = Image.new("RGB", (pw, ph), WHITE)
    ld = ImageDraw.Draw(layer)
    panel["picto"](ld, 0, 0, pw, ph)
    img.paste(layer, (x + 10, y + 116))
    cap_lines = wrap(panel["caption"], font(SANS, 18), w - 24, d)
    if len(cap_lines) > 2:
        print(f"WARNING: caption wraps to {len(cap_lines)} lines: {panel['kicker']}")
    cy = y + 212
    for line in cap_lines[:2]:
        d.text((x + 12, cy), line, font=font(SANS, 18), fill=MUTED)
        cy += 22


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 8, H - 8], outline=INK, width=3)
    d.text((W // 2, 12), "THE WORLD TODAY", font=font(SERIF_B, 80),
           fill=INK, anchor="ma")
    d.line([20, 108, W - 20, 108], fill=INK, width=3)
    d.rectangle([20, 118, W - 20, 164], fill=INK)
    d.text((W // 2, 124), "TUESDAY 24 NOVEMBER 2026",
           font=font(SANS_B, 36), fill=WHITE, anchor="ma")
    d.text((W // 2, 174),
           "War at sea, a nuclear satellite, a historic US vote, a $43.9bn "
           "deal, no climate deal, a Gulf blockade.",
           font=font(SANS, 19), fill=MUTED, anchor="ma")
    col_w = 486
    row_h = 262
    xs = [20, 518]
    ys = [206, 478, 750]
    for i, panel in enumerate(PANELS):
        draw_panel(img, d, panel, xs[i % 2], ys[i // 2], col_w, row_h)
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, optimize=True, compress_level=9)
    return out


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
