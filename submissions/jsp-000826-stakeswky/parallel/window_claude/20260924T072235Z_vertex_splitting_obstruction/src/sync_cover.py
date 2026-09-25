"""Per-index SYNC-COVER test for the inductive scheme.
P(F): LC of p(F) at every k in [1, top(F)], top(F) = (2*alpha(F)+1)//3 = ceil((2 alpha - 1)/3).
Identity (every vertex v, every k):  p_k^2 - p_{k-1}p_{k+1} = sA(k) + sC(k-1) - X_k(v),
 A = p(F-v), C = p(F-N[v]), sA(k) = a_k^2 - a_{k-1}a_{k+1}, X_k(v) = a_{k-1}c_k + a_{k+1}c_{k-2} - 2a_k c_{k-1}.
Covering (so that P of the two smaller forests gives sA(k) >= 0 and sC(k-1) >= 0):
 A-cover: k <= top(A) or k >= alpha(A);   C-cover: k-1 == 0 or k-1 <= top(C) or k-1 >= alpha(C).
SYNC-COVER(F,k): some v has X_k(v) <= 0, A-cover and C-cover.
If SYNC-COVER holds for all k in [1, min(top, alpha-1)] for every forest of order > n0, and P holds for all
forests of order <= n0, then P holds for all forests (strong induction on the order)."""
import sys, os, json, random, itertools
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def g(a, i): return a[i] if 0 <= i < len(a) else 0
def top(alpha): return (2*alpha + 1)//3

def cover_info(par, want_detail=False):
    n = len(par); ch = L.children_of(par)
    p = L.uni_poly(par, ch); a = len(p) - 1; T = top(a)
    ks = list(range(1, min(T, a - 1) + 1)) if a >= 2 else []
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    pieces = []
    for v in range(n):
        A = L.uni_poly(par, ch, removed=frozenset([v])); C = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        pieces.append((v, A, C, len(A) - 1, len(C) - 1))
    uncovered = []; single_v_all = None
    good_by_v = {v: True for v in range(n)}
    for k in ks:
        found = False
        for (v, A, C, aA, aC) in pieces:
            X = g(A, k-1)*g(C, k) + g(A, k+1)*g(C, k-2) - 2*g(A, k)*g(C, k-1)
            covA = (k <= top(aA)) or (k >= aA)
            covC = (k - 1 == 0) or (k - 1 <= top(aC)) or (k - 1 >= aC)
            ok = X <= 0 and covA and covC
            if not ok: good_by_v[v] = False
            if ok: found = True
        if not found: uncovered.append(k)
    single = [v for v, ok in good_by_v.items() if ok]
    return dict(n=n, alpha=a, top=T, uncovered=uncovered, single_v=single, p=p)

def tree_job(lv):
    r = cover_info(L.parents_from_levels(lv))
    return (not r['uncovered'], bool(r['single_v']), None if not r['uncovered'] else (list(lv), r['uncovered']))

def forest_from(parts):
    par = []; off = 0
    for q in parts:
        par += [(-1 if x < 0 else x + off) for x in q]; off += len(q)
    return par

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'trees':
        for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            trees = [tuple(lv) for lv in L.free_trees(n)]
            with Pool(8) as pool:
                res = list(pool.imap_unordered(tree_job, trees, chunksize=300))
            fails = [r[2] for r in res if not r[0]]
            print('trees n=%d: %d | SYNC-COVER at every k: %d | one v for all k: %d | first failure: %s' % (
                n, len(res), sum(r[0] for r in res), sum(r[1] for r in res), fails[:1]), flush=True)
    elif which == 'nonlc':
        H = os.path.dirname(os.path.abspath(__file__)); tot = ok = one = 0; bad = []
        for n, f in ((26, 'wlc_c_n26.json'), (28, 'wlc_c_n28.json'), (29, 'wlc_c_n29.json'), (30, 'wlc_strict_n30.json')):
            for e in json.load(open(os.path.join(H, f)))['examples']:
                lv = [int(x) for x in e.split('levels=')[1].split()[0].split(',')]
                r = cover_info(L.parents_from_levels(lv)); tot += 1; ok += not r['uncovered']; one += bool(r['single_v'])
                if r['uncovered']: bad.append((n, lv, r['uncovered']))
        print('non-LC trees n=26..30: %d | SYNC-COVER at every k: %d | one v for all k: %d | failures: %s' % (tot, ok, one, bad[:2]))
    elif which == 'forests':
        rng = random.Random(7); small = {1: [[-1]]}
        for m in range(2, 13): small[m] = [L.parents_from_levels(lv) for lv in L.free_trees(m)]
        tot = ok = 0; bad = None
        for _ in range(int(sys.argv[2])):
            c = rng.randint(2, 5); parts = [rng.choice(small[rng.randint(1, 12)]) for _ in range(c)]
            r = cover_info(forest_from(parts)); tot += 1; ok += not r['uncovered']
            if r['uncovered'] and bad is None: bad = (parts, r['uncovered'])
        print('random forests (2-5 components, each <=12 vertices): %d | SYNC-COVER at every k: %d | first failure: %s' % (tot, ok, bad))
