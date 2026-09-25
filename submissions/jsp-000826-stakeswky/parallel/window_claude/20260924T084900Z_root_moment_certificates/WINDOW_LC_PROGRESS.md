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

## 7. Continuation (2026-09-24): large-tree adversarial tests

These are exact computations; all trees tested are unimodal and strictly log-concave on the window.

| Family | Coverage | Window failures | Non-LC trees | Min window margin x n, margin = 1 - p_{k-1}p_{k+1}/p_k^2 |
|---|---|---|---|---|
| Complete b-ary trees, b = 2..6 | up to 4,095 vertices (binary depth 11, ternary depth 7, ...) | 0 | 0 (fully LC) | converges to about 6.8 (b=2), 5.26 (b=3), 4.8 (b=4), 4.64 (b=5), 4.54 (b=6) |
| Spherically symmetric trees with alternating branching | 248 trees, n <= 3000 | 0 | 28 (breaks in the tail) | 3.27 |
| Uniform random labelled trees (Pruefer) | 4,000 trees, 40 <= n <= 400 | 0 | 0 | 6.15 |

These trees are where the hard-core model is most non-local (deep regular trees), a regime that
exhaustive enumeration cannot reach. Across all computations of this run, the window LC margin
stays at least about 2.2/n.

## 8. A vertex-splitting induction scheme and its exact obstruction

For a forest F, a vertex v and an index k, put A = p(F-v) and C = p(F-N[v]), so that p = A + xC.
Exactly:

    p_k^2 - p_{k-1}p_{k+1} = [a_k^2 - a_{k-1}a_{k+1}] + [c_{k-1}^2 - c_{k-2}c_k] - X_k(v),
    X_k(v) = a_{k-1}c_k + a_{k+1}c_{k-2} - 2 a_k c_{k-1}.

**Scheme.** Let P(F) be LC on [1, top(alpha(F))], with top(alpha) = ceil((2 alpha - 1)/3). If, for
each k in that range, some vertex v has X_k(v) <= 0 and both pieces are covered at the needed index
(inside their own P-range, or at or above their own alpha), then P of the two smaller forests gives
P(F). P for all forests implies WindowLC, hence Erdős #993. The base case (orders <= 30) is
settled computationally.

**Findings** (exact, all trees with n <= 17 and all 149 non-LC trees with n = 26..30):

- A **synchronising vertex** (X_k(v) <= 0 simultaneously for every k in [1, top]) exists for
  **every** tested tree, including all non-LC trees.
- The **covering** fails only at the **top index** k = top(alpha), for about 5% of trees with
  n = 16, 62% of the non-LC trees, and 2.6% of random small forests. Shifting the range by one does
  not help; the failure moves with the top.

**Mechanism (smallest example: hubs(2,3), n=9, k=5).**

- The maximum independent set is unique (centre plus leaves). Every vertex in it synchronises
  (X = -58 or -63), but deleting it lowers alpha to 6, so the piece's P-range stops at 4.
- The pieces are in fact LC at k=5 (surplus 20), just not guaranteed by P.
- The two hubs keep alpha = 7 but have X = +7 > 0. Their piece has LC surplus 189, which
  outweighs X.

So the obstruction lies in the purely sign-based hypothesis, not in LC itself. The natural repair
is a quantitative hypothesis: lower bounds on LC surpluses, of order c p_k^2 / n as observed, which
are transferred through the identity. That repair is not carried out here.

### 8b. Quantitative version

**Hypothesis.** Q_c(F): p_k^2 - p_{k-1}p_{k+1} >= (c/n) p_k^2 for every k in [1, top(alpha(F))].

**Step.** For each k, find v with gA a_k^2 + gC c_{k-1}^2 - X_k(v) >= (c/n) p_k^2, where gA and gC are
the margins guaranteed for the pieces: c/(n-1) and c/(n-1-deg v) inside their ranges, and exact at
or beyond their alpha. No sign condition on X is required.

**Results** (exact; c = 1 and 2; all trees with n <= 15 and all 149 non-LC trees with n = 26..30):

- Q_c itself holds for **every** tested tree (c = 2), which supports a quantitative WindowLC
  conjecture with margin 2/n for trees. Over forests the largest admissible constant is 3/2: the
  forest 2K1 has n(p_1^2 - p_0 p_2)/p_1^2 = 3/2 (see Section 9).
- The step fails **only at the top index**: for about 5% of trees with n = 15, and for 92 of the
  149 non-LC trees (all at k = 11 for n = 29).
