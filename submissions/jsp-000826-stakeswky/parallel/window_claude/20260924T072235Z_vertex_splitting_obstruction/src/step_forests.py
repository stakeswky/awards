"""Exhaustive forest test of the LM-repaired quantitative scheme (quant_scheme_lm.step_info).
Forests of order n = multisets of free trees (K1 included) with total order n.
Reports: #forests, Q_c holds, STEP holds at every k, and min over forests/k in [1, min(top, alpha-1)]
of n * (1 - p_{k-1}p_{k+1}/p_k^2) (the largest admissible universal c is bounded by this minimum)."""
import sys, os, itertools
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from quant_scheme_lm import step_info, top

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield []; return
    for m in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - m, m): yield [m] + rest

def forest_from(parts):
    par = []; off = 0
    for q in parts:
        par += [(-1 if x < 0 else x + off) for x in q]; off += len(q)
    return par

TREES = {}
def trees_of(m):
    if m not in TREES:
        TREES[m] = [[-1]] if m == 1 else [L.parents_from_levels(lv) for lv in L.free_trees(m)]
    return TREES[m]

def forests(n):
    for part in partitions(n):
        sizes = sorted(set(part)); choices = []
        for s in sizes:
            choices.append(list(itertools.combinations_with_replacement(range(len(trees_of(s))), part.count(s))))
        for combo in itertools.product(*choices):
            parts = []
            for s, idxs in zip(sizes, combo): parts += [trees_of(s)[i] for i in idxs]
            yield forest_from(parts)

def minmargin(par):
    n = len(par); p = L.uni_poly(par, L.children_of(par)); a = len(p) - 1
    best = None
    for k in range(1, min(top(a), a - 1) + 1):
        m = Fr(n * (p[k]**2 - p[k-1]*p[k+1]), p[k]**2)
        if best is None or m < best: best = m
    return best

def job(args):
    par, c = args
    b, fl = step_info(par, c)
    return b, not fl, None if not fl else (par, fl), minmargin(par)

if __name__ == '__main__':
    c = int(sys.argv[1])
    for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        jobs = [(f, c) for f in forests(n)]
        with Pool(8) as pool: res = list(pool.imap_unordered(job, jobs, chunksize=max(1, len(jobs)//400)))
        mm = [r[3] for r in res if r[3] is not None]
        fails = [r[2] for r in res if not r[1]]
        print('c=%d forests n=%d: %d | Q_c holds: %d | STEP at every k: %d | min n*margin on [1,top]: %s | first STEP failure: %s' % (
            c, n, len(res), sum(r[0] for r in res), sum(r[1] for r in res), (float(min(mm)) if mm else None), fails[:1]), flush=True)
