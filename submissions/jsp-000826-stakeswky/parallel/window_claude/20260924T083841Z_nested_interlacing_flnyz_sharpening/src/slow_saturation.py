"""Find trees whose hard-core mean reaches 2/3 of alpha only at a large activity lambda* (slow saturation),
then re-run the G3 stress test with such partners (and disjoint unions of them)."""
import sys, os, math
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from g3_stress import NONLC, mul, window_margin, top

def mean_at(p, lam):
    num = den = 0.0; x = 1.0
    for k, c in enumerate(p):
        w = c * lam**k; num += k*w; den += w
    return num/den
def lam_star(p, frac=2/3):
    a = len(p) - 1; target = frac*a; lo, hi = 1e-6, 1e6
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        if mean_at(p, mid) < target: lo = mid
        else: hi = mid
    return lo

def job(lv):
    par = L.parents_from_levels(lv); p = L.uni_poly(par, L.children_of(par))
    return lam_star(p), tuple(lv), p

if __name__ == '__main__':
    best = []
    for n in range(4, int(sys.argv[1]) + 1):
        with Pool(3) as pool: res = list(pool.imap_unordered(job, [tuple(lv) for lv in L.free_trees(n)], chunksize=200))
        res.sort(key=lambda r: -r[0])
        best += res[:3]
        print('n=%d: max lambda* = %.3f  levels=%s' % (n, res[0][0], ','.join(map(str, res[0][1]))), flush=True)
    best.sort(key=lambda r: -r[0])
    # G3 test with the slowest partners, and unions of up to 4 copies
    worst = None; fails = 0; tested = 0
    for lamv, lv, gp in best[:12]:
        gn = len(lv)
        for copies in range(1, 5):
            G = [1]
            for _ in range(copies): G = mul(G, gp)
            for fn, fp in NONLC:
                P = mul(fp, G); n = fn + copies*gn
                w = window_margin(P, n); tested += 1
                if w[0] <= 0: fails += 1
                if worst is None or w[0] < worst[0]: worst = (w[0], w[1], w[2], lamv, copies, gn)
    print('G3 with slow-saturating partners: %d unions tested | window-LC failures %d | min n*margin %.4f at k=%d alpha=%d (partner lambda*=%.2f, %d copies of order %d)' % (
        tested, fails, worst[0], worst[1], worst[2], worst[3], worst[4], worst[5]))