- The cause is the **gap zone** top(alpha_A) < k < alpha_A of a piece whose alpha dropped by one.
  There the hypothesis guarantees nothing, and the pieces that keep alpha have X_k too large.

**Suggested repair** (carried out in Section 9). Inside the gap zone the formalized Levit–Mandrescu tail
still gives monotonicity. This yields sA(k) >= -a_k (a_{k-1} - a_k), a descent-type lower bound of
the same form as the project's slack S. Feeding it into the identity gives a two-regime
hypothesis: an LC margin on [1, top] and a descent-controlled defect in the tail. Whether that
closes is open.

## 9. Continuation (2026-09-24): the repaired scheme, the constant 3/2, and why one-step splitting cannot close

This section carries out the repair suggested in 8b and then tests it well beyond the exhaustive
range. The outcome is negative for the scheme as a proof strategy. There are explicit trees and
forests (orders 20 to 58) where the inductive step fails for every vertex, although the hypothesis
itself holds for them. The obstruction is identified exactly.

### 9.1 Precise scheme

- **Hypothesis Q(F).** For every k with 1 <= k <= min(top(alpha), alpha-1):
  2n (p_k^2 - p_{k-1}p_{k+1}) >= 3 p_k^2, that is, margin at least (3/2)/n.
- **Why c = 3/2.** It is the largest constant valid for all forests: the forest 2K1 attains equality at
  k = 1. With c = 2, Q already fails for 2K1. With c = 1, the step below fails at n = 9 (the tree
  hubs(2,3) of Section 8).
- **Q is sufficient.** Q implies strict LC on the window, hence WindowLC. Together with the formalised
  tail monotonicity, it also implies unimodality directly.
- **Lower bounds for a piece P** (order n_P, independence number a_P) at index i:
  - Exact: P_0^2 when i <= 0; 0 when i > a_P; P_i^2 when i = a_P.
  - IH: (3/(2 n_P)) P_i^2 when i <= top(a_P).
  - Gap zone top(a_P) < i < a_P, in increasing strength:
    - **LM**: P_i^2 - P_{i-1}P_i, from `antitoneOn_icoeff_tail`.
    - **TR**: P_i^2 - P_{i-1}P_i * 2(a_P-i)/(i+1), from `tail_ratio`. Both are formalised in
      `ErdosProblem993/Ends.lean`.
    - **TRnu**: P_i^2 - P_{i-1}P_i * (a_P-i+min(a_P-i, n_P-a_P))/(i+1). This follows from König:
      e(J) = alpha(H_J) + nu(H_J) and nu(H_J) <= nu(P) = n_P - a_P. Not formalised. It was checked on
      all forests with n <= 12 (24495 inequalities, 0 violations).
- **STEP(F,k).** Some vertex v satisfies
  LB_{F-v}(k) + LB_{F-N[v]}(k-1) - X_k(v) >= (3/(2n)) p_k^2.
- **Rigorous implication** (strong induction on n): if STEP(F,k) holds for every forest and every k
  in range, then Q holds for every forest. With LM or TR bounds, nK1 must be handled directly by the
  binomial computation n(n+1) >= (3/2)(k+1)(n-k+1), which holds for n >= 2.

### 9.2 Exhaustive evidence (small orders)

All results use exact arithmetic, in two implementations:

- Python with `Fraction` (`quant_scheme_lm.py`).
- C with `__int128` (`stepc.c` for trees; `stepf.c` for forests).
- `stepf.c` enumerates every forest of order n as T - r, for every tree T of order n+1 and every
  vertex r.

Cross-checks:

- With c = 1, both implementations find exactly the same single failing tree at n = 9.
- Tree counts equal OEIS A000055.
- At n = 12, the checksums equal those of `wlc.c` and `wlc3.c`.

| class | range | Q fails | STEP (LM bound) fails |
|---|---|---|---|
| all trees | 4 <= n <= 30 (23,522,619,472 trees) | 0 | 0 |
| all forests with an edge | order <= 19 (26.1e6 instances T - r) | 0 | 0 |
| all forests with an edge | order 20 (45.0e6 instances) | 0 | 1 forest: S(2,2,2,2) + 11 K1 |
| all forests with an edge | order 21 (123.7e6 instances) | 0 | 2 forests: S(2^5) + 10 K1, P5 + 16 K1 |
| all forests with an edge | order 22 (341.0e6 instances) | 0 | 2 forests: P7 + 15 K1, S(2,2,2) + 15 K1 |
| edgeless nK1 | n <= 14 | 0 | fails for n = 6, 7, 9, 10, 12, 13 (Q for nK1 is proved directly) |
| non-LC trees | all 149 with n = 26..30 | 0 | 0 |

