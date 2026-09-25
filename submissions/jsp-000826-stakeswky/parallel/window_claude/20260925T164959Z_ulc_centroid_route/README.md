# A centroid route past n = 34 without enumeration: ultra-log-concave branches (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is **not** proved or refuted here. This run records a possible
route beyond the exhaustively verified range (every forest of order <= 34, run
`20260925T090935Z`) that needs no enumeration of large trees. It depends on one lemma that is
**conjectural**: it survives adversarial numerical search, but it is not proved. PR #1 stays Draft;
`RESEARCH_STATE.json` is not modified. No novelty, priority or award claim is made.

## Results

1. **Ultra-log-concavity of small trees (verified).** Every tree of order 4..23 and 25 has an
   ultra-log-concave (ULC) independence polynomial, k p_k^2 >= (k+1) p_{k-1} p_{k+1}. Exactly one
   tree of order 24 fails, only at k = alpha - 1, and it is still LC there.
2. **Lemma U (conjectural).** Take d >= 2 centroid branches, with f_i = g_i + x h_i as in
   `NOTE.md`, h_i <= g_i coefficientwise, and g_i, h_i, f_i all ULC. The lemma says
   prod f_i + x prod g_i is unimodal. Adversarial hill-climbing finds no counterexample; the best
   configurations stay 6 to 9 % away from a dip.
3. **Conditional consequence.** If Lemma U holds, every forest of order <= 47 is unimodal. This
   would extend the unimodality range from 34 to 47. It would not give the strict window LC used by
   the Lean reduction.
4. **Negative results.** Three weaker or unstructured variants are false, with explicit
   counterexamples:
   - log-concavity with a coefficientwise sandwich;
   - Lemma U with LC in place of ULC;
   - ULC without the per-branch structure, even with a coefficientwise sandwich,
     d = F_1 - G_1 and alpha >= order/2.

   Both the ULC hypothesis and the branch structure are needed.

## What remains

Lemma U needs a proof (`NOTE.md`, Section 4 sketches the obstacles). Even with it, 48 <= n < N0
stays open, so this is not a route to a complete proof on its own.

## Files

- `NOTE.md`, `VERDICT.json`, `MANIFEST.sha256`.
- `src/`:
  - `ulc_vec.c` (exhaustive ULC check; `cwlc_vec.c` with the ULC test);
  - `ulc_trees_py.py` (independent Python check), with its helpers `ma_forests.py`, `modelib.py`
    and `ip.py`;
  - the lemma searches `lemma_search.py`, `lemma_search2.py`, `lemma_climb.py`,
    `lemma_climb_ulc.py`, `lemma_climb_ulc23.py` and `lemma_fg.py`, run by `run_lemma_logs.sh`;
    `lemma_fg_sandwich.py` and `lemma_fg_sandwich_bip.py` (seeds 1..4, run directly).
- `logs/`:
  - `ulc_n4..25.log`, `ulc_summary.log` and `ulc_trees_py.log`;
  - one log per lemma search and seed.
