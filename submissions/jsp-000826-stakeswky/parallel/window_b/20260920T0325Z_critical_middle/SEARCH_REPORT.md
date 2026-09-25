# Window B Round 2: critical middle search and real equality premises

**ORIGINAL = NOT_CLOSED.** No actual non-unimodal forest was found. No universal middle no-rebound theorem is proved. The two substantive outcomes are real interior-equality coverage and a verified, locally reduced, tail-only refutation of the actually published A2-C1 claim. The 239-vertex starting example is attributed prior work, not a discovery claimed here.

## Inputs and concurrency

The actual Round-2 task, A's entire prior proof, and both previous reports were read from the Project/Library. The prior B evidence archive was mounted and extracted read-only. Raw materialization of A's ZIP was denied; A's proof text was successfully read and is not described as missing. The initial live head was `1ff2fa87a0dac00947bad858229e7e5d0333760e`. A subsequently published `CLAIMS_FOR_B.md` at `05470e82d6a7460df0284b14f78b38710449d70e`; the entire A2-C1/A2-C2 requests were read and checked. A later head `7cecd22883fa337e5f389661428d7382a0da1394` and the unchanged claim blob `38eaa9926194035bb1f66afb3dc4afcac8a8cfeb` were reread after the main searches. Final publication uses a freshly read head, not these historical anchors.

The existing `forest_exact.py` and `independent_check.py` are reused byte-for-byte; the previous construction utilities are copied without code changes as `round1_search.py`. Only targeted diagnostics, constructions, reductions and audit drivers were added. The scoped write directory is `parallel/window_b/20260920T0325Z_critical_middle/`. No A file, historical package, top-level RESEARCH_STATE.json, main or live catalog is modified by B.

## The requested critical conditions

The following counts are on the union of stored graph records, deduplicated by exact forest AHU encoding. The separate complete small-forest equality census overlaps this union and must not simply be added to it.

| Condition | Actual coverage | Failures or qualifying cases |
|---|---:|---:|
| Middle LC positions h+1 <= k < beta | 57,039 positions | **0 negative minors** |
| Full PREFIX_BETA positions 1 <= k < beta | 202,247 positions | 0 negative minors |
| Actual strict-descent BARRIER premises | 16,035 positions | 0 next-step rises |
| Qualified equality p_k=p_(k+1), k+1<beta | **91 distinct forests / positions** | 91 next-step strict decreases |
| Qualified equalities after any prior strict descent | **0** | 0 |
| Equality followed by a rise without prior descent | **0** | 0 |
| Actual original descent-then-rise | Whole sequence of every completed graph | **0** |
| A2-C1 | 318,244 positions | 44 failing forests/positions, **all tail-only** |
| A2-C1 failure with k+1<beta | **0** | A2-C2 nonvacuous failure-history coverage **0** |
| Full-vertex LOCAL/U/D analysis | Five material forests | **0 residual position pairs** |

All 16,126 actual weak-descent/equality steps in the stored union have explicit signed numerators in `SIGNED_MIDDLE_BUDGETS.jsonl.gz`: both the current decrease and the next decrease use p_k as the denominator. There are no synthetic or floating-point equalities in this coverage.

## Real equality search

A deterministic census generated all unlabelled tree types through order 16, then all nondecreasing multisets of components with total order at most 16. It completed 85,625 forest records. Its purpose was equality, not additional large-graph sampling. It found 84 qualified graphs: 19 at order 14 and 65 at order 16. None occurred through order 13 or at order 15. This is a statement about the completed generated census and its implementation, not an unsupported all-order minimality claim.

The census also checked 90,901 middle LC positions, 3,927 strict-descent BARRIER positions, and 752,845 C1 positions, with zero relevant failures. Its 302 tail equality positions are reported separately and do not fill middle equality coverage. All 84 qualified graphs were independently recounted. Ordinary census graphs were not all recounted by a second algorithm.

Seven further distinct qualified examples come from explicit path and palindromic-polynomial families. Eight family graphs were counted, but one overlaps the small census. Their formulas and elementary equality proofs are in `EQUALITY_FAMILIES_PROOF.md`. These are useful exact controls, not original counterexamples and not a theorem classifying the unresolved forests.

A connected 14-vertex witness has

    P = (1,14,78,225,371,371,231,85,16,1),
    n=M=14, alpha=9, h=4, beta=6, k=4.

Thus p_4=p_5=371 and p_6=231, with 5<beta. There is no earlier descent. The full edge list is in `CRITICAL_CASES.json` and the evidence archive. Rooted counting, independent deletion counting and exhaustive subset enumeration agree. The path on 19 vertices independently gives p_5=p_6=3003 and p_7=1716, h=5,beta=7.

