"""Census of oriented corner/opening configurations around Jamaica Street, Glasgow (OS 1:500, surveyed 1857).

Reads  data/openings_OS1857_Jamaica.csv (62 openings, 12 facades)
       data/trades_1877.csv (directory trades at every orientation of every corner, tested or not; src/chance.py uses the full table)
Writes data/configurations_phase1.csv  (one row per oriented corner x opening on the facing facade)
       paper/tables/numbers.tex, corners.tex, sensitivity.tex (generated, never hand-edited)

Notation (paper, section 3): A = corner block, Y = the street the family looks across, X = the other street,
C = facade facing A across Y, d = offset of the nearer wall of the opening along the axis of Y, measured from the
line through A perpendicular to Y (positive on the side of X), D = distance from A to that wall, angle = atan(d / w_Y).
The model treats Y and X as perpendicular; d_plan and ang_plan measure the same quantities against the recorded face X
(signed distance from the plane of face X, and angle between the line of sight and that face), as a sensitivity.
"""
import csv, math, pathlib, re, sys
import numpy as np
from shapely.geometry import LineString
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from geo import enu, unit, load_openings, P, FACADES

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'; TABLES = ROOT / 'paper' / 'tables'

# Street widths, facade to facade, read with the NLS measuring tool on the 1857 layer (+/- 0.7 m); metres.
# Recomputed from the rounded corner coordinates below, Jamaica gives 22.1 and Howard 12.2 (ratio 1.8-2.2 either way).
WIDTH = {'Jamaica': 22.9, 'Howard': 11.5, 'Ann': 11.5, 'Dixon': 16.0, 'Oswald': 19.9, 'Argyle': 17.5,
         'Fox': 8.7, 'ACL': 3.9, 'StE': 55.1, 'Broomielaw': 20.0, 'GreatClyde': 20.0}
FACADE_CODE = {('Jamaica', 'W'): 'JW', ('Jamaica', 'E'): 'JE', ('Howard', 'N'): 'HN', ('Howard', 'S'): 'HS',
               ('Ann', 'S'): 'AS', ('Ann', 'N'): 'AN', ('Dixon', 'E'): 'DE', ('Dixon', 'W'): 'DW',
               ('Oswald', 'E'): 'OE', ('Oswald', 'W'): 'OW', ('Broomielaw', 'N'): 'BN', ('Great Clyde', 'N'): 'GN'}
TYPE_CODE = {'covered pend': 'pend', 'open recess': 'recess', 'street': 'street', 'lane': 'street', 'square': 'square'}
TYPE_EN = {'pend': 'covered pend', 'recess': 'open recess', 'street': 'street mouth', 'square': 'square'}

# Principal setting: no width-ratio filter. The band 1.5-3 used up to version 1.4 came from a single earlier exploratory
# ChatGPT reading; it is kept only as a sensitivity row. The distance threshold of 20.4 m (12 adult heights) was fixed
# in the author's earlier working dossier (not deposited); it is reported, not applied.
RATIO_MIN, RATIO_MAX, ANGLE_MIN = 0.0, math.inf, 15.0
AUTHOR_RATIO = (1.5, 3.0)
C5_WORKING_M = 20.4
ADULT = 1.7   # metres per adult height, for the D column
# H4-H5 in full: both streets are drawn as carriageways (a cart on Y, ch. 1 p. 7 panel 4; a cobbled roadway and a kerbed
# footway between the bar table and the shop on X, ch. 0), so an orientation with a lane as Y or X is excluded; and the
# stand is at the foot of the clothes shop on face X, so the clothier must have an address on X (select, front=True).
# Neither was coded in the first census of version 1.5; both were added after it returned Argyle x Adam's Court Lane SE.
# lanes=True / front=False give that first coding (and version 1.4).
LANES = {'ACL'}

# Street axes from reference corners (data/corners_reference_OS1857.csv)
JAM = unit(enu(55.85717, -4.25709), enu(55.85826, -4.25669))   # south -> north
HOW = unit(enu(55.85717, -4.25709), enu(55.85693, -4.25585))   # west -> east
ANN = unit(enu(55.85747, -4.25734), enu(55.85761, -4.25959)); ANN = (-ANN[0], -ANN[1])  # west -> east
DIX = unit(enu(55.85614, -4.25608), enu(55.85677, -4.25566))   # south -> north
OSW = unit(enu(55.85667, -4.25989), enu(55.85853, -4.25988))   # south -> north
rot90 = lambda v: (-v[1], v[0]); neg = lambda v: (-v[0], -v[1])

CORNERS = []
def add(name, A, Y, X, uY, v, dirX, fac):
    CORNERS.append(dict(name=name, A=enu(*A), Y=Y, X=X, uY=uY, v=v, dirX=dirX, fac=fac))
