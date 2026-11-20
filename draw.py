#!/usr/bin/env python3
"""Draw "The World Today" — a one-page newspaper front page summing up
Friday 20 November 2026, as a 1024x1024 PNG.

Deterministic: fixed random seed, no clock, no network, no file reads
beyond the system fonts. Run: python3 draw.py <output.png>

Stories are the verified events of Friday 20 November 2026:
- Kyiv hit by a wave of ballistic missiles in the early hours
- Severe Cyclone Akvan makes landfall on India's east coast
- Asian stocks plunge as the AI selloff spreads
plus a brief index of 17 further verified stories of the day.
"""

import math
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
LIGHT_GREY = (214, 208, 194)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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


def draw_kyiv(d, x, y, w, h, rng):
    """Night sky over Kyiv: skyline, missile trails, bursts."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for _ in range(26):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.55))
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 220, 200))
    # moon
    d.ellipse([x + w - 52, y + 14, x + w - 22, y + 44], fill=(238, 232, 200))
    # skyline silhouette
    base = y + h
    bx = x
    while bx < x + w:
        bw = rng.randint(22, 44)
        bh = rng.randint(38, 92)
        bx2 = min(bx + bw, x + w - 1)
        d.rectangle([bx, base - bh, bx2, base], fill=(8, 12, 24))
        for _ in range(bh // 14):
            wx = min(bx + rng.randint(4, max(5, bw - 6)), x + w - 5)
            wy = base - bh + rng.randint(6, max(7, bh - 8))
            if rng.random() < 0.55:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 110))
        bx += bw + rng.randint(2, 8)
    # missile trails: bright arcs with glowing heads
    for (sx, sy, ex, ey) in [
        (x + 30, y + 150, x + 150, y + 62),
        (x + 120, y + 158, x + 235, y + 70),
        (x + 210, y + 150, x + 300, y + 96),
    ]:
        mx, my = (sx + ex) / 2, min(sy, ey) - 34
        steps = 24
        prev = None
        for i in range(steps + 1):
            t = i / steps
            px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t * t * ex
            py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * my + t * t * ey
            if prev is not None:
                d.line([prev, (px, py)], fill=(255, 196, 90), width=3)
            prev = (px, py)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 240, 180))
        d.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(255, 255, 255))
    # explosion bursts above the skyline
    star(d, x + 88, y + 118, 16, 6, 8, (255, 150, 40))
    star(d, x + 88, y + 118, 8, 3, 8, (255, 220, 120))
    star(d, x + 262, y + 128, 12, 5, 8, (255, 150, 40))
    star(d, x + 262, y + 128, 6, 2, 8, (255, 220, 120))
    # searchlight beams (thin, pale)
    for bx0, ang in [(x + 60, -28), (x + 250, 24)]:
        d.line([(bx0, base), (bx0 + ang, y + 18)],
               fill=(255, 244, 190), width=2)


def draw_cyclone(d, x, y, w, h, rng):
    """Cyclone spiral over the Bay of Bengal coast."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 224))
    # spiral bands
    cx, cy = x + w // 2, y + h // 2 - 8
    for k in range(5):
        r = 18 + k * 17
        a0 = k * 0.9
        pts = []
        for i in range(41):
            a = a0 + i * 0.14
            rr = r + i * 0.55
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.92))
        d.line(pts, fill=(255, 255, 255), width=7 - k)
        d.line(pts, fill=(90, 130, 160), width=2)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(240, 244, 246))
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(120, 150, 175))
    # rain streaks
    for _ in range(46):
        rx = x + rng.randint(0, w)
        ry = y + rng.randint(0, h - 40)
        d.line([(rx, ry), (rx - 5, ry + 14)], fill=(110, 140, 165), width=2)
    # coast strip with shelters
    base = y + h
    d.rectangle([x, base - 34, x + w, base], fill=(222, 200, 150))
    d.rectangle([x, base - 34, x + w, base - 28], fill=(70, 120, 140))
    for hx in [x + 18, x + 78, x + 138, x + 205, x + 262]:
        d.rectangle([hx, base - 26, hx + 26, base - 6], fill=(176, 90, 60))
        d.polygon([(hx - 3, base - 26), (hx + 13, base - 36), (hx + 29, base - 26)],
                  fill=(120, 50, 40))
    # bending palm
    px0, py0 = x + w - 34, base - 6
    d.line([(px0, py0), (px0 - 14, py0 - 30)], fill=(90, 70, 40), width=4)
    for ang in (-70, -40, -15, 10):
        a = math.radians(ang)
        d.line([(px0 - 14, py0 - 30),
                (px0 - 14 + 20 * math.cos(a), py0 - 30 + 12 * math.sin(a))],
               fill=(40, 110, 60), width=3)


