# Exhaustive mode-alignment check: trees to n = 26, forests to order 20 (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is **not** proved or refuted here. This run executes the two
computations recommended by `20260924T143534Z_mode_alignment_route` (extend the (MA) check to
n = 26 with the centroid enumerator, and to forests of order 18) and goes two orders further for
forests. PR #1 stays Draft; `RESEARCH_STATE.json` is not modified. No novelty, priority or award
claim is made.

## What was checked

A vertex v of a forest F is **aligned** if the mode sets of I(F - v) and x I(F - N[v]) are at
distance at most one. By Theorem 3 of the previous run, "every forest with an edge has an aligned
vertex" (MA) implies Erdős #993. This run verifies (MA), the pendant-leaf statement (S2) and the
single-deletion statement (S1) exhaustively on:

- **all free trees with 4 <= n <= 26** (`src/cma.c`, centroid enumeration of run
  `20260924T092515Z`; one deletion DP per vertex, since I(T - v) = I(T) - x I(T - N[v]); leaves grouped by
  support; `-DFULL` scans every vertex);
- **all forests of order <= 20 with at least two components and an edge** (`src/ma_forests3.py`).

## Results

- **(MA) holds for every tree with 4 <= n <= 26** (447,467,592 trees at n = 19..26 in this run; 4..22 previously). No tree without an aligned vertex exists in this range.
- **(S2) holds for every leaf deletion** (5,331,352,953 of them at n = 19..26): the mode set moves by -1 or 0, never +1, never -2. Consequently a leaf at a degree-2 support is always aligned.
- **(S1) holds for every vertex deletion at n = 20..26** (FULL runs): every single-deletion shift is -1, 0 or +1; the +1 shifts occur only for vertices of degree 2..13.
- Trees without an aligned leaf: 3, 11, 7, 7, 93, 23, 224, 335 for n = 19..26 (703 trees, all re-verified in Python with no discrepancy). All are hub trees; in 699 of them a degree-2 vertex is aligned. **hubs(6,3) (n = 25) has no aligned vertex of degree <= 3** (its hubs and centre are aligned), which refutes the sharper claim of the previous run.
- **(MA) holds for every forest of order <= 20 with at least two components and an edge** (1,923,150 forests).
- Cross-validation: tree counts equal A000055 at every order; for n = 14..22 the per-tree and per-leaf statistics coincide with the independent program `modes.c` of the previous run.

## Files

- `NOTE.md`: method, tables, cross-validation and scope.
- `VERDICT.json`.
- `src/`: `cma.c`, `summarize_cma.py`, `reverify_noleaf.py`, `ma_forests3.py`, `ma_forests.py`
  (tree generator), `modelib.py`, `ip.py`.
- `results/`: `cma_summary.json`, `cma_table.md`, `trees_without_aligned_leaf_n19_26.json`.
- `logs/`: `cma_n{19..26}.log` (fast scan, with every `EX_NOLEAF` tree), `cma_full_n{20..26}.log`
  (every vertex), `ma_forests3_18.log`, `ma_forests3_20.log`, `reverify_noleaf.log`.
- `MANIFEST.sha256`.

## Reproduce

    cd src && gcc -O3 -march=native -fopenmp -o cma cma.c && gcc -O3 -march=native -fopenmp -DFULL -o cma_full cma.c
    for n in $(seq 19 26); do ./cma $n 4 > ../logs/cma_n$n.log; done        # n=26: 925 s on 4 cores
    for n in $(seq 20 26); do ./cma_full $n 4 > ../logs/cma_full_n$n.log; done   # n=26: 1891 s on 4 cores
    cd ../results && python3 ../src/summarize_cma.py ../logs/cma_n*.log ../logs/cma_full_n*.log > cma_table.md
    python3 ../src/reverify_noleaf.py ../logs/cma_n*.log
    cd ../src && python3 ma_forests3.py 20
