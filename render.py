#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261125 (Builder A).

Picture-led magazine / world atlas of Wednesday 25 November 2026.
Deterministic: no randomness, no network, no external files.
Draws with PIL locally at build time only; the grader never runs this file.
"""
import random
from PIL import Image, ImageDraw, ImageFont

random.seed(20261125)

W, H = 1024, 1024
OUT = "entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_O = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None, max_lines=None):
    """Draw wrapped text; returns y just below the last line."""
    leading = leading or int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def centre(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


# ---------------------------------------------------------------- scenes
# Each scene draws a small flat illustration inside box (x, y, w, h).
# Kinds are simple pictograms, drawn from scratch with PIL primitives.

def scene(draw, x, y, w, h, kind, bg):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=bg)
    cx, cy = x + w // 2, y + h // 2
    s = min(w, h)
    ink = (255, 255, 255)
    dark = (11, 31, 58)
    if kind == "missile":
        # night sky, tower, missile streaks
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(16, 24, 48))
        for sx, sy in [(x + 200, y + 18), (x + w - 14, y + 12), (x + w // 2, y + 6)]:
            draw.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 200))
        draw.rectangle([x + w // 2 - 9, y + h - 34, x + w // 2 + 9, y + h - 4],
                       fill=(90, 110, 150))
        draw.polygon([(x + w // 2 - 9, y + h - 34), (x + w // 2 + 9, y + h - 34),
                      (x + w // 2, y + h - 46)], fill=(120, 140, 180))
        for r in range(5):
            draw.ellipse([x + w // 2 - 2 - r, y + h - 50 - r * 3,
                          x + w // 2 + 2 + r, y + h - 46 - r * 3],
                         outline=(255, 200, 80))
        draw.line([x + 6, y + 34, x + w - 20, y + h - 40], fill=(255, 180, 60),
                  width=3)
        draw.line([x + 14, y + 46, x + w - 8, y + h - 52], fill=(255, 120, 40),
                  width=2)
    elif kind == "ship":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(28, 80, 110))
        draw.rectangle([x + 8, y + h // 2 + 4, x + w - 8, y + h // 2 + 16],
                       fill=(40, 40, 44))
        draw.rectangle([x + w // 2 - 12, y + 12, x + w // 2 + 12, y + h // 2 + 4],
                       fill=(200, 200, 200))
        draw.line([x + w // 2, y + 6, x + w // 2, y + 12], fill=(255, 255, 255),
                  width=2)
        draw.polygon([(x + w // 2, y + 6), (x + w // 2 + 12, y + 10),
                      (x + w // 2, y + 13)], fill=(220, 60, 50))
        for i in range(3):
            draw.arc([x + 6 + i * 18, y + h - 14, x + 22 + i * 18, y + h - 2],
                     0, 180, fill=(255, 255, 255), width=2)
        draw.ellipse([x + w - 16, y + 8, x + w - 8, y + 16], fill=(255, 170, 40))
    elif kind == "rocket":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(10, 16, 40))
        for sx, sy in [(x + 8, y + 10), (x + w - 12, y + 8), (x + 12, y + h - 12),
                        (x + w - 16, y + h - 16)]:
            draw.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 220))
        draw.polygon([(cx - 7, y + 14), (cx + 7, y + 14), (cx + 9, y + h // 2),
                      (cx - 9, y + h // 2)], fill=(230, 230, 230))
        draw.polygon([(cx - 7, y + 14), (cx + 7, y + 14), (cx, y + 4)],
                     fill=(220, 60, 50))
        draw.ellipse([cx - 3, y + 22, cx + 3, y + 28], fill=(60, 140, 220))
        draw.polygon([(cx - 9, y + h // 2 - 4), (cx - 16, y + h // 2 + 8),
                      (cx - 9, y + h // 2 + 8)], fill=(220, 60, 50))
        draw.polygon([(cx + 9, y + h // 2 - 4), (cx + 16, y + h // 2 + 8),
                      (cx + 9, y + h // 2 + 8)], fill=(220, 60, 50))
        draw.polygon([(cx - 4, y + h // 2 + 8), (cx + 4, y + h // 2 + 8),
                      (cx, y + h - 4)], fill=(255, 190, 60))
    elif kind in ("chartdown", "chartup"):
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(245, 245, 240))
        col = (200, 40, 40) if kind == "chartdown" else (30, 140, 70)
        pts = [(x + 8, y + h - 18), (x + w // 3, y + h - 30),
               (x + 2 * w // 3, y + h - 22), (x + w - 8, y + 12)] \
            if kind == "chartdown" else \
            [(x + 8, y + h - 14), (x + w // 3, y + h - 26),
             (x + 2 * w // 3, y + h - 34), (x + w - 8, y + 10)]
        draw.line(pts, fill=col, width=4, joint="curve")
        if kind == "chartdown":
            draw.polygon([(x + w - 8, y + 12), (x + w - 16, y + 12),
                          (x + w - 8, y + 20)], fill=col)
        else:
            draw.polygon([(x + w - 8, y + 10), (x + w - 16, y + 10),
                          (x + w - 8, y + 2)], fill=col)
        draw.line([x + 6, y + h - 8, x + w - 6, y + h - 8], fill=(120, 120, 120),
                  width=2)
    elif kind == "chip":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(30, 30, 40))
        draw.rectangle([x + 14, y + 14, x + w - 14, y + h - 14],
                       fill=(20, 90, 120), outline=(120, 200, 230), width=2)
        draw.rectangle([x + w // 2 - 7, y + h // 2 - 7, x + w // 2 + 7,
                        y + h // 2 + 7], fill=(160, 220, 240))
        for i in range(4):
            px = x + 18 + i * 10
            draw.line([px, y + 6, px, y + 14], fill=(200, 200, 200), width=2)
            draw.line([px, y + h - 14, px, y + h - 6], fill=(200, 200, 200),
                      width=2)
    elif kind == "building":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(235, 238, 245))
        for i, bh in enumerate([h - 22, h - 34, h - 16]):
            bx = x + 8 + i * 18
            draw.rectangle([bx, y + h - bh, bx + 14, y + h - 6],
                           fill=(90, 110, 150))
            for wy in range(3):
                draw.rectangle([bx + 3, y + h - bh + 5 + wy * 8, bx + 11,
                                y + h - bh + 9 + wy * 8], fill=(255, 230, 140))
    elif kind == "ball":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(20, 110, 60))
        draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 255, 255),
                     outline=(40, 40, 40), width=2)
        draw.polygon([(cx, cy - 8), (cx + 8, cy - 2), (cx + 5, cy + 8),
                      (cx - 5, cy + 8), (cx - 8, cy - 2)], fill=(30, 30, 30))
        draw.line([cx, cy - 16, cx, cy - 8], fill=(30, 30, 30), width=2)
        draw.line([cx + 14, cy - 6, cx + 8, cy - 2], fill=(30, 30, 30), width=2)
        draw.line([cx + 14, cy + 8, cx + 5, cy + 8], fill=(30, 30, 30), width=2)
    elif kind == "factory":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(240, 235, 225))
        draw.rectangle([x + 8, y + h - 24, x + w - 8, y + h - 6],
                       fill=(120, 120, 125))
        draw.polygon([(x + 8, y + h - 24), (x + 18, y + h - 36),
                      (x + 28, y + h - 24)], fill=(90, 90, 95))
        draw.rectangle([x + w - 20, y + 10, x + w - 14, y + h - 24],
                       fill=(90, 90, 95))
        draw.ellipse([x + w - 22, y + 4, x + w - 12, y + 12], fill=(200, 200, 200))
        draw.rectangle([x + 12, y + h - 18, x + 20, y + h - 10],
                       fill=(255, 210, 90))
    elif kind == "satellite":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(12, 20, 44))
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))
        draw.rectangle([cx - 8, cy - 5, cx + 8, cy + 5], fill=(200, 200, 210))
        draw.rectangle([cx - 24, cy - 3, cx - 9, cy + 3], fill=(40, 90, 180))
        draw.rectangle([cx + 9, cy - 3, cx + 24, cy + 3], fill=(40, 90, 180))
        draw.line([cx + 4, cy - 10, cx + 12, cy - 18], fill=(255, 255, 255),
                  width=2)
        draw.ellipse([cx + 11, cy - 20, cx + 14, cy - 17], fill=(255, 200, 60))
    elif kind == "drone":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(225, 232, 238))
        draw.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=(60, 60, 70))
        for dx, dy in [(-18, -12), (18, -12), (-18, 12), (18, 12)]:
            draw.line([cx, cy, cx + dx, cy + dy], fill=(90, 90, 100), width=2)
            draw.ellipse([cx + dx - 6, cy + dy - 2, cx + dx + 6, cy + dy + 2],
                         outline=(60, 60, 70), width=2)
    elif kind == "court":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(238, 232, 220))
        draw.line([cx, y + 8, cx, y + h - 14], fill=(90, 70, 40), width=3)
        draw.line([cx - 16, y + 12, cx + 16, y + 12], fill=(90, 70, 40), width=3)
        draw.polygon([(cx - 16, y + 12), (cx - 10, y + 26), (cx - 22, y + 26)],
                     outline=(90, 70, 40), width=2)
        draw.polygon([(cx + 16, y + 12), (cx + 10, y + 26), (cx + 22, y + 26)],
                     outline=(90, 70, 40), width=2)
        draw.ellipse([cx - 14, y + h - 14, cx + 14, y + h - 6], fill=(90, 70, 40))
    elif kind == "oil":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(40, 40, 46))
        draw.polygon([(cx, y + 8), (cx + 14, y + 26), (cx + 14, y + h - 10),
                      (cx - 14, y + h - 10), (cx - 14, y + 26)], fill=(20, 20, 24),
                     outline=(255, 190, 60), width=2)
        draw.ellipse([cx - 5, y + h - 22, cx + 5, y + h - 12], fill=(255, 190, 60))
    elif kind == "coin":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(245, 240, 220))
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(240, 180, 40),
                     outline=(160, 110, 20), width=3)
        draw.text((cx - 6, cy - 12), "B", font=font(SANS_B, 22), fill=(120, 80, 10))
    elif kind == "store":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(235, 245, 235))
        draw.rectangle([x + 8, y + h - 26, x + w - 8, y + h - 6],
                       fill=(40, 120, 70))
        draw.polygon([(x + 6, y + h - 26), (x + w - 6, y + h - 26),
                      (x + w - 12, y + h - 38), (x + 12, y + h - 38)],
                     fill=(220, 60, 50))
        draw.rectangle([x + w // 2 - 6, y + h - 18, x + w // 2 + 6, y + h - 6],
                       fill=(255, 255, 255))
    elif kind == "globe":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(210, 230, 245))
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(70, 140, 200),
                     outline=(20, 60, 120), width=2)
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], outline=(20, 60, 120),
                     width=2)
        draw.arc([cx - 18, cy - 18, cx + 18, cy + 18], 200, 340,
                 fill=(30, 160, 80), width=4)
        draw.arc([cx - 10, cy - 18, cx + 10, cy + 18], 90, 270,
                 fill=(20, 60, 120), width=2)
        draw.line([cx - 18, cy, cx + 18, cy], fill=(20, 60, 120), width=2)
    elif kind == "flag":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(240, 240, 238))
        draw.line([x + 10, y + 6, x + 10, y + h - 6], fill=(80, 60, 40), width=3)
        draw.polygon([(x + 10, y + 8), (x + w - 10, y + 14), (x + 10, y + 22)],
                     fill=(200, 40, 40))
    elif kind == "plane":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(215, 232, 245))
        draw.polygon([(x + 8, cy), (x + w - 8, cy - 6), (x + w - 8, cy + 6)],
                     fill=(230, 230, 230), outline=(60, 60, 70))
        draw.polygon([(cx - 2, cy - 4), (cx + 8, cy - 16), (cx + 12, cy - 4)],
                     fill=(200, 200, 210))
        draw.polygon([(cx - 2, cy + 4), (cx + 8, cy + 16), (cx + 12, cy + 4)],
                     fill=(200, 200, 210))
    elif kind == "shield":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(238, 238, 245))
        draw.polygon([(cx - 16, y + 8), (cx + 16, y + 8), (cx + 16, y + 26),
                      (cx, y + h - 8), (cx - 16, y + 26)], fill=(40, 90, 160))
        draw.line([cx - 8, cy + 2, cx - 2, cy + 8, cx + 10, cy - 6],
                  fill=(255, 255, 255), width=3)
    elif kind == "vaccine":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(235, 245, 240))
        draw.line([cx - 12, cy + 16, cx + 12, cy - 16], fill=(120, 120, 130),
                  width=5)
        draw.rectangle([cx - 4, cy - 20, cx + 8, cy - 8], fill=(200, 60, 60))
        draw.line([cx + 12, cy - 16, cx + 18, cy - 22], fill=(120, 120, 130),
                  width=3)
    elif kind == "flame":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(250, 235, 220))
        draw.polygon([(cx, y + 8), (cx + 12, y + 26), (cx + 8, y + h - 10),
                      (cx - 8, y + h - 10), (cx - 12, y + 26)], fill=(240, 90, 30))
        draw.polygon([(cx, y + 24), (cx + 7, y + 34), (cx + 4, y + h - 12),
                      (cx - 4, y + h - 12), (cx - 7, y + 34)], fill=(255, 200, 60))
    elif kind == "music":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(240, 235, 250))
        draw.ellipse([cx - 12, cy + 6, cx - 2, cy + 14], fill=(40, 40, 50))
        draw.ellipse([cx + 6, cy + 2, cx + 16, cy + 10], fill=(40, 40, 50))
        draw.line([cx - 3, cy + 8, cx - 3, cy - 14], fill=(40, 40, 50), width=2)
        draw.line([cx + 15, cy + 4, cx + 15, cy - 18], fill=(40, 40, 50), width=2)
        draw.line([cx - 3, cy - 14, cx + 15, cy - 18], fill=(40, 40, 50), width=2)
    elif kind == "handshake":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(235, 240, 250))
        draw.polygon([(x + 8, cy + 6), (cx - 4, cy - 8), (cx + 10, cy - 8),
                      (x + w - 8, cy + 8), (cx + 6, cy + 16), (cx - 6, cy + 16)],
                     fill=(200, 170, 120), outline=(120, 90, 50))
        draw.line([cx - 10, cy - 2, cx + 10, cy + 8], fill=(120, 90, 50), width=2)
    elif kind == "screen":
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(30, 40, 60))
        draw.rectangle([x + 8, y + 8, x + w - 8, y + h - 16], fill=(120, 180, 230),
                       outline=(255, 255, 255), width=2)
        draw.line([x + 12, y + 16, x + w - 16, y + 16], fill=(255, 255, 255),
                  width=2)
        draw.line([x + 12, y + 24, x + w - 24, y + 24], fill=(200, 220, 240),
                  width=2)
        draw.line([cx - 8, y + h - 12, cx + 8, y + h - 12], fill=(255, 255, 255),
                  width=3)
    else:  # "dot" fallback: simple globe marker
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=bg)
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(200, 60, 50))


# ---------------------------------------------------------------- world map
# Rough continent outlines in (lon, lat); equirectangular projection.

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-135, 58), (-155, 58),
     (-168, 66)],
    # South America
    [(-79, 9), (-62, 11), (-52, 5), (-44, -3), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -54), (-73, -37), (-70, -18),
     (-77, -12), (-79, 9)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 58), (10, 62), (18, 69),
     (30, 70), (40, 68), (45, 60), (40, 50), (30, 46), (28, 41), (23, 36),
     (19, 40), (12, 44), (3, 42), (-2, 37), (-10, 36)],
    # Africa
    [(-17, 15), (-10, 31), (10, 37), (20, 32), (32, 31), (43, 12), (51, 11),
     (48, 0), (40, -10), (36, -18), (33, -26), (26, -34), (18, -35),
     (12, -18), (9, -1), (-8, 4), (-17, 15)],
    # Asia
    [(45, 60), (60, 69), (80, 73), (110, 76), (140, 72), (160, 66),
     (178, 65), (162, 60), (142, 50), (135, 43), (127, 40), (122, 31),
     (110, 21), (105, 10), (100, 8), (92, 16), (88, 22), (80, 13),
     (75, 8), (68, 23), (60, 25), (52, 28), (48, 30), (43, 39), (40, 42),
     (45, 60)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19), (150, -23),
     (153, -27), (150, -37), (140, -38), (130, -32), (124, -33), (115, -35),
     (114, -22)],
]


def draw_map(draw, x, y, w, h):
    """Atlas panel: ocean, continents, graticule, 13 labelled pins."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(214, 232, 242))
    # graticule
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360 * w
        draw.line([gx, y, gx, y + h], fill=(190, 214, 230), width=1)
    for lat in range(-60, 61, 30):
        gy = y + (78 - lat) / 136 * h
        draw.line([x, gy, x + w, gy], fill=(190, 214, 230), width=1)

    def proj(lon, lat):
        # crop latitude to 78..-58 so continents are not squashed flat
        return (x + (lon + 180) / 360 * w,
                y + (78 - lat) / 136 * h)

    for cont in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in cont]
        draw.polygon(pts, fill=(196, 196, 150), outline=(140, 140, 105))

    # pins: (label, lon, lat, label dx, label dy) — exactly 13
    pins = [
        ("NEW YORK", -74.0, 40.7, -78, -16),
        ("WASHINGTON", -77.0, 38.9, -96, 12),
        ("WARSAW", 21.0, 52.2, 8, -16),
        ("KYIV", 30.5, 50.5, -52, 8),
        ("GAZA", 34.5, 31.5, -40, 12),
        ("RIYADH", 46.7, 24.7, -8, -18),
        ("HORMUZ", 56.5, 26.5, 8, 6),
        ("TAIZ", 44.0, 13.6, -30, 14),
        ("SEOUL", 127.0, 37.5, 6, -16),
        ("TOKYO", 139.7, 35.7, 4, 12),
        ("SHANGHAI", 121.5, 31.2, -66, 10),
        ("CIKANDE", 106.3, -6.2, -58, 10),
        ("SYDNEY", 151.2, -33.9, -58, -14),
    ]
    lab_f = font(SANS_B, 11)
    for label, lon, lat, dx, dy in pins:
        px, py = proj(lon, lat)
        lx, ly = px + dx, py + dy
        tw = draw.textlength(label, font=lab_f)
        draw.line([px, py, lx + tw / 2, ly + 10], fill=(120, 60, 60), width=1)
        draw.rectangle([lx - 2, ly - 1, lx + tw + 3, ly + 12],
                       fill=(255, 255, 255), outline=(150, 150, 150))
        draw.text((lx, ly), label, font=lab_f, fill=(140, 20, 20))
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(200, 30, 30),
                     outline=(255, 255, 255), width=2)
    return len(pins)


