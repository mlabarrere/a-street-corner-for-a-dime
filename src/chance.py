"""How often would the documentary match turn up by chance? (paper, Section 5)

Reads  data/trades_1877.csv (every orientation of every corner in the declared window) and the census survivors.
Writes paper/tables/chance.tex, paper/tables/chance_numbers.tex and data/chance_multiverse.csv (generated).

Unit: the physical corner. A corner matches when one of its orientations has a clothier at the corner and licensed
premises facing the stand ('strict': both 'yes'; 'inclusive': licensed may be 'partial'; 'upper': every cell not
coded 'no' is counted as a match). With the relations of H4-H5 in full (drawn=True, principal) the clothier must also
have an address on X and no orientation on a lane survives; drawn=False gives the first coding of version 1.5.
Among the survivors, a match counts only on an orientation that survives.
Population: every corner of the window except those that face a river quay across X in every orientation, which could
never carry the pair ('no quay', principal; with a row for every orientation in data/trades_1877.csv, no corner of the
window is in that case, so it holds all of them); the corners on Jamaica Street only ('Jamaica St', after H2's plate);
or the corners and recorded openings of version 1.4.
"""
import csv, itertools, math, pathlib, sys
from scipy.special import betaln
from scipy.stats import hypergeom
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import census

Q_GRID = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)   # chance that the corner Rosa drew carries both trades in the directory
PRIORS = {'Jeffreys': (0.5, 0.5), 'uniform': (1.0, 1.0)}   # Beta prior for the chance rate r of the pair
CAND = census.CAND
POPS = ('no quay', 'Jamaica St', 'v1.4')
CODINGS = ('strict', 'inclusive', 'upper')

def matches(t, coding, front=True):
    c, l, x = t['corner_clothier'], t['facing_licensed'], t['clothier_on_x']
    if coding == 'upper': return c != 'no' and l != 'no' and (not front or x != 'no')
    return c == 'yes' and l in (('yes',) if coding == 'strict' else ('yes', 'partial')) and (not front or x == 'yes')

def population(trades, pop):
    phys = {}
    for name, t in trades.items(): phys.setdefault(census.physical(name), []).append(t)
    if pop == 'v1.4': return {p for p, ts in phys.items() if any(t['in_v14'] == 'yes' for t in ts)}
    able = {p for p, ts in phys.items() if not all(t['facing_quay'] == 'yes' for t in ts)}
    return {p for p in able if 'Jamaica' in p} if pop == 'Jamaica St' else able

def analyse(rows, trades, hand=True, pop='no quay', coding='strict', prior='Jeffreys', drawn=True, **geo):
    points = 'openings' if pop == 'v1.4' else 'frontage'
    surv = {r['corner'] for r in census.filters(rows, chir=hand, points=points, lanes=not drawn, **geo)[3]}
    U = population(trades, pop)
    S = {census.physical(n) for n in surv} & U
    M = {census.physical(n) for n, t in trades.items() if matches(t, coding, drawn)} & U
    MS = {census.physical(n) for n in surv if matches(trades[n], coding, drawn)} & S
    N, n, K, k = len(U), len(S), len(M), len(MS)
    k_out, N_out = len(M - S), N - n
    a, b = PRIORS[prior][0] + k_out, PRIORS[prior][1] + N_out - k_out     # Beta posterior for r from the non-survivors
    E = lambda i, j: math.exp(betaln(a + i, b + j) - betaln(a, b))          # E[r^i (1-r)^j]
    h0 = E(k, n - k)                                                        # P(D | no real corner in the window)
    lr, post, power = {}, {}, {}
    for q in Q_GRID:
        hit = q * E(k - 1, n - k) if k else 0.0          # P(D | the real corner is a given matching survivor)
        miss = (1 - q) * E(k, n - k - 1) if n > k else 0.0   # P(D | the real corner is a given non-matching survivor)
        h1 = (k * hit + (n - k) * miss) / n
        lr[q] = h1 / h0
        post[q] = (hit if CAND in MS else miss) / (k * hit + (n - k) * miss)
        power[q] = q * E(0, n - 1)                        # P(a real, faithfully drawn survivor is the single match)
    return dict(N=N, n=n, K=K, k=k, survivors=sorted(S), matching=sorted(MS), p=hypergeom.sf(0, N, K, n),
                lr=lr, post=post, power=power, unique=(MS == {CAND}))

