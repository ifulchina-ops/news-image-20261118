#!/usr/bin/env python3
"""Draw the front page for Wednesday 18 November 2026 — no network, PIL only.

Design: a single broadsheet, "THE EIGHTEENTH". Masthead, one lead story
with a drawn skyline panel, two war-and-security stories in the right
column, a three-story middle band, and a "day in brief" strip at the foot.
All headlines are real stories first reported on 18 November 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (158, 27, 24)
BLUE = (24, 58, 110)
GREY = (96, 92, 84)
RULE = (60, 56, 48)
SKY = (214, 228, 238)
SEA = (52, 92, 130)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text):
    f = font(SANS_B, 15)
    draw.text((x, y), text, font=f, fill=RED)
    return y + 21


def headline(draw, x, y, text, size, max_w, leading=None):
    f = font(SERIF_B, size)
    leading = leading or int(size * 1.08)
    for line in wrap(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=INK)
        y += leading
    return y


def skyline_panel(draw, x, y, w, h):
    """Manila bay at dusk: sky, sun, towers, water, four Quad dots."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY, outline=RULE, width=2)
    # sun
    cx, cy, r = x + w - 70, y + 52, 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 164, 62))
    # towers
    import random
    rnd = random.Random(18)
    bx = x + 12
    while bx < x + w - 20:
        bw = rnd.randint(28, 52)
        bh = rnd.randint(60, h - 90)
        top = y + h - 46 - bh
        draw.rectangle([bx, top, bx + bw, y + h - 46], fill=(58, 74, 92))
        for wy in range(top + 10, y + h - 52, 16):
            for wx in range(bx + 6, bx + bw - 6, 12):
                if rnd.random() < 0.5:
                    draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(240, 214, 120))
        bx += bw + 8
    # water
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=SEA)
    for i in range(6):
        wy = y + h - 38 + i * 6
        draw.line([(x + 10 + i * 7, wy), (x + w - 10 - i * 5, wy)],
                  fill=(150, 190, 220), width=2)
    # four Quad flags as coloured dots above the skyline
    cols = [(178, 34, 34), (255, 255, 255), (255, 153, 51), (0, 0, 139)]
    for i, c in enumerate(cols):
        fx = x + 26 + i * 34
        draw.ellipse([fx, y + 14, fx + 20, y + 34], fill=c, outline=RULE, width=2)