# ---------------------------------------------------------------- content
# 34 stories, all dated 25 November 2026 (happened or first reported that day
# in some time zone). Evening events in the US/Europe are labelled in the
# DATE CHECK strip. Sources: Reuters, AP, UEFA, UN, BBC, company filings.

LEAD = ("MIDDLE EAST",
        "MISSILES OVER RIYADH",
        "Houthi missile strikes the PIF Tower in the Saudi capital; "
        "11 people hurt, among them 2 Indians, 2 Saudis, 3 Nepalis and "
        "4 Egyptians. The Houthis threaten Jeddah and every Saudi Red Sea "
        "port if Riyadh strikes Hodeidah. Attack on 24 Nov, reported 25 Nov.")

SECONDARY = [
    ("MIDDLE EAST",
     "MINES IN THE STRAIT OF HORMUZ",
     "Iran's navy claims mines hit two tankers in the world's busiest oil "
     "chokepoint. A claim of six tankers in 24 hours is unverified.",
     "ship"),
    ("SPACE",
     "CHINA LAUNCHES SHENZHOU-24",
     "Three astronauts lift off for Tiangong, among them Pakistan's "
     "Muhammad Zeeshan Ali — the first foreigner at China's station.",
     "rocket"),
]

# (region tag, headline, one line, scene kind) — 12 cards
GRID = [
    ("MIDDLE EAST", "US WEIGHS STRIKES ON IRAN",
     "Washington is considering strikes on senior Iranian figures, "
     "including Mojtaba Khamenei, reports say.", "missile"),
    ("MIDDLE EAST", "GAZA: HAMAS SECURITY CHIEF KILLED",
     "An Israeli strike kills Hamas internal security chief Naeem Abu "
     "Nahel, two months into the job, and seven others.", "shield"),
    ("MIDDLE EAST", "397 UNRWA STAFF DEAD",
     "A UNRWA worker is killed near a well in Jabalya. Gaza's toll "
     "reaches 74,746 since October 2023.", "flag"),
    ("EUROPE", "UKRAINE DRONE HITS RUSSIAN SHIP",
     "Zelenskyy confirms a drone struck a Russian cargo ship in the "
     "Gulf of Finland; 16 crew are evacuated.", "ship"),
    ("EUROPE", "RUSSIAN STRIKES KILL FOUR",
     "Strikes on Zaporizhzhia kill 2 and wound 20+; a missile on "
     "Kryvyi Rih kills 2 and wounds 60.", "flame"),
    ("EUROPE", "LEAK: 490,000 RUSSIAN WAR DEAD",
     "Leaked Russian records point to at least 490,000 war deaths, "
     "counted from death certificates.", "court"),
    ("AFRICA", "CHEAP DRONES RESHAPE SAHEL WAR",
     "Rebels in Mali, Burkina Faso and Niger fight with cheap FPV "
     "drones; JNIM has flown 187 attacks since 2023.", "drone"),
    ("SPACE", "NUCLEAR-ARMED SATELLITE FEAR",
     "Western intelligence warns Russia may launch a nuclear-armed "
     "satellite. NATO chief Rutte vows to defend space.", "satellite"),
    ("ASIA-PACIFIC", "ASIAN STOCKS PLUNGE",
     "KOSPI falls 6.16%, Taiwan 4.8%, Nikkei 2.8% in Wednesday's "
     "sell-off.", "chartdown"),
    ("NORTH AMERICA", "DOW TOPS 50,000 FIRST TIME",
     "The Dow closes at 50,018.70, up 0.85%, its first close above "
     "50,000. S&P 500 slips; Nasdaq falls 1.48%.", "chartup"),
    ("NORTH AMERICA", "DELL REVENUE DOUBLES",
     "Dell reports Q3 revenue of $54.94bn, up 103% year on year, "
     "with $22.0bn of AI server revenue.", "building"),
    ("EUROPE", "SANOFI BUYS INSMED FOR $41BN",
     "Sanofi agrees a $41bn all-cash deal at $175 a share, the "
     "biggest pharma deal of 2026. Insmed rises 14%.", "building"),
]

