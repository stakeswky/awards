## 9. A single explicit threshold, not a finite sample or an existential N

Every n-dependent summand in E(n) decreases with n. For n>=2^2600000, the
slow term has exponent

 154-2600000/15992 = -17154/1999 < -8.

The other four n-dependent exponents are

 199-2600000/4      = -649801,
 207-2600000/1999   = -2186207/1999,
 211-2600000/7996   = -228211/1999,
 11-2600000        = -2599989.

Each is below -12, as is the constant tail exponent -167. Therefore

 E(n)<2^(-8)+5*2^(-12)=21/4096<1/128<1/sqrt(2pi).            (9.1)

Indeed 1/sqrt(2pi)>1/3 since pi<4. Thus D_n>1/3-1/128=125/384>0.
No decimal evaluation at the astronomical n is needed: all comparisons in
this section reduce to small signed integers. There is no untracked
'choose sufficiently large' constant anywhere in Sections 2--9.

Positive D_n implies 2 pi_j>pi_(j-1)+pi_(j+1); arithmetic-geometric mean then
gives pi_j^2>pi_(j-1)pi_(j+1). Since

 pi_j^2-pi_(j-1)pi_(j+1)
   =lambda^(2j)/Z_F(lambda)^2 * (i_j^2-i_(j-1)i_(j+1)),      (9.2)

the same strict log-concavity holds for the independence coefficients at every
integer j which can be the mean for an activity in K.

## 10. Effective endpoint mean bracket (the wider paper interval)

This is the finite mean-range argument of [FLNYZ, Section 7], with its sole
numerical comparison verified by rational enclosures. Every vertex has
occupation probability <=lambda/(1+lambda), so mu(1/4)<=n/5.

At activity1, root each tree component, with descendant odds r_v<=1. The
partition product gives log Z(1)=sum_v log(1+r_v). For a nonroot vertex, the
parent-side odds s_v<=1 imply its WHOLE-FOREST marginal is
r_v/(1+r_v+s_v)>=r_v/(2+r_v). Roots use s_v=0.
The function f(r)=(2+r)log(1+r)/r increases on 0<r<=1: after multiplying its
derivative by r^2 the numerator is
r(r+2)/(1+r)-2log(1+r), whose derivative is r^2/(1+r)^2>=0 and whose value
at0 is0. Thus log Z(1)<=3log 2*mu(1).

Let Q(lambda)=log Z(lambda)/mu(lambda). For bipartite graphs, averaging the
two conditional Bernoulli variance bounds gives sigma^2>=mu/[2(1+lambda)].
Using lambda d(log Z)/d lambda=mu and lambda d mu/d lambda=sigma^2, we get

 lambda Q'(lambda)<=1-Q(lambda)/[2(1+lambda)].

Multiplying by sqrt(lambda/(1+lambda)) and integrating from1 gives

 Q(lambda)<=sqrt((1+lambda)/lambda)
 [3log 2/sqrt(2)+2log((sqrt(lambda)+sqrt(1+lambda))/(1+sqrt(2)))].

The value on the right at12 is Qstar. Subsets of a maximum independent set
give Z(12)>=13^alpha, hence

 mu(12)>=alpha log(13)/Qstar > (17/25)alpha.                 (10.1)

Both independent arithmetic implementations certify

 680891044148/10^12 < log(13)/Qstar < 680891044149/10^12,

so the comparison with17/25 has a positive rational margin. Square roots
are enclosed by integer-square inequalities. Logarithms use, with 0<=z<1,

 log x=2 sum_(r=0)^(m-1) z^(2r+1)/(2r+1)+R_m,
 z=(x-1)/(x+1),   0<=R_m<=2z^(2m+1)/[(2m+1)(1-z^2)].       (10.2)

One program uses exact fractions; the other uses outward-rounded integer
fixed-point intervals. They do not infer the continuous bound from decimal
grid values. sqrt and log monotonicity propagate the enclosures in Qstar.

For every nonempty graph, mu is continuous and strictly increasing in lambda,
because lambda mu'=sigma^2>0. Every integer in [n/5,17alpha/25] is therefore
attained at an activity in K. It lies inside positive support. Applying
Section9 proves (1.3) with the explicit N_LC in(1.2).
The weaker upper endpoint64alpha/95 follows as well; no claim is made that
this new finite proof or its constants have been formalized in the external Lean.

## 11. Finite prefix, finite tail and their explicit joins

For completeness the finite graph facts used here are supplied, rather than
hidden in an asymptotic statement. They are [FLNYZ, Lemma8.1/Proposition8.2]
(and the cited classical bipartite decreasing-tail result).

For a rooted tree let A_i=Z_(T_i), B_i=Z_(T_i-r_i), U_i=A_i-B_i>=0 coefficientwise.
Define
 D_T=sum_(J independent)(2|J|-sum_(v in J)deg_T(v)-2*1_(r in J))x^|J|,
 E_T=sum_(J independent,r notin J)(2|J|-sum_(v in J)deg_T(v)-1)x^|J|
                                                +Z_(T-N[r]).
