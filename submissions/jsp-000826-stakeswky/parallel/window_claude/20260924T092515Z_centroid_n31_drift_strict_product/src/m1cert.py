"""Exact certificate: the drift condition M1 (m_{r+1} <= m_r + 1) fails for the tree core((8,)*17),
deep in the tail, while that tree is unimodal. Also prints where M1 fails relative to alpha, the mode
and the window [ceil(n/4), ceil((2a-1)/3)-2]."""
from fractions import Fraction as Fr
from ip import indep_poly
from families import core_tree
import json, sys
def analyse(name, par):
    p = indep_poly(par); n = len(par); a = len(p) - 1
    m = [Fr((r + 1) * p[r + 1], p[r]) for r in range(a)]
    bad = [r for r in range(a - 1) if (r + 2) * p[r] * p[r + 2] > (r + 1) * p[r + 1] ** 2 + p[r] * p[r + 1]]
    q, top = (n + 3) // 4, (2 * a + 1) // 3
    k = 0
    while k < a and p[k] <= p[k + 1]: k += 1
    uni = all(p[t] >= p[t + 1] for t in range(k, a))
    mode = 0
    while mode < a and p[mode] < p[mode + 1]: mode += 1
    return dict(name=name, n=n, alpha=a, mode=mode, window=[q, top - 2], unimodal=uni,
                m1_fail_r=bad, m1_fail_in_window=[r for r in bad if q <= r <= top - 2],
                worst=None if not bad else dict(r=bad[0], drift=str(m[bad[0] + 1] - m[bad[0]]),
                     drift_float=float(m[bad[0] + 1] - m[bad[0]]), m_r=float(m[bad[0]]), r_over_alpha=bad[0] / a),
                p=p)
out = []
for s, k in [(8, 17), (8, 16), (8, 18), (8, 20)]:
    d = analyse(f'core(({s},)*{k})', core_tree((s,) * k)); out.append(d)
    print(d['name'], 'n', d['n'], 'alpha', d['alpha'], 'mode', d['mode'], 'window', d['window'], 'unimodal', d['unimodal'],
          'M1 fails at r =', d['m1_fail_r'], 'in window:', d['m1_fail_in_window'], d['worst'] and (d['worst']['drift_float'], d['worst']['r_over_alpha']))
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'm1_certificate.json', 'w'), indent=1)
