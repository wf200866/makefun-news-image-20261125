#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news poster (1024x1024 PNG).

Everything is vector-drawn with Pillow so the text stays crisp at any scale.
Run:  python3 draw.py [out.png]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (11, 18, 32)
PANEL = (20, 29, 46)
PANEL_LINE = (36, 48, 73)
TEXT = (240, 244, 250)
MUTED = (176, 188, 208)
DIM = (128, 143, 168)
RULE = (44, 58, 86)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    box = draw.textbbox((0, 0), s, font=f)
    return box[2] - box[0]


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def icon_trade(d, cx, cy, c):
    # globe with a rising tariff bar chart
    r = 30
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=3)
    d.ellipse((cx - 13, cy - r, cx + 13, cy + r), outline=c, width=2)
    d.line((cx - r, cy, cx + r, cy), fill=c, width=2)
    d.line((cx - 26, cy - 15, cx + 26, cy - 15), fill=c, width=2)
    d.line((cx - 26, cy + 15, cx + 26, cy + 15), fill=c, width=2)
    for i, h in enumerate((10, 19, 29)):
        x = cx + 20 + i * 10
        d.rectangle((x, cy + 8 - h, x + 6, cy + 8), fill=c)
    d.line((cx + 20, cy - 30, cx + 52, cy - 30), fill=c, width=3)
    d.line((cx + 45, cy - 37, cx + 52, cy - 30), fill=c, width=3)
    d.line((cx + 45, cy - 23, cx + 52, cy - 30), fill=c, width=3)


def icon_refinery(d, cx, cy, c):
    # three distillation columns, flames and smoke
    base = cy + 34
    for i, (x, h) in enumerate(((-34, 44), (-6, 62), (22, 50))):
        left = cx + x
        d.rectangle((left, base - h, left + 20, base), outline=c, width=3)
        d.arc((left, base - h - 10, left + 20, base - h + 10), 180, 360,
              fill=c, width=3)
        d.line((left + 10, base - h - 10, left + 10, base - h - 24), fill=c, width=2)
    for i, (fx, fy, s) in enumerate(((cx - 24, base - 70, 10),
                                     (cx + 4, base - 88, 12),
                                     (cx + 32, base - 76, 9))):
        d.polygon([(fx, fy + s), (fx - s * 0.7, fy), (fx, fy + s * 0.4),
                   (fx + s * 0.6, fy - s * 0.4)], fill=c)
    # smoke puffs drifting right
    for i, rr in enumerate((7, 10)):
        d.ellipse((cx + 24 + i * 15, cy - 44 - i * 9,
                   cx + 24 + i * 15 + rr, cy - 44 - i * 9 + rr),
                  outline=c, width=2)


def icon_gaza(d, cx, cy, c):
    # damaged skyline under a dust cloud
    base = cy + 30
    for i, (x, w, h) in enumerate(((-40, 22, 42), (-14, 26, 58),
                                   (16, 20, 34), (40, 18, 48))):
        left = cx + x
        top = base - h
        if i % 2:
            d.polygon([(left, top + 10), (left + w * 0.4, top),
                       (left + w, top + 8), (left + w, base), (left, base)],
                      outline=c)
        else:
            d.rectangle((left, top, left + w, base), outline=c, width=3)
        d.line((left + w * 0.5, top, left + w * 0.5, top + 12), fill=c, width=2)
    for i, rr in enumerate((9, 12)):
        d.arc((cx - 30 + i * 16, cy - 50 + i * 6,
               cx + 18 + i * 16, cy - 10 + i * 6), 200, 340, fill=c, width=2)
    d.ellipse((cx + 34, cy - 34, cx + 46, cy - 22), fill=c)


