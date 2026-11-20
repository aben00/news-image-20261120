#!/usr/bin/env python3
"""Draw "The World Today" — a one-page newspaper front page summing up
Friday 20 November 2026, as a 1024x1024 PNG. Round 2: 36 verified stories,
12 illustrations and a pinned world map.

Deterministic: fixed random seed, no clock, no network, no file reads
beyond the system fonts. Run: python3 draw.py <output.png>

Every story happened, or was first reported, on Friday 20 November 2026.
The 12 numbered illustrations are pinned on the world map by the same
numbers (1-3 lead stories, 4-12 illustrated briefs).
"""

import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SEED = 20261120

PAPER = (248, 244, 233)
INK = (26, 26, 26)
RED = (176, 30, 30)
BLUE = (31, 58, 95)
GREY = (90, 86, 76)
SEA = (186, 212, 226)
LAND = (201, 190, 152)
LAND_LINE = (148, 138, 108)


def pick_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def serif_b(size):
    return pick_font(["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"], size)


def serif(size):
    return pick_font(["/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
                      "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"], size)


def sans(size):
    return pick_font(["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"], size)


def sans_b(size):
    return pick_font(["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"], size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star(d, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- leads

def draw_kyiv(d, x, y, w, h, rng):
    """Night sky over Kyiv: skyline, missile trails, bursts."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for _ in range(26):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.55))
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 220, 200))
    d.ellipse([x + w - 52, y + 12, x + w - 22, y + 42], fill=(238, 232, 200))
    base = y + h
    bx = x
    while bx < x + w:
        bw = rng.randint(22, 44)
        bh = rng.randint(34, 80)
        bx2 = min(bx + bw, x + w - 1)
        d.rectangle([bx, base - bh, bx2, base], fill=(8, 12, 24))
        for _ in range(bh // 14):
            wx = min(bx + rng.randint(4, max(5, bw - 6)), x + w - 5)
            wy = base - bh + rng.randint(6, max(7, bh - 8))
            if rng.random() < 0.55:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 110))
        bx += bw + rng.randint(2, 8)
    for (sx, sy, ex, ey) in [
        (x + 28, y + 92, x + 148, y + 44),
        (x + 118, y + 94, x + 232, y + 50),
        (x + 205, y + 90, x + 296, y + 66),
    ]:
        mx, my = (sx + ex) / 2, min(sy, ey) - 26
        prev = None
        for i in range(25):
            t = i / 24
            px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t * t * ex
            py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * my + t * t * ey
            if prev is not None:
                d.line([prev, (px, py)], fill=(255, 196, 90), width=3)
            prev = (px, py)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 240, 180))
    star(d, x + 86, y + 72, 15, 6, 8, (255, 150, 40))
    star(d, x + 86, y + 72, 7, 3, 8, (255, 220, 120))
    star(d, x + 258, y + 78, 11, 5, 8, (255, 150, 40))
    star(d, x + 258, y + 78, 5, 2, 8, (255, 220, 120))


def draw_cyclone(d, x, y, w, h, rng):
    """Cyclone spiral over the Bay of Bengal coast."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 224))
    cx, cy = x + w // 2, y + h // 2 - 6
    for k in range(5):
        r = 10 + k * 9
        a0 = k * 0.9
        pts = []
        for i in range(41):
            a = a0 + i * 0.14
            rr = r + i * 0.3
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.92))
        d.line(pts, fill=(255, 255, 255), width=7 - k)
        d.line(pts, fill=(90, 130, 160), width=2)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(240, 244, 246))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(120, 150, 175))
    for _ in range(40):
        rx = x + rng.randint(0, w)
        ry = y + rng.randint(0, h - 36)
        d.line([(rx, ry), (rx - 5, ry + 13)], fill=(110, 140, 165), width=2)
    base = y + h
    d.rectangle([x, base - 30, x + w, base], fill=(222, 200, 150))
    d.rectangle([x, base - 30, x + w, base - 25], fill=(70, 120, 140))
    for hx in [x + 16, x + 74, x + 132, x + 198, x + 256]:
        d.rectangle([hx, base - 23, hx + 24, base - 5], fill=(176, 90, 60))
        d.polygon([(hx - 3, base - 23), (hx + 12, base - 32), (hx + 27, base - 23)],
                  fill=(120, 50, 40))
    px0, py0 = x + w - 32, base - 5
    d.line([(px0, py0), (px0 - 13, py0 - 27)], fill=(90, 70, 40), width=4)
    for ang in (-70, -40, -15, 10):
        a = math.radians(ang)
        d.line([(px0 - 13, py0 - 27),
                (px0 - 13 + 19 * math.cos(a), py0 - 27 + 11 * math.sin(a))],
               fill=(40, 110, 60), width=3)


