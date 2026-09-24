import sys, os
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from dispersion2 import profile

def work(chunk):
    worst = 0.0; over_win = 0; over_any = 0; tot = 0
    for lv in chunk:
        n, a, prof = profile(L.parents_from_levels(lv)); tot += 1
        w = [q for (k, q, inw, _) in prof if inw]
        if w: worst = max(worst, max(w))
        over_win += any(q > 1 for (k, q, inw, _) in prof if inw)
        over_any += any(q > 1 for (k, q, inw, _) in prof if k >= 2)
    return tot, worst, over_win, over_any

if __name__ == '__main__':
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        trees = [tuple(lv) for lv in L.free_trees(n)]
        chunks = [trees[i:i+2000] for i in range(0, len(trees), 2000)]
        T = W = OW = OA = 0
        with Pool(int(sys.argv[3])) as pool:
            for tot, worst, ow, oa in pool.imap_unordered(work, chunks):
                T += tot; W = max(W, worst); OW += ow; OA += oa
        print('UD n=%d trees=%d max window Var/mu=%.4f over-dispersed in window=%d over-dispersed anywhere (k>=2)=%d' % (n, T, W, OW, OA), flush=True)