Minimal normalised margin n(1 - p_{k-1}p_{k+1}/p_k^2) over [1, top] for trees: 2.22 at n = 4, 5
(stars), then 2.40, 2.64, 2.92, 3.21 for n = 6..9, rising to 3.75 at n = 30. Over forests of order
20, 21 and 22 the minima are 3.596, 3.608 and 3.631.

Hence Q holds for every tree with n <= 30 and every forest of order <= 22. STEP with the LM bound
holds for every forest of order <= 19, and its smallest failure is at order 20 (exact, by
exhaustion).

### 9.3 Structure of the witnesses (small orders)

- **Pendant-star centres.** A pendant-star centre is a support vertex with at most one non-leaf
  neighbour. For every tree with n <= 15 other than a star, and every forest with n <= 12 that is not
  a star forest, some pendant-star centre is a single witness for all k simultaneously. Neither "the
  centre with the fewest leaves" nor "a degree-2 vertex adjacent to a leaf" works in general: both
  fail on the same tree with n = 15.
- **Nested witnesses.** A vertex v is nested if it lies in some but not all maximum independent sets.
  Then alpha(F-v) = alpha and alpha(F-N[v]) = alpha-1, so both pieces are inside their IH ranges and
  **no gap-zone bound is ever used**. A nested vertex exists if and only if the maximum independent
  set is not unique.
- **STEP_nested.** This is STEP restricted to nested witnesses and IH-only bounds.
  - Python: it holds for every non-unique-MIS tree with n <= 16 and every non-unique-MIS forest
    with n <= 12.
  - C (`stepcn.c`, `stepfn.c`): it holds for every non-unique-MIS tree with n <= 26 and every
    non-unique-MIS forest of order <= 20. The C code aborts if a gap-zone index is ever needed; it
    never is.
  - Python and C agree on the unique-MIS counts 19, 145, 661, 3206 for n = 9, 12, 14, 16.
  - The share of unique-MIS trees falls with n: 16.6% at n = 16, 10.4% at n = 20 (85,790), 6.6% at
    n = 24 (2,583,328), 5.2% at n = 26 (14,619,303).

### 9.4 The obstruction: STEP is false beyond the exhaustive range

Every example below was confirmed by a second, independent computation (`closed_form_checks.py`,
`verify_obstruction_claims.py`):

- R(s,0): closed-form pieces for each vertex orbit, with p = A + xC asserted for each.
- T + mK1, including S(2,2,2,2) + 11 K1: pieces by brute-force subset enumeration on T, times
  binomials.
- Star forests: vertex-level code, against the component-level evaluator.

In every example Q holds; only the inductive step fails.

| example | order | k = top | STEP fails with |
|---|---|---|---|
| S(2,2,2,2) + 11 K1 (spider, four legs of length 2) | 20 | 11 | LM; the unique failure of order 20 (passes with TR, TRnu) |
| P5 + 16 K1 | 21 | 13 | LM (best orbit slack -0.040 p_k^2/n; true n*margin 4.49) |
| S(2,2,2) + 21 K1 (spider with three legs of length 2) | 28 | 17 | LM and TR (passes with TRnu) |
| 12 P3 + 13 K1 | 49 | 25 | LM, TR and TRnu |
| 28 K_{1,3} + 3 K1 | 115 | 58 | LM, TR and TRnu |
| R(19,0) (tree) | 58 | 26 | LM, TR and TRnu |

Here R(s,0) is the tree formed by a root joined to the centres of s cherries K_{1,2}. For n <= 90 it fails exactly
for s = 19, 21, 22, 24, 25, 27, 28. These are the s >= 19 with alpha = 2s+1 ≢ 2 (mod 3); R(20,0),
R(23,0) and R(26,0) pass. The best slack at k = top
decreases linearly in s: -0.08, -0.28, -0.44, -0.64 for s = 19, 21, 22, 24; -1.38 at s = 30;
-5.02 at s = 60.

Scans with the TRnu bound:

- s K_{1,t} + m K1 with n <= 160: 1061 failing forests, all with t = 2 or t = 3; t >= 4 does not fail
  in this range.
- R(s,m) with n <= 90 (m even, or 3 | s): 7 failing trees, all with m = 0.
- Spiders S(2^s, 1^m) (s legs of length 2, m pendant leaves): none fail (n <= 90).