def draw_markets(d, x, y, w, h, rng):
    """Plunging chart over an Asian city skyline."""
    d.rectangle([x, y, x + w, y + h], fill=(244, 238, 228))
    # skyline at the bottom
    base = y + h
    bx = x
    while bx < x + w:
        bw = rng.randint(24, 40)
        bh = rng.randint(22, 52)
        bx2 = min(bx + bw, x + w - 1)
        d.rectangle([bx, base - bh, bx2, base], fill=(120, 118, 110))
        bx += bw + rng.randint(3, 9)
    # grid
    for gy in range(y + 16, base - 40, 26):
        d.line([(x + 10, gy), (x + w - 10, gy)], fill=(222, 214, 200), width=1)
    # candlesticks, mostly red, on the right half
    cx0 = x + 140
    for i in range(5):
        cw = 16
        ox = cx0 + i * 32
        top = y + 30 + i * 16 + rng.randint(-4, 6)
        bot = top + rng.randint(22, 40)
        col = (176, 30, 30) if i != 3 else (40, 130, 70)
        d.line([(ox + cw // 2, top - 8), (ox + cw // 2, bot + 8)], fill=col, width=2)
        d.rectangle([ox, top, ox + cw, bot], fill=col)
    # plunging line with arrow
    pts = [(x + 130, y + 44), (x + 180, y + 56), (x + 225, y + 72),
           (x + 262, y + 96), (x + 296, y + 130)]
    d.line(pts, fill=(176, 30, 30), width=5)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey - 2), (ex - 4, ey - 14)], fill=(176, 30, 30))
    for (px, py) in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(176, 30, 30))
    # big fall figure, top left, clear of the chart
    f_big = font(SANS_B, 34)
    d.text((x + 12, y + 8), "-4.5%", font=f_big, fill=(176, 30, 30))
    f_small = font(SANS_B, 13)
    d.text((x + 14, y + 50), "NIKKEI 225", font=f_small, fill=(26, 26, 26))


TILES = [
    {
        "kicker": "UKRAINE  ·  WAR",
        "headline": "MISSILES OVER KYIV",
        "body": ("Russia fires a wave of ballistic missiles at the capital in the "
                 "early hours. Air-raid alerts sound from 01:19; about a dozen "
                 "missiles are reported, aimed at bridges and energy sites."),
        "draw": draw_kyiv,
    },
    {
        "kicker": "INDIA  ·  WEATHER",
        "headline": "CYCLONE AKVAN HITS THE COAST",
        "body": ("Severe Cyclone Akvan crosses the Odisha-Andhra coast by noon, "
                 "with winds of 90-100 kmph. About 300,000 people are evacuated "
                 "and 69 trains cancelled."),
        "draw": draw_cyclone,
    },
    {
        "kicker": "MARKETS  ·  ASIA",
        "headline": "ASIAN STOCKS PLUNGE",
        "body": ("The Nikkei falls 4.5% to below 57,000 and the Kospi 4.7% as the "
                 "AI selloff spreads. SoftBank drops 14%. The MSCI Asia-Pacific "
                 "index falls for a seventh straight session."),
        "draw": draw_markets,
    },
]

BRIEFS = [
    ("UKRAINE", "A projectile lands near the Dutch embassy in Kyiv, causing minor damage; the Dutch summon Russia's ambassador."),
    ("MIDEAST", "Houthis claim strikes on four Saudi targets; the coalition says it downed five missiles and one cruise missile."),
    ("MARKETS", "Taiwan's new short-selling curbs take effect today: stocks down 3.5% or more cannot be shorted below the previous close."),
    ("CLIMATE", "COP31 closes today in Antalya; the final draft deal drops any mention of fossil fuels and the $120bn adaptation-finance target."),
    ("WASHINGTON", "Trump to hold a noon White House news conference today after his China trip, on Thailand and Philippines trade deals."),
    ("ENERGY", "Oil steady near $92.60 a barrel (Brent) in early Asian trade as Hormuz tanker fears offset oversupply worries."),
    ("SPORT", "ATP Finals, Turin: Alcaraz v Cobolli at 2pm CET; Medvedev v Tiafoe is winner-takes-all for the last semi-final place."),
    ("MARKETS", "Taiwan's dollar nears a 10-year low against the US dollar; the Indian rupee leads Asian gains."),
    ("TAIWAN", "New Taipei council candidate Chen Zhuyin is released on NT$500,000 bail over alleged foreign funding."),
    ("TAIWAN", "The Executive Yuan approves an inheritance-law change raising a spouse's share to two-thirds."),
    ("MARKETS", "SK Hynix and Samsung each fall more than 5% in Seoul; Advantest, SoftBank and Kioxia lead Tokyo's declines."),
    ("MARKETS", "US monthly options expire today as Wall Street reels from a sharp tech reversal."),
    ("WASHINGTON", "Congress is back facing a Dec 11 deadline to fund the government or trigger a partial shutdown."),
    ("SPORT", "Abu Dhabi T10: Arabian Aces v UAE Bulls in today's qualifier."),
    ("MARKETS", "Tokyo faces a three-day weekend with markets shut on Monday as investors sell first."),
    ("MARKETS", "Nikkei futures fell 3.63% in early trade; the 10-year JGB yield eased to 2.80%."),
    ("MARKETS", "Taiwan stocks have fallen 5,248 points over three trading days this week."),
    ("INDIA", "GIFT Nifty points to a gap-down start for Indian markets."),
]


