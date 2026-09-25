# Window A Round 4: connected-tree root compensation, claims v1

ORIGINAL = NOT_CLOSED; A4-T = NOT_CLOSED. C1_GLOBAL is REFUTED.
This file contains one UNPROVED sufficient candidate and one proved restricted
compensation theorem. No result of Window C is an assumption of either proof.

## Definitions and the exact root interface

T is a finite simple undirected unweighted connected tree. Write p_i=0 outside
0,...,alpha. Put h=floor(n(n-1)/(4n-2))+1 and
beta=ceil(alpha(n-1)/(n+alpha)). History(T,k) means that some i<=k has
p_i>p_(i+1), and p_t>=p_(t+1) for every i<=t<=k. For any vertex r let
A=T-r, J=T-N[r], a_i=p_i(A), j_i=p_i(J). Retain ALL actual branches.
For a uniform independent k-set S use H=T-N[S], including an unselected root
whenever it is still available, and g_k(S)=(k+5)|H|-|H|^2-2c(H).
The unnormalized root-state budgets are exactly

    Qplus(r,k) = k*((k+2)*j_k-(k+1)*j_(k+1)),
    Qminus(r,k) = (k+1)(k+2)*(a_(k+1)-a_(k+2))
                 +(k+2)*j_k-2*(k+1)*j_(k+1),
    Qplus+Qminus = (k+1)(k+2)*(p_(k+1)-p_(k+2)).

Qplus sums g_k over sets containing r, Qminus over sets not containing r.
All formulas are division-free, including zero conditional mass. The root-
absent correction is signed; it is NOT discarded. Conditional means, variances
and the between-state variance are contained in these original-graph sums.

## A4-R-v1: existence of a compensating root (UNPROVED)

For every connected T whose EVERY proper induced subforest is unimodal, and
for every k with h<=k, k+1<beta and History(T,k), does there exist at least one
vertex r such that Qplus(r,k)>=0 and Qminus(r,k)>=0?

If true, summing these two inequalities forbids the next rise. Applying it
after the first strict descent and using the inherited tail proves A4-T.
A failure at every root refutes this stronger sufficient candidate ONLY if
its full HEREDITARY premise is established. A unimodal failure graph need not
refute ORIGINAL. Report actual graph, complete p, all root A/J arrays and exact
Q signs; distinguish HEREDITARY verified/unknown. A scan without HEREDITARY
can test the stronger no-H version, not establish a refutation of this version.
Platforms use p_(k+1)=p_k directly; no division by current descent slack.

The universal ALL-root, BOTH-state nonnegativity shortcut is not proposed.
For the actual n121 tree consisting of a center joined to 30 hubs, each with
three private leaves, P=(1+4x+3x^2+x^3)^30+x(1+x)^90. At its central root and
k43, h31, beta52, the graph has a strict first descent but
Qplus=-86*binom(90,43)<0. Its full sequence is unimodal. HEREDITARY is not
asserted for this control. This disproves the no-H all-root shortcut, not A4-R.

## A4-L-v1: pendant-leaf compensation (PROVED, complete proof below)

Let r have t selected pendant neighbors L. Set C=I(T-({r} union L)) and
D=I(T-N[r]), b=deg D. Assume the WHOLE coefficient sequence C is unimodal.
If t>=max(4,2b+3), then T is unimodal. No shape/size restriction is placed on
the remaining branches. In A4-T, unimodality of C follows from the proper-
induced-subforest premise, not from arbitrary unimodal convolution.

Proof. The actual root decomposition is P=(1+x)^t C+xD, with 0<=D_j<=C_j.
For 1<=k<=floor((t-1)/2), binomial differences in the convolution are
nonnegative. Keep the j=k+1,k,k-1 terms and bound D_k-D_(k-1)>=-C_(k-1):

    p_(k+1)-p_k >= C_(k+1)+(t-1)C_k
                         +(t(t-3)/2-1)C_(k-1).          (L)

This is a SIGNED adjacent-difference bound, not a total-mass bound. Because
t>=4, the last multiplier is >=1. For 1<=k<=b+1 the last coefficient is
positive and all indices are in the stated binomial range. At k0 the difference
is n-1>0. Thus P increases through b+2. The perturbation xD is zero beyond b+1.
The remaining H=(1+x)^t C is unimodal: multiplication by 1+x preserves a
nonnegative unimodal sequence, since its two shifted copies have modes at
distance at most one. Moreover H_(b+2)>H_(b+1), so its decreasing part cannot
create a later rise. P is therefore unimodal, including plateaus. QED.

Any vertex-minimal bad connected tree must violate this leaf-count condition
at every root. We have NOT proved that every remaining tree meets it, and do
not call this a proof of A4-T. A counterexample to (L) should include the full
actual C,D and the integer difference; a failure of the theorem must satisfy
its C-unimodality and t conditions, not merely look similar.

## Requested independent checks

Prioritize A4-R on positive-mass competing root states, the actual B239 middle
case available to B, separate B226/B212 controls, and arbitrary internal grafts.
Do not substitute a root-selected support endpoint or a small d for e close
to d. No statement here identifies B212 with a descendant of B226's reduction.
Finite checks of (L) are regression, not the proof of its unbounded quantifiers.
