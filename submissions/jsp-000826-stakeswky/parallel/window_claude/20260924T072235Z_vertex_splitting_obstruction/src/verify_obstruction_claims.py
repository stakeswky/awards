"""Independent checks of the claims in WINDOW_LC_PROGRESS.md 9.4.
(a) T + mK1 examples (S(2,2,2,2) + 11K1 and P5 + 16K1 with LM; S(2,2,2) + 21K1 with TR): piece polynomials from brute-force subset
    enumeration on the small tree T, times binomials; no tree DP from e993lib is used.
(b) Star-forest examples (12 P3 + 13 K1; 28 K_{1,3} + 3 K1): recomputed at vertex level with e993lib, a different code
    path from the component-level evaluator comp_step.py.
(c) For every failure in the scans (T + mK1 families, single-size star forests, R(s,0)): the failing k equals
    top(alpha), top jumps (alpha mod 3 != 2), and the maximum independent set is unique."""
import sys, os, itertools
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
c = Fr(3, 2)
def mul(a, b):
    r = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i+j] += x*y
    return r
def pw(a, e):
    r = [1]
    for _ in range(e): r = mul(r, a)
    return r
def g(a, i): return a[i] if 0 <= i < len(a) else 0
def top(al): return (2*al + 1)//3
def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0: a.pop()
    return a

def brute_poly(nv, edges, removed=()):
    rem = set(removed); verts = [v for v in range(nv) if v not in rem]; cnt = [0]*(nv + 1)
    for r in range(len(verts) + 1):
        for S in itertools.combinations(verts, r):
            s = set(S)
            if all(not (u in s and w in s) for u, w in edges): cnt[r] += 1
    return trim(cnt)

def LB(P, i, nP, gap):
    a = len(P) - 1
    if i <= 0: return Fr(P[0]**2)
    if i > a: return Fr(0)
    if i == a: return Fr(P[i]**2)
    cands = []
    if i <= top(a): cands.append(c/nP*P[i]**2)
    if i >= top(a) and gap == 'LM': cands.append(Fr(P[i]**2 - P[i-1]*P[i]))
    if gap in ('TR', 'TRnu'):
        mult = 2*(a - i) if gap == 'TR' else a - i + min(a - i, nP - a)
        cands.append(Fr(P[i]**2) - Fr(P[i-1]*P[i]*mult, i + 1))
    return max(cands) if cands else None

def step_fails(p, n, pieces, gap):
    a = len(p) - 1; fl = []
    for k in range(1, min(top(a), a - 1) + 1):
        ok = False
        for A, C, d in pieces:
            X = g(A,k-1)*g(C,k) + g(A,k+1)*g(C,k-2) - 2*g(A,k)*g(C,k-1)
            la, lc = LB(A, k, n - 1, gap), LB(C, k - 1, n - 1 - d, gap)
            if la is not None and lc is not None and la + lc - X >= c/n*p[k]**2: ok = True; break
        if not ok: fl.append(k)
    return fl

def tree_plus_iso(nv, edges, m, gap):
    B = [1, 1]; pT = brute_poly(nv, edges); p = trim(mul(pT, pw(B, m))); n = nv + m
    nbr = {v: set() for v in range(nv)}
    for u, w in edges: nbr[u].add(w); nbr[w].add(u)
    pieces = [(mul(brute_poly(nv, edges, [v]), pw(B, m)), mul(brute_poly(nv, edges, [v] + list(nbr[v])), pw(B, m)), len(nbr[v])) for v in range(nv)]
    if m: pieces.append((mul(pT, pw(B, m - 1)), mul(pT, pw(B, m - 1)), 0))
    pieces = [(trim(A), trim(C), d) for A, C, d in pieces]
    for A, C, d in pieces: assert trim([x + y for x, y in zip(A + [0]*len(p), [0] + C + [0]*len(p))]) == p
    return n, len(p) - 1, step_fails(p, n, pieces, gap)

print('(a) brute-force component pieces:')
S2222 = [(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6), (0, 7), (7, 8)]
for gap in ('LM', 'TR', 'TRnu'):
    print('  S(2,2,2,2) + 11K1, %-4s: n, alpha, failing k =' % gap, tree_plus_iso(9, S2222, 11, gap))
P5 = [(0, 1), (1, 2), (2, 3), (3, 4)]
print('  P5 + 16K1, LM   : n, alpha, failing k =', tree_plus_iso(5, P5, 16, 'LM'))
S222 = [(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6)]
print('  S(2,2,2) + 21K1, TR: n, alpha, failing k =', tree_plus_iso(7, S222, 21, 'TR'))
print('  S(2,2,2) + 21K1, TRnu: n, alpha, failing k =', tree_plus_iso(7, S222, 21, 'TRnu'))

print('(b) vertex-level recomputation of the star-forest examples (e993lib + quant_scheme_tr, TRnu):')
import quant_scheme_tr as QT
from step_forests import forest_from
QT.MODE['nu'] = True; QT.MODE['ptr'] = False
for t, s, m in ((2, 12, 13), (3, 28, 3)):
    par = forest_from([[-1] + [0]*t]*s + [[-1]]*m)
    b, fl = QT.step_info(par, c)
    print('  %d K_{1,%d} + %d K1: n=%d | Q holds %s | STEP failing k %s' % (s, t, m, len(par), b, fl))

print('(c) every failure found: k = top, top jumps, unique MIS:')
from comp_step import star, forest_step
bad = 0; tot = 0
for t in range(1, 13):
    for s in range(1, 60):
        for m in range(0, 100):
            if s*(t+1) + m > 160: continue
            q, fl, sl = forest_step([star(t)]*s + [star(0)]*m, c)
            if fl:
                al = s*t + m; tot += 1
                uniq = (t >= 2)            # s K_{1,t} + m K1 has a unique MIS iff t >= 2 (a K2 component has two)
                if not (fl == [top(al)] and al % 3 != 2 and uniq): bad += 1; print('   exception', t, s, m, fl, top(al))
print('  single-size star forests: failures %d, violating the pattern %d' % (tot, bad))
import e993lib as L
from spider_step import step as sp_step
fails = [r for r in (sp_step(('R', s, 0)) for s in range(1, 30)) if r[6]]
print('  R(s,0): failures', [(r[1], r[6], top(r[4]), r[4] % 3) for r in fails], '(k, top, alpha mod 3)')
