import sys, os
from math import comb
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from exp_g123 import rows_of, history_positions, populations

def s1_side(pops, j):
    """returns (holds, lhs, rhs, newpop_mass) for condition sum w tau^2 <= sum w tau with w=g*x (x=pi(j-1)).
    populations with x==0<y (start at j) make it fail (infinite)."""
    lhs = Fr(0); rhs = Fr(0); new = 0
    for (m, k), g in pops.items():
        x = comb(k, j-1-m) if 0 <= j-1-m <= k else 0
        y = comb(k, j-m) if 0 <= j-m <= k else 0
        if x == 0:
            if y > 0: new += g*y
            continue
        tau = Fr(x - y, x)
        lhs += g*x*tau*tau; rhs += g*x*tau
    return (new == 0 and lhs <= rhs), lhs, rhs, new

def run(n):
    res = dict(n=n, mid=0, mid_hold=0, allpos=0, all_hold=0, worst_mid=None)
    for lv in L.free_trees(n):
        par = L.parents_from_levels(lv); rows = rows_of(par); p = [sum(r) for r in rows]
        hp = history_positions(p)
        if not hp: continue
        alpha, h, beta = L.params(p, n, n)
        pops = [populations(rows, s) for s in (0, 1)]
        for j in hp:
            outs = [s1_side(pops[s], j) for s in (0, 1)]
            hold = any(o[0] for o in outs)
            res['allpos'] += 1; res['all_hold'] += hold
            if h + 1 <= j < beta:
                res['mid'] += 1; res['mid_hold'] += hold
                if not hold:
                    cand = [(o[1] / o[2] if o[2] > 0 else Fr(10**9)) for o in outs if o[3] == 0]
                    r = min(cand) if cand else Fr(10**12)   # 10**12 marks: both sides have new populations
                    if res['worst_mid'] is None or r > res['worst_mid'][0]:
                        res['worst_mid'] = (r, list(lv), j)
    return res

if __name__ == '__main__':
    with Pool(9) as pool:
        for r in pool.imap(run, range(8, int(sys.argv[1])+1)):
            w = r['worst_mid']
            print('S1 n=%d  History positions %d, S1 holds (best side) %d  | middle %d, holds %d  worst failing middle ratio %s' % (
                r['n'], r['allpos'], r['all_hold'], r['mid'], r['mid_hold'], None if w is None else (float(w[0]) if w[0] is not None else 'new-pop', w[1], w[2])), flush=True)
