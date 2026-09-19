# ORIGINAL: scoped component-order reduction

## Original statement

For a finite, simple, undirected, unweighted forest F, let

    I(F;x) = sum_k i_k(F) x^k

where i_k(F) is the number of independent k-vertex sets. Erdős #993 asks whether the finite coefficient sequence is unimodal for every forest. Plateaus are allowed.

The unrestricted statement remains **NOT_CLOSED** in this branch.

## Scoped theorem accepted in this run

Let F be any finite forest. If every connected component of F has at most 30 vertices, then I(F;x) has a unimodal coefficient sequence.

Equivalently, if an unweighted forest counterexample to Erdős #993 exists, at least one of its tree components has at least 31 vertices.

## Inputs

The scoped theorem uses three inputs.

1. **Pinned external tree census.** The external project reports that every tree on at most 30 vertices is unimodal and that, up to isomorphism, exactly 149 of those trees have non-log-concave independence sequences: 2 of order 26, 19 of order 28, 7 of order 29, and 121 of order 30.
2. **Pinned external closure computation.** On those 149 sequences it reports: all 11,175 unordered pair multisets are unimodal; exactly 97 pair products are non-log-concave; all 10,823 one-tree extensions of those 97 pairs are unimodal; among them 111 satisfy the hereditary pair condition and all 111 are log-concave, so the hereditary risk set at level 3 is empty.
3. **Classical convolution facts.** A finite positive log-concave sequence convolved with another such sequence is log-concave (Hoggar, 1974). A finite nonnegative sequence with interval support is strongly unimodal iff it is log-concave; in particular, log-concave * unimodal is unimodal (Keilson--Gerber, 1971), after harmless normalization.

The external computation is pinned to `scinet-ai/math-number-theory@fafb35784d4235c9e5dd701fd3b2c1f4955ae9ec`. The source and exact count files are identified in `certificates/EXTERNAL_EVIDENCE.json`.

## Boundaries

This run does not assert that the external large computations were freshly rerun here. It audits their published source, exact summary and closure logic. It also does not establish the unrestricted all-forest theorem, `J_H`, `RSM`, or a top-level Lean formalization.
