"""Window LC for forests built from non-log-concave trees (the only case not covered by Hoggar products)."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from families import core_tree

def poly(par): return L.uni_poly(par, L.children_of(par))
def mul(a, b):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] += x*y
    return c
def window_bad(p, n):
    a = len(p)-1; q = -(-n//4); LM = (2*a+1)//3
    return [k for k in range(max(q,1), min(LM, a-1)+1) if p[k]*p[k] <= p[k-1]*p[k+1]]   # strict failure (<=)

if __name__ == '__main__':
    nonlc = []
    for t in range(2, 6):
        for arms in itertools.combinations_with_replacement(range(1, 10), t):
            par = core_tree(arms); p = poly(par)
            if any(p[k]*p[k] < p[k-1]*p[k+1] for k in range(1, len(p)-1)) and len(par) <= 70:
                nonlc.append((len(par), p, arms))
    print('non-LC core trees (n<=70):', len(nonlc))
    small = {'K1': [1,1], 'K2': [1,2], 'P3': [1,3,1], 'K13': [1,4,3,1], 'P4': [1,4,3], 'K15': [1,6,10,10,5,1]}
    sn = {'K1':1,'K2':2,'P3':3,'K13':4,'P4':4,'K15':6}
    checked = bad = 0; examples = []
    # (a) one non-LC tree plus 0..6 copies of each small component type
    for (n0, p0, arms) in nonlc:
        for name, ps in small.items():
            p = p0; n = n0
            for c in range(1, 7):
                p = mul(p, ps); n += sn[name]; checked += 1
                wb = window_bad(p, n)
                if wb: bad += 1; examples.append(('one', arms, name, c, wb))
    # (b) two non-LC trees (products of pairs), and pair plus K1's
    for (n1, p1, a1), (n2, p2, a2) in itertools.combinations_with_replacement(nonlc[:120], 2):
        p = mul(p1, p2); n = n1 + n2; checked += 1
        wb = window_bad(p, n)
        if wb: bad += 1; examples.append(('two', a1, a2, wb))
    print('forests checked:', checked, ' strict window-LC failures:', bad)
    for e in examples[:10]: print('  ', e)
