# Phase 9: aggregate compensation, a scoped uniform theorem, and the missing barrier

ORIGINAL is NOT_CLOSED. The general middle-interval barrier and the original
minimal-counterexample elimination remain unproved. Sections 4--7 prove a
scoped family theorem, including genuinely unbounded parameter ranges; they
are not a proof for every forest. No priority or global novelty is claimed.

## 1. Target and retained boundary

F is a finite simple undirected unweighted forest, possibly empty or
 disconnected. Let p_k count its independent k-subsets; p_0=1 and p_k>0 for
0<=k<=alpha, where alpha is the maximum independent-set size. Pad by zero
outside the support. ORIGINAL says p is unimodal, allowing peak plateaus.
Failure is a strict negative difference followed later by a strict positive
one; a plateau between them does not remove the failure.

The established Basit--Galvin tail theorem applies to every graph:

    beta = ceil(alpha(n-1)/(n+alpha)),
    p_beta >= p_(beta+1) >= ... >= p_alpha.

For n=0 set beta=0. This is an imported theorem, not a new result. In
particular any true valley has its later difference at j<beta. The Phase-8
sufficient assertion L_k=p_k^2-p_(k-1)p_(k+1)>=0 for all 1<=k<beta remains
unproved here. Its fixed-union termwise-positivity shortcut stays refuted by
K1,5. We now aggregate over all independent sets of a fixed size instead.

All actual exterior vertices and other components stay in F. Nothing in
Sections 2--3 assumes a counterexample is connected or has one large component.
The retained component-30 and 247-small-index reductions still have their
original external-census dependencies; those computations are not rerun.

## 2. Exact aggregate availability identities

For a uniformly chosen independent k-set S define

    H_S = F[V(F) \ N[S]],
    T(S)=|V(H_S)|,  M(S)=|E(H_S)|,
    mu_k=E T(S),  v_k=Var T(S),  eta_k=E M(S).

T counts vertices that can be added to S. M counts incompatible unordered
pairs among those available vertices. Expectations are over ACTUAL independent
k-sets in the whole graph, not over arbitrary arrays or independently chosen
local branch states. For k<alpha, mu_k>0.

Double-count pairs (S,u) with u available:

    p_k mu_k = (k+1) p_(k+1).                              (2.1)

Double-count ordered pairs of distinct nonadjacent available vertices:

    p_k E[T(T-1)-2M] = (k+1)(k+2) p_(k+2).                (2.2)

Each (k+2)-set has exactly (k+2)(k+1) ordered choices of its two removed
vertices. Removing a vertex u from H_S on extension also removes its neighbors;
summing available sizes after extension over u gives T(T-1)-2M. Consequently

    mu_(k+1) = mu_k - 1 + (v_k-2 eta_k)/mu_k.              (2.3)

This derivation does NOT select S uniformly and then u uniformly and call the
resulting (k+1)-set uniform. That procedure is biased. Uniform extensions
correspond to weighting each S proportionally to T(S), or directly using the
incidence double count above. The variance term precisely retains this bias.
Equations (2.1)--(2.3) hold for any finite simple graph, not just forests.
Thus they alone cannot prove a statement special to forests.

The usual LC inequality at index k+1 is equivalent to

    v_k <= mu_k + 2 eta_k + mu_k^2/(k+1).                  (2.4)

Indeed it is equivalent to mu_(k+1)/(k+2)<=mu_k/(k+1), and substitution in
(2.3) gives (2.4). This is a reformulation, not an established universal bound.

## 3. A weaker direct no-rebound barrier, with plateaus handled

Consider the proposed sufficient assertion BARRIER:
for every forest, every 0<=k with k+1<beta and mu_k<=k+1,

    v_k <= mu_k(k+3-mu_k)+2 eta_k.                        (3.1)

By (2.3), (3.1) is equivalent at that index to mu_(k+1)<=k+2,
or p_(k+2)<=p_(k+1). If BARRIER holds uniformly, once any strict descent
p_(i+1)<p_i has occurred before beta, apply the WEAK premise repeatedly to
propagate nonincrease up to beta, then use the known decreasing tail.
If the first descent is already at or after beta-1, the tail itself finishes
the argument. Hence uniform BARRIER would imply ORIGINAL.

The weak premise is essential to this sufficient induction: checking only
that a strict descent cannot be followed immediately by a strict ascent
would miss a pattern such as (1,4,3,3,4). BARRIER may be stronger than necessary
because it also controls pre-peak equalities; we do not claim equivalence to
ORIGINAL. For example the NONFOREST obtained by joining K9 to six isolated
vertices has sequence (1,15,15,20,15,6,1), which is unimodal but violates the
weak step. Joining K10 instead gives (1,16,15,20,15,6,1), a NONFOREST with a
true valley. Both are only semantic controls, never forest counterexamples.

