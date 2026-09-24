# Open window, drift form of the window condition, strict products, and exhaustive trees through n = 31

Independent Claude window, 2026-09-24. It continues runs `20260923T153415Z`, `20260924T011530Z`,
`20260924T072235Z`, `20260924T083841Z` and `20260924T084900Z`.

**ORIGINAL=NOT_CLOSED.** Erdős #993 is neither proved nor refuted here.

The status before this run:

- Erdős #993 reduces formally (Lean, three standard axioms) to `WindowLC` for forests of order
  below an existential, astronomically large N0.
- Strict `WindowLC` had been checked for every tree with n <= 30.
- For forests, only the non-strict window condition had been checked. The strict version was
  recorded as depending on "the standard strict-product lemma, not re-verified here".

This run contributes:

- written proofs that the reduction needs less than `WindowLC` (Sections 1–2);
- an exact refutation of the natural global drift strengthening, together with evidence for its
  window form (Section 3);
- a second, independent exhaustive algorithm that extends the tree verification to n = 31
  (Section 4);
- a strict form of Hoggar's product theorem (Section 5);
- the resulting theorem that every forest of order <= 31 satisfies strict `WindowLC` and is unimodal
  (Section 6).

## 1. What the reduction actually needs: the open window

Notation: F is a forest of order n, p_k = i_k(F), alpha = alpha(F), q = ceil(n/4) = (n+3) div 4,
top = ceil((2 alpha - 1)/3) = (2 alpha + 1) div 3. Two facts are machine-checked for every forest in
the external development (audited in run `20260923T074907Z`):

- (P) `monotoneOn_icoeff_prefix`: p_k <= p_{k+1} for 0 <= k < q;
- (T) `antitoneOn_icoeff_tail`: p_k >= p_{k+1} for top <= k < alpha.

All p_k with 0 <= k <= alpha are positive.

**Lemma 1 (open window).** Let p_0, ..., p_alpha be positive and satisfy (P) and (T). If p is not
unimodal, then there is r with q <= r <= top - 2 such that p_{r+1} <= p_r and p_{r+2} > p_{r+1}.
Consequently each of the following suffices for unimodality:

- (a) **non-strict** log-concavity p_k^2 >= p_{k-1} p_{k+1} only for q+1 <= k <= top-1;
- (b) for every q <= r <= top-2: if p_{r+1} <= p_r, then
  M1_r: (r+2) p_r p_{r+2} <= (r+1) p_{r+1}^2 + p_r p_{r+1}.

*Proof.* If p is not unimodal there are i < j with p_i > p_{i+1} and p_j < p_{j+1}. Take the
smallest such j above i. Then p_t >= p_{t+1} for i <= t < j, so r = j-1 satisfies r >= i,
p_{r+1} <= p_r and p_{r+2} > p_{r+1}. By (P), i >= q, so r >= q. By (T), j < top, so r <= top-2.

(a) LC at k = r+1 and p_{r+1} <= p_r give p_{r+2} p_r <= p_{r+1}^2 <= p_{r+1} p_r, hence
p_{r+2} <= p_{r+1}, which is a contradiction.

(b) Write m_r = (r+1) p_{r+1}/p_r. Then p_{r+1} <= p_r iff m_r <= r+1, and M1_r says
m_{r+1} <= m_r + 1. Hence m_{r+1} <= r+2, i.e. p_{r+2} <= p_{r+1}. This is a contradiction. ∎

The formal proposition `WindowLC` (strict LC on the closed window [q, top]) therefore asks for
more than is used. Two indices can be dropped, and strictness can be dropped. Condition (b) is
weaker still (Section 2). None of this is formalized in this run, because Lean could not be run
here (Section 7).

## 2. The drift form of the condition

For an independent set J let N(J) be its open neighbourhood and e(J) = n - |J| - |N(J)| its number
of addable vertices. Let E_r denote the uniform average over independent r-sets. Then
m_r = E_r e(J), by double counting pairs (J, v).

**Lemma 2 (drift identity).** For every graph and 0 <= r <= alpha - 2, put d_r = m_{r+1} - m_r. Then

    d_r = E_r|N(J)| - E_{r+1}|N(J)| - 1 = Var_r(e)/m_r - 1 - D_{r+1},

where D_{r+1} is the extension-pair average of |N(v) ∩ Ext(J)| from run `20260924T011530Z`.

*Proof.* The first form holds because m_r = n - r - E_r|N(J)|, since N[J] = J ⊔ N(J) for an
independent J. The second form is the extension identity of run `20260924T011530Z`. ∎

**Consequences.**

