"""Vector figures for the paper (PDF): the situation plan, the corner plan (from geo.py and the census),
and three schematic readings of the panels (layout only; nothing traced from the drawings)."""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from geo import *
from census import WIDTH
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'paper' / 'figures'; OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'pdf.fonttype': 42})
INK, BLOCK = '#222', '#e6e1d6'
OPEN = load_openings(ROOT / 'data' / 'openings_OS1857_Jamaica.csv')

def base(ax, labels=True, openings=True):
    for poly in BLOCKS.values():
        ax.add_patch(Polygon(poly, closed=True, facecolor=BLOCK, edgecolor='none', zorder=1))
    for pts in FACADES.values():
        xs, ys = zip(*pts); ax.plot(xs, ys, color=INK, lw=1.0, zorder=3, solid_capstyle='round')
    if openings:
        for o in OPEN:
            if o['type'] in ('covered pend', 'open recess'):
                xs, ys = zip(o['p1'], o['p2']); ax.plot(xs, ys, color='#b3261e', lw=3, zorder=4, solid_capstyle='butt')
    if labels:
        for txt, (lat, lon), rot in [('JAMAICA STREET', (55.85770, -4.25720), 78), ('HOWARD STREET', (55.85697, -4.25640), -19),
                                     ('ANN STREET', (55.85748, -4.25830), -10), ('BROOMIELAW', (55.85652, -4.25870), -10),
                                     ('GREAT CLYDE ST', (55.85630, -4.25660), -19), ('DIXON ST', (55.85650, -4.25580), 80),
                                     ('OSWALD STREET', (55.85740, -4.25975), 90), ('ARGYLE STREET', (55.85838, -4.25740), -10),
                                     ("ADAM'S COURT LANE", (55.85755, -4.25610), 80), ("ST ENOCH'S SQUARE", (55.85720, -4.25540), 0)]:
            x, y = enu(lat, lon); ax.text(x, y, txt, rotation=rot, ha='center', va='center', fontsize=6.5, color='#555', zorder=5)

def finish(ax, x0, x1, y0, y1, scale=20, scale_left=False):
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect('equal'); ax.axis('off')
    sx, sy = (x0 + 6, y0 + 6) if scale_left else (x1 - scale - 6, y0 + 6)
    ax.plot([sx, sx + scale], [sy, sy], color=INK, lw=2); ax.text(sx + scale/2, sy + 2, f'{scale} m', ha='center', fontsize=7)
    ax.annotate('', xy=(x1-8, y1-6), xytext=(x1-8, y1-18), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1)); ax.text(x1-8, y1-4, 'N', ha='center', fontsize=7)

# ---- Map of the quarter: the surveyed area on the 1857 plan, the 62 openings, Paisley's, and the corner retained (A, B, C)
fig, ax = plt.subplots(figsize=(7.2, 6.3))
uJ = U_JAM; pw = (-uJ[1], uJ[0]); A0 = P['JH_NE']
river = [(P['JB_NW'][0]-160*pw[0]-12*uJ[0], P['JB_NW'][1]-160*pw[1]-12*uJ[1]), (P['JGC_NE'][0]+160*pw[0]-12*uJ[0], P['JGC_NE'][1]+160*pw[1]-12*uJ[1]),
         (P['JGC_NE'][0]+160*pw[0]-120*uJ[0], P['JGC_NE'][1]+160*pw[1]-120*uJ[1]), (P['JB_NW'][0]-160*pw[0]-120*uJ[0], P['JB_NW'][1]-160*pw[1]-120*uJ[1])]
