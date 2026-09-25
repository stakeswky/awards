"""Compare, for single activities l, the Hoelder-method upper exponent a_H(l) = 2 - 2/p*(l), where
   p*(l) = inf{ p : sup_{y>=0} y q^p / log(1+r) <= 1 },  r = l e^{-y}, q = r/(1+r)
(the condition in FLNYZ Lemma 4.2 at a single activity), with the lower exponent from adaptive nested-hub trees."""
import math
from rm_adaptive import run

def sup_y(p, l):
    best = 0.0; yb = 0.0
    for j in range(1, 40001):
        y = j*0.001; r = l*math.exp(-y); q = r/(1 + r); A = math.log1p(r)
        if A <= 0: break
        v = y*q**p/A
        if v > best: best, yb = v, y
    return best, yb
def p_star(l):
    lo, hi = 1.0 + 1e-9, 2.0
    for _ in range(50):
        mid = (lo + hi)/2
        if sup_y(mid, l)[0] <= 1: hi = mid
        else: lo = mid
    return hi, sup_y(hi, l)[1]

def build(l, k, yt, levels):
    counts = []; R = l
    for _ in range(levels):
        counts.append(k); R = l*math.exp(-k*math.log1p(R))
        L = math.log1p(R)
        if L <= 1e-300: return None
        d = max(1, round(yt/L)); counts.append(d); R = l*math.exp(-d*math.log1p(R))
    return counts

def lower(l, ystar):
    best = None
    ys = sorted(set([round(ystar*f, 3) for f in (0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4)] + [1.0, 2.0, 3.0]))
    for k in list(range(2, 60)) + [70, 85, 100, 120, 150, 200, 260, 340, 450]:
        for yt in ys:
            c = build(l, k, yt, 40)
            if c is None: continue
            h = run(c, l)
            (n1, m1, _), (n2, m2, _) = h[24], h[39]
            if m2 <= 0: continue
            s = (m2 - m1)/(n2 - n1)
            if best is None or s > best[0]: best = (s, k, yt)
    return best

if __name__ == '__main__':
    print('%-6s %-9s %-9s %-10s %-10s %s' % ('l', 'p*(l)', 'y at sup', 'a_H=2-2/p*', 'a_lower', 'best (k, y_target)'))
    for l in (0.25, 0.5, 1.0, 2.0, 2.6, 3.0, 5.0, 7.0, 12.0):
        p, ys = p_star(l); aH = 2 - 2/p
        lb = lower(l, ys)
        print('%-6s %-9.5f %-9.3f %-10.4f %-10.4f %s' % (l, p, ys, aH, lb[0], (lb[1], lb[2])), flush=True)
