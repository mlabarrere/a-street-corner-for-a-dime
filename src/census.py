"""Census of oriented corner/opening configurations around Jamaica Street, Glasgow (OS 1:500, surveyed 1857).

Reads  data/openings_OS1857_Jamaica.csv (62 openings, 12 facades)
       data/trades_1877.csv (directory trades of the corners that survive the geometric filters)
Writes data/configurations_phase1.csv  (one row per oriented corner x opening on the facing facade)
       paper/tables/numbers.tex, corners5.tex, sensitivity.tex (generated, never hand-edited)

Notation (paper, section 3): A = corner block, Y = the street the family looks across, X = the other street,
C = facade facing A across Y, d = offset of the nearer wall of the opening along the axis of Y, measured from the
line through A perpendicular to Y (positive on the side of X), D = distance from A to that wall, angle = atan(d / w_Y).
The model treats Y and X as perpendicular; d_plan and ang_plan measure the same quantities against the recorded face X
(signed distance from the plane of face X, and angle between the line of sight and that face), as a sensitivity.
"""
import csv, math, pathlib, sys
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

# Thresholds recorded in the author's working notes before the final census. The width-ratio band was adopted by the
# author from a single earlier exploratory ChatGPT reading; the replicated model readings gave 0.4-1.6 (see sensitivity). The distance threshold of 20.4 m
# (12 adult heights) was fixed in the author's earlier working dossier (not deposited) as a rule: a drawn distance clearly
# below it would leave no configuration in the window. The model readings' widest envelope is 17 m. Both are reported, neither applied.
RATIO_MIN, RATIO_MAX, ANGLE_MIN = 1.5, 3.0, 15.0
MODEL_RATIO = (0.4, 1.6)            # range of the five central readings
MODEL_RATIO_ENVELOPE = (0.2, 4.0)   # envelope of their individual intervals
C5_ENVELOPE_M, C5_WORKING_M = 17.0, 20.4
ADULT = 1.7   # metres per adult height, for the D column

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
          'Dixon x Great Clyde NE': None, 'Dixon x Great Clyde NW': 'Great Clyde N'}

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
        ops.append(dict(id=o['id'], fac=FACADE_CODE[(o['street'], o['side'])], type=TYPE_CODE[o['type']], w=o['w'], p1=o['p1'], p2=o['p2']))
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
                             d_plan=d_plan, ang_plan=ang_plan))
    return rows

def filters(rows, rmin=RATIO_MIN, rmax=RATIO_MAX, amin=ANGLE_MIN, chir=True, wshift=0.0, dmax=None, plan=False):
    """Cumulative filters. wshift widens Y and narrows X by that amount (width uncertainty).
    plan=True measures visibility and viewing angle against the recorded face X instead of the perpendicular model."""
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

def select(survivors, trades):
    """Documentary step: among the corners that survive the geometry, keep those with a clothier at the corner
    and licensed premises facing the stand (data/trades_1877.csv). Returns (corner names in order of D, winners)."""
    corners = []
    for r in sorted(survivors, key=lambda r: r['D']):
        if r['corner'] not in corners: corners.append(r['corner'])
    missing = [c for c in corners if c not in trades]
    assert not missing, f'no directory line for {missing} in data/trades_1877.csv'
    allowed = {'yes', 'no', 'partial', 'unknown'}
    for c in corners:
        assert trades[c]['corner_clothier'] in allowed, (c, trades[c]['corner_clothier'])
        assert trades[c]['facing_licensed'] in allowed, (c, trades[c]['facing_licensed'])
    winners = [c for c in corners if trades[c]['corner_clothier'] == 'yes' and trades[c]['facing_licensed'] == 'yes']
    return corners, winners

