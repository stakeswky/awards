# A vectorised exhaustive checker and the frontier at n = 34 (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is not proved or refuted here. This run continued the goal of a
complete proof. It extends the verified range by exhaustive computation by two orders and records
exactly what was checked. Enumeration stops at n = 34 (Section 5). PR #1 stays Draft;
`RESEARCH_STATE.json` is not modified. No novelty, priority or award claim is made.

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

`src/cwlc_vec3.c` removes the dependence on the counting bound of item 2. It computes every tree's
total I(T;1) exactly in 64 bits from 64-bit totals of the parts. A tree with I(T;1) < 2^32 has every
coefficient below 2^32 and takes the 32-bit path. Any other tree is rebuilt exactly (64-bit
coefficients, `__int128` comparisons) from its branch list and analysed exactly. It is exact for
n <= 37. It was validated (below) but not used for the production runs, because enumeration stops at
n = 34.

**Validation.**

- `src/crosscheck.sh` (`logs/crosscheck.log`): for every n = 4..24 the RESULT lines of `cwlc_vec`,
  `cwlc_vec2` and `cwlc_vec2 -DSTATS` equal those of `cwlc_lean` (63 comparisons, 0 differences).
- `src/crosscheck_cwlc.sh` (`logs/crosscheck_cwlc.log`): for every n = 4..25, `cwlc_lean` gives the
  same tree count, non-unimodal count, non-LC count and checksum as the committed `cwlc.c` logs of
  run `20260924T092515Z` (22 comparisons, 0 differences).
- `src/crosscheck3.sh` (`logs/crosscheck3.log`): for every n = 4..22, `cwlc_vec3` and
  `cwlc_vec3 -DSTATS` equal `cwlc_lean` at four thresholds. Threshold 2^32 uses only the fast path,
  2^1 and 2^(n/2) send every tree through the exact fallback, and 2^(4n/5) mixes both
  (152 comparisons, 0 differences).
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

**Speed.** On the same 4 cores, n = 29 takes 72 s against 856 s for `cwlc.c`. n = 33 takes 4,706 s,
where extrapolating `cwlc.c` from n = 32 (18,915 s) gives about 14 hours. n = 34 takes 19,532 s.
Even orders are slower per tree for a structural reason. When the largest centroid branch has
(n-2)/2 vertices, n/2 vertices remain, one more than the largest table (R = (n-2)/2). Those trees
pass through one more recursion level in small batches. A one-thread sample at n = 34 measured
about 5 million trees/s with a largest branch of 16 vertices, against 15 and 22 million with 15
and 14.

## 2. The trees with an interior log-concavity equality

Run `20260924T092515Z` found exactly one tree of order <= 31 with an interior equality
p_t^2 = p_{t-1} p_{t+1} and did not identify it. The new checker prints it, and it finds one at order
33 and six at order 34 (`results/interior_equality_trees_n31_n33_n34.txt`; parent arrays in
centroid order):

| n | trees | alpha | equality at | p_{alpha-2}, p_{alpha-1}, p_alpha | window |
|---|---|---|---|---|---|
| 31 | 1 | 17 | alpha - 1 | 4624, 68, 1 | [8, 11] |
| 33 | 1 | 18 | alpha - 1 | 4096, 64, 1 | [9, 12] |
| 34 | 1 | 18 | alpha - 1 | 11664, 108, 1 | [9, 12] |
| 34 | 1 | 18 | alpha - 1 | 9522, 138, 2 | [9, 12] |
| 34 | 1 | 18 | alpha - 1 | 5625, 75, 1 | [9, 12] |
| 34 | 3 | 19 | alpha - 1 | 3721, 61, 1 | [9, 13] |

Every one of these trees is LC. Each has exactly one equality, at alpha - 1, far outside the window,
and p_alpha is 1 or 2. All polynomials were recomputed from the parent arrays by an independent
Python DP.

## 3. Trees of orders 33 and 34