# One-line items for the ALSO strip — 15 more stories (total 30)
ALSO = [
    "Russian drones enter Polish airspace overnight.",
    "Amnesty urges ICC probe over Gaza reproductive health.",
    "Odesa: 80,000 homes without heat; Taiz kids miss jabs.",
    "Trump readies new tariffs after Section 301 probe.",
    "Nvidia slides 5.9% after Monday's 31.5% jump.",
    "Chip rout: Micron -11%, AMD -8.9%, Analog -17.4%.",
    "US data day: core PCE and Q3 GDP due 08:30 ET.",
    "Australia inflation 3.8%; RBA raised 125 bps in 2026.",
    "Oil: Brent $90.97; Bitcoin $59,258; Ether $1,661.",
    "US retail rallies: Dollar Tree +11.2%, Dick's +14.6%.",
    "Microsoft declares 'Code Red' after 24-hour outage.",
    "Champions League: Madrid 5-1 PSV; Arsenal 1-1 Dortmund.",
    "Miley Cyrus marries Maxx Morando (reported 25 Nov).",
    "Cikande factory fire toll rises to 26 in Indonesia.",
    "Myanmar landmine toll 1,891 — world's highest again.",
]

NUMBERS = [
    ("50,018.70", "Dow closes above 50,000, first time"),
    ("-6.16%", "KOSPI falls in Wednesday's sell-off"),
    ("$54.94bn", "Dell Q3 revenue, up 103% on year"),
    ("490,000+", "Russian war deaths in leaked records"),
    ("74,746", "Gaza death toll since October 2023"),
    ("26 dead", "Cikande factory fire, Indonesia"),
]

