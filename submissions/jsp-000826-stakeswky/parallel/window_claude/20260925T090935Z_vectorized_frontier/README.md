# Vectorised exhaustive checker; strict window LC and unimodality for every forest of order <= 34 (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is **not** proved or refuted here. The goal of the session was
a complete proof; it was not achieved. This run extends the exhaustively verified range by two
orders and then stops enumeration. PR #1 stays Draft; `RESEARCH_STATE.json` is not modified. No
novelty, priority or award claim is made.

## Results

1. **A faster exact checker.** `src/cwlc_vec.c` and `src/cwlc_vec2.c` keep the centroid
   enumeration of run `20260924T092515Z` and its per-tree exact analysis. They add precomputed
   tables of small rooted forests, AVX-512 blocks of 16 trees, 32-bit modular arithmetic that is
   exact for n <= 35, and double-precision screening with exact recheck of every flagged tree.
   They are about 12 times faster than `cwlc.c`. Their output equals the committed logs for every
   n <= 31 compared, including checksums and the sets of non-LC polynomials. `src/cwlc_vec3.c` adds
   an exact 64-bit fallback that removes the counting bound (exact for n <= 37). It is validated,
   including runs forced through the fallback, but it was not used for production.
2. **Trees of orders 33 and 34.** All 300,628,862,480 and 823,779,631,721 trees (= A000055 by
   Otter's formula) are unimodal, and strict window LC holds. 1,800 and 7,040 trees are non-LC, each
   breaking only at alpha - 1 (first break >= 0.944 alpha). All printed trees were re-verified in
   Python.
3. **Forests of orders 33 and 34.** All 5,797 and 18,204 (non-LC tree, small forest) polynomial
   pairs pass. Forests whose components are all LC are covered by the strict Hoggar lemma of run
   `20260924T092515Z`.
4. **Theorem (computer-assisted).** Every forest of order n <= 34 is strictly log-concave on
   [ceil(n/4), ceil((2 alpha - 1)/3)] and unimodal. The open range of `erdos993_of_windowLC_below`
   is now 35 <= n < N0.
5. **The LC-equality trees identified.** Run `20260924T092515Z` counted a single order-31 tree
   with an interior equality but did not identify it. This run identifies it, together with one
   such tree of order 33 and six of order 34. Every one is LC and has its only equality at
   alpha - 1.

## Why enumeration stops at n = 34

Each further order costs about 2.75 times more (n = 35 about 10 h, n = 36 about 2 days on 4 cores).
The only explicit analytic threshold in the repository is 2^2600000, and even an optimised one is
estimated near 10^6. No feasible enumeration closes 35 <= n < N0. See `NOTE.md`, Section 5.

## Files

- `NOTE.md`, `VERDICT.json`, `MANIFEST.sha256`.
- `src/`:
  - `cwlc_vec.c` (odd n) and `cwlc_vec2.c` (even n; vectorised bicentroid part; optional `-DSTATS`);
  - `cwlc_vec3.c` (exact 64-bit fallback; validated, not used for production);
  - `cwlc_lean.c` (exact per-tree reference);
  - `crosscheck.sh`, `crosscheck_cwlc.sh`, `crosscheck3.sh`;
  - `forest_nonlc_gen.py`, `reverify_examples.py`, `ip.py`, `otter.py`.
- `logs/`:
  - `cwlc_vec_n{26..29,31,33}.log` and `cwlc_vec2_n{30,34}.log`, each with an `.exit` file;
  - `crosscheck.log`, `crosscheck_cwlc.log`, `crosscheck3.log`;
  - `forest_nonlc_N33.log`, `forest_nonlc_N34.log`, `reverify_n33.log`, `reverify_n34.log`,
    `otter.log`.
- `results/`: `forest_nonlc_N33.json`, `forest_nonlc_N34.json`,
  `interior_equality_trees_n31_n33_n34.txt`.

Build with `gcc -O3 -march=native -fopenmp`. Run as `cwlc_vec n threads R`, with R = (n-1)/2 for the
production runs. `cwlc_vec3` takes a fourth argument, log2 of the fallback threshold (default 32).
