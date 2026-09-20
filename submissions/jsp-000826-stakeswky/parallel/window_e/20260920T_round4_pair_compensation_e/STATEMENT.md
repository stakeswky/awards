# Window E Round 4: statements

ORIGINAL: every finite simple undirected unweighted forest has a unimodal independent-set sequence, allowing plateaus. NOT_CLOSED.

## E4-S-v1 — PROVED scoped theorem

For every forest F and j>=0, group ordered independent-set pairs by intersection C and symmetric difference D, with actual C independence, C-D nonadjacency and 2|C|+|D|=2j. Let g(D) be the count at sizes (j,j) minus the count at sizes (j-1,j+1).

A high component of F[D] has bipartition-side difference at least two. It is splittable if some leaf w IN THAT COMPONENT with neighbor v leaves only gap-zero/gap-one components after deleting v,w.

The signed sum S_j over the UNION of (i) all high components are four-vertex claws, and (ii) exactly one high component, which is splittable, is nonnegative. Count the overlap once. Other balanced/unit components and original-graph exteriors are arbitrary. Size and index are unrestricted.

The proof uses actual cross-group matchings, an all-parameter Catalan capacity bound, and a contracted-forest incoming-multiplicity bound. A complete 165-case base is connected to a written proof of the infinite remaining range. It does not assume every group nonnegative.

## E4-L-v1 — UNPROVED sufficient candidate

Set Delta_k=p_(k+1)-p_k. History(F,k) means some i<=k has Delta_i<0 and every Delta_i through Delta_k is nonpositive. Compute h=floor(M(n-1)/(4M-2))+1 and beta=ceil(alpha(n-1)/(n+alpha)) on the complete forest.

Candidate: every HEREDITARY F and h+1<=j<beta with History(F,j-1) satisfy L_j>=0. HEREDITARY means every proper induced subforest is unimodal. A proof would rule out the first rebound of a minimum counterexample. Negative L_j without a complete descent-then-rise refutes only this stronger candidate, not ORIGINAL.

E4-S does not establish E4-L. No complete Lean theorem, build, axiom audit, external peer review or global novelty claim.