ax.add_patch(Polygon(river, closed=True, facecolor='#d6e4ee', edgecolor='none', zorder=0)); ax.text(A0[0]+40*pw[0]-128*uJ[0], A0[1]+40*pw[1]-128*uJ[1], 'River Clyde', fontsize=8, color='#5a7d99', style='italic', zorder=5)
for sgn in (1, -1):
    b0 = (A0[0]+sgn*11*pw[0]-102*uJ[0], A0[1]+sgn*11*pw[1]-102*uJ[1]); b1 = (A0[0]+sgn*11*pw[0]-257*uJ[0], A0[1]+sgn*11*pw[1]-257*uJ[1])
    ax.plot([b0[0], b1[0]], [b0[1], b1[1]], color='#555', lw=1.2, zorder=2)
ax.text(A0[0]+18*pw[0]-140*uJ[0], A0[1]+18*pw[1]-140*uJ[1], 'Glasgow Bridge', fontsize=6.5, color='#555', rotation=78, zorder=5, ha='center', va='center')
base(ax)
for o in OPEN:   # street mouths and the square, thin; pends and recesses are drawn thick by base()
    if o['type'] not in ('covered pend', 'open recess'):
        xs, ys = zip(o['p1'], o['p2']); ax.plot(xs, ys, color='#b3261e', lw=0.8, zorder=4)
c = P['PAISLEY']; ax.add_patch(Circle(c, 200, fill=False, ls='--', lw=0.8, color='#888', zorder=2))
ax.plot(*c, marker='o', color='#1a5fb4', ms=6, zorder=6); ax.text(c[0]-4, c[1]-4, "Paisley's corner\n(from 1885)", fontsize=6.5, color='#1a5fb4', zorder=6, ha='right', va='top')
Cn = P['JW6_N']; Bb = P['PH1893']   # B at the "P.H." of the 1892-94 plan
ax.plot([Cn[0], A0[0]], [Cn[1], A0[1]], color='#534ab7', lw=1.0, ls='--', zorder=7)
ax.plot(*A0, marker='s', color='#1d9e75', ms=7, zorder=8); ax.text(A0[0]+5, A0[1]+5, 'A', fontsize=8, fontweight='bold', color='#1d9e75', zorder=8)
ax.plot(*Bb, marker='D', color='#ba7517', ms=6, zorder=8); ax.text(Bb[0]+5, Bb[1]-9, 'B', fontsize=8, fontweight='bold', color='#ba7517', zorder=8)
ax.plot(*Cn, marker='^', color='#534ab7', ms=7, zorder=8); ax.text(Cn[0]-12, Cn[1]-3, 'C', fontsize=8, fontweight='bold', color='#534ab7', zorder=8)
from matplotlib.lines import Line2D
hand = [Line2D([], [], color='#b3261e', lw=3, label='covered pend or open recess (OS 1857)'), Line2D([], [], color='#b3261e', lw=0.8, label='street mouth'),
        Line2D([], [], color='#888', lw=0.8, ls='--', label="200 m reference circle (not the survey boundary)"),
        Line2D([], [], marker='s', ls='', color='#1d9e75', label='A: corner, clothier (1877–78)'), Line2D([], [], marker='D', ls='', color='#ba7517', label='B: spirit dealer facing the stand'),
        Line2D([], [], marker='^', ls='', color='#534ab7', label='C: covered pend JW6 (OS 1857), a possible watching point')]
ax.legend(handles=hand, loc='lower right', fontsize=6.5, frameon=True, framealpha=0.95, edgecolor='#aaa')
finish(ax, -200, 172, -175, 168, scale=50, scale_left=True)
fig.savefig(OUT / 'fig02_situation.pdf', bbox_inches='tight'); plt.close(fig)

