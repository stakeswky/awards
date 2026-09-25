# Window A Round 2: exact middle-bridge decompositions

**ORIGINAL: NOT_CLOSED.** No legal unweighted forest counterexample is produced.

This run preserves the previous Window-A prefix theorem and moves the analysis to the first strict descent. The new rigorous results are exact second-order decompositions, not a proof of the missing sign.

For a uniform independent k-set S of a forest F let H=F-N[S], T=|V(H)|, c(H) be the number of nonempty components of H, mu=E[T], and v=Var(T). Since H is a forest, eta=E|E(H)|=mu-E[c(H)]. The exact plateau-safe BARRIER slack is

    G_F(k)=mu(k+5-mu)-v-2 E[c(H)].

It is nonnegative exactly when p_(k+2)<=p_(k+1), provided p_k>0. Thus after a first strict descent, nonnegativity at every later pre-tail weak-descent index forbids a rebound, including descent--plateau--rise.

For a component decomposition F=disjoint_union_r F_r and an allocation a=(a_r), sum a_r=k, let w_a=prod_r p^r_(a_r)/p_k. Conditional on a, define mu_r(a_r), v_r(a_r), cbar_r(a_r) in component r and m_a=sum_r mu_r(a_r). Then

    G_F(k)=E_a[ sum_r G_r(a_r)
             + sum_(r<s) { a_s mu_r + a_r mu_s - 2 mu_r mu_s } ],

where

    G_r(j)=mu_r(j)(j+5-mu_r(j))-v_r(j)-2 cbar_r(j).

This identity retains the full component-allocation mixing term. It shows why componentwise no-rebound does not automatically imply forest no-rebound.

A second exact decomposition concerns the candidate one-step availability bound C1,

    mu_(k+1)<=mu_k+1.

C1 is equivalent to

    (k+1)p_(k+1)^2+p_k p_(k+1) >= (k+2)p_k p_(k+2),

and to

    Var(T)+2E[c(H)] <= 4mu.

For a component allocation a, define sigma_r(j)=4mu_r(j)-v_r(j)-2cbar_r(j). Then

    sigma_F(k)=E_a[sum_r sigma_r(a_r)]-Var_a(m_a).

Thus the between-allocation variance is exactly the obstruction omitted by any argument that checks components or conditional states separately.

C1 is only a candidate. If true for all forests it would imply the exact plateau-safe BARRIER and hence ORIGINAL with the inherited tail theorem. It is not proved here.

Finally, in any vertex-minimal disconnected ORIGINAL counterexample, every connected component has a unimodal but non-log-concave independence sequence. Each component is a proper induced forest, hence unimodal by minimality. If one component were log-concave, its coefficient sequence would be strongly unimodal, so convolving it with the unimodal sequence of the remaining proper induced forest would be unimodal, contradicting minimality.