W_, E_, N_, S_ = neg(HOW), HOW, JAM, neg(JAM)
add('Jamaica x Howard NE', (55.85717, -4.25709), 'Jamaica', 'Howard', JAM, W_, S_, 'JW')
add('Jamaica x Howard SE', (55.85706, -4.25712), 'Jamaica', 'Howard', JAM, W_, N_, 'JW')
add('Jamaica x Ann NW', (55.85747, -4.25734), 'Jamaica', 'Ann', JAM, E_, S_, 'JE')
add('Jamaica x Ann SW', (55.85737, -4.25738), 'Jamaica', 'Ann', JAM, E_, N_, 'JE')
add('Jamaica x Argyle SE', (55.85826, -4.25669), 'Jamaica', 'Argyle', JAM, W_, N_, 'JW')
add('Jamaica x Argyle SW', (55.85827, -4.25705), 'Jamaica', 'Argyle', JAM, E_, N_, 'JE')
add('Jamaica x Broomielaw NW', (55.85650, -4.25769), 'Jamaica', 'Broomielaw', JAM, E_, S_, 'JE')
add('Jamaica x Great Clyde NE', (55.85647, -4.25734), 'Jamaica', 'GreatClyde', JAM, W_, S_, 'JW')
add('Jamaica x Howard NE (Y = Howard)', (55.85717, -4.25709), 'Howard', 'Jamaica', HOW, S_, W_, 'HS')
add('Jamaica x Howard SE (Y = Howard)', (55.85706, -4.25712), 'Howard', 'Jamaica', HOW, N_, W_, 'HN')
add('Howard x Dixon SW (Y = Howard)', (55.85677, -4.25566), 'Howard', 'Dixon', HOW, N_, E_, 'HN')
add('Howard x Dixon SE (Y = Howard)', (55.85673, -4.25541), 'Howard', 'Dixon', HOW, N_, W_, 'HN')
add("Howard x Adam's Court Lane NW", (55.85701, -4.25630), 'Howard', 'ACL', HOW, S_, E_, 'HS')
add("Howard x Adam's Court Lane NE", (55.85700, -4.25624), 'Howard', 'ACL', HOW, S_, W_, 'HS')
add("Howard x St Enoch's Sq. NW", (55.85693, -4.25585), 'Howard', 'StE', HOW, S_, E_, 'HS')
add("Howard x St Enoch's Sq. NE", (55.85676, -4.25502), 'Howard', 'StE', HOW, S_, W_, 'HS')
AE, AW = ANN, neg(ANN); AN_ = rot90(ANN); AS_ = neg(AN_)
add('Jamaica x Ann NW (Y = Ann)', (55.85747, -4.25734), 'Ann', 'Jamaica', ANN, AS_, AE, 'AS')
add('Jamaica x Ann SW (Y = Ann)', (55.85737, -4.25738), 'Ann', 'Jamaica', ANN, AN_, AE, 'AN')
add('Ann x Oswald NE (Y = Ann)', (55.85761, -4.25959), 'Ann', 'Oswald', ANN, AS_, AW, 'AS')
add('Ann x Oswald SE (Y = Ann)', (55.85751, -4.25959), 'Ann', 'Oswald', ANN, AN_, AW, 'AN')
OWest = rot90(OSW); OEast = neg(OWest)
add('Ann x Oswald NE (Y = Oswald)', (55.85761, -4.25959), 'Oswald', 'Ann', OSW, OWest, neg(OSW), 'OW')
add('Ann x Oswald SE (Y = Oswald)', (55.85751, -4.25959), 'Oswald', 'Ann', OSW, OWest, OSW, 'OW')
add('Oswald x Broomielaw NE', (55.85666, -4.25958), 'Oswald', 'Broomielaw', OSW, OWest, neg(OSW), 'OW')
add('Oswald x Broomielaw NW', (55.85667, -4.25989), 'Oswald', 'Broomielaw', OSW, OEast, neg(OSW), 'OE')
add('Oswald x Argyle SE', (55.85850, -4.25960), 'Oswald', 'Argyle', OSW, OWest, OSW, 'OW')
add('Oswald x Argyle SW', (55.85853, -4.25988), 'Oswald', 'Argyle', OSW, OEast, OSW, 'OE')
DWest = rot90(DIX); DEast = neg(DWest)
add('Howard x Dixon SW (Y = Dixon)', (55.85677, -4.25566), 'Dixon', 'Howard', DIX, DEast, DIX, 'DE')
add('Howard x Dixon SE (Y = Dixon)', (55.85673, -4.25541), 'Dixon', 'Howard', DIX, DWest, DIX, 'DW')
add('Dixon x Fox NE (Y = Dixon)', (55.85641, -4.25562), 'Dixon', 'Fox', DIX, DWest, neg(DIX), 'DW')
add('Dixon x Fox SE (Y = Dixon)', (55.85634, -4.25568), 'Dixon', 'Fox', DIX, DWest, DIX, 'DW')
add('Dixon x Great Clyde NE', (55.85607, -4.25586), 'Dixon', 'GreatClyde', DIX, DWest, neg(DIX), 'DW')
add('Dixon x Great Clyde NW', (55.85614, -4.25608), 'Dixon', 'GreatClyde', DIX, DEast, neg(DIX), 'DE')
# Orientations added in version 1.5 so that every corner of the window is tested wherever its facing frontage is digitised.
ARG = unit(enu(55.85853, -4.25988), enu(55.85817, -4.25587)); ARG_N = rot90(ARG)                    # west -> east along Argyle
ACLu = unit(enu(55.85701, -4.25630), enu(55.85817, -4.25587)); ACL_W = rot90(ACLu); ACL_E = neg(ACL_W)  # south -> north along the lane
STE = unit(enu(55.85693, -4.25585), enu(55.85812, -4.25545)); STE_W = rot90(STE); STE_E = neg(STE_W)     # south -> north along the square
add('Jamaica x Argyle SE (Y = Argyle)', (55.85826, -4.25669), 'Argyle', 'Jamaica', ARG, ARG_N, neg(ARG), 'RN')
add('Jamaica x Argyle SW (Y = Argyle)', (55.85827, -4.25705), 'Argyle', 'Jamaica', ARG, ARG_N, ARG, 'RN')
add("Argyle x Adam's Court Lane SW", (55.85817, -4.25587), 'Argyle', 'ACL', ARG, ARG_N, ARG, 'RN')
add("Argyle x Adam's Court Lane SE", (55.85817, -4.25580), 'Argyle', 'ACL', ARG, ARG_N, neg(ARG), 'RN')
add("Argyle x St Enoch's Sq. SW", (55.85812, -4.25545), 'Argyle', 'StE', ARG, ARG_N, ARG, 'RN')
add("Argyle x St Enoch's Sq. SE", (55.85795, -4.25500), 'Argyle', 'StE', ARG, ARG_N, neg(ARG), 'RN')
add("Argyle x Adam's Court Lane SW (Y = ACL)", (55.85817, -4.25587), 'ACL', 'Argyle', ACLu, ACL_E, ACLu, 'LE')
add("Argyle x Adam's Court Lane SE (Y = ACL)", (55.85817, -4.25580), 'ACL', 'Argyle', ACLu, ACL_W, ACLu, 'LW')
add("Howard x Adam's Court Lane NW (Y = ACL)", (55.85701, -4.25630), 'ACL', 'Howard', ACLu, ACL_E, neg(ACLu), 'LE')
add("Howard x Adam's Court Lane NE (Y = ACL)", (55.85700, -4.25624), 'ACL', 'Howard', ACLu, ACL_W, neg(ACLu), 'LW')
add("Howard x St Enoch's Sq. NW (Y = StE)", (55.85693, -4.25585), 'StE', 'Howard', STE, STE_E, neg(STE), 'QE')
add("Howard x St Enoch's Sq. NE (Y = StE)", (55.85676, -4.25502), 'StE', 'Howard', STE, STE_W, neg(STE), 'QW')
add("Argyle x St Enoch's Sq. SW (Y = StE)", (55.85812, -4.25545), 'StE', 'Argyle', STE, STE_E, STE, 'QE')
add("Argyle x St Enoch's Sq. SE (Y = StE)", (55.85795, -4.25500), 'StE', 'Argyle', STE, STE_W, STE, 'QW')
# In the window but not testable. Across the quay street (the Broomielaw, Great Clyde St) lie the river quay and the approach
# to Glasgow Bridge: no frontage, so no watching point in this census (H5's panel draws a building edge and a kerbed footway
# on the watchers' side). Other facing frontages are not digitised. All these corners still enter the chance population
# through data/trades_1877.csv, which has a row for every orientation.
QUAY = 'river quay or bridge approach across Y: no frontage, no watching point'
UNTESTED = {'Jamaica x Broomielaw NW (Y = Broomielaw)': QUAY, 'Jamaica x Great Clyde NE (Y = Great Clyde)': QUAY,
            'Oswald x Broomielaw NE (Y = Broomielaw)': QUAY, 'Oswald x Broomielaw NW (Y = Broomielaw)': QUAY,
            'Dixon x Great Clyde NE (Y = Great Clyde)': QUAY, 'Dixon x Great Clyde NW (Y = Great Clyde)': QUAY,
            'Broomielaw x Wood Lane NE (Y = Broomielaw)': QUAY, 'Broomielaw x Wood Lane NW (Y = Broomielaw)': QUAY,
            'Broomielaw x Wood Lane NE (Y = Wood Lane)': 'Y is a lane; its frontages not digitised',
            'Broomielaw x Wood Lane NW (Y = Wood Lane)': 'Y is a lane; its frontages not digitised',
            'Oswald x Argyle SE (Y = Argyle)': 'Argyle N west of Alston St not digitised', 'Oswald x Argyle SW (Y = Argyle)': 'Argyle N west of Alston St not digitised',
            'Dixon x Fox NE (Y = Fox)': 'Fox St frontages not digitised', 'Dixon x Fox SE (Y = Fox)': 'Fox St frontages not digitised'}

