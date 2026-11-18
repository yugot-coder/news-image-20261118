#!/usr/bin/env python3
"""Build poster.png -- "The World Today", Wednesday 18 November 2026.

Design source for the entry image of the make.fun competition
news-image-20261118. It renders a one-page newspaper front page with
Pillow, from the day's wire reports (18 November 2026):

  * U.S. jets strike a Revolutionary Guard missile site on Qeshm Island;
    Iran answers with drones against U.S. positions in Bahrain and Kuwait.
  * Xi Jinping and Vladimir Putin open the APEC summit in Shenzhen,
    attacking sanctions and protectionism ahead of three-way talks with
    Donald Trump.
  * Ukraine strikes the Kerch Bridge to Crimea for a second day; part of
    the road span falls into the strait.
  * DR Congo's Ebola outbreak passes 11,000 cases and 5,400 deaths.
  * The United States loses its measles elimination status after 26 years.
  * NASA's Voyager 1 reaches one light-day from Earth.
  * Grand Theft Auto VI begins its rolling midnight launch after record
    pre-orders.
  * Briefs: Peltola flips Alaska (Senate 56-44); Category 5 Cyclone
    Xavier hits the Cook Islands; a Russian military plane crash in
    Siberia kills 19.

This script is run once, at build time, on the author's machine. The
submitted program (main.py) only copies the rendered poster.png, because
the grading sandbox is standard-library only. Rendering is fully
deterministic: fixed canvas, fixed fonts, no clock, no randomness.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
RIGHT = W - MARGIN
COLW = (RIGHT - MARGIN - 36) // 2  # two-column width
X2 = MARGIN + COLW + 36            # second column x

PAPER = (246, 242, 231)
INK = (20, 20, 22)
SOFT = (52, 50, 46)
RED = (172, 30, 36)
SEA = (26, 55, 92)
SAND = (216, 198, 158)
WHITE = (245, 243, 238)
PALE_RED = (255, 176, 166)
FAINT = (196, 190, 174)

FONTS = "/usr/share/fonts/truetype"
SERIF_BOLD = f"{FONTS}/dejavu/DejaVuSerif-Bold.ttf"
SERIF = f"{FONTS}/dejavu/DejaVuSerif.ttf"
SERIF_IT = f"{FONTS}/liberation/LiberationSerif-Italic.ttf"
SANS_BOLD = f"{FONTS}/liberation/LiberationSans-Bold.ttf"
SANS = f"{FONTS}/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(path, lines, max_width, start):
    """Largest size <= start at which every line fits max_width."""
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    size = start
    while size > 8:
        f = font(path, size)
        if all(probe.textlength(t, font=f) <= max_width for t in lines):
            return f
        size -= 2
    return font(path, size)


def tracked(draw, cx, y, text, fnt, fill, tracking=6):
    """Draw text centred on cx with extra letter tracking."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def wrap(draw, text, fnt, max_width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def dashed_arc(draw, p0, p1, p2, fill, width=4, dash=14, gap=10):
    """Dashed quadratic Bezier from p0 to p2 with control point p1."""
    pts = []
    steps = 90
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    dist = 0.0
    pen = True
    for a, b in zip(pts, pts[1:]):
        seg = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        if pen:
            draw.line([a, b], fill=fill, width=width)
        dist += seg
        if pen and dist >= dash:
            pen, dist = False, 0.0
        elif not pen and dist >= gap:
            pen, dist = True, 0.0


