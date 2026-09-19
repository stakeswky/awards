# Phase 10 internal review and repairs

Review: **SAME_MODEL_SELF_REVIEW**, not a second model, mathematician or external
peer reviewer. Distinct exact algorithms and fresh execution are not peer review.

## Mathematical verdict

Accept PROOF.md Theorem 3.1 and its explicit all-parameter corollaries, with
the stated vertex-cover and private-arm conditions and the known tail theorem.
The unrestricted original target is not proved. The new theorem removes a
specified unbounded whole-forest class, including non-LC component products;
it does not bound or classify every remaining actual forest.

## Critical scope checks

- Every core edge meets H. An uncovered external edge makes the formula
  invalid; regression rejects that configuration. H need not be independent.
- S ranges over ACTUAL independent subsets of H. Every uncoated core vertex
  and every other component remains in W or H. The term d(S) forbids precisely
  the available original neighbors, not arbitrary synthetic coefficients.
- A private arm has two new vertices and two edges. Selected hubs allow the
  far vertex, not the near vertex. Thus alpha=M+alpha(C) is exact.
- No unimodality of the original core or root-absent part is assumed. This
  removes the unproved shape premise that blocked a naive Phase9 extension.
- The middle bound uses l=k-s-j>=M/3, justified by M>=24q. The upper index
  beta<=3M/4 includes both endpoints of every needed difference.
- The error bound is coefficientwise in the required interval. It is not a
  total mass estimate misapplied at an arbitrarily small tail coefficient.
- The denominator D_k in (4.5) is a COMMON denominator; a nonzero integer
  numerator has magnitude at least one. There are 1,218 exact denominator
  checks, including four zero-difference/plateau occurrences.
- Q is strictly LC, so at most one difference equals zero. Leaving that one
  undecided is safe only because earlier signs are positive and later signs
  negative. The known tail covers all later coefficients of the ACTUAL graph.
- The equal-arm bound treats a not divisible by six using floor(a/6) and
  a<6(z+1). The decreasing z^d 2^(-z) estimate and endpoint inequality cover
  every larger integer; finite checks do not supply the unbounded quantifier.
- Multiple non-LC components are proved only in the stated complete-core
  regime. It is never assumed that arbitrary unimodal products are unimodal.
- A good graph formed by adding arms is not a reduction of a bad undecorated
  core. There is no completed minimum-counterexample elimination.

## Computation and counting checks

233 search records are distinct by full canonical strings, not polynomial
hashes alone. The arbitrary-tree representation is not an exhaustive census.
There were 251 proposals, 18 repeated types, 119 distinct subtree-relocation
operations; no over-cap proposal and no historical overlap. History was checked
against the supplied Phase7/8/9 inventory only, not all sessions or literature.

Every whole P has independent rooted and vertex-deletion recounts. Every
vertex A/B was computed (83,710); only 12 materials have a second recount of
all 5,920 A/B arrays. Their 2,930 edge-neighborhood counts verify global
availability moments. All 1,240 middle weak-descent indices are checked by
complete coefficient comparisons, not all by full variance-distribution
recounts. U/D residual pairs and true valleys remain zero. New HEREDITARY
is UNKNOWN, even for the four much larger theorem controls.

The four theorem controls have complete polynomials recomputed by actual
core-subset expansion, rooted DP and vertex deletion. They are distinct from
and not added as disjoint historical novelty to the 233-search count. The
largest is 4,616 vertices, two non-LC components of 2,308 each. These controls
do not constitute an order bound. Root/availability mixture identities are
checked on five materials; their fine root-state moment split is not claimed
independently recounted on large graphs. Literal small-subset/root checks
number 10,626; the tiny decorated-graph subset check adds 128 separate controls.

## Repairs retained

The first regression source had `==not u`, a SyntaxError caught by py_compile
before running that file. It was changed to `==(not u)`. The original source
and compile-failure note are in delivery provenance. No mathematical result
was produced by the failed compile attempt. Final regression execution passes.

The search initially read the historical inventory as a generation filter.
It had zero historical hits. To make the mathematical search independently
reproducible without old raw files, the final version separates this comparison
into history_audit.py. The complete final search was rerun; counts and graph
content are unchanged. The first source/log remain in delivery provenance.
The final replay uses final source; no fields are excluded from comparison.

## Fresh replay and publication

Six programs ran from a newly created temporary directory. All ten complete
outputs matched byte-for-byte, including large polynomial/material arrays.
Actual exit codes, duration, platform, source/input hashes and cleanup outcome
are in CLEAN_REPLAY. No archived receipt substitutes for this execution.

Publish only beneath submissions/jsp-000826-stakeswky. Re-read the live branch
before a non-force update, preserving concurrent work. PR #1 must stay Draft,
main unchanged. A post-write delivery receipt records real publication;
repository CI is not mathematics. No Lean build or axiom audit was run.