def draw_markets(d, x, y, w, h, rng):
    """Plunging chart over an Asian city skyline."""
    d.rectangle([x, y, x + w, y + h], fill=(244, 238, 228))
    base = y + h
    bx = x
    while bx < x + w:
        bw = rng.randint(24, 40)
        bh = rng.randint(20, 46)
        bx2 = min(bx + bw, x + w - 1)
        d.rectangle([bx, base - bh, bx2, base], fill=(120, 118, 110))
        bx += bw + rng.randint(3, 9)
    for gy in range(y + 14, base - 36, 24):
        d.line([(x + 10, gy), (x + w - 10, gy)], fill=(222, 214, 200), width=1)
    for i in range(5):
        cw = 15
        ox = x + 138 + i * 31
        top = y + 22 + i * 12 + rng.randint(-4, 6)
        bot = top + rng.randint(14, 24)
        col = (176, 30, 30) if i != 3 else (40, 130, 70)
        d.line([(ox + cw // 2, top - 7), (ox + cw // 2, bot + 7)], fill=col, width=2)
        d.rectangle([ox, top, ox + cw, bot], fill=col)
    pts = [(x + 128, y + 36), (x + 176, y + 46), (x + 220, y + 58),
           (x + 258, y + 76), (x + 292, y + 92)]
    d.line(pts, fill=(176, 30, 30), width=5)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 15, ey - 2), (ex - 4, ey - 13)], fill=(176, 30, 30))
    for (px, py) in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(176, 30, 30))
    d.text((x + 34, y + 6), "-4.5%", font=sans_b(32), fill=(176, 30, 30))
    d.text((x + 14, y + 44), "NIKKEI 225", font=sans_b(12), fill=(26, 26, 26))


# ------------------------------------------------------- small illustrations

def draw_intercept(d, x, y, w, h, rng):
    """Houthi claim, 20 Nov: missiles rise over the desert, intercepts burst."""
    d.rectangle([x, y, x + w, y + h], fill=(40, 32, 58))
    for _ in range(14):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.5))
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 220, 200))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(194, 164, 110))
    d.polygon([(x, y + h - 12), (x + 20, y + h - 22), (x + 44, y + h - 12)],
              fill=(170, 140, 92))
    for (sx, sy, ex, ey) in [(x + 12, y + h - 14, x + 34, y + 22),
                             (x + 52, y + h - 14, x + 66, y + 16)]:
        mx, my = (sx + ex) / 2, min(sy, ey) - 8
        prev = None
        for i in range(13):
            t = i / 12
            px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t * t * ex
            py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * my + t * t * ey
            if prev is not None:
                d.line([prev, (px, py)], fill=(255, 196, 90), width=2)
            prev = (px, py)
        star(d, ex, ey, 9, 4, 8, (255, 150, 40))
        star(d, ex, ey, 4, 2, 8, (255, 220, 120))