**Mechanism.**

- Every failure occurs at k = top(alpha) with top(alpha) = top(alpha-1) + 1, in a forest whose maximum
  independent set is unique. This was checked programmatically for all 1061 star-forest failures and
  all 7 R(s,0) failures.
- Such a forest has no nested vertex. Every split therefore either removes a vertex of the unique MIS
  (so alpha(F-v) = alpha - 1) or puts F-N[v] at least one index past its own top. Some piece is
  always needed one index into its gap zone.
- There the extension-counting bounds are worst-case over the independent k-sets J. They overstate
  P_{i+1}/P_i by a factor of about 2, and the resulting deficit grows linearly with the number of
  components or branches.
- **Diagnostic.** For R(s,0) with v a cherry centre, the piece C = (s-1)P3 is real-rooted.
  Replacing its gap bound by Newton's inequality (true for real-rooted polynomials) turns the slack
  from -0.08 ... -5.02 into +1.82 ... +2.02 for s = 19 ... 60. So the obstruction is exactly the
  quality of the gap-zone bound, not LC itself.

**Consequence.** One-step vertex splitting cannot prove WindowLC with this kind of hypothesis. That
is, any hypothesis supported on [1, top(alpha)], closed under IH, and completed by
extension-counting bounds in the gap zone fails. What is missing is a lower bound for the LC surplus
of a forest just beyond 2 alpha/3. Along chains of unique-MIS splits the excess over top can
accumulate, so this is a statement of the same type as WindowLC itself, and the scheme does not
reduce the problem. The exhaustive small-order success (9.2) is misleading. The smallest failures
are at order 20 for LM (exact minimum, by exhaustion), and at orders 28 (TR) and 49 (TRnu) among
the families tested. For TR and TRnu these orders are not claimed to be minimal.

### 9.5 What remains: the unique-MIS class

Conditional reduction (rigorous): Q holds for all forests provided that

- (N) STEP_nested holds for every forest with a non-unique maximum independent set, and
- (U) Q holds for every forest with a unique maximum independent set.

Part (N) uses the induction hypothesis only, with no gap-zone input, and has no counterexample so
far (9.3). Part (U) is the real difficulty. Unique-MIS trees are 5-17% of all trees for
n = 16..26, and include hubs(2,3), R(s,0), and every example of 9.4.

For a unique-MIS forest with MIS I, write N_I(S) = N(S) ∩ I. Then
p(x) = sum over independent S ⊆ V \ I of x^{|S|} (1+x)^{alpha - |N_I(S)|}, with |N_I(S)| >= |S| + 1
for S nonempty. Otherwise (I \ N_I(S)) ∪ S would be a second maximum independent set. In particular,
every vertex outside I has at least two neighbours in I. This is the
population representation used by the colour-mass criteria of earlier stages. A direct argument for
(U) through it is the natural next target.

**Stress tests of (N) beyond the exhaustive range** (exact, c = 3/2, nested witnesses, IH-only bounds;
`nested_stress.py`, `nested_adv.py`):

| family | size | STEP_nested fails | min slack (units p_k^2/n) |
|---|---|---|---|
| s P3 + m K1 + K2 (without the K2, STEP fails; see 9.4) | 2140 forests, n <= 140 | 0 | 0.83 |
| R(s,1): R(s,0) plus one pendant leaf at the root | s <= 29, n <= 88 | 0 | 1.10 |
| random trees (Pruefer) with a non-unique MIS | 209 trees, n = 40..70 | 0 | 1.01 |
| unique-MIS forest U plus one K2 or P4, U in {R(s,0), s P3 + m K1, s K_{1,3} + m K1} | 80 forests, n <= 95 | 0 | 0.98 |

**Caveat on what (N) buys.** STEP_nested does not use gap-zone bounds for the pieces, but X_k(v)
is evaluated exactly. For F = U + K2 with v an end of the K2, write Q = p(U). Then
p = (1+2x)Q, A = (1+x)Q, C = Q and

    X_k = -[Q_{k-1}Q_k - Q_{k-2}Q_{k+1}] - 2 (Q_{k-1}^2 - Q_{k-2}Q_k),

which encodes the LC behaviour of Q itself at k-1 and k. When top jumps, k can sit one index past
top(alpha(U)). Nested splitting therefore moves the gap-zone information into the cross term
rather than removing it.

For a nested v, with a = a_k, c = c_{k-1} and n_C = n-1-deg v, STEP_nested is equivalent to the
quantitative synchronisation inequality

    X_k(v) <= (3/2) [ a^2/(n(n-1)) + c^2 (deg v + 1)/(n n_C) - 2ac/n ].

