# Window A Round 5: full-mass signed root compensation

**ORIGINAL = NOT_CLOSED. A4-T and A4-R remain UNPROVED.**
This document proves a conditional signed coefficient bound and an actual
adjacent-edge compatibility identity. It does not prove that HEREDITARY
supplies a paying bound for every tree. No new universal forest exclusion,
external peer review, formal verification, or literature priority is claimed.

## 1. Graphs, history, and the statement still sought

A graph here is finite, simple, undirected and unweighted. For a forest F,
p_i counts independent vertex sets of size i, p_0=1, and p_i=0 outside
0,...,alpha. All coefficients in this interval are positive: use subsets of
one maximum independent set. A sequence is unimodal, allowing plateaus,
exactly when there is no strictly negative adjacent difference followed by
a strictly positive one. Write Delta_k=p_(k+1)-p_k.

History(F,k) means that some i<=k has Delta_i<0 and every Delta_t for
 i<=t<=k is nonpositive. The cases i=k and i<k are recorded separately.
For p_k>0 put mu_k=(k+1)p_(k+1)/p_k. For k<alpha put
 d_k=k+1-mu_k and e_k=mu_(k+1)-mu_k-1.
Thus d_(k+1)=d_k-e_k. The true next-step target is e_k<=d_k, not e_k<=0.
No division by d_k is allowed at a plateau.

For reporting, use the actual n, largest component order M, and
 h=floor(M(n-1)/(4M-2))+1,
 beta=ceil(alpha(n-1)/(n+alpha)).
The inherited initial-prefix result and Basit--Galvin tail theorem restrict
a possible first rebound to h<=k, k+1<beta. The new algebra below does not
need either endpoint theorem. The empty forest and singleton are direct.

A4-T asks: if T is connected and ALL proper induced subforests are unimodal
(HEREDITARY), must T be unimodal? A hypothetical vertex-minimal bad forest
supplies the stronger premise that every smaller forest is unimodal. It
need not be connected; the connected case is this window's target. Neither
C's unproved general component closure nor D's unproved ADMC is assumed.

## 2. The root decomposition retains all mass

For any actual vertex r let A=T-r, J=T-N_T[r]. Set
 a_i=p_i(A), b_i=p_(i-1)(J), and P=a+b.
The partition into sets excluding/including r proves this equality. Every
edge and exterior branch in the induced graphs remains. In particular
b_i already includes the selected root in the size. It is not a free
weight or a polynomial from an invented attachment.

At s=k+1 the exact full minor is

 L_s(P)=L_s(a)+L_s(b)+2a_s b_s-a_(s-1)b_(s+1)-b_(s-1)a_(s+1),       (2.1)
 L_s(q)=q_s^2-q_(s-1)q_(s+1).

Equation (2.1) is an identity only. Neither local minor nor its mixed term
is assumed nonnegative. Replacing (a_s+b_s)^2 by a_s^2 loses positive
middle mass. This was precisely the overstrong entrance behind A4-Q;
Path32 at k9 refutes its universal availability, not the valid conditional
A4-Q lemma and not the different existential A4-R conjecture.

## 3. A5-FM-v1: a signed lower bound keeping both middle masses

Assume a_s>0 and b_s>0. Define

 c0=1-a_(s-1)a_(s+1)/a_s^2,
 c1=1-b_(s-1)b_(s+1)/b_s^2,
 x=a_(s-1)/a_s-b_(s-1)/b_s,
 y=a_(s+1)/a_s-b_(s+1)/b_s.

Suppose rational bounds have actually been proved:
 c0>=l0, c1>=l1, xL<=x<=xU, yL<=y<=yU.
The numbers l0,l1 may be negative. Put
 m=min(xL*yL,xL*yU,xU*yL,xU*yU), and
 B=p_s(a_s*l0+b_s*l1)+a_s*b_s*m.

**Conditional theorem:**

 L_s(P)>=B,                                                       (3.1)
 1-p_(s+1)/p_s >= 1-p_s/p_(s-1)+B/(p_(s-1)p_s),                  (3.2)

where (3.2) also requires p_(s-1)>0. In particular,

 B>=p_s(p_s-p_(s-1))                                             (3.3)

certifies p_(s+1)<=p_s. Under actual History this forbids the next rebound.
A negative B is permitted when the existing decline pays for it. No
conclusion that the whole sequence is LC is needed.

