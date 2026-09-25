"""G3 stress test: is WindowLC stable under disjoint union with a non-LC tree?
For f in the 149 non-LC trees (n = 26..30) and g in a family of trees/forests, check strict LC of p(f)p(g) on the
window [ceil(n/4), top(alpha)] of the union (n = n_f + n_g, alpha = alpha_f + alpha_g), and report the minimal
normalised margin n(1 - P_{k-1}P_{k+1}/P_k^2) over the window, and where (k/alpha, and the activity lambda_k at which
the union's hard-core mean equals k)."""
import sys, os, json, math
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def mul(a, b):
    r = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i+j] += x*y
    return r
def top(al): return (2*al + 1)//3

def nonlc_trees():
    H = os.path.dirname(os.path.abspath(__file__)); out = []
    for n, f in ((26, 'wlc_c_n26.json'), (28, 'wlc_c_n28.json'), (29, 'wlc_c_n29.json'), (30, 'wlc_strict_n30.json')):
        for e in json.load(open(os.path.join(H, f)))['examples']:
            lv = [int(x) for x in e.split('levels=')[1].split()[0].split(',')]
            par = L.parents_from_levels(lv); out.append((len(par), L.uni_poly(par, L.children_of(par))))
    return out

def window_margin(P, n):
    a = len(P) - 1; lo = (n + 3)//4; hi = min(top(a), a - 1); best = None
    for k in range(max(lo, 1), hi + 1):
        lhs = P[k]*P[k]; rhs = P[k-1]*P[k+1]
        m = n*(1 - rhs/lhs) if lhs > 10**300 else n*(lhs - rhs)/lhs
        if best is None or m < best[0]: best = (m, k, a)
    return best

def job(args):
    gname, gpoly, gn = args
    worst = None
    for fn, fpoly in NONLC:
        P = mul(fpoly, gpoly); n = fn + gn
        w = window_margin(P, n)
        if w and (worst is None or w[0] < worst[0]): worst = (w[0], w[1], w[2], fn)
    return gname, gn, worst

NONLC = nonlc_trees()
if __name__ == '__main__':
    fams = []
    B = [1, 1]
    for m in range(1, 201): fams.append(('P%d' % m, L.uni_poly(list(range(-1, m - 1)), L.children_of(list(range(-1, m - 1)))) if m >= 1 else [1], m))
    for m in range(1, 60): fams.append(('%dK2' % m, [1] + [0]*0 if False else None, 2*m))
    fams = [(nm, (p if p is not None else None), gn) for nm, p, gn in fams]
    fixed = []
    for nm, p, gn in fams:
        if p is None:
            m = gn // 2; q = [1]
            for _ in range(m): q = mul(q, [1, 2])
            p = q
        fixed.append((nm, p, gn))
    for t in range(0, 30): fixed.append(('K1,%d' % t, [1, 1] if t == 0 else [sum(x) for x in zip((lambda b: b)([math.comb(t, i) for i in range(t + 1)]), [0, 1] + [0]*(t - 1))], t + 1))
    for n in range(4, 15):
        for lv in L.free_trees(n):
            par = L.parents_from_levels(lv); fixed.append(('T%d:%s' % (n, ''.join(map(str, lv))), L.uni_poly(par, L.children_of(par)), n))
    for fn, fp in NONLC[:30]: fixed.append(('nonLC%d' % fn, fp, fn))
    with Pool(3) as pool: res = list(pool.imap_unordered(job, fixed, chunksize=20))
    res = [r for r in res if r[2] is not None]
    res.sort(key=lambda r: r[2][0])
    neg = [r for r in res if r[2][0] <= 0]
    print('G3 stress: %d partner forests g x 149 non-LC trees f | window-LC failures: %d' % (len(res), len(neg)))
    for r in res[:10]:
        print('  g=%-24s n_g=%3d | min window n*margin %.4f at k=%d (alpha=%d, k/alpha=%.3f), f order %d' % (r[0][:24], r[1], r[2][0], r[2][1], r[2][2], r[2][1]/r[2][2], r[2][3]))