def icon_tanker(d, cx, cy, c):
    # fuel truck with fire behind it
    d.rounded_rectangle((cx - 44, cy - 14, cx + 18, cy + 18), 6,
                        outline=c, width=3)
    d.rectangle((cx + 18, cy - 4, cx + 40, cy + 18), outline=c, width=3)
    d.rectangle((cx + 24, cy + 1, cx + 35, cy + 9), outline=c, width=2)
    for wx in (cx - 28, cx + 12, cx + 32):
        d.ellipse((wx, cy + 12, wx + 14, cy + 26), outline=c, width=3)
        d.ellipse((wx + 4, cy + 16, wx + 10, cy + 22), fill=c)
    for i, (fx, fy) in enumerate(((cx - 26, cy - 14), (cx - 8, cy - 16))):
        d.polygon([(fx - 8, fy), (fx - 1, fy - 14), (fx + 2, fy - 7),
                   (fx + 7, fy - 22), (fx + 9, fy - 4), (fx + 2, fy + 2)],
                  fill=c)


def icon_labour(d, cx, cy, c):
    # t-shirt on a hanger
    d.line((cx, cy - 44, cx, cy - 30), fill=c, width=3)
    d.polygon([(cx, cy - 44), (cx - 20, cy - 34), (cx - 44, cy - 16)],
              outline=c, width=3)
    d.polygon([(cx - 34, cy - 22), (cx - 20, cy - 30), (cx - 8, cy - 12),
               (cx - 8, cy + 34), (cx + 8, cy + 34), (cx + 8, cy - 12),
               (cx + 20, cy - 30), (cx + 34, cy - 22), (cx + 46, cy - 6),
               (cx + 30, cy + 4), (cx + 30, cy + 34), (cx - 30, cy + 34),
               (cx - 30, cy + 4), (cx - 46, cy - 6)],
              outline=c, width=3)
    d.arc((cx - 9, cy - 20, cx + 9, cy - 4), 0, 180, fill=c, width=2)


def icon_space(d, cx, cy, c):
    # space station: core module and solar wings
    d.rounded_rectangle((cx - 26, cy - 9, cx + 26, cy + 9), 8, outline=c, width=3)
    d.ellipse((cx - 8, cy - 5, cx + 2, cy + 5), outline=c, width=2)
    for side in (-1, 1):
        x0 = cx + (20 if side > 0 else -54)
        d.line((cx + side * 22, cy, x0, cy), fill=c, width=3)
        d.rectangle((x0, cy - 20, x0 + 34, cy + 20), outline=c, width=3)
        for k in (1, 2):
            d.line((x0 + k * 11, cy - 20, x0 + k * 11, cy + 20), fill=c, width=2)
        d.line((x0, cy, x0 + 34, cy), fill=c, width=2)
    for sx, sy in ((-52, -38), (44, -40), (58, 30), (-40, 34), (10, -42)):
        d.ellipse((cx + sx, cy + sy, cx + sx + 3, cy + sy + 3), fill=c)


ICONS = {
    "trade": icon_trade,
    "refinery": icon_refinery,
    "gaza": icon_gaza,
    "tanker": icon_tanker,
    "labour": icon_labour,
    "space": icon_space,
}

STORIES = [
    {
        "kind": "trade",
        "tag": "TRADE  ·  WASHINGTON",
        "color": (242, 179, 61),
        "head": "US unveils tariffs on 14 partners",
        "body": "New duties target China, the EU and 12 others over excess industrial capacity; US stocks fall.",
    },
    {
        "kind": "refinery",
        "tag": "ENERGY  ·  SAUDI ARABIA",
        "color": (240, 122, 60),
        "head": "Houthis hit Saudi oil refinery",
        "body": "Drones hit Saudi Arabia's largest refinery; fires and thick smoke rise over the export hub.",
    },
    {
        "kind": "gaza",
        "tag": "CONFLICT  ·  GAZA",
        "color": (224, 85, 85),
        "head": "Strike kills Hamas official's family",
        "body": "An Israeli raid on Al-Shati camp kills a senior Hamas security official, his wife and daughters; 7 die in Gaza.",
    },
    {
        "kind": "tanker",
        "tag": "DISASTER  ·  EGYPT",
        "color": (230, 101, 58),
        "head": "Cairo fuel tanker blast kills 30+",
        "body": "A tanker overturns and explodes on a Cairo highway, killing at least 30 people and injuring dozens.",
    },
    {
        "kind": "labour",
        "tag": "LABOUR  ·  BANGLADESH",
        "color": (88, 192, 138),
        "head": "Garment wage set at Tk 17,000",
        "body": "A wage board vote lifts the minimum from Tk 12,500; workers reject it and 140 factories shut.",
    },
    {
        "kind": "space",
        "tag": "SPACE  ·  CHINA",
        "color": (86, 168, 232),
        "head": "First Pakistani aboard Tiangong",
        "body": "Shenzhou-24 arrives at China's station with Muhammad Zeeshan Ali, its first foreign astronaut.",
    },
]

