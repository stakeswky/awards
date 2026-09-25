# Attempt on the remaining gaps G1, G2, G3 (independent Claude window)

**Outcome: ORIGINAL=NOT_CLOSED.** The core gap G1 is **not** proved. This note records:

- what is rigorously proved: reductions, sharp lemmas and a new tail bound;
- which natural routes provably cannot work;
- the exact computational evidence;
- the single inequality family that remains open.

Notation is as in the earlier `STATEMENT.md`: p_k counts independent k-sets, n is the order,
alpha the independence number, and History(F,j-1) means a strict descent at some i <= j-1 with no
rise from i to j. We write a=p_j, b=p_{j-1}, c=p_{j+1}.

## 0. The gaps being attacked

- **G1 (core).** For forests of moderate order, show that no rise follows a descent in the
  window between the prefix bound ceil(n/4) and the tail bound.
- **G2 (plateau).** The case a=b after an earlier strict descent, where the colour-mass
  criterion has zero slack.
- **G3 (forests).** Products of several tree sequences.

## 1. Proved results

### Theorem 1 (reduction of the whole problem to window log-concavity)

Let F be a forest with n>=2. Suppose that for every k with ceil(n/4) <= k <= ceil((2 alpha-1)/3),

    (W)   p_k^2 >= p_{k-1} p_{k+1}.

Then p(F) is unimodal.

*Proof.* The following are machine-checked for **every** forest in the external Lean
development (fresh build of `b2a1d3e`, run `20260923T074907Z_external_flnyz_lean_build`):

- `monotoneOn_icoeff_prefix`: p is nondecreasing on [0, ceil(n/4)];
- `antitoneOn_icoeff_tail`: p is nonincreasing on [ceil((2 alpha-1)/3), alpha].

If ceil(n/4) >= ceil((2 alpha-1)/3), unimodality is immediate. Otherwise all p_k are positive on
the window, so by (W) the ratios p_{k+1}/p_k are nonincreasing across it. The prefix gives ratio
>= 1 at its left end. Hence p rises until the ratio first drops below 1, then falls through the
window, and the tail lemma continues the fall.

The Lean lemma `isUnimodal_of_central_logConcave` (Main.lean) formalizes the same assembly with
*strict* LC. For n >= N0, (W) is exactly covered by the formal `central` (strict LC on
n/5 <= k <= 64 alpha/95, which contains the window). ∎

**Formalized (this run).** `lean/WindowReduction.lean` defines `WindowLC G`, strict LC on
[(n+3)/4, (2 alpha+1)/3]. On top of the external development at `b2a1d3e` it proves:

- `isUnimodal_of_windowLC`: every forest satisfying `WindowLC` is unimodal, at every order;
- `erdos993_of_windowLC`: `WindowLC` for all forests implies Erdős #993 for all forests;
- `erdos993_of_windowLC_below`: there is N0 such that `WindowLC` for all forests of order < N0
  implies Erdős #993 for all forests.

`lake build ErdosProblem993.WindowReduction` exits 0, and `#print axioms` gives only
`propext`, `Classical.choice`, `Quot.sound` for all three. The whole remaining problem is
therefore the single formal proposition `WindowLC` below N0.

**Consequences.**

- **Trees with n <= 25.** They are log-concave, so (W) holds for them. This is reported in the
  literature (Kadrawi–Levit, arXiv:2305.01784) and re-checked exhaustively by this run; see the
  table in §3.
- **Plateaus (G2).** Under (W) a plateau after a strict descent cannot occur inside the window,
  because the ratios are nonincreasing. So G2 is subsumed by (W).
- **What remains.** Everything reduces to (W) for 26 <= n < N0. For trees this is the
  all-orders analogue of FLNYZ Theorem 1.2 restricted to the window.

### Theorem 2 (anchor lemma; handles G2 inside any payment scheme)

Let G be any graph and j>=1. Let i <= j-1 with p_i >= p_{i+1}, and fix any grading of pairs. Put

    N_t = #{(I,J) in I_i x I_{j+1} of class t},
    P_t = #{(I',J') in I_{i+1} x I_j of class t},
    D_i = sum_t max(N_t - P_t, 0).

If D_i <= p_j (p_i - p_{i+1}), then p_{j+1} <= p_j.

