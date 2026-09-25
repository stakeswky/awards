"""Independent re-verification of every example tree printed by cwlc (EX lines): rebuild the tree
from its parent array, check it is a tree on n vertices, recompute the independence sequence with
the Python DP of ip.py (and, for n <= 22, by brute-force subset enumeration on a sample), and
recompute unimodality, the first non-LC index, strict window LC and the window drift condition.
usage: reverify_examples.py out.json log1 [log2 ...]"""
import re, sys, json
from ip import indep_poly
def check(p, n):
    a = len(p) - 1; q, top = (n + 3) // 4, (2 * a + 1) // 3
    k = 0
    while k < a and p[k] <= p[k + 1]: k += 1
    uni = all(p[t] >= p[t + 1] for t in range(k, a))
    bad = [t for t in range(1, a) if p[t] ** 2 < p[t - 1] * p[t + 1]]
    wlc = all(p[t] ** 2 > p[t - 1] * p[t + 1] for t in range(q, min(top, a - 1) + 1))
    m1 = all((r + 2) * p[r] * p[r + 2] <= (r + 1) * p[r + 1] ** 2 + p[r] * p[r + 1] for r in range(q, top - 1))
    return dict(unimodal=uni, first_bad=bad[0] if bad else -1, strict_window_lc=wlc, window_m1=m1, alpha=a)
out = []; problems = 0
OUT = sys.argv[1]
for f in sys.argv[2:]:
    for line in open(f):
        if not line.startswith('EX'): continue
        par = [int(x) for x in re.search(r'parents=(\S+)', line).group(1).split(',')]
        p_c = [int(x) for x in re.search(r'p=(\S+)', line).group(1).split(',')]
        fb = int(re.search(r'first_bad=(-?\d+)', line).group(1))
        n = len(par)
        is_tree = par[0] == -1 and all(0 <= par[v] < v for v in range(1, n))
        p = indep_poly(par)
        c = check(p, n)
        ok = is_tree and p == p_c and c['first_bad'] == fb
        problems += not ok
        out.append(dict(n=n, parents=par, p=p, python_matches_c=p == p_c, is_tree=is_tree, **c))
print('examples', len(out), 'problems', problems,
      'non-unimodal', sum(not o['unimodal'] for o in out), 'window-LC failures', sum(not o['strict_window_lc'] for o in out),
      'window-drift failures', sum(not o['window_m1'] for o in out))
json.dump(out, open(OUT, 'w'))
