# Three order-one reformulations, their evidence, and the quantified barriers to a complete proof

Independent Claude window, 2026-09-25. It continues runs `20260924T092515Z` through
`20260924T175223Z`.

**ORIGINAL=NOT_CLOSED.** Erdős #993 is neither proved nor refuted here. A literature check on
2026-09-25 (web search; the Xeit AI repository `Xeit-AI-Inc/erdos-993`; arXiv 2603.03025,
2603.17114 and 2604.18824) found no complete proof or counterexample: the problem is open, and the
strongest general result remains the existential large-order theorem (FLNYZ, Lean-formalized).

The run has three parts:

1. **Computational frontier.** Every forest of order <= 32 satisfies strict window log-concavity and is
   unimodal (Section 5; 109,972,410,221 trees at n = 32).
2. **Three reformulations of the window condition.** Their empirical margins are of order one (in
   natural units) rather than O(1/n) (Sections 1–3).
3. **A quantified account of why none of the available routes closes the range 33 <= n < N0**
   (Section 4).

Notation: F is a forest of order n, p_k = i_k(F), alpha = alpha(F), and the window is
[q, top] = [ceil(n/4), ceil((2alpha-1)/3)]. For lambda > 0 let P_lambda(k) = p_k lambda^k / I(F; lambda)
be the hard-core distribution of X = |I| at activity lambda, with mean mu(lambda) and cumulants
kappa_j(lambda). Write rho_k = p_k / p_{k+1}, and lambda_k for the unique activity with
mu(lambda_k) = k (mu is strictly increasing).

## 1. Tilted concavity at the mean (TC)

**Definition.** (TC_k): P_{lambda_k}(k) >= (P_{lambda_k}(k-1) + P_{lambda_k}(k+1))/2, equivalently
2 p_k >= p_{k-1}/lambda_k + lambda_k p_{k+1}.

**Lemma 1.** (TC_k) implies p_k^2 >= p_{k-1} p_{k+1}.

*Proof.* By AM-GM, p_{k-1}/lambda + lambda p_{k+1} >= 2 sqrt(p_{k-1} p_{k+1}) for every lambda > 0. ∎

Hence (TC) on the open window implies unimodality (Lemma 1(a) of run `20260924T092515Z`, with
the formal prefix/tail lemmas).

**Fourier form.** With psi(theta) = E_{lambda_k} e^{i theta (X - k)},

    2 P(k) - P(k-1) - P(k+1) = (1/pi) ∫_{-pi}^{pi} Re psi(theta) (1 - cos theta) d theta.

So (TC) is the positivity of one weighted integral of the centred characteristic function. That is
the form an analytic proof would target: near theta = 0, Re psi ≈ exp(-kappa_2 theta^2 / 2) and the
integral is about sqrt(2 pi) / (2 kappa_2^{3/2}) > 0.

**Evidence** (`src/tcheck.c`, exhaustive, long double with the tilt solved to 90 bisection steps, a
failure declared when the relative slack is below 1e-12): (TC) holds at every window position of
every tree with 6 <= n <= 25 (445,510,527 window positions at n = 25 alone; `logs/tc_summary.log`).
The minimum of n (2p_k - p_{k-1}/lambda_k - lambda_k p_{k+1})/(2p_k) is 1.33 at n = 6, rises to 1.923 at n = 24, 25, and approaches 2; it is attained by stars. The largest
lambda_k needed is 4.29 (n = 7) and about 3 for n >= 14. The Python implementation (`src/tiltconc.py`,
exact tree data, float tilt) agrees with the C program on the counts of window positions and on the
minima for n = 12, 16, 18. The C program's enumeration checksums equal those of `wlc2` (for example
8106175532762750100 at n = 20).

## 2. Darroch's mean–mode relation (DT) and its interlacing form

**Definition.** (DT_k): rho_{k-1} <= lambda_k <= rho_k. Equivalently, since mu is increasing:

- (DT+_k) at the tilt lambda = rho_k, where P(k) = P(k+1), the mean is >= k;
- (DT-_k) at the tilt lambda = rho_{k-1}, where P(k-1) = P(k), the mean is <= k.

**Lemma 2.** (DT_k) implies (TC_k) and p_k^2 >= p_{k-1}p_{k+1}.

