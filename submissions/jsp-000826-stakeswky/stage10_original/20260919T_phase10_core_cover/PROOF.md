# Phase 10: arbitrary cores, genuine exteriors, and non-LC component products

**ORIGINAL remains NOT_CLOSED.** This document proves a sufficient theorem
for arbitrary finite core shapes with explicit private-arm hypotheses. It
does not prove that all forests satisfy those hypotheses. The unrestricted
BARRIER/minimum-counterexample gap remains open. No global novelty is claimed.

## 1. Original statement and inherited tail

All target graphs are finite, simple, undirected, unweighted forests, possibly
empty or disconnected. Let p_k count independent k-subsets, alpha be the
maximum independent-set size, and P(x)=sum p_k x^k. The positive support is
0,...,alpha: take subsets of a maximum independent set. Unimodality allows
plateaus. A counterexample requires i<j with p_(i+1)<p_i and p_(j+1)>p_j;
appending zero coefficients does not change this test.

The Basit--Galvin tail theorem for any finite simple graph gives

    beta = ceil(alpha (N-1)/(N+alpha)),
    p_beta >= p_(beta+1) >= ... >= p_alpha.               (1.1)

N is the total number of graph vertices. Empty graphs are trivial. This is a
classical external input, not a theorem discovered in this task. Source:
Basit and Galvin, On the independent set sequence of a tree, Electronic
Journal of Combinatorics 28(3) (2021), P3.23, Theorem 1.3;
arXiv:2006.12562v2. Its statement/proof were re-read in HTML.

The previous component-30 census and H2/H3 are not needed by the new theorem
or its exact controls. Their dependency remains in the inherited minimal
counterexample restrictions; they were not rerun. No connectedness or
single-large-component premise is added to the original target.

## 2. Arbitrary-core construction and exact exterior-preserving formula

Let C be ANY finite simple graph on q>=1 vertices. For applications to
ORIGINAL, C is a forest, with no restriction on its component shapes. Choose
a nonempty vertex cover H: every edge of C has at least one endpoint in H.
Write h=|H|, W=V(C)\H, r=|W|=q-h. Thus W is independent. H itself need not be
independent. At every v in H append a_v private paths v-u-v' of two edges,
with two new, distinct vertices on each path and no other new edges. Put

    M = sum_(v in H) a_v,     a = min_(v in H) a_v.

Call the resulting graph D(C,H,a_v). If C is a forest, D is an ordinary
unweighted forest. It has N=q+2M vertices. Its independence number is
M+alpha(C): each private edge allows at most one selected new vertex, and
all far endpoints can be selected simultaneously with a maximum independent
set in C.

For an independent subset S of H, write s=|S|,
A(S)=sum_(v in S) a_v, and d(S)=|N_C(S) intersect W|. Conditional on exactly S
being selected inside H, a private path offers 1+2x if its hub is absent,
and 1+x if its hub is selected. Precisely r-d(S) original vertices in W
remain free. Consequently

 P_D(x) = sum_(S subset H independent)
          x^s (1+x)^(A(S)+r-d(S)) (1+2x)^(M-A(S)).       (2.1)

No exterior is discarded. An attached tree must be included in C, including
all its vertices and edges; any other connected components stay in C as well.
For S empty, the summand is

    Q(x)=(1+x)^r(1+2x)^M.

Write P_D=Q+E, where E has nonnegative coefficients. Formula (2.1) sums the
ACTUAL allowable core selections. Counting all subsets of H in the estimates
below is an upper bound, not replacement of the graph by a fictitious one.

## 3. The scoped uniform theorem

Define the exact rational number

 rho = (1 + (3/2) 2^(-floor(a/6)))^h - 1.

**Theorem 3.1.** If

    a>=24,       M>=24q,
    2 * 5^r * (M+r+1)^(r+1) * rho < 1,                 (3.1)

then the complete independence sequence of D(C,H,a_v) is unimodal.
The theorem permits arbitrary core edges, arbitrary core size, and arbitrary
numbers of connected components. It does not assume the components or their
products are LC, nor that the root-absent polynomial is unimodal.

