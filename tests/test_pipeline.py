"""One runnable check: the census and the chance analysis reproduce the numbers used in the paper, and every generated
table and data file on disk is byte-identical to what the code writes now. Run: make test (does not regenerate them first)."""
import pathlib, re, shutil, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import census, chance

rows = census.run()
trades = census.load_trades()
phys = lambda names: {census.physical(n) for n in names}

# Inputs.
# One row per orientation of every corner of the window, tested (census.CORNERS) or not (census.UNTESTED).
assert len(trades) == 60 and set(trades) == {c['name'] for c in census.CORNERS} | set(census.UNTESTED)
for t in trades.values():
    assert t['corner_clothier'] in {'yes', 'no', 'partial', 'unknown'} and t['facing_licensed'] in {'yes', 'no', 'partial', 'unknown'}
    assert t['facing_quay'] in {'yes', 'no'} and t['checked'] in {'image', 'ocr'} and t['in_v14'] in {'yes', 'no'}
    assert t['clothier_on_x'] in {'yes', 'no', 'unknown', 'n/a'} and (t['clothier_on_x'] == 'n/a') == (t['corner_clothier'] == 'no'), t['corner']
    if t['facing_quay'] == 'yes': assert t['facing_licensed'] == 'no', t['corner']          # codebook: a quay is never licensed
assert len(phys(trades)) == 30 and len(census.CORNERS) == 46 and len(census.UNTESTED) == 14

# The version 1.4 census (recorded 1857 openings only) is unchanged up to the projection: 187 -> 45 -> 23 -> 20 on 7 corners.
o1, o12, o123, o123a = census.filters(rows, points='openings', lanes=True)
assert (len([r for r in rows if r['kind'] == 'opening']), len(o1), len(o12), len(o123a)) == (187, 45, 23, 20)
assert len(phys(r['corner'] for r in o123a)) == 7
jw6 = min((r for r in o123a if r['corner'] == census.CAND), key=lambda r: r['D'])
assert jw6['open'] == 'JW6' and abs(jw6['D'] - 27.9) < 0.15 and abs(jw6['ang'] - 37) < 1, jw6

# Principal census: every frontage point may be the watching point, H4-H5 in full (no lane, clothier with an address
# on X); both handedness settings are reported.
hand = census.filters(rows)[3]; nohand = census.filters(rows, chir=False)[3]
_, win_hand = census.select(hand, trades); _, win_nohand = census.select(nohand, trades)
assert len(phys(r['corner'] for r in hand)) == 8 and len(phys(r['corner'] for r in nohand)) == 14
assert phys(win_hand) == {census.CAND} and phys(win_nohand) == {census.CAND, 'Jamaica x Argyle SW'}
assert phys(r['corner'] for r in hand) <= phys(r['corner'] for r in nohand)
assert not [r for r in hand + nohand if 'ACL' in (r['Y'], r['X'])]
# First coding of version 1.5 (lanes kept, clothier anywhere at the corner): the corner on Adam's Court Lane also matches.
hand1 = census.filters(rows, lanes=True)[3]; nohand1 = census.filters(rows, chir=False, lanes=True)[3]
_, w1 = census.select(hand1, trades, front=False); _, w1n = census.select(nohand1, trades, front=False)
assert len(phys(r['corner'] for r in hand1)) == 10 and len(phys(r['corner'] for r in nohand1)) == 17
assert phys(w1) == {census.CAND, "Argyle x Adam's Court Lane SE"} and phys(w1n) == phys(w1) | {'Jamaica x Argyle SW'}
assert trades["Argyle x Adam's Court Lane SE"]['clothier_on_x'] == 'no' and trades[census.CAND]['clothier_on_x'] == 'yes'
# The later Paisley's corner watched across Jamaica St fails the first relation (no point of the frontage sees both faces);
# watched across the Broomielaw, the watchers would stand on the quay (no frontage, untested), yet the corner carries the pair.
assert not [r for r in rows if r['corner'] == 'Jamaica x Broomielaw NW' and r['d'] > 0]
assert chance.matches(trades['Jamaica x Broomielaw NW (Y = Broomielaw)'], 'strict') and 'Jamaica x Broomielaw NW (Y = Broomielaw)' in census.UNTESTED
# Reversed orientation at the candidate: no point of the south frontage of Howard St sees both faces.
assert all(r['d'] < 0 for r in rows if r['corner'] == 'Jamaica x Howard NE (Y = Howard)')