Both are zero for a singleton. Partitioning by r absent/present and expanding
products gives

 D_T=sum_i D_(T_i) product_(j!=i) A_j
     +sum_i U_i[product_(j!=i)A_j-product_(j!=i)B_j]
     +x sum_i E_(T_i) product_(j!=i) B_j,
 E_T=sum_i D_(T_i) product_(j!=i) A_j
     +sum_(S subset children,|S|>=2)(|S|-1) product_(i in S)U_i
                                                    product_(i notin S)B_i.

To check the first recurrence: absent-root sets have sum of child scores
plus one child-root indicator, giving sum_i(D_i+U_i)prod A_j; occupied-root
sets contribute x sum_i E_i prod B_j - sum_i U_i prod B_j. Adding yields it.
For the second, expand sum_i U_i prod_(j!=i)(B_j+U_j)-prod_i(B_i+U_i)+prod_iB_i:
a nonempty subset S has coefficient |S|-1. Every displayed contribution is
nonnegative under induction. Thus D_T,E_T have nonnegative coefficients.
Multiplying D_T by the other complete component polynomials and summing gives,
for a uniform independent k-set J of any forest,

                 E sum_(v in J)deg_F(v)<=2k.

The number of vertices which can be adjoined to J is at least
n-k-sum_(v in J)deg(v). Double counting its one-point extensions proves
(k+1)i_(k+1)>=(n-3k)i_k, so the sequence is nondecreasing through ceil(n/4).
For the tail, the residual after deleting N[J] is bipartite and has independence
number at most alpha-k, so at most 2(alpha-k) vertices. The same extension
count proves (k+1)i_(k+1)<=2(alpha-k)i_k and gives nonincrease from
ceil((2alpha-1)/3). All support endpoints are included with zero padding.

For n>=1000 and alpha>=n/2, these finite intervals overlap the central one:

 ceil(n/5)<=ceil(n/4)<ceil((2alpha-1)/3)<=floor(17alpha/25).

For the strict middle inequality use ceil(n/4)<=n/4+1<(n-1)/3.
For the final inequality, ceil((2alpha-1)/3)<(2alpha+2)/3<=17alpha/25
when alpha>=50. Thus n>=1000 is more than sufficient FOR THESE JOINS ONLY.
The analogous last join for64/95 already holds at alpha>=95, since
64/95-2/3=2/285. These elementary bounds do not replace the analytic cutoff.

Within the LC interval the successive positive ratios decrease. Before it
meets the prefix no decrease occurs; after it meets the tail no rise occurs.
Consequently no strict fall can be followed by a strict rise, including a
plateau between them. Since (1.2) exceeds1000, take N_unimodal=N_LC.

## 12. Relation to the project history target and remaining finite orders

For the project's whole-component M and beta, h<=k and s=k+1<beta imply
n/5<s<2alpha/3<64alpha/95<17alpha/25. The lower bound follows from
h>(n-1)/4 and s>=h+1. For the upper bound, integrality gives
s<alpha(n-1)/(n+alpha)<2alpha/3 using alpha>=n/2.
Thus for n>=N_LC, actual current nonincrease i_s<=i_(s-1) yields

 i_(s-1)(i_s-i_(s+1))=L_s+i_s(i_(s-1)-i_s)>0.

This pays the ENTIRE tau and hence the no-rebound target, without requiring
some root to have both conditional budgets nonnegative. All existing root
identities, their negative correction, and the full adjacent-edge remainders
remain valid; no individual positive contribution is re-spent across roots.
The new proof uses the actual activity law on the whole graph, with all
component and root-state mixing explicitly tracked in Sections3--8.

What is now explicit is the finite order range n<2^2600000. It has not been
exhausted. The component-order-30 prior result, wherever invoked, retains
its original external/computational dependencies and does not cover every
forest in this range. No all-size ORIGINAL closure, A4-R proof, or legal
original counterexample is established in this run.

## Sources and exact evidence boundary

[FLNYZ] E. X. Fang, J. Lu, E. Nevo, Y. Yao and H. Zheng, Unimodality of
Independence Polynomials for Sufficiently Large Forests, arXiv:2609.20961v1,
https://arxiv.org/html/2609.20961v1 (official full HTML read).
The original theorem/strategy belongs to those authors. Sections2--5 and7
above expose constants in their recurrences; Section6 gives a self-contained
finite replacement for their Berry--Esseen/qualitative-limit step. Sections8--11
supply an explicit cutoff and a certified wider-endpoint comparison. Prior
A8 and C8 used the same external theorem only existentially; they are not
independent discoveries of it. The paper's finite endpoint facts were proved
again above with attribution. No original PDF/TeX bytes or hash is asserted.

The exact constant certificates verify (2.4),(2.5), moment/centroid constants,
interval arithmetic, exponent comparisons and the cutoff magnitude. Small graph
checks are regressions for the conditioning and centroid identities, not the
source of any uniform inequality. No graph of order near the cutoff was tested.
Formal source was read at its actual pinned HEAD for interface comparison;
Lean compilation, axiom audit and independent external review: NOT_RUN.