The strict inequality is a SUFFICIENT condition. Failure of (3.1) does not
mean a counterexample exists. The explicit equal-arm corollary in Section 7
shows this is a genuine unbounded region, not a disguised finite sample.

## 4. Three elementary coefficient estimates

Set b_k=binom(M,k)2^k, the coefficients of (1+2x)^M.

### 4.1 Weighted elementary-symmetric upper bound

For L nonnegative weights w_i of sum L times wbar, the elementary symmetric
polynomial satisfies e_t(w)/binom(L,t)<=wbar^t. One proof repeatedly replaces
two weights by their average. With their sum fixed, e_t depends on them as
w_i w_j e_(t-2)(others)+(w_i+w_j)e_(t-1)(others)+e_t(others), which cannot
decrease under averaging. Repeated averaging converges to equal weights;
continuity yields the bound. Cases t=0,1 are immediate.

Apply this to M weights: A(S) copies of 1 and M-A(S) copies of 2. For
c_l=[x^l](1+x)^A(1+2x)^(M-A),

    c_l <= binom(M,l) 2^l (1-A/(2M))^l.                 (4.1)

### 4.2 Each nonempty-core summand is exponentially small in the middle

Suppose floor(M/2)<=k<=3M/4 and 0<=j<=r-d(S). Since s+j<=q<=M/24,

    l=k-s-j >= floor(M/2)-q >= M/3.

Here M>=24 follows from the theorem premises; the last inequality follows
from M/2-1-M/24>=M/3 for M>=8. Furthermore

 binom(M,k-s-j) 2^(k-s-j) / b_k
   = product_(i=0)^(s+j-1) (k-i)/(2(M-k+i+1))
   <= (3/2)^(s+j).

Using 1-u<=exp(-u), (4.1), and A>=as gives

 c_(k-s-j)/b_k <= (3/2)^(s+j) exp(-A/6)
               <= (3/2)^(s+j) 2^(-floor(a/6)*s).        (4.2)

The last step uses e>2 and a/6>=floor(a/6). Summing over the j free original
vertices produces a factor at most (1+3/2)^r=(5/2)^r. Summing over every
nonempty independent S, and upper-bounding their number by all subsets of H,
therefore proves

    0 <= E_k <= b_k (5/2)^r rho
    for floor(M/2)<=k<=3M/4.                            (4.3)

This is a coefficientwise *middle-range* bound. It is not just a total-mass
bound that could hide a far-away valley.

### 4.3 A nonzero baseline difference cannot be arbitrarily small

For k<M write

 Q_k/b_k = sum_(j=0)^r binom(r,j) 2^(-j)
                   (k)_j / (M-k+1)^(overline j),        (4.4)

where (k)_j is falling factorial, and the denominator is rising factorial;
terms with j>k vanish. For Q_(k+1)/b_k the j=0 term is 2(M-k)/(k+1), and for
j>=1 the term is

    binom(r,j) 2^(1-j) (k)_(j-1)/(M-k+1)^(overline(j-1)).

Thus (Q_(k+1)-Q_k)/b_k is a rational number whose denominator divides

    D_k=2^r (k+1) product_(j=1)^r (M-k+j).

If that difference is nonzero, its absolute value is at least 1/D_k. In the
middle range D_k<=2^r(M+r+1)^(r+1), hence

 |Q_(k+1)-Q_k| >= b_k/[2^r(M+r+1)^(r+1)].               (4.5)

This arithmetical gap avoids an unsupported approximation to the location of
the mode. It is valid even when the mode changes with parameters.

## 5. Proof of Theorem 3.1: early range, middle range, complete tail

Each summand in (2.1) is a shifted product of M+r-d(S) positive linear
factors with weights 1 or 2. Double-counting weighted subsets gives

    (l+1)c_(l+1) >= (M-l)c_l.

Therefore every summand is nondecreasing at k<floor(M/2); leading zeros are
harmless, and Q makes the whole sum strictly increasing there.

For the decorated graph, alpha=M+alpha(C)<=M+q. The expression in (1.1)
increases with alpha, so

 beta <= ceil((M+q)(2M+q-1)/(3M+2q))
      <= ceil(2(M+q)/3)
      <= 25M/36+1 <= 3M/4.                              (5.1)

