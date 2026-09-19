# Stage 5 ORIGINAL: component-order-30 closure audit

Date: 2026-09-18.

This bounded run audits and imports a pinned external reduction relevant to Erdős Problem #993. It does **not** claim a new exhaustive enumeration and it does not close the unrestricted forest problem.

## Result

Using the pinned SciNet/Roman Labs computation and the classical convolution theorems of Hoggar (1974) and Keilson--Gerber (1971), the following scoped statement is accepted for use in this research branch:

> Every finite unweighted forest whose tree components all have at most 30 vertices has a unimodal independent-set sequence.

Therefore any counterexample to the unrestricted forest statement must contain at least one tree component on at least 31 vertices.

The external computation is pinned to `scinet-ai/math-number-theory@fafb35784d4235c9e5dd701fd3b2c1f4955ae9ec`. This run did not rerun the 52,068,524,664-forest sweep, the 23,522,619,475-tree sweep, or the 21,998 closure products. Those remain external computational evidence. The external finding reports an independent reproduction dated 2026-08-04. A stale absolute path in one auxiliary verification script is recorded there as a reproducibility fault, not a mathematical contradiction.

## Files

- `STATEMENT.md`: exact scoped theorem and boundaries.
- `PROOF.md`: reduction and minimal-counterexample closure argument.
- `REVIEW.md`: same-model audit of the imported result and its hypotheses.
- `VERDICT.json`: machine-readable status.
- `src/check_summary.py`: a small fresh transcription-consistency checker.
- `certificates/TRANSCRIPTION_CHECK.json`: its actual output.
- `certificates/EXTERNAL_EVIDENCE.json`: pinned external sources and counts.
- `certificates/HASHES.json`: SHA-256 hashes of this package before state update.

The fresh checker only verifies copied integer relations and evidence metadata. It does not independently recompute the external graph enumeration.

## ORIGINAL boundary

The unrestricted Erdős #993 forest statement is still **NOT_CLOSED**. The existing `J_H` and `RSM` structural routes remain unresolved. This scoped component-size reduction does not prove either one and is not a Lean theorem.
