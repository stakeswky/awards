# Window C Round 4: signed budgets and a finite-palette closure theorem

ORIGINAL = NOT_CLOSED. C4-F = NOT_CLOSED. The uniform result below has an
explicit restricted component palette. No global novelty is claimed.

## 1. Definitions and the exact scope

F is a finite, simple, undirected, unweighted forest. Its independence
polynomial is P_F(x)=sum_j p_j(F)x^j. If alpha is its independence number,
p_j>0 for 0<=j<=alpha: take subsets of a maximum independent set. Outside
this interval p_j=0. Unimodality permits plateaus, and is equivalent to the
absence of a strict descent followed later by a strict rise.

For 0<=j<=alpha, set mu_F(j)=(j+1)p_(j+1)/p_j and d_F(j)=j+1-mu_F(j).
For j<alpha, e_F(j)=mu_F(j+1)-mu_F(j)-1. In particular mu_F(alpha)=0.
For a uniform independent j-set S in F, let H=F-N_F[S], T=|V(H)| and c=c(H).
All residuals and neighborhoods are computed in the ORIGINAL F. Define

    sigma_F(j)=4mu_F(j)-Var(T)-2E[c],
    G_F(j)=sigma_F(j)+mu_F(j)d_F(j).

History(F,k) means there is i<=k with p_(i+1)<p_i, and p_(t+1)<=p_t for
every i<=t<=k. It is not inferred from a floating-point near-equality.
The common middle range is h<=k and k+1<beta, where

    h=floor(M(n-1)/(4M-2))+1,
    beta=ceil(alpha(n-1)/(n+alpha)),

and M is the largest component order of the completed graph. These range
formulas are used for reporting the targeted tests, not as an external
assumption needed to prove our palette theorem. No component-order-30
computation or unproved Window A no-rebound assertion is used below.

## 2. Derive the budget from actual forest counting

Double counting pairs (S,v) with v available gives E[T]=mu_F(j). For each
residual forest, |E(H)|=T-c, so its number of independent two-sets satisfies

    2p_2(H)=T(T-1)-2|E(H)|=T^2-3T+2c.

Each independent (j+2)-set in F has binom(j+2,2) choices of the two new
vertices outside S. Therefore

    E[T^2]-3mu+2E[c]=(j+1)(j+2)p_(j+2)/p_j,
    sigma=mu+mu^2-(j+1)(j+2)p_(j+2)/p_j.                 (2.1)

For j<alpha this is sigma=mu(1+mu-mu_(j+1))=-mu e_j.
At j=alpha, every maximum independent set is maximal, T=c=0, and sigma=0.
There is no need to form an undefined ratio beyond the support. Consequently

    G_F(j)=(j+1)(j+2)[p_(j+1)-p_(j+2)]/p_j.            (2.2)

For j<alpha, G=mu(d-e). Under History, G<0 is exactly a subsequent rise
p_(j+2)>p_(j+1), hence an ORIGINAL counterexample. By contrast e>0 alone
just refutes the stronger C1 bound. No division by d is used, including at
plateaus d=0. The normalized next decline is

    (d-e)/(j+2)=1-p_(j+2)/p_(j+1),                     (2.3)

where p_(j+1)>0. These are identities, not inequalities.

## 3. Whole-component partition and refinement conservation

Partition F into nonempty complete component subunions Z_1,...,Z_r. Given
an allocation a_1+...+a_r=k, the selected sets in the Z_i are independent
and uniform at their respective sizes. Every supported allocation has weight

    w_a = product_i p_(a_i)(Z_i)/p_k(F).

These are graph-count weights, not arbitrary probabilities. Put
m_a=sum_i mu_(a_i)(Z_i). Residual vertex and component counts add across
blocks. Conditional independence and the law of total variance yield

    mu_F=E_w[m],
    Var(T_F)=E_w[sum_i Var(T_i)]+Var_w(m),
    sigma_F=E_w[sum_i sigma_i]-Var_w(m).

Thus, with R_P=E_w[sum_i sigma_i]+mu_F d_F and V_P=Var_w(m),

    R_P-V_P=G_F(k).                                    (3.1)