We used q<=M/24 and M>=24. Thus every middle difference from floor(M/2) to
beta-1 has both coefficient indices covered by (4.3). Also
b_(k+1)/b_k=2(M-k)/(k+1)<=2 in this range. Nonnegativity of E gives

 |E_(k+1)-E_k| <= max(E_(k+1),E_k)
                 <= 2 b_k(5/2)^r rho
                 < b_k/[2^r(M+r+1)^(r+1)].              (5.2)

By (4.5), whenever Delta Q_k is nonzero in that middle range,
Delta P_k has its sign. At a zero of Delta Q_k, the
sign of Delta P_k is deliberately left uncontrolled.

Q is strictly LC on internal positive indices. For completeness, multiplication
of a positive LC sequence a by 1+wx preserves LC because its minor is

 L_i(a) + w(a_i a_(i-1)-a_(i-2)a_(i+1)) + w^2 L_(i-1)(a).

All terms are nonnegative by ratio monotonicity; beginning with the strictly
LC binomial sequence and treating the new endpoint separately gives strict
LC for Q. Hence its successive ratios strictly decrease, so its differences
have positive signs, at most one zero, then negative signs. There cannot be
two separated baseline zero differences in the middle.

It follows that P_D has no strict descent followed by a rise before beta:
its early part increases; in the middle all strict baseline signs persist,
and the single possible undecided difference cannot create a valley between
a positive portion and a negative portion. At and after beta, (1.1) gives
weak decrease for the actual decorated graph. These ranges cover the full
positive support, and padded zero coefficients cannot create a rebound.
This proves complete unimodality, including plateaus. QED.

## 6. Why this handles true exterior information, and what it still does not

The proof uses the whole core C, not only messages at one selected root.
It retains all internal vertices and all components through (2.1); it never
cancels an exterior polynomial in a coefficient comparison. The correction
also includes core edges between two vertices of H via the independent-S
restriction and all edges into W via d(S).

Nevertheless, arbitrary attached exteriors are NOT automatically safe. An
attachment made after selecting a cover may create an edge with neither end
in H. Even when H is still a cover, q,r,beta and the bound change. The cover
and private-arm hypotheses must be verified again for the completed graph.
Replacing an uncovered external edge by an absent edge to retain (2.1) would
be invalid. A fixed tree with arbitrary uncoated attachments is not proved
unimodal merely because a smaller part satisfies (3.1).

The theorem covers whole completed forests meeting (3.1). No rule is proved
that transforms EVERY remaining minimal counterexample into one of them while
preserving non-unimodality. Adding private paths changes the graph; proving
the changed graph good does not prove the original core good.

## 7. An explicit region with arbitrary core size and component count

**Corollary 7.1.** For every q>=1, every core C and every nonempty vertex
cover H, give every vertex of H the same integer number a of private arms.
Then every integer

    a >= 192(q+1)^2                                    (7.1)

satisfies Theorem 3.1. This bound is deliberately sufficient, not optimal.

Proof. Put d=q+1 and z=floor(a/6)>=32d^2. Then M=ha>=24q and a>=24.
Let y=(3/2)2^(-z). We have hy<=1/2 (for example z>=q+2 and 2^q>=q).
The binomial bound (1+y)^h-1<=hy/(1-hy)<=2hy gives rho<=3h2^(-z).
Since a<6(z+1), M+r+1<=14dz. The left side of (3.1) is at most

    6q * 5^q * (14dz)^d * 2^(-z).                      (7.2)

For integer z>=32d^2, z^d 2^(-z) is decreasing. Indeed its successive ratio
is (1+1/z)^d/2 <= 1/[2(1-d/z)]<1 when z>2d. At z=32d^2, (7.2) is at most

    8d * 2^(12d) * d^(3d) * 2^(-32d^2) < 1,

because log2(d)<=d implies the base-two logarithm is at most
3+13d-29d^2<0. This proves (7.1) for all integers a, not only multiples of
six and not just a finite list. QED.

