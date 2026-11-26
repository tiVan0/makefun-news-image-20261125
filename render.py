#!/usr/bin/env python3
"""Render news-image-20261125 v3-B entry.png (1024x1024, <=1 MiB).
Rebalance of the v2 winner ("THE WORLD TODAY"): 50 stories (3 big + 10
medium + 37 ALSO, the #1 formula), bigger ALSO type, roomier layout, and
the Shenzhou Earth-arc clipped inside its illustration (v2's arc spilled
over the body text). Facts carried from verified v2; two mediums demoted
to ALSO (ZNPP, US data) so the facts stay in the paper; five weakest
ALSO lines dropped (see research/verification-notes.md).
Drawn by hand in code with PIL. Deterministic: no timestamps, no random,
fixed fonts, fixed layout.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (247, 243, 232)
INK = (26, 26, 26)
MUTED = (107, 101, 88)
RULE = (216, 208, 188)
CARD = (255, 253, 246)
RED = (179, 39, 30)
BLUE = (31, 78, 121)
DARKBLUE = (22, 50, 79)
GOLD = (200, 162, 39)
GREEN = (30, 107, 58)
AMBER = (138, 90, 0)
TAN = (229, 220, 195)
TAN_LINE = (185, 172, 138)


def F(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_O = lambda s: F("DejaVuSans.ttf", s)  # no Oblique face installed; use regular


def wrap(draw, text, font, width):
    """Greedy word wrap; returns list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, font, width, max_lines):
    """Wrap text; raise if it needs more than max_lines (no truncation allowed)."""
    lines = wrap(draw, text, font, width)
    assert len(lines) <= max_lines, "OVERFLOW %r -> %d lines (max %d)" % (
        text[:40], len(lines), max_lines)
    return lines


