"""True growth of the root-moment quantity  M(v) = q_v (1 - q_v) delta_v^2  (FLNYZ root_moments bounds it by C n^a,
a = 31998/31999).  delta_v = meanDiff = 1 + E|I|(S minus N[v]) - E|I|(S minus v); tree recursion rooted at v:
   R_v = l prod_c 1/(1+R_c),  q_v = R_v/(1+R_v),  delta_v = 1 - sum_c q_c delta_c   (children c of v in the tree rooted at v).
We compute max_v M(v) over (i) all trees with n <= NMAX (exact enumeration, every root v), (ii) large structured families,
for activities l in {1/4, 1, 2.6, 12}, and fit the growth exponent."""
import sys, os, math
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def all_roots_M(adj, l):
    n = len(adj); best = 0.0; arg = None
    for root in range(n):
        order = [root]; parent = {root: -1}
        for u in order:
            for w in adj[u]:
                if w not in parent: parent[w] = u; order.append(w)
        R = {}; D = {}
        for u in reversed(order):
            prodinv = 1.0; s = 0.0
            for w in adj[u]:
                if w != parent[u]:
                    prodinv /= (1 + R[w]); q = R[w]/(1 + R[w]); s += q*D[w]
            R[u] = l*prodinv; D[u] = 1 - s
        q = R[root]/(1 + R[root]); M = q*(1 - q)*D[root]**2
        if M > best: best = M; arg = root
    return best, arg

def adj_from_par(par):
    adj = [[] for _ in par]
    for v, p in enumerate(par):
        if p >= 0: adj[v].append(p); adj[p].append(v)
    return adj

def job(args):
    lv, lams = args
    adj = adj_from_par(L.parents_from_levels(lv))
    return [all_roots_M(adj, l)[0] for l in lams], lv

def spider(legs):
    par = [-1]
    for l in legs:
        prev = 0
        for _ in range(l): par.append(prev); prev = len(par) - 1
    return par
def complete(b, d):
    par = [-1]; fr = [0]
    for _ in range(d):
        nf = []
        for u in fr:
            for _ in range(b): par.append(u); nf.append(len(par) - 1)
        fr = nf
    return par
def broom(handle, bristles):
    par = [-1] + list(range(0, handle - 1))
    for _ in range(bristles): par.append(handle - 1)
    return par
def caterpillar(spine, per):
    par = [-1] + list(range(0, spine - 1))
    for i in range(spine):
        for _ in range(per): par.append(i)
    return par
def double_broom(handle, bristles):
    par = [-1]
    for _ in range(bristles): par.append(0)
    prev = 0
    for _ in range(handle): par.append(prev); prev = len(par) - 1
    for _ in range(bristles): par.append(prev)
    return par

if __name__ == '__main__':
    lams = [0.25, 1.0, 2.6, 12.0]
    print('exact max over all trees and all v of q(1-q)delta^2, by n (columns: l = %s):' % lams)
    for n in range(4, int(sys.argv[1]) + 1):
        with Pool(3) as pool: res = list(pool.imap_unordered(job, [(tuple(lv), lams) for lv in L.free_trees(n)], chunksize=200))
        mx = [max(r[0][i] for r in res) for i in range(len(lams))]
        print('  n=%2d: %s' % (n, '  '.join('%8.4f' % x for x in mx)), flush=True)
    fams = {}
    for n in (10, 30, 100, 300, 1000, 3000):
        fams.setdefault('path', []).append(list(range(-1, n - 1)))
        fams.setdefault('star', []).append([-1] + [0]*(n - 1))
        s = max(1, int(round(math.sqrt(n)))); fams.setdefault('spider sqrt(n) legs', []).append(spider([max(1, n//s)]*s))
        fams.setdefault('broom (n/2 handle)', []).append(broom(n//2, n - n//2))
        fams.setdefault('caterpillar 1 leaf', []).append(caterpillar(n//2, 1))
        fams.setdefault('double broom', []).append(double_broom(n//2, n//4))
    for b in (2, 3, 5):
        for d in range(2, 12):
            if b**d < 5000: fams.setdefault('complete %d-ary' % b, []).append(complete(b, d))
    print('families: max over v of q(1-q)delta^2 (columns: n, then l = %s)' % lams)
    for name, pars in fams.items():
        rows = []
        for par in pars:
            adj = adj_from_par(par)
            rows.append((len(par), [all_roots_M(adj, l)[0] for l in lams]))
        print('  %-22s ' % name + ' | '.join('n=%d: %s' % (n, ','.join('%.3g' % x for x in m)) for n, m in rows))
