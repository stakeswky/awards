# Vectorised exhaustive checker; strict window LC and unimodality for every forest of order <= 33 (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is **not** proved or refuted here. The goal of the session was
a complete proof; it was not achieved. This run extends the exhaustively verified range by one order.
PR #1 stays Draft; `RESEARCH_STATE.json` is not modified. No novelty, priority or award claim is made.

## Results

1. **A faster exact checker.** `src/cwlc_vec.c` and `src/cwlc_vec2.c` keep the centroid
   enumeration of run `20260924T092515Z` and its per-tree exact analysis. They add precomputed
   tables of small rooted forests, AVX-512 blocks of 16 trees, 32-bit modular arithmetic that is
   exact for n <= 35, and double-precision screening with exact recheck of every flagged tree.
   They are about 12 times faster than `cwlc.c`. Their output equals the committed logs for every
   n <= 31 compared, including checksums and the sets of non-LC polynomials.
2. **Trees of order 33.** All 300,628,862,480 trees (= A000055(33) by Otter's formula) are
   unimodal, and strict window LC holds. 1,800 trees are non-LC, each breaking only at alpha - 1
   (first break >= 0.944 alpha). All printed trees were re-verified in Python.
3. **Forests of order 33.** All 5,797 (non-LC tree, small forest) polynomial pairs pass. Forests
   whose components are all LC are covered by the strict Hoggar lemma of run `20260924T092515Z`.
4. **Theorem (computer-assisted).** Every forest of order n <= 33 is strictly log-concave on
   [ceil(n/4), ceil((2 alpha - 1)/3)] and unimodal. The open range of `erdos993_of_windowLC_below`
   is now 34 <= n < N0.
5. **The LC-equality trees identified.** The single order-31 tree with an interior equality, counted
   but not identified by run `20260924T092515Z`, and a new one at order 33 both have the equality at
   alpha - 1, with p_{alpha-2} = p_{alpha-1}^2 and p_alpha = 1.

## What remains

No route closes 34 <= n < N0. The exhaustive cost still grows by about a factor 2.75 per order,
and the only explicit analytic threshold in the repository is 2^2600000. See `NOTE.md`, Section 5.

## Files

- `NOTE.md`, `VERDICT.json`, `MANIFEST.sha256`.
- `src/`:
  - `cwlc_vec.c` (odd n) and `cwlc_vec2.c` (even n; vectorised bicentroid part; optional `-DSTATS`);
  - `cwlc_lean.c` (exact per-tree reference);
  - `crosscheck.sh` and `crosscheck_cwlc.sh`;
  - `forest_nonlc_gen.py`, `reverify_examples.py`, `ip.py`, `otter.py`.
- `logs/`:
  - `cwlc_vec_n{26..29,31,33}.log` and `cwlc_vec2_n30.log`, each with an `.exit` file;
  - `crosscheck.log`, `crosscheck_cwlc.log`, `forest_nonlc_N33.log`, `reverify_n33.log`,
    `otter.log`.
- `results/`: `forest_nonlc_N33.json`, `interior_equality_trees_n31_n33.txt`.

Build with `gcc -O3 -march=native -fopenmp`. Run as `cwlc_vec n threads R`, with R = (n-1)/2 for the
production runs.
