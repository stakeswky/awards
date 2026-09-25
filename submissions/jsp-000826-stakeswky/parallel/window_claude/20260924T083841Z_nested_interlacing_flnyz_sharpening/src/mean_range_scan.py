"""How large an activity is needed so that the hard-core mean reaches the top of the window?
m(lam) = min over forests of mu(lam)/alpha.  FLNYZ (mean_range) use m(12) >= 64/95.  The window [ceil(n/4), top(alpha)]
needs mu(Lambda) >= 2 alpha/3, i.e. Lambda >= lambda*(F) for every forest.  Also the lower end: lambda_lo(F) with mu = n/4.
Exact trees n <= NMAX plus structured large families (spiders with equal legs, caterpillars, brooms, complete d-ary trees)."""
import sys, os, math
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def moments(p, lam):
    # numerically stable via log-scaling
    lw = [math.log(c) + k*math.log(lam) if c > 0 else -1e300 for k, c in enumerate(p)]
    m = max(lw); w = [math.exp(x - m) for x in lw]; Z = sum(w)
    mu = sum(k*x for k, x in enumerate(w))/Z
    return mu
def solve(p, target):
    lo, hi = 1e-9, 1e9
    for _ in range(300):
        mid = math.sqrt(lo*hi)
        if moments(p, mid) < target: lo = mid
        else: hi = mid
    return lo
def stats(p, n):
    a = len(p) - 1
    return solve(p, 2*a/3), solve(p, n/4), a

def job(lv):
    par = L.parents_from_levels(lv); p = L.uni_poly(par, L.children_of(par))
    s = stats(p, len(par)); return s + (tuple(lv),)

def spider(legs):
    par = [-1]
    for l in legs:
        prev = 0
        for _ in range(l): par.append(prev); prev = len(par) - 1
    return par
def caterpillar(spine, leaves_per):
    par = [-1]
    for i in range(1, spine): par.append(i - 1)
    for i in range(spine):
        for _ in range(leaves_per): par.append(i)
    return par
def complete(b, d):
    par = [-1]; fr = [0]
    for _ in range(d):
        nf = []
        for u in fr:
            for _ in range(b): par.append(u); nf.append(len(par) - 1)
        fr = nf
    return par

if __name__ == '__main__':
    hi_all = (0, None); lo_all = (1e9, None)
    for n in range(4, int(sys.argv[1]) + 1):
        with Pool(3) as pool: res = list(pool.imap_unordered(job, [tuple(lv) for lv in L.free_trees(n)], chunksize=200))
        h = max(res, key=lambda r: r[0]); l = min(res, key=lambda r: r[1])
        if h[0] > hi_all[0]: hi_all = (h[0], n, h[3])
        if l[1] < lo_all[0]: lo_all = (l[1], n, l[3])
    print('exact trees 4..%s: max lambda*(top) = %.4f (n=%d) | min lambda_lo(n/4) = %.4f (n=%d)' % (sys.argv[1], hi_all[0], hi_all[1], lo_all[0], lo_all[1]))
    fam = []
    for l in range(1, 9):
        for s in (1, 2, 3, 5, 8, 13, 30, 60):
            if s*l <= 600: fam.append(('spider %d legs of %d' % (s, l), spider([l]*s)))
    for sp in (5, 20, 80, 200):
        for lp in (0, 1, 2, 3, 5):
            fam.append(('caterpillar spine %d leaves %d' % (sp, lp), caterpillar(sp, lp)))
    for b, d in ((2, 3), (2, 5), (2, 7), (3, 3), (3, 4), (4, 3), (5, 3), (10, 2), (30, 1)):
        fam.append(('complete %d-ary depth %d' % (b, d), complete(b, d)))
    out = []
    for name, par in fam:
        p = L.uni_poly(par, L.children_of(par)); n = len(par)
        ls, ll, a = stats(p, n); out.append((ls, ll, name, n, a))
    out.sort(key=lambda r: -r[0])
    print('families, largest lambda* (activity where mean = 2 alpha/3):')
    for r in out[:8]: print('  %-34s n=%4d alpha=%4d  lambda*=%.4f  lambda_lo=%.4f' % (r[2], r[3], r[4], r[0], r[1]))
    print('families, smallest lambda_lo (activity where mean = n/4):')
    for r in sorted(out, key=lambda r: r[1])[:4]: print('  %-34s n=%4d alpha=%4d  lambda*=%.4f  lambda_lo=%.4f' % (r[2], r[3], r[4], r[0], r[1]))