# Chance analysis (Section 5): version 1.4 figures are reproduced, then the principal ones and the first coding.
v14 = chance.analyse(rows, trades, pop='v1.4', drawn=False)
assert (v14['N'], v14['n'], v14['K'], v14['k']) == (24, 7, 3, 1) and abs(v14['p'] - 0.664) < 0.001
a = chance.analyse(rows, trades)
assert (a['N'], a['n'], a['K'], a['k']) == (30, 8, 3, 1) and abs(a['p'] - 0.621) < 0.001 and a['unique']
assert abs(min(a['lr'].values()) - 1.245) < 0.01 and abs(max(a['lr'].values()) - 1.5) < 0.01 and abs(a['post'][0.8] - 0.86) < 0.01
b = chance.analyse(rows, trades, hand=False)
assert (b['n'], b['K'], b['k']) == (14, 3, 2) and abs(b['p'] - 0.862) < 0.001 and not b['unique']
f = chance.analyse(rows, trades, drawn=False)
assert (f['N'], f['n'], f['K'], f['k']) == (30, 10, 4, 2) and abs(f['p'] - 0.823) < 0.001 and abs(f['post'][0.8] - 0.44) < 0.01
j = chance.analyse(rows, trades, pop='Jamaica St')
assert (j['N'], j['n'], j['K'], j['k']) == (8, 3, 3, 1) and abs(j['p'] - 0.821) < 0.001
# Every corner has an orientation with premises across X, so the population is the whole window.
assert chance.population(trades, 'no quay') == phys(trades)

# The generated files on disk are byte-identical to what the code writes now (run `make tables` after changing code or data).
tmp = pathlib.Path(tempfile.mkdtemp())
census.TABLES = census.DATA = tmp
shutil.copy(ROOT / 'data' / 'trades_1877.csv', tmp)   # write_tables reads it from census.DATA
census.write_configurations(rows); census.write_tables(rows); chance.write(rows, trades)
for f in ['numbers.tex', 'corners.tex', 'sensitivity.tex', 'chance.tex', 'chance_numbers.tex']:
    assert (tmp / f).read_bytes() == (ROOT / 'paper' / 'tables' / f).read_bytes(), f'paper/tables/{f} is stale'
for f in ['configurations_phase1.csv', 'chance_multiverse.csv']:
    assert (tmp / f).read_bytes() == (ROOT / 'data' / f).read_bytes(), f'data/{f} is stale'
def macros(name): return dict(re.findall(r'\\newcommand\{\\(\w+)\}\{([^}]*)\}', (ROOT / 'paper' / 'tables' / name).read_text()))
nums, ch = macros('numbers.tex'), macros('chance_numbers.tex')
assert (nums['nUniverse'], nums['nAngle'], nums['nCorners'], nums['nSurv'], nums['nSurvNoHand'], nums['nWin'], nums['nWinNoHand']) == ('187', '20', '7', '8', '14', '1', '2'), nums
assert (nums['nSurvFirst'], nums['nSurvNoHandFirst'], nums['nWinFirst'], nums['nWinNoHandFirst']) == ('10', '17', '2', '3'), nums
assert (nums['SfourOpen'], nums['SfourD'], nums['nPhysicalWindow'], nums['nOrient']) == ('JW6', '27.9', '30', '46')
assert (ch['ChanceHandStrict'], ch['MatchSurvHandStrict'], ch['PostHandStrict'], ch['nPop'], ch['ChanceFirstHandStrict'], ch['ChanceVfourStrict']) == ('62', '1', '0.86', '30', '82', '66'), ch
assert (nums['nUntested'], nums['nCornersRatio']) == ('14', '5'), nums
print('ok: v1.4 census reproduced; H4-H5 in full: 8 corners (14 without handedness), 1 (2) with both trades, chance 62% of 30 corners; '
      'first coding 10 (17), 2 (3), 82%; generated files up to date')