def main(out_path):
    rng = random.Random(SEED)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=1)

    # ---- masthead ----
    f_mast = font(SERIF_B, 64)
    d.text((W // 2, 22), "THE WORLD TODAY", font=f_mast, fill=INK, anchor="ma")
    d.line([(30, 104), (W - 30, 104)], fill=INK, width=2)

    # ---- date band ----
    d.rectangle([30, 112, W - 30, 152], fill=RED)
    f_date = font(SANS_B, 28)
    d.text((W // 2, 118), "FRIDAY  ·  20 NOVEMBER  ·  2026",
           font=f_date, fill=(255, 255, 255), anchor="ma")

    # ---- standfirst ----
    f_stand = font(SERIF_I, 18)
    d.text((W // 2, 162),
           "Missiles over Kyiv  ·  Cyclone Akvan hits India's east coast  ·  Asian stocks plunge",
           font=f_stand, fill=INK, anchor="ma")
    d.line([(30, 190), (W - 30, 190)], fill=INK, width=1)

    # ---- three lead tiles ----
    tile_w, tile_h = 317, 316
    tile_y = 200
    gap = 12
    for i, tile in enumerate(TILES):
        tx = 24 + i * (tile_w + gap)
        d.rectangle([tx, tile_y, tx + tile_w, tile_y + tile_h],
                    outline=INK, width=2)
        tile["draw"](d, tx + 1, tile_y + 1, tile_w - 1, 158, rng)
        d.line([(tx, tile_y + 159), (tx + tile_w, tile_y + 159)],
               fill=INK, width=1)
        f_kick = font(SANS_B, 13)
        d.text((tx + 10, tile_y + 166), tile["kicker"], font=f_kick, fill=RED)
        f_head = font(SERIF_B, 21)
        head_lines = wrap(d, tile["headline"], f_head, tile_w - 20)
        hy = tile_y + 188
        for ln in head_lines:
            d.text((tx + 10, hy), ln, font=f_head, fill=INK)
            hy += 24
        f_body = font(SANS, 13)
        body_lines = wrap(d, tile["body"], f_body, tile_w - 20)
        by = hy + 4
        for ln in body_lines:
            d.text((tx + 10, by), ln, font=f_body, fill=INK)
            by += 17

    # ---- brief index ----
    d.line([(30, 528), (W - 30, 528)], fill=INK, width=2)
    f_sec = font(SANS_B, 17)
    d.text((30, 536), "ALSO TODAY — THE DAY IN BRIEF", font=f_sec, fill=INK)
    d.text((W - 30, 536), "20 NOVEMBER 2026", font=f_sec, fill=RED, anchor="ra")
    d.line([(30, 562), (W - 30, 562)], fill=INK, width=1)

    f_tag = font(SANS_B, 12)
    f_brief = font(SANS, 13)
    col_w = 472
    col_x = [30, 522]
    row_h = 46
    top = 570
    for i, (tag, text) in enumerate(BRIEFS):
        col = 0 if i < 9 else 1
        row = i if i < 9 else i - 9
        cx = col_x[col]
        cy = top + row * row_h
        # Inline tag: first wrapped line starts with the blue tag, so a
        # two-line item can never collide with the next row's tag.
        prefix = tag + " — "
        pre_w = d.textlength(prefix, font=f_tag)
        first = wrap(d, text, f_brief, col_w - pre_w)
        lines = []
        if first:
            lines.append(first[0])
            rest = " ".join(first[1:])
            lines += wrap(d, rest, f_brief, col_w) if rest else []
        lines = lines[:2]
        ly = cy
        for j, ln in enumerate(lines):
            if j == 0:
                d.text((cx, ly), prefix, font=f_tag, fill=BLUE)
                d.text((cx + pre_w, ly), ln, font=f_brief, fill=INK)
            else:
                d.text((cx, ly), ln, font=f_brief, fill=INK)
            ly += 15

    # ---- footer ----
    d.line([(30, 978), (W - 30, 978)], fill=INK, width=1)
    f_foot = font(SANS, 11)
    d.text((W // 2, 984),
           "Sources: Reuters · BBC · AP · The Hindu · IMD · AFP · UDN · TradingView · ATP",
           font=f_foot, fill=GREY, anchor="ma")
    d.text((W // 2, 998),
           "Every story happened, or was first reported, on Friday 20 November 2026.",
           font=f_foot, fill=GREY, anchor="ma")

    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png")