## A2-C1: prior witness, fresh verification, property-preserving reduction

The primary public repository `kylekaba/erdos-problem-993` already records the homogeneous bush B(8,14). Its README blob is `e6b4ef3540a09490be54e57fbccb4575498ac32c`. The actual unweighted tree was rebuilt with our existing generator and freshly counted by both algorithms. It has n=239, alpha=126, h=60,beta=83. At k=113, the C1 integer slack is strictly negative. The sequence is still unimodal.

Starting only after saving the original graph and every coefficient, 27 accepted vertex deletions reduced it to a connected **212-vertex tree**. Every accepted step was independently recounted. The final parameters are n=M=212, alpha=112,h=53,beta=73. Its C1 failure is at k=100, while its negative LC minor is at k=101. Both remain far into the tail.

There were 962 reduction proposals, 831 within-step isomorphic duplicates and 131 exact distinct-within-step trials. At the final graph all 13 distinct neighbors under single-vertex deletion, pendant-pair deletion or degree-two suppression were independently recounted; none preserved a C1 failure. This proves only local irreducibility under those operations, not global minimum. Original-candidate reductions are **0**, because there was no original failure candidate.

## Critical fixed-size comparisons

Two targeted lanes generated complete polynomials for 2,878 and 1,542 within-lane distinct forests. Their overlap is removed in the critical-condition table. The first lane used eight geometrically different seeds, including an existing 26-vertex external seed, unequal bushes, grafts, a two-component union and the C1 witnesses. Each seed had a 240-step fixed-n/fixed-k middle-minor trajectory and a 240-step non-LC-preserving trajectory. The latter optimized the absolute first-negative index, not just k-beta.

No fixed-order trajectory moved the first negative index left. The fixed-middle normalized minor n L_k/p_k^2 decreased on the selected comparisons, but remained positive. For example n=26,k=8 changed from approximately 7.66579 to 4.52446. This is an actual same-n/same-k comparison, not a claim of approaching a proved numerical threshold.

The separate six-trajectory, 600-step lane required an actual weak-descent premise at a fixed k and fixed n before accepting a move. It optimized the signed next decrease, not an unsigned distance from equality. No next increase was found. Every modified forest recomputed n,M,alpha,h,beta, retained all vertices/edges of its exterior, and received a complete exact original-sequence scan.

Path-attachment panels explain why the initial tail constructions did not supply middle failures: some additions removed the negative minor; others moved it right with the enlarged graph. On the 212-vertex seed, disjoint path extension from length 0 to 24 moved the first bad minor from 101 to 113 and beta from 73 to 81: the gap worsened from 28 to 32. The search therefore changed objective to actual descent-constrained fixed-size comparisons instead of merely accumulating these tail examples.

## Verification scope

The stored union has 4,632 distinct actual forests, 327,508 primary coefficient entries, and no canonical matches with the 1,546 previous B graphs. This does not establish newness against all older project packages. Its maximum order, 985, comes from a path equality control and is not a progress measure.

Every stored equality and C1-failure graph, and every fixed-comparison start/best, was freshly dual-recounted in the audit: 154 distinct graphs and 7,893 coefficients. Including the ten earlier dual-recounted tail controls gives 164 distinct stored graphs and 7,943 coefficients independently checked at least once. **Not all 4,632 ordinary graph arrays received an independent recount.**

Five graphs of orders 14,19,16,212,239 received full A/B profiles at every vertex, with 1,000 independently recounted A/B arrays and 109,175 coefficient entries. All five are LOCAL, and both raw and refined residual-pair counts are zero. No HEREDITARY conclusion is inferred. Three small material graphs were additionally checked by enumerating all 606,208 vertex subsets in total, giving 33 complete coefficient entries and actual residual-graph moment distributions.

An exact root-state calculation on B(8,14) retains all 238 edges, grouping only three isomorphic induced residual graphs that were independently counted. At k=113, mean availability is about 0.34012 and variance 0.97471. Within-state variance contributes 0.42371, between-state mixing 0.55100. The hub-present phase contains 2^112 independent sets and has no available vertex; it ends at that support index. This provides an actual mixing obstruction to the stronger C1 bound, while staying far below the threshold needed for an original rise. Exact integers and fractions, not decimals, determine the signs.

Final deterministic replay and publication receipts are separate machine-readable files. No Lean build, axiom audit, external peer review or original completion is claimed.
