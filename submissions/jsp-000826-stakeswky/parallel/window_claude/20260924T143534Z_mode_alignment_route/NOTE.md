# A mode-alignment route to unimodality: the aligned-sum lemma, exhaustive evidence, and the exact obstruction

Independent Claude window, 2026-09-24. It continues `20260924T092515Z_centroid_n31_drift_strict_product`.

**ORIGINAL=NOT_CLOSED.** Erdős #993 is neither proved nor refuted here.

**Correction (run `20260924T150627Z_ma_exhaustive_n26_forests18`).** The statement that an aligned vertex of degree at most 3 always exists holds for n <= 22 but not in general: hubs(6,3) (n = 25) has aligned hubs (degree 4) and centre (degree 6) but no aligned vertex of degree <= 3. The main statement (MA) is unaffected and is verified there for all trees with n <= 26 and all forests of order <= 20.

## 0. Why this direction

Every induction tried so far on this problem carries a log-concavity (LC) hypothesis. These fail to
propagate at the top of the hypothesis range (runs `20260924T072235Z` and `20260924T083841Z`),
because the pieces `F - v` and `F - N[v]` can have a smaller independence number and are then
needed one index beyond their own range. The analytic route (FLNYZ) needs an Edgeworth-level local
limit theorem, since LC is a second-order property; its constants are astronomical.

Unimodality itself is a first-order property: it only concerns where the sequence stops rising.
This run asks how far one can go with hypotheses that mention only **unimodality and the position
of the mode** of smaller forests. The answer:

- there is a clean sufficient condition (Lemma 1 / Theorem 3) that needs no quantitative input;
- it holds for every forest tested (6.6 million trees exhaustively, all forests of order <= 15,
  large structured and random trees);
- proving it still requires one quantitative comparison near the mode (Section 5), so it is a
  **localisation** of the difficulty, not a removal.

Notation: p_k = i_k(F), alpha = alpha(F), m_k = (k+1) p_{k+1}/p_k (mean number of addable vertices
of a uniform independent k-set), M(p) = the set of indices where p attains its maximum (an
interval for a unimodal p).

## 1. The aligned-sum lemma and the reduction

**Lemma 1 (aligned sum).** Let P, Q be unimodal sequences of nonnegative numbers. Suppose there are
m_P in M(P) and m_Q in M(Q) with |m_P - m_Q| <= 1. Then P + Q is unimodal, nondecreasing on
[0, min(m_P, m_Q)] and nonincreasing on [max(m_P, m_Q), infinity).

*Proof.* A unimodal sequence is nondecreasing up to any element of its mode set and nonincreasing
from any element of its mode set on. Both P and Q are nondecreasing on [0, min(m_P, m_Q)] and
nonincreasing on [max(m_P, m_Q), infinity). The two intervals overlap or are adjacent, so P + Q is
unimodal. ∎

Nothing quantitative is used. The lemma is false when the modes are two apart: (1, 2, 1, 0) + (0, 0, 1, 2)
= (1, 2, 2, 2) is still unimodal, but (1, 3, 1, 0) + (0, 0, 1, 3) = (1, 3, 2, 3) is not.

**Corollary 2 (aligned vertex).** For a graph G and a vertex v write A = I(G - v), C = I(G - N[v]),
so that I(G) = A + xC. If A and C are unimodal and

    dist(M(A), M(C) + 1) <= 1,                                          (AL)

then I(G) is unimodal. Call such a v **aligned**. ∎

**Theorem 3 (reduction).** Suppose

    (MA) every forest with at least one edge has an aligned vertex,

where the mode sets in (AL) are those of the actual sequences. Then every forest is unimodal.

*Proof.* Induction on the order. Edgeless forests have the sequence (1+x)^n. Otherwise take an aligned
v; F - v and F - N[v] are smaller forests, unimodal by induction, and Corollary 2 applies. ∎

So Erdős #993 reduces to locating modes: (MA) is a statement about the mode sets of pairs of smaller
forests, and nothing else. Any proof of (MA) proves the conjecture.

## 2. Evidence for (MA)

All computations are exact (64-bit integers in C for the exhaustive runs, Python integers
otherwise). `src/modes.c` walks all free trees of order n (WROM generation, the code audited in the
previous runs) and, for every vertex v, computes M(I(T - v)) and M(I(T - N[v])) and the alignment
distance.