This is an interlacing-type statement about the pair (A, xC), which have the same degree. It is not
evidently easier than LC.

**Why no full-range hypothesis rescues the scheme.**

- The boundary problem disappears only if the hypothesis covers every index up to alpha-1. But the
  LC defect near alpha is not small. For example, take the non-LC tree with n = 30 and alpha = 16
  (levels 0,1,2,3,2,3,2,3,2,3,2,3,1,2,3,2,3,2,3,2,3,1,2,3,2,3,2,3,2,3). Its tail is
  p_13..p_16 = 76126, 10238, 77, 1, so p_14 p_16 / p_15^2 = 1.7268 at k = alpha-1.
- Even the weak form "p_k/k! is LC", i.e. p_{k-1}p_{k+1} <= (1+1/k) p_k^2 at every k, is therefore
  false for trees.
- Structural facts about the non-LC trees:
  - Of the 149 non-LC trees with n = 26..30, 119 have a unique maximum independent set, and all have
    at most 3.
  - The irregular behaviour sits in (U), at the very end of the sequence.
  - Near 2 alpha/3 the sequences are regular; there, the counting bounds are what is weak.
- A proof has to see this regularity in the middle of the range: for example local-limit or
  hard-core-model estimates of the kind FLNYZ use for n >= N0, made quantitative. Worst-case
  extension counting cannot provide it.

**Relation to FLNYZ.** The missing regularity beyond top is exactly what FLNYZ supply
asymptotically. In `ErdosProblem993/Central.lean`, the theorem `central` gives strict LC at every k
with ceil(n/5) <= k <= floor(64 alpha/95), for all forests of order >= N0. Its ingredients are
`mean_range`, which places these k between the hard-core means at activities 1/4 and 12, and the
CLT-based `mean_lc`. Since 64/95 > 2/3, the central interval extends 2 alpha/285 - O(1) indices past
top(alpha). This covers the gap-zone indices top(alpha_P) + O(1) of any piece with alpha_P of order
a few hundred and order >= N0.

So the splitting scheme would close above the (existential) FLNYZ threshold, but `main_fin`
already covers that range. The open range 31 <= n < N0 needs this central regularity with an
explicit, small threshold. The natural next step is therefore to make `mean_lc` effective, not to
refine the combinatorial induction.

**Effectiveness audit of `mean_lc`.** Every constant below was checked against the Lean source.

- No step is ineffective: there are no compactness arguments and no limits without rates. Every
  existential wraps a computable quantity.
- Explicit constants:
  - `charFn_bound` (Fourier.lean:695): |chi(t)| <= exp(-n sin^2(t/2)/114244);
  - `linear_variance` (CLT.lean:1074): Var >= n/(8*13^4) = n/228488;
  - `exists_scalar_two` (RootMoments.lean:456): b = 999/1000;
  - `exists_scalar_p` (RootMoments.lean:527): theta = 1-(1-b)/8 = 7999/8000 and
    p = 3/2 + theta/2 = 31999/16000;
  - `root_moments` (RootMoments.lean:1097): u = p/(2-p) = 31999 and a = 1 - 1/u = 31998/31999.
- `stdCharFn_tendsto_gaussian` (CLT.lean:1861) chooses the reveal threshold
  b = ceil(eta^{1/(a-1)}) + 1 = ceil(eta^{-31999}) + 1 and returns N = ceil(Lambda^2/c) + 1, with
  Lambda >= b. Here eta = min((eps/(4R))^2 c/K1, eps c/(2 R^2 K2)), and
  K2 >= 1 + potL(a) = 1 + 1/(2^{1/31999} - 1) ≈ 46165.
- Consequence: for eps <= 1 and R >= 1, eta <= 4.7e-11, so b >= 10^{330364}. An explicit N0 read off
  from the formalisation as it stands therefore exceeds 10^{660000}.
- The obstruction is the root-moment exponent a = 1 - 1/31999, which sits extremely close to 1.
  Making this route useful for 31 <= n < N0 needs a genuinely sharper analytic argument (an exponent
  well below 1, much better constants), not just bookkeeping.

### 9.6 Files (in `src/`)

- **Repaired scheme and constant scans:** `quant_scheme_lm.py` (LM-repaired scheme, rational c),
  `step_broad.py`, `step_forests.py` (exhaustive forests as multisets of trees), `cscan.py`,
  `norm_scan.py`, `ulc_scheme.py` (the ULC(∞) normalisation, which closes less often).
