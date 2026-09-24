# The pendant-leaf statement (S2): reduction to one local inequality, the degree-one case, and the exact remaining hypothesis

Independent Claude window, 2026-09-24. It continues `20260924T143534Z_mode_alignment_route` and
`20260924T150627Z_ma_exhaustive_n26_forests18`.

**ORIGINAL=NOT_CLOSED.** Erdős #993 is neither proved nor refuted here. (S2) is **not** proved
unconditionally. What is proved: a rigorous reduction of (S2) to a single inequality at one index
next to the modes of two smaller forests (Theorem 1), the impossibility of the bad case when the
attachment vertex is a leaf (Lemma 3), and a conditional form of (S2) (Corollary 4). The remaining
hypothesis is stated exactly and its margin is measured on all trees with n <= 19.

## 1. Setting

H is a forest, w a vertex of H, and G = H + u is H with a new leaf u attached at w. Put

    P = I(H),   Q = I(H - w),   Q' = I(H - N_H[w]),

so that P = Q + xQ' and I(G) = P + xQ = (1+x)Q + xQ'. For a unimodal sequence S let
M(S) = [s1, s2] be its mode set (the indices attaining the maximum); S is nondecreasing on [0, s2]
and nonincreasing on [s1, infinity). Write M(P) = [p1, p2], M(Q) = [q1, q2], M(Q') = [r1, r2].

(S2) for the pair (H, w) is the statement that M(P) meets M(G) or ends immediately before it;
equivalently max M(G) >= p1 and min M(G) <= p2 + 1. (S1) for (H, w) is dist(M(Q), M(P)) <= 1,
split into (S1-lower): q2 >= p1 - 1, and (S1-upper): q1 <= p2 + 1.

## 2. The reduction

**Theorem 1.** Assume P, Q, Q' are unimodal.

(a) If q2 >= p1 - 1, then I(G) is nondecreasing on [0, p1].

(b) If q1 <= p2, then I(G) is nonincreasing on [p2 + 1, infinity).

(c) If q1 = p2 + 1 =: m + 1, then I(G) is nonincreasing on [m + 2, infinity), and it is nonincreasing
on [m + 1, infinity) if and only if

    Q_m + Q'_m >= Q_{m+2} + Q'_{m+1}.                                                   (*)

In this case Q'_{m+1} <= Q'_m, so (*) holds whenever Q_m >= Q_{m+2}.

(d) If the hypothesis of (a) holds together with the hypothesis of (b), or with that of (c) and (*),
then I(G) is unimodal, M(I(G)) is contained in [p1, p2 + 1], and (S2) holds for (H, w).

*Proof.* Write G_k for the coefficients of I(G), so G_{k+1} - G_k = (P_{k+1} - P_k) + (Q_k - Q_{k-1}).

(a) For k < p1 we have P_{k+1} >= P_k, and k - 1 < p1 - 1 <= q2 gives Q_k >= Q_{k-1}.

(b) For k >= p2 + 1 we have P_{k+1} <= P_k, and k - 1 >= p2 >= q1 gives Q_k <= Q_{k-1}.

(c) For k >= m + 2, P_{k+1} <= P_k and k - 1 >= m + 1 = q1, so G is nonincreasing there. At k = m + 1,
substituting P = Q + xQ',

    G_{m+2} - G_{m+1} = (P_{m+2} - P_{m+1}) + (Q_{m+1} - Q_m) = (Q_{m+2} - Q_m) + (Q'_{m+1} - Q'_m),

which is <= 0 exactly when (*) holds. Since m = p2 is the last index of the maximum of P,
P_{m+1} < P_m, that is

    Q_{m+1} - Q_m < Q'_{m-1} - Q'_m.                                                     (1)

The left side is positive because q1 = m + 1 is the first index of the maximum of Q. Hence
Q'_{m-1} > Q'_m, so m - 1 >= r2 and Q' is nonincreasing from m - 1 on; in particular Q'_{m+1} <= Q'_m.

(d) Under the hypotheses, G is nondecreasing on [0, p1] and nonincreasing on [p2 + 1, infinity). On
[p1, p2 - 1] the increments of G are G_{k+1} - G_k = Q_k - Q_{k-1}, since P is constant on [p1, p2];
these are nonnegative for k - 1 <= q2 - 1 and nonpositive for k - 1 >= q1, so they change sign at most
once, from + to -. If some increment on [p1, p2 - 1] is negative, then at k = p2 both
P_{p2+1} - P_{p2} < 0 and Q_{p2} - Q_{p2-1} <= 0, so the increment at p2 is negative as well. Hence the
sign pattern of all increments is + ... + - ... -, and G is unimodal. Its maximum over [0, p1] is at
p1 and over [p2 + 1, infinity) at p2 + 1, so M(I(G)) is contained in [p1, p2 + 1]. This interval meets
M(P) = [p1, p2] unless M(I(G)) = {p2 + 1}, which is the "one step to the right" case of (S2). ∎

All four parts were checked exactly on every pair (H, w) with H a tree of order n <= 15
(188,254 pairs; `logs/thm1_check_15.log`): the hypothesis of (a) holds in all of them, that of (b) in
187,436, that of (c) in 818, and the equivalence in (c) holds in all 818. The case q1 >= p2 + 2 never
occurs.

**Lemma 2 (the +1 case is a curvature statement).** In case (c) put

    rise = Q_{m+1} - Q_m,   phi = Q'_{m-1} - Q'_m,   gamma = 2Q_{m+1} - Q_m - Q_{m+2}.

Then (1) says rise < phi, and Q_m >= Q_{m+2} holds if and only if gamma >= 2 rise. Consequently
(*) holds whenever

    gamma >= 2 phi.                                                                     (Q1)

*Proof.* Q_m - Q_{m+2} = (2Q_{m+1} - Q_m - Q_{m+2}) - 2(Q_{m+1} - Q_m) = gamma - 2 rise. ∎

So the +1 case asks that the concavity gap of Q at its own mode be at least twice the fall of the
smaller piece Q' one step earlier.

**Lemma 3 (attachment at a leaf).** Suppose deg_H(w) = 1, with neighbour y, and suppose (S1-lower)
holds for the pair (H - w, y). Then case (c) does not occur.

*Proof.* Here Q' = I((H - w) - y). (S1-lower) for (H - w, y) says r2 >= q1 - 1 = m, so Q' is
nondecreasing on [0, m] and phi = Q'_{m-1} - Q'_m <= 0. This contradicts 0 < rise < phi. ∎

**Corollary 4 (conditional (S2)).** Let N >= 2. Suppose every forest of order < N is unimodal and
satisfies (S1), and suppose (Q1) holds for every pair (H, w) in case (c) with |H| < N and
deg_H(w) >= 2. Then (S2) holds for every forest of order <= N.

*Proof.* Let G = H + u have order <= N, so |H| < N and P, Q, Q' are unimodal. (S1-lower) for (H, w)
gives the hypothesis of (a); (S1-upper) for (H, w) excludes q1 >= p2 + 2, so (b) or (c) applies. In
case (c), Lemma 3 handles deg_H(w) = 1 (using (S1-lower) for (H - w, y)), and (Q1) with Lemma 2
handles deg_H(w) >= 2. Theorem 1(d) concludes. ∎

## 3. What the +1 configurations look like

`src/s2_config.py`, `src/lh_margin.py` and `src/lh_quant.py` list every pair (H, w), H a tree of
order n, in case (c), and evaluate the quantities of Lemma 2 exactly (`logs/`):

| n | pairs in case (c) | deg w = 2 / 3 / 4 / 5 / >= 6 | min (Q_{m+1} - Q_{m+2}) / rise | (Q1) failures | min gamma / (2 phi) | max n rise / Q_{m+1} | max n phi / Q_{m+1} | min n gamma / Q_{m+1} |
|---|---|---|---|---|---|---|---|---|
| 10 | 5 | 0/0/2/3/0 | 7.33 | 0 | 3.13 | 0.51 | 0.68 | 4.04 |
| 11 | 17 | 0/12/5/0/0 | 10.33 | 0 | 3.90 | 0.44 | 0.70 | 4.82 |
| 13 | 119 | 1/30/42/35/11 | 9.25 | 0 | 3.15 | 0.46 | 0.74 | 4.31 |
| 14 | 440 | 0/179/232/29/0 | 7.35 | 0 | 3.38 | 0.68 | 0.84 | 5.04 |
| 15 | 237 | 0/35/106/65/31 | 9.96 | 0 | 4.04 | 0.40 | 0.55 | 4.20 |
| 16 | 1,826 | 8/392/731/479/216 | 7.62 | 0 | 3.65 | 0.56 | 0.68 | 4.59 |
| 17 | 8,011 | 5/2629/3931/1270/176 | 7.65 | 0 | 3.60 | 0.66 | 0.79 | 4.19 |
| 18 | 7,436 | – | 9.12 | 0 | – | – | – | – |
| 19 | 29,987 | – | 8.30 | 0 | – | – | – | – |

(No pair is in case (c) for n <= 9 or n = 12. Columns 6-9 were computed for n <= 17.)

Observations, all exact:

- **Case (c) needs deg w >= 2**, as Lemma 3 predicts; deg w = 2 is rare (14 pairs for n <= 17).
- **The rise into the peak of Q is tiny**: at most 0.68 Q_{m+1}/n. The +1 shift is a near tie
  Q_m ≈ Q_{m+1} broken by the small piece. Typical example (n = 13, deg w = 2): Q = (140, 215, **216**,
  141), Q' = (36, 63, 61, 35), P = (176, **278**, 277, 176) at indices m-1..m+2.
- **The peak of Q is sharp**: gamma >= 4.0 Q_{m+1}/n, and the fall after the peak is at least 7.3
  times the rise. So Q_m >= Q_{m+2} holds in every case, with (Q1) satisfied by a factor >= 3.1
  (tightest for deg w = 3, 4; looser for higher degrees).
- **Q never has a plateau at its peak** in case (c), and Q' is log-concave at m in every case, but Q'
  is concave at m in only 72% of the cases and its fall can stop entirely (fall ratio 0). So neither
  concavity nor "the fall of Q' persists" can replace (Q1).
- **(Q1) is specific to case (c).** Right-heavy peaks (I_{q1-1} < I_{q1+1}) are common for trees in
  general: 62% of all trees at n = 20 and 48% at n = 22 (`logs/rh_peaks.log`). What forces
  Q_m >= Q_{m+2} in case (c) is the near tie: rise < phi and phi is a first difference of the smaller
  piece near its own peak, hence small compared with the curvature of Q.

## 4. The two configurations behind (S1)

The same analysis applies to (S1) for (H, w), with P = Q + xQ' peaking against Q:

- **(S1-lower)** (q2 >= p1 - 1) holds when r1 <= q2, and in the remaining case r1 = q2 + 1 it is
  equivalent to Q_{q2+1} - Q_{q2+2} >= Q'_{q2+1} - Q'_{q2}: the fall of Q one step after its plateau
  must dominate the rise of Q' into its peak. This case occurs for 1,939 of the 188,254 pairs with
  n <= 15; the inequality holds in all of them with ratio >= 6.9; r1 >= q2 + 2 never occurs.      (Q2)
- **(S1-upper)** (q1 <= p2 + 1) holds when r2 >= q1 - 1, and in the remaining case r2 <= q1 - 2 it is
  equivalent to Q_{k+1} - Q_k >= Q'_{k-1} - Q'_k for every k in [r2 + 1, q1 - 2]: the rise of Q at
  least two steps before its peak must dominate the fall of Q'. This case occurs for 11,407 pairs
  (n <= 15); the inequality holds in all, with ratio >= 9.                                          (Q3)

So (S1), (S2) and hence the leaf part of (MA) rest on three inequalities of one type: **near the
modes, the first or second differences of the larger piece dominate the first differences of the
smaller piece I(H - N[w]).** All three hold on every tree pair with n <= 15 (n <= 19 for (Q1)) with
factors between 3 and 9.

## 5. The remaining hypothesis, and why it is second order

In the +1 case the data say n gamma / Q_{m+1} >= 4.0 while n phi / Q_{m+1} <= 0.84. A proof of (Q1)
therefore needs two things about the smaller forests:

1. a **lower bound on the curvature of Q = I(H - w) at its mode**: gamma >= c_1 Q_{m+1}/n with
   c_1 > 2 · 0.84. This is the log-concavity margin at the single index m + 1
   (n(1 - Q_m Q_{m+2}/Q_{m+1}^2) >= c_1 to leading order). The exhaustive data of run
   `20260924T092515Z` give n · (LC margin) >= 3.4 on the whole window for all trees with n <= 31,
   and the mode always lies in the window;
2. an **upper bound on the fall of the smallest piece Q' = I(H - N[w]) one step before m**:
   phi <= c_2 Q_{m+1}/n with c_2 < c_1/2. This combines the mass ratio Q'/Q (about
   0.7^{deg w}) with the slope of Q' just past its own mode.

