# A centroid route past n = 34 without enumeration: ultra-log-concave branches (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is not proved or refuted here. This note records a possible
route that would extend unimodality from n <= 34 to n <= 47 without enumerating trees of those
orders. It rests on one lemma, which is **conjectural**: it survives adversarial numerical search,
but it is not proved here. PR #1 stays Draft; `RESEARCH_STATE.json` is not modified. No novelty,
priority or award claim is made.

Notation: for a sequence s, s is **LC** if s_k^2 >= s_{k-1} s_{k+1}, and **ULC** (ultra-log-concave
of infinite order) if k s_k^2 >= (k+1) s_{k-1} s_{k+1} for every interior k, i.e. k! s_k is LC.

## 1. The reduction at the centroid

Let T be a tree of order n >= 3 with centroid c, and let tau_1, ..., tau_d be the branches at c
(d >= 2), rooted at the neighbours r_i of c. Put

    f_i = I(tau_i),   g_i = I(tau_i - r_i),   h_i = I(tau_i - N[r_i]),   so   f_i = g_i + x h_i.

Then I(T) = prod f_i + x prod g_i. Every branch has order <= n/2, g_i and h_i are forests with
constant term 1, and h_i <= g_i coefficientwise (h_i counts independent sets of a subforest).

**Lemma U (conjectural).** Let d >= 2. For i = 1..d let g_i, h_i be positive sequences with no
internal zeros and constant term 1, with h_i <= g_i coefficientwise, such that g_i, h_i and
f_i = g_i + x h_i are ULC. Then p = prod f_i + x prod g_i is unimodal.

**Consequence (conditional on Lemma U).** Every forest of order n <= 47 is unimodal.

*Proof of the consequence.* A tree of order n <= 47 has centroid branches of order <= 23. By
Section 2, the independence polynomial of every tree of order <= 23 is ULC. ULC sequences are closed
under convolution (Walkup 1976; Liggett 1997), so the forests g_i and h_i, whose components have
order <= 22, are ULC too. Lemma U then makes every tree of order <= 47 unimodal. A forest of order
<= 47 has at most one component of order >= 26, since two would need order >= 52. Every tree of
order <= 25 is LC (runs `20260924T092515Z` and earlier), so the product of the other components is
LC. An LC sequence convolved with a unimodal one is unimodal (strong unimodality of LC sequences,
Ibragimov / Keilson–Gerber). ∎

This would move the verified range from n <= 34 to n <= 47 for unimodality. It would not give strict
window LC, which the Lean reduction `erdos993_of_windowLC_below` asks for, and it would not touch
48 <= n < N0.

## 2. Ultra-log-concavity of small trees

`src/ulc_vec.c` is `cwlc_vec.c` of run `20260925T090935Z` with the screen and the exact recheck
changed to the ULC inequality (`logs/ulc_summary.log`, `logs/ulc_n*.log`):

- every tree of order 4..23 and 25 has a ULC independence polynomial;
- exactly one tree of order 24 does not. Its polynomial is
  1, 24, 253, 1553, 6193, 16912, 32389, 43650, 40711, 25144, 9348, 1653, 42, 1 (alpha = 13). ULC
  fails only at k = 12 = alpha - 1, where 12·42^2 = 21,168 < 13·1,653·1 = 21,489. It is LC there.

A Python check (`src/ulc_trees_py.py`, `logs/ulc_trees_py.log`) confirms 0 failures for n <= 18.

ULC has a direct meaning here. With m_k = (k+1) p_{k+1} / p_k, the expected number of vertices that
can be added to a uniformly random independent k-set, ULC at k+1 says m_{k+1} <= m_k: bigger
independent sets leave fewer addable vertices on average. ULC implies LC, and LC implies unimodality.
But trees of order 26 can be non-LC, so ULC cannot hold for all trees.

## 3. Adversarial tests of candidate lemmas

Each candidate was attacked by random sampling and by simulated-annealing hill-climbing on the
sequences' log-increments. The objective is the relative depth of the deepest dip of p, which is
positive exactly when p is not unimodal. All scripts are seeded (`src/lemma_*.py`, `logs/lemma_*.log`).

| Candidate | Result |
|---|---|
| F, B LC; F_0 = B_0 = 1; B <= F <= (1+x)^d B coefficientwise; F + xB unimodal | false (random search) |
| Lemma U with LC in place of ULC | false. Random sampling (10^5 cases) finds no dip, but one of four hill-climbs finds one with d = 2, 0.25 % deep, built on a near-flat plateau and a branch with g = (1, 46.9) |
| F, G ULC; F_0 = G_0 = 1; G <= F coefficientwise; F + xG unimodal (no branch structure) | false; F_1 is far larger than any forest with deg F vertices allows |
| **Lemma U** (branch-structured, ULC) | **no counterexample**; best configurations stay 6 to 9 % away from a dip (d = 2..8) |

So both ingredients matter. ULC excludes the plateaus behind the LC counterexamples. The per-branch
link f_i = g_i + x h_i with h_i <= g_i keeps prod g_i from sitting to the right of prod f_i with
large mass, which is what the unstructured ULC counterexamples exploit.

## 4. Why Lemma U might be provable, and where a proof would need care

Write F = prod f_i, G = prod g_i (both ULC), p_k = F_k + G_{k-1}, and

    a_k = (k+1) F_{k+1}/F_k - (k+1),   b_k = k G_k / G_{k-1} - k.

ULC means a_{k+1} <= a_k - 1 and b_{k+1} <= b_k - 1, and

    p_{k+1} - p_k = F_k a_k / (k+1) + G_{k-1} b_k / k.

Outside the interval between the sign changes of a and of b, both terms have the same sign. A dip
therefore needs two indices k < l in that interval with the combined sign going -, then +. Comparing
the two conditions and using the unit decrease of a and b gives a necessary condition. Heuristically,
for Poisson-like F and G at level k, it reads a_k |b_k| > k, meaning the modes of F and xG differ by
more than about 2 sqrt(k). At such a separation, the branch structure bounds the mass of xG. The
mean gap is sum_i theta_i (1 + mean h_i - mean g_i) - 1, with theta_i = h_i(1)/f_i(1) <= 1/2, while
G(1)/F(1) = prod (1 - theta_i) <= exp(-sum theta_i). A dip would need xG to beat F's Gaussian-like
decay at the separation. The two sides balance only when all theta_i = 1/2, which is the star, and
stars are unimodal.

Making this rigorous needs two things not done here. One is a precise version of the necessary
condition, including the case where G drops steeply near the end of its support (|b_k| close to k).
The other is a quantitative bound on G_{k-1}/F_k from the branch structure. Section 3 is evidence,
not proof.

## 5. Status

- Proved here: nothing new about unimodality. Section 1's consequence is conditional on Lemma U.
- Verified here: ULC of all trees of order <= 25 except one tree of order 24 (Section 2).
- Evidence: Lemma U survives the searches of Section 3.
- Unchanged: every forest of order <= 34 is unimodal with strict window LC (run
  `20260925T090935Z`); the open range of the formal reduction is 35 <= n < N0.