# ---- Figure 2: the corner, measured (plan, true scale)
fig, ax = plt.subplots(figsize=(7.2, 6.4))
plt.rcParams.update({'font.size': 9})
base(ax, labels=False)
A = P['JH_NE']; jw6 = next(o for o in OPEN if o['id'] == 'JW6'); Fn = jw6['p1']; Fs = jw6['p2']; uH = U_HOW; uJ = U_JAM; pw = (-uJ[1], uJ[0])
AF = (Fn[0]-A[0], Fn[1]-A[1])
cross_sep = abs(AF[0]*pw[0] + AF[1]*pw[1])
along_sep = abs(AF[0]*uJ[0] + AF[1]*uJ[1])
model_D = math.hypot(cross_sep, along_sep)
ax.plot([A[0], A[0]+pw[0]*30], [A[1], A[1]+pw[1]*30], color='#777', lw=0.7, ls=':')
ax.plot([Fn[0], A[0]], [Fn[1], A[1]], color='#534ab7', lw=1.2)
mid = ((Fn[0]+A[0])/2, (Fn[1]+A[1])/2); ax.text(mid[0]-1, mid[1]+2, f'D = {model_D:.1f} m', fontsize=7.5, color='#534ab7', rotation=-30)
model_angle = math.degrees(math.atan2(along_sep, WIDTH['Jamaica']))   # the census's angle, streets treated as perpendicular
fh = unit(A, P['HACL_NW']); sight = unit(Fn, A); plan_angle = math.degrees(math.acos(sight[0]*fh[0] + sight[1]*fh[1]))   # on the plan, against the Howard face
ax.text(Fn[0]+10, Fn[1]-7.5, f'{model_angle:.0f}° (model)\n{plan_angle:.0f}° (plan)', fontsize=6.5, color='#534ab7', va='top')
foot = (A[0]+pw[0]*cross_sep, A[1]+pw[1]*cross_sep)
ax.annotate('', xy=Fn, xytext=foot, arrowprops=dict(arrowstyle='<->', color='#777', lw=0.7)); ax.text(foot[0]+1.5, (foot[1]+Fn[1])/2, f'd = {along_sep:.1f} m', fontsize=7, color='#555', ha='left')
ax.annotate('', xy=foot, xytext=A, arrowprops=dict(arrowstyle='<->', color='#777', lw=0.7)); ax.text((foot[0]+A[0])/2, A[1]+4.5, f'coordinate separation {cross_sep:.1f} m', fontsize=6.5, color='#555', ha='center')
hs = P['JH_SE']; ax.text(A[0]+18, A[1]+9, f"viewer measurements:\nJamaica {WIDTH['Jamaica']} ± 0.7 m\nHoward {WIDTH['Howard']} ± 0.7 m", fontsize=6.5, color='#555', ha='left')
ax.plot(*A, marker='s', color='#1d9e75', ms=7, zorder=7); ax.text(A[0]+22, A[1]+22, 'block A\n51–53 Jamaica St / 1–9 Howard St\nMorrison, clothier (PO Directory 1877–78)\n"Warehouses" (OS 1857)', fontsize=7, color='#333')
# the pend JW6 drawn as what the plan shows: a 2.8 m x 12 m covered passage through the block, a small court behind, a lamp at its south corner
L_PEND = 12.0
pend = [Fn, Fs, (Fs[0]+L_PEND*pw[0], Fs[1]+L_PEND*pw[1]), (Fn[0]+L_PEND*pw[0], Fn[1]+L_PEND*pw[1])]
ax.add_patch(Polygon(pend, closed=True, facecolor='#c9c4b8', edgecolor=INK, lw=0.8, zorder=4, hatch='////'))
court = [(Fn[0]+L_PEND*pw[0]+1.5*uJ[0], Fn[1]+L_PEND*pw[1]+1.5*uJ[1]), (Fs[0]+L_PEND*pw[0]-1.5*uJ[0], Fs[1]+L_PEND*pw[1]-1.5*uJ[1]),
         (Fs[0]+(L_PEND+5)*pw[0]-1.5*uJ[0], Fs[1]+(L_PEND+5)*pw[1]-1.5*uJ[1]), (Fn[0]+(L_PEND+5)*pw[0]+1.5*uJ[0], Fn[1]+(L_PEND+5)*pw[1]+1.5*uJ[1])]
