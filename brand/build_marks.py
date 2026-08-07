import math
IRON,PAPER,MIST,STEEL,BRASS="#14171C","#FAFBFC","#E8EBEF","#7A8494","#E0A32E"

# One continuous silhouette: every junction is a true fillet, not a butt joint.
PROFILE = [
    ((150,424), 22),   # horn tip, softened to a forged point
    ((300,372), 16),   # horn rises into the face
    ((812,372), 14),   # face, far corner
    ((812,470), 14),
    ((652,470), 30),   # face underside filleting into the waist
    ((630,612), 32),   # waist flaring into the base
    ((764,656), 20),
    ((786,700), 15),
    ((786,744), 14),
    ((330,744), 14),
    ((330,700), 15),
    ((348,656), 20),
    ((482,612), 32),
    ((460,470), 30),
    ((300,470), 16),
]

def _lerp(a,b,t): return (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)
def _dist(a,b): return math.hypot(b[0]-a[0], b[1]-a[1])

def rounded_path(profile):
    """Trim each corner by its radius and bridge it with a quadratic — tangent-continuous."""
    n=len(profile); segs=[]
    for i in range(n):
        p_prev = profile[(i-1)%n][0]
        p, r    = profile[i]
        p_next = profile[(i+1)%n][0]
        r = min(r, _dist(p,p_prev)/2.2, _dist(p,p_next)/2.2)
        a = _lerp(p, p_prev, r/_dist(p,p_prev))
        b = _lerp(p, p_next, r/_dist(p,p_next))
        segs.append((a,p,b))
    d = f"M {segs[0][0][0]:.2f},{segs[0][0][1]:.2f}"
    for i,(a,p,b) in enumerate(segs):
        if i: d += f" L {a[0]:.2f},{a[1]:.2f}"
        d += f" Q {p[0]:.2f},{p[1]:.2f} {b[0]:.2f},{b[1]:.2f}"
    return d + " Z"

ANVIL_D = rounded_path(PROFILE)

def anvil(uid, x=0, y=0, scale=1.0, ink=PAPER, heat=BRASS, heat_h=26):
    """Heat is clipped to the silhouette so it follows the filleted top edge exactly."""
    g  = f'<g transform="translate({x},{y}) scale({scale})">'
    g += f'<defs><clipPath id="cp{uid}"><path d="{ANVIL_D}"/></clipPath></defs>'
    g += f'<path d="{ANVIL_D}" fill="{ink}"/>'
    if heat:
        g += f'<rect x="130" y="372" width="700" height="{heat_h}" fill="{heat}" clip-path="url(#cp{uid})"/>'
    return g + '</g>'