Every supported allocation is included, including local endpoints mu=0
and all locally negative sigma terms. Global history and global middle
position impose NO corresponding local-history or local-middle assumptions.

Let Q refine partition P. The coarse conditional mean is the conditional
expectation of the fine mean. The variance decomposition therefore gives

    V_Q-V_P=E[Var(m_Q | coarse allocation)] >= 0.

Applying (3.1) to both partitions shows the exact same transfer in budget:

    R_Q-R_P=V_Q-V_P.                                   (3.2)

This proves the multiblock interface directly for any r, without an induction
that presumes unknown local histories. In particular, for the exact variance,

    (there exists P with R_P>=V_P)
       iff G_F(k)>=0 iff (every P has R_P>=V_P).         (3.3)

Choosing a different split or refining it can change an auxiliary upper bound,
but cannot change the real deficit. This is a limitation of that strategy,
not a forest-wide proof of the missing nonnegativity.

## 4. Signed two-block kernel and the price of removing cancellations

For F=X disjoint-union Y, let A_a=p_a(X), B_b=p_b(Y), and
lo=max(0,k-alpha_Y), hi=min(k,alpha_X). Define w_a=A_a B_(k-a)/p_k(F),
m_a=mu_X(a)+mu_Y(k-a), delta_t=m_(t+1)-m_t for lo<=t<hi, and
F_t=sum_(a<=t)w_a. Empty sums are zero.

Write m_a=m_lo+sum_t delta_t 1_(a>t). The covariance of 1_(a>s) and
1_(a>t) is K_st=F_min(s,t)(1-F_max(s,t)). Hence

    V=Var_w(m)=sum_(s,t)delta_s delta_t K_st.            (4.1)

The increments can have both signs. Define V_abs by replacing delta_s delta_t
with its absolute value in (4.1), and define the inherited Cauchy bound

    U_var=sum_t delta_t^2 sum_(a<=t<b)w_a w_b(b-a).

The pair-variance identity gives V=sum_(a<b)w_a w_b(m_b-m_a)^2. On each
interval, Cauchy gives (sum delta)^2<=(b-a)sum delta^2, so V<=U_var.
The triangle inequality gives V<=V_abs, and exactly

    V_abs-V=4 sum_(s<t,delta_s delta_t<0)
                     |delta_s delta_t| F_s(1-F_t).     (4.2)

The factor four counts both symmetric ordered kernel entries and the change
from a negative product to a positive one. Equation (4.2) is the lost signed
cancellation, not an amount already known to be affordable.

Actual weights and increments also satisfy, whenever adjacent allocations
are in the positive support,

    w_(a+1)/w_a=(k-a)mu_X(a)/[(a+1)mu_Y(k-a-1)],
    delta_a=e_X(a)-e_Y(k-a-1).                          (4.3)

The first denominator is positive in this adjacent-support situation; local
terminal mu values elsewhere are retained as zero. We checked (4.3) on the
actual allocations. Neither (4.1) nor (4.3), by itself, proves R>=V. This
work makes NO unrestricted claim that V_abs<=R or U_var<=R. The tests of
these stronger inequalities are regression controls only.

## 5. An elementary LC-times-unimodal lemma

Let a be a finite nonnegative sequence with interval positive support and
log-concavity a_i^2>=a_(i-1)a_(i+1). Let b be finite, nonnegative and unimodal.
Both are extended by zeros to all integer indices. We prove a*b unimodal.

First, for k<l and j<t, log-concavity implies

    a_(l-j) a_(k-t) <= a_(k-j) a_(l-t).                (5.1)

The two indices on the left are the extreme ones, and the two on the right
are between them with the same total. Ratio monotonicity on the positive
support proves (5.1) by moving the extreme indices inward. If the left side
is zero the claim is immediate; otherwise all intermediate indices are in
the interval support. Thus this also handles boundary zeros.

Choose m so that d_j=b_j-b_(j-1)>=0 for j<=m and d_j<=0 for j>m. Set

    P_k=sum_(j<=m) d_j a_(k-j),
    N_k=sum_(t>m) (-d_t) a_(k-t).

