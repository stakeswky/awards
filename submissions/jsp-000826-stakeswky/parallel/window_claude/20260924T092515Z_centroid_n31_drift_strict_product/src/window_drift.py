"""Adversarial evidence for the window drift condition: maximise
   wd(T) = max_{r in [ceil(n/4), ceil((2a-1)/3)-2]} (m_{r+1} - m_r),  m_r = (r+1) p_{r+1}/p_r,
over structured families and by random local search. M1 on the window needs wd <= 1. Exact
coefficients; the reported maxima are floats of exact rationals."""
import random, sys, json, time
from fractions import Fraction as Fr
from ip import indep_poly
from families import hubs, core_tree
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
BUDGET = float(sys.argv[2]) if len(sys.argv) > 2 else 300
def wd(par):
    p = indep_poly(par); n = len(par); a = len(p) - 1
    q, top = (n + 3) // 4, (2 * a + 1) // 3
    best = None
    for r in range(q, top - 1):
        if r + 2 > a: break
        d = Fr((r + 2) * p[r + 2], p[r + 1]) - Fr((r + 1) * p[r + 1], p[r])
        if best is None or d > best[0]: best = (d, r)
    return best, a
def spider(legs):
    par = [-1]
    for L in legs:
        prev = 0
        for _ in range(L): par.append(prev); prev = len(par) - 1
    return par
def R(s, m):
    par = [-1]
    for _ in range(s):
        c = len(par); par.append(0); par.append(c); par.append(c)
    for _ in range(m): par.append(0)
    return par
def kary(b, depth):
    par = [-1]; frontier = [0]
    for _ in range(depth):
        nf = []
        for u in frontier:
            for _ in range(b): par.append(u); nf.append(len(par) - 1)
        frontier = nf
    return par
def caterpillar(spine, legs):
    par = [-1]
    for i in range(1, spine): par.append(i - 1)
    for i in range(spine):
        for _ in range(legs[i % len(legs)]): par.append(i)
    return par
fam = []
for t in range(2, 25):
    for l in range(1, 12):
        if 1 + t * (l + 1) <= 220: fam.append((f'hubs({t},{l})', hubs(t, l)))
for s in range(2, 40):
    for L in (2, 3, 4, 5):
        if 1 + s * L <= 220: fam.append((f'spider({L}^{s})', spider([L] * s)))
for s in range(2, 60):
    for m in (0, 1, 2):
        if 1 + 3 * s + m <= 220: fam.append((f'R({s},{m})', R(s, m)))
for b, dmax in ((2, 7), (3, 4), (4, 3), (5, 3), (6, 2)):
    for d in range(2, dmax + 1): fam.append((f'kary({b},{d})', kary(b, d)))
for sp in range(3, 60):
    for legs in ((1,), (2,), (3,), (1, 2), (0, 3), (1, 0), (2, 0, 0), (4, 0)):
        if sp + sp * sum(legs) / len(legs) <= 220: fam.append((f'cat({sp},{legs})', caterpillar(sp, list(legs))))
for s in range(3, 13):
    for k in range(3, 12):
        if 1 + k * (2 * s + 1) <= 220: fam.append((f'core(({s},)*{k})', core_tree((s,) * k)))
res = []
for name, par in fam:
    b, a = wd(par)
    if b: res.append((float(b[0]), name, len(par), a, b[1]))
res.sort(reverse=True)
print('families:', len(res), 'top 8:')
for r in res[:8]: print('  ', r)
# random local search: mutate by moving a leaf / subtree reattachment
def rand_tree(n):
    return [-1] + [random.randrange(v) for v in range(1, n)]
def relabel(par):
    n = len(par); ch = [[] for _ in range(n)]
    for v in range(1, n): ch[par[v]].append(v)
    order = []; st = [0]
    while st:
        u = st.pop(); order.append(u); st.extend(reversed(ch[u]))
    pos = {u: i for i, u in enumerate(order)}
    return [-1] + [pos[par[u]] for u in order[1:]]
def mutate(par):
    par = list(par); n = len(par)
    v = random.randrange(1, n)
    # descendants of v
    ch = [[] for _ in range(n)]
    for u in range(1, n): ch[par[u]].append(u)
    sub = set(); st = [v]
    while st:
        u = st.pop(); sub.add(u); st.extend(ch[u])
    cand = [u for u in range(n) if u not in sub]
    par[v] = random.choice(cand)
    return relabel(par)
t0 = time.time(); best_overall = (-9, None)
while time.time() - t0 < BUDGET:
    n = random.randint(30, 90)
    cur = relabel(rand_tree(n)); cb = wd(cur)[0][0]
    for it in range(150):
        nxt = mutate(cur); nb = wd(nxt)[0]
        if nb and nb[0] >= cb: cur, cb = nxt, nb[0]
    if cb > best_overall[0]: best_overall = (cb, cur); print('climb', round(float(cb), 4), 'n', len(cur), flush=True)
print('local search best window drift', float(best_overall[0]), 'parents', best_overall[1])
json.dump(dict(families_top=res[:40], local_search_best=float(best_overall[0]), local_search_parents=best_overall[1]),
          open(f'window_drift_seed{sys.argv[1] if len(sys.argv) > 1 else 1}.json', 'w'), indent=1)
