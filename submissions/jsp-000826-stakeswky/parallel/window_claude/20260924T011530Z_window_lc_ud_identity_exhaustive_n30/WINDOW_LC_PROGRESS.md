# Progress on WindowLC: an exact extension identity and a Newton-type strengthening

Independent Claude window, continuation of run `20260923T153415Z`. **ORIGINAL=NOT_CLOSED.**
WindowLC is **not** proved for orders n >= 31. This note records:

- a new exact identity valid for every graph;
- a sufficient condition (UD) for window log-concavity, with its exact coefficient form;
- the numerical evidence for UD;
- a refuted route;
- the extension of the exhaustive verification to n = 30.

## 1. The extension identity (every finite simple graph)

For an independent set J let Ext(J) = V \ N[J] be the set of addable vertices and e(J) = |Ext(J)|.
For J uniform in I_r, write mu_r = E e(J). Double counting pairs (J, v) with v in Ext(J) gives
mu_r = (r+1) p_{r+1} / p_r.

**Identity.** For k >= 1 with p_{k-1} > 0,

    mu_k = mu_{k-1} + Var_{k-1}(e)/mu_{k-1} - 1 - D_k,

where D_k is the average, over uniformly chosen extension pairs (J,v) with |J| = k-1 and v in
Ext(J), of |N(v) ∩ Ext(J)|.

*Proof.* A uniform extension pair (J,v) produces J+v uniform in I_k: each k-set arises from exactly
k pairs. Its J-marginal is the e-size-biased law, so E_pairs e(J) = E e^2 / E e =
mu_{k-1} + Var_{k-1}(e)/mu_{k-1}. Moreover e(J+v) = e(J) - 1 - |N(v) ∩ Ext(J)|. ∎

**Corollary (LC criterion).** p_k^2 >= p_{k-1} p_{k+1} holds if and only if

    Var_{k-1}(e) <= mu_{k-1} (1 + D_k + mu_{k-1}/k).

This is because LC at k is equivalent to mu_k <= mu_{k-1}(k+1)/k.

## 2. Under-dispersion (UD) and its coefficient form

**UD at level k-1** means Var_{k-1}(e) <= mu_{k-1}. Since D_k >= 0, UD at level k-1 implies LC at k.

**Coefficient form.** Count ordered pairs of distinct free vertices. A non-adjacent pair (u,w)
corresponds bijectively to (J+u+w in I_{k+1}, ordered pair of its elements). Adjacent pairs number
2 e(G[Ext(J)]). Hence

    UD at level k-1  <=>  (k p_k)^2 >= k(k+1) p_{k-1} p_{k+1} + 2 p_{k-1} A_k,
    A_k = sum_{uv in E} p_{k-1}(G - N[u] - N[v]).

Equivalently, p_k^2 >= (1 + 1/k) p_{k-1} p_{k+1} + (2/k^2) p_{k-1} A_k. This is a Newton-type
inequality, the kind real-rooted polynomials satisfy, plus a nonnegative edge term. It is strictly
stronger than LC.

## 3. Evidence for UD in the window [ceil(n/4), ceil((2 alpha-1)/3)] (exact rationals)

| Set | Coverage | Max window Var/mu | Window UD failures | Where UD fails (outside the window) |
|---|---|---|---|---|
| All trees | every tree 8 <= n <= 19 | 0.75 at n=8; 0.55–0.63 for 13 <= n <= 19 | 0 | among all trees with 8 <= n <= 19, exactly 2 (both n=18) fail anywhere (k >= 2): both at k = 0.9 alpha, both log-concave there |
| Non-LC trees | all 28 non-LC trees with n <= 29 | 0.198 | 0 | first failure at 0.9286 alpha, the same index where LC fails |
| Core family (Kadrawi–Levit type) | 1,468 trees, n <= 60 | 0.620 | 0 | first failure at 0.842 alpha |
| Hub family | 2,957 trees, n <= 60 | 0.607 | 0 | none |

**Extremal structure.** The window maximisers of Var/mu are path-like trees of maximum degree 3
with alpha ≈ 0.6n, at the right end of the window. These are not the non-LC structures: those
are markedly under-dispersed in the window (<= 0.2). UD fails only in the deep tail
(>= 0.84 alpha), where the formalized Levit–Mandrescu tail already gives monotonicity.

## 4. Refuted route

**Real-rootedness of free-count slices.** g_r(y) = sum_{J in I_r} y^{e(J)} is **not** real-rooted
in general, even inside the window: for n=14 only 73 of 8,718 window positions are real-rooted.
The cause is structural: g_1(y) = sum_v y^{n-1-deg v}. So UD is not a consequence of a
Bernoulli-sum structure, and a proof must bound the variance directly.

## 5. Exhaustive extension to n = 30

**Trees, n = 30.** The C checker `wlc2` (K=10, 2,210 s, exit 0) covered all 14,830,871,802 trees
with n = 30 (equal to OEIS A000055):

- every tree is unimodal;
- 121 trees are non-log-concave, and their first break lies at >= 0.9375 alpha;
- no non-LC index lies in the window, and there are **0** equalities p_k^2 = p_{k-1}p_{k+1} in the
  window, so **strict** WindowLC holds.

Together with the earlier runs, strict window log-concavity holds for **every tree with n <= 30**
(23,522,619,475 trees), and unimodality for every tree with n <= 30.

**Forests of order <= 30.** A forest with a non-LC component is one non-LC tree of order 26–30
plus a forest of the remaining order (<= 4). All 237 such forests satisfy strict WindowLC and
unimodality. Forests whose components are all LC are LC by Hoggar's theorem, which gives the
non-strict window condition; the strict version needs the standard strict-product lemma, not
re-verified here. Hence **(W) holds for every forest of order <= 30**, and the open range for (W)
becomes 31 <= n < N0.

**UD as single-point log-concavity.** Let g_r(y) = [x^r] sum_J x^{|J|} y^{e(J)}. Then
E_r[e(e-1)] <= (E_r e)^2 is equivalent to (log g_r)''(1) <= 0. So UD asks for log-concavity of g_r
at the single point y = 1. Real-rootedness (refuted in §4) would give log-concavity on all of
(0, infinity), which explains why the weaker UD survives.

## 6. What a proof of WindowLC via UD would need

One must prove, for every forest and every k in the window, that the number of addable vertices
of a uniform random independent (k-1)-set is under-dispersed. In correlation form:

    sum_{v != w} Cov(f_v, f_w) <= sum_v P(f_v)^2,    f_v = 1[v addable].

Two effects compete:

- local positive correlations (e.g. siblings sharing a parent);
- the global negative correlation created by the fixed size, which is strong inside the window
  because |J| is a constant fraction of n there.

The observed slack is large: Var/mu <= 0.63 for n >= 13. This suggests that a quantitative
decorrelation argument for the canonical ensemble on trees, not a local CLT, might suffice.
No such argument is known to this run.
