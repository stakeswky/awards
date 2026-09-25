"""(DT) on forests = products of tree sequences, exact rationals, window [ceil(n/4), ceil((2a-1)/3)]:
   s+ = E_{lambda~}|I| - k at lambda~ = p_k/p_{k+1},  s- = k - E_{lambda^}|I| at lambda^ = p_{k-1}/p_k.
Families: (i) all forests with >= 2 components of order <= NMAX; (ii) products of two or three of the
308 non-LC trees (n = 26..31), with and without small trees; (iii) (non-LC tree) x K1^m, x K2^m."""
import sys, json, random, itertools
from fractions import Fraction as Fr
from modelib import parents_from_levels, indep_poly_del
from ma_forests import free_trees
from ip import mul
random.seed(3)
def tmean(p, lam):
    num = 0; den = 0; pw = Fr(1)
    for j, c in enumerate(p): num += j * c * pw; den += c * pw; pw *= lam
    return num / den
def dt(p, n):
    a = len(p) - 1; q, top = (n + 3) // 4, (2 * a + 1) // 3; best = Fr(99)
    for k in range(max(q, 1), min(top, a - 1) + 1):
        best = min(best, tmean(p, Fr(p[k], p[k + 1])) - k, k - tmean(p, Fr(p[k - 1], p[k])))
    return best
NMAX = int(sys.argv[1])
trees = {m: [indep_poly_del(parents_from_levels(lv)) for lv in free_trees(m)] for m in range(1, NMAX)}
def forests(n):
    def rec(rem, maxm, cur):
        if rem == 0: yield cur; return
        for m in range(min(rem, maxm), 0, -1):
            for tp in trees[m]: yield from rec(rem - m, m, mul(cur, tp))
    yield from rec(n, n - 1, [1])
worst = Fr(99); cnt = 0
for n in range(4, NMAX + 1):
    wn = Fr(99)
    for p in forests(n):
        cnt += 1; s = dt(p, n); wn = min(wn, s)
    worst = min(worst, wn); print(f'forests n={n}: min DT slack {float(wn):.4f}', flush=True)
print('all forests (>=2 components) n<=%d: %d, min slack %.4f' % (NMAX, cnt, float(worst)))
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '20260924T092515Z_centroid_n31_drift_strict_product', 'results', 'reverified_examples.json')
nl = [(e['n'], e['p']) for e in json.load(open(R))]
w2 = Fr(99); c2 = 0
for _ in range(120):
    (n1, p1), (n2, p2) = random.choice(nl), random.choice(nl)
    p = mul(p1, p2); c2 += 1; w2 = min(w2, dt(p, n1 + n2))
for _ in range(30):
    (n1, p1), (n2, p2), (n3, p3) = random.choice(nl), random.choice(nl), random.choice(nl)
    p = mul(mul(p1, p2), p3); c2 += 1; w2 = min(w2, dt(p, n1 + n2 + n3))
print(f'products of 2-3 non-LC trees: {c2}, min DT slack {float(w2):.4f}')
w3 = Fr(99); c3 = 0
for n1, p1 in nl[::10]:
    for m in (1, 3, 10, 30):
        for base, sz in (([1, 1], 1), ([1, 2], 2)):
            p = p1
            for _ in range(m): p = mul(p, base)
            c3 += 1; w3 = min(w3, dt(p, n1 + m * sz))
print(f'non-LC tree x K1^m / K2^m: {c3}, min DT slack {float(w3):.4f}')