def draw_map(draw, y0, height=114):
    """Schematic panel: the Strait of Hormuz and the Gulf."""
    y1 = y0 + height
    draw.rectangle([MARGIN, y0, RIGHT, y1], fill=SEA)
    # North shore: Iran.
    draw.polygon(
        [(MARGIN, y0), (RIGHT, y0), (RIGHT, y0 + 26), (770, y0 + 34),
         (648, y0 + 22), (520, y0 + 36), (398, y0 + 26), (238, y0 + 34),
         (118, y0 + 24), (MARGIN, y0 + 32)],
        fill=SAND,
    )
    # South shore: Arabia.
    draw.polygon(
        [(MARGIN, y1), (MARGIN, y0 + 86), (220, y0 + 80), (420, y0 + 92),
         (560, y0 + 82), (700, y0 + 94), (862, y0 + 84), (RIGHT, y0 + 92),
         (RIGHT, y1)],
        fill=SAND,
    )
    f_land = font(SANS_BOLD, 19)
    draw.text((MARGIN + 16, y0 + 5), "I R A N", font=f_land, fill=INK)
    draw.text((MARGIN + 16, y1 - 25), "A R A B I A", font=f_land, fill=INK)
    draw.text((MARGIN + 262, y0 + 50), "Strait of Hormuz",
              font=font(SERIF_IT, 23), fill=WHITE)
    f_lab = font(SANS_BOLD, 20)
    draw.text((MARGIN + 16, y0 + 45), "IRANIAN DRONES", font=f_lab, fill=PALE_RED)

    # Qeshm Island, in the strait; its labels sit to its right.
    qx, qy = 668, y0 + 47
    draw.ellipse([qx - 38, qy - 10, qx + 38, qy + 10], fill=SAND, outline=RED, width=3)
    draw.ellipse([qx - 6, qy - 6, qx + 6, qy + 6], fill=RED)
    draw.text((qx + 52, qy - 24), "QESHM ISLAND", font=f_lab, fill=WHITE)
    draw.text((qx + 52, qy + 1), "U.S. STRIKE", font=f_lab, fill=PALE_RED)

    # Targets on the south shore: Bahrain and Kuwait.
    targets = [(452, y0 + 88, "BAHRAIN"), (168, y0 + 84, "KUWAIT")]
    for tx, ty, name in targets:
        dashed_arc(draw, (qx - 12, qy + 7), ((qx + tx) / 2, y0 + 16), (tx, ty - 8),
                   (255, 96, 84), width=4)
        draw.ellipse([tx - 7, ty - 7, tx + 7, ty + 7], fill=RED, outline=WHITE, width=2)
        draw.text((tx + 14, ty - 11), name, font=f_lab, fill=INK)