- **C implementations:** `stepc.c` (trees), `stepf.c` (forests via T - r), and the nested-mode
  variants `stepcn.c` and `stepfn.c`.
- **Witness structure:** `step_anatomy.py`, `step_canonical.py`, `step_rules.py`,
  `step_support_exc.py`, `step_nested.py`, `nested_stress.py`, `nested_adv.py`.
- **Gap-zone bounds and obstructions:** `quant_scheme_tr.py` (TR and TRnu bounds), `comp_step.py`
  (component-level evaluator), `star_scan.py`, `star_fail_detail.py`, `step_isolated.py`,
  `spider_step.py`, `smallest_fail.py`, `closed_form_checks.py`, `verify_obstruction_claims.py`,
  `wlc_ratio_nonlc.py`.

## 10. Continuation (2026-09-24, later): nested splits are a product problem; how far FLNYZ can be sharpened

### 10.1 Nested splits and ratio interlacing

- **Ratio interlacing, trees n <= 16.** For every tree with n <= 16 that has a nested vertex, some
  nested v makes A = p(F-v) and B = x p(F-N[v]) *ratio-interlacing on the whole range [1, alpha-1]*:
      b_{k+1} a_{k-1} <= a_k b_k   and   a_{k+1} b_{k-1} <= a_k b_k,
  hence X_k(v) <= 0 (`interlace_test.py`). The counts are 1, 3, 5, ..., 16114 trees for
  n = 5..16, with 0 exceptions.
- **The U + K2 identity.** This is exact; it was checked on all 45115 pairs (U, k) with |U| <= 14.
  Let U be any forest, Q = p(U) and F = U + K2. Then
      s_F(k) = (1 + 2 Q_{k-1}/Q_k) s_Q(k) + (4 + 2 Q_{k+1}/Q_k) s_Q(k-1).
  For nested v in the K2, interlacing is equivalent to LC of Q at k-1 and k.
- **What this means.** When top jumps, window LC of U + K2 therefore needs U just past its own top.
  For U + mK2 = (1+2x)^m Q, it needs a binomially weighted positivity of Q's surpluses up to about
  top + O(sqrt m).
  - So (N) is not independent of (U). Any complete induction must control products with
    components whose top is exceeded, which is the G3 (disjoint union) problem.
  - Interlacing is the right structural notion for a single split, but it cannot by itself
    decouple the problem.
- **G3 stress test** (`g3_stress.py`, `slow_saturation.py`). This probes whether window LC is
  stable under disjoint union with a non-LC tree.
  - Setup: each of the 149 non-LC trees (n = 26..30) was multiplied by 5763 partner forests:
    - paths up to P200;
    - mK2 for m <= 59;
    - stars up to K_{1,29};
    - all trees 4..14;
    - 30 non-LC trees;
    - the slowest-saturating trees of each order <= 18, in up to 4 copies (7152 further unions).
  - Result: no window-LC failure. The minimal normalised window margin is 5.23 (partner K_{1,29});
    with slow-saturating partners it is 7.51.

### 10.2 Which activities does the window need?

For a forest F, let lambda*(F) be the activity at which the hard-core mean equals 2 alpha/3, and
lambda_lo(F) the activity at which it equals n/4 (`mean_range_scan.py`).

- lambda*: at most **2.581** over all trees n <= 20 (n = 17). The structured families peak at 2.53,
  and long-leg spiders tend to 1 + sqrt 2 ≈ 2.414.
- lambda_lo: at least **0.34** (stars).
- Both quantities are monotone under disjoint union (means and alpha add). Hence the window needs
  only activities in [1/4, Lambda] with Lambda ≈ 2.6, if a sharper mean-range lemma
  mu_F(Lambda) >= top(alpha_F) can be proved for some Lambda <= 3. FLNYZ use [1/4, 12], proving
  mu(12) >= 64 alpha/95.

### 10.3 Root moments: polynomial, and the FLNYZ Hoelder exponent is sharp

FLNYZ `root_moments` (paper Prop. 4.1) bounds

    M(v) = q_v(1-q_v) delta_v^2 = Cov(1_v, |I|)^2 / Var(1_v)

by C n^a. An earlier version of this section conjectured M = O(log^2 n). **That conjecture is false.**

- **Small trees are misleading.** Over all trees n <= 18, max M <= 0.47. Adversarial leaf-regraft
  search up to n = 400 fits M ≈ 0.13 ln n (`root_moment_growth.py`, `rm_climb.py`). The growth only
  becomes visible at n ≳ 10^5.
