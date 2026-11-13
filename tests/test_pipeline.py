"""One runnable check: the census reproduces the counts used in the paper. Run: make test"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import census

rows = census.run()
c1, c12, c123, c123a = census.filters(rows)
assert (len(rows), len(c1), len(c12), len(c123), len(c123a)) == (187, 45, 23, 20, 17), (len(rows), len(c1), len(c12), len(c123), len(c123a))
corners, winners = census.select(c123a, census.load_trades())
assert len(corners) == 5 and winners == ['Jamaica x Howard NE'], (corners, winners)
s4 = min((r for r in c123a if r['corner'] == 'Jamaica x Howard NE'), key=lambda r: r['D'])
assert s4['open'] == 'JW6' and abs(s4['D'] - 27.8) < 0.15 and abs(s4['ang'] - 37) < 1, s4
# Sensitivity to the readings and conventions that the paper does not control.
assert len(census.filters(rows, dmax=census.C5_ENVELOPE_M)[3]) == 0
assert len(census.filters(rows, dmax=census.C5_WORKING_M)[3]) == 1
model_ratio = census.filters(rows, rmin=0.4, rmax=1.6)[3]
assert (len(model_ratio), len({r['corner'] for r in model_ratio})) == (2, 1)
assert 'Jamaica x Howard NE' not in {r['corner'] for r in model_ratio}
envelope = census.filters(rows, rmin=census.MODEL_RATIO_ENVELOPE[0], rmax=census.MODEL_RATIO_ENVELOPE[1])[3]
assert (len(envelope), len({r['corner'] for r in envelope})) == (20, 7) and 'Jamaica x Howard NE' in {r['corner'] for r in envelope}
no_ratio = census.filters(rows, rmin=0.0, rmax=float('inf'))[3]
assert (len(no_ratio), len({r['corner'] for r in no_ratio})) == (20, 7)
assert {'Howard x Dixon SE (Y = Howard)', "Howard x St Enoch's Sq. NW"} <= {r['corner'] for r in no_ratio}
no_hand = census.filters(rows, chir=False)[3]
assert (len(no_hand), len({r['corner'] for r in no_hand})) == (34, 9)
# JW7 is on the wrong side of X for the opposite-handed Jamaica/Howard orientation.
mirror_jw7 = next(r for r in rows if r['corner'] == 'Jamaica x Howard SE' and r['open'] == 'JW7')
assert not mirror_jw7['chir'] and mirror_jw7['d'] < 0
assert mirror_jw7 not in census.filters(rows, chir=False)[0]
# Plan-angle sensitivity: visibility and angle against the recorded face X (the model treats the streets as perpendicular).
plan = census.filters(rows, plan=True)[3]
assert (len(plan), len({r['corner'] for r in plan})) == (18, 5), len(plan)
assert {r['corner'] for r in plan} == {r['corner'] for r in c123a}
jw6 = next(r for r in plan if r['corner'] == 'Jamaica x Howard NE' and r['open'] == 'JW6')
assert abs(jw6['ang_plan'] - 46) < 1 and jw6['d_plan'] > 0, jw6
assert len(census.filters(rows, plan=True, dmax=census.C5_WORKING_M)[3]) == 2
assert len(census.filters(rows, plan=True, dmax=census.C5_ENVELOPE_M)[3]) == 0
# Claims of the paper that the counts above do not cover.
mirror = [r for r in rows if r['corner'] == 'Jamaica x Howard NE (Y = Howard)']
assert len(mirror) == 4 and all(r['d'] < 0 and not r['chir'] for r in mirror)          # reversed orientation: no opening sees both faces
paisley = [r for r in rows if r['corner'] == 'Jamaica x Broomielaw NW']
assert len(paisley) == 9 and all(r['d'] < 0 for r in paisley)                         # the later Paisley's corner fails the first relation
assert len([r for r in c123a if r['corner'] == 'Jamaica x Howard NE']) == 4
assert abs(min(r['D'] for r in c123a) - 20.0) < 0.05
assert abs(census.math.dist(census.P['PAISLEY'], census.CORNERS[0]['A']) - 83) < 0.5
for t in census.load_trades().values():
    assert t['corner_clothier'] in {'yes', 'no', 'partial', 'unknown'}
    assert t['facing_licensed'] in {'yes', 'no', 'partial', 'unknown'}
nums = (ROOT / 'paper' / 'tables' / 'numbers.tex').read_text()
assert '\\SfourD}{27.8}' in nums and '\\nOpenings}{62}' in nums and '\\nAngle}{17}' in nums and '\\nCfive}{0}' in nums
assert '\\nCone}{45}' in nums and '\\nNoHand}{34}' in nums and '\\nNoRatio}{20}' in nums and '\\nModelCorners}{1}' in nums
assert '\\nCornersOriented}{32}' in nums and '\\nPhysicalCorners}{24}' in nums
print('ok: census 187 -> 45 -> 23 -> 20 -> 17 on 5 corners -> 1 complete documentary match; sensitivities and numbers.tex match')
