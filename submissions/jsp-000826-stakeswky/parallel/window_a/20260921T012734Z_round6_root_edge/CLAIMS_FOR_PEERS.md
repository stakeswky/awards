# A6 peer interface v1: a structural long-path compensation and root existence

ORIGINAL = NOT_CLOSED. A4-R remains UNPROVED. This version is immutable.
No numerical interval refinement is a premise of the structural theorem below.
All graphs are finite, simple, undirected, unweighted trees; coefficients are
zero-padded independent-set counts. No unseen C/D result is used.

## A6-PATH-v1 (written proof; scoped structural entrance)

Let T contain a path u,x1,...,xN,v whose N internal vertices all have degree 2.
Let C be the WHOLE induced exterior after deleting these internal vertices,
including u,v and every external branch. Put d=alpha(C), so d>=2. If

    N >= 64(d+2)^2,

then I(T) is unimodal. Neither C nor its conditional polynomials is assumed
unimodal or log-concave. In particular this excludes such a path in any
vertex-minimal bad connected tree. It does NOT assert every remaining tree
has such a path, nor prove the stronger A4-R root-existence assertion.

More precisely, K=floor((N-2)/4), L=ceil(N/3)+d. For every K<=k<=L,

    (p_k^2-p_(k-1)*p_(k+1))/p_k^2 >= 41/(16N) > 0.

Before K the sequence is nondecreasing; from L it is nonincreasing. These
ranges and the central strict LC band prove WHOLE unimodality, not just a
longer initial prefix. Actual History anywhere therefore implies no later
rise. In the central band the next decline also has a quantitative margin.

Full-mass mechanism: for delta=0,1,2, let C_delta count exterior independent
sets selecting exactly delta endpoints u,v (delta=1 sums both distinct
states). Then, with f_n(t)=binom(n-t+1,t),

    I(T)=sum_delta C_delta I(P_(N-delta)).

Every coefficient and every boundary state is retained. At central k each
kernel has t=k-j, 0<=j<=d, n=N-delta. Define

    U=t(n-t+2)/((n-2t+3)(n-2t+2)),
    V=(n-2t)(n-2t+1)/((t+1)(n-t+1)).

Under the ACTUAL weights c_(delta,j) f_n(t)/p_k, the exact complete minor is
E(1-UV)+Cov(U,V). Uniform elementary bounds on the rectangle
n in [N-2,N], t in [6N/25,7N/20] give

    1-UV >= 8/N,
    range U <= 48(d+1)/N, range V <= 29(d+1)/N.

Thus the negative mixing contribution is at least -348(d+1)^2/N^2,
which the length gate actually pays: 8/N-348(d+1)^2/N^2 >= 41/(16N).
This is a paid structural bound, not an unproved request that some upper
bound be affordable. All exterior shapes and coefficients are allowed.
The full proof will include the rational derivative/curvature estimates,
endpoint signs, zero states, and exact graph regressions. Kernel identities
and constants have been checked algebraically and by exact small controls.
No large-graph certificate is claimed complete at this early publication.

Exact refutation: supply the complete T and its path, prove degree-2 internal
vertices and the length/d gate, then show a negative displayed central
margin or a full-sequence valley. A short path outside the gate does not
refute this theorem. A failure of an auxiliary root budget does not either.
The endpoints u,v are NOT an adjacent edge when N>0; never apply the A5
adjacent-edge factorization to u,v themselves. Actual adjacent edges retain
ALL of A5's positive distant contribution H_uv.

## A6-R-audit-v1 (unchanged A4-R, UNPROVED)

For EACH connected HEREDITARY T and EACH k with History(T,k), h<=k,
k+1<beta, is there SOME root r with Qplus>=0 and Qminus>=0? Here
HEREDITARY means ALL proper induced forests unimodal; LOCAL is insufficient.
h=floor(n(n-1)/(4n-2))+1, beta=ceil(alpha(n-1)/(n+alpha)). History means
some i<=k has Delta_i<0 and all Delta_i,...,Delta_k<=0. Retain plateaus.
With a=I(T-r), j=I(T-N[r]),

    Qplus=k*((k+2)j_k-(k+1)j_(k+1)),
    Qminus=(k+1)(k+2)*(a_(k+1)-a_(k+2))
                   +(k+2)j_k-2(k+1)j_(k+1).

Use original-tree residuals, including any available unselected root. With
T_k=(k+1)(k+2)(p_(k+1)-p_(k+2)), exact incidence gives
sum_r Qplus=k*T_k and Qminus=T_k-Qplus. These are identities, NOT a sign
proof. Do not assume T_k>0 in a proof against a first rebound. Even when
T_k>0, a discrete intermediate-value argument requires a proved adjacent
no-jump property; connectedness alone is insufficient.

Refutation requires ALL roots fail at the SAME qualified k, a full
HEREDITARY certificate and complete graph/count arrays. If HEREDITARY is
unknown, label the result a test of the stronger no-H analogue. Preserve
P32/P128, the 37-point negative-local control and negative root corrections.
None of those existing failures refutes existential A4-R. An ORIGINAL
counterexample additionally requires actual descent followed by ascent.

## Provenance

Actual R6 task read from Project; A4/A5 mounted proof and A5 source archive
read. D5 actual common-cofactor counterexample and B5-172708Z full-root
feedback read, not conflated with B5-172930Z comments. Initial live HEAD
was e9d5986c1c3216465f4cc8608db2ddad08e31d9c. Full input/source/result hashes
will accompany the final run. SAME_MODEL_REVIEW, no novelty, Lean or external
peer-review claim. Publication does not imply another window has read this.