*Proof.* At lambda = lambda_k: P(k-1)/P(k) = rho_{k-1}/lambda_k <= 1 and P(k+1)/P(k) = lambda_k/rho_k <= 1,
so P(k) >= max(P(k-1), P(k+1)) >= (P(k-1) + P(k+1))/2. Also rho_{k-1} <= rho_k is LC at k. ∎

So (DT) on the window is an **interlacing** between two increasing sequences: the coefficient
ratios rho_k and the mean-activities lambda_k. For real-rooted polynomials it is Darroch's theorem.
Its natural slack is measured in **mean units**: a distribution symmetric about the tied pair
{k, k+1} has mean exactly k + 1/2, so both slacks s+ = mu(rho_k) - k and s- = k - mu(rho_{k-1}) equal 1/2.

**Evidence** (exact rationals):

| set | min slack min(s+, s-) over the window |
|---|---|
| all trees, 6 <= n <= 16 (`logs/dt_slack.log`) | 0.105 (n = 8, star); 0.165–0.25 for 11 <= n <= 16, no downward trend |
| all forests with >= 2 components, n <= 13, 4,393 forests (`logs/dt_forests.log`) | 0.157 |
| 150 products of two or three of the 308 non-LC trees (n = 52..93) | 0.244 |
| 248 unions (non-LC tree) + m K1 or m K2, m <= 30 | 0.236 |
| structured families and adversarial local search, 30 <= n <= 80 (`logs/dt_search.log`) | 0.202 (families; hubs(2,3), n = 9); 0.234 (local search, best at n = 35, exact) |

So (DT) holds everywhere tested with an **order-one** margin in mean units; the margin does not
shrink with n. By contrast the LC margin is about 3.4/n.

**Asymptotic meaning.** In the Gaussian regime (Edgeworth to first order) the mode of P_lambda lies at
mu - kappa_3/(2 kappa_2) + O(1/kappa_2). At the tie tilt the continuous mode is k + 1/2, so the
tie-point mean is k + 1/2 + kappa_3/(2 kappa_2) + O(1/kappa_2). (DT+) and (DT-) then say essentially
-kappa_2 < kappa_3 < kappa_2 at the relevant activity, which is Section 3.

**Mediant structure and a refuted sufficient condition.** For a vertex split p = A + xC:

- rho_k(p) = (A_k + C_{k-1})/(A_{k+1} + C_k) lies between rho_k(A) and rho_{k-1}(C) (mediant);
- lambda_k(p) lies between lambda_k(A) and lambda_{k-1}(C), because
  mu_p(lambda) = w mu_A(lambda) + (1-w)(1 + mu_C(lambda)) with both summands increasing.

Hence (DT_k) for p follows from a *joint interlacing* (JDT_k) of the family {A, xC}, the analogue of
a common interlacer:

    max(rho_{k-1}(A), rho_{k-2}(C)) <= min(lambda_k(A), lambda_{k-1}(C)),
    max(lambda_k(A), lambda_{k-1}(C)) <= min(rho_k(A), rho_{k-1}(C)).

`src/jdt.py` tests whether every tree has a vertex satisfying (JDT_k) for all window k. **It does
not.** It fails for every tree with n = 4, 5, and for 1,305 of the 3,159 trees with n = 14
(`logs/jdt.log`). The convex-hull bounds lose too much, notably at the window boundary where
lambda_{k-1}(C) degenerates. (DT) itself holds for all these trees, so what fails is this particular
sufficient condition.

## 3. The skewness bound |kappa_3| <= kappa_2

(Phi3): |kappa_3(lambda)| <= kappa_2(lambda), i.e. |d log Var_lambda(X) / d log lambda| <= 1.

- It holds for Bernoulli sums, since kappa_3 = sum p(1-p)(1-2p) and |1 - 2p| <= 1, hence for every
  real-rooted polynomial.
- It is closed under disjoint union: cumulants add, and |sum kappa_3^(i)| <= sum kappa_2^(i).
- **Evidence** (`logs/k3k2.log`): for every tree with n <= 16 and every lambda on a grid in
  [e^-4, e^4], |kappa_3|/kappa_2 <= 0.928. For lambda <= 12 the maximum grows slowly, 0.914 -> 0.928 for
  n = 6..16; it tends to 1 only as lambda -> infinity.