Proof. Expanding and collecting all terms gives

 L_s(P)=p_s(a_s*c0+b_s*c1)+a_s*b_s*x*y.                            (3.4)

For example, the coefficient of a_(s-1)a_(s+1) is
 -p_s/a_s+b_s/a_s=-1; the other diagonal and both mixed products follow
similarly. A bilinear function on a rectangle attains a minimum at a
corner (first minimize in one coordinate and then in the other). Hence
x*y>=m. Both a_s and b_s are positive, so substituting the lower bounds
proves (3.1). Finally
 p_(s+1)/p_s=p_s/p_(s-1)-L_s(P)/(p_(s-1)p_s)
proves (3.2), and clearing its positive denominator proves (3.3). QED.

This is a conditional algebraic theorem, also valid for other nonnegative
sequences with these premises. Its graph input is that every term and bound
belongs to the same ACTUAL root split. It is not a new general shape theorem.
If a middle state has zero mass, use (2.1) directly; ratios for that state
are not defined. The verification includes such cases separately.

### A non-circularity audit of the interval method

Certified rational intervals are useful for proving a strict numerical
margin, but increasing precision is not a structural proof. For a fixed
positive triple, the floor-grid bounds in the program converge to the true
c0,c1,x,y, so B converges to L_s(P). If the next step is strictly decreasing,
eventually sufficiently fine intervals certify (3.3). If the next step
increases, every valid B is below the required threshold. At exact equality,
coarse intervals may keep failing even when the true target is zero.
Thus unrestricted adaptive refinement would only re-detect the target sign.
The absent general step is a forest-specific bound supplied by HEREDITARY
and common adjacency, not existence of arbitrarily precise decimal grids.

## 4. Decisive complete-state controls

The certificate uses fixed grids D=10,100,1000,10000,1000000. Each c lower
bound is floor(D*c)/D; each x,y interval has width 1/D. Rational computation
is independently checked by clearing the common denominator D^2. The
program retains every tested root and complete coefficient array.

### 4.1 The former Path32 obstruction

At k9, s10, Path32 has
 (p9,p10,p11)=(1307504,1144066,705432).
Every one of its 32 roots has a10^2-p9*p11<0, so the old dropped-middle
entrance is unavailable everywhere. At endpoint r0 the actual state triples
are
 a=(817190,646646,352716), b=(490314,497420,352716).
Here c0=311/1001, c1=1159/3850, x=253/910, y=-9/55.
Using l0=l1=3/10, x in [2/10,3/10], y in [-2/10,-1/10], (3.1) gives
 B=1866834122538/5, and (3.2) gives
 rho_next >= 15853/42320 > 0.
All 32 full-mass tests pay; all 32 A4-R roots also have both raw budgets
nonnegative. These are different checks, recorded separately.

### 4.2 A genuine middle point with negative local curvature and cross term

Let K be the actual 26-vertex bush with arm counts [3,4,4]. Add a new root r
and neighbor w; join w to the central vertex of K, and attach nine private
leaves to r. There are 37 vertices, with alpha24, h10, beta15. Its whole
polynomial has coefficients

 (1,37,630,6599,47958,258449,1076892,3567212,9571482,21060414,
  38286901,57724289,72222901,74828014,63877940,44559077,25086002,
  11195704,3860499,991095,179450,21192,1486,61,1).

The first strict decline is k13 and 14<beta. At r, s14,
 a=(74825035,63877889,44559076), b=(2979,51,1).
The two local minors and the mixed contribution are respectively
 746250281828661, -378, -126300767761.
Their sum is 746123981060522. In particular neither the bad local minor
nor the negative mixed term has been dropped or treated as nonnegative.

One coarse, rigorously checked choice is
 l0=1/10, l1=-2/10, x in [-573/10,-572/10], y in [6/10,7/10].
It gives
 B=40790747528336071/100,
 rho_next >= 15819652075013153/68283705551588000 > 0.
The lower bound is about 0.231675, for orientation only. This pays the
actual next decline without assuming local LC. The full graph, arrays,
fractions and direct integer comparisons are stored. HEREDITARY is NOT
asserted for this 37-vertex tree; the signed conditional theorem needs no
such premise. No minimality or literature novelty is claimed for the graph.

### 4.3 Negative raw root-state budget and negative total-minor controls

The inherited 121-vertex tree has a center adjacent to 30 hubs, each with
three private leaves. At k43, h31, beta52, its central Qplus is
 -86*binom(90,43)<0. Both root states remain positive. The full-mass grid