| n | trees | trees with an aligned vertex | with an aligned vertex of degree <= 3 | with an aligned leaf | in which every leaf is aligned | rule "leaf at a support of minimum degree" |
|---|---|---|---|---|---|---|
| 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| 8 | 23 | 23 | 23 | 23 | 23 | 23 |
| 10 | 106 | 106 | 106 | 106 | 106 | 106 |
| 12 | 551 | 551 | 551 | 551 | 535 | 551 |
| 14 | 3,159 | 3,159 | 3,159 | 3,158 | 3,059 | 3,158 |
| 16 | 19,320 | 19,320 | 19,320 | 19,319 | 19,158 | 19,317 |
| 18 | 123,867 | 123,867 | 123,867 | 123,866 | 116,761 | 123,864 |
| 20 | 823,065 | 823,065 | 823,065 | 823,054 | 800,875 | 823,051 |
| 22 | 5,623,756 | 5,623,756 | 5,623,756 | 5,623,749 | 5,431,070 | 5,623,704 |

- **(MA) holds for every tree with 4 <= n <= 22**, always with a vertex of degree at most 3.
- **Forests.** `src/ma_forests2.py` enumerates every forest of order <= 15 as a multiset of trees
  (35,704 forests with an edge) and tries every vertex of every component: **(MA) holds for all of them**
  (`logs/ma_forests2.log`).
- **Large trees.** `src/ma_random.py`: 140 trees with 40 <= n <= 120 (uniform random labelled trees,
  random recursive trees, hubs(t,l), core trees, spiders, complete k-ary trees, caterpillars): all
  have an aligned vertex (`logs/ma_random.log`).

Not every leaf is aligned, and a few trees have no aligned leaf at all: 1, 1, 1, 11, 7 trees for
n = 14, 16, 18, 20, 22. All 21 are recorded with their per-vertex alignment data in
`results/trees_without_aligned_leaf.json`. They are hub trees: every leaf hangs on a support
vertex of degree >= 4. In each of them the aligned vertices are low-degree internal vertices that
are not supports (path vertices next to the centre), with degrees 2 to 5.

**No local rule is known.** "A leaf at a support vertex of minimum degree" fails for 1, 3, 3, 14, 52
trees (n = 14..22). "Any vertex of degree 2" fails: in the n = 16 example
`parents = [-1,0,1,2,3,3,3,3,0,8,9,9,9,0,0,0]`, the degree-2 vertex 8 (between the root of degree 5 and a
hub of degree 4) has alignment distance 2, while the degree-2 vertices 1 and 2 have distance 0.

## 3. How the mode moves under one deletion

The same runs record, for every tree T and vertex v, the signed shift of M(I(T - v)) relative to
M(I(T)) (0 if the intervals meet, otherwise the gap, positive when M(T - v) lies to the right).

| n | shift range over all (T, v) | shift range for leaves v | number of (T, v) with shift +1, by deg v |
|---|---|---|---|
| 14 | {-1, 0, +1} | {-1, 0} | 3: 179, 4: 232, 5: 29 |
| 16 | {-1, 0, +1} | {-1, 0} | 2: 8, 3: 392, 4: 731, 5: 479, 6: 190, 7: 24, 8: 2 |
| 18 | {-1, 0, +1} | {-1, 0} | 2: 33, 3: 3400, 4: 1993, 5: 1292, 6: 564, 7: 135, 8: 12, 9: 7 |
| 20 | {-1, 0, +1} | {-1, 0} | 2: 202, 3: 42588, 4: 64020, 5: 29877, 6: 4821, 7: 746, 8: 162, 9: 21 |
| 22 | {-1, 0, +1} | {-1, 0} | 2: 1559, 3: 113588, 4: 194550, 5: 137349, 6: 60437, 7: 14528, 8: 1790, 9: 187, 10: 41 |

Two empirical statements, never violated (6.6 million trees, 140 large trees):

- **(S1) single-deletion stability:** dist(M(T - v), M(T)) <= 1 for every vertex v;
- **(S2) pendant-leaf lemma:** for a leaf v, M(T - v) lies at, or one step to the left of, M(T).
  Equivalently: attaching a pendant leaf to a forest moves the mode set by 0 or +1, never down and
  never by 2.

Deleting a vertex of degree 2 to 10 can move the mode **up** by one (third column); it never moves
it by two in either direction. These +1 events are exactly the alignment failures of leaf splits
(Section 5).

**(S2) alone settles a large class.** Let v be a leaf whose support u has degree 2, and G = F - v.
Then u is a leaf of G and (S2) for (G, u) says M(G - u) is at or one left of M(G), so
M(I(F - N[v])) + 1 = M(G - u) + 1 is at or one right of M(I(F - v)) = M(G): v is aligned. Hence