- **Counterexample family: adaptive nested hubs** (`nested_hubs.py`, `rm_hp_adaptive.py`). Build a
  spherically symmetric tree bottom-up, alternating two kinds of level:
  - a *hub level*, where every vertex has k children;
  - a *gather level*, where every vertex has d children, with d = round(y_t / ln(1+R_hub)) chosen from
    the current state so that y = sum_children ln(1+R) ≈ y_t.

  This keeps the R-trajectory on an unstable (expanding) orbit. Because
  delta_v = d log R_v / d log lambda, delta then grows by the orbit's expansion factor per double
  level.
  - For exactly periodic child counts the orbit is attracting and delta stays bounded
    (`rm_exponent.py`), so the adaptive choice is essential.
  - Example (l = 1, k = 14): M = 9.63, 135.5, 1893, 26647, 373951, 5254278 at n ≈ 10^5.4, 10^8.4,
    10^11.5, 10^14.5, 10^17.6, 10^20.6. These values agree to 1e-13 between double precision and
    60-digit Decimal (`rm_highprec_check.py`); for comparison, (ln n)^2 ≈ 2260 at the last size.
- **Rigorous certificates** (`rm_certificate.py`). n is computed exactly as an integer; the recursion
  is evaluated in outward-rounded interval arithmetic (Decimal, 80 digits, correctly rounded ln/exp
  widened by a relative 1e-75; rechecked at 300 digits):
  - l = 1, k = 14, 6 double levels: n has 21 digits (log10 n = 20.647) and
    M ∈ [5.254278e6, 5.254278e6], so M/(ln n)^2 >= 2325.
  - l = 3, k = 18, y_t = 2.814, 24 double levels: n has 71 digits and M ∈ [4.562450e41, 4.562450e41],
    so M/(ln n)^2 >= 1.7e37 and log M / log n >= 0.588.
- **Numerical caveat, handled.** On long chains, double-precision states drift off the unstable orbit.
  Counts chosen from drifted states give a different, non-growing tree (`rm_highprec_check.py` shows
  the discrepancy). All exponent estimates below therefore choose d from 250-digit states. Rerunning
  at 400 digits gives the same values: the log M values differ by less than 1e-9.
- **Sharpness.** Let p*(l) = inf{ p : sup_{y>=0} y q^p / log(1+r) <= 1 } (the single-activity form of
  FLNYZ Lemma 4.2), and a_H(l) = 2 - 2/p*(l). Then the Hoelder induction gives
  M <= C n^{a_H(l)+eps}, while the construction gives M >= n^{a(l)} with (`rm_sharpness.py`,
  `rm_hp_adaptive.py`, slope over double levels 12..24):

| l | 0.5 | 1 | 2 | 2.6 | 3 | 5 | 7 | 12 |
|---|---|---|---|---|---|---|---|---|
| a_H(l) = 2-2/p* (upper) | 0.4567 | 0.5217 | 0.6094 | 0.6493 | 0.6726 | 0.7639 | 0.8300 | 0.9426 |
| construction (lower) | 0.4561 | 0.5212 | 0.6092 | 0.6486 | 0.6717 | 0.7603 | 0.8279 | 0.9340 |

  The optimal y_t of the construction coincides with the maximiser y of the scalar function (for
  example 3.146 at l = 1), so the two sides are the same mechanism. **The true root-moment exponent
  is a*(l) = 2 - 2/p*(l)**, established numerically to about 3 decimals, and FLNYZ's Hoelder
  induction is sharp up to eps. No polylogarithmic bound exists. Uniformly over K = [1/4, Lambda],
  the best exponent is a*(Lambda): about 0.672 for Lambda = 3 and about 0.94 for Lambda = 12.

### 10.4 Sharpening FLNYZ: free and paid improvements

All scalar values below were computed by `scalar_sup.py`; the Lean constants were checked in the
source. The following improvements need **no new mathematics**:

1. **Scalar sup.** `exists_scalar_two` uses b = 999/1000, but the true
   sup_{l in [1/4,12], y >= 0} y q^2 / log(1+r) is 0.9103, attained at (l, y) = (12, 2.74).
2. **Hoelder exponent.** Interpolating between 3/2 and 2 with theta = 1-(1-b)/8 forces p ≈ 2. The
   smallest p with sup y q^p / log(1+r) < 1 is **p = 1.8915**. That gives u = p/(2-p) = 17.4
   (instead of 31999) and a = 0.943. The reveal threshold b = eta^{-u} shrinks accordingly.
