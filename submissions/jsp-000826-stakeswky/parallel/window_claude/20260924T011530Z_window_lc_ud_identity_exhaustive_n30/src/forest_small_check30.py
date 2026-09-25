"""All forests of total order <= 30 that contain a non-log-concave component: one non-LC tree
(orders 26..29, taken from the exhaustive C runs) plus any forest of order <= 30 - |T|."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def mul(a, b):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] += x*y
    return c
small = {0: {'empty': [1]}, 1: {'K1': [1,1]}, 2: {'2K1': [1,2,1], 'K2': [1,2]},
         3: {'3K1': [1,3,3,1], 'K1+K2': [1,3,2], 'P3': [1,3,1]},
         4: {'4K1': [1,4,6,4,1], '2K1+K2': [1,4,5,2], '2K2': [1,4,4], 'K1+P3': [1,4,4,1], 'P4': [1,4,3], 'K13': [1,4,3,1]}}
nonlc = []
for n in (26, 27, 28, 29, 30):
    d = json.load(open(os.path.join(HERE, ('wlc_strict_n%d.json' % n if n == 30 else 'wlc_c_n%d.json' % n))))
    for e in d['examples']:
        p = [int(x) for x in e.split('p=')[1].split(',')]
        nonlc.append((n, p))
print('non-LC trees collected:', [(n, sum(1 for m, _ in nonlc if m == n)) for n in (26, 27, 28, 29, 30)])
checked = bad = 0
for n0, p0 in nonlc:
    for r in range(0, 30 - n0 + 1):
        for name, q in small[r].items():
            p = mul(p0, q); n = n0 + r; a = len(p) - 1
            lo = (n + 3)//4; hi = (2*a + 1)//3
            fails = [k for k in range(max(lo, 1), min(hi, a - 1) + 1) if p[k]*p[k] <= p[k-1]*p[k+1]]
            # also whole-sequence unimodality
            k = 0
            while k < a and p[k] <= p[k+1]: k += 1
            uni = all(p[t] >= p[t+1] for t in range(k, a))
            checked += 1
            if fails or not uni: bad += 1; print('FAIL', n0, name, fails, uni)
print('forests of order <= 30 with a non-LC component checked:', checked, ' strict window-LC or unimodality failures:', bad)