# Facing frontage of each facade code: every point of it is a possible watching point (principal census);
# the openings recorded on the 1857 plan are a subset, kept as a sensitivity and for the distances quoted in the text.
FRONT = {'JW': ['Jamaica W (south of Ann)', 'Jamaica W (north of Ann)'], 'JE': ['Jamaica E (north of Howard)', 'Jamaica E (south of Howard)'],
         'HN': ['Howard N (west of ACL)', 'Howard N (east of ACL)'], 'HS': ['Howard S', 'Howard S (east of Dixon)'],
         'AN': ['Ann N'], 'AS': ['Ann S'], 'DE': ['Dixon E (north of Fox)', 'Dixon E (south of Fox)'], 'DW': ['Dixon W'],
         'OE': ['Oswald E (south of Ann)', 'Oswald E (north of Ann)'], 'OW': ['Oswald W'],
         'BN': ['Broomielaw N (east of Wood)', 'Broomielaw N (west of Wood)'], 'GN': ['Great Clyde N'],
         'RN': ['Argyle N', 'Argyle N (Union-Mitchell)'], 'LW': ['ACL W'], 'LE': ['ACL E'], 'QW': ['Square W'], 'QE': ['Square E']}
STEP = 0.5   # metres between sampled watching points along a frontage

def frontage_points():
    """Points every STEP metres along each facing frontage (shapely), in the same form as the recorded openings."""
    out = []
    for code, names in FRONT.items():
        for name in names:
            line = LineString(FACADES[name])
            for s in np.arange(0.0, line.length + 1e-9, STEP):
                p = line.interpolate(s); xy = (p.x, p.y)
                out.append(dict(id=f'{name} @ {s:.1f} m', fac=code, type='frontage', w=0.0, p1=xy, p2=xy, kind='frontage'))
    return out