ax.add_patch(Polygon(court, closed=True, facecolor='white', edgecolor=INK, lw=0.8, zorder=4))
ax.text(court[3][0]-1, court[3][1]+1.5, 'court, spiral stair', fontsize=6, color='#555', zorder=8, ha='left')
for k in range(3):   # three watchers (father and two daughters), if placed at the north wall of the pend
    q = (Fn[0]+(1.2+1.1*k)*pw[0]-0.5*uJ[0], Fn[1]+(1.2+1.1*k)*pw[1]-0.5*uJ[1]); ax.plot(*q, marker='o', color='#534ab7', ms=4, zorder=7)
ax.annotate('', xy=(A[0]-1.0*uJ[0], A[1]-1.0*uJ[1]), xytext=(Fn[0]+0.3*pw[0]-0.6*uJ[0], Fn[1]+0.3*pw[1]-0.6*uJ[1]), arrowprops=dict(arrowstyle='-|>', color='#534ab7', lw=0.8, ls='--'), zorder=7)
ax.text(Fn[0]-40, Fn[1]-13, 'C: covered pend JW6, 2.8 m wide, about 12 m long\n(drawn on OS 1857; frontage continuous on OS 1893;\nstate in 1877 unknown). A possible watching point.', fontsize=6.5, color='#534ab7', ha='left', zorder=8)
bar = P['PH1893']
ax.plot(*bar, marker='D', color='#ba7517', ms=6, zorder=7); ax.text(bar[0]+2, bar[1]-2, 'B: 6 Howard St\nTurner, spirit dealer (1877–78)\nplaced at the "P.H." of OS 1893', fontsize=7, color='#ba7517', zorder=7)
ax.text(hs[0]+24, hs[1]-20, 'Custom House block\n57 Jamaica St / 2 Howard St', fontsize=7, color='#333')
ax.text(Fn[0]-36, Fn[1]+24, 'west side of Jamaica St\n54–62 Jamaica St; "Smith\'s Court, 62" (index 1877)\n"Iron Warehouse" (OS 1857)', fontsize=7, color='#333')
ax.text(Fn[0]-8, Fn[1]-27, '"Colosseum", "Hall" (JW7)', fontsize=7, color='#333', ha='right')
ax.plot(*P['LP_JW6'], marker='o', color='#555', ms=3, zorder=8); ax.text(P['LP_JW6'][0]+1, P['LP_JW6'][1]-1.5, 'lamp (OS 1857)', fontsize=6, color='#555')
ax.text(A[0]-5, A[1]+30, 'JAMAICA STREET', rotation=78, fontsize=7, color='#777', ha='center'); ax.text(A[0]+30, A[1]-9, 'HOWARD STREET', rotation=-19, fontsize=7, color='#777')
finish(ax, -62, 52, -44, 40, scale=10)
fig.savefig(OUT / 'fig03_corner.pdf', bbox_inches='tight'); plt.close(fig)

# ---- Figure: original sketches of the three panels (layout only: boxes, silhouettes, arrows; nothing traced from the drawings)
from matplotlib.patches import Ellipse, Circle as _Circle
def silhouette(ax, x, y, h=1.0, lying=False, color=INK):
    if lying:
        ax.add_patch(Ellipse((x, y), h*0.9, h*0.3, facecolor=color, edgecolor='none')); return
    ax.plot([x, x], [y, y+h*0.62], color=color, lw=2.2, solid_capstyle='round')
    ax.add_patch(Ellipse((x, y+h*0.8), h*0.26, h*0.32, facecolor=color, edgecolor='none'))
def frame(ax, title):
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 10, fill=False, edgecolor=INK, lw=1.2)); ax.set_title(title, fontsize=8, loc='left')
def label(ax, x, y, s, **kw): ax.text(x, y, s, fontsize=7, ha='center', va='center', color=kw.pop('color', '#333'), **kw)
def box(ax, pts, **kw): ax.add_patch(Polygon(pts, closed=True, facecolor=kw.pop('fc', '#eeeae0'), edgecolor=INK, lw=0.9, **kw))

fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.75))
def collapsed(ax, x, y, s=1.0):
    """The boy on his back on the pavement, head towards x, legs in the air."""
    k = dict(color=INK, lw=2.0, solid_capstyle='round')
    ax.add_patch(_Circle((x, y + 0.18*s), 0.22*s, facecolor=INK, edgecolor='none'))            # head
    ax.plot([x + 0.2*s, x + 1.1*s], [y + 0.12*s, y + 0.12*s], **k)                                # body, flat
    ax.plot([x + 1.1*s, x + 1.45*s, x + 1.55*s], [y + 0.12*s, y + 0.75*s, y + 1.05*s], **k)       # leg up
    ax.plot([x + 1.1*s, x + 1.65*s, x + 1.9*s], [y + 0.12*s, y + 0.55*s, y + 0.8*s], **k)         # other leg up
    ax.plot([x + 0.55*s, x + 0.35*s], [y + 0.12*s, y + 0.55*s], color=INK, lw=1.4, solid_capstyle='round')   # arm flung up
    ax.plot([x + 0.65*s, x + 0.95*s], [y + 0.12*s, y - 0.05*s], color=INK, lw=1.4, solid_capstyle='round')   # arm flat

# P0: the visitor at a table in licensed premises B looks across narrow street X at the clothes shop SOU'S;
# the corner edge is on the left; the boy lies collapsed at the foot of the shop, by the corner, next to his box
ax = axs[0]; frame(ax, "P0: from B, across X")
box(ax, [(1.0, 5.0), (10.0, 5.0), (10.0, 9.6), (1.0, 9.6)], fc='#e9d3c8')                 # brick front of the shop (X face of A)
for yy in np.arange(5.45, 9.6, 0.45): ax.plot([1.0, 10.0], [yy, yy], color='#d4b8aa', lw=0.4, zorder=1.2)   # brick courses
ax.add_patch(Rectangle((0.0, 5.0), 1.0, 4.6, facecolor='#d9c3b6', edgecolor=INK, lw=0.6))   # the other face (Y), foreshortened
ax.plot([1.0, 1.0], [5.0, 9.6], color=INK, lw=2.6)                                           # corner edge
ax.add_patch(Rectangle((3.3, 8.35), 3.2, 0.8, facecolor='white', edgecolor=INK, lw=0.8, zorder=2)); label(ax, 4.9, 8.75, "SOU'S", fontweight='bold', zorder=3)
ax.add_patch(Rectangle((2.4, 5.5), 3.0, 2.5, facecolor='white', edgecolor=INK, lw=0.7, zorder=2))     # display window
ax.add_patch(Rectangle((5.9, 5.0), 1.5, 3.0, facecolor='white', edgecolor=INK, lw=0.7, zorder=2)); ax.plot([6.65, 6.65], [5.0, 8.0], color=INK, lw=0.5, zorder=2.1)   # double door
ax.add_patch(Rectangle((7.9, 5.5), 1.8, 2.5, facecolor='white', edgecolor=INK, lw=0.7, zorder=2))     # second window
ax.plot([0, 10], [4.1, 4.1], color='#888', lw=0.8)                                           # kerb
collapsed(ax, 1.5, 4.35, s=0.95)                                                              # the boy, flat out on the pavement
ax.add_patch(Rectangle((3.65, 4.3), 0.75, 0.5, facecolor='#8a5a3c', edgecolor=INK, lw=0.6))  # his box
label(ax, 6.8, 3.6, 'street X (narrow)', color='#777')
ax.plot([0.0, 4.6], [1.9, 1.9], color=INK, lw=1.6); ax.plot([2.3, 2.3], [0.0, 1.9], color=INK, lw=1.1)   # table edge
ax.add_patch(Rectangle((0.8, 1.95), 0.55, 0.75, facecolor='white', edgecolor=INK, lw=0.8)); ax.plot([1.35, 1.55, 1.55, 1.35], [2.5, 2.5, 2.15, 2.15], color=INK, lw=0.8)   # mug
ax.add_patch(Ellipse((7.4, 2.25), 1.0, 1.15, facecolor=INK, edgecolor='none'))               # the visitor, back of the head
ax.add_patch(Polygon([(6.3, 0.0), (8.6, 0.0), (8.1, 1.75), (6.7, 1.75)], closed=True, facecolor=INK, edgecolor='none'))   # shoulders
ax.annotate('', xy=(2.4, 4.7), xytext=(6.9, 2.6), arrowprops=dict(arrowstyle='-|>', ls='--', color='#534ab7', lw=0.9))
label(ax, 9.4, 0.5, 'B', fontweight='bold', color='white'); label(ax, 9.4, 9.15, 'A', fontweight='bold'); label(ax, 9.5, 3.4, 'X', fontweight='bold')
# P1 (ch. 1 p. 7 panel 4): the corner edge in the middle, the boy and his stand on the X face; the watchers' heads cut by the lower
# left edge of the frame: they see the corner from the side, never from in front of the boy
ax = axs[1]; frame(ax, 'P1: the corner (A)')
box(ax, [(4.2, 3.0), (4.2, 9.5), (0.0, 8.6), (0.0, 3.9)], fc='#e6e1d6')            # face Y (left, receding)
box(ax, [(4.2, 3.0), (4.2, 9.5), (10.0, 8.9), (10.0, 3.5)], fc='#f0ece2')          # face X (right, long, seen obliquely)
ax.plot([4.2, 4.2], [3.0, 9.5], color=INK, lw=2.6)                                  # corner edge
for y0 in (5.3, 7.3):
    ax.add_patch(Polygon([(1.0, y0), (2.4, y0 - 0.15), (2.4, y0 + 1.05), (1.0, y0 + 1.2)], closed=True, facecolor='white', edgecolor=INK, lw=0.6))
    for x0 in (5.4, 7.6):
        ax.add_patch(Polygon([(x0, y0 - 0.2), (x0 + 1.3, y0 - 0.25), (x0 + 1.3, y0 + 0.9), (x0, y0 + 0.95)], closed=True, facecolor='white', edgecolor=INK, lw=0.6))
