# C4-K-v1: two claims from Window C

ORIGINAL = NOT_CLOSED. C4-F (all disconnected hereditary forests) = NOT_CLOSED.
These claims use no unproved Window A estimate. All graphs are finite simple
undirected unweighted forests, with the complete coefficient support retained.

## Claim 1 — exact budget conservation (PROVED, written proof)

For any partition P of F into complete component subunions Z_1,...,Z_r, condition
a uniform independent k-set on its allocation a_1+...+a_r=k. Use actual weights
w_a=product p_(a_i)(Z_i)/p_k(F), m_a=sum mu_(a_i)(Z_i), and

    R_P = E_w[sum sigma_(a_i)(Z_i)] + mu_F(k)d_F(k),
    V_P = Var_w(m),
    R_P - V_P = (k+1)(k+2)[p_(k+1)(F)-p_(k+2)(F)]/p_k(F).

Here mu_j=(j+1)p_(j+1)/p_j, d_j=j+1-mu_j,
sigma_j=4mu_j-Var(|F-N[S]|)-2E[c(F-N[S])]. Terminal mu and sigma are zero.
Nonterminal negative local sigma terms are NOT clipped. There is no history,
LC, HEREDITARY, or middle-range premise in this identity.

For a refinement Q of P, R_Q-R_P=V_Q-V_P>=0. Thus for the EXACT variance,
"some partition pays its budget" is equivalent to "every partition pays".
This is an accounting identity, NOT a proof that the common gap is nonnegative.

For two blocks, put delta_t=m_(t+1)-m_t, F_t=sum_(a<=t)w_a,
K_st=F_min(s,t)(1-F_max(s,t)). Then

    V=sum_(s,t)delta_s delta_t K_st,
    V_abs=sum_(s,t)|delta_s delta_t| K_st,
    U_var=sum_t delta_t^2 sum_(a<=t<b)w_a w_b(b-a),
    V_abs-V=4 sum_(s<t,delta_s delta_t<0)|delta_s delta_t|K_st.

V<=V_abs and V<=U_var, but no universal V_abs<=R or U_var<=R is asserted.
B can refute a proposed budget implication only after checking real weights,
full support, actual history, and h<=k, k+1<beta. An upper-bound failure alone
is not an original counterexample. See PROOF.md for all derivations.

## Claim 2 — finite palette, unbounded multiplicities (PROVED_COMPUTER_ASSISTED)

Define T(a;l) by a central vertex, t adjacent hubs, and at hub j, a_j private
length-two paths and l_j private leaves. No other edges or vertices are present.
Use the four exact types, in this index order:

    0: T26  = T([3,4,4]; [0,0,0]);
    1: B212 = T([6,7,7,7]+[8]*9; [0]*13);
    2: B226 = T([0]+[8]*13; [3]+[0]*13);
    3: B239 = T([8]*14; [0]*14).

Every finite disjoint multiset of these types is unimodal, with NO bound on
multiplicities. The same holds after disjoint union with any forest whose
WHOLE independence polynomial is LC. Therefore, for every such whole forest,
every actual component partition, and every genuine descent-history position,
R_P>=V_P. This real comparison holds throughout the positive support; it does
not require the additional middle restriction.

The certificate contains 19 inclusion-minimal LC component multisets. The
remaining all-submultisets-nonLC configurations number 4,9,13,1 at sizes 1,2,3,4,
and zero at size 5. All 27 residual configurations are unimodal. The only
size-four residual is (0,2,2,2). The finite test is connected to arbitrary
multiplicities by an explicit induction and a proved LC-times-unimodal lemma.

In an ACTUAL vertex-minimal bad forest, even with arbitrary other component
shapes present, none of the 19 LC blockers can occur as complete components.
In particular there are at most four components from this palette; if four,
the multiset must be (0,2,2,2). A forest containing only palette components
cannot be a minimum counterexample. This uses HEREDITARY for the proper
complement; it is not an assertion that ordinary test graphs are HEREDITARY.

For adversarial checks, supply an actual palette graph/multiset, full integer
coefficients and a strict decline followed by a rise, or a mismatch in the
19-blocker certificate. Arbitrary new component types are outside this claim.
The interface does not automatically apply to original-graph conditional
root states: a root that was not selected may still be available.
