# Fixed Phase-3 diagnosis, before new execution

The primary claim is J_H: for a nonempty unweighted simple forest with no isolated
vertex or K2 component, HEREDITARY implies D<=U+1. This is NOT assumed. A true
valley remains the direct ORIGINAL target. RSM keeps its original quantifiers.

1. Reuse the exact Stage-2 forest DP/deletion counter, after reading source and
   matching Git blob identities at the actual baseline. Preserve old controls
   tree-11, old25, new30, and star7 separately from new graphs.
2. New objects are deterministic joins of two rooted bushes across an INTERNAL
   edge or a subdivided internal path. Six side types, parameter pairs
   (leaves per branch, branches) = (1,2),(2,2),(2,4),(3,3),(4,4),(6,6).
   Each branch is a star rooted at its center. For every unordered pair of types,
   connect roots by paths of length 1 and 3. Retain all 42 actual graphs.
   For each same-type length-1 join, also retain its disjoint union with P3 and
   with the old30 control. These 12 graphs test the noncancellable common R.
   Two small internal-edge controls (P4 and the double-star with two leaves at
   each endpoint) exercise full induced-subset coverage. No random seed is used.
3. Recompute the complete whole/A_v/B_v/C_uv coefficients by forest DP AND
   independent vertex deletion. Verify every full-edge partition and the rooted
   R*X_u*X_v, R*Y_u*X_v, R*X_u*Y_v formulas. Record modes only for unimodal
   sequences, n, edges, components, all coefficients, U,D, and actual residual
   pairs. Stop unrelated new cases if any ORIGINAL candidate occurs.
4. Whole/A/B checks establish only LOCAL. On the controls and new graphs of
   order <=12, check all proper induced subsets by exact rooted-signature DP.
   Also attempt that complete coverage on tree-11 (order 23); a cap or timeout
   yields UNKNOWN, never HEREDITARY. The coverage proof and multiplicity sum
   must accompany any positive certificate. It is not a global-minimality test.
   Every distinct retained signature is recounted independently on its witness
   mask, with brute independent-subset enumeration on graphs of order <=7.
5. Separate counts: inherited controls, new graphs, LOCAL, fully HEREDITARY,
   D>=U+2, residual pairs, RSM tests with LOCAL only, RSM tests with all original
   premises, and actual whole or induced ORIGINAL candidates. A pair is tested
   against every leaf; it refutes RSM only if every leaf fails and all premises
   are established. No residual pair means exactly zero nonvacuous tests.

Limits: <=60 graphs as specified (no extension after an empty result), <=120
seconds for the all-edge batch, <=10 seconds per graph; <=30 seconds and 100000
intermediate signatures for each hereditary attempt. All arithmetic is exact.
If a limit is hit, preserve completed coverage and explicit exclusions. Store
full material coefficients with a lossless tuple table. Re-run final sources
in a clean temporary directory and compare the entire deterministic output.

These computations do not prove a universal inequality. New edge sign
identities, shape-only examples, or more files cannot justify GAP_REDUCED.