- M1_r is equivalent to E_r|N(J)| - E_{r+1}|N(J)| <= 2. In words: a uniformly random independent
  (r+1)-set has, on average, a neighbourhood at most two smaller than a random r-set.
- M1_r is also equivalent to Var_r(e) <= (2 + D_{r+1}) m_r, an index-of-dispersion bound of 2 for
  the addable-vertex count. The under-dispersion condition UD of run `20260924T011530Z` asks for 1.
- LC_{r+1} (p_{r+1}^2 >= p_r p_{r+2}) is equivalent to d_r <= m_r/(r+1).
  - After a descent (m_r <= r+1), LC_{r+1} implies M1_r. So (b) of Lemma 1 is implied by (a).
  - The implication is strict wherever m_r < r+1, that is, to the right of the mode.
  - Before the mode, M1_r is stronger than LC; this is why (b) is stated only after a descent.
- Heuristically, if the sequence is locally Gaussian with the hard-core activity lambda whose mean is
  r, then d_r ≈ (1 - mu_lambda / sigma_lambda^2)/lambda. The drift is negative exactly when |I| is
  under-dispersed at that activity. This is not used anywhere.

## 3. The drift condition cannot hold everywhere; on the window it holds with a large margin

**Proposition 3 (certificate).** The tree core((8,)^17) is a centre joined to 17 hubs, each hub
carrying 8 pendant paths of length two. It has n = 290 and alpha = 153 and is unimodal, with mode 91.
M1 fails at r = 137, with m_138 - m_137 = 1.2184 > 1 (exact rational in
`results/m1_certificate.json`). The window range for (b) is [73, 100]. The failure sits at
r/alpha = 0.895, far to its right, where m_137 = 0.78 is much smaller than r+1. The neighbours
core((8,)^16), core((8,)^18) and core((8,)^20) fail in the same way, at r/alpha ≈ 0.895.

So "m_{r+1} <= m_r + 1 for all r" is **false** for trees. The mechanism is the two-population
crossover in the far tail, the same mechanism that breaks log-concavity there. Any drift-type
hypothesis must be restricted to the window, as in Lemma 1(b); in the tail, (T) does the work.

**Evidence on the window** (exact coefficients; the drift itself is reported in floating point):

| set | coverage | max window drift max_{q<=r<=top-2} (m_{r+1}-m_r) | failures of (b) |
|---|---|---|---|
| all trees (exhaustive, Section 4) | 4 <= n <= 31 (window empty for n <= 6) | -0.762 (n = 8) | 0 |
| hubs(t,l), spiders, R(s,m), k-ary, caterpillars, core((s,)^k) | 1065 trees, n <= 220 | -0.772 (hubs(2,3), n = 9) | 0 |
| random local search maximising the window drift | 30 <= n <= 90, 400 s | -0.824 | 0 |
| uniform random labelled trees, random recursive trees, spherically symmetric trees | 170 trees, n <= 800 | -0.840 (spherically symmetric, n = 190); random trees <= -1.147 | 0 |
| forests: products of 2 to 4 trees from hubs(t,l), K1, K2, P3, K_{1,3}, plus 300 products of two non-LC trees with one small tree | 2,578 forests | -0.804 | 0 |
| all 149 non-LC trees with n = 26..30 (sequences from the earlier runs) | — | -1.685 | 0 |

In every tested tree and forest the window drift is not only <= 1 but **negative**, at most
-0.762. So m_r decreases strictly across the window, which is a strictly stronger property than window
log-concavity (d_r <= 0 < m_r/(r+1)). This suggests a scale-free quantitative form, stated here
as a conjecture only:

**(DG) Window drift gap.** There is an absolute c > 0 (the data suggest c ≈ 0.76) such that
m_{r+1} - m_r <= -c for every forest and every ceil(n/4) <= r <= ceil((2alpha-1)/3) - 2.

(DG) implies strict log-concavity on the open window, hence unimodality by Lemma 1. Unlike the
normalised LC margin, which is of order 1/n, the gap in (DG) is of order one. In the local-CLT
regime, (DG) corresponds to mu_lambda - sigma_lambda^2 >= c lambda sigma_lambda^2 at the
activities lambda that sweep the window (Section 2 heuristic). That is an under-dispersion
statement for |I| under the hard-core measure at moderate activity. No proof is claimed.

## 4. Exhaustive trees through n = 31 with a second algorithm

**Algorithm (`src/cwlc.c`).** By Jordan's theorem a free tree has one centroid or two adjacent
centroids.