A more tempting sufficient condition is v_k<=mu_k+2 eta_k, which would make
mean availability nonincreasing. Its unrestricted all-k version is false on
the historical H_10 tree of order 64:

    mu_31=99264/1076964787,  mu_32=33/3102 > mu_31.

The whole sequence is still decreasing there, and both means are far below
their respective thresholds 32 and 33. This is a tail-only failure, not a
refutation of BARRIER or of a middle-restricted assertion. Exact moment and
availability-distribution calculations in DIAGNOSTICS confirm this example.

### Other components cannot be canceled

For F=F1 disjoint-union ... disjoint-union Fr, conditioning on total size k
introduces an allocation vector K=(k1,...,kr), with probability

    Prob(K)=prod_h p_(h,kh) / p_(F,k),   sum kh=k.

Conditioned on K, choices in the components are independent, so

    Var_F(T) = E_K[sum_h Var(T_h | kh)]
               + Var_K(sum_h mu_(h,kh)),
    E_F M = E_K[sum_h eta_(h,kh)].                         (3.2)

The second variance is an actual nonnegative contribution from allocation
between components. Componentwise claims without a bound for this term do
not yield (3.1). Section 9 checks the complete identity for a two-large-component
control at all 48 possible sizes. No arbitrary product-unimodality is assumed.

## 4. A uniform polynomial compensation lemma

We next pursue a route that really DOES bound a total perturbation, rather
than merely rename the missing inequality.

Let A,Q be nonnegative finite polynomials with interval support and suppose
A is unimodal. Write A=Q+E with E coefficientwise nonnegative. Let the full
mode interval of Q be [l,r], with strictly positive boundary gaps

    delta = min(Q_l-Q_(l-1), Q_r-Q_(r+1)) > 0.

If E(1)<delta, then

    A_l-A_(l-1) >= delta-E(1)>0,
    A_r-A_(r+1) >= delta-E(1)>0.

Since A is unimodal, its entire mode interval lies within [l,r]. If Q is
unimodal as well, A+xQ is unimodal: write [a,b] for A's mode interval. The
mode interval of xQ is [l+1,r+1]. Since l<=a<=b<=r, we have
max(a,l+1)<=b+1. Below b both component differences can be certified
nonnegative up to their common right-mode bound; after max(a,l+1) both are
nonpositive. At most one difference is uncontrolled, so no descent-then-rise
is possible. This is the standard adjacent/overlapping-mode argument,
including plateaus, not a general closure rule for sums of unimodal sequences.

The assumption that A is unimodal is indispensable. The regression
A=(1+2x)^10+x^11+x^12+2x^13 has a perturbation of total mass four, far below
the central gap bound used below, yet A+x(1+2x)^10 has a tail valley. This is
an artificial polynomial control, not a realized forest. Peak localization
without the shape premise would not establish unimodality.

## 5. A standalone branch LC lemma

For integer a>=1 put

    s_a(x)=(1+2x)^a+x(1+x)^a.

This counts the subdivided star with a pendant paths of length two and their
common hub: when the hub is absent each edge offers polynomial 1+2x; when
present only each far leaf is free. Its coefficients are strictly log-concave
on their internal positive support.

Proof. At index 1<=i<=a put d=a-i>=0, z=2^(i-1), C=binom(a,i).
The three adjacent coefficients divided by C are

    s_i/C       = 2z+i/(d+1),
    s_(i-1)/C   = i/(d+1) * (z+(i-1)/(d+2)),
    s_(i+1)/C   = 4zd/(i+1)+1.

These formulas also handle i=a. Their LC minor divided by C^2 is
c2 z^2+c1 z+c0, where

    c2=4(d+i+1)/((d+1)(i+1)) >= 4/(d+1),
    c1=i/(d+1)*(3-4(i-1)d/((i+1)(d+2))) >= -i/(d+1),
    c0=i(d+i+1)/((d+1)^2(d+2)) > 0.

Thus the minor is at least (4z^2-iz)/(d+1)+c0>0, since 4*2^(i-1)>=i.
The last positive coefficient is at a+1; its zero-padded next minor is
nonnegative directly. This proves the lemma for ALL a, not just tested a.

We also use LC convolution closure. For completeness: interval-supported LC
coefficients have nonnegative 2-by-2 minors in their Toeplitz matrix, because
successive positive ratios decrease. The Toeplitz matrix of a convolution
is the product of the two Toeplitz matrices. Each 2-by-2 minor of that product
is a sum of products of nonnegative minors by the 2-by-2 Cauchy--Binet formula.
All relevant sums are finite for finite supports. In particular the adjacent
minor is exactly the LC minor of the convolution. This proves the needed
closure, rather than assuming products of merely unimodal sequences are safe.

