# A vectorised exhaustive checker and the frontier at n = 33 (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is not proved or refuted here. This run continues the goal of a
complete proof. It extends the verified range by exhaustive computation and records exactly what was
checked. PR #1 stays Draft; `RESEARCH_STATE.json` is not modified. No novelty, priority or award
claim is made.

Throughout, p_k = p_k(F) is the number of independent k-sets of a forest F of order n, alpha is the
independence number, and the window is [ceil(n/4), ceil((2 alpha - 1)/3)] as in earlier runs.
"Non-LC" means p_t^2 < p_{t-1} p_{t+1} at some interior index t.

## 1. The checker

The enumeration is the centroid enumeration of run `20260924T092515Z` (`cwlc.c`), unchanged:

- every rooted tree of order <= n/2 is generated once as a root plus a multiset of smaller rooted
  trees, with f = I(tau) and g = I(tau - root);
- a unicentroid tree is the centroid plus a multiset of rooted trees of order <= (n-1)/2 summing to
  n - 1, with I = prod f_c + x prod g_c;
- a bicentroid tree (n even) is an unordered pair of rooted trees of order n/2 joined at their
  roots, with I = f1 f2 - h1 h2, where h = f - g.

Each free tree occurs exactly once (Jordan's centroid theorem). The tree counts are compared with
Otter's formula for A000055, computed independently by `src/otter.py` (`logs/otter.log`).

`src/cwlc_vec.c` (used for odd n) and `src/cwlc_vec2.c` (the same, with the bicentroid pairs also
vectorised; used for even n) differ from `cwlc.c` in three ways. None changes what is checked.

1. **Tail tables.** For every r <= R the program lists all multisets of rooted trees of total order
   r, with prod f and prod g, sorted by their largest index. When the recursion has r <= R vertices
   left and largest allowed index M, the allowed completions are exactly the items with largest
   index <= M. They form a prefix of the sorted list. That prefix is processed in blocks of 16 trees
   by loops the compiler vectorises (AVX-512). `cwlc_vec2.c` processes the bicentroid partners j of
   each i the same way, 16 at a time.
2. **32-bit arithmetic.** Coefficients are stored as unsigned 32-bit integers, and all arithmetic is
   modulo 2^32. Every value the program compares or reports is a coefficient of I(F) for a forest F
   of order <= n. Each such coefficient is below 2^32 when n <= 35:
   - for a forest of order m <= 34, p_k <= C(34,17) = 2,333,606,220;
   - for a tree of order n <= 35 with a leaf l adjacent to s,
     p_k = p_k(T - l) + p_{k-1}(T - l - s) <= C(34,17) + C(33,16) = 3,500,409,330.

   So every compared or reported value is exact. The programs refuse n > 35.
3. **Screening.** Log-concavity at every interior index is screened in double precision. Every
   coefficient below 2^32 is an exact double, and each product has relative error at most 2^-52.
   A tree is flagged if some interior index has p_t^2 <= (1 + 2^-40) p_{t-1} p_{t+1}. Only flagged
   trees are analysed further, exactly (`__int128`), by the per-tree code of `cwlc_lean.c`
   (`src/`). That analysis covers unimodality, the first non-LC index, window membership and
   interior equalities, and prints the tree. A tree that is not flagged is strictly log-concave at
   every interior index. Its coefficients are positive up to alpha, so it is unimodal and has no
   interior equality. The checksum sum_k p_k (k+1) 0x9E3779B97F4A7C15 mod 2^64 is linear, so the
   program accumulates sum_k p_k (k+1) and multiplies once at the end; the value is identical.

With `-DSTATS`, `cwlc_vec2.c` also reports three floating-point statistics with the definitions of
`cwlc.c`: the minimum of n (1 - p_{t-1} p_{t+1} / p_t^2) over the window, the minimum of mode/n and
the maximum of mode/alpha. They are never used for pass or fail, and they roughly double the run
time, so the production runs do not use them.

**Validation.**

- `src/crosscheck.sh` (`logs/crosscheck.log`): for every n = 4..24 the RESULT lines of `cwlc_vec`,
  `cwlc_vec2` and `cwlc_vec2 -DSTATS` equal those of `cwlc_lean` (63 comparisons, 0 differences).
- `src/crosscheck_cwlc.sh` (`logs/crosscheck_cwlc.log`): for every n = 4..25, `cwlc_lean` gives the
  same tree count, non-unimodal count, non-LC count and checksum as the committed `cwlc.c` logs of
  run `20260924T092515Z` (22 comparisons, 0 differences).
- For 26 <= n <= 31 the output equals the committed logs of run `20260924T092515Z` (`cwlc.c`, which
  was cross-checked there against the level-sequence checker `wlc2`):

  | n | trees | non-LC | checksum |
  |---|---|---|---|
  | 26 | 279,793,450 | 2 | 15187486801461999869 |
  | 27 | 751,065,460 | 0 | 12541249224799509550 |
  | 28 | 2,023,443,032 | 19 | 14581303118083433297 |
  | 29 | 5,469,566,585 | 7 | 9518382814496898618 |
  | 30 | 14,830,871,802 | 121 | 15443233505184601198 |
  | 31 | 40,330,829,030 | 159 | 15334209151319815503 |

  n = 30 uses `cwlc_vec2`; the others use `cwlc_vec`. At n = 30 and n = 31 the sets of printed
  non-LC polynomials are identical to the committed ones. The n = 31 log was produced by an earlier
  revision of `cwlc_vec.c` whose table generator scanned every rooted-tree index instead of jumping
  by order. The enumeration and all checks are the same; only table construction was slower. The
  n = 26..29 logs were re-run with the final source.
- The statistics of `cwlc_vec2 -DSTATS` equal the MARGIN lines of `cwlc.c` at n = 12, 20, 23, 26
  and 28.

**Speed.** On the same 4 cores, n = 29 takes 72 s against 856 s for `cwlc.c`, and n = 33 takes
4,706 s. Extrapolating `cwlc.c` from n = 32 (18,915 s) by the tree-count ratio gives about 14 hours.

## 2. The trees with an interior log-concavity equality

Run `20260924T092515Z` found exactly one tree of order <= 31 with an interior equality
p_t^2 = p_{t-1} p_{t+1} and did not identify it. The new checker prints it, and it finds one more at
order 33 (`results/interior_equality_trees_n31_n33.txt`; parent arrays in centroid order):

| n | alpha | equality | p_{alpha-2}, p_{alpha-1}, p_alpha | window |
|---|---|---|---|---|
| 31 | 17 | t = 16 = alpha - 1 | 4624, 68, 1 | [8, 11] |
| 33 | 18 | t = 17 = alpha - 1 | 4096, 64, 1 | [9, 12] |

Both trees are LC, have a unique maximum independent set, and satisfy p_{alpha-2} = p_{alpha-1}^2.
Both equalities are isolated and lie far outside the window. Both polynomials were recomputed from
the parent arrays by an independent Python DP.

## 3. Trees of order 33

`src/cwlc_vec.c` with n = 33, R = 16 (`logs/cwlc_vec_n33.log`, 4,706 s on 4 cores, exit 0):

- 300,628,862,480 trees, equal to A000055(33) from Otter's formula; the rooted counts equal
  A000081 up to order 16;
- every tree is unimodal;
- 1,800 trees are non-LC (1,788 distinct polynomials). Each breaks only at t = alpha - 1:
  1,587 with alpha = 18, 206 with alpha = 19 and 7 with alpha = 20. The first break is at
  >= 0.944 alpha;
- no non-LC index and no equality lies in the window, so **strict** window LC holds;
- exactly one tree has an interior equality (Section 2); no tree has two consecutive equalities.

All 1,801 printed trees were rebuilt from their parent arrays and re-verified by the Python DP of
`src/ip.py`: polynomial, tree property, first non-LC index, unimodality, strict window LC and the
window drift condition (`src/reverify_examples.py`, `logs/reverify_n33.log`, 0 problems).

## 4. Forests of order 33

**Forests with a non-LC component** (`src/forest_nonlc_gen.py`, `logs/forest_nonlc_N33.log`,
`results/forest_nonlc_N33.json`). Every tree of order <= 25 is LC, so a forest of order <= 51 has at
most one non-LC component. Such a forest is therefore T + R, with T a non-LC tree of order 26..33
and R a forest of order <= 33 - |T| <= 7. Since I(T + R) = I(T) I(R), the script multiplies every
non-LC tree polynomial of order 26..33 by every distinct forest polynomial of the remaining order. It
checks unimodality, strict window LC and the window drift condition exactly. Tree polynomials of
order <= 7 come from a rooted-tree generator; for m <= 6 their numbers (1, 1, 1, 2, 3, 6) equal those
of the Prüfer enumeration used in run `20260925T040924Z`. There are

    2·79 + 19·23 + 7·13 + 121·7 + 159·4 + 920·2 + 1788·1 = 5,797

pairs; all pass. The same script with NMAX = 32 reproduces the 1,184 pairs of run
`20260925T040924Z` (plus the 920 order-32 trees themselves).

**Forests of order 33 whose components are all LC.** Every component has order <= 32. The only tree
of order <= 32 with an interior equality is the order-31 tree of Section 2. Its equality is
isolated, and in a forest of order 33 it occurs only with K2 or 2K1, whose sequences (1, 2) and
(1, 2, 1) are strictly LC on their supports and have degree >= 1. Every other component is strictly
LC on its support. Lemma 4, Corollary 5 and the isolated-equality remark of run `20260924T092515Z`
(Section 5) then give strict LC of p(F) on [0, alpha(F)].

**Theorem (computer-assisted).** Every forest of order n <= 33 satisfies strict log-concavity on
[ceil(n/4), ceil((2 alpha - 1)/3)] and is unimodal.

*Proof.* Trees of order <= 32: runs `20260924T092515Z` and `20260925T040924Z`. Trees of order 33:
Section 3. Forests of order <= 32: run `20260925T040924Z`. Forests of order 33 with at least two
components: the two paragraphs above. ∎

So the Lean proposition `WindowLC` holds for every forest on Fin n with n <= 33, and the open range of
`erdos993_of_windowLC_below` is **34 <= n < N0**.

## 5. What this does and does not change

- The verified range grows by one order. The cost per order is still about a factor 2.75, so the
  exhaustive route gains a few orders at best. With the 32-bit bound, n = 34 and n = 35 are
  feasible on 4 cores; n >= 36 needs 64-bit lanes.
- The only explicit threshold in the repository is N_LC = 2^2600000 (run
  `window_a/20260921T161559Z_round9_effective_cutoff`). The barrier analysis of run
  `20260925T040924Z` (Section 4) still applies: neither exhaustive computation nor the available
  analytic estimates close 34 <= n < N0, and no structural invariant that implies window LC has
  been found.
- The non-LC pattern persists at n = 33: every break is at alpha - 1, with a first break at
  >= 0.944 alpha, far above the window top ~ (2/3) alpha. Every LC equality found so far is also at
  alpha - 1, in a tree with a unique maximum independent set.

## 6. Boundaries

- ORIGINAL=NOT_CLOSED. No Lean was run (the environment cannot fetch the toolchain or the mathlib
  cache).
- The theorem is conditional on the correctness of the programs and of the hardware. The
  mitigations are the cross-checks of Section 1, the independent Python re-verification of every
  printed tree, and the tree counts from Otter's formula.
- Floating point is used only for screening, with a 2^-40 safety factor. It is never used to
  declare a tree non-LC, unimodal or non-unimodal; flagged trees are decided exactly.