**Corollary 7.2: genuinely non-LC large-component products.** Take C to be
the disjoint union of t three-leaf stars, and H to be their 3t leaves. Then
D is the disjoint union of t trees T(a,a,a) from Phase 9. Formula (7.1), with
q=4t, proves unimodality of their product whenever

    t>=1,    a>=192(4t+1)^2.                            (7.3)

Every component is non-LC in this range, not just potentially non-LC. With
A=2^a+a and B=a2^(a-1)+binom(a,2), the penultimate minor of T(a,a,a) is

    6A^2 - 2^(3a) - 3B < 0    for a>=6.

Indeed A<=2^(a+1), so 6A^2<=24*2^(2a)<2^(3a) for 2^a>24. This is the
previous explicit top-coefficient calculation, not an original valley.
Thus (7.3) covers arbitrarily many actually non-LC tree components without
assuming the invalid general rule "unimodal times unimodal is unimodal".
The theorem does NOT cover all products of these trees for all a or all
arbitrary non-LC component shapes.

## 8. Unrestricted remaining case: root mixtures and allocation budgets

For the general forest, use the previous actual availability variables:
T(S)=|V(F)\N[S]|, M(S)=|E(F-N[S])| over uniform independent k-sets. Write
mu=E T, v=Var T, eta=E M. Incidence counts give

    mu=(k+1)p_(k+1)/p_k,
    E[T(T-1)-2M]=(k+1)(k+2)p_(k+2)/p_k.

Consequently the proposed no-rebound slack is also

 B_k = mu(k+3-mu)+2eta-v
     = E[(k+3)T-T^2+2M]
     = (k+1)(k+2)(p_(k+1)-p_(k+2))/p_k.               (8.1)

For a root-state partition, this last expectation is the probability-weighted
sum of the *actual whole-forest* conditional budgets. It does not follow that
each root-state budget is nonnegative. Nor can root-absent availability be
identified with availability in F-r: the absent root can itself still be an
available vertex when no neighbor was selected.

For a size allocation K among components, let u(K) be the sum of conditional
component means, w(K) the sum of their conditional variances, and e(K) the
sum of their residual-edge means. The exact whole budget is

    B_k = E_K[(k+3)u(K)-u(K)^2+2e(K)-w(K)].             (8.2)

Equivalently Var(T)=E_K[w(K)]+Var_K[u(K)]. Thus allocation variance is
retained, not set to zero. Our material checks group the first actual
component versus the union of ALL remaining components, compare every
possible allocation to those two groups, and verify the identity exactly.
Root-state conditional moment jets are also verified by literal subset
counts on small controls. These are identities/diagnostics, NOT a proof of
B_k>=0 from mu<=k+1 and k+1<beta.

The first substantive missing implication remains a forest-specific bound
on (8.1)/(8.2), or another direct contradiction excluding a real valley in
all remaining forests. A root recurrence, a renamed inequality, or a finite
set of positive budgets does not establish it. Plateaus still require the
weak-descent premise for iteration. HEREDITARY is not inferred from LOCAL.

## 9. Evidence and original-proof boundary

Native source independently checks complete polynomial correspondence and
middle sign control on four explicit theorem controls, including one forest
with two non-LC components. The uniform proof above, not the finite checks,
supplies the unbounded cover of its stated parameter region. These much
larger formula controls are not an all-order census and do not receive a
claim of all-vertex conditional recounts.

A separate fixed, seeded study explores arbitrary Prüfer/core tree shapes,
whole-subtree relocations, attached true exteriors at one or two sites, and
2..7 actual non-LC large components. It does NOT impose the private-arm
criterion. Every accepted P is counted by two graph algorithms; every
vertex A/B is computed; material conditional and edge-moment recount scopes
are explicit in SEARCH_SUMMARY. No graph is merged merely for equal root
polynomials. Repeated types and marked operations are not new coverage.

The study found no actual valley, prefix failure, BARRIER violation or U/D
residual pair. All new HEREDITARY labels remain UNKNOWN. The theorem does
exclude an explicit additional unbounded whole-forest class, including
non-LC products; it is not a classification of every original counterexample.
No full ORIGINAL proof, original counterexample, global minimum, Lean build,
axiom audit, independent external review, or global novelty is claimed.
