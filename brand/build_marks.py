#!/usr/bin/env python3
"""Generates every CodeForge brand asset from one profile.

Never redraw the silhouette by hand. Edit PROFILE, re-run this, and every asset keeps its
fillets and its optical centring.

    python3 brand/build_marks.py && ls brand/
Requires rsvg-convert and Archivo on the fontconfig path.
"""
import math, os, subprocess

IRON, PAPER, MIST, STEEL = "#14171C", "#FAFBFC", "#E8EBEF", "#7A8494"
BRASS = "#E0A32E"   # heat — the logo accent
OXIDE = "#0E7C7B"   # interface accent: rules, links, focus. Not used inside the logo.

# Silhouette as (vertex, fillet radius). One closed outline, so face, waist and base
# transition the way a cast anvil does instead of being butted together.
PROFILE = [
    ((150, 424), 22),   # horn tip, softened to a forged point
    ((300, 372), 16),   # horn rises into the face
    ((812, 372), 14),
    ((812, 470), 14),
    ((652, 470), 30),   # face underside fillets into the waist
    ((630, 612), 32),   # waist flares into the base
    ((764, 656), 20),
    ((786, 700), 15),
    ((786, 744), 14),
    ((330, 744), 14),
    ((330, 700), 15),
    ((348, 656), 20),
    ((482, 612), 32),
    ((460, 470), 30),
    ((300, 470), 16),
]

# Centred 50/50 between bounding box and area centroid. The horn is thin and the face and
# base carry the mass, so centring on the box alone reads visibly right-heavy.
ANCHOR = (510.3, 551.4)


def _lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
def _dist(a, b): return math.hypot(b[0] - a[0], b[1] - a[1])


def rounded_path(profile=PROFILE):
    n = len(profile); segs = []
    for i in range(n):
        prev = profile[(i - 1) % n][0]
        p, r = profile[i]
        nxt = profile[(i + 1) % n][0]
        r = min(r, _dist(p, prev) / 2.2, _dist(p, nxt) / 2.2)
        segs.append((_lerp(p, prev, r / _dist(p, prev)), p, _lerp(p, nxt, r / _dist(p, nxt))))
    d = f"M {segs[0][0][0]:.2f},{segs[0][0][1]:.2f}"
    for i, (a, p, b) in enumerate(segs):
        if i:
            d += f" L {a[0]:.2f},{a[1]:.2f}"
        d += f" Q {p[0]:.2f},{p[1]:.2f} {b[0]:.2f},{b[1]:.2f}"
    return d + " Z"


D = rounded_path()


def mark(uid, ink=PAPER, heat=BRASS, heat_h=26):
    """Heat is clipped to the silhouette, so it can never drift off the filleted top edge."""
    s = (f'<defs><clipPath id="cp{uid}"><path d="{D}"/></clipPath></defs>'
         f'<path d="{D}" fill="{ink}"/>')
    if heat:
        s += f'<rect x="130" y="372" width="700" height="{heat_h}" fill="{heat}" clip-path="url(#cp{uid})"/>'
    return s


def placed(uid, cx, cy, scale, **kw):
    ax, ay = ANCHOR
    return f'<g transform="translate({cx},{cy}) scale({scale}) translate({-ax},{-ay})">{mark(uid, **kw)}</g>'


def wordmark(x, y, size, ink, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="Archivo" font-weight="700" font-size="{size}"'
            f' fill="{ink}" text-anchor="{anchor}" dominant-baseline="central" letter-spacing="1">'
            f'CODEFORGE<tspan fill="{BRASS}">.</tspan></text>')


def svg(w, h, bg, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


ASSETS = {
    "avatar":       (1024, 1024, svg(1024, 1024, IRON,  placed("av", 512, 512, 1.14))),
    "avatar-light": (1024, 1024, svg(1024, 1024, PAPER, placed("al", 512, 512, 1.14, ink=IRON))),
    "lockup-dark":  (1600, 420,  svg(1600, 420,  IRON,
                     placed("ld", 240, 210, 0.46) + wordmark(460, 210, 104, PAPER))),
    "lockup-light": (1600, 420,  svg(1600, 420,  PAPER,
                     placed("ll", 240, 210, 0.46, ink=IRON) + wordmark(460, 210, 104, IRON))),
    "cover":        (1640, 624,  svg(1640, 624,  IRON,
                     placed("cv", 820, 190, 0.33)
                     + wordmark(820, 374, 104, PAPER, anchor="middle")
                     + f'<rect x="620" y="434" width="400" height="2" fill="{OXIDE}"/>'
                     + f'<text x="820" y="492" font-family="Archivo" font-weight="500" font-size="34"'
                       f' fill="#96A0AE" text-anchor="middle">Software engineering studio</text>'
                     + f'<text x="820" y="544" font-family="Archivo" font-weight="500" font-size="26"'
                       f' fill="{STEEL}" text-anchor="middle" letter-spacing="4">'
                       f'ALBUQUERQUE, NM &#183; EST. 2026</text>')),
}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for name, (w, h, body) in ASSETS.items():
        s = os.path.join(here, f"{name}.svg")
        with open(s, "w") as f:
            f.write(body)
        subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), s,
                        "-o", os.path.join(here, f"{name}.png")], check=True)
        print(f"built {name}")