def cell(draw, x, y, kicker, big, body):
    draw.text((x, y), kicker, font=font(SANS_BOLD, 20), fill=RED)
    f_big = fit_font(SERIF_BOLD, [big], COLW, 42)
    draw.text((x, y + 25), big, font=f_big, fill=INK)
    f_body = font(SERIF, 22)
    ly = y + 25 + 44 + 5
    for line in wrap(draw, body, f_body, COLW):
        draw.text((x, ly), line, font=f_body, fill=SOFT)
        ly += 27
    return ly


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    cx = W / 2

    # --- Masthead -------------------------------------------------------
    draw.rectangle([MARGIN, 22, RIGHT, 27], fill=INK)
    draw.rectangle([MARGIN, 30, RIGHT, 32], fill=INK)
    tracked(draw, cx, 38, "WEDNESDAY · 18 NOVEMBER 2026", font(SANS_BOLD, 25), INK, tracking=5)
    f_mast = fit_font(SERIF_BOLD, ["THE WORLD TODAY"], RIGHT - MARGIN, 96)
    draw.text((cx, 66), "THE WORLD TODAY", font=f_mast, fill=INK, anchor="ma")
    draw.rectangle([MARGIN, 163, RIGHT, 166], fill=INK)
    draw.rectangle([MARGIN, 169, RIGHT, 170], fill=INK)

    # --- Lead story -----------------------------------------------------
    y = 174
    draw.text((MARGIN, y), "GULF CRISIS", font=font(SANS_BOLD, 25), fill=RED)
    draw.text((MARGIN + 200, y + 2), "— THE DAY'S TOP STORY", font=font(SANS, 22), fill=SOFT)
    y += 33
    lead = ["U.S. STRIKES IRAN MISSILE SITE,", "IRAN HITS BACK ACROSS THE GULF"]
    f_h1 = fit_font(SERIF_BOLD, lead, RIGHT - MARGIN, 56)
    draw.text((MARGIN, y), lead[0], font=f_h1, fill=INK)
    draw.text((MARGIN, y + 56), lead[1], font=f_h1, fill=INK)
    y += 116
    f_sub = font(SERIF, 25)
    sub = ("U.S. jets hit a Revolutionary Guard missile site on Qeshm Island; "
           "Iran answers with drones on U.S. positions in Bahrain and Kuwait.")
    for line in wrap(draw, sub, f_sub, RIGHT - MARGIN):
        draw.text((MARGIN, y), line, font=f_sub, fill=SOFT)
        y += 30
    y += 2
    draw_map(draw, y)
    y += 114 + 8
    draw.rectangle([MARGIN, y, RIGHT, y + 2], fill=INK)
    y += 12

    # --- Middle band: APEC and Crimea ----------------------------------
    top = y
    draw.text((MARGIN, y), "APEC SUMMIT · SHENZHEN", font=font(SANS_BOLD, 21), fill=RED)
    draw.text((X2, y), "WAR IN EUROPE · CRIMEA", font=font(SANS_BOLD, 21), fill=RED)
    y += 26
    left_h = ["XI & PUTIN ATTACK", "SANCTIONS AT APEC"]
    right_h = ["UKRAINE DROPS A SPAN", "OF THE CRIMEA BRIDGE"]
    f_h2 = fit_font(SERIF_BOLD, left_h + right_h, COLW, 36)
    for i, line in enumerate(left_h):
        draw.text((MARGIN, y + i * 38), line, font=f_h2, fill=INK)
    for i, line in enumerate(right_h):
        draw.text((X2, y + i * 38), line, font=f_h2, fill=INK)
    y += 2 * 38 + 4
    f_b = font(SERIF, 23)
    left_b = ("In Shenzhen they attack sanctions and protectionism; "
              "Trump flies in for talks.")
    right_b = ("A second day of strikes; part of the Kerch road bridge "
               "falls into the strait.")
    ly = y
    for line in wrap(draw, left_b, f_b, COLW):
        draw.text((MARGIN, ly), line, font=f_b, fill=SOFT)
        ly += 28
    ry = y
    for line in wrap(draw, right_b, f_b, COLW):
        draw.text((X2, ry), line, font=f_b, fill=SOFT)
        ry += 28
    y = max(ly, ry) + 4
    draw.line([MARGIN + COLW + 18, top, MARGIN + COLW + 18, y], fill=INK, width=1)
    draw.rectangle([MARGIN, y, RIGHT, y + 2], fill=INK)
    y += 9

    # --- Bottom grid: four stories with big numbers ---------------------
    gy = y
    cell(draw, MARGIN, gy, "HEALTH · DR CONGO", "11,000",
         "Ebola cases; 5,400 dead — children bear the heaviest toll.")
    cell(draw, X2, gy, "SCIENCE · DEEP SPACE", "1 LIGHT-DAY",
         "Voyager 1, 16 billion miles out: its signal takes a full day "
         "to reach Earth.")
    gy2 = gy + 131
    draw.line([MARGIN, gy + 123, RIGHT, gy + 123], fill=FAINT, width=1)
    cell(draw, MARGIN, gy2, "HEALTH · UNITED STATES", "5,400+",
         "Measles cases; U.S. loses its measles-free status of 26 years.")
    cell(draw, X2, gy2, "CULTURE · TONIGHT", "MIDNIGHT",
         "GTA VI unlocks, NZ first, after record PlayStation pre-orders.")
    draw.line([MARGIN + COLW + 18, gy, MARGIN + COLW + 18, gy2 + 117], fill=INK, width=1)

    # --- Footer briefs ---------------------------------------------------
    fy = gy2 + 131
    draw.rectangle([MARGIN, fy, RIGHT, fy + 3], fill=INK)
    f_brief = font(SANS_BOLD, 20)
    briefs = ("ALSO TODAY — Peltola flips Alaska: Senate Democrats reach 56 seats  ·  "
              "Cyclone Xavier, Cat 5, hits the Cook Islands  ·  Russian plane crash in Siberia kills 19")
    lines = wrap(draw, briefs, f_brief, RIGHT - MARGIN)
    for i, line in enumerate(lines):
        draw.text((cx, fy + 7 + i * 25), line, font=f_brief, fill=INK, anchor="ma")
    end = fy + 7 + len(lines) * 25
    assert end <= H - 10, f"layout overflows: {end}"

    out = Path(__file__).resolve().parent / "poster.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
