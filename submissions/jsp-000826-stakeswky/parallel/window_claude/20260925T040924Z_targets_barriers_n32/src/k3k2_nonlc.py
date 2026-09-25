"""|kappa3|/kappa2 on the 308 non-LC trees (n = 26..31) and on large hub/core families, lambda in [e^-4, e^8]."""
import math, re, glob, json
from modelib import indep_poly_del
from families import hubs, core_tree
from k3k2 import cumulants
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '20260924T092515Z_centroid_n31_drift_strict_product', 'results', 'reverified_examples.json')
seqs = [(e['n'], e['p']) for e in json.load(open(R))]
fam = []
for t, l in ((2, 20), (5, 10), (10, 10), (20, 5), (40, 3), (3, 30)): fam.append((f'hubs({t},{l})', indep_poly_del(hubs(t, l))))
for arms in ((3, 4, 4), (5,) * 8, (8,) * 17, (10,) * 10, (6,) * 12): fam.append((f'core{arms[:1]}x{len(arms)}', indep_poly_del(core_tree(arms))))
grid = [math.exp(t / 20) for t in range(-80, 161)]
def scan(p):
    best = (0, None); first = None
    for lam in grid:
        m1, c2, c3 = cumulants(p, lam); r = abs(c3) / c2
        if r > best[0]: best = (r, round(lam, 3), round(m1, 2))
        if r > 1 and first is None: first = (round(lam, 3), round(r, 3), round(m1, 2))
    return best, first
worst = (0, None); nviol = 0; firsts = []
for n, p in seqs:
    b, f = scan(p)
    if b[0] > worst[0]: worst = (b[0], n, b)
    if f: nviol += 1; firsts.append((n, len(p) - 1, f))
print('non-LC trees:', len(seqs), 'max |k3|/k2 =', worst, 'trees with |k3|>k2 somewhere:', nviol)
firsts.sort(key=lambda x: x[2][0])
for x in firsts[:6]: print('   first violation (n, alpha, (lambda, ratio, mean)):', x)
for name, p in fam:
    b, f = scan(p); print(f'{name}: n-ish alpha={len(p)-1} max |k3|/k2 = {b[0]:.3f} at lambda={b[1]} mean={b[2]}; first |r|>1: {f}')