def draw_index(d, x, y, w, h, rng):
    """Anthropic joins the big indexes: rising green bars and an AI chip."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 232))
    for i, bh in enumerate([14, 22, 18, 30, 38]):
        bx = x + 8 + i * 11
        d.rectangle([bx, y + h - 12 - bh, bx + 8, y + h - 12],
                    fill=(40, 130, 70))
    d.line([(x + 6, y + h - 26), (x + 66, y + h - 44)], fill=(40, 130, 70), width=3)
    d.polygon([(x + 66, y + h - 44), (x + 56, y + h - 44), (x + 64, y + h - 34)],
              fill=(40, 130, 70))
    cx, cy = x + w - 20, y + 16
    d.rectangle([cx - 10, cy - 10, cx + 10, cy + 10], fill=(31, 58, 95))
    d.text((cx, cy), "AI", font=sans_b(10), fill=(255, 255, 255), anchor="mm")


def draw_talks(d, x, y, w, h, rng):
    """Europe ready for talks: a table with the EU flag and a white flag."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 215))
    d.line([(x + 14, y + 8), (x + 14, y + h - 20)], fill=(90, 80, 60), width=2)
    d.line([(x + 52, y + 8), (x + 52, y + h - 20)], fill=(90, 80, 60), width=2)
    d.rectangle([x + 15, y + 10, x + 37, y + 30], fill=(31, 58, 95))
    for k in range(6):
        a = 2 * math.pi * k / 6 - math.pi / 2
        star(d, x + 26 + 7 * math.cos(a), y + 20 + 7 * math.sin(a),
             2, 1, 5, (255, 215, 0))
    d.rectangle([x + 53, y + 10, x + 73, y + 30], fill=(255, 255, 255),
                outline=(150, 150, 150))
    d.rectangle([x + 6, y + h - 20, x + w - 6, y + h - 14], fill=(150, 110, 70))
    d.rectangle([x + 12, y + h - 14, x + 18, y + h - 4], fill=(120, 85, 50))
    d.rectangle([x + w - 18, y + h - 14, x + w - 12, y + h - 4], fill=(120, 85, 50))
    d.ellipse([x + 34, y + h - 34, x + 42, y + h - 26], fill=(232, 190, 150))
    d.ellipse([x + 34, y + h - 34, x + 42, y + h - 30], fill=(60, 50, 40))


