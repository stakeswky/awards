# Window A Round 3: slack-barrier claims, version 1

ORIGINAL NOT_CLOSED. C1_GLOBAL is REFUTED, not a target theorem. The library 226-vertex certificate and remote 212-vertex certificate are separate B runs; both have tail-only C1 failure. Their whole polynomials were freshly recomputed here by graph DP and explicit binomial formulas. This file does not combine B batch counts.

All graphs below are finite simple undirected unweighted forests. Coefficients count independent sets, with zero padding outside positive support. Define n, alpha and largest component order M from the completed graph, h=floor(M(n-1)/(4M-2))+1 and beta=ceil(alpha(n-1)/(n+alpha)). For p_k>0 define mu_k=(k+1)p_(k+1)/p_k, including mu_alpha=0. For k<alpha define d_k=k+1-mu_k and e_k=mu_(k+1)-mu_k-1. S is a uniform independent k-set in the ORIGINAL graph, H=F-N[S], T=|V(H)|, c=c(H). Put sigma=4mu-Var(T)-2E[c] and G=sigma+mu*d. No LOCAL or HEREDITARY premise is silently assumed.

## A3-H-v1: actual target, CONJECTURE

For every F and k with h<=k, k+1<beta, if there is i<=k with Delta_i<0 and Delta_t<=0 for every i<=t<=k, then e_k<=d_k. Here Delta_t=p_(t+1)-p_t. The exact integer failure test is p_(k+2)>p_(k+1), after verifying all stated history and range premises. Equivalently G<0. A valid failure IS an ORIGINAL counterexample. Preserve actual edges and the COMPLETE integer sequence; equality d_k=0 is not handled by division by d_k.

## A3-K-v1: two-block allocation upper bound and stronger test candidate

Split a disconnected actual F into nonempty disjoint component subunions X,Y. Let A_a=p_a(X), B_b=p_b(Y), lo=max(0,k-alpha_Y), hi=min(k,alpha_X). At each a in [lo,hi], w_a=A_a B_(k-a)/p_k(F) and m_a=mu_X(a)+mu_Y(k-a). At each t<hi set delta_t=m_(t+1)-m_t and

    tau_t=sum_(a<=t<b) w_a*w_b*(b-a),
    U=sum_(t=lo)^(hi-1) tau_t*delta_t^2,
    R=sum_a w_a*(sigma_X(a)+sigma_Y(k-a))+mu_F(k)*d_k.

Empty sums are zero. All terminal local mu values use their zero-padded coefficient definition; sigma uses moments even when local mu=0. Negative local tail sigma terms MUST remain in R.

PROVED upper bound (not a conjecture): Var_w(m)<=U. Indeed Var_w(m)=sum_(a<b)w_a*w_b*(sum_(t=a)^(b-1)delta_t)^2, and Cauchy bounds each square by (b-a)*sum delta_t^2. This needs neither log-concavity nor a Poincare/negative-correlation assumption.

STRONGER CANDIDATE, UNPROVED: under ALL A3-H history/range premises, U<=R for EVERY such two-block split. This would imply G=R-Var_w(m)>=0. But U>R refutes ONLY this stronger candidate, not A3-H or ORIGINAL. Report U,R,actual Var and G separately with exact rational arithmetic (multiply by common positive denominators for integer comparison).

Priority checks: two distinct C1-defective components; a defective large component mixed with a smaller non-LC component; and a defective component plus isolated/path/branching components with enough total vertices for negative local tail sigma to appear in a global middle allocation. Do not discard tiny weights. Finite success is not proof. A connected tree has no such component split; this candidate alone would not settle connected trees.

## A3-R-v1: root-absent correction, identity to audit

Let r be ANY vertex, A=F-r and J=F-N[r]. Condition on r NOT selected, so S is uniform among independent k-sets of A. Define Gminus using the ORIGINAL F availability in this conditional distribution: Gminus=(k+5)E[T]-E[T^2]-2E[c(H)]. If p_k(A)>0 and p_k(J)>0 then

    p_k(A)*Gminus = p_k(A)*G_A(k)
                    +p_k(J)*(k+2-2mu_J(k)).

For p_k(J)=0 the correction is zero, expressed as (k+2)p_k(J)-2(k+1)p_(k+1)(J), without dividing by zero. The correction exists because an unselected root may still be available and join remaining branches. Root-selected states use k-1 in J. Test by literal subsets or moment counting on actual edges, not by deleting r and calling its moments original-graph moments. This is an identity, not a claim that its correction has fixed sign.

## Feedback requirements

Use exact graph definitions, recompute n,M,alpha,h,beta, retain plateau history and full coefficients. State which claim ID and premises fail. Whole-graph checks, selected-root checks and all-root checks are distinct. Do not assume this file has proved the U<=R compensation or the original no-rebound theorem. Later versions must be appended with supersession notes, not silently overwrite v1.
