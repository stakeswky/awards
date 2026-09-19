# Phase 7: inverse-cut counterexample search

**ORIGINAL NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** No legal non-unimodal forest, no positive residual-corridor test, and no universal elimination were obtained. This is a completed finite directed search, not a proof of the conjecture or a new all-forest verification bound.

## Definitions

For a finite simple undirected unweighted forest F, let P_k count independent k-vertex subsets. Unimodality allows plateaus. Its failure is exactly a pair i<j with P_(i+1)-P_i<0<P_(j+1)-P_j. Every whole sequence is tested through its last positive coefficient; appending zeros cannot create a later rise. Isolated vertices and disconnected forests are permitted.

For every actual vertex v, A_v=I(F-v) and B_v=xI(F-N[v]), including all other components. LOCAL means all these polynomials are unimodal. Under LOCAL, with full mode intervals [ell,r], define U=max_v min(r_Av,r_Bv) and D=min_v max(ell_Av,ell_Bv). The inherited sign bounds force a true valley to lie in U<=i<j<D. D-U>=2 alone is not a counterexample. HEREDITARY concerns every proper induced subforest and is not inferred from LOCAL.

## Exact operations targeted at the unresolved edge-cut bridge

All X/Y below count absent/present root states in actual components, with a selected root already contributing x.

### Add one bridge

For disjoint actual trees S,T and marked vertices s,t, set C=B_s(S)B_t(T). Adding edge st deletes exactly the independent sets selecting both endpoints. Hence

    P_join = P_S P_T - C.

Thus a true valley at i<j is equivalent to

    Delta C_i > Delta(P_S P_T)_i,
    Delta C_j < Delta(P_S P_T)_j.

This directly reverses the previous cut problem; it does not replace exterior components by arbitrary arrays. Graph construction, rooted DP and vertex-deletion recurrence independently verify each accepted complete polynomial. Coefficientwise C>=0 does not order its adjacent differences.

### Preserve vertex count by a wedge slide

In an actual path u-v-w, delete v-w and add u-w. No loop, duplicate edge or cycle is created, because the original graph is a forest. Cutting u-v and v-w exposes components U,V,W rooted at u,v,w, and an unchanged factor R for any other components. Counting independent sets on the two three-vertex core patterns gives

    P_slide - P_original = R Y_W (X_U Y_V - Y_U X_V).

Indeed the original core has v absent or present, and the new core has u absent or present. Common terms cancel, leaving the displayed signed difference. Each factor comes from the same actual graph. The sign of this polynomial, or of its differences, is not assumed. The identity was checked on every accepted graph of the direct slide lane. All indices and valleys are recomputed after the operation; the old valley location is not imposed.

## Exact search scores, not replacements for the target

For a positive-support sequence p, put g_k=(p_(k+1)-p_k)/(p_(k+1)+p_k). The first score is

    nu(p)=max_(i<j) min(-g_i,g_j).

An exact rational running-maximum scan evaluates it. Nu>0 is equivalent to a true valley; nu=0 is not a counterexample. Multiplication by the graph's order is used only to rank search seeds across different sizes. It is not a probability or a mathematically calibrated distance to a counterexample.

A second lane targets all vertices at once. Let

    e_i=min_v max(-g_i(A_v),-g_i(B_v)),
    l_j=min_v max(g_j(A_v),g_j(B_v)),
    rho=max_(i<j) min(e_i,l_j).

Zero-over-zero terms are assigned zero. Under LOCAL, rho>0 makes every vertex have a strictly descending conditional at i and a strictly ascending conditional at j. Unimodality forces these to be opposite conditionals. Therefore U<=i<j<D. This is only a sufficient auxiliary condition, not an equivalence and not an original counterexample. For selection only, rho is evaluated in a six-difference window near the whole-sequence peak. That heuristic never restricts the full P valley scan or the exact all-vertex U/D computation. All graphs, including failures of the auxiliary score, keep their complete original-problem test.

## Fixed finite surfaces actually completed

The 20 actual-tree bank includes the six connected Phase-6 fixed seeds, three specified bush trees, nine specified deeper spherical trees, and two specified tail-asymmetry transfers. The deeper spherical shapes are motivated by Galvin's discussion of multiple log-concavity failures (arXiv:2502.10654v2); no novelty is claimed for those constructions. The bank is not an exhaustive order census. Root classes are actual rooted-tree isomorphism classes, not equal-polynomial classes: a rooted isomorphism extends to the same completed bridge graph, including all internal vertices. Every pair satisfying the declared order limit and the selected non-LC-factor heuristic is checked at every pair of root classes. Omitting pairs of two LC trees is a directed choice, NOT a theorem about their bridge joins.

* Bridge lane: 7,111 distinct joined trees, maximum order 248. The declared limit is 250, not a claimed achieved order. Three bank pairs exceed that limit and 91 other bank pairs are omitted because both input trees are LC.
* Direct slide lane: all wedge slides of 24 selected seeds over three rounds of width eight. There are 20,690 marked operations but only 942 new isomorphism types; the other results are duplicates or already present.
* Forest lane: every size-two and size-three multiset from 13 selected actual non-LC tree types: 91+455=546 forests, maximum order 525. There are 84 non-LC pairs and 371 non-LC triples all of whose pairs are non-LC. These are component-block conditions, NOT HEREDITARY certificates. This risk set does not close at level three.
* Corridor lane: after rescoring 166 existing D-U=1 records, all wedge slides of 12 selected seeds over two rounds of width six. There are 7,292 marked operations and 283 new types. Rescoring the initial 166 records is not new coverage.

Across the four files there are 8,882 distinct graphs, consisting of 8,336 trees and 546 disconnected forests. Five reproduce supplied Phase-6 graph controls, leaving 8,877 new relative to that supplied inventory only. Two of these are small-component-only controls already inside the conditionally excluded component-30 domain; they are not new remaining-domain exploration. No global novelty or full earlier-history deduplication is claimed.

Every complete P was independently recounted by rooted occupancy DP and vertex-deletion recurrence. All 2,739,450 vertex-conditional array occurrences were computed to obtain exact all-vertex modes, U and D. In 25 selected materials, all 8,490 A/B arrays were additionally recounted by the vertex-deletion algorithm. These material recounts overlap discovery; they are not extra graph coverage. Whole P and all vertex mode intervals are stored for every record; full A/B arrays are stored for the 25 materials and regenerated/hashes checked for other records. It would be incorrect to describe every one of the 2,739,450 arrays as independently recounted.

All 8,882 whole sequences are unimodal and LOCAL. D-U is 0 in 8,595 cases and 1 in 287. There are zero residual graphs, zero residual pairs, zero eligible nonvacuous RSM tests and zero original counterexamples. HEREDITARY stays UNKNOWN for every new record. No shrinking or global-minimality claim follows.

## Unchanged first gap

The previous conditional small-component normal form and its external dependencies are retained, not recomputed or weakened. The remaining domain still includes a single >=31 tree and arbitrary large components with at most two permitted small components. No proof bounds all large boundaries or eliminates the mandatory terminal structure. Finite failure to meet the displayed slope inequalities does not prove that no actual forest can meet them.

The first substantive missing arrow remains: actual mandatory structure plus all minimum-counterexample conditions -> a smaller non-unimodal forest or a contradiction, uniformly over all genuine exteriors. This run does not establish J_H, RSM, an all-forest finite UNSAT, any original Lean theorem/build/axiom audit, or independent external peer review. FAMILY work is inherited unchanged. No organizer or prize claim is made.