def draw_crowd(d, x, y, w, h, rng):
    """13,000 march in Tokyo: crowd heads and placards."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 205))
    for (px, py, col) in [(x + 12, y + 16, (176, 30, 30)), (x + 40, y + 10, (31, 58, 95)),
                          (x + 64, y + 18, (200, 120, 40))]:
        d.rectangle([px, py, px + 16, py + 12], fill=col)
        d.line([(px + 8, py + 12), (px + 8, py + 26)], fill=(90, 80, 60), width=2)
    for i in range(7):
        hx = x + 4 + i * 11
        hy = y + h - 26 + (i % 2) * 4
        d.ellipse([hx, hy, hx + 9, hy + 9], fill=(232, 190, 150))
        d.ellipse([hx, hy, hx + 9, hy + 4], fill=(40, 32, 26))
        d.rectangle([hx - 1, hy + 10, hx + 10, y + h], fill=(90, 100, 130))
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(120, 110, 95))


def draw_boat(d, x, y, w, h, rng):
    """Capsized migrant boat off Senegal: hull, waves, rescue light."""
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 205))
    d.ellipse([x + w - 20, y + 6, x + w - 8, y + 18], fill=(255, 244, 190))
    for wy in (y + 26, y + 40, y + 54):
        for wx in range(x + 2, x + w - 10, 16):
            d.arc([wx, wy, wx + 14, wy + 10], 180, 360, fill=(255, 255, 255), width=2)
    d.polygon([(x + 14, y + 44), (x + 62, y + 44), (x + 56, y + 34),
               (x + 22, y + 34)], fill=(120, 80, 50))
    d.polygon([(x + 14, y + 44), (x + 62, y + 44), (x + 58, y + 50),
               (x + 18, y + 50)], fill=(90, 55, 35))
    d.ellipse([x + 30, y + 28, x + 36, y + 34], fill=(232, 190, 150))
    d.ellipse([x + 46, y + 30, x + 52, y + 36], fill=(200, 160, 120))


def draw_eu_coins(d, x, y, w, h, rng):
    """EU stars and gold coins: the 45-billion-euro loan for Ukraine."""
    d.rectangle([x, y, x + w, y + h], fill=(31, 58, 95))
    cx, cy = x + 22, y + 24
    for k in range(8):
        a = 2 * math.pi * k / 8 - math.pi / 2
        star(d, cx + 15 * math.cos(a), cy + 15 * math.sin(a), 4, 2, 5, (255, 215, 0))
    for i, (cx2, cw) in enumerate([(x + 52, 16), (x + 56, 20), (x + 48, 14)]):
        cy2 = y + h - 12 - i * 9
        d.ellipse([cx2, cy2 - cw // 2, cx2 + cw, cy2 + cw // 2], fill=(255, 200, 60))
        d.ellipse([cx2, cy2 - cw // 2, cx2 + cw, cy2 + cw // 2],
                  outline=(180, 130, 20), width=1)


def draw_flags(d, x, y, w, h, rng):
    """Paris meeting: French tricolore and US stars and stripes."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 215))
    d.line([(x + 14, y + 6), (x + 14, y + h - 6)], fill=(90, 80, 60), width=2)
    d.line([(x + 52, y + 6), (x + 52, y + h - 6)], fill=(90, 80, 60), width=2)
    fx = x + 15
    for i, col in enumerate([(31, 58, 140), (255, 255, 255), (200, 40, 40)]):
        d.rectangle([fx + i * 9, y + 8, fx + i * 9 + 9, y + 30], fill=col)
    ux = x + 53
    for i in range(4):
        col = (200, 40, 40) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([ux, y + 8 + i * 6, ux + 22, y + 14 + i * 6], fill=col)
    d.rectangle([ux, y + 8, ux + 10, y + 20], fill=(31, 58, 95))
    for (sx, sy) in [(ux + 3, y + 11), (ux + 7, y + 15), (ux + 3, y + 18)]:
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(150, 140, 120))


def draw_cricket(d, x, y, w, h, rng):
    """Wellington Test: bat, ball and stumps on a green pitch."""
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 90))
    d.rectangle([x + 24, y + 6, x + 54, y + h - 6], fill=(210, 190, 150))
    for sx in (x + 30, x + 35, x + 40):
        d.line([(sx, y + 12), (sx, y + 24)], fill=(240, 210, 120), width=3)
    d.line([(x + 28, y + 11), (x + 43, y + 11)], fill=(240, 210, 120), width=2)
    d.line([(x + 58, y + 20), (x + 70, y + 44)], fill=(200, 170, 120), width=5)
    d.line([(x + 58, y + 20), (x + 64, y + 10)], fill=(120, 80, 40), width=3)
    d.ellipse([x + 60, y + 46, x + 70, y + 56], fill=(176, 30, 30))
    d.arc([x + 60, y + 46, x + 70, y + 56], 20, 160, fill=(255, 255, 255), width=1)
    d.text((x + 8, y + h - 16), "113*", font=sans_b(13), fill=(255, 255, 255))


