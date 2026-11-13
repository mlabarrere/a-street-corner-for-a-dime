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
c = P['PAISLEY']
ax.plot(*c, marker='o', color='#1a5fb4', ms=6, zorder=6); ax.text(c[0]-4, c[1]-4, "Paisley's corner\n(1890s)", fontsize=6.5, color='#1a5fb4', zorder=6, ha='right', va='top')
Cn = P['JW6_N']; Bb = P['PH1893']   # B at the "P.H." of the 1892-94 plan
ax.plot([Cn[0], A0[0]], [Cn[1], A0[1]], color='#534ab7', lw=1.0, ls='--', zorder=7)
ax.plot(*A0, marker='s', color='#1d9e75', ms=7, zorder=8); ax.text(A0[0]+5, A0[1]+5, 'A', fontsize=8, fontweight='bold', color='#1d9e75', zorder=8)
ax.plot(*Bb, marker='D', color='#ba7517', ms=6, zorder=8); ax.text(Bb[0]+5, Bb[1]-9, 'B', fontsize=8, fontweight='bold', color='#ba7517', zorder=8)
ax.plot(*Cn, marker='^', color='#534ab7', ms=7, zorder=8); ax.text(Cn[0]-12, Cn[1]-3, 'C', fontsize=8, fontweight='bold', color='#534ab7', zorder=8)
from matplotlib.lines import Line2D
hand = [Line2D([], [], color='#b3261e', lw=3, label='covered pend or open recess (OS 1857)'), Line2D([], [], color='#b3261e', lw=0.8, label='street mouth'),
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

# ---- Figure 1: the three views reduced to their geometry (edges, faces, stand, watchers, sight lines). No lettering, pose,
# prop or staging is taken from the drawings; the panels themselves remain (c) Disney and are not reproduced.
def frame(ax, title):
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 10, fill=False, edgecolor=INK, lw=1.2)); ax.set_title(title, fontsize=8, loc='left')
def label(ax, x, y, s, **kw): ax.text(x, y, s, fontsize=7, ha='center', va='center', color=kw.pop('color', '#333'), **kw)
def box(ax, pts, fc='#eeeae0'): ax.add_patch(Polygon(pts, closed=True, facecolor=fc, edgecolor=INK, lw=0.9))
def stand(ax, x, y): ax.add_patch(Rectangle((x, y), 0.6, 0.45, facecolor='#8a5a3c', edgecolor=INK, lw=0.6, zorder=3))
def watchers(ax, pts): [ax.plot(*q, marker='o', color='#534ab7', ms=6, zorder=4) for q in pts]
def sight(ax, a, b): ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', ls='--', color='#534ab7', lw=0.9))

fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.75))
ax = axs[0]; frame(ax, 'P0: from B, across X')                      # the X face of A seen frontally from the licensed premises
box(ax, [(1.0, 4.6), (10.0, 4.6), (10.0, 9.6), (1.0, 9.6)])
box(ax, [(0.0, 4.6), (1.0, 4.6), (1.0, 9.6), (0.0, 9.6)], fc='#d9d4c8')
ax.plot([1.0, 1.0], [4.6, 9.6], color=INK, lw=2.6); ax.plot([0, 10], [4.0, 4.0], color='#888', lw=0.8)
stand(ax, 1.6, 4.6); ax.plot(7.6, 1.6, marker='D', color='#ba7517', ms=7)
sight(ax, (7.4, 1.9), (2.1, 4.5)); label(ax, 5.2, 3.3, 'street X', color='#777')
label(ax, 5.5, 8.6, 'A (face X)', fontweight='bold'); label(ax, 8.6, 1.0, 'B', fontweight='bold', color='#ba7517')
ax = axs[1]; frame(ax, 'P1: the corner (A)')                         # the corner edge seen obliquely, both faces in view
box(ax, [(4.2, 3.0), (4.2, 9.5), (0.0, 8.6), (0.0, 3.9)], fc='#e6e1d6')
box(ax, [(4.2, 3.0), (4.2, 9.5), (10.0, 8.9), (10.0, 3.5)], fc='#f0ece2')
ax.plot([4.2, 4.2], [3.0, 9.5], color=INK, lw=2.6); ax.plot([0, 4.2, 10], [2.2, 3.0, 2.7], color='#888', lw=0.8)
stand(ax, 5.0, 3.0); watchers(ax, [(0.6, 0.6), (1.3, 0.4)]); sight(ax, (1.5, 0.8), (4.9, 3.1))
label(ax, 2.1, 9.0, 'A', fontweight='bold'); label(ax, 9.5, 2.3, 'X', fontweight='bold'); label(ax, 0.5, 3.3, 'Y', fontweight='bold'); label(ax, 3.4, 0.45, 'watchers', color='#534ab7')
ax = axs[2]; frame(ax, 'P2: the hiding place')                      # their own wall and corner edge, a roadway, the boy at A beyond it
box(ax, [(0.0, 0.0), (3.0, 0.0), (3.0, 10.0), (0.0, 10.0)], fc='#c9c4b8')
ax.plot([3.0, 3.0], [0.0, 10.0], color=INK, lw=2.2)
box(ax, [(6.4, 3.6), (10.0, 3.3), (10.0, 10.0), (6.4, 10.0)], fc='#f0ece2')
ax.plot([6.4, 6.4], [3.6, 10.0], color=INK, lw=2.2); ax.plot([6.4, 10.0], [3.35, 3.05], color='#999', lw=0.7)
stand(ax, 7.4, 3.5); watchers(ax, [(0.9, 1.0), (1.9, 1.2), (2.7, 1.4)]); sight(ax, (2.9, 1.6), (7.3, 3.7))
label(ax, 1.5, 9.2, 'wall'); label(ax, 8.2, 9.2, 'A', fontweight='bold'); label(ax, 4.8, 2.3, 'roadway', color='#777')
label(ax, 1.7, 0.35, 'watchers', color='#534ab7'); label(ax, 8.4, 2.6, 'stand')
fig.savefig(OUT / 'fig01_sketches.pdf', bbox_inches='tight'); plt.close(fig)
print('sketches ok')
