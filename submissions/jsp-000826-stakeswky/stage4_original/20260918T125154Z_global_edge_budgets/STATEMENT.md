# ORIGINAL: global edge budgets and exact residual counts

**NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** No ORIGINAL proof or legal counterexample is produced. The first missing universal connection has not been reduced. New identities and necessary budgets below are not a substitute for that connection.

## Definitions and premises
A forest F=(V,E) is finite, undirected, simple and unweighted, with no cycle. Disconnected forests, the empty forest and isolated vertices belong to ORIGINAL. Write n=|V|, m=|E| and P_k for the number of independent k-subsets; P=I(F;x), P_0=1, and retain all coefficients through n, with zero extension outside. Unimodal means weakly increasing through one maximum interval and weakly decreasing afterwards. A counterexample must have indices 0<=i<j<n with Delta P_i<0<Delta P_j, where Delta Q_k=Q_(k+1)-Q_k.

LOCAL: every I(F-v) and I(F-N[v]) is unimodal. HEREDITARY: every proper induced subforest is unimodal. GLOBAL-MINIMAL: a hypothetical counterexample with every smaller-order forest unimodal. LEX-MINIMAL additionally minimizes |E| among counterexamples of that least order. Only LEX-MINIMAL => GLOBAL-MINIMAL => HEREDITARY => LOCAL is used. Edge deletion needs LEX-MINIMAL; contraction needs GLOBAL-MINIMAL, not induced-subgraph status.

Let A_v=I(F-v), B_v=xI(F-N[v]), with P=A_v+B_v. Under LOCAL use complete mode intervals [ell_Av,r_Av], [ell_Bv,r_Bv], and set U=max_v min(r_Av,r_Bv), D=min_v max(ell_Av,ell_Bv). These extrema are only defined for nonempty F. The read and checked Stage-2 reductions give nonnegative differences below U, nonpositive differences at/above D, and unimodality when D<=U+1. A minimum counterexample has neither isolates nor K2 components; every actual valley lies in U<=i<j<D. Connectedness is not assumed.

For each edge e=uv set C_e=I(F-{u,v}), H_e=I(F-(N[u] union N[v])), Z_e=x^2 H_e. The inherited full counting identities and mixed-edge disjunction remain unchanged; no disconnected factor is canceled in coefficient comparisons.

## Newly written scoped deductions
PROOF_ATTEMPT gives proofs, independent of the numerical tables, of:

* Exact degree-weighted endpoint slack and three coefficient-level valley budgets, followed by legitimate sums over edges and vertices.
* W_k=sum_e (Z_e)_k counts k-subsets inducing exactly one edge. For k>=2, W_k=(k-1)P_(k-1)-K_(k-2), where K_r sums component counts of F-N[S] over independent r-subsets S. A second available-pair identity and a blocked-extension/star budget are proved.
* For every nonisolated v, x product_(e incident v) C_e = B_v A_v^(d(v)-1). For a nonempty isolate-free forest with c components, product_e C_e=P^(c-1) product_v A_v^(d(v)-1). These retain complete real-forest products and all other-component factors.
* Leaf/support slope consequences and a telescoped endpoint budget; deleting or contracting a leaf edge adds no independent minimality information beyond the smaller leaf-deleted forest.
* An exact candidate linear functional for the flow attempt. It does not provide a valid directed-growth contradiction.

These do not prove J_H, RSM, or impossibility of all simultaneous residual configurations. The degree-weighted identities do not turn average degree <2 into a sign bound on weighted slopes. Coefficient budgets may not be differenced as inequalities.

## Unresolved sufficient routes, unchanged quantifiers
J_H: every nonempty isolate-free forest with no K2 component satisfying HEREDITARY has D<=U+1.

RSM: for every nonempty isolate-free HEREDITARY forest and every U<=i<j<D, some leaf l with support w blocks that pair. Put C=I(F-{l,w}), H=I(F-N[w]), X=(1+x)C, Y=xH. The blocking test is that neither ordering (E,L) is polarized, or the polarized ordering has
Q=Delta L_i*(-Delta E_j)-Delta L_j*(-Delta E_i)>=0,
where polarized means Delta E_i<0, Delta E_j<=0, Delta L_i>=0, Delta L_j>0. The leaf may depend on the pair, and no K2 exclusion is added to RSM. A true valley forces every such split to have Q<0; this is the inherited conditional route to ORIGINAL. Neither existence nor nonnegativity is proved here.

## Computational and formal status
There are 243 exact-edge-list-deduplicated structural discovery records, not an isomorphism census. All are LOCAL, all whole sequences are unimodal, and max(D-U)=1. Residual graphs=0, residual pairs=0, eligible RSM tests=0. The second graft round repeated the same four seeds and added no new records after exact deduplication. The search budget was not enlarged.

Seven fixed controls and four selected discovery records have complete material arrays, including all vertex and edge polynomials. Four small fixed controls have fresh complete HEREDITARY checks; larger records retain fresh HEREDITARY=UNKNOWN. The inherited old23 HEREDITARY result is not rescinded, but is not described as a new execution. The non-log-concave/unimodal control remains intact.

ORIGINAL_FORMAL=NOT_ESTABLISHED. No target Lean source, build or axiom audit was attempted. FAMILY is inherited unchanged and not replayed or expanded. Review is SAME_MODEL_SELF_REVIEW, not independent peer review. No latest worldwide solution-status or novelty claim is made.