def bridge_panel(draw, x, y, w, h):
    """A long bridge over dark water, smoke rising from one span."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 214, 196), outline=RULE, width=2)
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(70, 96, 122))
    # deck + pylons
    dy = y + h - 26
    draw.rectangle([x + 8, dy, x + w - 8, dy + 6], fill=(52, 52, 52))
    for px in (x + 34, x + w // 2 - 4, x + w - 42):
        draw.rectangle([px, y + 10, px + 8, dy], fill=(52, 52, 52))
    # cables
    draw.line([(x + 38, y + 10), (x + w // 2, dy)], fill=(52, 52, 52), width=2)
    draw.line([(x + w - 38, y + 10), (x + w // 2, dy)], fill=(52, 52, 52), width=2)
    # smoke from the middle span
    for i, (sx, sy, sr) in enumerate([(x + w // 2 - 6, y + 16, 9),
                                      (x + w // 2 + 8, y + 8, 11),
                                      (x + w // 2 + 22, y + 4, 12)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 116, 110))
    # orange flash on the deck
    draw.polygon([(x + w // 2 - 12, dy), (x + w // 2, dy - 14),
                  (x + w // 2 + 12, dy)], fill=(224, 110, 30))


def radar_panel(draw, x, y, w, h):
    """Radar dish under a night sky, three drone dots overhead."""
    draw.rectangle([x, y, x + w, y + h], fill=(30, 38, 54), outline=RULE, width=2)
    for i in range(24):
        import random
        rnd = random.Random(100 + i)
        draw.point((x + rnd.randint(4, w - 4), y + rnd.randint(4, h // 2)),
                   fill=(200, 200, 200))
    # dish
    cx, cy = x + w // 2, y + h - 16
    draw.pieslice([cx - 34, cy - 52, cx + 34, cy + 6], 180, 360, fill=(190, 196, 205))
    draw.line([(cx, cy - 26), (cx, cy)], fill=(190, 196, 205), width=4)
    draw.polygon([(cx - 18, cy), (cx + 18, cy), (cx + 28, y + h - 4),
                  (cx - 28, y + h - 4)], fill=(120, 126, 136))
    # sweeping beam
    draw.line([(cx, cy - 26), (cx + 44, y + 12)], fill=(120, 220, 130), width=3)
    # drones
    for dx, dy in [(x + 22, y + 16), (x + w - 34, y + 26), (x + w // 2 + 40, y + 10)]:
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(240, 90, 60))
        draw.ellipse([dx - 9, dy - 9, dx + 9, dy + 9], outline=(240, 90, 60), width=2)


def cyclone_panel(draw, x, y, w, h):
    """Spiral storm over a teal sea."""
    draw.rectangle([x, y, x + w, y + h], fill=(204, 226, 228), outline=RULE, width=2)
    import math
    cx, cy = x + w // 2, y + h // 2
    for k in range(5):
        pts = []
        for t in range(0, 540, 6):
            a = math.radians(t)
            r = 6 + t * 0.055 + k * 3
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.85))
        draw.line(pts, fill=(24, 58, 110) if k % 2 == 0 else (240, 240, 240), width=5)
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(158, 27, 24))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    # ---- top dateline bar ----
    d.text((M, 16), "WEDNESDAY 18 NOVEMBER 2026", font=font(SANS_B, 17), fill=INK)
    rt = "ONE DAY  ·  ONE FRONT PAGE"
    d.text((W - M - d.textlength(rt, font=font(SANS_B, 17)), 16), rt,
           font=font(SANS_B, 17), fill=GREY)
    rule(d, M, 44, W - M, 3)
    # ---- masthead ----
    title = "THE EIGHTEENTH"
    tf = font(SERIF_B, 92)
    d.text(((W - d.textlength(title, font=tf)) / 2, 52), title, font=tf, fill=INK)
    sub = "The world's news of Wednesday 18 November 2026 — in one picture"
    sf = font(SERIF, 24)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 152), sub, font=sf, fill=GREY)
    rule(d, M, 192, W - M, 2)
    rule(d, M, 197, W - M, 5)

    # ---- lead story (left, wide) ----
    lx, lw = M, 560
    y = 214
    y = kicker(d, lx, y, "MANILA  ·  DIPLOMACY")
    y = headline(d, lx, y, "TRUMP LANDS IN MANILA FOR QUAD TALKS AHEAD OF CHINA VISIT",
                 36, lw, leading=40)
    y = para(d, lx, y + 8,
             "The US president arrives in the Philippines for talks with Quad "
             "leaders before a visit to China.",
             font(SANS, 18), lw, 24, fill=(52, 50, 46))
    y += 10
    skyline_panel(d, lx, y, lw, 150)
    y += 150 + 12
    d.text((lx, y), "Manila hosts the Quad as summits season peaks.  —  Photo: drawn",
           font=font(SANS, 13), fill=GREY)

    # ---- right column: war + security ----
    rx, rw = M + lw + 28, W - M - (M + lw + 28)
    y = 214
    y = kicker(d, rx, y, "UKRAINE  ·  WAR")
    y = headline(d, rx, y, "UKRAINE HITS CRIMEAN BRIDGE FOR SECOND DAY",
                 24, rw, leading=27)
    y = para(d, rx, y + 6,
             "Kyiv strikes the bridge to Crimea again as Russia pounds bridges "
             "near the capital.",
             font(SANS, 15), rw, 20, fill=(52, 50, 46))
    y += 8
    bridge_panel(d, rx, y, rw, 80)
    y += 80 + 12
    rule(d, rx, y, rx + rw, 1)
    y += 10
    y = kicker(d, rx, y, "BAHRAIN  ·  SECURITY")
    y = headline(d, rx, y, "IRAN DRONES STRIKE US RADAR; BAHRAIN SOUNDS ALL-CLEAR",
                 22, rw, leading=24)
    y = para(d, rx, y + 6,
             "Tehran's drones target a US radar system; Bahrain lifts its "
             "threat warning overnight.",
             font(SANS, 15), rw, 20, fill=(52, 50, 46))
    y += 8
    radar_panel(d, rx, y, rw, 72)

    # ---- middle band: three stories (text only) ----
    rule(d, M, 700, W - M, 2)
    cols = [
        ("TRADE  ·  APEC", "CANADA AND CHINA EXTEND TRADE DEALS",
         "Xi meets Carney ahead of the APEC summit as Ottawa and Beijing "
         "widen trade cooperation."),
        ("BRITAIN  ·  MIDDLE EAST", "UK SANCTIONS FIRMS OVER WEST BANK SETTLEMENTS",
         "London blacklists eight firms in a push to protect the "
         "two-state solution."),
        ("WEATHER  ·  BAY OF BENGAL", "CYCLONE AKVAN GAINS STRENGTH",
         "The storm over the Bay of Bengal is set to intensify into a "
         "severe cyclone by Thursday."),
    ]
    cw = (W - 2 * M - 2 * 24) // 3
    for i, (kick, head, deck) in enumerate(cols):
        cx = M + i * (cw + 24)
        yy = 716
        yy = kicker(d, cx, yy, kick)
        yy = headline(d, cx, yy, head, 21, cw, leading=23)
        yy = para(d, cx, yy + 5, deck, font(SANS, 15), cw, 19,
                  fill=(52, 50, 46))

    # ---- day in brief strip ----
    rule(d, M, 862, W - M, 2)
    y = 876
    d.text((M, y), "THE DAY IN BRIEF", font=font(SANS_B, 16), fill=RED)
    y += 26
    briefs = [
        "Dhoni retires from the IPL; Chennai name him mentor.",
        "Gaza: WFP now gives one hot meal every two days.",
        "Modi presses peace and stability at the ASEAN summit.",
        "Baidu chief warns of an AI bubble ahead of APEC.",
        "Latvia's parliament backs a new Kulbergs cabinet.",
        "UN: at least 372 civilians killed in Ukraine in October.",
    ]
    bx = M
    bw = (W - 2 * M - 20) // 2
    for i, b in enumerate(briefs):
        x = M + (i % 2) * (bw + 20)
        yy = y + (i // 2) * 26
        d.text((x, yy), "•  " + b, font=font(SANS, 15), fill=INK)

    # ---- footer ----
    rule(d, M, 980, W - M, 1)
    foot = ("Sources: Reuters · AP · Hindustan Times · EIN Presswire · Jagran Josh — "
            "stories first reported 18 November 2026  ·  make.fun news-image-20261118")
    d.text((M, 988), foot, font=font(SANS, 12), fill=GREY)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print(f"saved {out}: {img.size}, {size} bytes")
    assert size <= 1_048_576, "over 1 MiB"
