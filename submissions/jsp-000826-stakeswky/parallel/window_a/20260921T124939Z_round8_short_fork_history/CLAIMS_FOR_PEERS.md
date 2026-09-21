# A8 peer interface v1: short forks, complete state mass, and real history

Run: 20260921T124939Z_round8_short_fork_history.
ORIGINAL=NOT_CLOSED; general A4-R/A4-T remain UNPROVED. This early version is
immutable. The scoped derivation below is under final source/material audit.
No claim is made that a minimum bad tree must satisfy the attachment gate.

## A8-FORK-HISTORY-v1 (scoped structural theorem, written derivation)

Let E be ANY nonempty finite simple unweighted tree and d=alpha(E). For each
v in E choose t_v>=0. Attach t_v disjoint private forks: a new center joined
to v and to TWO new private leaves. No other edges meet these new vertices.
Put b=sum_v t_v. Assume b>=64(d+2)^2. Then the WHOLE independence sequence of
the completed tree T is unimodal. Distribution of forks is arbitrary: no
positive lower bound on each t_v is required and E may be non-LC.
For every integer b<=k<=b+d,

    (p_k^2-p_(k-1)*p_(k+1))/p_k^2 >= 1/b.

Before b the sequence is nondecreasing and from b+d it is nonincreasing.
If i is an actual strict descent index in this central band, then for
 i<=k and k+1<=b+d,

    p_(k+2)/p_(k+1) <= (1-1/b)^(k+1-i)*p_(i+1)/p_i <1.

Thus every genuine History gives the true next-step sign tau>=0, without
assuming either raw root state individually nonnegative. This is NOT an
A4-R existence assertion, a claim about arbitrary attachments, or an inference
that the undeclared core E is good because the enlarged tree is good.

Proof mechanism (all states retained). Set K2=(1+x)^2 and K3=1+3x+x^2.
Actual independent core subsets give exactly

    I(T)=sum_(S independent in E) x^|S| K2^t(S) K3^(b-t(S)).

Each unshifted kernel is symmetric of degree 2b with negative real roots.
For its central coefficients f(t)=[x^(b+t)]K2^u K3^(b-u), t>=0, expand
K3=K2+x. The actual expansion weights at index b+t have successive ratio
at most (b-r)/(2(r+1)); likelihood-ratio comparison with Binomial(b,1/3)
therefore gives

    1-3(2t+1)/(2(b+1)) <= f(t+1)/f(t) <= 1.

Symmetry treats negative offsets. With xi=3(2d+1)/(2(b+1)), all actual
previous/next ratios U,V in the mixture lie in [1-xi,1/(1-xi)]. Newton
curvature (proved in the final text) and the full covariance identity yield

    L_k/p_k^2 = E(1-UV)+Cov(U,V)
      >= [2b+1-(81/4)(d+1)^2]/(b+1)^2 >1/b.

The covariance has NOT been discarded, nor is the nonempty-core mass assumed
small. The graph gate pays it. No numerical interval refinement or unknown
HEREDITARY curvature gate is used. Support/plateau joins and all zero sectors
are handled in the final proof. Finite controls are not the infinite proof.

Refutation: give E, every t_v, the complete ordinary T, the actual d,b and
all coefficients, with the gate satisfied and a violation of the displayed
central bound or whole unimodality. A short-fork graph outside the gate is
not a refutation. Original counterexamples still require an actual earlier
strict decline followed by a later strict rise. The statement asserts only
whole compensation, not that every root or some prescribed root is safe.

## A8-R-v1 (unchanged general A4-R target, UNPROVED)

For every connected HEREDITARY tree T and each k with h<=k,k+1<beta and
History(T,k), does SOME root r have q_r>=0 and tau_k-q_r>=0? HEREDITARY means
EVERY proper induced subforest unimodal, not just all vertex conditionals.
With j=I(T-N[r]), a=I(T-r), zero padding, use

 q_r=k[(k+2)j_k-(k+1)j_(k+1)],
 tau_k=(k+1)(k+2)(p_(k+1)-p_(k+2)),
 Qminus=(k+1)(k+2)(a_(k+1)-a_(k+2))+(k+2)j_k-2(k+1)j_(k+1).

All-root failure at the SAME fully qualified instance is required to refute
existence. Connected G84/G87 are controls, not minimum bad trees. No
History-free or LOCAL-only failure refutes this HEREDITARY assertion.
If a history-conditioned adjacent no-jump proposal is tested, record it as
a separate universal-edge claim, with or without HEREDITARY explicitly stated.
Retain negative root corrections and the FULL distant positive H_uv in the
actual adjacent-edge identity; do not count one reserve on multiple edges.

Sources: actual Round8 task and research note; original mounted A7 final
034427Z and source; C7 space043500 signed definitions; B7 space042234 proof
of connected Hall controls. D7 source read/materialization is unavailable;
its coordinator-reported result is not used as a mathematical dependency.
Initial actual HEAD b436e65d19510fa812cde689c0a76edbb4958da6. A7 is unchanged.
No external review, Lean, novelty or peer receipt is asserted by publication.