# Face X of each oriented corner, as a frontage of geo.FACADES that starts or ends at A (plan-angle sensitivity).
# None: that frontage was not recorded; the perpendicular approximation is kept for the corner.
FACE_X = {'Jamaica x Howard NE': 'Howard N (west of ACL)', 'Jamaica x Howard SE': 'Howard S', 'Jamaica x Ann NW': 'Ann N',
          'Jamaica x Ann SW': 'Ann S', 'Jamaica x Argyle SE': 'Argyle S (east of Jamaica)', 'Jamaica x Argyle SW': 'Argyle S (west of Jamaica)',
          'Jamaica x Broomielaw NW': 'Broomielaw N (east of Wood)', 'Jamaica x Great Clyde NE': 'Great Clyde N',
          'Jamaica x Howard NE (Y = Howard)': 'Jamaica E (north of Howard)', 'Jamaica x Howard SE (Y = Howard)': 'Jamaica E (south of Howard)',
          'Howard x Dixon SW (Y = Howard)': 'Dixon W', 'Howard x Dixon SE (Y = Howard)': 'Dixon E (north of Fox)',
          "Howard x Adam's Court Lane NW": 'ACL W', "Howard x Adam's Court Lane NE": 'ACL E',
          "Howard x St Enoch's Sq. NW": 'Square W', "Howard x St Enoch's Sq. NE": 'Square E',
          'Jamaica x Ann NW (Y = Ann)': 'Jamaica W (north of Ann)', 'Jamaica x Ann SW (Y = Ann)': 'Jamaica W (south of Ann)',
          'Ann x Oswald NE (Y = Ann)': 'Oswald E (north of Ann)', 'Ann x Oswald SE (Y = Ann)': 'Oswald E (south of Ann)',
          'Ann x Oswald NE (Y = Oswald)': 'Ann N', 'Ann x Oswald SE (Y = Oswald)': 'Ann S',
          'Oswald x Broomielaw NE': 'Broomielaw N (west of Wood)', 'Oswald x Broomielaw NW': None,
          'Oswald x Argyle SE': 'Argyle S (west of Jamaica)', 'Oswald x Argyle SW': None,
          'Howard x Dixon SW (Y = Dixon)': 'Howard S', 'Howard x Dixon SE (Y = Dixon)': 'Howard S (east of Dixon)',
          'Dixon x Fox NE (Y = Dixon)': None, 'Dixon x Fox SE (Y = Dixon)': None,
          'Dixon x Great Clyde NE': None, 'Dixon x Great Clyde NW': 'Great Clyde N',
          'Jamaica x Argyle SE (Y = Argyle)': 'Jamaica E (north of Howard)', 'Jamaica x Argyle SW (Y = Argyle)': 'Jamaica W (north of Ann)',
          "Argyle x Adam's Court Lane SW": 'ACL W', "Argyle x Adam's Court Lane SE": 'ACL E',
          "Argyle x St Enoch's Sq. SW": 'Square W', "Argyle x St Enoch's Sq. SE": 'Square E',
          "Argyle x Adam's Court Lane SW (Y = ACL)": 'Argyle S (east of Jamaica)', "Argyle x Adam's Court Lane SE (Y = ACL)": None,
          "Howard x Adam's Court Lane NW (Y = ACL)": 'Howard N (west of ACL)', "Howard x Adam's Court Lane NE (Y = ACL)": 'Howard N (east of ACL)',
          "Howard x St Enoch's Sq. NW (Y = StE)": 'Howard N (east of ACL)', "Howard x St Enoch's Sq. NE (Y = StE)": None,
          "Argyle x St Enoch's Sq. SW (Y = StE)": None, "Argyle x St Enoch's Sq. SE (Y = StE)": None}

