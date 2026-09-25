"""Structure of the 149 non-LC trees (n = 26..30): unique-MIS count, number of maximum independent sets,
and the largest LC defect k*(p_{k-1}p_{k+1}/p_k^2 - 1)."""
import sys, json, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
H = os.path.dirname(os.path.abspath(__file__)); tot = uniq = 0; pa = []; worst = None
for n, f in ((26, 'wlc_c_n26.json'), (28, 'wlc_c_n28.json'), (29, 'wlc_c_n29.json'), (30, 'wlc_strict_n30.json')):
    for e in json.load(open(os.path.join(H, f)))['examples']:
        lv = [int(x) for x in e.split('levels=')[1].split()[0].split(',')]
        par = L.parents_from_levels(lv); ch = L.children_of(par); p = L.uni_poly(par, ch); a = len(p) - 1
        nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(len(par))]
        nested = any(len(L.uni_poly(par, ch, removed=frozenset([v]))) - 1 == a and
                     len(L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))) - 1 == a - 1 for v in range(len(par)))
        tot += 1; uniq += (not nested); pa.append(p[a])
        for k in range(1, a):
            r = Fr(p[k-1]*p[k+1], p[k]**2)
            if worst is None or k*(r - 1) > worst[0]: worst = (k*(r - 1), n, k, a, float(r))
print('non-LC trees: %d | unique MIS: %d | #maximum independent sets: min %d max %d | max k*(ratio-1) = %.4f at n=%d k=%d alpha=%d ratio=%.6f' % (
    tot, uniq, min(pa), max(pa), float(worst[0]), worst[1], worst[2], worst[3], worst[4]))
