# Fixed diagnostic plan, before execution

Primary aim: ORIGINAL via a minimum-order counterexample, actual all-vertex
splits, and the remaining first-difference interval. No B59 extension.

Claims tested (not assumed):
L: if all 2n specified deletion polynomials are unimodal, some vertex has
conditional mode-interval distance at most one.
J: under the same LOCAL premises, D <= U+1.
Both are stronger than claims restricted to a globally minimum counterexample.
A local-premise witness cannot refute the stronger minimality-premise assertion.
Also test proposed leaf/edge sign obstructions derived in PROOF_ATTEMPT.md.
Every whole/conditional polynomial is checked for ORIGINAL directly.

Fixed scope: exhaustive labeled simple graphs of orders 0..5, rejecting cycles;
these are algorithm regressions, not a new research coverage claim. Deterministic
stress inputs: the stored 25/30 controls; subdivided-star bushes c=1..6,m=1..8;
64 seeded recursive trees n=12..75, and their 64 independently edge-deleted
forests; paths/stars at orders 2,3,4,8,16,32; three disconnected control unions.
Seed 99320260918. No claim of isomorphism deduplication or random completeness.

One dedicated fixed structural follow-up may be designed if a concrete gap or
counterexample is located; it must be logged before computation and have a
separate budget. Never increase the same sample budget after no candidate.

Resource limits: initial diagnostic suite 120 seconds, <= 512 MB intended
working memory, <= 200 vertices per stored input. Any single graph exceeding
10 seconds is recorded as excluded, not silently counted. Material witnesses
require a full second-algorithm replay of all 2n+1 polynomials before use.
Stop unrelated scans immediately on a whole or conditional ORIGINAL candidate.

Two independent combinatorial algorithms: rooted forest absent/present DP and
vertex/closed-neighborhood deletion recursion, with independent multiplication
implementations. Compare every integer coefficient including zero padding;
validate a0=1, a1=n, a2=binomial(n,2)-|E|. Third subset enumeration on n<=5.
Record graph edges, n, degrees, full mode intervals, all U/D inputs, actual
first differences, all failures, completed/excluded coverage, and commands.
Final evidence must be replayed from a clean source copy with full output
comparison, not merely matching hash or mode. No external services or paid API.

## Fixed follow-up after the concrete findings

No enlargement of the 193-graph search. Recount the material tree-11 witness,
old25/new30, and the hand-specified 7-vertex star. On the star, test the proposed
unlocalized opposite-slope minor at i=1,j=2; inspect every induced mask by all
three algorithms. Also inspect two explicitly ABSTRACT sequence controls:
C=[1,6,7,8,9,8,1], H=[1,4,1] for shape-only leaf smoothing; and
E=[3,2,1], L=[1,4,8] to distinguish a negative minor from an actual valley.
These are not asserted to be graph-count sequences. Follow-up budget 20 seconds.
No greedy minimization, further random sampling, or global minimality claim.