def tex(s): return s.replace('&', '\\&')
def write_tables(rows, c1, c12, c123, c123a):
    TABLES.mkdir(parents=True, exist_ok=True)
    trades = load_trades()
    corners, winners = select(c123a, trades)
    assert len(winners) == 1, winners
    win = winners[0]
    best = min((r for r in c123a if r['corner'] == win), key=lambda r: r['D'])   # nearest admissible opening (a choice, stated in the paper)
    # Table: the corners that pass the geometry, with their directory trades
    L = ['\\begin{tabular}{>{\\raggedright\\arraybackslash}p{2.7cm}>{\\raggedright\\arraybackslash}p{1.8cm}rr>{\\raggedright\\arraybackslash}p{3.9cm}>{\\raggedright\\arraybackslash}p{3.8cm}}', '\\toprule',
         'Corner A (Y / X) & Nearest opening & $D$ (m) & Angle & At the corner, 1877--78 & Facing the stand across X, 1877--78 \\\\', '\\midrule']
    for name in corners:
        t = trades[name]; b = min((r for r in c123a if r['corner'] == name), key=lambda r: r['D'])
        n_op = len([r for r in c123a if r['corner'] == name])
        short = name.replace(' (Y = Howard)', '').replace(' (Y = Dixon)', '').replace(' (Y = Oswald)', '').replace(' (Y = Ann)', '').replace(' x ', ' $\\times$ ')
        bold = (lambda s: f'\\textbf{{{s}}}') if name == win else (lambda s: s)
        L.append(f"{bold(short)} ({b['Y']} / {b['X']}) & {b['open']}, {TYPE_EN[b['otype']]} ({n_op} admissible) & {b['D']:.1f} & {b['ang']:.0f}$^\\circ$ & "
                 f"{tex(t['corner_trade'])}: clothier {t['corner_clothier']} & {tex(t['facing_trade'])}: licensed {t['facing_licensed']} \\\\")
    L += ['\\bottomrule', '\\end{tabular}']
    (TABLES / 'corners5.tex').write_text('\n'.join(L) + '\n')
    # Table: sensitivity of the geometric step to the parameters the paper controls, and to the two readings it does not
    variants = [('as published: ratio 1.5--3, angle $\\ge 15^\\circ$', dict()),
                ('ratio 1.2--4.0', dict(rmin=1.2, rmax=4.0)), ('ratio 1.8--2.5', dict(rmin=1.8, rmax=2.5)),
                ('angle $\\ge 10^\\circ$', dict(amin=10.0)), ('angle $\\ge 25^\\circ$', dict(amin=25.0)),
                ('widths: $Y$ $+0.7$~m, $X$ $-0.7$~m', dict(wshift=0.7)), ('widths: $Y$ $-0.7$~m, $X$ $+0.7$~m', dict(wshift=-0.7)),
                ('no handedness constraint', dict(chir=False)),
                ('no width-ratio constraint', dict(rmin=0.0, rmax=math.inf)),
                ('ratio 0.4--1.6 (aggregate model reading)', dict(rmin=MODEL_RATIO[0], rmax=MODEL_RATIO[1])),
                ('ratio 0.2--4.0 (envelope of the model readings)', dict(rmin=MODEL_RATIO_ENVELOPE[0], rmax=MODEL_RATIO_ENVELOPE[1])),
                ('visibility and angle measured on the plan', dict(plan=True)),
                (f"distance $D \\le {C5_WORKING_M:g}$~m (author's earlier dossier threshold)", dict(dmax=C5_WORKING_M)),
                (f"distance $D \\le {C5_ENVELOPE_M:g}$~m (model-reading envelope)", dict(dmax=C5_ENVELOPE_M))]
    L = ['\\begin{tabular}{lrrl}', '\\toprule', 'Geometric filters & Configurations & Corners & Jamaica $\\times$ Howard NE kept \\\\', '\\midrule']
    sens = {}
    for label, kw in variants:
        s = filters(rows, **kw)[3]; cs = {r['corner'] for r in s}
        keep = 'yes' if win in cs else 'no'
        sens[label] = (len(s), len(cs), keep)
        L.append(f'{label} & {len(s)} & {len(cs)} & {keep} \\\\')
    L += ['\\bottomrule', '\\end{tabular}']
    (TABLES / 'sensitivity.tex').write_text('\n'.join(L) + '\n')
    # Numbers quoted in the text
    nC5 = len(filters(rows, dmax=C5_ENVELOPE_M)[3]); nC5p = len(filters(rows, dmax=C5_WORKING_M)[3])
    model_rows = filters(rows, rmin=MODEL_RATIO[0], rmax=MODEL_RATIO[1])[3]
    no_ratio = filters(rows, rmin=0.0, rmax=math.inf)[3]
    env_rows = filters(rows, rmin=MODEL_RATIO_ENVELOPE[0], rmax=MODEL_RATIO_ENVELOPE[1])[3]
    no_hand = filters(rows, chir=False)[3]
    nModel = len(model_rows)
    physical_corners = {tuple(round(x, 3) for x in c['A']) for c in CORNERS}
    macros = {'nOpenings': len(OPS), 'nCornersOriented': len(CORNERS), 'nPhysicalCorners': len(physical_corners), 'nUniverse': len(rows), 'nCone': len(c1), 'nCtwo': len(c12),
              'nCthree': len(c123), 'nAngle': len(c123a), 'nCorners': len(corners), 'nCfive': nC5, 'nCfiveWorking': nC5p, 'nModelRatio': nModel,
              'SfourD': f"{best['D']:.1f}", 'SfourH': f"{best['D']/ADULT:.0f}", 'Sfourd': f"{best['d']:.1f}", 'SfourAngle': f"{best['ang']:.0f}",
              'SfourOpen': best['open'], 'DminAll': f"{min(r['D'] for r in c123a):.1f}", 'CfiveEnvelope': f'{C5_ENVELOPE_M:g}', 'CfiveWorking': f'{C5_WORKING_M:g}'}
    macros.update({'nNoRatio': len(no_ratio), 'nNoRatioCorners': len({r['corner'] for r in no_ratio}),
                   'nNoHand': len(no_hand), 'nNoHandCorners': len({r['corner'] for r in no_hand}),
                   'nModelCorners': len({r['corner'] for r in model_rows}),
                   'nModelEnvelope': len(env_rows), 'nModelEnvelopeCorners': len({r['corner'] for r in env_rows})})
    ann = min((r for r in c123a if r['corner'] == 'Jamaica x Ann SW'), key=lambda r: r['D'])
    macros.update({'AnnSWD': f"{ann['D']:.1f}", 'AnnSWAngle': f"{ann['ang']:.0f}",
                   'nSfourAdmissible': len([r for r in c123a if r['corner'] == win]),
                   'nBroomielawNW': len([r for r in rows if r['corner'] == 'Jamaica x Broomielaw NW']),
                   'WidthJamaica': f"{WIDTH['Jamaica']:.1f}", 'WidthHoward': f"{WIDTH['Howard']:.1f}",
                   'RatioJH': f"{WIDTH['Jamaica'] / WIDTH['Howard']:.1f}", 'RatioMirror': f"{WIDTH['Howard'] / WIDTH['Jamaica']:.2f}",
                   'DPaisleyA': f"{math.dist(P['PAISLEY'], CORNERS[0]['A']):.0f}"})   # later Paisley's corner (1885) to Jamaica x Howard NE
    plan_rows = filters(rows, plan=True)[3]
    plan_c1 = filters(rows, plan=True)[0]
    ann_plan = next(r for r in plan_rows if r['corner'] == 'Jamaica x Ann SW' and r['open'] == ann['open'])
    ja, jh = FACADES['Jamaica E (north of Howard)'], FACADES['Howard N (west of ACL)']
    ea, eh = unit(ja[0], ja[1]), unit(jh[0], jh[1])
    macros.update({'nPlanCone': len(plan_c1), 'nPlanAngle': len(plan_rows), 'nPlanCorners': len({r['corner'] for r in plan_rows}),
                   'SfourAnglePlan': f"{best['ang_plan']:.0f}", 'AnnSWAnglePlan': f"{ann_plan['ang_plan']:.0f}",
                   'nCfiveWorkingPlan': len(filters(rows, plan=True, dmax=C5_WORKING_M)[3]),
                   'nCfivePlan': len(filters(rows, plan=True, dmax=C5_ENVELOPE_M)[3]),
                   'DminPlan': f"{min(r['D'] for r in plan_rows):.1f}",
                   'CornerAngleJH': f"{math.degrees(math.acos(ea[0]*eh[0] + ea[1]*eh[1])):.0f}",
                   'nRivals': len(corners) - 1})
    (TABLES / 'numbers.tex').write_text(''.join(f'\\newcommand{{\\{k}}}{{{v}}}\n' for k, v in macros.items()))
    return corners, win, best, sens

if __name__ == '__main__':
    rows = run()
    with open(DATA / 'configurations_phase1.csv', 'w', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=';', lineterminator='\n'); wr.writeheader(); wr.writerows(rows)
    c1, c12, c123, c123a = filters(rows)
    corners, win, best, sens = write_tables(rows, c1, c12, c123, c123a)
    print(f'universe {len(rows)}  C1 {len(c1)}  C1+C2 {len(c12)}  +C3 {len(c123)}  +angle {len(c123a)}  on {len(corners)} corners')
    print(f"documentary step: {win}; nearest admissible opening {best['open']} D={best['D']:.1f} m = {best['D']/ADULT:.1f} adult heights, angle {best['ang']:.0f} deg")
    for k, v in sens.items(): print(f'  {k:60s} {v[0]:3d} configs {v[1]:2d} corners  {v[2]}')