| | n = 33 | n = 34 |
|---|---|---|
| program, R | `cwlc_vec`, 16 | `cwlc_vec2`, 16 |
| log | `logs/cwlc_vec_n33.log` | `logs/cwlc_vec2_n34.log` |
| seconds on 4 cores | 4,706 | 19,532 |
| trees (= A000055 by Otter's formula) | 300,628,862,480 | 823,779,631,721 |
| non-unimodal | 0 | 0 |
| non-LC trees (distinct polynomials) | 1,800 (1,788) | 7,040 (6,980) |
| non-LC by alpha | 18: 1,587; 19: 206; 20: 7 | 18: 4,497; 19: 2,359; 20: 184 |
| non-LC index | only alpha - 1 | only alpha - 1 |
| first break / alpha | >= 0.944 | >= 0.944 |
| non-LC or equality in the window | 0 | 0 |
| trees with an interior equality | 1 | 6 |
| checksum | 16974435275170290889 | 17699116221550610219 |

So every tree of order 33 or 34 is unimodal and **strictly** log-concave on the window. No tree has
two consecutive equalities. The rooted counts equal A000081 up to order 17.

All 1,801 printed trees of order 33 and all 7,046 of order 34 were rebuilt from their parent arrays
and re-verified by the Python DP of `src/ip.py`. The check covers the polynomial, the tree property,
the first non-LC index, unimodality, strict window LC and the window drift condition
(`src/reverify_examples.py`, `logs/reverify_n33.log`, `logs/reverify_n34.log`, 0 problems).

## 4. Forests of orders 33 and 34

**Forests with a non-LC component** (`src/forest_nonlc_gen.py`; `logs/forest_nonlc_N33.log`,
`logs/forest_nonlc_N34.log`; `results/forest_nonlc_N33.json`, `results/forest_nonlc_N34.json`).
Every tree of order <= 25 is LC, so a forest of order <= 51 has at most one non-LC component. Such a
forest is therefore T + R, with T a non-LC tree of order 26..N and R a forest of order <= N - |T|.
Since I(T + R) = I(T) I(R), the script multiplies every non-LC tree polynomial of order 26..N by
every distinct forest polynomial of the remaining order. It checks unimodality, strict window LC
and the window drift condition exactly. Tree polynomials of order <= 8 come from a rooted-tree
generator. For m <= 6 their numbers (1, 1, 1, 2, 3, 6) equal those of the Prüfer enumeration used in
run `20260925T040924Z`. The pair counts are:

    N = 33:  2·79 + 19·23 + 7·13 + 121·7 + 159·4 + 920·2 + 1788·1 = 5,797
    N = 34:  2·152 + 19·43 + 7·23 + 121·13 + 159·7 + 920·4 + 1788·2 + 6980·1 = 18,204

All pass. The same script with N = 32 reproduces the 1,184 pairs of run `20260925T040924Z`, plus
the 920 order-32 trees themselves.

**Forests of order 33 or 34 whose components are all LC.** Every component has order <= 33. The
only trees of order <= 33 with an interior equality are the order-31 and order-33 trees of
Section 2. Each has one isolated equality, and they cannot occur together in a forest of order
<= 34. The order-31 tree occurs with a forest of order <= 3. The order-33 tree occurs only with K1.
The possible partners are K1, K2, 2K1, P3, K2 + K1 and 3K1, with sequences (1,1), (1,2), (1,2,1),
(1,3,1), (1,3,2) and (1,3,3,1). Each is strictly LC on its support and has degree >= 1. Every other
component is strictly LC on its support. Lemma 4, Corollary 5 and the isolated-equality remark of
run `20260924T092515Z` (Section 5) then give strict LC of p(F) on [0, alpha(F)].

**Theorem (computer-assisted).** Every forest of order n <= 34 satisfies strict log-concavity on
[ceil(n/4), ceil((2 alpha - 1)/3)] and is unimodal.

*Proof.* Trees of order <= 32: runs `20260924T092515Z` and `20260925T040924Z`. Trees of orders 33
and 34: Section 3. Forests of order <= 32: run `20260925T040924Z`. Forests of orders 33 and 34 with
at least two components: the two paragraphs above. ∎

So the Lean proposition `WindowLC` holds for every forest on Fin n with n <= 34, and the open range of
`erdos993_of_windowLC_below` is **35 <= n < N0**.

## 5. Why enumeration stops here

The verified range grew by two orders. Continuing would not change the status of the problem:

| n | trees | time on these 4 cores |
|---|---|---|
| 33 | 3.0 · 10^11 | 1.3 h (measured) |
| 34 | 8.2 · 10^11 | 5.4 h (measured) |
| 35 | 2.3 · 10^12 | about 10 h (estimated) |
| 36 | 6.2 · 10^12 | about 2 days (estimated; needs `cwlc_vec3`) |

- Each order costs about a factor 2.75 more. Any feasible amount of computation gains a few orders.
- The only explicit threshold in the repository is N_LC = 2^2600000 (run
  `window_a/20260921T161559Z_round9_effective_cutoff`). The barrier analysis of run
  `20260925T040924Z` (Section 4) puts even an optimised analytic threshold near 10^6. No amount of
  enumeration reaches that.
- No structural invariant that implies window LC for all trees has been found. Closing 35 <= n < N0
  needs such an invariant, or a new analytic method valid for small n.
- The data remain consistent with the conjecture. Through n = 34, every non-LC break and every LC
  equality is at alpha - 1, with the first break at >= 0.944 alpha, far above the window top
  ~ (2/3) alpha.

## 6. Boundaries

- ORIGINAL=NOT_CLOSED. No Lean was run (the environment cannot fetch the toolchain or the mathlib
  cache).
- The theorem is conditional on the correctness of the programs and of the hardware. The
  mitigations are the cross-checks of Section 1, the independent Python re-verification of every
  printed tree, and the tree counts from Otter's formula.
- Floating point is used only for screening, with a 2^-40 safety factor. It is never used to
  declare a tree non-LC, unimodal or non-unimodal; flagged trees are decided exactly.
