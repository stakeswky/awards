# Sources, recovery and dependency boundaries

## Actual repository recovery

Observed initial remote HEAD: b71e0e5c87b7da24980af0f4cc73f2fc34593f11.
Branch: jsp-000826-research-snapshot; PR #1 was open, Draft and unmerged.
Main/base SHA: f4e7173d89dfe91022a185427d63452c8ffbf6ae.
RESEARCH_PROTOCOL and the complete RESEARCH_STATE were read from this pin.
The reconstructed state bytes match blob 90d469db9e34881a7f77f0844a005711c51552be.
Prior phase statements, proof attempts, GAP and reviews were consulted from
this conversation and the mounted Phase6/Phase7 delivery archives.

The prior engine.py and forest_exact.py are reused unchanged, with exact
source hashes recorded in AUDIT/CLEAN_REPLAY. The Phase7 bank is actual graph
data, not a collection of arbitrary polynomial messages. The four prior raw
coefficient streams are reread only for positional auditing and exact graph
identity exclusion; no claim of freshly repeating Phase7's DP is made.
The earlier position-audit JSON is retained as a cross-check, not authority
in place of the actual coefficients. Its two counts (8,882 and 6,818) were
rederived from the complete streams.

## External mathematical inputs (primary sources, HTML inspected)

1. Abdul Basit and David Galvin, On the independent set sequence of a tree,
   Electronic Journal of Combinatorics 28(3) (2021), P3.23;
   arXiv:2006.12562v2 (July 3, 2021).
   https://arxiv.org/html/2006.12562
   Theorem 1.2 recalls Levit--Mandrescu's decreasing tail for
   Konig--Egervary graphs, explicitly including forests. Theorem 1.3 gives
   beta=ceil(alpha(n-1)/(n+alpha)) for EVERY graph. Section 2.1 proves it
   using Fisher--Ryan and Zykov inequalities. We use this established result,
   not the separate random-tree asymptotic results in that paper.
2. Grace M. X. Li, Unimodality of independence polynomials of two family
   of trees, arXiv:2603.03025v1 (March 3, 2026).
   https://arxiv.org/html/2603.03025v1
   Theorem 2.10 states the older tail bound. Restricted-family arguments
   motivate combining prefix LC with a decreasing tail; no general forest
   prefix theorem is imported or attributed to that paper.
3. David Galvin, Trees with non log-concave independent set sequences,
   arXiv:2502.10654v2 (January 23, 2026).
   https://arxiv.org/html/2502.10654v2
   Provides context for multiple tail log-concavity failures, not an
   unrestricted single-peak theorem. Existing tree families are not claimed
   as inventions of this run.

The proofs of the prefix implication, pair partition, star obstruction,
k=2 estimate and sparse initial-range estimate are given in PROOF_ATTEMPT;
they are not inferred from these sources or finite data. No exhaustive novelty
search has been performed, so there is no first-discovery claim.

## Retained external component-30 computation

scinet-ai/math-number-theory@fafb35784d4235c9e5dd701fd3b2c1f4955ae9ec remains
the pinned input to the earlier component-30 closure and 247-small-index
normal form. Neither its full census nor complete H2/H3 is rerun here. Its
scope does not bound the count, order, or external boundary of large
components. The present direct graph counts do not depend on accepting that
census. No changes to FAMILY, ORIGINAL formalization, or prize records.

## Execution and hosting

No paid API, user machine, new cloud service, or unattended future worker was
used. All computations ran in the current container. The container's direct
network route was unavailable; connected GitHub reads/writes worked. No
claim of a locally cloned remote repository is made. Git writes preserve the
read base tree and use a non-force child update only after rechecking HEAD.
Full arrays/logs are in the delivery ZIP. Compact Git files identify exactly
which bytes are hosted and which are regenerated. OpenAI ChatGPT assisted
this run; review is same-model self-review, not external peer review.
