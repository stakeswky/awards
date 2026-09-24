"""(MA) and single-deletion mode shifts on larger trees: random (Pruefer, recursive), structured
(hubs, core, spiders, caterpillars, k-ary), n up to ~150. Exact arithmetic."""
import random, sys, time
from modelib import *
from families import hubs, core_tree, hub_tree
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
def relabel(par):
    n = len(par); ch = [[] for _ in range(n)]
    for v in range(1, n): ch[par[v]].append(v)
    order = []; st = [0]
    while st:
        u = st.pop(); order.append(u); st.extend(reversed(ch[u]))
    pos = {u: i for i, u in enumerate(order)}
    return [-1] + [pos[par[u]] for u in order[1:]]
def pruefer(n):
    import heapq
    code = [random.randrange(n) for _ in range(n - 2)]
    deg = [1] * n
    for x in code: deg[x] += 1
    leaves = [v for v in range(n) if deg[v] == 1]; heapq.heapify(leaves)
    adj = [[] for _ in range(n)]
    for x in code:
        l = heapq.heappop(leaves); adj[l].append(x); adj[x].append(l); deg[x] -= 1
        if deg[x] == 1: heapq.heappush(leaves, x)
    u, v = heapq.heappop(leaves), heapq.heappop(leaves); adj[u].append(v); adj[v].append(u)
    par = [-2] * n; par[0] = -1; st = [0]
    while st:
        u = st.pop()
        for w in adj[u]:
            if par[w] == -2: par[w] = u; st.append(w)
    return relabel(par)
def spider(legs):
    par = [-1]
    for L in legs:
        prev = 0
        for _ in range(L): par.append(prev); prev = len(par) - 1
    return par
def kary(b, depth):
    par = [-1]; fr = [0]
    for _ in range(depth):
        nf = []
        for u in fr:
            for _ in range(b): par.append(u); nf.append(len(par) - 1)
        fr = nf
    return par
def caterpillar(spine, legs):
    par = [-1]
    for i in range(1, spine): par.append(i - 1)
    for i in range(spine):
        for _ in range(legs[i % len(legs)]): par.append(i)
    return par
def analyse(name, par):
    n = len(par); nb = neighbours(par)
    p = indep_poly_del(par); m1, m2, uni = mode_set(p)
    best = 99; bestv = None; shifts = set(); leaf_best = 99
    for v in range(n):
        d, MA, MC = split_alignment(par, v, nb)
        if d < best: best, bestv = d, (v, len(nb[v]))
        if len(nb[v]) == 1 and d < leaf_best: leaf_best = d
        # single-deletion shift of the mode set
        a1, a2 = MA
        s = 0 if not (a1 > m2 or m1 > a2) else (a1 - m2 if a1 > m2 else -(m1 - a2))
        shifts.add((len(nb[v]), s))
    return dict(name=name, n=n, unimodal=uni, best_dist=best, best_vertex=bestv, leaf_best=leaf_best,
                shift_range=(min(s for _, s in shifts), max(s for _, s in shifts)),
                shifts_by_degree=sorted(set((d, s) for d, s in shifts if s != 0)))
tests = []
for n in (40, 60, 80, 120): 
    for _ in range({40: 40, 60: 20, 80: 10, 120: 4}[n]): tests.append(('pruefer%d' % n, pruefer(n)))
for n in (40, 80):
    for _ in range(10): tests.append(('recursive%d' % n, relabel([-1] + [random.randrange(v) for v in range(1, n)])))
for t in (2, 3, 5, 8, 12):
    for l in (2, 3, 5, 8, 12): tests.append((f'hubs({t},{l})', hubs(t, l)))
for arms in ((3, 4, 4), (5, 5, 5), (8, 8, 8), (4, 5, 6, 7), (5,) * 8, (8,) * 6): tests.append((f'core{arms}', core_tree(arms)))
for legs in ((2,) * 6, (3,) * 8, (2,) * 15, (1, 2, 3, 4, 5, 6), (5,) * 5): tests.append((f'spider{legs[:3]}x{len(legs)}', spider(list(legs))))
for b, d in ((2, 5), (3, 3), (4, 3), (6, 2), (10, 2)): tests.append((f'kary({b},{d})', kary(b, d)))
for sp, legs in ((10, (3,)), (20, (1,)), (15, (2, 0)), (8, (6,)), (30, (1, 0))): tests.append((f'cat({sp},{legs})', caterpillar(sp, list(legs))))
t0 = time.time(); worst = 0; nonaligned = []; shift_out = []
for name, par in tests:
    r = analyse(name, par)
    if r['best_dist'] > 1: nonaligned.append(r)
    if r['shift_range'][0] < -1 or r['shift_range'][1] > 1: shift_out.append((name, r['shift_range'], r['shifts_by_degree'][:6]))
    worst = max(worst, r['best_dist'])
print('trees', len(tests), 'max over trees of min alignment distance', worst, 'trees with no aligned vertex', len(nonaligned), 'secs', round(time.time() - t0))
for r in nonaligned[:10]: print('  NOALIGN', r)
print('trees with a single-deletion mode shift outside {-1,0,1}:', len(shift_out))
for s in shift_out[:10]: print('  ', s)
lb = [(r['name'], r['leaf_best']) for r in map(lambda t: analyse(*t), tests[:0])]
