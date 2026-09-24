# Open window, drift form, strict products, and exhaustive trees through n = 31 (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is **not** proved or refuted here. This run continues
`20260924T084900Z_root_moment_certificates` and the WindowLC line of runs `20260923T153415Z` onward.
PR #1 stays Draft. The shared `RESEARCH_STATE.json` is not modified, as in the earlier independent
windows. No novelty, priority or award claim is made.

## Results

1. **Open window, non-strict (Lemma 1; written proof).** The formal reduction
   `erdos993_of_windowLC_below` asks for strict LC on the closed window [q, top], with
   q = ceil(n/4) and top = ceil((2alpha-1)/3). The (P)/(T) lemmas already used there need less:
   - **non-strict** LC on the open window [q+1, top-1] suffices;
   - so does the weaker condition "after a descent, m_{r+1} <= m_r + 1" on r in [q, top-2].
2. **Drift identity (Lemma 2; written proof).** With m_r = (r+1)p_{r+1}/p_r, the mean number of
   addable vertices of a uniform independent r-set,

       m_{r+1} - m_r = E_r|N(J)| - E_{r+1}|N(J)| - 1.

   So the drift condition says that the mean neighbourhood of a random independent set shrinks by
   at most 2 per extra vertex. LC_{r+1} is exactly m_{r+1} - m_r <= m_r/(r+1).
3. **The drift condition fails outside the window (Proposition 3; exact certificate).** core((8,)^17)
   has n = 290 and is unimodal. It has m_138 - m_137 = 1.218 > 1 at r = 0.895 alpha, far to the
   right of the window. Inside the window, the drift is **negative** for every tested tree and
   forest:
   - at most -0.762 over all trees with n <= 31 (exhaustive);
   - -0.772 over 1,065 family trees up to n = 220, -0.824 by local search, -0.804 over 2,578 forests,
     -1.685 over the 149 non-LC trees.

   This motivates the scale-free conjecture (DG): window drift <= -c. It is stated, not proved.
4. **Strict Hoggar (Lemma 4 and Corollary 5; written proof).** Dc_k >= sum_j Da_{k-j} Db_j for
   c = a*b. Hence products of sequences that are strictly LC on their supports are again strictly LC.
   This closes the caveat "strict-product lemma not re-verified", recorded twice for the forest base
   case of the strict `WindowLC`.
5. **Exhaustive trees through n = 31 with a second, independent algorithm (computation).**
   - Method: `src/cwlc.c` enumerates free trees by centroid decomposition, as multisets of rooted
     trees with precomputed (I(tau), I(tau - root)). It shares no code with the WROM checkers
     `wlc.c`/`wlc2.c`.
   - Tree and rooted-tree counts equal OEIS A000055/A000081.
   - Checksums equal those of `wlc2` for every order compared (n = 4..27).
   - The non-LC trees for n = 26..30 coincide, as multisets of sequences, with the earlier runs.
   - **New order n = 31 (40,330,829,030 trees, 6,834 s on 4 cores):**
     - every tree is unimodal;
     - no non-LC index and no equality lies in the window, so strict `WindowLC` holds;
     - 159 trees are non-LC, each breaking only at k = alpha - 1 (>= 0.9412 alpha);
     - the drift condition holds at every r;
     - exactly one tree has an interior LC equality, isolated and outside the window.
   - The Python DP re-verifies all 308 non-LC trees (n = 26..31) from their parent arrays.
6. **Every forest of order <= 31 (Theorem 6).** Strict window LC and unimodality hold, by
   Corollary 5, the exhaustive tree data (no tree of order <= 30 has any interior LC equality) and a
   direct check of all 608 (non-LC tree, small forest) polynomial pairs. The open range of the formal
   reduction `erdos993_of_windowLC_below` is therefore 32 <= n < N0.

Lean was **not** run: from this container, GitHub returns 403 for the external FLNYZ repository
and the mathlib cache host is unreachable. Lemmas 1, 2 and 4 are written proofs with exact
numerical sanity checks.

## Files

- `NOTE.md`: statements, proofs, tables and exact scope.
- `VERDICT.json`: machine-readable status.
- `src/`:
  - `cwlc.c`: centroid exhaustive checker;
  - `summarize_cwlc.py`, `make_table.py`, `crosscheck_nonlc.py`, `reverify_examples.py`,
    `forest_nonlc.py`;
  - `m1cert.py`, `window_drift.py`, `big_drift.py`, `forest_drift.py`, `lemma_checks.py`;
  - `ip.py`, `families.py`: Python DP, and families copied from the previous run.
- `results/`:
  - `cwlc_summary.json`, `table4.md`: per order;
  - `crosscheck_nonlc.json`, `reverified_examples.json`, `forest_nonlc_N31.json`;
  - `m1_certificate.json`, `window_drift_seed1.json`, `big_drift.json`.
- `logs/`:
  - raw `cwlc` logs per order;
  - `wlc2_crosscheck/`: the `wlc2` source used (SHA-256 identical to run `20260924T011530Z`) and
    its logs;
  - every Python run log with its exit code.
- `MANIFEST.sha256`.

## Reproduce

    cd src && gcc -O3 -march=native -fopenmp -o cwlc cwlc.c && cd ..
    for n in $(seq 4 31); do src/cwlc $n 4 > logs/cwlc_n$n.log; done   # n=31: 6,834 s on 4 cores
    cd results
    python3 ../src/summarize_cwlc.py ../logs/cwlc_n*.log
    python3 ../src/make_table.py cwlc_summary.json ../logs/wlc2_crosscheck/wlc2_*.log > table4.md
    python3 ../src/crosscheck_nonlc.py ../.. ../logs/cwlc_n2[6-9].log ../logs/cwlc_n30.log
    python3 ../src/forest_nonlc.py 31 ../logs/cwlc_n2[6-9].log ../logs/cwlc_n3[01].log
    python3 ../src/reverify_examples.py ../logs/cwlc_n2[6-9].log ../logs/cwlc_n3[01].log
    python3 ../src/m1cert.py m1_certificate.json; python3 ../src/lemma_checks.py; python3 ../src/forest_drift.py
    python3 ../src/window_drift.py 1 400; python3 ../src/big_drift.py      # time-budgeted / seeded searches

The `wlc2` cross-check used `logs/wlc2_crosscheck/wlc2.c.used`: `./wlc2 n 1 0` for n = 4..24, and
`./wlc2 n 4 id` (id = 0..3) for n = 25..27.