## 6. Arbitrary branch count: a proved aggregate-dominance region

Define T(a1,...,at), t>=1 and ai>=1, as the following WHOLE connected tree:
one central vertex joined to t hubs, with ai pendant two-edge paths at hub i.
It has n=1+t+2m vertices, where m=sum ai. Direct root occupancy gives

    A=prod_i s_ai,    Q=(1+2x)^m,    P(T)=A+xQ.             (6.1)

A is LC by Section 5, hence unimodal. Write A=Q+E; E>=0 and

    E(1)=3^m [prod_i (1+(2/3)^ai)-1].                     (6.2)

The binomial Q has coefficients q_j=binom(m,j)2^j. Their ratio is
2(m-j)/(j+1), so Q is unimodal. Let [l,r] be its mode interval and q*=q_l=q_r.
At the two strict boundaries,

    q_l-q_(l-1)=q* (2m-3l+2)/(2(m-l+1)) >= q*/(2(m+1)),
    q_r-q_(r+1)=q* (3r+1-2m)/(r+1) >= q*/(m+1).

The numerators are positive integers. Also q*>=Q(1)/(m+1)=3^m/(m+1).
Therefore delta>=3^m/[2(m+1)^2]. Sections 4--5 prove:

THEOREM 6.1. For ALL t>=1 and ai>=1 satisfying

    2(m+1)^2 [prod_i(1+(2/3)^ai)-1] < 1,                  (6.3)

P(T(a1,...,at)) is unimodal. The numbers of vertices and hubs are unbounded.
This is a uniform sufficient parameter inequality, not finite sampling.

A coarse but explicit infinite subregion is

    ai=a for all i;  t>=1;  a>=16(t+1).                   (6.4)

Here q=(2/3)^a. If tq<=1/2, then
(1+q)^t-1 <= sum_(j>=1)(tq)^j <=2tq, because binom(t,j)<=t^j.
Thus it suffices that 4t(ta+1)^2(2/3)^a<1.
For a0=16(t+1), the left side decreases with t: its successive ratio is at
most 18(2/3)^16<1, using
[16(t+1)(t+2)+1]/[16t(t+1)+1] <= (t+2)/t <=3.
At t=1 it is 4*33^2(2/3)^32<1. For fixed t it decreases with a>=a0,
since its successive ratio is at most (2/3)((a+1)/a)^2<1 for a>=32.
Similarly t(2/3)^(16(t+1))<= (2/3)^32<1/2, and increasing a reduces it.
This proves (6.4) for every t,a in the region, including arbitrarily many hubs.
The four rational base comparisons are checked by exact integers in source;
the preceding monotonicity argument supplies the infinite coverage.

The bounds are intentionally sufficient rather than optimal. Their failure
is NOT evidence for a counterexample, and we do not spend this run merely
lowering the numerical threshold.

## 7. Complete all-parameter result for three equal hub groups

For H_a=T(a,a,a), the whole P is unimodal for EVERY integer a>=1.
For a>=26 put Q=(1+2x)^(3a). Its unique mode is 2a, and its boundary gaps are
q*/(a+1) and q*/(2a+1), respectively. Also q*>=3^(3a)/(3a+1).
With q=(2/3)^a<=1, E(1)/3^(3a)=(1+q)^3-1<=7q. Thus it suffices that

    7(3a+1)(2a+1)(2/3)^a < 1.                            (7.1)

At a=26 this is the exact integer inequality 7*79*53*2^26<3^26.
Its successive ratio for a>=26 is at most
(2/3)*(82/79)*(55/53)<1. Hence every a>=26 satisfies (7.1).
Section 4 puts A's unique mode at 2a, while xQ has mode 2a+1, and proves P
unimodal. This is the same single argument for ALL a>=26.

For the FINITE remainder a=1,...,25, compensation.py computes the complete
A,Q,P and verifies A's mode interval is contained in [2a,2a+1]. A's LC is
already uniform by Section 5, and xQ's mode is 2a+1. Thus the adjacent-mode
lemma finishes every remaining case. The graph counts are separately
recomputed by vertex deletion and the finite A coefficients by direct nested
convolution. Exact arrays, hashes and clean replay accompany this proof.
This last finite portion makes the full all-a theorem computer-assisted;
it is not Lean-formalized and has not received independent external review.

The historical H_10, whose LC fails at a high index, is included. There is no
contradiction: this theorem proves UNIMODALITY, not full LC of H_a.

## 8. Exterior scope and comparison with the original target