- **Rooted trees.** Every rooted tree tau of order <= n/2 is generated once, as a root plus a
  multiset of smaller rooted trees; indices are sorted by order. Each tau is stored with
  f = I(tau) and g = I(tau - root).
- **One centroid.** Free trees of order n with one centroid are exactly the multisets of rooted
  trees of order <= (n-1)/2 with total order n-1. Here I = prod f_c + x prod g_c.
- **Two centroids** (n even). These are the unordered pairs of rooted trees of order n/2, joined
  at their roots. Here I = f_1 f_2 - (f_1 - g_1)(f_2 - g_2).
- **Execution.** The multisets are walked depth-first with incremental partial products, under
  OpenMP dynamic scheduling.

All pass/fail tests use exact 64/128-bit integers; coefficients are below 2^n. Floating point is
used only for the reported extremal statistics. The program shares no code with the WROM checkers
of the earlier runs.

**Cross-validation.**

- Free-tree counts equal A000055 for every n <= 31, and rooted counts equal A000081.
- The order-independent checksum sum_k p_k (k+1) 0x9E3779B97F4A7C15 mod 2^64 is the one used by
  `wlc.c`/`wlc2.c`. It is identical to `wlc2` (WROM) for every n = 4..27.
- The multiset of independence sequences of the non-LC trees is identical to the earlier runs for
  every n = 26..30 (`results/crosscheck_nonlc.json`).
- Every printed example tree is rebuilt from its parent array and recomputed by the Python DP
  (`results/reverified_examples.json`).

| n | trees (= A000055) | non-LC | min first non-LC / alpha | window LC failures / equalities | trees with an interior LC equality | drift condition failures (any r / window) | max window drift | min n * LC margin on window | min mode/n | max mode/alpha | checksum = wlc2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 2 | 0 | – | 0 / 0 | 0 | 0 / 0 | – | 2.222 | 0.250 | 0.500 | yes |
| 5 | 3 | 0 | – | 0 / 0 | 0 | 0 / 0 | – | 2.222 | 0.400 | 0.667 | yes |
| 6 | 6 | 0 | – | 0 / 0 | 0 | 0 / 0 | – | 2.400 | 0.333 | 0.667 | yes |
| 7 | 11 | 0 | – | 0 / 0 | 0 | 0 / 0 | -1.0000 | 2.644 | 0.286 | 0.600 | yes |
| 8 | 23 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.7619 | 2.921 | 0.250 | 0.750 | yes |
| 9 | 47 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.7719 | 3.240 | 0.333 | 0.600 | yes |
| 10 | 106 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8154 | 3.333 | 0.300 | 0.667 | yes |
| 11 | 235 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8072 | 3.361 | 0.273 | 0.667 | yes |
| 12 | 551 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8129 | 3.429 | 0.333 | 0.667 | yes |
| 13 | 1,301 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.7837 | 3.449 | 0.308 | 0.625 | yes |
| 14 | 3,159 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.7980 | 3.500 | 0.286 | 0.714 | yes |
| 15 | 7,741 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8281 | 3.516 | 0.267 | 0.625 | yes |
| 16 | 19,320 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8102 | 3.556 | 0.312 | 0.667 | yes |
| 17 | 48,629 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8022 | 3.568 | 0.294 | 0.667 | yes |
| 18 | 123,867 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8152 | 3.600 | 0.278 | 0.667 | yes |
| 19 | 317,955 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8381 | 3.610 | 0.263 | 0.636 | yes |
| 20 | 823,065 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8131 | 3.636 | 0.300 | 0.700 | yes |
| 21 | 2,144,505 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8086 | 3.645 | 0.286 | 0.636 | yes |
| 22 | 5,623,756 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8193 | 3.667 | 0.273 | 0.667 | yes |
| 23 | 14,828,074 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8143 | 3.674 | 0.304 | 0.667 | yes |
| 24 | 39,299,897 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8141 | 3.692 | 0.292 | 0.667 | yes |
| 25 | 104,636,890 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8115 | 3.698 | 0.280 | 0.643 | yes |
| 26 | 279,793,450 | 2 | 0.9286 | 0 / 0 | 0 | 0 / 0 | -0.8197 | 3.714 | 0.269 | 0.692 | yes |
| 27 | 751,065,460 | 0 | – | 0 / 0 | 0 | 0 / 0 | -0.8206 | 3.719 | 0.296 | 0.643 | yes |
| 28 | 2,023,443,032 | 19 | 0.9333 | 0 / 0 | 0 | 0 / 0 | -0.8145 | 3.733 | 0.286 | 0.667 | not run |
| 29 | 5,469,566,585 | 7 | 0.9375 | 0 / 0 | 0 | 0 / 0 | -0.8124 | 3.738 | 0.276 | 0.667 | not run |
| 30 | 14,830,871,802 | 121 | 0.9375 | 0 / 0 | 0 | 0 / 0 | -0.8193 | 3.750 | 0.300 | 0.667 | not run |
| 31 | 40,330,829,030 | 159 | 0.9412 | 0 / 0 | 1 | 0 / 0 | -0.8224 | 3.754 | 0.290 | 0.647 | not run |