*Proof.* p_i p_{j+1} - p_{i+1} p_j = sum_t (N_t - P_t) <= D_i <= p_j(p_i - p_{i+1}). Hence
p_i p_{j+1} <= p_i p_j, and p_i > 0. ∎

At a plateau, take i to be the last strict descent; the slack p_j(p_i - p_{i+1}) is then strictly
positive. With i=j-1 the lemma is exactly the colour-mass entrance (D\*).

### Theorem 3 (forest reduction for G3)

Let F = T_1 ⊔ ... ⊔ T_c. If all but at most one component have log-concave sequences, and the
remaining component is unimodal, then F is unimodal.

*Proof.* Two classical facts suffice:

- products of log-concave polynomials with nonnegative coefficients and no internal zeros are
  log-concave (Hoggar 1974);
- log-concave sequences are exactly the strongly unimodal ones, i.e. their convolution with
  any unimodal sequence is unimodal (Keilson–Gerber 1971, the discrete form of Ibragimov's
  theorem). ∎

Since all trees with n <= 25 are log-concave, **G3 is open only for forests with at least two
non-log-concave components, hence with at least 52 vertices.** Forests of order >= N0 are covered
by FLNYZ.

### Theorem 4 (population representation; closure under disjoint union)

For a bipartite graph with sides (L,R), write k_S = |L \ N(S)|. Then

    Z(x,y) = sum_{S subset R} y^{|S|} (1+x)^{k_S},     p_r = sum_S C(k_S, r-|S|).

Here x marks L-vertices and y marks R-vertices. For a disjoint union with R = R_1 ⊔ R_2 we have
k_{S_1 ⊔ S_2} = k_{S_1} + k_{S_2}. So the population distribution g(m,k) = #{S : |S|=m, k_S=k}
of a forest is the convolution of the components' distributions (Vandermonde), and the
colour-mass class of a pair is determined by the total R-count m_1+m_2.

**Consequence.** Any proof of D\* that uses only a convolution-closed property of g covers
forests automatically.

### Theorem 5 (turned populations imply D\*; sharp)

Let p = sum_s pi_s, where each pi_s is nonnegative and log-concave with no internal zeros. Put
x_s=pi_s(j-1), y_s=pi_s(j), z_s=pi_s(j+1), and assume:

- y_s <= x_s for every s;
- no population starts after j-1, i.e. x_s = 0 implies z_s = 0.