def draw_baseball(d, x, y, w, h, rng):
    """Pete Rose pardoned: baseball, bat and diamond."""
    d.rectangle([x, y, x + w, y + h], fill=(140, 180, 110))
    d.polygon([(x + w // 2, y + 10), (x + w - 10, y + h - 14),
               (x + w // 2, y + h - 6), (x + 10, y + h - 14)], fill=(210, 190, 150))
    d.line([(x + w // 2, y + 10), (x + w // 2, y + h - 6)], fill=(255, 255, 255), width=1)
    d.line([(x + 10, y + h - 14), (x + w - 10, y + h - 14)], fill=(255, 255, 255), width=1)
    bx, by = x + 16, y + 12
    d.line([(bx, by), (bx + 26, by + 30)], fill=(200, 170, 120), width=5)
    cx, cy = x + w - 26, y + 16
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 255, 255))
    d.arc([cx - 11, cy - 11, cx + 11, cy + 11], 300, 60, fill=(176, 30, 30), width=2)
    d.arc([cx - 11, cy - 11, cx + 11, cy + 11], 120, 240, fill=(176, 30, 30), width=2)


# ------------------------------------------------------------------- data

LEADS = [
    {
        "num": 1, "kicker": "UKRAINE  ·  WAR",
        "headline": "MISSILES OVER KYIV",
        "body": ("Russia fires a wave of ballistic missiles at the capital in the "
                 "early hours. Air-raid alerts sound from 01:19; about a dozen "
                 "missiles reported."),
        "draw": draw_kyiv,
    },
    {
        "num": 2, "kicker": "INDIA  ·  WEATHER",
        "headline": "CYCLONE AKVAN HITS THE COAST",
        "body": ("Severe Cyclone Akvan crosses the Odisha-Andhra coast by noon, "
                 "with winds of 90-100 kmph. About 300,000 people evacuated; "
                 "69 trains cancelled."),
        "draw": draw_cyclone,
    },
    {
        "num": 3, "kicker": "MARKETS  ·  ASIA",
        "headline": "ASIAN STOCKS PLUNGE",
        "body": ("The Nikkei falls 4.5% to below 57,000 and the Kospi 4.7% as the "
                 "AI selloff spreads. SoftBank drops 14%; MSCI Asia-Pacific "
                 "falls for a seventh session."),
        "draw": draw_markets,
    },
]

MINIS = [
    {"num": 4, "kicker": "MIDEAST", "headline": "HOUTHIS CLAIM 4 SAUDI STRIKES",
     "body": "Houthis claim strikes on four Saudi targets; five missiles downed.",
     "draw": draw_intercept},
    {"num": 5, "kicker": "MARKETS", "headline": "ANTHROPIC JOINS TOP INDEXES",
     "body": "Anthropic joins MSCI and FTSE global indexes after its record IPO.",
     "draw": draw_index},
    {"num": 6, "kicker": "EUROPE", "headline": "EUROPE READY FOR TALKS",
     "body": "Europe is ready for talks with Russia on ending the war, leaders say.",
     "draw": draw_talks},
    {"num": 7, "kicker": "JAPAN", "headline": "13,000 MARCH IN TOKYO",
     "body": "Thousands protest in Tokyo against the Takaichi government's policies.",
     "draw": draw_crowd},
    {"num": 8, "kicker": "AFRICA", "headline": "SENEGAL SEARCH RESUMES",
     "body": "Four bodies recovered off Yenne; search resumes for dozens missing.",
     "draw": draw_boat},
    {"num": 9, "kicker": "EUROPE", "headline": "EU PLANS €45BN FOR UKRAINE",
     "body": "The EU Commission proposes a €45 billion joint-debt loan to fund Kyiv.",
     "draw": draw_eu_coins},
    {"num": 10, "kicker": "FRANCE", "headline": "HARRIS MEETS MACRON",
     "body": "Kamala Harris meets Emmanuel Macron in Paris amid 2028 speculation.",
     "draw": draw_flags},
    {"num": 11, "kicker": "SPORT", "headline": "NICHOLLS TONS UP",
     "body": "Henry Nicholls hits an unbeaten 113 for New Zealand against India.",
     "draw": draw_cricket},
    {"num": 12, "kicker": "WASHINGTON", "headline": "PETE ROSE PARDONED",
     "body": "Trump posthumously pardons US baseball legend Pete Rose.",
     "draw": draw_baseball},
]

BRIEFS = [
    ("UKRAINE", "A projectile lands near the Dutch embassy in Kyiv, causing minor damage; the Dutch summon Russia's ambassador."),
    ("MARKETS", "SK Hynix and Samsung each fall more than 5% in Seoul; Advantest and SoftBank lead Tokyo's declines."),
    ("RUSSIA", "Three killed in a drone attack on the Saratov region."),
    ("MARKETS", "Taiwan's dollar nears a 10-year low against the US dollar; the Indian rupee leads Asian gains."),
    ("GEORGIA", "A 3-year-old is rescued from rubble 8 hours after a Tbilisi gas explosion."),
    ("LEBANON", "The US sanctions Hezbollah-linked charities and gold traders."),
    ("VENEZUELA", "Venezuela signs a military deal with the US less than a year after Maduro's removal."),
    ("WASHINGTON", "The White House taps Kirsten Davies as cyber chief after widespread outages."),
    ("TECH", "California targets Nvidia in a China AI chip probe."),
    ("INDIA", "GIFT Nifty points to a gap-down start for Indian markets."),
    ("YEMEN", "Yemen's parliament passes a law designating the Houthis a terrorist organisation."),
    ("ENERGY", "IEA calls the Mideast conflict the biggest energy security threat in history."),
    ("TECH", "IEA: data-centre power use could double by 2030, straining grids."),
    ("WASHINGTON", "Congress is back facing a Dec 11 deadline to fund the government or trigger a partial shutdown."),
    ("CHILDREN", "Nearly a quarter of the world's children live in conflict zones, Save the Children says."),
    ("INDIA", "Modi hails India's growth at the FICCI centenary convention in New Delhi."),
    ("BANGLADESH", "A fire is reported at Muhammad Yunus's ancestral home in Chattogram."),
    ("EDUCATION", "The NTA publishes the UGC NET December 2026 exam schedule."),
    ("AUSTRALIA", "A man is charged with terrorism offences after a Sydney raid."),
    ("TAIWAN", "New short-selling curbs take effect: stocks down 3.5% or more cannot be shorted below the previous close."),
    ("CLIMATE", "COP31 closes today in Antalya; the final draft drops fossil fuels and the $120bn adaptation target."),
    ("WASHINGTON", "Trump holds a noon White House news conference after his China trip."),
    ("SPORT", "ATP Finals, Turin: Alcaraz v Cobolli at 2pm CET; Medvedev v Tiafoe winner-takes-all."),
    ("MARKETS", "US monthly options expire today as Wall Street reels from a sharp tech reversal."),
]

# --------------------------------------------------------------------- map

# Rough continent outlines as (lon, lat) points, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73),
     (-65, 60), (-55, 47), (-60, 45), (-70, 42), (-75, 35), (-80, 26),
     (-85, 30), (-90, 21), (-95, 16), (-100, 18), (-105, 20), (-110, 24),
     (-115, 30), (-125, 40), (-125, 48), (-135, 58), (-150, 60), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-25, 70), (-40, 76), (-58, 76)],
    [(-80, 10), (-75, 12), (-65, 10), (-60, 5), (-52, 5), (-50, 0),
     (-45, -5), (-38, -8), (-35, -10), (-40, -20), (-48, -28), (-55, -35),
     (-65, -40), (-68, -50), (-70, -55), (-73, -45), (-73, -30), (-75, -18),
     (-80, -8), (-80, 0), (-80, 8)],
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 11), (51, 10), (45, 0), (40, -10),
     (35, -18), (30, -28), (20, -35), (15, -30), (12, -18), (10, -5),
     (8, 4), (-8, 5), (-15, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (5, 53), (8, 57),
     (10, 59), (5, 60), (5, 62), (12, 65), (18, 69), (25, 71), (30, 70),
     (40, 68), (50, 69), (60, 70), (70, 72), (80, 73), (90, 75), (100, 76),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 45),
     (142, 40), (135, 35), (130, 33), (127, 35), (122, 38), (120, 32),
     (115, 25), (110, 20), (108, 12), (105, 8), (100, 7), (98, 10),
     (95, 16), (92, 21), (88, 22), (85, 19), (80, 13), (77, 8), (75, 12),
     (72, 20), (68, 23), (65, 25), (60, 25), (57, 26), (54, 26), (52, 28),
     (50, 29), (48, 30), (44, 29), (40, 32), (36, 36), (30, 36), (26, 38),
     (22, 37), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37),
     (-6, 36), (-9, 37)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (141, 41), (140, 44), (142, 44), (144, 42), (141, 39)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12),
     (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (174, -41),
     (172, -43)],
]