def draw_lines(draw, lines, x, y, font, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


TAG_FILL = {"C": GREEN, "R": BLUE, "CL": AMBER}
TAG_LABEL = {"C": "C", "R": "R", "CL": "CL"}


def tag_chip(draw, x, y, tag):
    """Small attribution chip at (x, y); returns width used."""
    label = TAG_LABEL[tag]
    f = SANS_B(8)
    w = int(draw.textlength(label, font=f)) + 8
    draw.rounded_rectangle([x, y, x + w, y + 11], radius=2,
                           fill=TAG_FILL[tag])
    draw.text((x + 4, y + 1), label, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- data
NUMBERS = [
    ("20%", "proposed tariff\non China"),
    ("-6.2%", "KOSPI, Seoul\nworst day since Jan"),
    ("+26%", "UK energy price\ncap from 1 Jan"),
    ("31", "dead in Giza\ntanker fire"),
    ("9 / 17", "dead / trapped\nin Bogor mine flood"),
    ("1ST", "foreigner aboard\nTiangong station"),
]

BIG = [
    dict(num="1", place="WASHINGTON", tag="C",
         head="U.S. PROPOSES TARIFFS ON 14 ECONOMIES",
         body=("USTR opens its Section 301 probe: China faces a proposed "
               "20% tariff on top of duties; the EU, Japan, "
               "South Korea and Taiwan are capped at 15%."),
         why="WHY IT MATTERS: hearings 25 Jan; duties could land Feb-Mar."),
    dict(num="2", place="SEOUL", tag="C",
         head="KOSPI CRASHES 6.2% AS AI DOUBTS SINK CHIP STOCKS",
         body=("Seoul closes at 4,697.51, down 308.52 — its worst day since January. "
               "Samsung -9.9%, SK hynix -11.1% as AI-spending fears spread across Asia."),
         why="WHY IT MATTERS: wipes out Monday's record +6.3% rally in one session."),
    dict(num="3", place="JIUQUAN", tag="C",
         head="SHENZHOU-24 DOCKS — FIRST FOREIGNER ABOARD TIANGONG",
         body=("Long March 2F lifts off 00:18 UTC; the crew docks 03:56 UTC. "
               "Pakistan's Muhammad Zeeshan Ali joins Tang Hongbo and Wu Yi, "
               "the first foreigner aboard."),
         why="WHY IT MATTERS: Beijing's space diplomacy in orbit — a ~week mission."),
]

MEDIUM = [
    dict(num="4", place="LONDON", tag="C", icon="bolt",
         kick="+26%",
         head="UK ENERGY BILLS TO JUMP 26% IN JANUARY",
         body=("Ofgem lifts the cap: a typical bill rises "
               "£1,723 to £2,166 (+£443 a year). Government pays £100 to "
               "~20m homes.")),
    dict(num="5", place="CANBERRA", tag="C", icon="shield",
         kick="NO FOREIGN BASES",
         head="SOLOMONS NAME AUSTRALIA TOP PARTNER",
         body=("Treaty in Canberra: no foreign military base on Solomons "
               "soil; $740m Australian support over a decade; China's "
               "pact lapses.")),
    dict(num="6", place="DHAKA", tag="C", icon="factory",
         kick="TK17,000",
         head="GARMENT WAGE SET AT TK17,000 (+36%)",
         body=("Wage board votes 4-2: minimum "
               "rises Tk12,500 to Tk17,000 from December. Workers wanted "
               "Tk18,000.")),
    dict(num="7", place="CARTAGENA", tag="C", icon="store",
         kick="ALL FREED",
         head="ALL HOSTAGES FREED AFTER 17-HOUR SIEGE",
         body=("Forces storm an Éxito supermarket at 01:30 local: about "
               "30 held since a failed truck robbery; 1 captor killed.")),
    dict(num="8", place="SAMARA", tag="R", icon="derrick",
         kick="2 REFINERIES HIT",
         head="UKRAINE DRONES BURN TWO RUSSIAN REFINERIES",
         body=("Kyiv says overnight strikes hit Kuibyshev and Syzran plants — "
               "crude units and tanks ablaze; capacity 15m+ tonnes "
               "a year.")),
    dict(num="9", place="BOGOR", tag="C", icon="mine",
         kick="9 DEAD · 17 TRAPPED",
         head="9 DEAD, 17 TRAPPED IN FLOODED GOLD MINE",
         body=("Rain swells the Ciseureuh River into an unauthorised shaft about "
               "100m deep near Pongkor. 325 rescuers work; 11 escaped.")),
    dict(num="10", place="GIZA", tag="C", icon="tanker",
         kick="31 KILLED",
         head="TANKER FIRE KILLS 31 ON CAIRO RING ROAD",
         body=("A fuel tanker overturns at 18:08 local and explodes: 31 dead, "
               "21 hurt, 27 vehicles burned; 14 who stopped to help died.")),
    dict(num="11", place="CAPE TOWN", tag="C", icon="gavel",
         kick="PANEL VOID",
         head="FARMGATE PANEL VOID; RAMAPHOSA CLEAR",
         body=("High Court scraps the 2022 Section 89 report as unlawful; "
               "impeachment falls away. The $580,000 case is no trial.")),
    dict(num="12", place="HODEIDAH", tag="C", icon="crane",
         kick="PORT STRUCK",
         head="COALITION HITS HODEIDAH; 4 DRONES DOWNED",
         body=("Saudi-led jets strike the Yemeni port overnight; "
               "4 Houthi drones downed over Ras Tanura. Houthis threaten "
               "Jeddah.")),
    dict(num="13", place="GAZA", tag="R", icon="candle",
         kick="74,746 KILLED",
         head="GAZA TOLL 74,746 — 1,679 SINCE CEASEFIRE",
         body=("Health Ministry count: 74,746 killed, 176,234 hurt since Oct 2023; "
               "1,679 killed since the October 2025 ceasefire.")),
]

ALSO = [
    ("14", "Savasleyka: 3 MiG-31 + 2 Su-34 hit at airfield", "R"),
    ("15", "U.S. weighs strikes on senior Iranian leaders", "R"),
    ("16", "Russia war deaths 490,000+ in leaked records", "R"),
    ("17", "Ukraine drone hits Russian cargo ship, Gulf of Finland", "R"),
    ("18", "Russian drones enter Polish airspace", "R"),
    ("19", "Kryvyi Rih missile: 2 killed, 60 injured", "R"),
    ("20", "Sahel: FPV drones reshape the desert war (Reuters)", "R"),
    ("21", "Russia warned over nuclear-armed satellite", "R"),
    ("22", "Amnesty urges ICC probe of Gaza war crimes", "R"),
    ("23", "Taiz: 350,000 children missed measles vaccines", "C"),
    ("24", "Odesa: 80,000 homes without heat", "C"),
    ("25", "UK warns Ukraine suppliers on Russian sabotage", "R"),
    ("26", "U.S. pauses joint military ops with Ecuador", "R"),
    ("27", "Chen Jining, top Beijing aide, under investigation", "R"),
    ("28", "Sarkozy + Carla Bruni ordered to stand trial", "R"),
    ("29", "Myanmar landmine victims 1,891 in 2025", "R"),
    ("30", "Cikande candy factory fire kills 26", "R"),
    ("31", "Japan PMI 53.7 — factories speed up", "C"),
    ("32", "Australia inflation: trimmed mean 3.8%", "C"),
    ("33", "Brent $90.97, WTI $81.58", "C"),
    ("34", "Bitcoin $59,258, Ether $1,660", "C"),
    ("35", "U.S. retail: Dollar Tree +11%, Dick's +15%", "R"),
    ("36", "Netflix buys Radford Studio for $380m", "R"),
    ("37", "UCL: Real Madrid 5-1 PSV", "C"),
    ("38", "UCL: Arsenal 1-1 Dortmund; Man City 2-2 Napoli", "C"),
    ("39", "Rings of Power renewed for season 4", "R"),
    ("40", "Tidal drops AI music from 9 Dec", "R"),
    ("41", "S&P 500 slips 0.25% on tariff news", "R"),
    ("42", "Zaporizhzhia: 6 hurt in 25 Nov strike, 2 children", "R"),
    ("43", "ZNPP: nuclear plant loses external power", "R"),
    ("44", "UNSC emergency talks on Iran attacks", "R"),
    ("45", "Qatar-U.S. sign AI + critical minerals deals", "R"),
    ("46", "Kherson aid convoy reaches 600 residents left", "C"),
    ("47", "U.S. jobless claims 189,000", "C"),
    ("48", "U.S. GDP revised up to 4.3%; core PCE 3.3%", "C"),
    ("49", "Israel: Eisenkot seals pact with Lieberman", "R"),
    ("50", "Gaza: 1 killed in strike on displacement camp", "R"),
]

TIMELINE = [
    ("00:18", "Shenzhou-24 lifts off, Jiuquan"),
    ("03:56", "Shenzhou-24 docks at Tiangong"),
    ("06:30", "KOSPI closes -6.2% at 4,697.51"),
    ("06:30", "Cartagena: all hostages freed"),
    ("06:35", "Shenzhou crew enters the station"),
    ("16:08", "Giza tanker explodes, 31 killed"),
]

# Region per story (subject/location, not actor). Sums to 50.
REGIONS = [("Europe", 16), ("Middle East", 9), ("North America", 6),
           ("East Asia", 4), ("Global", 4), ("Southeast Asia", 3),
           ("Africa", 3), ("Latin America", 2), ("Oceania", 2),
           ("South Asia", 1)]

# Field per story (type of event). Sums to 50.
FIELDS = [("Ukraine war", 5), ("Disaster", 5), ("Courts & politics", 5),
          ("Strikes", 5), ("Economy", 4), ("Stocks", 3),
          ("Airspace & warnings", 3), ("Diplomacy", 3), ("Energy", 2),
          ("Gaza war", 2), ("Culture", 2), ("Sport", 2), ("Trade", 1),
          ("Space", 1), ("Defence pacts", 1), ("Labour", 1), ("Crime", 1),
          ("Health", 1), ("Commodities", 1), ("Crypto", 1), ("Tech", 1)]

DATE_CHECK = ("NOT 25 NOV — EXCLUDED: Riyadh Houthi missile (24 Nov) · Dell Q3 "
              "(24 Nov) · Sanofi–Insmed (24 Nov) · Miley Cyrus wedding (21 Nov) · "
              "Hamas chief Abu Nahel killed (24 Nov) · Zaporizhzhia strike, 2 killed "
              "(24 Nov) · UNRWA toll 397 announced (24 Nov) · Nvidia +31.5% Mon "
              "(23 Nov) · Nvidia -5.9% Tue (24 Nov) · Dow 50,000 first close "
              "(24 Nov) · Huawei ruling (24 Nov) · Miss Universe (24 Nov) · COP31 · "
              "AFCON: Senegal title · US consumer confidence 103.3 (24 Nov)")

NOT_YET = ("NOT YET: US Thanksgiving (26 Nov) · Bank of Korea decision "
           "(Thu 26 Nov) · OPEC+ meeting (29 Nov) · Fed meeting (9 Dec) · "
           "USTR tariff hearing (25 Jan) · Tariffs may take effect Feb–Mar")

PINS = [("1", -77, 39), ("2", 127, 37.5), ("3", 98, 40), ("4", -0.1, 51.5),
        ("5", 149, -35), ("6", 90, 23.8), ("7", -75.5, 10.4),
        ("8", 50, 53), ("9", 107, -6.6), ("10", 31, 30), ("11", 18.4, -34),
        ("12", 43, 15), ("13", 34.5, 31.5)]
PIN_NUDGE = {"13": (8, 8), "10": (-4, 2)}
PIN_KEY = ("1 Washington (tariffs) · 2 Seoul · 3 Jiuquan · 4 London · "
           "5 Canberra · 6 Dhaka · 7 Cartagena · 8 Samara · 9 Bogor · "
           "10 Giza · 11 Cape Town · 12 Hodeidah · 13 Gaza")

# ---------------------------------------------------------------- illustrations
def illo_tariffs(img, d, x, y, w, h):
    """Container ship + rising tariff bars."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 242), outline=RULE)
    # sky bars: tariff rates rising (fit inside the illustration)
    bars = [("5%", 12), ("10%", 20), ("15%", 28), ("20%", 38)]
    bx = x + 10
    for label, bh in bars:
        d.rectangle([bx, y + h - 12 - bh, bx + 26, y + h - 12], fill=BLUE)
        d.text((bx + 2, y + h - 12 - bh - 11), label, font=SANS_B(8), fill=BLUE)
        bx += 32
    # ship
    sx, sy = x + w - 150, y + h - 34
    d.polygon([(sx, sy), (sx + 140, sy), (sx + 128, sy + 18), (sx + 12, sy + 18)],
              fill=DARKBLUE)
    for i, c in enumerate([(179, 39, 30), (200, 162, 39), (31, 78, 121)]):
        d.rectangle([sx + 14 + i * 34, sy - 22, sx + 44 + i * 34, sy - 2],
                    fill=c, outline=(255, 255, 255))
    d.rectangle([sx + 118, sy - 30, sx + 138, sy - 2], fill=(255, 255, 255),
                outline=INK)
    d.line([(sx, sy + 18), (sx + 140, sy + 18)], fill=BLUE, width=2)
    # waves
    for i in range(5):
        wx = x + 12 + i * 60
        d.arc([wx, y + h - 8, wx + 34, y + h + 4], 180, 360, fill=BLUE, width=2)


def illo_kospi(img, d, x, y, w, h):
    """Plunging chart + chip."""
    d.rectangle([x, y, x + w, y + h], fill=(242, 228, 228), outline=RULE)
    # grid
    for i in range(1, 4):
        gy = y + i * h // 4
        d.line([(x + 6, gy), (x + w - 6, gy)], fill=(225, 205, 205))
    pts = [(x + 12, y + 14), (x + 60, y + 20), (x + 105, y + 12),
           (x + 150, y + 30), (x + 195, y + 48), (x + 240, y + 62),
           (x + w - 14, y + h - 16)]
    d.line(pts, fill=RED, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.text((x + 12, y + 4), "-6.2%", font=SANS_B(13), fill=RED)
    # chip
    cx, cy = x + w - 62, y + 10
    d.rectangle([cx, cy, cx + 44, cy + 44], fill=DARKBLUE, outline=GOLD,
                width=2)
    d.rectangle([cx + 12, cy + 12, cx + 32, cy + 32], fill=GOLD)
    for i in range(3):
        d.line([(cx + 6 + i * 14, cy), (cx + 6 + i * 14, cy - 5)], fill=GOLD,
               width=2)
        d.line([(cx + 6 + i * 14, cy + 44), (cx + 6 + i * 14, cy + 49)],
               fill=GOLD, width=2)


def illo_shenzhou(img, d, x, y, w, h):
    """Rocket + station over Earth arc.

    v2 BUG FIX: the Earth arc used to be drawn straight onto the page,
    and its arms swept down past the illustration into the body text
    (the blue swoosh across feature 3's first body line, and into
    feature 2's column). The arc is now drawn on a layer the exact size
    of the illustration and pasted with its own alpha mask, so nothing
    can spill past the illustration's edges.
    """
    d.rectangle([x, y, x + w, y + h], fill=(22, 38, 64), outline=RULE)
    # Earth arc, clipped to the illustration rect via a layer
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.arc([-60, h - 6, w + 60, h + 90], 180, 360,
           fill=(90, 160, 220, 255), width=5)
    img.paste(layer, (x, y), layer)
    # stars
    for sx, sy in [(20, 12), (70, 22), (150, 10), (230, 18), (290, 12),
                   (40, 40), (190, 30), (260, 38), (110, 16)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(255, 255, 255))
    # station
    stx, sty = x + w - 120, y + 12
    d.rectangle([stx, sty + 8, stx + 76, sty + 20], fill=(200, 200, 200),
                outline=(255, 255, 255))
    d.rectangle([stx - 26, sty + 4, stx, sty + 24], fill=BLUE,
                outline=(255, 255, 255))
    d.rectangle([stx + 76, sty + 4, stx + 102, sty + 24], fill=BLUE,
                outline=(255, 255, 255))
    d.ellipse([stx + 30, sty + 9, stx + 46, sty + 19], fill=GOLD)
    # rocket (fits inside the illustration)
    rx, ry = x + 60, y + 14
    d.polygon([(rx + 8, ry), (rx + 16, ry + 12), (rx + 16, ry + 36),
               (rx + 8, ry + 36), (rx, ry + 12)], fill=(255, 255, 255),
              outline=RED)
    d.ellipse([rx + 6, ry + 18, rx + 10, ry + 22], fill=BLUE)
    d.polygon([(rx, ry + 36), (rx - 10, ry + 46), (rx, ry + 40)],
              fill=RED)
    d.polygon([(rx + 16, ry + 36), (rx + 26, ry + 46), (rx + 16, ry + 40)],
              fill=RED)
    d.polygon([(rx + 4, ry + 36), (rx + 8, ry + 52), (rx + 12, ry + 36)],
              fill=(255, 180, 60))
    d.text((x + w - 72, y + h - 18), "TIANGONG", font=SANS_B(9),
           fill=(255, 255, 255))


def icon(d, kind, x, y, s=26):
    """Small pictogram for a medium cell."""
    d.rectangle([x, y, x + s, y + s], fill=TAN, outline=RULE)
    if kind == "bolt":
        d.polygon([(x + 15, y + 2), (x + 7, y + 15), (x + 13, y + 15),
                   (x + 11, y + 24), (x + 19, y + 11), (x + 13, y + 11)],
                  fill=GOLD)
    elif kind == "shield":
        d.polygon([(x + 13, y + 3), (x + 22, y + 6), (x + 22, y + 14),
                   (x + 13, y + 23), (x + 4, y + 14), (x + 4, y + 6)],
                  fill=BLUE)
        d.text((x + 10, y + 8), "*", font=SANS_B(12), fill=(255, 255, 255))
    elif kind == "factory":
        d.polygon([(x + 4, y + 12), (x + 8, y + 6), (x + 12, y + 12),
                   (x + 16, y + 6), (x + 20, y + 12), (x + 22, y + 12),
                   (x + 22, y + 22), (x + 4, y + 22)], fill=DARKBLUE)
        d.rectangle([x + 17, y + 3, x + 20, y + 10], fill=RED)
    elif kind == "store":
        d.rectangle([x + 4, y + 10, x + 22, y + 22], fill=(255, 255, 255),
                    outline=INK)
        for i, c in enumerate([RED, (255, 255, 255), BLUE, (255, 255, 255)]):
            d.rectangle([x + 4 + i * 5, y + 4, x + 9 + i * 5, y + 10], fill=c,
                        outline=INK)
        d.rectangle([x + 10, y + 15, x + 16, y + 22], fill=INK)
    elif kind == "derrick":
        d.polygon([(x + 6, y + 22), (x + 13, y + 3), (x + 20, y + 22)],
                  fill=None, outline=INK, width=2)
        d.line([(x + 9, y + 14), (x + 17, y + 14)], fill=INK, width=2)
        d.ellipse([x + 18, y + 2, x + 24, y + 10], fill=(255, 140, 40))
    elif kind == "mine":
        d.rectangle([x + 5, y + 4, x + 21, y + 22], fill=DARKBLUE)
        d.line([(x + 9, y + 5), (x + 9, y + 21)], fill=(255, 255, 255),
               width=2)
        d.line([(x + 13, y + 5), (x + 13, y + 21)], fill=(255, 255, 255),
               width=2)
        d.arc([x + 2, y + 16, x + 24, y + 26], 180, 360, fill=BLUE, width=3)
    elif kind == "tanker":
        d.rectangle([x + 3, y + 8, x + 16, y + 17], fill=GOLD, outline=INK)
        d.rectangle([x + 17, y + 11, x + 22, y + 17], fill=RED, outline=INK)
        d.ellipse([x + 6, y + 17, x + 10, y + 21], fill=INK)
        d.ellipse([x + 16, y + 17, x + 20, y + 21], fill=INK)
        d.polygon([(x + 8, y + 2), (x + 11, y + 7), (x + 5, y + 7)],
                  fill=(255, 140, 40))
    elif kind == "gavel":
        d.rectangle([x + 4, y + 5, x + 16, y + 11], fill=(120, 72, 20))
        d.line([(x + 13, y + 11), (x + 20, y + 21)], fill=(120, 72, 20),
               width=3)
        d.line([(x + 4, y + 22), (x + 22, y + 22)], fill=INK, width=2)
    elif kind == "crane":
        d.line([(x + 5, y + 22), (x + 5, y + 4)], fill=INK, width=2)
        d.line([(x + 5, y + 5), (x + 22, y + 5)], fill=INK, width=2)
        d.line([(x + 18, y + 5), (x + 18, y + 12)], fill=INK, width=1)
        d.rectangle([x + 14, y + 12, x + 22, y + 18], fill=RED)
        d.line([(x + 3, y + 22), (x + 23, y + 22)], fill=BLUE, width=3)
    elif kind == "candle":
        d.rectangle([x + 11, y + 10, x + 15, y + 22], fill=(255, 255, 255),
                    outline=INK)
        d.ellipse([x + 11, y + 3, x + 15, y + 10], fill=(255, 180, 60))
        d.line([(x + 5, y + 22), (x + 21, y + 22)], fill=INK, width=2)
    elif kind == "tower":
        d.polygon([(x + 7, y + 4), (x + 19, y + 4), (x + 16, y + 22),
                   (x + 10, y + 22)], fill=(200, 200, 200), outline=INK)
        d.line([(x + 8, y + 10), (x + 18, y + 10)], fill=INK, width=1)
        d.ellipse([x + 19, y + 2, x + 24, y + 8], fill=GOLD)
    elif kind == "chart":
        for i, hgt in enumerate([7, 12, 18]):
            d.rectangle([x + 4 + i * 7, y + 22 - hgt, x + 9 + i * 7, y + 22],
                        fill=GREEN)
        d.line([(x + 3, y + 4), (x + 23, y + 4)], fill=GREEN, width=2)
        d.polygon([(x + 23, y + 4), (x + 18, y + 2), (x + 18, y + 6)],
                  fill=GREEN)


ILLUSTRATIONS = {"tariffs": illo_tariffs, "kospi": illo_kospi,
                 "shenzhou": illo_shenzhou}
BIG_ILLUSTRATION = ["tariffs", "kospi", "shenzhou"]

# ---------------------------------------------------------------- world map
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 70), (-80, 73),
           (-75, 60), (-70, 45), (-80, 32), (-85, 25), (-97, 26),
           (-105, 20), (-115, 28), (-125, 40), (-130, 55), (-150, 60),
           (-165, 60)],
    "SA": [(-80, 10), (-60, 5), (-50, -5), (-40, -20), (-50, -35),
           (-60, -45), (-70, -55), (-75, -40), (-80, -20), (-80, -5)],
    "EU": [(-10, 36), (-5, 44), (0, 50), (10, 55), (20, 60), (30, 62),
           (40, 60), (35, 50), (30, 45), (20, 40), (10, 38), (0, 36)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31),
           (35, 27), (40, 15), (50, 10), (45, 0), (40, -15), (35, -25),
           (25, -35), (15, -30), (10, -20), (5, -5), (0, 5), (-10, 5)],
    "AS": [(40, 60), (50, 70), (70, 72), (90, 75), (120, 75), (150, 70),
           (170, 66), (160, 60), (140, 50), (130, 40), (120, 30),
           (110, 20), (100, 10), (95, 5), (90, 15), (85, 20), (80, 10),
           (75, 8), (70, 20), (60, 25), (55, 30), (50, 35), (45, 40),
           (40, 45)],
    "OC": [(113, -22), (125, -15), (140, -12), (150, -20), (150, -35),
           (140, -38), (130, -32), (120, -35), (113, -30)],
}


def project(lon, lat, x0, y0, w, h):
    px = x0 + (lon + 170) / 360.0 * w
    py = y0 + (70 - lat) / 125.0 * h
    return px, py


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 240, 244),
                outline=RULE)
    for pts in CONTINENTS.values():
        xy = [project(lon, lat, x0, y0, w, h) for lon, lat in pts]
        d.polygon(xy, fill=TAN, outline=TAN_LINE)
    for num, lon, lat in PINS:
        px, py = project(lon, lat, x0, y0, w, h)
        dx, dy = PIN_NUDGE.get(num, (0, 0))
        px, py = px + dx, py + dy
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = SANS_B(7 if len(num) == 1 else 6)
        tw = d.textlength(num, font=f)
        d.text((px - tw / 2, py - 5), num, font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------- layout
W, H = 1024, 1024
M = 14
CW = W - 2 * M


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (y 8..60)
    title = "THE WORLD TODAY"
    tf = SERIF_B(38)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 6), title, font=tf, fill=INK)
    d.line([(M, 50), (W - M, 50)], fill=INK, width=2)
    sub = ("WEDNESDAY 25 NOVEMBER 2026  ·  50 STORIES  ·  10 REGIONS  ·  "
           "21 FIELDS  ·  DRAWN BY HAND IN CODE — NO PHOTOGRAPHS")
    sf = SANS_B(10)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 54), sub, font=sf,
           fill=MUTED)

    # ---- number strip (y 66..108)
    y0, y1 = 66, 108
    bw = (CW - 5 * 6) // 6
    for i, (num, label) in enumerate(NUMBERS):
        x = M + i * (bw + 6)
        d.rectangle([x, y0, x + bw, y1], fill=CARD, outline=RULE)
        d.text((x + 8, y0 + 3), num, font=SANS_B(20), fill=RED)
        ly = y0 + 24
        for ln in label.split("\n"):
            d.text((x + 8, ly), ln, font=SANS(8), fill=MUTED)
            ly += 9

    # ---- big features (y 112..320)
    by0, by1 = 112, 320
    colw = (CW - 2 * 8) // 3
    for i, b in enumerate(BIG):
        x = M + i * (colw + 8)
        d.rectangle([x, by0, x + colw, by1], fill=CARD, outline=RULE)
        px, py = x + 8, by0 + 6
        d.text((px, py), b["num"] + "  ·  " + b["place"], font=SANS_B(10),
               fill=RED)
        tw_chip = tag_chip(d, x + colw - 30, py + 1, b["tag"])
        py += 15
        head_lines = fit_lines(d, b["head"], SANS_B(15), colw - 16, 2)
        py = draw_lines(d, head_lines, px, py, SANS_B(15), INK, 17)
        py += 3
        ILLUSTRATIONS[BIG_ILLUSTRATION[i]](img, d, px, py, colw - 16, 74)
        py += 78
        body_lines = fit_lines(d, b["body"], SANS(10), colw - 16, 3)
        py = draw_lines(d, body_lines, px, py, SANS(10), INK, 13)
        py += 2
        why_lines = fit_lines(d, b["why"], SANS_O(9), colw - 16, 2)
        py = draw_lines(d, why_lines, px, py, SANS_O(9), MUTED, 11)
        assert py <= by1 - 4, "big feature %s overflows" % b["num"]

    # ---- medium grid (y 326..538): 5 cols x 2 rows
    my0 = 326
    cellw = 192
    cellh = 106
    for i, m in enumerate(MEDIUM):
        r, c = divmod(i, 5)
        x = M + c * (cellw + 9)
        y = my0 + r * (cellh + 4)
        d.rectangle([x, y, x + cellw, y + cellh], fill=CARD, outline=RULE)
        px, py = x + 8, y + 6
        icon(d, m["icon"], px, py, 28)
        d.text((px + 34, py), m["num"] + " · " + m["place"],
               font=SANS_B(10), fill=RED)
        d.text((px + 34, py + 12), m["kick"], font=SANS_B(10), fill=DARKBLUE)
        tag_chip(d, x + cellw - 30, py + 1, m["tag"])
        py += 34
        head_lines = fit_lines(d, m["head"], SANS_B(11), cellw - 16, 2)
        py = draw_lines(d, head_lines, px, py, SANS_B(11), INK, 12)
        body_lines = fit_lines(d, m["body"], SANS(8), cellw - 16, 3)
        py = draw_lines(d, body_lines, px, py, SANS(8), INK, 11)
        assert py <= y + cellh - 3, "medium %s overflows" % m["num"]

    return img, d

def build_rest(img, d):
    # ---- ALSO (y 548..733): 3 columns x 13 rows
    ay0 = 548
    d.text((M, ay0), "ALSO — THE REST OF THE DAY",
           font=SANS_B(12), fill=INK)
    d.line([(M + 218, ay0 + 8), (W - M, ay0 + 8)], fill=RULE, width=1)
    colw = (CW - 2 * 10) // 3
    rows = 13
    for i, (num, text, tag) in enumerate(ALSO):
        col, row = divmod(i, rows)
        x = M + col * (colw + 10)
        y = ay0 + 16 + row * 13
        line = num + ". " + text
        # bigger type than v2 (9pt, was 8pt); shrink only if it must
        f = SANS(9)
        if d.textlength(line, font=f) > colw - 16:
            f = SANS(8)
        assert d.textlength(line, font=f) <= colw - 16, \
            "ALSO %s too long: %r" % (num, line)
        d.text((x, y), line, font=f, fill=INK)
        tag_chip(d, x + colw - 16, y, tag)

    # ---- map + timeline (y 742..856)
    ty0 = 742
    d.line([(M, ty0 - 4), (W - M, ty0 - 4)], fill=INK, width=1)
    # map (left, 500 wide)
    map_w = 500
    d.text((M, ty0), "WHERE IT HAPPENED — PINS 1–13 (SCHEMATIC)",
           font=SANS_B(10), fill=INK)
    draw_map(d, M, ty0 + 15, map_w, 76)
    key_lines = wrap(d, PIN_KEY, SANS(8), map_w)
    assert len(key_lines) <= 2, "pin key too long"
    ky = ty0 + 94
    for ln in key_lines:
        d.text((M, ky), ln, font=SANS(8), fill=MUTED)
        ky += 9
    # timeline (right)
    tx = M + map_w + 16
    tw = W - M - tx
    d.text((tx, ty0), "THE DAY IN UTC", font=SANS_B(10), fill=INK)
    tyy = ty0 + 16
    for t, text in TIMELINE:
        d.text((tx, tyy), t, font=SANS_B(10), fill=RED)
        d.text((tx + 46, tyy), text, font=SANS(10), fill=INK)
        tyy += 15
    d.text((tx, tyy + 2), "All times UTC, 25 Nov 2026.", font=SANS_O(8),
           fill=MUTED)

    # ---- region bar (y 860..878)
    ry = 860
    d.line([(M, ry - 2), (W - M, ry - 2)], fill=RULE, width=1)
    reg = "REGIONS (50): " + "  ·  ".join(
        "%s %d" % (name, n) for name, n in REGIONS)
    assert d.textlength(reg, font=SANS(10)) <= CW, "region bar too long"
    d.text((M, ry), reg, font=SANS(10), fill=INK)

    # ---- fields bar (y 880..906, two lines)
    fy = 880
    fld = "FIELDS (50): " + "  ·  ".join(
        "%s %d" % (name, n) for name, n in FIELDS)
    fld_lines = wrap(d, fld, SANS(10), CW)
    assert len(fld_lines) <= 2, "fields bar too long"
    for ln in fld_lines:
        d.text((M, fy), ln, font=SANS(10), fill=INK)
        fy += 13

    # ---- DATE CHECK + NOT YET (y 912..964)
    dy = 912
    d.line([(M, dy - 2), (W - M, dy - 2)], fill=RULE, width=1)
    dc_w = 640
    d.text((M, dy), "DATE CHECK", font=SANS_B(10), fill=RED)
    dc_lines = wrap(d, DATE_CHECK, SANS(8), dc_w)
    assert len(dc_lines) <= 3, "DATE CHECK too long: %d lines" % len(dc_lines)
    yy = dy + 12
    for ln in dc_lines:
        d.text((M, yy), ln, font=SANS(8), fill=INK)
        yy += 10
    nx = M + dc_w + 16
    d.text((nx, dy), "NOT YET", font=SANS_B(10), fill=BLUE)
    ny_lines = wrap(d, NOT_YET, SANS(8), W - M - nx)
    assert len(ny_lines) <= 3, "NOT YET too long"
    yy = dy + 12
    for ln in ny_lines:
        d.text((nx, yy), ln, font=SANS(8), fill=INK)
        yy += 10

    # ---- footer (y 968..1012)
    fy2 = 968
    d.line([(M, fy2 - 2), (W - M, fy2 - 2)], fill=INK, width=1)
    legend = ("TAGS:  C = CONFIRMED (official source)   ·   R = REPORTED   ·   "
              "CL = CLAIM (unverified)")
    d.text((M, fy2 + 2), legend, font=SANS_B(9), fill=INK)
    src = ("Sources: Reuters, AP, Xinhua/CMSA, Ofgem, USTR, BEA, UN/OCHA, "
           "court and wire reports, 25 Nov 2026. All figures as reported that day.")
    d.text((M, fy2 + 15), src, font=SANS(8), fill=MUTED)
    foot = ("THE WORLD TODAY — 25 November 2026 · entry for make.fun "
            "news-image-20261125 · drawn by hand in code, no photographs")
    d.text((M, fy2 + 27), foot, font=SANS(8), fill=MUTED)


def main():
    img, d = build()
    build_rest(img, d)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print("entry.png: %dx%d, %d bytes (limit 1048576)" % (img.width, img.height, size))
    assert img.width <= 1024 and img.height <= 1024
    assert size <= 1048576, "entry.png over 1 MiB"
    print("OK")


if __name__ == "__main__":
    main()