Neither follows from unimodality or from the positions of the modes: Section 3 shows that the
shape information available to a mode-only induction (unimodality of P, Q, Q' plus (S1)) is
consistent with both Q_m >= Q_{m+2} and its failure. The curvature bound (1) is precisely the kind of
statement that the whole problem is about, restricted to one index. So the pendant-leaf route
does not escape the quantitative core; it localises it to the mode, where the empirical margins
are largest (factor 3 to 9), instead of the whole window.

## 6. Consequences and follow-up

- **Conditional chain.** Corollary 4 gives (S2) from unimodality, (S1) and (Q1) for smaller forests;
  Section 4 gives (S1) from (Q2), (Q3) and unimodality of smaller forests; the previous runs give:
  (S2) ⟹ every leaf at a degree-2 support vertex is aligned ⟹ (Corollary 2 of run
  `20260924T143534Z`) every forest with a degree-2 support vertex is unimodal, given unimodality of
  smaller forests. Hence

  > **Theorem 5 (conditional).** If (Q1), (Q2), (Q3) hold for all forests, then every forest that has a
  > support vertex of degree 2 is unimodal, and (S1), (S2) hold for all forests.

  The proof is the induction on the order with Corollary 4 and Section 4 supplying (S1), (S2).
  Forests all of whose support vertices have degree >= 3 (hub forests; they include all stars,
  hubs(t, l), the Kadrawi–Levit trees and the 703 trees without an aligned leaf found up to n = 26)
  are not covered: there the aligned vertex is a hub or the centre, and its alignment needs the
  analogue of Theorem 1 for the split I(F) = (1+x)^l I(F') + x I(F' - w) at a hub with l leaves. That
  analysis was not carried out here.
- **What a full proof along this route needs.** A "peak regularity" theorem for forests: log-concavity
  with margin c/n at the mode, plus a bound on the slope of I(K - S) just past its mode in terms of
  I(K) for a vertex set S. Both are quantitative statements about the neighbourhood of the mode
  only.

## 7. Boundaries

- ORIGINAL=NOT_CLOSED; (S2) is proved only modulo (Q1) (Corollary 4). No Lean was run.
- Theorem 1, Lemmas 2 and 3, Corollary 4 and Theorem 5 are written proofs of elementary statements;
  the structural facts they use (I(H) = I(H - w) + x I(H - N[w]), mode sets of unimodal sequences)
  are standard. Their exact verification on all tree pairs with n <= 15 is a sanity check, not part
  of the proof.
- The margins in Sections 3 and 4 are exhaustive for trees at the stated orders and are not claimed
  for forests with several components or for larger orders.
- Novelty is not claimed.