ax.plot([0, 4.2, 10], [2.2, 3.0, 2.7], color='#888', lw=0.8)                        # pavement edge along both faces
silhouette(ax, 5.1, 3.0, h=1.15)                                                     # the boy, standing at his stand
ax.add_patch(Rectangle((5.5, 3.0), 0.55, 0.42, facecolor='#8a5a3c', edgecolor=INK, lw=0.6))
for (x0, y0) in ((0.25, 0.25), (1.0, 0.05)):                                         # watchers' heads, cut by the frame, at the far left
    ax.add_patch(Ellipse((x0, y0), 0.8, 1.0, facecolor='#3a3a5a', edgecolor='none', clip_on=True))
ax.annotate('', xy=(4.9, 3.25), xytext=(1.2, 0.7), arrowprops=dict(arrowstyle='-|>', ls='--', color='#534ab7', lw=0.9))
label(ax, 3.4, 0.45, 'watchers', color='#534ab7')
label(ax, 2.1, 9.0, 'A', fontweight='bold'); label(ax, 9.5, 2.3, 'X', fontweight='bold'); label(ax, 0.5, 3.3, 'Y', fontweight='bold')
# P2 (ch. 1 p. 6 panel 6; p. 7 panel 6 and the pencil draft agree): the hiding place as drawn. A brick wall in shade, frontal, over 0.62 of the width; a quoined corner pier at
# 0.62-0.70, full height; beyond it the far face recedes. The family stand with their backs to the wall, cut at the chest by the
# frame, the father nearest the pier looking round it; the boy sits at the foot of the far face, beyond the pier, by his box; the customer
# walks in from the right, shovel on his shoulder. No street is drawn between them: the pier is not labelled A, and the geometry follows P1 (see Section 4).
ax = axs[2]; frame(ax, 'P2: the hiding place')
box(ax, [(0.0, 0.0), (6.2, 0.0), (6.2, 10.0), (0.0, 10.0)], fc='#c9c4b8')                  # the wall in shade
for yy in np.arange(0.6, 10.0, 0.6): ax.plot([0.0, 6.2], [yy, yy], color='#b5b0a4', lw=0.4, zorder=1.2)   # brick courses
box(ax, [(7.0, 3.6), (10.0, 3.3), (10.0, 10.0), (7.0, 10.0)], fc='#f0ece2')               # the far face, beyond the pier
ax.add_patch(Rectangle((6.2, 3.0), 0.8, 7.0, facecolor='white', edgecolor=INK, lw=0.9, zorder=2))   # the quoined pier
for k, yy in enumerate(np.arange(3.0, 10.0, 0.55)):
    ax.plot([6.2, 7.0], [yy, yy], color=INK, lw=0.4, zorder=2.1)
    if k % 2: ax.plot([6.68, 6.68], [yy, yy + 0.55], color=INK, lw=0.4, zorder=2.1)