**Column notes.**

- "Window" means [ceil(n/4), ceil((2alpha-1)/3)] for LC and [ceil(n/4), ceil((2alpha-1)/3) - 2] for
  the drift condition; the latter is empty for n <= 6.
- The drift is m_{r+1} - m_r. "Min n * LC margin" is min n (1 - p_{k-1}p_{k+1}/p_k^2) over the
  LC window.
- The mode is the first k with p_k >= p_{k+1}.
- Checksums were compared with `wlc2` (WROM, the unchanged source of run `20260924T011530Z`,
  identical SHA-256) at n = 4..24 in one process and at n = 25..27 in four residue classes. The
  per-order sums are equal everywhere. For n = 28..31 no `wlc2` run was made in this session.

**New at n = 31.**

- All 40,330,829,030 trees are unimodal.
- The strict window condition holds, with no equality anywhere in the window.
- 159 trees are non-LC. Each breaks only at k = alpha - 1, with first break index >= 0.9412 alpha
  (152 with alpha = 17, 7 with alpha = 18).
- The drift condition holds at **every** r for every tree of order <= 31. Its global failure first
  appears in larger trees (Section 3).
- **Exactly one** tree of order 31 has an interior equality p_t^2 = p_{t-1}p_{t+1}.
  - It lies outside the window, and the tree is LC.
  - No tree has two consecutive equalities.
  - No tree of order <= 30 has any interior equality.
  - The checker records only trees with a window equality, so this tree's identity was not
    printed. Printing it needs one more full n = 31 pass (about 1.9 h on 4 cores), which was not
    run. It plays no role in Section 6, and the remark after Lemma 4 covers such isolated
    equalities.

**Scope of the n = 31 result.** It comes from one implementation, `cwlc`. The count equals
A000055(31). The same program reproduces the independent WROM checksums at every order where both
were run. Every non-LC tree of order 31 was re-verified in Python. A second full n = 31 pass by the
WROM code (about 4.7 h on 4 cores) was not run.

## 5. A strict form of Hoggar's product theorem

For a finite sequence a = (a_0, ..., a_m), padded with zeros, put Da_t = a_t^2 - a_{t-1} a_{t+1}.
Call a **strictly LC on its support** if a_t > 0 for 0 <= t <= m and Da_t > 0 for 0 <= t <= m. At
t = 0 and t = m this is automatic.

**Lemma 4.** Let a (length m+1) and b (length l+1) be positive LC sequences with no internal zeros,
and let c = a * b. Then for every k,

    Dc_k >= sum_j Da_{k-j} Db_j.

If a and b are strictly LC on their supports, then so is c.