with D10 gives a NEGATIVE B, yet (3.3) pays using the already present strict
decline. Thus the certificate need not prove a nonnegative minor lower
bound, and it does not demand both raw states be nonnegative at that root.

The separate B212 and B226 trees retain their tail-only C1 failures at
k100 and k108. At their last labeled leaf as root, both middle masses are
positive and BOTH local minors are negative. D10 full-mass certificates
still pay. These are deliberately tail controls: beta73 and beta79. They
are not middle counterexamples. The central roots have zero selected-state
middle mass at these positions and are handled by the undivided formula;
a draft verification that demanded positive-state certification there was
rejected and repaired, with its error log preserved.

The 14-vertex equality control has p4=p5=371 and p6=231. Its previous
history is absent, so it is NOT a descent-plateau example. The zero-current-
deficit algebra is checked without division by d. No equality after prior
strict decline was found in the targeted material.

## 5. Correct raw root budgets and A4-R's unchanged quantifiers

For a uniform independent k-set S use the ORIGINAL residual H=T-N_T[S]
and g_k(S)=(k+5)|H|-|H|^2-2c(H), including any available unselected root.
Let j_i=p_i(J). The division-free original-state sums are

 Qplus_r=k[(k+2)j_k-(k+1)j_(k+1)],
 Qminus_r=(k+1)(k+2)(a_(k+1)-a_(k+2))
           +(k+2)j_k-2(k+1)j_(k+1),                              (5.1)
 Qplus_r+Qminus_r=(k+1)(k+2)(p_(k+1)-p_(k+2)).                   (5.2)

Here is a direct check of the correction, not a new claim of fixed sign.
When r is selected, remove r and use (k-1)-sets in J; g_k=g_(k-1)+|H|.
The extension-pair count gives (5.1)'s first formula. When r is absent,
S ranges over k-sets of A. Unless S avoids all neighbors of r the residual
is the A residual. Otherwise S is a k-set of J and adding back the available
r changes T by 1 and c by 1-q, where q is its number of available neighbors.
The q neighbors lie in distinct residual branches because T is a tree.
The change in g is k+2-2(T_A-q)=k+2-2T_J. Summing gives the signed correction
 (k+2)j_k-2(k+1)j_(k+1).
This proves (5.1) including zero conditional mass. Counting residual pairs
also gives (5.2) directly. No root or tiny-probability state is deleted.

A4-R asks, for EACH connected HEREDITARY T and EACH qualified middle
History index k, for SOME root with BOTH quantities in (5.1) nonnegative.
It remains UNPROVED here. Seven specified trees were scanned at EVERY root
and EVERY one of their qualified middle-history indices: 35 graph/index
positions and 6093 root/index checks. No all-root failure occurred. Only
the two paths have a general HEREDITARY proof supplied here; the other
large graphs' HEREDITARY status remains unestablished. Thus the scans do
not silently promote LOCAL to HEREDITARY or establish universal A4-R.
A single negative root, as in Section 4.3, does not refute existence.

## 6. A genuine adjacent-edge compatibility relation for Window D

For an actual edge uv of a connected tree set
 C=P_(T-{u,v}), D=P_(T-(N[u] union N[v])),
 B_u=xP_(T-N[u]), B_v=xP_(T-N[v]), A_u=P_(T-u), A_v=P_(T-v).
The two endpoints cannot both be selected, so P=C+B_u+B_v,
A_u=C+B_v and A_v=C+B_u. Deleting uv separates two sides. If R,R0 count
the first side with its endpoint removed/closed neighborhood removed,
and S,S0 count the second analogously, then
 C=R*S, B_u=x*R0*S, B_v=x*R*S0, D=R0*S0.
Therefore the ACTUAL graph polynomials obey

 B_u*B_v=x^2*C*D.                                               (6.1)

This is a constraint linking adjacent roots and their common neighbors,
not just two arbitrary splits with the same total. Arbitrary branches on
both sides remain in all four factors. For every s>=1, expansion gives

 L_s(P)=E_uv(s)+H_uv(s),                                        (6.2)
 E_uv(s)=L_s(A_u)+L_s(A_v)-L_s(C)+3(B_u)_s(B_v)_s
            -[x^(2s-2)](C*D),
 H_uv(s)=sum_(0<=t<=2s, |t-s|>=2) (B_u)_t(B_v)_(2s-t) >=0.

