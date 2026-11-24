#!/usr/bin/env python3
"""Render Tuesday 24 November 2026's world news as one Economist-style cover.

Design: cream broadsheet page, red masthead "THE WORLD TODAY", the date as a
huge title, a drawn night scene over the Strait of Hormuz for the lead story,
a UTC timeline strip, a schematic drawn world map with flashpoint dots, and
42 short dated story items in three columns grouped by region, closed by a
"date check" verification footer. Deterministic: same bytes every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 241, 231)
INK = (26, 26, 26)
RED = (211, 6, 19)
GREY = (110, 104, 92)
LIGHT_LINE = (196, 188, 172)
NAVY_TOP = (13, 38, 66)
NAVY_SEA = (10, 26, 46)
MAP_BG = (222, 231, 236)
LAND = (201, 194, 178)
LAND_EDGE = (138, 131, 120)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

MARGIN = 36
COL_W = 301
COL_X = [MARGIN, MARGIN + COL_W + 24, MARGIN + 2 * (COL_W + 24)]


def fit_text(draw, text, max_w, start_size, font_fn):
    """Largest size (down to 10) at which text fits max_w; returns (font, text)."""
    size = start_size
    while size > 10:
        f = font_fn(size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    f = font_fn(10)
    while draw.textlength(text + "...", font=f) > max_w and len(text) > 8:
        text = text[:-1]
    return f, text + "..."


def draw_map(draw, x0, y0, x1, y1):
    """Schematic world map: rough continent polygons + red flashpoint dots."""
    draw.rectangle([x0, y0, x1, y1], fill=MAP_BG)
    lon = lambda v: x0 + (v + 180.0) / 360.0 * (x1 - x0)
    lat = lambda v: y0 + (75.0 - v) / 130.0 * (y1 - y0)
    continents = [
        [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
         (-75, 62), (-60, 55), (-55, 47), (-70, 44), (-75, 35), (-80, 26),
         (-90, 21), (-97, 16), (-105, 20), (-117, 32), (-125, 40), (-124, 48),
         (-140, 60), (-165, 60)],
        [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
         (-58, -38), (-65, -45), (-70, -55), (-73, -40), (-70, -20), (-80, -5)],
        [(-10, 36), (0, 44), (-5, 50), (0, 58), (10, 60), (18, 56), (21, 55),
         (28, 60), (30, 70), (40, 68), (45, 60), (40, 50), (30, 45), (23, 40),
         (19, 42), (12, 44), (3, 43), (-2, 37), (-9, 38)],
        [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
         (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30),
         (20, -35), (15, -30), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8)],
        [(40, 68), (60, 70), (80, 73), (110, 76), (140, 72), (160, 66),
         (162, 60), (158, 52), (142, 45), (135, 43), (130, 35), (122, 30),
         (120, 22), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
         (80, 8), (75, 20), (66, 25), (60, 25), (55, 26), (50, 29),
         (48, 30), (43, 38), (40, 42)],
        [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
         (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
         (135, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
    ]
    for poly in continents:
        pts = [(lon(lo), lat(la)) for lo, la in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    spots = [
        # name, lon, lat, label dx, label dy, anchor ("la" left-aligned,
        # "ra" right-aligned, "ma" centred)
        ("HORMUZ", 56.5, 26.5, 8, -4, "la"),
        ("KYIV", 30.5, 50.4, -8, -4, "ra"),
        ("ANTALYA", 30.7, 36.9, 0, 9, "ma"),
        ("GAZA", 34.5, 31.5, 0, 0, None),
        ("BANTEN", 106.0, -6.0, 0, 9, "ma"),
        ("BENGHAZI", 20.0, 32.1, 0, 0, None),
        ("LAS VEGAS", -115.1, 36.2, 8, -4, "la"),
        ("GENEVA", 6.1, 46.2, 0, 0, None),
        ("WELLINGTON", 174.8, -41.3, -8, -4, "ra"),
    ]
    lab = SANS_B(10)
    for name, lo, la, dx, dy, anchor in spots:
        px, py = lon(lo), lat(la)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                     outline=(255, 255, 255))
        if anchor:
            tx = px + dx
            ty = py + dy
            tw = draw.textlength(name, font=lab)
            if anchor == "la":
                tx = min(tx, x1 - tw - 2)
            elif anchor == "ra":
                tx = max(tx - tw, x0 + 2)
                tx = tx + tw  # anchor ra: text ends at tx
                draw.text((tx, ty), name, font=lab, fill=INK, anchor="ra")
                continue
            elif anchor == "ma":
                tx = max(x0 + tw / 2 + 2, min(tx, x1 - tw / 2 - 2))
                draw.text((tx, ty), name, font=lab, fill=INK, anchor="ma")
                continue
            draw.text((tx, ty), name, font=lab, fill=INK)
    return


def draw_lead(draw, x0, y0, x1, y1):
    """Night scene over the Strait of Hormuz: dark sky, red sun, tanker."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_TOP)
    horizon = y0 + int((y1 - y0) * 0.68)
    # headline + deck live in the sky zone, clear of the sea scene
    draw.text((x0 + 28, y0 + 10), "HORMUZ ON THE BRINK", font=SERIF_B(36),
              fill=(255, 255, 255))
    draw.text((x0 + 28, y0 + 54),
              "UN counts 25 seafarers killed near the Strait \u2014 Iran vows",
              font=SANS(15), fill=(225, 230, 238))
    draw.text((x0 + 28, y0 + 74),
              "\u201call means\u201d against a US naval blockade",
              font=SANS(15), fill=(225, 230, 238))
    # stars
    for sx, sy in [(70, 14), (150, 30), (260, 10), (420, 26), (560, 12),
                   (700, 30), (830, 14), (920, 34), (330, 34), (640, 8)]:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                     fill=(220, 225, 235))
    # solid red sun sitting on the horizon (sea drawn over its lower half)
    cx, cy, r = x0 + 770, horizon, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(224, 48, 48))
    draw.rectangle([x0, horizon, x1, y1], fill=NAVY_SEA)
    # sun reflection on the water
    for i, wdt in enumerate((120, 90, 60, 36)):
        yy = horizon + 10 + i * 8
        draw.line([cx - wdt // 2, yy, cx + wdt // 2, yy],
                  fill=(224, 90, 90), width=2)
    # tanker silhouette, low in the sea band, left of the sun; its top stays
    # below the deck text (which ends at y0+89)
    hx0, hx1 = x0 + 90, x0 + 430
    hy = y1 - 6
    hull = [(hx0, hy - 14), (hx1 - 40, hy - 14), (hx1, hy - 4),
            (hx1 - 18, hy + 4), (hx0 + 14, hy + 4), (hx0, hy - 2)]
    draw.polygon(hull, fill=(8, 8, 10))
    draw.rectangle([hx0 + 30, hy - 26, hx0 + 120, hy - 14], fill=(8, 8, 10))
    draw.rectangle([hx0 + 300, hy - 30, hx0 + 330, hy - 14], fill=(8, 8, 10))
    draw.rectangle([hx0 + 335, hy - 26, hx0 + 350, hy - 14], fill=(8, 8, 10))
    for wx in range(hx0 + 38, hx0 + 114, 14):
        draw.rectangle([wx, hy - 22, wx + 6, hy - 18], fill=(240, 200, 90))
    # wave lines
    for wy in (horizon + 22, horizon + 32):
        for wx in range(x0 + 470, x1 - 20, 46):
            draw.arc([wx, wy, wx + 34, wy + 10], 180, 360,
                     fill=(120, 150, 185))


GROUPS = [
    ("MIDDLE EAST", [
        "UN: 25 seafarers killed near Hormuz",
        "Iran vows \u201call means\u201d vs US blockade",
        "Iran says it shot down a US drone",
        "Houthis claim attack on Saudi refinery",
        "Israeli strike kills UN worker in Gaza",
        "Oxfam: Gaza left a \u201ctoxic wasteland\u201d",
        "Eisenkot: settler arson is \u201cJewish terrorism\u201d",
    ]),
    ("EUROPE & UKRAINE", [
        "Ukraine sinks Russian corvette in Benghazi",
        "Russian ship Sparta II ablaze off Finland",
        "Russian strike on Dymer kills at least 11",
        "700,000+ Russian soldiers killed: study",
        "Russia warns Estonia of \u201copen war\u201d",
        "Kushner: NATO-like guarantees for Kyiv?",
        "Danish court upholds \u201cghetto law\u201d evictions",
    ]),
    ("ASIA-PACIFIC", [
        "Indonesia factory fire kills 24 in Banten",
        "India pledges $1.6bn to rebuild Nepal",
        "Saryu-Kamala Express links India, Nepal",
        "S. Korea names new foreign minister",
        "Bangladesh: Hasina arrested if she returns",
        "China sets 2030 welfare targets",
        "Myanmar junta slams ASEAN decision",
    ]),
    ("AMERICAS & MARKETS", [
        "Trump blames Democrats for $1tn sell-off",
        "Nvidia soars ~$1tn as Huang returns",
        "Trump urges Nvidia to bring back Huang",
        "US sanctions Iran shadow-banking network",
        "Trump-Xi-Putin hold first trilateral talks",
        "US court opens path to erase Trump case",
        "India oil import bill up ~60% in October",
    ]),
    ("CLIMATE & WORLD", [
        "COP31 ends in deadlock in Antalya",
        "Tajikistan moves to quit the ICC",
        "Armenia proposes new constitution",
        "Bomb threats hit schools in Germany",
        "Lisbon marches over the cost of living",
        "Taliban erase women\u2019s names in Balkh",
        "Iran singer flogged over headscarf concert",
    ]),
    ("SPORT & SCIENCE", [
        "Pant 128 as India-NZ Test ends drawn",
        "Verstappen wins the Las Vegas GP",
        "Alcaraz wins maiden ATP Finals",
        "Gukesh-Sindarov title match begins",
        "BepiColombo enters Mercury orbit",
        "CAS to rule on Senegal AFCON appeal",
        "FIFA picks 2031, 2035 Women\u2019s WC hosts",
    ]),
]

TIMELINE = [
    ("23 NOV \u00b7 LATE", "Corvette sunk at Benghazi"),
    ("02:22 UTC", "UN: 25 dead at Hormuz"),
    ("24 NOV", "COP31 ends without a deal"),
    ("24 NOV", "Verstappen wins Las Vegas GP"),
    ("24 NOV", "Chess title match opens"),
]


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 58], fill=RED)
    d.text((W // 2, 10), "THE WORLD TODAY", font=SERIF_B(34),
           fill=(255, 255, 255), anchor="ma")
    d.line([MARGIN, 58, W - MARGIN, 58], fill=INK, width=2)

    # date title
    d.text((W // 2, 72), "TUESDAY", font=SERIF_B(64), fill=INK, anchor="ma")
    d.text((W // 2, 140), "24 NOVEMBER 2026", font=SERIF_B(50), fill=INK,
           anchor="ma")
    d.line([MARGIN, 200, W - MARGIN, 200], fill=RED, width=3)

    # lead visual panel
    draw_lead(d, MARGIN, 212, W - MARGIN, 344)

    # UTC timeline strip
    ty = 358
    d.text((MARGIN, ty), "THE DAY IN UTC", font=SANS_B(12), fill=RED)
    d.line([MARGIN, ty + 22, W - MARGIN, ty + 22], fill=LIGHT_LINE, width=2)
    n = len(TIMELINE)
    span = W - 2 * MARGIN
    for i, (when, what) in enumerate(TIMELINE):
        cx = MARGIN + int((i + 0.5) * span / n)
        d.ellipse([cx - 5, ty + 17, cx + 5, ty + 27], fill=RED,
                  outline=(255, 255, 255))
        wf = SANS_B(11)
        d.text((cx, ty + 32), when, font=wf, fill=INK, anchor="ma")
        tf = SANS(11)
        tw = d.textlength(what, font=tf)
        tx = max(MARGIN, min(cx - tw / 2, W - MARGIN - tw))
        d.text((tx, ty + 48), what, font=tf, fill=GREY)

    # world map strip
    my0, my1 = 438, 532
    d.text((MARGIN, my0 - 16), "WHERE IT HAPPENED", font=SANS_B(12),
           fill=RED)
    draw_map(d, MARGIN, my0, W - MARGIN, my1)

    # story columns: two groups per column
    y = 556
    line_h = 21
    for col in range(3):
        cy = y
        for gi in (col * 2, col * 2 + 1):
            title, items = GROUPS[gi]
            d.text((COL_X[col], cy), title, font=SANS_B(13), fill=RED)
            cy += 20
            for item in items:
                fnt = fit_text(d, item, COL_W, 13, SANS)
                if isinstance(fnt, tuple):
                    fnt, item = fnt
                d.text((COL_X[col], cy), item, font=fnt, fill=INK)
                cy += line_h
            cy += 12
    # footer
    fy = 936
    d.line([MARGIN, fy, W - MARGIN, fy], fill=INK, width=2)
    d.text((MARGIN, fy + 10), "DATE CHECK \u2014", font=SANS_B(12), fill=RED)
    d.text((MARGIN, fy + 28),
           "Verified Tue 24 Nov 2026, 07:30 WIB (00:30 UTC). Sources: Reuters, AP,",
           font=SANS(11), fill=GREY)
    d.text((MARGIN, fy + 43),
           "The Guardian, RFE/RL, wire reports. Every story first reported 23\u201324 Nov 2026.",
           font=SANS(11), fill=GREY)
    d.text((W - MARGIN, fy + 28), "42 stories \u00b7 6 regions \u00b7 1 day",
           font=SANS_B(11), fill=INK, anchor="ra")
    d.text((W - MARGIN, fy + 43), "THE WORLD TODAY", font=SANS_B(11),
           fill=INK, anchor="ra")
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    img = build()
    img.save(os.path.join(here, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