# (number, lon, lat, badge dx, badge dy) — numbers match the 12 illustrations.
PINS = [
    (1, 30.5, 50.4, 12, -13),
    (2, 86.0, 19.8, 11, 6),
    (3, 139.7, 35.7, 11, -13),
    (4, 46.7, 24.7, 12, -11),
    (5, -74.0, 40.7, 11, -13),
    (6, 13.4, 52.5, 12, -12),
    (7, 139.7, 35.7, 11, 11),
    (8, -17.2, 14.7, -15, 11),
    (9, 4.35, 50.85, 9, -16),
    (10, 2.35, 48.85, -20, 3),
    (11, 174.8, -41.3, -17, -11),
    (12, -84.5, 39.1, 11, -13),
]


def draw_map(d, x, y, w, h):
    """Simplified world map with numbered pins for the 12 illustrations."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)

    def px(lon):
        return x + (lon + 180.0) / 360.0 * w

    def py(lat):
        return y + (78.0 - lat) / 136.0 * h

    for lon in range(-150, 181, 30):
        d.line([(px(lon), y), (px(lon), y + h)], fill=(205, 224, 233), width=1)
    for lat in (-30, 0, 30, 60):
        d.line([(x, py(lat)), (x + w, py(lat))], fill=(205, 224, 233), width=1)
    for poly in CONTINENTS:
        pts = [(px(lon), py(lat)) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    f_pin = sans_b(9)
    for num, lon, lat, dx, dy in PINS:
        cx, cy = px(lon), py(lat)
        bx, by = cx + dx, cy + dy
        d.line([(cx, cy), (bx, by)], fill=INK, width=1)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED, outline=(255, 255, 255))
        d.text((bx, by), str(num), font=f_pin, fill=(255, 255, 255), anchor="mm")


# -------------------------------------------------------------------- page

def main(out_path):
    rng = random.Random(SEED)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=1)

    # ---- masthead ----
    d.text((W // 2, 20), "THE WORLD TODAY", font=serif_b(56), fill=INK, anchor="ma")
    d.line([(30, 98), (W - 30, 98)], fill=INK, width=2)

    # ---- date band ----
    d.rectangle([30, 106, W - 30, 142], fill=RED)
    d.text((W // 2, 112), "FRIDAY  ·  20 NOVEMBER  ·  2026",
           font=sans_b(26), fill=(255, 255, 255), anchor="ma")

    # ---- standfirst ----
    d.text((W // 2, 150),
           "Missiles over Kyiv  ·  Cyclone Akvan hits India  ·  Asian stocks plunge",
           font=serif(16), fill=INK, anchor="ma")
    d.line([(30, 172), (W - 30, 172)], fill=INK, width=1)

    # ---- three lead tiles ----
    tile_w, tile_h = 312, 216
    tile_y = 180
    for i, tile in enumerate(LEADS):
        tx = 24 + i * (tile_w + 20)
        d.rectangle([tx, tile_y, tx + tile_w, tile_y + tile_h], outline=INK, width=2)
        tile["draw"](d, tx + 1, tile_y + 1, tile_w - 1, 100, rng)
        d.line([(tx, tile_y + 101), (tx + tile_w, tile_y + 101)], fill=INK, width=1)
        # number badge on the art, top left
        d.ellipse([tx + 8, tile_y + 8, tx + 26, tile_y + 26], fill=RED,
                  outline=(255, 255, 255))
        d.text((tx + 17, tile_y + 17), str(tile["num"]), font=sans_b(11),
               fill=(255, 255, 255), anchor="mm")
        d.text((tx + 10, tile_y + 108), tile["kicker"], font=sans_b(12), fill=RED)
        head_lines = wrap(d, tile["headline"], serif_b(19), tile_w - 20)
        hy = tile_y + 127
        for ln in head_lines:
            d.text((tx + 10, hy), ln, font=serif_b(19), fill=INK)
            hy += 21
        body_lines = wrap(d, tile["body"], sans(11), tile_w - 20)
        by = hy + 3
        for ln in body_lines[:3]:
            d.text((tx + 10, by), ln, font=sans(11), fill=INK)
            by += 13

    # ---- world map ----
    d.text((30, 404), "WHERE IT HAPPENED — THE 12 ILLUSTRATED STORIES, PINNED",
           font=sans_b(15), fill=INK)
    d.text((W - 30, 404), "20 NOVEMBER 2026", font=sans_b(15), fill=RED, anchor="ra")
    draw_map(d, 24, 424, 976, 116)

    # ---- nine illustrated mini tiles ----
    d.text((30, 548), "MORE OF THE DAY — IN PICTURES", font=sans_b(15), fill=INK)
    mini_w, mini_h = 312, 68
    for i, tile in enumerate(MINIS):
        col, row = i % 3, i // 3
        tx = 24 + col * (mini_w + 20)
        ty = 568 + row * (mini_h + 6)
        d.rectangle([tx, ty, tx + mini_w, ty + mini_h], outline=INK, width=1)
        tile["draw"](d, tx + 1, ty + 1, 76, mini_h - 1, rng)
        d.ellipse([tx + 5, ty + 4, tx + 21, ty + 20], fill=RED,
                  outline=(255, 255, 255))
        d.text((tx + 13, ty + 12), str(tile["num"]), font=sans_b(10),
               fill=(255, 255, 255), anchor="mm")
        tx0 = tx + 84
        d.text((tx0, ty + 4), tile["kicker"], font=sans_b(10), fill=RED)
        head_lines = wrap(d, tile["headline"], sans_b(12), mini_w - 92)
        hy = ty + 18
        for ln in head_lines[:1]:
            d.text((tx0, hy), ln, font=sans_b(12), fill=INK)
            hy += 14
        body_lines = wrap(d, tile["body"], sans(10), mini_w - 92)
        by = hy + 1
        for ln in body_lines[:2]:
            d.text((tx0, by), ln, font=sans(10), fill=INK)
            by += 12

    # ---- brief index, 3 columns x 8 ----
    d.line([(30, 790), (W - 30, 790)], fill=INK, width=2)
    d.text((30, 796), "ALSO TODAY — 24 MORE STORIES", font=sans_b(15), fill=INK)
    d.text((W - 30, 796), "20 NOVEMBER 2026", font=sans_b(15), fill=RED, anchor="ra")
    d.line([(30, 816), (W - 30, 816)], fill=INK, width=1)
    col_w = 312
    col_x = [24, 356, 688]
    for i, (tag, text) in enumerate(BRIEFS):
        col, row = i % 3, i // 3
        cx = col_x[col]
        cy = 822 + row * 21
        prefix = tag + " — "
        pre_w = d.textlength(prefix, font=sans_b(10))
        first = wrap(d, text, sans(10), col_w - pre_w)
        lines = []
        if first:
            lines.append(first[0])
            rest = " ".join(first[1:])
            lines += wrap(d, rest, sans(10), col_w) if rest else []
        lines = lines[:2]
        ly = cy
        for j, ln in enumerate(lines):
            if j == 0:
                d.text((cx, ly), prefix, font=sans_b(10), fill=BLUE)
                d.text((cx + pre_w, ly), ln, font=sans(10), fill=INK)
            else:
                d.text((cx, ly), ln, font=sans(10), fill=INK)
            ly += 11

    # ---- footer ----
    d.line([(30, 994), (W - 30, 994)], fill=INK, width=1)
    d.text((W // 2, 998),
           "Sources: Reuters · BBC · AP · The Hindu · IMD · AFP · Le Monde · EIN Presswire · ATP  —  Every story happened, or was first reported, on Friday 20 November 2026.",
           font=sans(9), fill=GREY, anchor="ma")

    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png")