def face_x(c):
    """Unit vector along face X from A, or None when the frontage was not recorded."""
    f = FACE_X[c['name']]
    if f is None: return None
    p, q = FACADES[f]
    near, far = (p, q) if math.dist(p, c['A']) < math.dist(q, c['A']) else (q, p)
    assert math.dist(near, c['A']) < 1.0, (c['name'], f)
    return unit(c['A'], far)

OPS = []
def run():
    ops = OPS; ops.clear()
    for o in load_openings(DATA / 'openings_OS1857_Jamaica.csv'):
        ops.append(dict(id=o['id'], fac=FACADE_CODE[(o['street'], o['side'])], type=TYPE_CODE[o['type']], w=o['w'], p1=o['p1'], p2=o['p2'], kind='opening'))
    ops += frontage_points()
    rows = []
    for c in CORNERS:
        perp = rot90(c['uY'])
        sv = 1 if (c['v'][0]*perp[0] + c['v'][1]*perp[1]) > 0 else -1
        v = (sv*perp[0], sv*perp[1])          # perpendicular to Y, towards the facing facade
        left = rot90(v)
        sx = 1 if (c['dirX'][0]*c['uY'][0] + c['dirX'][1]*c['uY'][1]) > 0 else -1
        dirX = (sx*c['uY'][0], sx*c['uY'][1])
        # C2: seen from A facing the far facade, X lies to the left; seen from the opening facing A, X is on the right.
        chir = (dirX[0]*left[0] + dirX[1]*left[1]) > 0
        w, s = WIDTH[c['Y']], WIDTH[c['X']]
        for o in ops:
            if o['fac'] != c['fac']: continue
            t1 = (o['p1'][0]-c['A'][0])*left[0] + (o['p1'][1]-c['A'][1])*left[1]
            t2 = (o['p2'][0]-c['A'][0])*left[0] + (o['p2'][1]-c['A'][1])*left[1]
            # The positive side is the side beyond X. ``left`` points that way only for the
            # retained handedness; for the opposite handedness the axis and nearer wall reverse.
            if chir:
                near = o['p1'] if t1 < t2 else o['p2']; d = min(t1, t2)
            else:
                near = o['p1'] if t1 > t2 else o['p2']; d = -max(t1, t2)
            D = math.hypot(near[0]-c['A'][0], near[1]-c['A'][1])
            ang = math.degrees(math.atan2(d, w)) if d > 0 else 0.0
            ex = face_x(c)
            if ex is None:
                d_plan, ang_plan = d, ang
            else:   # outward normal of face X, pointing away from the block (whose face Y runs along -dirX)
                n = rot90(ex)
                if n[0]*-dirX[0] + n[1]*-dirX[1] > 0: n = neg(n)
                d_plan = (near[0]-c['A'][0])*n[0] + (near[1]-c['A'][1])*n[1]
                ang_plan = math.degrees(math.asin(d_plan / D)) if d_plan > 0 else 0.0
            rows.append(dict(corner=c['name'], Y=c['Y'], X=c['X'], chir=chir, ratio=w/s, open=o['id'], otype=o['type'], ow=o['w'], d=d, D=D, ang=ang,
                             d_plan=d_plan, ang_plan=ang_plan, kind=o['kind']))
    return rows