Then (a*b)_k-(a*b)_(k-1)=P_k-N_k. Multiply (5.1) by d_j(-d_t)>=0 and sum:

    P_l N_k <= P_k N_l  for k<l.                      (5.2)

If P_k<N_k, then N_k>0. For every l>k, (5.2) implies P_l<=N_l: when
N_l>0 divide by N_k and use P_k/N_k<1; when N_l=0 it forces P_l=0.
A strict decline is therefore never followed by a strict rise. This proves
the lemma including all plateaus and boundary cases. The zero sequence is
trivial. No external convolution theorem is needed as an unproved dependency.

## 6. Four actual non-LC tree types

For lists a=(a_1,...,a_t), l=(l_1,...,l_t), construct a central vertex r
adjacent to t distinct hubs. Hub j has a_j private paths of length two and
l_j private leaves, with all new vertices distinct and no further edges.
This is an ordinary unweighted tree. Classifying its independent sets by
whether r and each hub are selected gives

    P_(a;l)(x) = product_j[(1+2x)^(a_j)(1+x)^(l_j)
                                  +x(1+x)^(a_j)]
                +x(1+2x)^(sum a_j)(1+x)^(sum l_j).     (6.1)

There is no missing exterior in this formula. It defines only the specified
complete trees. An absent hub permits both endpoints of each private edge;
a present hub forbids its adjacent endpoints and direct leaves. This proves
the coefficient-to-graph correspondence in (6.1).

Use the following palette (indices are used in the certificate):

| Index | Name | Arms a | Leaves l | Vertices | alpha | Negative LC indices |
|---|---|---|---|---:|---:|---|
| 0 | T26 | [3,4,4] | [0,0,0] | 26 | 14 | 13 |
| 1 | B212 | [6,7,7,7] followed by nine 8s | thirteen zeros | 212 | 112 | 101 |
| 2 | B226 | [0] followed by thirteen 8s | [3] followed by thirteen zeros | 226 | 120 | 109 |
| 3 | B239 | fourteen 8s | fourteen zeros | 239 | 126 | 114 |

All four whole sequences are unimodal but not LC. B212 and B226 are distinct
historical constructions, not successive stages of one reduction chain.
Their historical equality statistics are not used or combined here. The
B239 bush is attributed prior work, not claimed as a new graph discovery.

## 7. A finite LC-blocker certificate

For a multiset t of palette indices, let P_t be the product of its actual
graph polynomials. Let H_r consist of size-r multisets for which EVERY
nonempty submultiset has a non-LC polynomial. At size one test all four types.
At size r>=2, a candidate can lie in H_r only if each one-element deletion
lies in H_(r-1). Conversely this condition means all proper nonempty
submultisets are non-LC. Test the candidate itself: LC candidates become
minimal blockers, and non-LC candidates enter H_r. Test their whole-sequence
unimodality too. Repeated types are handled as multisets, not ordered tuples.

The exact certificate has these counts:

| Size | Candidate multisets counted as graphs | Retained non-LC H_r | Minimal LC blockers |
|---:|---:|---:|---:|
| 1 | 4 | 4 | 0 |
| 2 | 10 | 9 | 1 |
| 3 | 16 | 13 | 3 |
| 4 | 16 | 1 | 15 |
| 5 | 0 | 0 | 0 |

All 27 retained non-LC configurations are unimodal. The only member of H_4
is (0,2,2,2), namely T26 disjoint-union three B226 trees, with 704 vertices.
Its negative LC index is 339; non-LC is not a unimodality failure.

The complete 19 minimal LC blockers are

    00;
    111, 112, 113;
    0122, 0123, 0133, 0223, 0233, 0333,
    1222, 1223, 1233, 1333,
    2222, 2223, 2233, 2333, 3333.                     (7.1)

Here, for example, 0122 means one component of type 0, one of type 1 and
two of type 2. This is a list of component types, not graph vertex labels.

No size-five multiset has every size-four deletion equal to (0,2,2,2): a
multiset with at least two distinct types has two different deletion
multisets; one with only one type cannot have that deletion. This proves
H_5 is empty from the sole H_4 member. As a second finite combinatorial
check, the program visits ALL 56 size-five multisets and verifies each
contains a blocker in (7.1). These 56 are not additional graph recounts.
For any size>5, taking any five components proves that it too contains a
blocker of size at most four.

