"""Search for counterexamples to the candidate lemma:
  F, B positive LC sequences with no internal zeros, F_0 = B_0 = 1, B <= F <= (1+x)^d B coefficientwise
  ==> F + xB unimodal.
Random concave log-sequences, projected onto the constraints, then hill-climbing on a non-unimodality score."""
import random, math
from math import comb
random.seed(7)
def is_lc(a):
    return all(a[i] > 0 for i in range(len(a))) and all(a[i]*a[i] >= a[i-1]*a[i+1] - 1e-9*a[i]*a[i] for i in range(1, len(a)-1))
def unimodal_defect(p):
    # largest "dip": max over j of min(p[l] for l<j max) ... score = max_{i<j<k} min(p_i, p_k) - p_j (relative)
    best = 0.0; n = len(p)
    pre = [0]*n; m = 0
    for i in range(n): m = max(m, p[i]); pre[i] = m
    suf = [0]*n; m = 0
    for i in range(n-1, -1, -1): m = max(m, p[i]); suf[i] = m
    for j in range(1, n-1):
        d = min(pre[j-1], suf[j+1]) - p[j]
        if d > 0: best = max(best, d / p[j])
    return best
def conv(a, b):
    o = [0.0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): o[i+j] += x*y
    return o
def feasible(F, B, d):
    if len(B) > len(F): return False
    if abs(F[0]-1) > 1e-12 or abs(B[0]-1) > 1e-12: return False
    if not (is_lc(F) and is_lc(B)): return False
    U = conv(B, [comb(d, j) for j in range(d+1)])
    for k in range(len(F)):
        b = B[k] if k < len(B) else 0.0
        u = U[k] if k < len(U) else 0.0
        if b > F[k]*(1+1e-12) or F[k] > u*(1+1e-12): return False
    return True
def rand_lc(L):
    # log-concave: increments nonincreasing
    inc = sorted([random.uniform(-3, 3) for _ in range(L-1)], reverse=True)
    s = [0.0]
    for x in inc: s.append(s[-1] + x)
    return [math.exp(v) for v in s]
best = (0, None)
trials = 0; feas = 0
for it in range(200000):
    d = random.randint(2, 12); LB = random.randint(3, 14); LF = LB + random.randint(0, d)
    B = rand_lc(LB); F = rand_lc(LF)
    # scale to satisfy constant terms and try to satisfy sandwich by mixing: F <- max(F*c, B) not LC-preserving; instead reject
    trials += 1
    if not feasible(F, B, d): continue
    feas += 1
    p = [(F[k] if k < len(F) else 0.0) + (B[k-1] if 1 <= k <= len(B) else 0.0) for k in range(max(len(F), len(B)+1))]
    sc = unimodal_defect(p)
    if sc > best[0]: best = (sc, (d, F, B, p))
print('trials', trials, 'feasible', feas, 'max relative dip', best[0])
if best[1]:
    d, F, B, p = best[1]; print('d', d); print('F', [round(x,4) for x in F]); print('B', [round(x,4) for x in B]); print('p', [round(x,4) for x in p])