3. **Fourier constant.** `charFn_bound` bounds beta = min(l/(1+l), 2l/(1+l)^2) >= 1/338 and
   (1+l)^2 <= 169 *separately* (Fourier.lean:659, 679). The joint minimum of beta/(1+l)^2 on
   [1/4, 12] is 0.142/169. So c = 1/114244 improves to about 1/2380, a factor of 48.

The following improvements need **new lemmas**:

4. **K = [1/4, 3].** This requires a sharper mean-range lemma, mu(3) >= top(alpha); see 10.2 for the
   evidence. FLNYZ's own argument (paper Prop. 7.1: E_l X >= alpha log(1+l)/Q*(l), with
   Q*(l) = sqrt((1+l)/l) [3 log 2/sqrt 2 + 2 log((sqrt l + sqrt(1+l))/(1+sqrt 2))]) gives only
   0.513 alpha at l = 3. It reaches 2/3 only at l ≈ 10.3 (0.681 at l = 12), while the true minimum
   of mu(3)/alpha over trees is about 0.69. A genuinely better argument is needed. Then:
   - the sup at exponent 2 is 0.492, the smallest admissible p is 1.5067, u = 3.05 and a = 0.673;
   - the Fourier constant becomes about 1/85;
   - the variance constant becomes 1/(8*4^4) = 1/2048.
5. **Root moments cannot help further (10.3).** The exponent a*(Lambda) = 2 - 2/p*(Lambda) is
   attained by explicit trees. Once K is fixed, the optimal Hoelder exponent of item 2 or 4 is already
   essentially best possible; a polylog lemma does not exist.

**Scale after items 1–4 (rough estimate; item 5 is impossible).** The remaining costs are the standardised
characteristic-function constant (c_1/(pi^2 C_var), still ~1e-6), the Gaussian-tail radius R ~ 1e3
and eta ~ 1e-15. The threshold N ~ (b R)^2 / c then remains of order 1e30 or more. The analytic
route can come down from 10^660000 by many orders of magnitude, but not to the exhaustive range
n ≈ 30. Closing 31 <= n < N0 needs a different idea for moderate n.

### 10.5 Literature check (web; key items verified against the sources)

- **FLNYZ, arXiv:2609.20961 v1 (17 Sep 2026).** The title is "Unimodality of Independence Polynomials
  for Sufficiently Large Forests".
  - Verified in the PDF text: Theorem 1.2 proves strict LC for n/5 <= k <= 17 alpha(F)/25, with
    fugacities in [1/4, 12].
  - The upper fugacity 12 comes from Lemma 4.2 via "12 < e^{5/2}".
  - Proposition 4.1 has a in (2/3, 1).
  - Section 9 remarks that 17/25 is not optimal and that "it is possible that b_lc = 1".
  - The Lean formalisation audited here (commit b2a1d3e, Central.lean) states the slightly weaker
    upper end floor(64 alpha/95). Both exceed 2/3.
- **Chen–Yang–Yin–Zhang, arXiv:2404.04668, "Spectral Independence Beyond Total Influence on Trees
  and Related Graphs".** Verified abstract: constant spectral independence and an optimal spectral
  gap for the hard-core model on all trees (any maximum degree) with fugacity below e^2. This covers
  K = [1/4, 3].
  - Spectral independence controls sum_v q_v(1-q_v) delta_v^2 only on average.
  - A per-vertex polylog root-moment bound is impossible (10.3), so spectral independence cannot
    be upgraded to that.
- **Zero-free-region route (Michelen–Sahasrabudhe) is closed for all trees.** Surveyed, not
  re-derived here:
  - Every connected graph's independence polynomial divides that of some tree of the same maximum
    degree (Bencs).
  - Zeros of regular trees accumulate at lambda_c(Delta). This lies in [0.258, 4] for
    Delta = 3..13, hence inside [1/4, 3].
  - So there is no zero-free neighbourhood of the needed activities that is uniform over trees.
- **No explicit LCLT for all trees (unbounded degree) was found.** Jain–Perkins–Sah–Sawhney
  (arXiv:2108.01161) need bounded degree and uniqueness.
- **Ramos–Sun, arXiv:2510.18826, "An AI enhanced approach to the tree unimodality conjecture".**
  Verified abstract: "tens of thousands of new counter-examples to log-concavity" with 27 to 101
  vertices; no public data link in the abstract. These would be natural extra inputs for the G3
  stress test of 10.1.