TICKER = ("Greece: 15,000 march in a general strike   ·   "
          "Australia and Solomon Islands sign a security treaty   ·   "
          "EU and UK fine fragrance makers €570m")


def main(out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_kicker = font(BOLD, 17)
    f_date = font(BOLD, 62)
    f_date2 = font(REG, 22)
    f_tag = font(BOLD, 13)
    f_head = font(BOLD, 29)
    f_body = font(REG, 18)
    f_tick = font(REG, 13)
    f_ticklab = font(BOLD, 13)

    # masthead
    d.rectangle((0, 0, W, 8), fill=(179, 33, 43))
    d.text((44, 30), "WEDNESDAY   ·   WORLD NEWS", font=f_kicker,
           fill=(242, 179, 61))
    d.text((40, 56), "25 NOVEMBER 2026", font=f_date, fill=TEXT)
    d.text((W - 44, 32), "ONE DAY  ·  SIX STORIES", font=f_date2,
           fill=DIM, anchor="ra")
    d.line((32, 146, W - 32, 146), fill=RULE, width=2)

    # panel grid
    x0, y0 = 34, 164
    pw, ph, gap_x, gap_y = 468, 250, 20, 16
    for i, s in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = x0 + col * (pw + gap_x)
        y = y0 + row * (ph + gap_y)
        d.rounded_rectangle((x, y, x + pw, y + ph), 14, fill=PANEL,
                            outline=PANEL_LINE, width=2)
        d.rounded_rectangle((x, y, x + 7, y + ph), 4, fill=s["color"])
        head_lines = wrap(d, s["head"], f_head, pw - 150)[:3]
        body_lines = wrap(d, s["body"], f_body, pw - 150)[:4]
        block_h = 24 + len(head_lines) * 34 + 6 + len(body_lines) * 22
        ty = y + (ph - block_h) // 2
        ICONS[s["kind"]](d, x + 64, y + ph // 2, s["color"])
        d.text((x + 130, ty), s["tag"], font=f_tag, fill=s["color"])
        ty += 24
        for ln in head_lines:
            d.text((x + 130, ty), ln, font=f_head, fill=TEXT)
            ty += 34
        ty += 6
        for ln in body_lines:
            d.text((x + 130, ty), ln, font=f_body, fill=MUTED)
            ty += 22

    # ticker strip
    ty0 = 952
    d.rectangle((0, ty0, W, H), fill=(16, 24, 39))
    d.line((0, ty0, W, ty0), fill=RULE, width=2)
    d.text((36, ty0 + 12), "ALSO ON 25 NOV", font=f_ticklab,
           fill=(242, 179, 61))
    d.text((36, ty0 + 34), TICKER, font=f_tick, fill=MUTED)
    d.text((W - 36, H - 7), "Sources: Reuters · AP · AFP · NBC · Al Jazeera · The Daily Star",
           font=font(REG, 10), fill=DIM, anchor="rs")

    img.save(out_path, "PNG", optimize=True)
    print("wrote", out_path, img.size)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