*Proof.* Let A and B be the Toeplitz matrices A_{i,j} = a_{i-j} and B_{j,h} = b_{j-h}. Then
(AB)_{i,h} = c_{i-h}. By Cauchy–Binet for the rows {k, k+1} and columns {0, 1},

    c_k^2 - c_{k-1} c_{k+1} = sum_{j < j'} [a_{k-j} a_{k+1-j'} - a_{k-j'} a_{k+1-j}] [b_j b_{j'-1} - b_{j-1} b_{j'}].

The sum is finite. With u = k-j' < v = k-j, the first bracket is a_v a_{u+1} - a_u a_{v+1}.

- If a_u = 0 or a_{v+1} = 0, the bracket is >= 0.
- Otherwise u and v+1 lie in [0, m], so every index between them does too. The ratios a_{t+1}/a_t are
  nonincreasing there (LC with no internal zeros), so a_{u+1}/a_u >= a_{v+1}/a_v, and again the
  bracket is >= 0.

The second bracket is the same expression for b with u' = j-1 < v' = j'-1, so it is >= 0 too.
Keeping only the terms with j' = j+1, whose brackets are exactly Da_{k-j} and Db_j, gives the
inequality.

If a and b are strictly LC on their supports and 0 <= k <= m+l, the index set
j in [max(0, k-m), min(l, k)] is nonempty. For such j both factors are positive, so Dc_k > 0. ∎

**Corollary 5.** Suppose every component T of a forest F is strictly LC on its support; this
includes K1 with sequence (1,1). Then p(F) is strictly LC on [0, alpha(F)], so F satisfies the
strict window condition.

**Remark (isolated equalities are harmless).** The proof only needs, for each k, one j in the
index interval with Da_{k-j} Db_j > 0. The indices k-j fill the interval [max(0,k-l), min(m,k)].
This interval contains a boundary index of a unless l < k < m, and then it is [k-l, k]. Hence:

- if b is strictly LC on its support with l >= 1, and Da vanishes on no l+1 consecutive indices of
  [0, m], then c is strictly LC on its support;
- in particular, a factor whose interior equalities are isolated (such as the order-31 tree of
  Section 4) keeps the product strictly LC, provided the other factor is strictly LC on its support
  and has degree >= 1.

**Strictness cannot be dropped.** (1+x+x^2+x^3+x^4)(1+x) = 1 + 2x + 2x^2 + 2x^3 + 2x^4 + x^5 has
Dc_2 = 0. Hoggar's theorem alone therefore does not give the strict `WindowLC` required by
`erdos993_of_windowLC_below` for forests. This is the caveat left open in runs
`20260923T153415Z` and `20260924T011530Z` ("strict-product lemma, not re-verified here"). Lemma 4
closes it, given the exhaustive fact (Section 4) that no tree of order <= 30 has an interior
log-concavity equality.

## 6. Every forest of order <= 31

**Theorem 6** (computer-assisted; conditional on the computations of Sections 4 and 6 being
correct). Every forest F of order n <= 31 satisfies strict log-concavity p_k^2 > p_{k-1} p_{k+1}
at every k in [ceil(n/4), ceil((2alpha-1)/3)]. Every such forest is unimodal. In particular the
Lean proposition `WindowLC` holds for every forest on Fin n with n <= 31.

*Proof.*

- **F is a tree.** For n >= 4 this is the exhaustive run (Section 4): no non-LC index and no
  equality lies in the window, and every tree is unimodal. The trees with n <= 3 are immediate.
- **All components are LC trees** (at least two components). Every component has order <= 30. By
  Section 4, no tree of order 4..30 has an interior equality p_t^2 = p_{t-1} p_{t+1}. The trees of
  order <= 3 are K1 = (1,1), K2 = (1,2) and P3 = (1,3,1), checked by hand. So every LC component is
  strictly LC on its support. Corollary 5 then gives strict LC
  of p(F) on [0, alpha(F)], and unimodality.
- **Some component T is non-LC.** No tree of order <= 25 is non-LC, so |T| >= 26. A second non-LC
  component would force n >= 52, so F = T ⊔ R where every component of R is LC and |R| <= 5.
  `src/forest_nonlc.py` multiplies every non-LC tree sequence of order 26..31 found in Section 4
  by every distinct forest polynomial of order <= 31 - |T|. It checks unimodality, strict window
  LC and the window drift condition exactly. There are 46 + 133 + 28 + 242 + 159 = 608 pairs, for
  non-LC orders 26, 28, 29, 30 and 31 (none at 27); all pass (`results/forest_nonlc_N31.json`). ∎

**Consequence for the formal reduction.** `erdos993_of_windowLC_below` reduces Erdős #993 to
`WindowLC` for forests of order below the existential N0. That proposition now holds for every
order n <= 31, so the open range is 32 <= n < N0. By Lemma 1 the needed hypothesis can moreover be
weakened to non-strict LC on the open window, or to the post-descent drift condition. The
weakening is not formalized here.

## 7. Boundaries and what was not done

- **ORIGINAL=NOT_CLOSED.** There is no proof for n >= 32 below the (astronomical, existential) N0,
  and no counterexample.
- **Lean was not run.** From this container the external repository
  `junwei-lu/Erdos_993_Tree_Independent_Set_Unimodality` returns HTTP 403, and the mathlib cache
  host is unreachable. Lemmas 1, 2 and 4 are written proofs, checked numerically in exact
  arithmetic (`src/lemma_checks.py`: 200,182 adjacent-term inequalities and 1,207 drift identities by
  brute force, with no violations). They are neither formalized nor externally reviewed.
- **Conjecture (DG)** and the drift evidence are empirical. The drift route inherits the same core
  difficulty as WindowLC: an order-one, non-asymptotic regularity statement in the middle of the
  sequence.
- The window-drift local search is time-budgeted and so not bit-for-bit reproducible. Its
  best-found tree is recorded.
- Novelty is not claimed for Lemma 4 (a strict form of a classical total-positivity argument), for
  Lemma 1 or for Lemma 2.
