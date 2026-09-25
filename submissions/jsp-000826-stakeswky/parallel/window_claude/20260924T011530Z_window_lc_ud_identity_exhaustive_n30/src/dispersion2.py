import sys, os, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from ext_identity import size_free_poly, moments
from families import hub_tree, core_tree

def profile(par):
    """for every k>=1: Q_k = Var_{k-1}(e)/mu_{k-1}; window flag; returns (n, alpha, list)"""
    n = len(par); G = size_free_poly(par)
    p = [sum(v for (s, f), v in G.items() if s == k) for k in range(n + 1)]
    while p and p[-1] == 0: p.pop()
    a = len(p) - 1; lo = (n + 3)//4; hi = (2*a + 1)//3; out = []
    for k in range(1, a):
        cnt, mu, var = moments(G, k - 1)
        if mu: out.append((k, float(var/mu), lo <= k <= hi, p[k]*p[k] < p[k-1]*p[k+1]))
    return n, a, out

def summarize(label, pars):
    worst_win = 0.0; first_over = []; win_over = 0; tot = 0
    for par in pars:
        n, a, prof = profile(par); tot += 1
        w = [q for (k, q, inw, _) in prof if inw]
        if w: worst_win = max(worst_win, max(w))
        win_over += any(q > 1 for (k, q, inw, _) in prof if inw)
        ov = [k for (k, q, inw, _) in prof if q > 1 and k >= 2]
        if ov: first_over.append(min(ov) / a)
    print('%s: trees=%d  max window Var/mu=%.4f  trees over-dispersed somewhere in window=%d  smallest (first over-dispersed k>=2)/alpha=%s' % (
        label, tot, worst_win, win_over, None if not first_over else round(min(first_over), 4)), flush=True)

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'exh':
        for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            summarize('all trees n=%d' % n, [L.parents_from_levels(lv) for lv in L.free_trees(n)])
    elif which == 'nonlc':
        pars = []
        for n in (26, 28, 29):
            d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wlc_c_n%d.json' % n)))
            for e in d['examples']:
                lv = [int(x) for x in e.split('levels=')[1].split()[0].split(',')]
                pars.append(L.parents_from_levels(lv))
        summarize('28 non-LC trees (n=26,28,29)', pars)
    elif which == 'fam':
        core = [core_tree(arms, x) for t in range(2, 6) for arms in itertools.combinations_with_replacement(range(1, 8), t) for x in range(0, 2) if 1 + sum(1 + 2*s for s in arms) + x <= 60]
        summarize('core family (n<=60)', core)
        hub = []
        for t1 in range(1, 7):
            for l1 in range(1, 13):
                for t2 in range(0, 3):
                    for l2 in ([None] if t2 == 0 else range(l1 + 1, 15)):
                        groups = ((t1, l1),) if t2 == 0 else ((t1, l1), (t2, l2))
                        if t1 + t2 < 2: continue
                        for s in range(0, 3):
                            par, _ = hub_tree(groups, s, 0)
                            if len(par) <= 60: hub.append(par)
        summarize('hub family (n<=60)', hub)
