"""Window drift for forests built from extremal / non-LC trees (products of sequences); exact."""
import json, glob, re, random, itertools
from fractions import Fraction as Fr
from ip import indep_poly, mul
from families import hubs, core_tree
random.seed(7)
def wdrift(p, n):
    a = len(p) - 1; q, top = (n + 3) // 4, (2 * a + 1) // 3
    best = None
    for r in range(q, top - 1):
        d = Fr((r + 2) * p[r + 2], p[r + 1]) - Fr((r + 1) * p[r + 1], p[r])
        if best is None or d > best: best = d
    return best
base = {}
for t, l in [(2, 3), (3, 3), (2, 2), (4, 3), (2, 4), (1, 3), (1, 1), (5, 3), (2, 1)]:
    par = hubs(t, l); base[f'hubs({t},{l})'] = (indep_poly(par), len(par))
base['K1'] = ([1, 1], 1); base['K2'] = ([1, 2], 2); base['P3'] = ([1, 3, 1], 3); base['K13'] = ([1, 4, 3, 1], 4)
import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
nl = []
for f in glob.glob(D + '20260923T153415Z_window_lc_reduction_exhaustive_n29/results/wlc_strict_n2[6-9].json'):
    d = json.load(open(f)); n = d['summary']['n']
    for ex in d['examples']: nl.append(([int(x) for x in re.search(r'p=(\S+)', ex).group(1).split(',')], n))
names = list(base)
best = (-9, None); cnt = 0; fails = 0
for k in (2, 3, 4):
    for combo in itertools.combinations_with_replacement(names, k):
        p, n = [1], 0
        for c in combo: p = mul(p, base[c][0]); n += base[c][1]
        w = wdrift(p, n)
        if w is None: continue
        cnt += 1; fails += w > 1
        if w > best[0]: best = (w, combo)
for i in range(300):
    (p1, n1), (p2, n2) = random.choice(nl), random.choice(nl)
    extra = random.choice(names)
    p = mul(mul(p1, p2), base[extra][0]); n = n1 + n2 + base[extra][1]
    w = wdrift(p, n); cnt += 1; fails += w > 1
    if w > best[0]: best = (w, ('nonLC', n1, 'nonLC', n2, extra))
print('forests tested', cnt, 'window-drift > 1:', fails, 'max window drift', float(best[0]), best[1])