Take any grading in which every pair drawn from populations (s,s') lies in the same class as its
reversal (s',s) and as the target pairs drawn from (s,s'); the colour mass with binomial
populations S subset R has this property. Then

    Dmass_j <= sum over unordered pairs of max(Delta,0) <= a(b-a) = S.

*Proof.* Self-pairs contribute xz - y^2 <= 0 by log-concavity.

For s != s', let Delta = x_1 z_2 + x_2 z_1 - 2 y_1 y_2, and let the pair's share of the slack be
y_1(x_2-y_2) + y_2(x_1-y_1) >= 0.

- If y_1 = 0, then z_1 = 0, so Delta = x_1 z_2 <= x_1 y_2, which is the share.
- Otherwise set rho_i = y_i/x_i in (0,1]. Log-concavity gives z_i <= y_i rho_i, so
  Delta <= y_1 y_2 (rho_1/rho_2 + rho_2/rho_1 - 2). The share minus this bound equals
  y_1 y_2 [rho_1(1-rho_1) + rho_2(1-rho_2)]/(rho_1 rho_2) >= 0.

Summing over unordered pairs (subadditivity of the positive part within each class) and adding
the unused self-shares y(x-y) >= 0 gives at most sum_{s,s'} y_s(x_{s'} - y_{s'}) = a(b-a). ∎

**Sharpness.** For hubs(2,l) at j=l+1 with R = hubs, all populations are turned. The bound is
attained asymptotically: Lemma 2 of run `20260923T063246Z` gives
Dmass/S = A(l^2-2l-4)/((A+2)(l^2+l-2)) -> 1.

### Theorem 6 (population tail bound)

For a bipartite graph and either side R, put mu*(R) = max_{S subset R} (|S| + (k_S - 1)/2).
Then p_{r+1} <= p_r for every r >= mu*(R).

*Proof.* Since mu* >= |R| - 1/2, every population has started when r >= mu*. For each S we have
r - |S| >= (k_S-1)/2, which is exactly where the binomial C(k_S, .) is nonincreasing. ∎

**Corollary 6'.** Let F be a forest in which every vertex of one colour class R has degree >= 3.
Then p is nonincreasing from ceil((|L|-1)/2).

*Proof.* In the sub-forest on S ∪ N(S), 3|S| <= e(S,N(S)) <= |S| + |N(S)| - 1, so
|N(S)| >= 2|S| + 1 for S nonempty. Hence mu* = (|L|-1)/2. ∎

For this class the bound is at least as good as Levit–Mandrescu's ceil((2 alpha-1)/3), since
alpha >= |L|, and strictly better once |L| >= 3. Numerically (all trees with n=18), the best side improves Basit–Galvin's beta for
4,989 trees and Levit–Mandrescu's bound for 16,074 trees. Novelty is not claimed.

## 2. Routes that provably or empirically fail

1. **Colour-class population inequalities.** The sufficient condition (S1), sum w tau^2 <= sum w tau
   (w = population mass at j-1, tau = relative descent), implies c <= a by log-concavity. With
   colour-class populations it fails in about 91% of middle-range positions at n=18 (holds in
   1,021 of 11,866). Almost every failure has, on both sides, populations whose support **starts
   inside the window** (|S| = j). Any population argument must therefore use a decomposition with
   no births in the window, e.g. conditioning on a small separator.
2. **Pairwise positive parts.** Bounding Dmass by pairwise positive parts is too weak (the
   project's D_fine exceeds S on F14 and F61). Cancellation inside a mass class is essential.
3. **Turned populations only.** In the middle range, a side with all populations turned exists
   for only 0–8% of positions (n<=18; 8.1% at n=16, 4.5% at n=18). Rising populations carry up to about 60% of the mass at j.
4. **Why (W) is not local.** For mixtures of many populations, the curvature of each single
   population is negligible against cross terms. So (W) is a global property; its large-n proof
   (FLNYZ) is a central limit theorem. A proof for moderate n needs a global or structural input
   that has not been found.

## 3. Computational evidence (exact integers; new independent implementation)

| Statement | Coverage | Result |
|---|---|---|
| Theorem 2 at every anchor (i <= j-1, strict descent at i, no rise from i to j), colour-mass grading | all trees n<=19: 9,137,760 anchor pairs (n=19 alone 5,949,964) | 0 failures; maximum ratio at i=j-1, attained by hubs(2,l) |
| D\* for two-component forests, **every** relative colouring | all 26,432 forests with total order <= 16 (122,145 History positions) | 0 failures, even for the worst colouring (max 0.5 overall, 0.0037 in the middle range) |
| D\* for three-component forests, all 4 colourings | balanced sample, order <= 13 | 0 failures |
| (W) on structured non-log-concave trees | 95,319 core/hub trees (n<=130), of which 4,497 are non-LC | no non-LC position inside [ceil(n/4), beta] or [ceil(n/4), ceil((2 alpha-1)/3)]; every first non-LC index is >= 0.875 alpha |
| (W) exhaustively (Python for n<=24, C for 21<=n<=29; C and Python agree bit for bit on every coefficient checksum for n in {5,10,14,16,18,20}) | **all** free trees with 4 <= n <= 29 (see table below) | every tree unimodal; no non-LC position inside the window at any order |
| Strict (W), the form required by `WindowLC` | all trees with 5 <= n <= 29 (C variant `wlc2`) | 0 equalities p_k^2 = p_{k-1}p_{k+1} inside the window across all 25 orders, so strict (W) holds for every tree with n <= 29 |
| Forests of order <= 29 with a non-LC component (one non-LC tree of order 26–29 plus any forest of order <= 29-|T|) | all 59 such forests | strict (W) and unimodality hold. Forests with only LC components are LC by Hoggar, so (W) holds non-strictly for **every forest of order <= 29**; strictness for all-LC forests needs the standard strict-product lemma, not re-verified here |
| (W) for forests with non-LC components | 26,520 forests: 535 non-LC core trees (n<=70) times up to 6 copies of K1/K2/P3/K_{1,3}/P4/K_{1,5}, plus 7,260 products of two non-LC trees | 0 strict window failures |
| Plateaus after a strict descent | all tested sets | none occur |

**Exhaustive tree table** (C for n >= 21, cross-checked against Python; counts equal OEIS A000055):

| n | trees | non-LC trees | smallest first non-LC index / alpha | non-LC index in window | non-unimodal |
|---|---|---|---|---|---|
| 4–25 | 167,879,143 in total | 0 | – | 0 | 0 |
| 26 | 279,793,450 | 2 (the Kadrawi–Levit trees; tails ...,18683,2979,51,1 and ...,15498,2372,48,1) | 0.9286 | 0 | 0 |
| 27 | 751,065,460 | 0 | – | 0 | 0 |
| 28 | 2,023,443,032 | 19 | 0.9333 | 0 | 0 |
| 29 | 5,469,566,585 | 7 | 0.9375 | 0 | 0 |

Including the three trees with n <= 3, the total is 8,691,747,673, exactly Reynolds' count for
n <= 29. This run independently reproduces his unimodality verification and adds the
log-concavity map: every log-concavity break in a tree with <= 29 vertices lies at
>= 0.9286 alpha.

## 3b. Literature context (web-search sub-agent report; items marked * were read first-hand earlier)

- **Theorem 4 is not new.** FLNYZ* use the same population representation (conditioning on the
  R-part; Lemma 6.1 bounds the characteristic function). The sub-agent found no tree result
  bounding the peaks of individual populations, so Theorem 6 may be new; novelty is not claimed.
- **Theorem 3 is classical.** It rests on Hoggar and Keilson–Gerber, and its use for forests
  whose components are small except one has been noted on the erdosproblems forum. An
  unrefereed forum experiment reports 253,695 forests built from extreme non-LC trees
  (<= 60 vertices), all unimodal.
- **(W\*) matches Galvin's Question 3.1** (arXiv:2502.10654). Galvin notes that producing a
  non-unimodal tree by his mechanism would need log-concavity breaks at (1-c) alpha with c > 1/3,
  i.e. inside the window, and asks whether this can happen. (W\*) conjectures that it cannot. The
  exhaustive data of §3 is direct evidence for all trees n<=29: every break index is >= 0.9286 alpha.
- **Where known breaks sit.** Kadrawi–Levit, Bautista-Ramos and Ramos–Sun report breaks within a
  few indices of alpha. Galvin's families break near alpha(1 - 1/(16 log alpha)). All are far
  outside the window.
- **A possibly useful tool.** Synchronised sequences (Gross–Mansour–Tucker–Wang,
  arXiv:1407.6325): pairwise synchronised LC populations give an LC mixture. Colour-class
  populations are not pairwise synchronised in the window (see §2), so any use needs a different
  decomposition.

## 4. What remains open, stated exactly

**(W\*) Window log-concavity.** For every forest F with 30 <= n < N0 and every
ceil(n/4) <= k <= ceil((2 alpha-1)/3): p_k^2 >= p_{k-1} p_{k+1}. Orders n <= 29 are settled
computationally (§3). The strict version is exactly the Lean proposition `WindowLC`, and plugs into
`erdos993_of_windowLC_below`.

**Minimal mathematical form.** By Theorem 3, (W\*) is needed only for:

- **(W\*_tree):** trees with 30 <= n < N0;
- **(F\*):** forests with at least two non-log-concave components (>= 52 vertices) below N0,
  for which one can also target unimodality of the product directly.

Forests with at most one non-LC component follow from (W\*_tree) through Keilson–Gerber.
Plateaus (G2) are subsumed, since (W) excludes a plateau after a strict descent inside the window.

**Weaker sufficient forms.** "No rise after descent in the window" also suffices. Among its
sufficient forms:

- D\* (anchor i=j-1) and its anchored version (Theorem 2) are strongly supported numerically;
- (S1) with colour-class populations is refuted as a general tool (§2).

**Status.** No proof of (W\*_tree), (F\*) or D\* for general trees is known to this run. Settled
here:

- orders n <= 29 (exhaustive trees plus the forest argument);
- the reduction of everything else to the single formal proposition `WindowLC` below N0
  (Lean, three standard axioms only).

(W\*_tree) is the negative answer to Galvin's Question 3.1 restricted to the window. Current
evidence: all 8.69 billion trees with n <= 29, and 95,319 structured trees up to n=130 (4,497 of
them non-LC). Every log-concavity break found lies at >= 0.875 alpha, far to the right of the
window end, which is about 2 alpha/3.