def physical(name): return name.split(' (Y =')[0]

def filters(rows, rmin=RATIO_MIN, rmax=RATIO_MAX, amin=ANGLE_MIN, chir=True, wshift=0.0, dmax=None, plan=False, points='frontage', lanes=False):
    """Cumulative filters. points='frontage': every point of the facing frontage and every recorded opening may be the
    watching point (principal); points='openings': only the openings recorded on the 1857 plan (version 1.4 census).
    wshift widens Y and narrows X by that amount (width uncertainty).
    plan=True measures visibility and viewing angle against the recorded face X instead of the perpendicular model.
    lanes=False drops the orientations whose Y or X is a lane (principal); lanes=True keeps them (first coding)."""
    if points == 'openings': rows = [r for r in rows if r['kind'] == 'opening']
    if not lanes: rows = [r for r in rows if r['Y'] not in LANES and r['X'] not in LANES]
    def ratio(r): return (WIDTH[r['Y']] + wshift) / (WIDTH[r['X']] - wshift)
    def ang(r):
        if plan: return r['ang_plan']
        return math.degrees(math.atan2(r['d'], WIDTH[r['Y']] + wshift)) if r['d'] > 0 else 0.0
    c1 = [r for r in rows if (r['d_plan'] if plan else r['d']) > 0]
    c12 = [r for r in c1 if r['chir']] if chir else c1
    c123 = [r for r in c12 if rmin <= ratio(r) <= rmax]
    c123a = [r for r in c123 if ang(r) >= amin]
    if dmax is not None: c123a = [r for r in c123a if r['D'] <= dmax]
    return c1, c12, c123, c123a

def load_trades():
    with open(DATA / 'trades_1877.csv', encoding='utf-8') as f:
        return {r['corner']: r for r in csv.DictReader(f, delimiter=';')}

def select(survivors, trades, front=True):
    """Documentary step: among the orientations that survive the geometry, those with a clothier at the corner and
    licensed premises facing the stand (data/trades_1877.csv); front=True also requires the clothier to have an address
    on X. Returns (orientation names in order of D, winners)."""
    corners = []
    for r in sorted(survivors, key=lambda r: r['D']):
        if r['corner'] not in corners: corners.append(r['corner'])
    missing = [c for c in corners if c not in trades]
    if missing: raise ValueError(f'no directory line for {missing} in data/trades_1877.csv')
    allowed = {'yes', 'no', 'partial', 'unknown', 'n/a'}
    for c in corners:
        if not {trades[c]['corner_clothier'], trades[c]['clothier_on_x'], trades[c]['facing_licensed']} <= allowed: raise ValueError(f'bad code for {c}')
    winners = [c for c in corners if trades[c]['corner_clothier'] == 'yes' and trades[c]['facing_licensed'] == 'yes'
               and (not front or trades[c]['clothier_on_x'] == 'yes')]
    return corners, winners

def tex(s): return ''.join({'&': r'\&', '%': r'\%', '#': r'\#', '_': r'\_', '$': r'\$'}.get(ch, ch) for ch in s)
def occupant(text):
    """Short occupant name for the table: the firm or 'Surname, Initials', or the first clause of a note."""
    if 'not identified' in text[:40] or 'no clothier' in text[:20]: return 'not identified'
    text = text.split(':')[0] if text.startswith(('not ', 'no ')) else text.split(' (')[0]
    parts = [x.strip() for x in text.split(',')]
    return parts[0] if '&' in parts[0] or len(parts) == 1 else f'{parts[0]}, {parts[1]}'
def short(name): return re.sub(r' \(Y = \w+\)', '', name).replace(' x ', ' $\\times$ ').replace("Adam's Court Lane", 'ACL').replace("St Enoch's Sq.", 'St Enoch Sq.')

