#!/usr/bin/env python3
"""Build poster.png -- "The World Today", Wednesday 18 November 2026.

MAX revision (2026-11-19) of the entry image for make.fun's
news-image-20261118. Same one-page newspaper front page, rebuilt after a
critical audit of the first edition against the day's wire reports
(Reuters / AFP, 18 November 2026):

  * SEQUENCE CORRECTED. The first edition implied the U.S. struck first
    and Iran "hit back". The wires say the opposite order: Revolutionary
    Guard drones targeted a U.S.-operated radar at Bahrain's Sheikh Isa
    Air Base on Tuesday morning; U.S. jets struck the Guard missile
    launch site on Qeshm Island on Tuesday evening in reply; early
    Wednesday, Bahrain and Kuwait intercepted fresh drone/missile waves
    (Ali Al Salem air base, Kuwait, among the targets). No casualties or
    damage were reported from the interceptions.
  * Detail added from the same wires: three U.S. carrier strike groups
    now in the region (Theodore Roosevelt, George H. W. Bush, George
    Washington); five to six explosions heard on Qeshm; Iran's claim --
    unverified, and labelled as such -- to have downed a U.S. MQ-9 drone
    east of the Strait of Hormuz.
  * APEC corrected and enriched: Xi Jinping greeted Donald Trump at the
    airport on his arrival -- the first time Xi has done so for a
    visiting leader -- after Xi and Vladimir Putin attacked sanctions
    and protectionism at the Shenzhen summit; the three-way meeting
    follows on Thursday and has already drawn comparisons with Yalta.
  * Map redrawn: no label sits on a flight path or a shoreline any more;
    every label was checked on the rendered image.
  * Bottom grid tightened so no body text touches a rule.

Stories carried (all from the 18 November 2026 reports):
  * Gulf crisis (lead, above).
  * APEC summit, Shenzhen; Ukraine drops a span of the Kerch Bridge.
  * DR Congo Ebola passes 11,000 cases and 5,400 deaths.
  * The United States loses its measles elimination status after 26 years.
  * NASA's Voyager 1 reaches one light-day from Earth.
  * Grand Theft Auto VI begins its rolling midnight launch.
  * Briefs: Peltola flips Alaska (Senate Democrats reach 56 seats);
    Category 5 Cyclone Xavier hits the Cook Islands; a Russian plane
    crash in Siberia kills 19.

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


def draw_map(draw, y0, height=88):
    """Schematic panel: the Strait of Hormuz and the Gulf.

    Label placement was the first edition's weak point (labels sat on
    the dashed flight paths and on the target marker). Here every label
    has its own clear water: the strait name top-left, the drone label
    mid-left below the Kuwait arc's high point, the target names in the
    water just above their shore dots, and Qeshm's name in the open
    water to the island's right.
    """
    y1 = y0 + height
    draw.rectangle([MARGIN, y0, RIGHT, y1], fill=SEA)
    # North shore: Iran.
    draw.polygon(
        [(MARGIN, y0), (RIGHT, y0), (RIGHT, y0 + 20), (770, y0 + 27),
         (648, y0 + 18), (520, y0 + 28), (398, y0 + 20), (238, y0 + 26),
         (118, y0 + 18), (MARGIN, y0 + 24)],
        fill=SAND,
    )
    # South shore: Arabia.
    draw.polygon(
        [(MARGIN, y1), (MARGIN, y0 + 68), (220, y0 + 63), (420, y0 + 72),
         (560, y0 + 65), (700, y0 + 74), (862, y0 + 67), (RIGHT, y0 + 72),
         (RIGHT, y1)],
        fill=SAND,
    )
    f_land = font(SANS_BOLD, 17)
    draw.text((MARGIN + 14, y0 + 3), "I R A N", font=f_land, fill=INK)
    draw.text((MARGIN + 14, y1 - 20), "A R A B I A", font=f_land, fill=INK)
    # (No in-map "Strait of Hormuz" label: every water position for it is
    # crossed by a shore or a flight arc, so the strait is named in the
    # caption line under the map instead.)

    # Qeshm Island, in the strait; name in the open water to its right.
    qx, qy = 660, y0 + 40
    draw.ellipse([qx - 40, qy - 10, qx + 40, qy + 10], fill=SAND, outline=RED, width=3)
    draw.ellipse([qx - 6, qy - 6, qx + 6, qy + 6], fill=RED)
    f_lab = font(SANS_BOLD, 19)
    draw.text((qx + 56, qy - 25), "QESHM ISLAND", font=f_lab, fill=WHITE)
    draw.text((qx + 56, qy + 0), "U.S. STRIKE", font=f_lab, fill=PALE_RED)

    # Drone arcs: from the Iranian shore down to Bahrain and Kuwait.
    # Targets sit on the south shore; their names float in the water
    # just above each dot, clear of the arcs' endpoints.
    # Bahrain: name in the water above its dot. Kuwait: name on the sand
    # beside its dot -- the water above Kuwait is crossed by its own arc.
    bx, by = 452, y0 + 70
    dashed_arc(draw, (qx - 46, qy + 4), ((qx + bx) / 2, y0 + 6), (bx, by - 9),
               (255, 96, 84), width=4)
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED, outline=WHITE, width=2)
    draw.text((bx - 64, by - 32), "BAHRAIN", font=f_lab, fill=WHITE)
    kx, ky = 172, y0 + 66
    dashed_arc(draw, (qx - 46, qy + 4), ((qx + kx) / 2, y0 + 6), (kx, ky - 9),
               (255, 96, 84), width=4)
    draw.ellipse([kx - 7, ky - 7, kx + 7, ky + 7], fill=RED, outline=WHITE, width=2)
    draw.text((kx + 15, ky + 1), "KUWAIT", font=font(SANS_BOLD, 18), fill=INK)
    draw.text((MARGIN + 14, y0 + 29), "IRANIAN DRONES", font=font(SANS_BOLD, 17),
              fill=PALE_RED)


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
    lead = ["IRAN DRONES HIT U.S. RADAR,", "U.S. JETS ANSWER ON QESHM"]
    f_h1 = fit_font(SERIF_BOLD, lead, RIGHT - MARGIN, 56)
    draw.text((MARGIN, y), lead[0], font=f_h1, fill=INK)
    draw.text((MARGIN, y + 54), lead[1], font=f_h1, fill=INK)
    y += 108
    f_sub = font(SERIF, 24)
    sub = ("Guard drones strike a U.S. radar in Bahrain; U.S. jets reply on "
           "Qeshm. By morning, Bahrain and Kuwait are batting away fresh waves.")
    for line in wrap(draw, sub, f_sub, RIGHT - MARGIN):
        draw.text((MARGIN, y), line, font=f_sub, fill=SOFT)
        y += 27
    y += 2
    draw_map(draw, y)
    y += 88 + 4
    f_cap = fit_font(SANS_BOLD,
                     ["STRAIT OF HORMUZ · 3 U.S. CARRIER GROUPS IN THE REGION · NO CASUALTIES · IRAN CLAIMS MQ-9 DOWNED — UNVERIFIED"],
                     RIGHT - MARGIN, 17)
    draw.text((MARGIN, y), "STRAIT OF HORMUZ · 3 U.S. CARRIER GROUPS IN THE REGION · NO CASUALTIES · IRAN CLAIMS MQ-9 DOWNED — UNVERIFIED",
              font=f_cap, fill=RED)
    y += 20
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
    f_b = font(SERIF, 22)
    left_b = ("Xi greets Trump at the airport — a first — as both "
              "attack sanctions and protectionism.")
    right_b = ("A second day of strikes; part of the Kerch road bridge "
               "falls into the strait.")
    ly = y
    for line in wrap(draw, left_b, f_b, COLW):
        draw.text((MARGIN, ly), line, font=f_b, fill=SOFT)
        ly += 27
    ry = y
    for line in wrap(draw, right_b, f_b, COLW):
        draw.text((X2, ry), line, font=f_b, fill=SOFT)
        ry += 27
    y = max(ly, ry) + 4
    draw.line([MARGIN + COLW + 18, top, MARGIN + COLW + 18, y], fill=INK, width=1)
    draw.rectangle([MARGIN, y, RIGHT, y + 2], fill=INK)
    y += 7

    # --- Bottom grid: four stories with big numbers ---------------------
    gy = y
    cell(draw, MARGIN, gy, "HEALTH · DR CONGO", "11,000",
         "Ebola cases and 5,400 dead; children are hit hardest.")
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