> (S2) for all forests  ==>  every forest having a support vertex of degree 2 is unimodal (given the
> induction hypothesis).

The complementary class, "hub forests" in which every support vertex has degree >= 3, contains
the stars, hubs(t,l), the 21 recorded examples, and the Kadrawi–Levit trees; there the aligned
vertex must be found elsewhere.

## 4. The mean number of addable vertices under one deletion (first-order data)

The mode is the first k with m_k < k + 1. A proof of (MA) through means would compare m_k(G) and
m_k(G - u). `src/meanlemma.py` computes, over all trees of order n and all vertices u, the extremes
of m_k(G - u) - m_k(G) on the window [ceil(n/4), ceil((2alpha-1)/3)] (`logs/meanlemma.log`):

| n | max of m_k(G-u) - m_k(G) | max of m_k(G) - m_k(G-u) | same, leaves u only | n * LC margin on the window: min / max |
|---|---|---|---|---|
| 8 | 0.405 | 1.231 | -0.067 / 1.231 | 2.921 / 5.900 |
| 10 | 0.319 | 1.307 | 0.000 / 1.307 | 3.333 / 6.550 |
| 12 | 0.326 | 1.386 | 0.058 / 1.386 | 3.429 / 8.012 |
| 14 | 0.289 | 1.488 | -0.060 / 1.488 | 3.500 / 7.889 |
| 15 | 0.287 | 1.448 | -0.046 / 1.448 | 3.516 / 7.695 |

So a deletion raises the mean addable count by at most about 0.4, and lowers it by at most about
1.5, growing slowly with n. Combined with the drift-gap conjecture (DG) of the previous run
(m_{k+1} - m_k <= -0.76 on the window, so that m_k - (k+1) falls by at least 1.76 per step), such
first-order bounds locate the mode of G - u within [m_G - 2, m_G + 1]. This does **not** exclude the
+1 case. The +1 case is real (Section 3), so (MA) cannot follow from first-order comparisons alone.

The last column extends the previous run's curvature data: the normalised LC margin
n(1 - p_{k-1}p_{k+1}/p_k^2) on the window stays above 3.4 but its maximum grows slowly (8.0 at
n = 12, 10.2 at n = 24, from `logs/curv.log`). A two-sided "Gaussian tube" hypothesis with a uniform
upper constant is therefore not supported by the data.

## 5. The exact obstruction, and what would close it

Take a leaf v with support u, G = F - v, and write P = I(G - u), Q = I(G - N[u]), so that
I(G) = P + xQ and I(F) = I(G) + xP = (1+x)P + xQ. The pieces of the split at v are A = I(G) and
C = P. By the mediant property

    rho_k(G) = (P_{k+1} + Q_k)/(P_k + Q_{k-1})  lies between  rho_k(P) and rho_{k-1}(Q),

G is rising wherever both P (at k) and xQ (at k) are rising, and falling wherever both are
falling. Hence M(G) is contained in the convex hull of M(P) and M(Q) + 1. This is all that
unimodality of the pieces gives, and it allows M(P) = M(G) + 1 (the +1 shift), which is exactly
the misaligned configuration dist(M(A), M(C) + 1) = 2.

When does the +1 shift happen? Write m = m_P. It happens iff G falls at m - 1 although P rises
there:

    P_m - P_{m-1} <= Q_{m-2} - Q_{m-1}.                                              (1)

So Q, which has its mode to the left, must be falling at m - 2 at least as fast as P is still rising
at m - 1. For I(F) = (1+x)P + xQ to be unimodal in this configuration one needs, for every k with
m_Q < k <= m - 1,

    (P_{k+1} - P_k) + (P_k - P_{k-1}) >= Q_{k-1} - Q_k,                                (2)

that is, the two-step rise of P must dominate the one-step fall of Q, although by (1) the one-step
rise of P at k = m - 1 does not. Under a Gaussian picture with variance sigma^2, P rises by about
0.5 P/sigma^2 at m - 1 and by about 1.5 P/sigma^2 at m - 2, so (2) at k = m - 1 asks that the fall of
Q at m - 2 be at most about 2 P/sigma^2 while (1) says it is at least 0.5 P/sigma^2. The +1 shift is
therefore a window of moderate relative mass and moderate offset of Q, and unimodality of F there
holds by a quantitative margin, not by shape.