ax.plot([6.2, 6.2], [0.0, 10.0], color=INK, lw=2.2, zorder=3)                               # the corner edge
ax.plot([7.0, 10.0], [3.05, 2.7], color='#999', lw=0.7)                                       # kerb along the far face
silhouette(ax, 7.75, 3.45, h=0.9)                                                             # the boy, seated small at the foot of the far face
ax.add_patch(Rectangle((8.15, 3.42), 0.4, 0.3, facecolor='#8a5a3c', edgecolor=INK, lw=0.5, zorder=3))
silhouette(ax, 9.35, 3.2, h=2.3, color='#ba7517'); ax.plot([9.35, 8.75], [4.75, 5.55], color='#ba7517', lw=1.2)   # the customer, shovel on his shoulder
ax.annotate('', xy=(8.6, 2.9), xytext=(9.6, 2.85), arrowprops=dict(arrowstyle='-|>', color='#ba7517', lw=1.0))
for (x0, w, ys, hw, hh) in ((1.2, 1.5, 1.9, 1.05, 1.25), (3.0, 1.7, 2.5, 1.15, 1.4), (5.0, 2.1, 3.6, 1.4, 1.7)):   # the family, backs to the wall, cut at the chest by the frame
    ax.add_patch(Polygon([(x0 - w/2, 0.0), (x0 + w/2, 0.0), (x0 + 0.4*w, ys), (x0 - 0.4*w, ys)], closed=True, facecolor='#3a3a5a', edgecolor='none', zorder=5))
    ax.add_patch(Ellipse((x0, ys + 0.5*hh), hw, hh, facecolor='#3a3a5a', edgecolor='none', zorder=5))
ax.annotate('', xy=(7.55, 4.6), xytext=(5.8, 4.7), arrowprops=dict(arrowstyle='-|>', ls='--', color='#534ab7', lw=0.9, connectionstyle='arc3,rad=-0.3'))
label(ax, 1.6, 9.2, 'wall', color='#333'); label(ax, 8.6, 9.2, 'corner', color='#333', zorder=6); ax.plot([7.75, 7.05], [9.2, 9.2], color='#333', lw=0.6, zorder=6); label(ax, 2.4, 6.2, 'watchers', color='#534ab7')
label(ax, 7.9, 2.2, 'boy', color='#333'); label(ax, 9.2, 6.4, 'customer', color='#ba7517')
fig.savefig(OUT / 'fig01_sketches.pdf', bbox_inches='tight'); plt.close(fig)
print('sketches ok')
