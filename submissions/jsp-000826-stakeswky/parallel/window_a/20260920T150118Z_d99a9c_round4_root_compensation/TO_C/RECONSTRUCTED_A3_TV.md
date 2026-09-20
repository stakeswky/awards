# Handoff to C: RECONSTRUCTED A3 absolute-variation bound

This is a new written reconstruction, NOT byte restoration of the unavailable
A3 final archive. The prior conversation reports V<=V_TV<=U; its local final
source and replay records were not accessible in this Round-4 runtime. The
following proof is self-contained. No prior execution counts are imported.

For an actual two-block component decomposition F=X disjoint_union Y at total
size k, use w_a=p_a(X)p_(k-a)(Y)/p_k(F) on its full positive interval [lo,hi].
Set m_a=mu_X(a)+mu_Y(k-a), delta_t=m_(t+1)-m_t, and

    V = sum_(a<b)w_a w_b (m_b-m_a)^2,
    V_TV = sum_(a<b)w_a w_b (sum_(t=a)^(b-1)|delta_t|)^2,
    U = sum_(a<b)w_a w_b (b-a)sum_(t=a)^(b-1)delta_t^2.

The pairwise variance identity proves V=Var_w(m). Triangle inequality applied
to each increment sum proves V<=V_TV; Cauchy proves V_TV<=U. If P_ab,N_ab
are the positive and absolute-negative variations from a to b, respectively,

    V_TV-V = 4 sum_(a<b)w_a w_b P_ab N_ab >=0.

This is valid without LC, negative association, or sign assumptions on local
sigma. For multiple components use Doob conditional means M_i=E[m|a_1,...,a_i].
Orthogonality of successive martingale increments gives
Var(m)=sum_i E Var(M_i|a_1,...,a_(i-1)); at each fixed prefix the remaining
coordinate has its true conditional product-coefficient weights. Apply the
one-dimensional V_TV bound to that conditional mean profile. Degenerate
supports contribute zero. This gives a genuine upper bound at arbitrary
component count; it does NOT prove it is payable by the signed local budget.

The unresolved comparison is still Var(m)<=E sum sigma_i+mu*d. Refusing to
clip negative sigma is essential. This handoff neither claims arbitrary
component closure nor applies component formulas to a root-forbidden state.

C4-K-v1 at 370f0a1d was read as an actual published interface. Its whole-forest
palette theorem is not used in A's connected-tree proof: the supporting
certificate and full proof have not been independently read/replayed here.
Our A4 root interface is in TO_B/CLAIMS_v1.md and will be proved in PROOF.md.