The same computation gives the minimal quantitative input for (S2). With P = I(H), Q = I(H - w) and
Q' = I(H - N[w]) (so P = Q + xQ'), the only case of (S2) not covered by the mediant argument is
m_Q = m_P + 1, and there (S2) is equivalent to

    Q_{m_P+1} - Q_{m_P} <= P_{m_P+1} - P_{m_P+2}  = (Q_{m_P+1} - Q_{m_P+2}) + (Q'_{m_P} - Q'_{m_P+1}),

while the hypothesis m_Q = m_P + 1 gives Q_{m_P+1} - Q_{m_P} <= Q'_{m_P-1} - Q'_{m_P}. A sufficient
condition is that the decrements of Q' do not shrink from m_P - 1 to m_P, i.e. that Q' = I(H - N[w])
is **concave** at m_P:

    Q'_{m_P-1} - 2 Q'_{m_P} + Q'_{m_P+1} <= 0.                                          (3)

Here m_P lies to the right of the mode of Q' (Q' is the small, left-shifted piece). Concavity just
past the mode is stronger than log-concavity there, but it is only needed at one index, for the
smallest of the three forests, and only in the +1 configuration. The concavity radius of the
sequences of all trees (the largest a with p_{k-1} + p_{k+1} <= 2p_k on [mode - a, mode + a]) is
recorded in `logs/conc.log`: the minimum radius over all trees is 0 for n <= 14 and n = 18, and 1 for n = 16, 20, 22, 24; the minimum of radius/sqrt(n) is 0.20-0.25 for n >= 16, and at n = 24 only 476,924 of 39,299,897 trees are concave on [mode - 2, mode + 2]. So the sequences are concave only within about 0.2 sqrt(n) of the mode, and the sufficient condition (3) is **not** uniformly available at small orders; (S2) holds for finer reasons than (3).

**Conclusion of the analysis.** The mode-alignment route replaces "LC on the whole window" by
"one inequality between an increment and a decrement, at one index next to the modes of two
smaller forests". It does not remove the quantitative core; it localises it. The statement to
prove is (S2) (or directly (MA)), and the natural sufficient condition is local concavity of the
smallest piece at the mode of the larger one.

## 6. Assessment of directions

1. **Shape-only inductions.** (MA) is the sharpest sufficient condition of this type: it is implied
   by (S1)+(S2)-type mode statements, holds everywhere tested, and any proof of it closes the
   problem. It cannot be proved from unimodality of the pieces alone (Section 5). Its quantitative
   core is one local inequality near the mode.
2. **LC-margin inductions** (Q_c, previous runs): obstructed at the top index for unique-MIS forests;
   the missing input is the LC surplus of a piece just beyond 2 alpha/3.
3. **Drift form** (previous run): WindowLC and unimodality are equivalent to bounds on
   E_k[number of non-adjacent free pairs] against m_k^2; the pairwise-covariance sum over
   non-adjacent vertices must be at most m_k. Still second order.
4. **Analytic (FLNYZ) route:** constants of order 10^30 at best after all free improvements.
5. **Unique-MIS forests:** p(x) = sum over independent S in V \ I of x^{|S|} (1+x)^{alpha - |N_I(S)|}
   with |N_I(S)| >= |S| + 1; a direct proof of the window condition for this class, plus the nested
   step (N) of run `20260924T072235Z`, would close the LC-margin induction.

**Recommended next steps.**

- Prove the pendant-leaf lemma (S2) for forests. It is the cleanest never-violated single
  statement about modes found in this project, and it settles every forest with a degree-2 support
  vertex. Its quantitative core is (3).
- For hub forests, identify the aligned vertex structurally (in all 21 recorded examples it is a
  low-degree non-support vertex near the centre) and prove alignment for it, or split hub forests
  differently (a hub u with l leaves gives I(F) = (1+x)^l I(F') + x I(F' - w), where the binomial
  factor smooths the dominant term).
- Extend the exhaustive (MA) check to n = 26 with the centroid generator of the previous run
  (about 15 minutes per order at n = 24 on 4 cores), and to all forests of order <= 18.

## 7. Boundaries

- ORIGINAL=NOT_CLOSED; no Lean was run (same container limitations as the previous run).
- Lemma 1, Corollary 2 and Theorem 3 are elementary and proved above. (S1), (S2), (MA) are
  empirical statements. The mode-shift and mean tables are exhaustive for the stated orders;
  the large-tree tests are samples.
- Novelty is not claimed for Lemma 1, which is a standard observation about sums of unimodal
  sequences.
