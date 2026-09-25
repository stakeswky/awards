# Attempt on the remaining gaps: reduction to window log-concavity (independent Claude window)

**ORIGINAL=NOT_CLOSED.** The core inequality is not proved for general orders. This run records
proved reductions, a machine-checked formal reduction, exhaustive computations through n=29, and
the exact remaining proposition. No novelty, priority or award claim is made. PR #1 stays Draft;
the shared `RESEARCH_STATE.json` is not modified.

## Main points

1. **Reduction (written; formalized).** Let (W) be log-concavity of p on the window
   [ceil(n/4), ceil((2 alpha - 1)/3)]. Then (W) implies unimodality for every forest.
   - `lean/WindowReduction.lean` builds on the external FLNYZ Lean development at `b2a1d3e`.
   - It proves `isUnimodal_of_windowLC`, `erdos993_of_windowLC` and `erdos993_of_windowLC_below`.
     The last says: there is N0 such that `WindowLC` for all forests of order < N0 implies
     Erdős #993 for all forests.
   - Axioms: `propext`, `Classical.choice`, `Quot.sound` only.
2. **G2 (plateaus)** is subsumed by (W). An anchor lemma also covers plateaus inside any payment
   scheme.
3. **G3 (forests).** By Hoggar and Keilson–Gerber, only forests with at least two
   non-log-concave components (>= 52 vertices) are not reduced to trees.
4. **Exhaustive computation.** All 8,691,747,673 trees with n <= 29 are unimodal and strictly
   log-concave on the window. There are 28 non-LC trees (orders 26, 28, 29), and every break lies
   at >= 0.9286 alpha. All 59 forests of order <= 29 with a non-LC component also pass.
5. **What remains.** (W) for forests of order 30 <= n < N0; formally, `WindowLC` below N0. This
   is the negative answer to Galvin's Question 3.1 (arXiv:2502.10654), restricted to the window.

## Files

- `PROOF_ATTEMPT_G1_G2_G3.md`: statements and proofs (Theorems 1–6), failed routes, evidence
  tables, literature context, and the exact open statement.
- `lean/`: `WindowReduction.lean` (copy into `ErdosProblem993/` of the external repository at
  `b2a1d3e`, then run `lake build ErdosProblem993.WindowReduction`) and `WindowReductionAxioms.lean`.
- `logs/`:
  - Lean build and axiom outputs;
  - `EXHAUSTIVE_RUNS.json`: per-order counts, exit codes, times and source hashes;
  - `rerun/`: outputs of every console-only experiment, re-run from the published sources;
  - logs of the Python reference sweep.
- `src/`:
  - `wlc.c`, `wlc2.c`: C exhaustive checkers; `wlc2` adds the window-equality count;
  - `run_wlc.py`, `run_wlc2.py`: drivers;
  - `e993lib.py`, `families.py` and the experiment scripts;
  - `rerun_console_experiments.sh`.
- `results/`: JSON outputs, including every non-LC tree found with n <= 29 (level sequences and
  full integer sequences).

## Reproduce

- **Exhaustive runs:** `cc -O2 -o wlc src/wlc.c && python src/run_wlc.py 21 29 10`. This takes
  about 20 minutes on 10 cores. For strict equality counts use `wlc2`/`run_wlc2.py`.
- **Cross-check:** C and Python agree exactly on coefficient checksums over all trees for
  n in {5,10,14,16,18,20}.
- **Scope:** these are new independent implementations. They are neither author-program replays
  nor peer review.