- **It fails at large activity for non-LC trees** (`logs/k3k2_nonlc.log`): all 308 non-LC trees with
  n = 26..31 violate it for some lambda >= 164, with a maximum ratio of 1.198. core((8,)^17) violates it
  from lambda = 54.6 and core((10,)^10) reaches ratio 3.08. These activities put the mean at about
  0.9 alpha, far beyond the window (lambda_k <= 4.3). So (Phi3) can only hold on a bounded range of
  activities.
- **It cannot by itself give coefficient log-concavity.** It constrains only the real-lambda profile,
  which does not determine coefficient LC; a two-point-like distribution violates it, which is the
  bimodal mechanism, but no real-lambda inequality excludes an LC failure invisible at real lambda.

**The scale-free form of window log-concavity** (`src/mixture_test.py`, `logs/mixture_test.log`). Over all
trees with 8 <= n <= 16 and all window indices k, the product kappa_2(lambda_k) · (1 - p_{k-1}p_{k+1}/p_k^2) is at
least 0.465 (n = 8), rising to 0.652 at n = 16; a discrete Gaussian gives exactly 1. So the window LC
margin is at least about 0.46 / Var_{lambda_k}(X), and this is the normalisation in which any activity-local
invariant would have to be stated. At fixed lambda the vertex split is a two-component mixture,
P_lambda(F) = w P_lambda(A) + (1-w) P_lambda(xC). By the law of total variance,
kappa_2(F) = w kappa_2(A) + (1-w) kappa_2(xC) + w(1-w) delta^2 with delta = mu(xC) - mu(A). The curvature a
mixture loses, about w(1-w) delta^2 / kappa_2^2, is therefore matched at leading order by the gain
from the pieces' smaller variances.

## 4. Why the available routes do not close 33 <= n < N0

**(a) Analytic (FLNYZ-type).** A proof of (TC) from the Fourier form needs
(i) a uniform decay |phi_lambda(theta)| <= exp(-c n sin^2(theta/2)) for lambda in the window range and
(ii) cumulant bounds kappa_3, kappa_4 = O(n) with explicit constants, for all forests.

- The FLNYZ formalization proves (i) with c = 1/114244.
- `src/charfn.py` measures the true best constant: c_eff = 0.134–0.148 over all trees with
  n = 12..20 (worst: caterpillar-like trees at lambda = 2.6), 0.11–0.29 on hubs, core trees and stars
  up to n = 290 (`logs/charfn.log`). So step (i) is pessimistic by about 10^4.
- Even with c = 0.1 proved, the argument needs the tail ∫_{|theta| > theta_0} to be below the
  main term ~ kappa_2^{-3/2}. That forces theta_0^2 ≈ 150 ln n / n and then Taylor control of
  kappa_4 theta_0^4 ≈ 2·10^4 kappa_4 (ln n)^2 / n^2, i.e. n of order 10^6 for kappa_4 ~ 0.1 n.
- Run `20260924T083841Z` showed that root moments grow polynomially (exponent up to 0.94) on nested
  hub trees, so uniform O(n) higher-cumulant bounds are themselves not available.

Realistic analytic thresholds are therefore >= 10^6, against a computational frontier of 32 (Section 5).

**(b) Exhaustive computation.** The number of free trees grows like 2.955^n: 1.1·10^11 trees at
n = 32 take about 5 hours on 4 cores, n = 33 would take about 15 hours, and each further order about
2.95 times longer. The range up to 10^6 is out of reach by any margin.

**(c) Structural induction.** Every inductive scheme tried in this project (vertex splitting with LC
margins, colour-mass criteria, mode alignment, pendant-leaf reduction, joint Darroch interlacing)
reduces the problem to a local quantitative statement at scale O(1/n) near the mode or the window
boundary: (Q1)–(Q3) of run `20260924T175223Z`, the gap-zone bound of run `20260924T072235Z`, or
(JDT). None is implied by the shape information that such an induction carries. The order-one
margins of (DT) and (TC) found here suggest that the right inductive quantity lives in mean/activity
units rather than in coefficient units. The mediant/convex-combination structure is exact, but its
naive use (JDT) is refuted.

**What would close the problem.** One of:

1. a uniform, explicit near-mode Gaussianity theorem for independent sets in forests, valid down to
   n = 33 (far beyond current technique; see (a));
2. a *closed* invariant: a property of polynomials, or of rooted pairs (I(T - r), I(T - N[r])), that
   holds for a single vertex, is preserved by the rooted-tree recursion g = prod f_i, h = prod g_i
   (products included), and implies (DT) or (TC) on the window. The natural candidates found here are
   activity-local: statements about P_lambda for lambda in a bounded range. Products act pointwise in
   lambda, as convolution of P_lambda's, and the vertex sum acts as a two-component mixture at fixed
   lambda. At leading order, the law of total variance makes the variance gain of the pieces balance
   exactly the curvature lost by mixing; whether a non-asymptotic version with explicit third- and
   fourth-cumulant control closes is the open question this run identifies.

## 5. Computational frontier: trees of order 32 and forests of order 32

**Forests of order 32 with a non-LC component** (`src/forest_nonlc32.py`, `logs/forest_nonlc_N32.log`).
A non-LC component has order >= 26, so it is one non-LC tree T of order 26..31 plus a forest of order
<= 32 - |T| <= 6. Every non-LC tree sequence found in run `20260924T092515Z` is multiplied by every
distinct forest polynomial of the remaining order. There are 2·43 + 19·13 + 7·7 + 121·4 + 159·2 = 1,184
pairs. All are unimodal, strictly log-concave on the window, and satisfy the window drift condition.

**Forests of order 32 whose components are all LC.** Every component has order <= 31. By run
`20260924T092515Z`, no tree of order <= 30 has an interior equality p_t^2 = p_{t-1}p_{t+1}, and exactly one
tree of order 31 does, with isolated equalities. That tree can only occur as T + K1. The strict Hoggar
lemma and its isolated-equality remark (same run, Section 5) then give strict LC on [0, alpha].

**Trees of order 32** (`src/cwlc.c`, unchanged from run `20260924T092515Z`; `logs/cwlc_n32.log`,
18,915 s on 4 cores, exit 0):

- 109,972,410,221 trees, equal to OEIS A000055(32); rooted counts equal A000081 up to order 16;
- every tree is unimodal;
- no non-LC index and no LC equality lies in the window, so **strict** window LC holds;
- 922 trees are non-LC, each breaking only at k = alpha - 1 (735 with alpha = 17, 180 with alpha = 18,
  7 with alpha = 19; first break at >= 0.941 alpha). All 922 were rebuilt from their parent arrays and
  re-verified by the Python DP (`logs/reverify_n32.log`, 0 problems);
- no tree of order 32 has any interior LC equality;
- the drift condition m_{r+1} <= m_r + 1 holds at every r for every tree, with maximum window drift
  -0.814;
- min n (1 - p_{k-1}p_{k+1}/p_k^2) over the window is 3.765; the mode/n minimum is 0.281 and the
  mode/alpha maximum is 0.688.

**Theorem (computer-assisted).** Every forest of order n <= 32 satisfies strict log-concavity on
[ceil(n/4), ceil((2alpha-1)/3)] and is unimodal.

*Proof.* Trees: the exhaustive runs for n <= 31 (run `20260924T092515Z`) and n = 32 above; trees with
n <= 3 by inspection. Forests of order <= 31: Theorem 6 of run `20260924T092515Z`. Forests of order 32
with at least two components are covered by the two paragraphs above. ∎

So the Lean proposition `WindowLC` holds for every forest on Fin n with n <= 32, and the open range of
`erdos993_of_windowLC_below` is **33 <= n < N0**.

## 6. Boundaries

- ORIGINAL=NOT_CLOSED. No Lean was run. Lemmas 1 and 2 and the mediant statements are elementary and
  proved above. (TC), (DT) and (Phi3) are empirical.
- Floating point is used in `tcheck.c` (long double tilt solving; failures would be reported below a
  1e-12 relative slack, while the observed slacks are > 0.05) and in `charfn.py`, `k3k2*.py`, `jdt.py`
  and `dt_search.py`. `dt_slack.py`, `dt_forests.py` and the exact re-evaluation in `dt_search.py` use
  exact rationals.
- Novelty is not claimed. Darroch's theorem and tilt invariance are classical; the reformulations
  are recorded because of their order-one margins.
