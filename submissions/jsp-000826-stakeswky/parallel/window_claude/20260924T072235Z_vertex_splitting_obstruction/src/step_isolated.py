"""Stress test for forests with many isolated vertices / many star components (new LB with tail_ratio).
(a) F = T + m K1 for every tree T with 2 <= |T| <= 7 and 0 <= m <= M;  (b) all star forests of order n <= NS
(disjoint unions of stars K_{1,s}, s >= 0; K1 = K_{1,0}) that have at least one edge."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from quant_scheme_tr import step_info, MODE
if 'nu' in sys.argv[3:]: MODE['nu'] = True
if 'noptr' in sys.argv[3:]: MODE['ptr'] = False
from step_forests import forest_from, partitions
C = Fr(3, 2)

def job(par):
    b, fl, s = step_info(par, C, True)
    return b, fl, s, par

def star(s): return [-1] + [0]*s

if __name__ == '__main__':
    M = int(sys.argv[1]); NS = int(sys.argv[2])
    items = []
    for t in range(2, 8):
        for lv in L.free_trees(t) if t >= 3 else [[0, 1]]:
            T = L.parents_from_levels(lv) if t >= 3 else [-1, 0]
            for m in range(0, M + 1): items.append(('T%d+%dK1' % (t, m), forest_from([T] + [[-1]]*m)))
    with Pool(3) as pool: res = list(pool.imap_unordered(job, [x[1] for x in items], chunksize=20))
    bad = [(len(r[3]), r[1]) for r in res if r[1] or not r[0]]
    print('(a) T + mK1, |T|<=7, m<=%d: %d forests | Q/STEP failures: %d %s | min slack %.4f' % (M, len(res), len(bad), bad[:6], float(min(r[2] for r in res if r[2] is not None))), flush=True)
    for n in range(4, NS + 1):
        fs = [forest_from([star(s - 1) for s in part]) for part in partitions(n) if max(part) >= 2]
        with Pool(3) as pool: res = list(pool.imap_unordered(job, fs, chunksize=20))
        bad = [(sorted(set([sum(1 for x in r[3] if x == -1)])), r[1]) for r in res if r[1] or not r[0]]
        mn = min((r[2], r[3]) for r in res if r[2] is not None)
        print('(b) star forests n=%d: %d | failures: %d | min slack %.4f' % (n, len(res), len(bad), float(mn[0])), flush=True)
