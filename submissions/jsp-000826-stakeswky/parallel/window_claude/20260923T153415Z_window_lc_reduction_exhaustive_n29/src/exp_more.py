import sys, os
from math import comb
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from exp_g123 import rows_of, flip, mul_rows, dmass_pair, history_positions, populations

def tailcheck(n):
    """population tail bound: p nonincreasing from ceil(mu*(R)) for each side; compare with beta and LM."""
    res = dict(n=n, trees=0, viol=0, better_than_beta=0, better_than_LM=0, deg3_trees=0, deg3_bound_eq=0)
    for lv in L.free_trees(n):
        par = L.parents_from_levels(lv); rows = rows_of(par); p = [sum(r) for r in rows]
        alpha, h, beta = L.params(p, n, n); LM = -(-(2*alpha-1)//3)
        res['trees'] += 1
        best = None
        for side in (0, 1):
            pops = populations(rows, side)
            mustar = max(Fr(2*m + k - 1, 2) for (m, k) in pops)      # max_S (m + (k-1)/2)
            t0 = -(-mustar.numerator // mustar.denominator)          # ceil
            if any(p[r+1] > p[r] for r in range(max(t0, 0), len(p)-1)): res['viol'] += 1
            best = t0 if best is None else min(best, t0)
        res['better_than_beta'] += best < beta
        res['better_than_LM'] += best < LM
        # trees where some colour class has all degrees >= 3
        ch = L.children_of(par); col = L.colours(par)
        deg = [len(ch[v]) + (par[v] >= 0) for v in range(n)]
        for c in (0, 1):
            R = [v for v in range(n) if col[v] == c]
            if R and all(deg[v] >= 3 for v in R):
                res['deg3_trees'] += 1
                Lsz = n - len(R)
                pops = populations(rows, 1 - c if False else (1 if c == 1 else 0))
                mustar = max(Fr(2*m + k - 1, 2) for (m, k) in pops)
                res['deg3_bound_eq'] += (mustar == Fr(Lsz - 1, 2))
    return res

def e2(n):
    res = dict(n=n, pairs=0, viol=0, max_ratio=Fr(0))
    for lv in L.free_trees(n):
        par = L.parents_from_levels(lv); rows = rows_of(par); p = [sum(r) for r in rows]
        for j in history_positions(p):
            a = p[j]
            for i in range(j):
                if not (p[i] > p[i+1] and all(p[k] >= p[k+1] for k in range(i+1, j))): continue
                dm, _, _ = dmass_pair(rows, i, j); Si = a*(p[i]-p[i+1]); res['pairs'] += 1
                if dm > Si: res['viol'] += 1
                if Si and Fr(dm, Si) > res['max_ratio']: res['max_ratio'] = Fr(dm, Si)
    return res

def f3(args):
    (n1, R1), rest = args
    out = dict(forests=0, positions=0, viol_best=0, viol_worst=0, max_worst=Fr(0))
    for (n2, R2) in rest:
        for (n3, R3) in rest:
            if not (n1 <= n2 <= n3): continue
            out['forests'] += 1
            opts = []
            for f2 in (0, 1):
                for f3_ in (0, 1):
                    A = mul_rows(R1, flip(R2) if f2 else R2); A = mul_rows(A, flip(R3) if f3_ else R3); opts.append(A)
            p = [sum(r) for r in opts[0]]
            for j in history_positions(p):
                b, a = p[j-1], p[j]; S = a*(b-a); vals = [dmass_pair(o, j-1, j)[0] for o in opts]
                out['positions'] += 1
                if (S == 0 and min(vals) > 0) or (S and min(vals) > S): out['viol_best'] += 1
                if (S == 0 and max(vals) > 0) or (S and max(vals) > S): out['viol_worst'] += 1
                if S and Fr(max(vals), S) > out['max_worst']: out['max_worst'] = Fr(max(vals), S)
    return out

if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'tail':
        with Pool(9) as pool:
            for r in pool.imap(tailcheck, range(4, int(sys.argv[2])+1)):
                print('TAIL n=%d trees=%d violations=%d  best-side bound < beta: %d  < LM: %d | trees with a colour class all deg>=3: %d, mu*=(|L|-1)/2 holds: %d' % (r['n'], r['trees'], r['viol'], r['better_than_beta'], r['better_than_LM'], r['deg3_trees'], r['deg3_bound_eq']), flush=True)
    elif what == 'e2':
        with Pool(9) as pool:
            for r in pool.imap(e2, range(18, int(sys.argv[2])+1)):
                print('E2 n=%d anchor-pairs=%d violations=%d max=%.5f' % (r['n'], r['pairs'], r['viol'], float(r['max_ratio'])), flush=True)
    elif what == 'f3':
        NMAX = int(sys.argv[2]); trees = [(1, [[1], [0, 1]])]
        for n in range(2, NMAX-1):
            for lv in L.free_trees(n): trees.append((n, rows_of(L.parents_from_levels(lv))))
        jobs = [(t, [u for u in trees if u[0] >= t[0] and 2*u[0] + t[0] <= NMAX]) for t in trees if 3*t[0] <= NMAX]
        # restrict total order via filtering inside: keep only triples with n1+n2+n3<=NMAX
        def ok(t): return True
        tot = dict(forests=0, positions=0, viol_best=0, viol_worst=0, max_worst=Fr(0))
        jobs2 = []
        for t, rest in jobs:
            jobs2.append((t, [u for u in rest if t[0] + u[0] <= NMAX]))
        with Pool(9) as pool:
            for r in pool.imap_unordered(f3, jobs2):
                for k in ('forests', 'positions', 'viol_best', 'viol_worst'): tot[k] += r[k]
                tot['max_worst'] = max(tot['max_worst'], r['max_worst'])
        print('F3 three-component forests (n1<=n2<=n3, pairwise sums bounded, see filter) NMAX=%d:' % NMAX, {k: (float(v) if isinstance(v, Fr) else v) for k, v in tot.items()})
