# Proof attempt and exact second-order bridge

## 1. Exact availability recurrence

For a uniform independent k-set S, let H=F-N[S], T=|V(H)|, M_H=|E(H)|, mu_k=E T, v_k=Var(T), eta_k=E M_H. Standard incidence counting gives

    p_k mu_k=(k+1)p_(k+1),
    mu_(k+1)=mu_k-1+(v_k-2eta_k)/mu_k.

Because H is a forest, M_H=T-c(H), with c(empty)=0. Hence eta_k=mu_k-Ec and

    mu_(k+1)=mu_k-3+(v_k+2Ec)/mu_k.                 (1)

The next coefficient is weakly decreasing exactly when mu_(k+1)<=k+2. Therefore its exact slack can be written

    G_F(k)=mu_k(k+5-mu_k)-v_k-2Ec.                 (2)

If p_(k+1)<=p_k then mu_k<=k+1. Thus G_F(k)>=0 is the exact sign needed at a weak-descent index. Repeating this after the first strict descent handles intervening equalities; no claim about a plateau before any descent is needed.

## 2. Component allocation: the missing mixed term is explicit

Write F as the disjoint union of F_1,...,F_s. Condition a uniform independent k-set on its component sizes a=(a_1,...,a_s), sum a_r=k. The allocation probability is

    w_a=prod_r p^r_(a_r)/p_k.

Conditional on a, the component independent sets are independent and uniform. Put

    mu_r=mu_r(a_r), v_r=v_r(a_r), c_r=E[c(H_r)|a_r],
    m_a=sum_r mu_r.

Then

    mu_F=E_a m_a,
    v_F=E_a sum_r v_r + Var_a(m_a),
    Ec_F=E_a sum_r c_r.                                  (3)

Substitute (3) into (2). The variance cancellation gives

    G_F(k)=E_a[m_a(k+5)-m_a^2-sum_r v_r-2sum_r c_r].      (4)

For each component define

    G_r(j)=mu_r(j)(j+5-mu_r(j))-v_r(j)-2c_r(j).

Using k=sum a_r and expanding m_a^2 yields the exact identity

    G_F(k)=E_a[sum_r G_r(a_r)
      +sum_(r<s)(a_s mu_r+a_r mu_s-2mu_r mu_s)].          (5)

No component or exterior factor is cancelled. The pair term is the genuine allocation-mixing contribution. It can have either sign: writing delta_r=mu_r-a_r, the pair term is -mu_r delta_s-mu_s delta_r. Therefore proving every conditional/component budget nonnegative is not enough unless the pair terms are also controlled. This is the precise point at which a naive componentwise induction would fail.

## 3. Candidate C1 and an even cleaner obstruction formula

Consider

    C1: mu_(k+1)<=mu_k+1.                                (6)

By the extension identity, (6) is exactly

    (k+1)p_(k+1)^2+p_k p_(k+1)
       >=(k+2)p_k p_(k+2).                               (7)

Using (1), it is also exactly

    sigma_F(k):=4mu_k-v_k-2Ec_F >=0.                     (8)

If p_(k+1)<=p_k, then mu_k<=k+1; C1 gives mu_(k+1)<=mu_k+1<=k+2, so C1 would prove the plateau-safe BARRIER. This implication is rigorous; C1 itself is not established.

Under the component allocation above, define

    sigma_r(j)=4mu_r(j)-v_r(j)-2c_r(j).

Equation (3) gives the exact decomposition

    sigma_F(k)=E_a[sum_r sigma_r(a_r)]-Var_a(m_a).        (9)

This is useful because it isolates the full between-allocation variance with coefficient one. Any proof of C1 for forests must either control this variance or exploit compensation unavailable in a per-state proof. This directly respects the mixed contribution that the refuted selected-count grouping lost.

## 4. Minimal disconnected counterexamples cannot contain an LC component

Assume F is an ORIGINAL counterexample with the minimum possible number of vertices and is disconnected. Every connected component C is a proper induced forest, so C is unimodal by minimality. The complementary forest R=F-C is also proper induced and unimodal.

If P_C were log-concave, its positive coefficient sequence would be strongly unimodal: convolution with any unimodal finite sequence is unimodal (the standard discrete strong-unimodality characterization of log-concave sequences). But P_F=P_C P_R is exactly that convolution. It would be unimodal, contradiction. Hence every component of a vertex-minimal disconnected counterexample is unimodal but non-LC.

This does not prove connectedness and does not justify arbitrary products of non-LC unimodal components.

## 5. Active refutation of C1

The candidate C1 was tested, not assumed. Exact integer arithmetic found no failure among all 81,136 unlabelled trees of orders 2 through 17, covering 741,584 C1 indices. For orders through 11, complete P arrays were independently recomputed by deletion/component splitting. The ten material graphs from the previous A run also pass; those P arrays had already been dual-recounted. Repeated products of the previous `three_nonLC_components` material forest were checked for 1 through 10 copies and pass.

These finite checks are evidence only. They do not prove C1 and are not substituted for the missing arbitrary-forest argument.

## 6. First unproved step

The first missing arrow remains a sign theorem in the middle. One sufficient form is C1, but after (9) the exact unresolved task is sharper:

    control Var_a(m_a) together with the within-component/root-state
    second-order slacks for arbitrary actual forest allocations,

or bypass C1 and prove G_F(k)>=0 only under the genuine history of a first strict descent followed by no rise. Neither has been completed.