DATE_CHECK = [
    ("1. WHAT COUNTS AS 25 NOVEMBER: ",
     "events that happened, or were first reported, on Wednesday 25 "
     "November 2026 in any time zone on Earth."),
    ("2. EVENING IN THE WEST = WEDNESDAY IN ASIA: ",
     "Tuesday-night US closes and Tuesday's Champions League reached "
     "Wednesday's papers in Asia — dated as reported 25 Nov."),
    ("3. NOT 25 NOVEMBER EVENTS: ",
     "the Riyadh strike was 24 Nov (reported 25 Nov); Miley married 21 Nov "
     "(reported 25 Nov); Microsoft's outage was 12–13 Nov."),
]

NAVY = (11, 31, 58)
RED = (178, 34, 34)
GOLD = (212, 160, 40)
INK = (20, 20, 22)
PAPER = (250, 248, 240)



# ---------------------------------------------------------------- layout
NAVY = (11, 31, 58)
RED = (178, 34, 34)
GOLD = (212, 160, 40)
INK = (20, 20, 22)
PAPER = (250, 248, 240)


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (0-96) ------------------------------------------
    d.rectangle([0, 0, W, 95], fill=NAVY)
    d.rectangle([0, 93, W, 96], fill=RED)
    centre(d, W // 2, 6, "THE WORLD TODAY",
           font(SERIF, 24), (255, 255, 255))
    centre(d, W // 2, 34, "WEDNESDAY  25  NOVEMBER  2026",
           font(SERIF, 38), GOLD)
    centre(d, W // 2, 76,
           "One day — one picture — the news that mattered, from every region",
           font(SANS_O, 12), (200, 210, 225))

    # ---- atlas (100-238) ------------------------------------------
    d.rectangle([0, 100, W, 118], fill=NAVY)
    d.text((12, 102), "THE WORLD AT A GLANCE  ·  13 PLACES THAT MADE THE NEWS",
           font=font(SANS_B, 12), fill=(255, 255, 255))
    d.text((W - 12 - d.textlength("WED 25 NOV 2026", font=font(SANS_B, 12)),
            102), "WED 25 NOV 2026", font=font(SANS_B, 12), fill=GOLD)
    n_pins = draw_map(d, 0, 120, W, 118)

    # ---- lead (242-392) -------------------------------------------
    ly = 242
    d.rectangle([0, ly, W, ly + 2], fill=RED)
    tag_f = font(SANS_B, 11)
    scene(d, 12, ly + 10, 300, 140, "missile", (16, 24, 48))
    d.text((16, ly + 14), "LEAD STORY", font=tag_f, fill=(255, 255, 255))
    tx = 324
    d.text((tx, ly + 12), LEAD[0], font=tag_f, fill=RED)
    y = text_block(d, tx, ly + 30, LEAD[1], font(SERIF, 28), INK,
                   W - tx - 12, leading=32, max_lines=1)
    text_block(d, tx, y + 4, LEAD[2], font(SANS, 13), (40, 40, 44),
               W - tx - 12, leading=17, max_lines=5)

    # ---- secondary (396-452): two half-width cards -----------------
    sy = 396
    for i, (tag, head, line, kind) in enumerate(SECONDARY):
        cx0 = 12 + i * 504
        cw = 496
        d.rectangle([cx0, sy, cx0 + cw - 1, sy + 56],
                    fill=(255, 255, 255), outline=(200, 200, 195))
        scene(d, cx0 + 4, sy + 4, 48, 48, kind, (200, 200, 200))
        tx2 = cx0 + 58
        d.text((tx2, sy + 4), tag, font=font(SANS_B, 9), fill=RED)
        y2 = text_block(d, tx2, sy + 16, head, font(SANS_B, 12), INK,
                        cw - 64, leading=14, max_lines=1)
        text_block(d, tx2, y2 + 1, line, font(SANS, 10), (50, 50, 54),
                   cw - 64, leading=11, max_lines=2)

    # ---- grid (456-770): 12 cards, 3 cols x 4 rows -----------------
    gy = 456
    d.rectangle([0, gy, W, gy + 2], fill=NAVY)
    d.text((12, gy + 6), "THE DAY IN BRIEF  ·  12 MORE STORIES",
           font=font(SANS_B, 13), fill=NAVY)
    d.text((W - 12 - d.textlength("8 REGIONS  ·  30 STORIES IN ALL",
                                  font=font(SANS_B, 11)), gy + 8),
           "8 REGIONS  ·  30 STORIES IN ALL", font=font(SANS_B, 11), fill=RED)
    col_w = (W - 24 - 16) // 3
    row_h = 70
    gx0, gy0 = 12, gy + 24
    for i, (tag, head, line, kind) in enumerate(GRID):
        r, c = divmod(i, 3)
        cx0 = gx0 + c * (col_w + 8)
        cy0 = gy0 + r * (row_h + 4)
        d.rectangle([cx0, cy0, cx0 + col_w - 1, cy0 + row_h - 1],
                    fill=(255, 255, 255), outline=(200, 200, 195))
        scene(d, cx0 + 4, cy0 + 4, 62, 62, kind, (230, 230, 230))
        tx2 = cx0 + 72
        d.text((tx2, cy0 + 4), tag, font=font(SANS_B, 9), fill=RED)
        y3 = text_block(d, tx2, cy0 + 17, head, font(SANS_B, 12), INK,
                        col_w - 78, leading=14, max_lines=1)
        text_block(d, tx2, y3 + 1, line, font(SANS, 10), (50, 50, 54),
                   col_w - 78, leading=12, max_lines=3)

    # ---- also strip (774-866): 16 items, 3 columns ------------------
    ay = 774
    d.rectangle([0, ay, W, ay + 2], fill=RED)
    d.text((12, ay + 6), "ALSO ON 25 NOVEMBER", font=font(SANS_B, 12), fill=RED)
    cols = [ALSO[0:5], ALSO[5:10], ALSO[10:15]]
    for ci, items in enumerate(cols):
        x0 = 12 + ci * 336
        yy = ay + 24
        for item in items:
            yy = text_block(d, x0, yy, "•  " + item, font(SANS, 10),
                            (30, 30, 34), 328, leading=11, max_lines=1)
            yy += 2

    # ---- by the numbers (870-930) -----------------------------------
    ny = 870
    d.rectangle([0, ny, W, ny + 2], fill=NAVY)
    d.text((12, ny + 6), "BY THE NUMBERS", font=font(SANS_B, 13), fill=NAVY)
    bw = (W - 24 - 5 * 6) // 6
    for i, (val, lab) in enumerate(NUMBERS):
        bx = 12 + i * (bw + 6)
        d.rectangle([bx, ny + 22, bx + bw - 1, ny + 64],
                    fill=(255, 255, 255), outline=(200, 200, 195))
        centre(d, bx + bw // 2, ny + 25, val, font(SANS_B, 15), RED)
        text_block(d, bx + 5, ny + 44, lab, font(SANS, 9), (50, 50, 54),
                   bw - 10, leading=10, max_lines=2)

    # ---- date check (934-1006) --------------------------------------
    dy = 938
    d.rectangle([0, dy, W, dy + 2], fill=RED)
    d.text((12, dy + 6), "DATE CHECK — READ THIS BEFORE YOU QUOTE THE DATE",
           font=font(SANS_B, 12), fill=RED)
    yy = dy + 24
    for bold, rest in DATE_CHECK:
        full = bold + rest
        lines = wrap(d, full, font(SANS, 11), W - 24)
        for j, ln in enumerate(lines):
            if j == 0:
                d.text((12, yy), bold, font=font(SANS_B, 11), fill=INK)
                d.text((12 + d.textlength(bold, font=font(SANS_B, 11)), yy),
                       ln[len(bold):], font=font(SANS, 11), fill=(40, 40, 44))
            else:
                d.text((12, yy), ln, font=font(SANS, 11), fill=(40, 40, 44))
            yy += 12
        yy += 1

    # ---- footer (1010-1024) -----------------------------------------
    d.rectangle([0, 1004, W, 1006], fill=(180, 180, 175))
    d.text((12, 1010), "Sources: Reuters · AP · UEFA.com · UN OCHA / UNRWA · "
           "BBC · Al Jazeera · Xinhua · company filings — drawn by hand in "
           "code, no photographs.", font=font(SANS, 9), fill=(90, 90, 95))
    return img, n_pins


def main():
    img, n_pins = draw()
    img.save(OUT, "PNG", optimize=True)
    import os
    print("pins:", n_pins)
    print("stories: 30 (1 lead + 2 secondary + 12 grid + 15 also)")
    print("regions: 8")
    print("illustrations: 15 (1 lead + 2 secondary + 12 card scenes)")
    print("bytes:", os.path.getsize(OUT))


if __name__ == "__main__":
    main()
