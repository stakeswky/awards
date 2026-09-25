"""SYNC-EXISTS test for the inductive scheme.
H(F): p(F) is log-concave at every k in [1, top(F)], top(F) = ceil((2 alpha(F) - 1)/3) = (2a+1)//3.
For a vertex v: A = p(F - v), C = p(F - N[v]); X_k(v) = a_{k-1}c_k + a_{k+1}c_{k-2} - 2 a_k c_{k-1}.
Exact identity: p_k^2 - p_{k-1}p_{k+1} = [a_k^2 - a_{k-1}a_{k+1}] + [c_{k-1}^2 - c_{k-2}c_k] - X_k(v).
Inductive step: if alpha(F-v) = alpha and alpha(F-N[v]) = alpha-1 (nesting) and X_k(v) <= 0 for all
k in [1, top(F)], then H(F-v) and H(F-N[v]) imply H(F).
SYNC-EXISTS(F): some vertex v satisfies nesting and X_k(v) <= 0 on [1, top(F)].
Works on forests given as parent arrays (parent < child; -1 for roots)."""
import sys, os, random, itertools
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def g(a, i): return a[i] if 0 <= i < len(a) else 0

def sync_info(par):
    n = len(par); ch = L.children_of(par)
    p = L.uni_poly(par, ch); a = len(p) - 1; top = (2*a + 1)//3
    ks = list(range(1, min(top, a - 1) + 1)) if a >= 2 else []
    deg = [len(ch[v]) + (par[v] >= 0) for v in range(n)]
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    good = []; good_nest = []
    for v in range(n):
        A = L.uni_poly(par, ch, removed=frozenset([v])); C = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        ok = all(g(A, k-1)*g(C, k) + g(A, k+1)*g(C, k-2) - 2*g(A, k)*g(C, k-1) <= 0 for k in ks)
        if ok:
            good.append(v)
            if len(A) - 1 == a and len(C) - 1 == a - 1: good_nest.append(v)
    return dict(n=n, alpha=a, top=top, deg=deg, good=good, good_nest=good_nest,
                leaf_nest=[v for v in good_nest if deg[v] == 1], support_nest=[v for v in good_nest if any(deg[w] == 1 for w in nbr[v])])

def tree_job(lv):
    r = sync_info(L.parents_from_levels(lv))
    return (bool(r['good']), bool(r['good_nest']), bool(r['leaf_nest']), bool(r['support_nest']), None if r['good_nest'] else list(lv))

def forest_from(parts):
    """disjoint union of parent arrays"""
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
            fails = [r[4] for r in res if not r[1]]
            print('trees n=%d: %d | sync v exists: %d | sync+nesting v exists: %d | via a leaf: %d | via a support vertex: %d | first nesting failure: %s' % (
                n, len(res), sum(r[0] for r in res), sum(r[1] for r in res), sum(r[2] for r in res), sum(r[3] for r in res), fails[:1]), flush=True)
    elif which == 'forests':
        rng = random.Random(5); small = {}
        for n in range(1, 12):
            small[n] = [L.parents_from_levels(lv) for lv in L.free_trees(n)] if n >= 2 else [[-1]]
        tot = ok = okn = 0; firstfail = None
        for _ in range(int(sys.argv[2])):
            c = rng.randint(2, 4); parts = []
            for _ in range(c):
                m = rng.randint(1, 11); parts.append(rng.choice(small[m]))
            F = forest_from(parts); r = sync_info(F); tot += 1; ok += bool(r['good']); okn += bool(r['good_nest'])
            if not r['good_nest'] and firstfail is None: firstfail = parts
        print('random forests (2-4 components, each <=11 vertices): %d | sync v exists: %d | sync+nesting: %d | first nesting failure: %s' % (tot, ok, okn, firstfail))