CAND = 'Jamaica x Howard NE'
def write_tables(rows):
    TABLES.mkdir(parents=True, exist_ok=True)
    trades = load_trades()
    hand = filters(rows)[3]; nohand = filters(rows, chir=False)[3]
    _, win_hand = select(hand, trades); _, win_nohand = select(nohand, trades)
    hand1 = filters(rows, lanes=True)[3]; nohand1 = filters(rows, chir=False, lanes=True)[3]     # first coding
    _, win_hand1 = select(hand1, trades, front=False); order, win_nohand1 = select(nohand1, trades, front=False)
    surv_hand = {r['corner'] for r in hand1}
    lane = lambda name: next(c['Y'] in LANES or c['X'] in LANES for c in CORNERS if c['name'] == name)
    # Table: every orientation that passes the geometry with or without the handedness convention (lanes included), with its trades
    L = ['\\begin{tabular}{>{\\raggedright\\arraybackslash}p{3.0cm}crr>{\\raggedright\\arraybackslash}p{3.6cm}>{\\raggedright\\arraybackslash}p{3.6cm}}', '\\toprule',
         'Corner A (Y / X) & Hand. & $D$ (m) & 1857 &  At the corner, 1877--78 & Facing the stand across X, 1877--78 \\\\', '\\midrule']
    for name in order:
        t = trades[name]; b = min((r for r in nohand1 if r['corner'] == name), key=lambda r: r['D'])
        ops = [r for r in nohand1 if r['corner'] == name and r['kind'] == 'opening']
        op = min(ops, key=lambda r: r['D'])['open'] if ops else '--'
        bold = (lambda s: f'\\textbf{{{s}}}') if name in win_nohand else (lambda s: s)
        onx = f", on X: {t['clothier_on_x']}" if t['corner_clothier'] == 'yes' and t['clothier_on_x'] != 'yes' else ''
        L.append(f"{bold(short(name))}{'$^\\dagger$' if lane(name) else ''} ({b['Y']} / {b['X']}) & {'yes' if name in surv_hand else 'no'} & {b['D']:.0f} & {op} & "
                 f"{tex(occupant(t['corner_trade']))}: {t['corner_clothier']}{onx} & {tex(occupant(t['facing_trade']))}: {t['facing_licensed']} \\\\")
    L += ['\\bottomrule', '\\end{tabular}']
    (TABLES / 'corners.tex').write_text('\n'.join(L) + '\n')
    # Table: sensitivity of the geometric step
    variants = [('every frontage point, handedness kept', dict()), ('every frontage point, no handedness', dict(chir=False)),
                ('first coding: lanes kept, clothier anywhere at the corner', dict(lanes=True, front=False)),
                ('first coding, no handedness', dict(chir=False, lanes=True, front=False)),
                ('1857 openings only, first coding (version 1.4 without its width-ratio filter)', dict(points='openings', lanes=True, front=False)),
                ('1857 openings only, width ratio 1.5--3, first coding (version 1.4 as published)',
                 dict(points='openings', lanes=True, front=False, rmin=AUTHOR_RATIO[0], rmax=AUTHOR_RATIO[1])),
                ('1857 openings only, no handedness', dict(points='openings', chir=False)),
                ('width ratio 1.5--3 (used up to version 1.4)', dict(rmin=AUTHOR_RATIO[0], rmax=AUTHOR_RATIO[1])),
                ('angle $\\ge 10^\\circ$', dict(amin=10.0)), ('angle $\\ge 25^\\circ$', dict(amin=25.0)),
                ('widths: $Y$ $+0.7$~m, $X$ $-0.7$~m', dict(wshift=0.7)), ('widths: $Y$ $-0.7$~m, $X$ $+0.7$~m', dict(wshift=-0.7)),
                ('visibility and angle measured on the plan', dict(plan=True)),
                (f"distance $D \\le {C5_WORKING_M:g}$~m (author's earlier rule)", dict(dmax=C5_WORKING_M))]
    L = ['\\begin{tabular}{>{\\raggedright\\arraybackslash}p{7cm}rrl}', '\\toprule', 'Geometric setting & Corners & With both trades & Jamaica $\\times$ Howard NE kept \\\\', '\\midrule']
    sens = {}
    for label, kw in variants:
        kw = dict(kw); front = kw.pop('front', True)
        s = filters(rows, **kw)[3]; _, w = select(s, trades, front)
        cs = {physical(r['corner']) for r in s}; ws = {physical(n) for n in w}
        sens[label] = (len(cs), len(ws), CAND in cs)
        L.append(f"{label} & {len(cs)} & {len(ws)} & {'yes' if CAND in cs else 'no'} \\\\")
    L += ['\\bottomrule', '\\end{tabular}']
    (TABLES / 'sensitivity.tex').write_text('\n'.join(L) + '\n')
    # Numbers quoted in the text
    o1, o12, o123, o123a = filters(rows, points='openings', lanes=True)
    best = min((r for r in o123a if r['corner'] == CAND), key=lambda r: r['D'])      # JW6, the recorded opening nearest the candidate
    near = min((r for r in hand if r['corner'] == CAND), key=lambda r: r['D'])        # nearest admissible frontage point
    c1, c12, _, _ = filters(rows)
    plan = filters(rows, plan=True)[3]
    ja, jh = FACADES['Jamaica E (north of Howard)'], FACADES['Howard N (west of ACL)']
    ea, eh = unit(ja[0], ja[1]), unit(jh[0], jh[1])
    phys_all = {physical(n) for n in trades}
    m = {'nOpenings': len([o for o in OPS if o['kind'] == 'opening']), 'nUniverse': len([r for r in rows if r['kind'] == 'opening']),
         'nCone': len(o1), 'nCtwo': len(o12), 'nAngle': len(o123a), 'nCorners': len({physical(r['corner']) for r in o123a}),
         'nOrient': len(CORNERS), 'nUntested': len(UNTESTED), 'nUntestedQuay': sum(v == QUAY for v in UNTESTED.values()), 'nPhysicalWindow': len(phys_all),
         'nOrientCone': len({r['corner'] for r in c1}), 'nOrientTwo': len({r['corner'] for r in c12}), 'nOrientAngle': len({r['corner'] for r in hand}),
         'nSurv': len({physical(r['corner']) for r in hand}), 'nSurvNoHand': len({physical(r['corner']) for r in nohand}),
         'nWin': len({physical(n) for n in win_hand}), 'nWinNoHand': len({physical(n) for n in win_nohand}),
         'nSurvFirst': len({physical(r['corner']) for r in hand1}), 'nSurvNoHandFirst': len({physical(r['corner']) for r in nohand1}),
         'nWinFirst': len({physical(n) for n in win_hand1}), 'nWinNoHandFirst': len({physical(n) for n in win_nohand1}),
         'nLaneOrient': len([c for c in CORNERS if c['Y'] in LANES or c['X'] in LANES]),
         'nPlanSurv': len({physical(r['corner']) for r in plan}),
         'nCfiveWorking': sens[f"distance $D \\le {C5_WORKING_M:g}$~m (author's earlier rule)"][0], 'CfiveWorking': f'{C5_WORKING_M:g}',
         'SfourD': f"{best['D']:.1f}", 'SfourH': f"{best['D']/ADULT:.0f}", 'Sfourd': f"{best['d']:.1f}", 'SfourAngle': f"{best['ang']:.0f}",
         'SfourAnglePlan': f"{best['ang_plan']:.0f}", 'SfourOpen': best['open'], 'nSfourAdmissible': len([r for r in o123a if r['corner'] == CAND]),
         'DnearJH': f"{near['D']:.0f}", 'DnearJHH': f"{near['D']/ADULT:.0f}", 'SfourWidth': f"{best['ow']:.1f}",
         'DPHSE': f"{math.dist(P['PH1893'], CORNERS[1]['A']):.0f}",   # the 1892-94 "P.H." from the SE corner of Jamaica x Howard
         'nCornersRatio': sens['1857 openings only, width ratio 1.5--3, first coding (version 1.4 as published)'][0],
         'nBroomielawNW': len([r for r in rows if r['corner'] == 'Jamaica x Broomielaw NW' and r['kind'] == 'opening']),
         'WidthJamaica': f"{WIDTH['Jamaica']:.1f}", 'WidthHoward': f"{WIDTH['Howard']:.1f}", 'WidthACL': f"{WIDTH['ACL']:.1f}",
         'RatioJH': f"{WIDTH['Jamaica'] / WIDTH['Howard']:.1f}", 'RatioMirror': f"{WIDTH['Howard'] / WIDTH['Jamaica']:.2f}",
         'DPaisleyA': f"{math.dist(P['PAISLEY'], CORNERS[0]['A']):.0f}",
         'CornerAngleJH': f"{math.degrees(math.acos(ea[0]*eh[0] + ea[1]*eh[1])):.0f}"}
    (TABLES / 'numbers.tex').write_text(''.join(f'\\newcommand{{\\{k}}}{{{v}}}\n' for k, v in m.items()))
    return dict(win_hand=win_hand, win_nohand=win_nohand, win_hand1=win_hand1, win_nohand1=win_nohand1, surv_hand=surv_hand, order=order, best=best, sens=sens)

def write_configurations(rows):
    with open(DATA / 'configurations_phase1.csv', 'w', newline='') as f:   # the recorded-opening configurations only
        ops = [{k: v for k, v in r.items() if k != 'kind'} for r in rows if r['kind'] == 'opening']
        wr = csv.DictWriter(f, fieldnames=list(ops[0].keys()), delimiter=';', lineterminator='\n'); wr.writeheader(); wr.writerows(ops)

if __name__ == '__main__':
    rows = run()
    write_configurations(rows)
    out = write_tables(rows)
    print('both trades, handedness kept:', out['win_hand'], '| without handedness:', out['win_nohand'])
    print('first coding:', out['win_hand1'], '|', out['win_nohand1'])
    for k, v in out['sens'].items(): print(f'  {k:60s} corners {v[0]:2d}  both trades {v[1]}  candidate kept {v[2]}')