def multiverse(rows, trades):
    out = []
    for drawn, hand, pop, coding in itertools.product((True, False), (True, False), POPS, CODINGS):
        a = analyse(rows, trades, hand, pop, coding, drawn=drawn)
        u = analyse(rows, trades, hand, pop, coding, prior='uniform', drawn=drawn)
        out.append(dict(relations='H4-H5 in full' if drawn else 'first coding', handedness='kept' if hand else 'dropped', population=pop, coding=coding, N=a['N'], survivors=a['n'],
                        matching_corners=a['K'], matching_survivors=a['k'], names='; '.join(a['matching']),
                        chance=round(a['p'], 3), bayes_factor_q08_jeffreys=round(a['lr'][0.8], 2), bayes_factor_q08_uniform=round(u['lr'][0.8], 2),
                        bayes_factor_min=round(min(a['lr'].values()), 2), bayes_factor_max=round(max(a['lr'].values()), 2),
                        p_candidate_q08=round(a['post'][0.8], 2), candidate_unique=a['unique']))
    return out

def pct(x): return f'{100 * x:.0f}'

def write(rows, trades):
    L = ['\\begin{tabular}{llrrrrrr}', '\\toprule',
         'Handedness & Coding & Survivors & Matching survivors & Matching corners & Chance & Bayes factor & P(candidate) \\\\']
    m = {}
    for drawn in (True, False):
        L += ['\\midrule', '\\multicolumn{8}{l}{\\emph{' + ('Relations of H4--H5 in full (principal)' if drawn else
              'First coding: lanes kept, clothier anywhere at the corner') + '}} \\\\', '\\midrule']
        for hand, coding in itertools.product((True, False), CODINGS):
            a = analyse(rows, trades, hand, 'no quay', coding, drawn=drawn)
            L.append(f"{'kept' if hand else 'dropped'} & {coding} & {a['n']} & {a['k']} & {a['K']} of {a['N']} & {pct(a['p'])}\\% & "
                     f"{min(a['lr'].values()):.1f}--{max(a['lr'].values()):.1f} & {a['post'][0.8]:.2f} \\\\")
            tag = ('' if drawn else 'First') + ('Hand' if hand else 'NoHand') + coding.capitalize()
            m.update({f'Chance{tag}': pct(a['p']), f'Match{tag}': a['K'], f'MatchSurv{tag}': a['k'], f'Surv{tag}': a['n'],
                      f'BF{tag}': f"{a['lr'][0.8]:.1f}", f'BFlo{tag}': f"{min(a['lr'].values()):.1f}", f'BFhi{tag}': f"{max(a['lr'].values()):.1f}",
                      f'Post{tag}': f"{a['post'][0.8]:.2f}", f'Power{tag}': pct(a['power'][0.8])})
    L += ['\\bottomrule', '\\end{tabular}']
    (census.TABLES / 'chance.tex').write_text('\n'.join(L) + '\n')
    mv = multiverse(rows, trades)
    with open(census.DATA / 'chance_multiverse.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(mv[0].keys()), delimiter=';', lineterminator='\n'); w.writeheader(); w.writerows(mv)
    p = analyse(rows, trades)
    jam = analyse(rows, trades, pop='Jamaica St')
    v4r = analyse(rows, trades, pop='v1.4', drawn=False, rmin=census.AUTHOR_RATIO[0], rmax=census.AUTHOR_RATIO[1])
    m.update({'nPop': p['N'], 'nPopJam': jam['N'], 'ChanceJam': pct(jam['p']),
              'BFloJam': f"{min(jam['lr'].values()):.1f}", 'BFhiJam': f"{max(jam['lr'].values()):.1f}",
              'ChanceMin': pct(min(r['chance'] for r in mv)), 'ChanceMax': pct(max(r['chance'] for r in mv)),
              'BFminAll': f"{min(r['bayes_factor_min'] for r in mv):.1f}", 'BFmaxAll': f"{max(r['bayes_factor_max'] for r in mv):.1f}",
              'nMultiverse': len(mv), 'nUniqueCells': sum(r['candidate_unique'] for r in mv),
              'ChanceVfourStrict': pct(analyse(rows, trades, pop='v1.4', drawn=False)['p']),
              'ChanceVfourRatio': pct(v4r['p']), 'BFloVfourRatio': f"{min(v4r['lr'].values()):.1f}", 'BFhiVfourRatio': f"{max(v4r['lr'].values()):.1f}",
              'BFUniform': f"{analyse(rows, trades, prior='uniform')['lr'][0.8]:.1f}"})
    (census.TABLES / 'chance_numbers.tex').write_text(''.join(f'\\newcommand{{\\{k}}}{{{v}}}\n' for k, v in m.items()))
    return mv

if __name__ == '__main__':
    rows = census.run()
    mv = write(rows, census.load_trades())
    for r in mv:
        print(f"{r['relations'][:5]:5s} {r['handedness']:7s} {r['population']:9s} {r['coding']:9s} N={r['N']:2d} n={r['survivors']:2d} K={r['matching_corners']:2d} "
              f"k={r['matching_survivors']} chance={r['chance']:.2f} BF={r['bayes_factor_q08_jeffreys']:.2f}/{r['bayes_factor_q08_uniform']:.2f} "
              f"P(cand)={r['p_candidate_q08']:.2f} unique={r['candidate_unique']}  [{r['names']}]")
