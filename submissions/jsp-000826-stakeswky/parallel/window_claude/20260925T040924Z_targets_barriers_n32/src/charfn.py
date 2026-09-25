"""Exact product formula I(T; z) = prod_v (1 + R_v(z)), R_v(z) = z prod_{c child of v} 1/(1+R_c(z)),
and the per-vertex characteristic-function decay it gives:
   |phi_lambda(theta)| = prod_v |1 + R_v(lambda e^{i theta})| / (1 + R_v(lambda)).
For a family of trees we measure c_eff(lambda, theta) := -log|phi| / (n sin^2(theta/2)), the best constant
in |phi| <= exp(-c n sin^2(theta/2)), minimised over theta in (0, pi] and lambda in the window range,
and compare with the FLNYZ constant 1/114244 and with what a Fourier proof of window LC needs."""
import cmath, math, random, sys
from modelib import parents_from_levels, indep_poly_del
from ma_forests import free_trees
from families import hubs, core_tree
def ratios(par, z):
    n = len(par); ch = [[] for _ in range(n)]
    for v in range(1, n): ch[par[v]].append(v)
    R = [0j] * n
    for v in range(n - 1, -1, -1):
        r = z
        for c in ch[v]: r = r / (1 + R[c])
        R[v] = r
    return R
_cache = {}
def logabsphi(par, lam, th):
    key = tuple(par)
    if key not in _cache: _cache[key] = indep_poly_del(par)
    p = _cache[key]
    z = lam * cmath.exp(1j * th)
    num = abs(sum(c * z ** k for k, c in enumerate(p))); den = sum(c * lam ** k for k, c in enumerate(p))
    return math.log(num) - math.log(den) if num > 0 else -1e9
# sanity: product formula vs polynomial
par = parents_from_levels([0, 1, 2, 1, 2, 3, 1])
p = indep_poly_del(par); z = 0.7 * cmath.exp(0.9j)
lhs = sum(c * z ** k for k, c in enumerate(p)); rhs = 1
for r in ratios(par, z): rhs *= (1 + r)
print('product formula check', abs(lhs - rhs) < 1e-9)
def ceff(par, lams=(0.25, 0.5, 1, 1.5, 2.6), ths=None):
    n = len(par); ths = ths or [math.pi * k / 60 for k in range(1, 61)]
    best = 1e9; arg = None
    for lam in lams:
        for th in ths:
            v = -logabsphi(par, lam, th) / (n * math.sin(th / 2) ** 2)
            if v < best: best, arg = v, (lam, round(th, 3))
    return best, arg
fam = []
for n in (12, 16, 20):
    worst = (1e9, None)
    for lv in free_trees(n):
        par = parents_from_levels(lv); c, a = ceff(par, ths=[math.pi * k / 12 for k in range(1, 13)])
        if c < worst[0]: worst = (c, a, lv)
    print(f'all trees n={n}: min c_eff = {worst[0]:.5f} at (lambda, theta) = {worst[1]}; tree levels = {worst[2]}', flush=True)
for t, l in ((2, 20), (5, 20), (10, 10), (20, 5), (40, 3)):
    c, a = ceff(hubs(t, l)); print(f'hubs({t},{l}) n={1 + t * (l + 1)}: c_eff = {c:.5f} at {a}')
for arms in ((5,) * 8, (8,) * 17, (10,) * 10):
    c, a = ceff(core_tree(arms)); print(f'core{arms[:1]}x{len(arms)} n={len(core_tree(arms))}: c_eff = {c:.5f} at {a}')
def star(s): return [-1] + [0] * s
for s in (10, 50, 200):
    c, a = ceff(star(s)); print(f'star K_1,{s}: c_eff = {c:.5f} at {a}')
