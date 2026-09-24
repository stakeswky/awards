# Mode-alignment route to unimodality (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is **not** proved or refuted here. This run continues
`20260924T092515Z_centroid_n31_drift_strict_product`. PR #1 stays Draft; `RESEARCH_STATE.json` is not
modified. No novelty, priority or award claim is made.

## What this run does

It tests a sufficient condition for unimodality that mentions only unimodality and mode positions
of smaller forests, and no log-concavity:

- **Lemma 1 (aligned sum):** the sum of two unimodal sequences whose mode sets are at distance at
  most one is unimodal. **Corollary 2:** with I(G) = I(G - v) + x I(G - N[v]), a vertex v whose two
  pieces have mode sets at distance <= 1 (after the shift by one) makes I(G) unimodal.
- **Theorem 3 (reduction):** if every forest with an edge has such an aligned vertex, then every
  forest is unimodal. So the whole problem reduces to locating modes.

## Findings

1. **(MA) holds everywhere tested.** All 6,594,041 trees with 4 <= n <= 22 have an aligned vertex,
   always one of degree <= 3 (`src/modes.c`, exhaustive). All 35,704 forests of order <= 15 with an
   edge have one (`src/ma_forests2.py`). 140 random and structured trees with n <= 120 have one
   (`src/ma_random.py`).
2. **Mode shifts.** Deleting one vertex moves the mode set by -1, 0 or +1, never more; deleting a leaf
   moves it by -1 or 0. The +1 moves (deleting a vertex of degree 2..10 raises the mode) are exactly
   the alignment failures of leaf splits.
3. **Pendant-leaf lemma (S2), empirical:** attaching a pendant leaf to a forest moves its mode set by
   0 or +1. (S2) alone implies that every forest with a support vertex of degree 2 is unimodal
   (given the induction hypothesis). The remaining class, hub forests (every support vertex of
   degree >= 3), needs a differently chosen vertex; in the 21 trees of order <= 22 that have no
   aligned leaf, the aligned vertices are low-degree non-support vertices near the centre.
4. **The exact obstruction.** Unimodality of the pieces plus the mediant property only confines the
   mode of a forest to the hull of the two pieces' modes, which allows the +1 shift. The remaining
   content of (S2)/(MA) is one inequality between an increment and a decrement at one index next
   to the modes (NOTE, Section 5). So the route localises the quantitative core of the problem
   to a single local comparison; it does not remove it. The natural sufficient condition (local
   concavity of the smallest piece) is not uniformly available: the concavity radius of tree
   sequences is only about 0.2 sqrt(n).
5. **First-order data.** Deleting a vertex changes the mean number of addable vertices of a uniform
   independent k-set by at most +0.41 and at least -1.49 on the window (n <= 15); the maximum
   normalised LC margin on the window grows slowly (8.0 at n = 12, 10.2 at n = 24).

## Files

- `NOTE.md`: statements, proofs, tables, the obstruction analysis and the assessment of directions.
- `VERDICT.json`.
- `src/`: `modes.c` (exhaustive per-vertex alignment and mode shifts), `modelib.py`, `ma_forests.py`
  (tree generator and (T, R) pair scan), `ma_forests2.py` (all forests as multisets), `ma_random.py`,
  `meanlemma.py`, `cwlc_curv.c`, `cwlc_conc.c`, `ip.py`, `families.py`.
- `results/`: `modes_summary.json` (per order), `trees_without_aligned_leaf.json` (all 21 trees with
  per-vertex data).
- `logs/`: `modes_n{14..22}_{0..3}.log`, `ma_forests2.log`, `ma_random.log`, `meanlemma.log`,
  `curv.log`, `conc.log`.
- `MANIFEST.sha256`.

## Reproduce

    cd src && gcc -O2 -o modes modes.c && for i in 0 1 2 3; do ./modes 22 4 $i > ../logs/modes_n22_$i.log & done; wait
    python3 ma_forests2.py 15; python3 ma_random.py 5; python3 meanlemma.py 15
    gcc -O3 -fopenmp -o cwlc_curv cwlc_curv.c && ./cwlc_curv 24 4 | grep MARGIN
    gcc -O3 -fopenmp -o cwlc_conc cwlc_conc.c -lm && ./cwlc_conc 24 4 | grep CONCAVITY