The graph certificate records all 46 candidates, their actual edge lists,
all 14,406 integer coefficients and every LC minor. Every complete array
was freshly computed in three ways: explicit (6.1), rooted graph DP, and
vertex deletion with component factorization. The deletion implementation
uses a separate carry-free integer multiplication algorithm. The supplied
standard-library source regenerates the certificate, not just its hashes.
This is a finite computer-assisted part of a uniform theorem, not a claim
that checking a few ordinary products proves the unrestricted conjecture.

## 8. Complete induction for arbitrary multiplicities

THEOREM. Every finite disjoint multiset of the four trees in Section 6 has
a unimodal independence sequence. The same is true after disjoint union
with any forest having an LC whole independence polynomial.

Proof by the number r of palette components. The empty multiset is [1].
If the multiset contains a blocker s from (7.1), its polynomial is LC.
If s is the entire multiset, it is unimodal. Otherwise its complement has
fewer components, is unimodal by induction, and Section 5 proves that the
full product is unimodal. If the multiset contains no blocker, Section 7
shows it has at most four elements and is one of the 27 retained configurations,
each of which the exact certificate proves unimodal. This proves every r,
without an assumption about any local descent history. Finally apply
Section 5 once more to the arbitrary LC exterior factor. QED.

REAL BUDGET COROLLARY. For every forest in this theorem, every partition
into complete component subunions, and every actual History(F,k) with
k<alpha, R_P>=V_P. Indeed unimodality and History imply p_(k+2)<=p_(k+1),
and (2.2)--(3.1) give the claimed comparison. This applies at every supported
history position, so in particular at h<=k, k+1<beta. It does not assert
V_abs<=R or U_var<=R and does not delete negative local budgets.

The theorem is not being proved by restating the budget identity: Sections
5--8 establish unimodality separately using the LC blockers and induction.
Only then is the exact budget corollary taken.

## 9. Implications for the common minimum-counterexample framework

Suppose F is an ACTUAL vertex-minimal non-unimodal forest. Every proper
induced subforest is then unimodal. A nonempty proper union X of complete
components cannot have an LC polynomial, because its complementary induced
forest Y is smaller and unimodal; Section 5 would make F=X disjoint-union Y
unimodal. If X=F is LC, F is good directly.

Therefore none of the 19 patterns (7.1) can occur among complete components
of F, EVEN WHEN OTHER COMPONENTS HAVE ARBITRARY SHAPES. This is a conditional
structural exclusion for a minimum bad graph, not a claim of unimodality
for an arbitrary graph with an arbitrary non-LC exterior.

In particular F has at most four components drawn from our palette. If it
has four, they must be (0,2,2,2). The individual multiplicity bounds include
at most one T26, at most two B212, at most three B226 and at most three B239;
the mixed blockers impose stronger simultaneous restrictions. If every
component belongs to the palette, Section 8 excludes F entirely.

HEREDITARY is used exactly in the assertion that the proper complement Y
is unimodal. We do not infer HEREDITARY for any ordinary large test graph
from its whole-sequence test, from LOCAL checks, or from the palette theorem.

## 10. What remains unproved

C4-F asks for ALL disconnected forests under HEREDITARY, not only the
palette or the blocker exclusions above. For arbitrary component types,
we have not proved that an LC proper component subunion must exist, and
not proved R_P>=V_P when it does not. In particular a putative minimum bad
forest made from new non-LC component types is not covered by the finite
certificate. The exact signed kernel, compatible weights and HEREDITARY
have not been connected by a general budget-paying inequality.

The claim "choose a paying exact partition" does not weaken this missing
step, by (3.3). A newly tightened variance upper bound alone would not close
it either. No full ORIGINAL counterexample or proof is asserted.

These results concern whole graphs and whole-component unions. They do not
automatically apply to root-selected/root-absent conditional availability
in an original graph. In particular an unselected root may still be available;
it cannot simply be deleted when importing this budget formula. Independent
ordinary residual-graph counts can be used only after that distinction is
proved for the proposed interface. No unproved root correction is used here.