Indeed the missing mixed term is
2(B_u)_s(B_v)_s-(B_u)_(s-1)(B_v)_(s+1)-(B_u)_(s+1)(B_v)_(s-1).
Extracting coefficient 2s in (6.1) and retaining its off-center summands
turns this into 3(B_u)_s(B_v)_s-[x^(2s-2)]CD+H_uv. This proves (6.2).
Consequently E_uv>=p_s(p_s-p_(s-1)) is a sufficient no-rebound certificate.
The exact H term is supplied to D; its positive mass is not called zero.

The simpler entrance that discards H is NOT universal: Path128, k36,
h32, beta43, satisfies History and HEREDITARY, but NONE of its 127 edges
pays the threshold using E alone. The maximum of E-threshold over those
edges is the strictly negative integer
 -346848450555243163088595620635431883352087433049980.
Its full sequence is unimodal and all 128 roots pass A4-R at k36.
Thus (6.2) must keep H or gain a separate structural bound; declaring that
some paying edge exists would be another unproved and here false shortcut.
It is not used to finish the general proof. Full arrays and all edges were
checked, not a chosen failing edge. These data do not refute A4-R.

## 7. The path HEREDITARY premise used in the controls

For an n-vertex path the gap-removal bijection for independent positions
 i_1<...<i_j with i_(t+1)>=i_t+2 gives p_j=binom(n-j+1,j).
Its ratio p_(j+1)/p_j is
 [(n-2j)/(j+1)] * [(n-2j+1)/(n-j+1)].
Each nonnegative factor decreases with j on the relevant positive support,
so the path sequence is LC. Any induced subforest of a path is a disjoint
union of paths (singletons included).

For completeness the elementary LC-times-unimodal fact is sufficient here.
If a is LC with interval support, and k<l,j<t, then
 a_(l-j)a_(k-t)<=a_(k-j)a_(l-t): move the two extreme indices inward,
using decreasing adjacent ratios; zero boundaries cause no exception.
For a unimodal b, choose a split of its differences d_j=b_j-b_(j-1) into
nonnegative early and nonpositive late terms. Writing the differences of
a*b as P_k-N_k and summing the preceding inequality with weights d_j(-d_t)
gives P_l N_k<=P_k N_l. Once P_k<N_k, this prevents P_l>N_l later, including
N_l=0. Thus a*b is unimodal. Repeatedly convolving path factors proves
unimodality of every induced path forest. This certifies HEREDITARY for
P32 and P128 without enumerating all 2^32 or 2^128 induced sets.

## 8. Direct first-descent/first-rebound attempt and its first gap

Suppose a HEREDITARY tree first descends at i and first rises afterwards
at j>i. For every root the two proper-forest sequences a and b are unimodal.
At i some summand E has a strictly negative difference. It cannot increase
at j. Hence the other summand L increases strictly at j and cannot have
had a negative difference at i. Put
 e_i=-Delta E_i>0, e_j=-Delta E_j>=0,
 l_i=Delta L_i>=0, l_j=Delta L_j>0.
The whole signs force l_i<e_i and l_j>e_j, and therefore
 l_i e_j-l_j e_i<0.                                             (8.1)
Platforms between i and j have not been removed. Zero l_i/e_j values are
handled without forming ratios. This is the inherited RSM obstruction,
not a new proof or a new universal two-end monotonicity assertion.

The exact full-mass and edge relations do not yet contradict (8.1).
HEREDITARY gives unimodality, not quantitative local curvature or bounds
on the relative opposite-sign changes. C4's palette theorem concerns
ordinary complete-component unions, not arbitrary new rooted exteriors.
C5's published buffered-band interface was read, but its conditions do not
automatically apply to these root-deleted forests, and no such application
is an assumption here. D's ADMC existence is also still unproved.

**First unproved structural step:** use the common actual tree adjacency,
including both state masses and positive H_uv, to force the signed total
at a prospective first rebound above the threshold, or prove A4-R's
existential two-budget condition under HEREDITARY. No such general payment
or existence theorem has been established in this run.

Accordingly the new universally proved statements are conditional (3.1)
and the exact tree relation (6.2), with scoped decisive sign certificates.
They DO NOT narrow the remaining unrestricted original-problem domain.
ORIGINAL, A4-T, and A4-R retain their separate NOT_CLOSED/UNPROVED statuses.