If R is any actual forest whose independence polynomial is LC, then
I(R)P(T) is unimodal for every T proved above: LC times unimodal preserves
unimodality. One self-contained justification uses the Toeplitz ratio
inequality q_(i-a)q_(j-b)>=q_(j-a)q_(i-b) for i<j and a<b, with q LC.
Positive differences of a unimodal sequence precede negative ones; summing
that inequality with their magnitudes shows convolution cannot have a
negative difference followed by a positive difference. Zero boundaries and
plateaus are allowed. This is the same strong-unimodality direction proved
in the retained Phase-6 work.

This extension keeps R in the count and REQUIRES its stated LC premise. It
does not cover arbitrary non-LC disconnected factors or arbitrary additional
branches ATTACHED inside T. In particular, we cannot delete a T-component
from a hypothetical disconnected counterexample on the ground that T is only
unimodal. No theorem for arbitrary products of H_a is asserted.

The new scoped result excludes a connected minimum counterexample equal to
one of these whole T trees. It does not eliminate every occurrence of their
local hub patterns inside a larger forest. Nor does it prove every remaining
forest must lie in (6.3), (6.4), or the three-equal family. The old mandatory
terminal-structure -> arbitrary-real-exterior elimination is still missing.

## 9. General-forest stress tests and proof checks

The three-state availability recurrence counts all independent sets and their
available vertices, retaining the whole forest. At each root use S=selected,
D=unselected and dominated by a child, and U=undominated within its subtree,
with the root's own y marker deferred until its parent's state is known.
For child states (Si,Di,Ui),

    U=prod_i(Di+yUi),
    D=prod_i(Si+Di+yUi)-U,
    S=x prod_i(Di+Ui),
    completed root=S+D+yU.

Root selection blocks each child's root, hence Di+Ui with no y on that root.
An unselected root does not block children. This partition proves the
recurrence by tree induction. Different components multiply without dropping
vertices. Differentiating zero, one and two times at y=1 gives p_k, sum T and
sum T(T-1). Jet multiplication includes the cross factor two in the second
derivative. The computation is a lossless counting recurrence, NOT an invariant
proving the missing variance bound.

For each edge uv, the independent sets leaving both endpoints available are
exactly the independent sets of F-(N[u] union N[v]). Summing these graph
polynomials supplies a second algorithm for sum M. This independently checks
(2.2) against the availability recurrence on every new record.

The fixed stress grammar produces 288 distinct forests, all absent from the
supplied Phase7/Phase8 canonical inventory (not a global novelty claim). It
varies nested hub depth and parity, then retains either no exterior, a whole
non-LC disconnected H_10 factor, or two different actual bridge completions.
No prior recorded wedge/position expansion is repeated. This is one finite
surface, not all forests or all completions. Maximum order is 234; 72 are
disconnected. Every P is recounted by two graph algorithms, all 82,272 A/B
arrays are computed, 40,776 edge-neighborhood polynomials are recounted, and
six materials receive 2,808 independent A/B recounts.

There are 428 actual k positions with k+1<beta and p_(k+1)<=p_k; all 428 are
strict descents and all satisfy the no-rebound inequality. These are
NONVACUOUS TESTS OF BARRIER'S PREMISE, but not 428 residual U/D pairs.
True valleys, prefix-LC failures, residual graphs/pairs, and middle mean-
availability increases are all zero. HEREDITARY is UNKNOWN for new records.

Sixteen small forest controls and two NONFOREST semantic controls check
102,223 literal subsets in total (3,919 in forest controls). Full availability
histograms for H_10 match the moment computation at every size. The complete
law of component-allocation variance is verified for H_10 disjoint-union
T(3,4,4), not extrapolated to an unbounded product theorem.

## 10. Final chain and first substantive gap

General route, proved implications only:

    true forest valley -> a later rise before beta;
    uniform BARRIER -> no later rise after any first descent -> ORIGINAL;
    exact counting -> moment identities (2.1)--(2.3).

MISSING: a forest-specific bound proving (3.1) throughout the middle range.
The moment identity is equivalent to a local coefficient comparison and does
not reduce this gap by itself. The positive component-allocation variance
and the fixed-union negative terms cannot simply be discarded.

Scoped route, complete with its stated hypotheses:

    whole tree T(a1,...,at) -> exact A+xQ;
    branch LC -> A LC;
    total remainder mass bound -> A peak localization;
    adjacent modes -> whole-sequence unimodality.

Sections 6--7 provide uniform bounds and a proved finite remainder, rather
than assuming finite observations cover unbounded parameters. However, there
is NO proved cover of all forests by those hypotheses. ORIGINAL remains
NOT_CLOSED, and the core universal barrier/terminal-elimination gap remains
unreduced. Record the scoped theorem separately from core NO_STRUCTURAL_ADVANCE.
J_H, RSM, PREFIX_BETA, ORIGINAL formalization and independent review remain
unresolved or not established with their earlier boundaries unchanged.
