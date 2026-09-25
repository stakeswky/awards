# A7: history-driven compensating roots with an arbitrary exterior

Run: `20260921T034427Z_round7_history_root`.

**ORIGINAL = NOT_CLOSED. General A4-T and A4-R remain UNPROVED.**
The new theorem supplies a compensating leaf from an actual structural gate,
not from a finer numerical interval. Its exterior is arbitrary, but its long
bare pendant path is a real restriction. A hypothetical minimum bad tree is
not proved to have such a path. No general theorem about all trees is claimed.

## 1. Definitions, history, and the two A6 sources

All graphs are finite, simple, undirected and unweighted. Write I(F;x)=sum p_i x^i
for the polynomial counting independent vertex sets by size. If alpha is the
maximum independent-set size, p_i>0 exactly on 0,...,alpha: use subsets of a
maximum set. Coefficients are zero outside that interval. Unimodality allows
plateaus; its failure is precisely a strict fall followed later by a strict rise.

Put Delta_k=p_(k+1)-p_k. History(F,k) means some i<=k has Delta_i<0 and all
Delta_i,...,Delta_k are nonpositive. HEREDITARY means every proper induced
subforest is unimodal, including disconnected ones. LOCAL checks only F-r and
F-N[r] for every r and does not imply HEREDITARY. A hypothetical least-order
ORIGINAL counterexample makes all smaller forests good, but need not be connected.

For positive denominators, mu_k=(k+1)p_(k+1)/p_k, d_k=k+1-mu_k,
e_k=mu_(k+1)-mu_k-1. Define, without any sign assumption,

 tau_k=(k+1)(k+2)(p_(k+1)-p_(k+2)).

Then tau_k/p_k=mu_k(d_k-e_k). The desired sign is e_k<=d_k, not globally e_k<=0.
At a current plateau do not divide by d_k. For a connected n-vertex tree the
inherited reporting boundaries are

 h=floor(n(n-1)/(4n-2))+1,   beta=ceil(alpha(n-1)/(n+alpha)).

No external endpoint theorem is needed for the new full-sequence proof below;
these formulas only specify the A4-R middle domain in Section 8.

Two A6 objects are kept separate. The mounted final package is
`20260921T014921Z_round6_leaf_history_guard`, with the A6-LEAF identity and its
all-path consequence. It has complete local proofs and certificates. The remote
`20260921T012734Z_round6_root_edge` directory at the initial actual HEAD contains
ONLY an early CLAIMS_FOR_PEERS.md. Its A6-PATH-v1 asserts a long-connector result
with a 64(d+2)^2 gate, but no final constant proof or certificate was obtained.
That result is INTERFACE_ONLY in this audit. Sections 3--9 below are a new written
derivation inspired by its path-mixture mechanism, NOT recovery of missing A6
bytes or certification of its original constants. The graph regions overlap;
indeed this whole-unimodality region is contained in its CLAIMED region: use
N-1 internal vertices and exterior E plus the isolated final endpoint, whose
independence number is d+1. The new gate implies N-1>=64(d+3)^2. We do not
count the two interfaces as two independent exclusions. The new
shortening and compensating-root/history conclusions are not in that interface.

## 2. Original-graph root budgets and the inherited leaf identity

For a root r set a=I(T-r), j=I(T-N[r]); actual independent sets give P=a+xj.
If S is an independent k-set, let H=T-N[S], t=|H|, c=c(H), and
 g_k(S)=(k+5)t-t^2-2c.
Because H is a forest, twice its independent-pair count is t^2-3t+2c.
Double counting one- and two-point extensions gives sum_S g_k(S)=tau_k.
Separating whether r belongs to S gives

 q_r=Qplus_r=k[(k+2)j_k-(k+1)j_(k+1)],
 Qminus_r=(k+1)(k+2)(a_(k+1)-a_(k+2))
                   +(k+2)j_k-2(k+1)j_(k+1),
 Qminus_r=tau_k-q_r.                                      (2.1)

The correction is SIGNED. When r is absent but available, adding it back to
the residual changes its order by 1 and its component count by 1-q, where q
is its number of available neighbors. They are in different residual branches,
by acyclicity. The score change is k+2-2t_J; summing it yields the last two
terms in Qminus. Thus (2.1) does not delete an available absent root. All
formulas are unnormalized, so empty conditional classes cause no division.
Counting each S at its k selected vertices gives sum_r q_r=k tau_k for ALL
signs of tau. This identity is not a sign or existence proof.

For an actual leaf l with support w put C=I(T-{l,w}), H=I(T-N[w]). Then
 P=(1+x)C+xH.
For c0=c_k,c1=c_(k+1),c2=c_(k+2), let
 F_k=(k+1)c1^2-(k+2)c0*c2.
The exact A6 leaf factorization is

 c0 Qminus_l = c0^2
   +(k+1)(c0-c1)(c0+(k+1)c1)
   +(k+1)F_k +(k+1)(k+2)c0(h_k-h_(k+1)).                (2.2)

It follows by substituting the leaf decomposition into (2.1) and expanding.
It retains every H term. If c0>0, c1<=c0, F_k>=0 and h_(k+1)<=h_k, then

 q_l>=k c0,                 Qminus_l>=c0.              (2.3)

These are sufficient conditions, not assumed for an arbitrary tree. The new
step below proves them from a long pendant path and the ACTUAL current fall.

## 3. A7-PENDANT-ROOT: statement and complete graph counting

Let E be ANY nonempty connected tree with a specified vertex v. Put d=alpha(E).
Attach N distinct new vertices as the bare pendant path v,x1,...,xN. No other
edge meets these new vertices. Let F_m=E with the first m vertices of this path,
and T=F_N. Assume

                     N >= 128(d+2)^2.                  (3.1)

THEOREM. I(T) is unimodal. At every k with h<=k, k+1<beta and p_(k+1)<=p_k,
the ACTUAL tip l=xN satisfies q_l>0 and Qminus_l>=p_k(F_(N-2))>0. Consequently
it witnesses A4-R at every genuine middle-History position in this class,
without requiring HEREDITARY of E or any of its conditional sequences.
The whole-history contraction is specified in Section 9.

Write
 A=I(E-v),  B=xI(E-N[v]),  f_n(t)=binom(n-t+1,t).
The path formula follows by sending independent positions i_1<...<i_t to
 i_1, i_2-1,...,i_t-(t-1), ordinary t-subsets of {1,...,n-t+1}.
It includes the empty path. Define f_n(t)=0 outside 0,...,ceil(n/2).
Partitioning by whether v is selected gives the EXACT two-state mixture

                  p^(m)=A f_m + B f_(m-1).             (3.2)

The exponent already included in B counts v. All branches and every edge of E
remain in A,B. No exterior term is removed or required LC/unimodal. Every
nonzero A_j or B_j has 0<=j<=d. A coefficient can thus be regarded as a sum
of nonnegative sectors c_(delta,j) f_(m-delta)(s-j), delta in {0,1}.
Zero exterior sectors simply have zero weight; no nonzero sector is truncated.

Set
             K=floor(N/4),       L=ceil(N/3)+d.
Since d>=1, (3.1) gives N>=1152. For all m=N-3,...,N, K<=s<=L and 0<=j<=d,
put n=m-delta and t=s-j. Then

 .99N <= n <= N,       .24N <= t <= .35N,
 .29N <= a:=n-2t <= .52N,       n-t+1 >= .64N.         (3.3)

Indeed n>=N-4>=.99N. Also K-d>=N/4-1-d>=.24N, since
N>=100(d+1); and L<=N/3+1+d<=.35N, since N>=60(d+1).
Both auxiliary size inequalities follow from (3.1). Thus f_n(t-1),f_n(t),
f_n(t+1) are positive throughout the required band. In particular ratios
below have positive denominators and neither endpoint state disappears there.

## 4. Uniform kernel estimates with explicit constants

Treat n,t as real variables on (3.3); every denominator stays positive.
The following rational expressions agree with path coefficient ratios at
integer n,t:

 U=f_n(t-1)/f_n(t)=t(n-t+2)/[(a+3)(a+2)],
 V=f_n(t+1)/f_n(t)=a(a+1)/[(t+1)(n-t+1)],
 H=f_(n-1)(t)/f_n(t)=(a+1)/(n-t+1).                   (4.1)

We prove, throughout (3.3) for N>=1024,

 1-UV>=8/N, V>=3/10,
 |U_t|<60/N, |U_n|<23/N,
 |V_t|<25/N, |V_n|<6/N,
 |H_t|<5/(2N), |H_n|<1/N,
 H(n,t)-H(n,t+1)>=1/N.                              (4.2)

These are analytic estimates, not a grid certificate.

### 4.1 Intrinsic curvature

Let z=(a+1)/[(t+1)(n-t+1)] and b=(4a+6)/[(a+2)(a+3)]. Direct multiplication gives
 UV=(1-z)(1-b).
Here 0<z<1. Since t+1<=.36N, n-t+1<=.77N, a>=.29N,
 z >= .29/(.36*.77*N) >=1/N.
The function b decreases for a>0: its derivative numerator is -4a^2-12a-6.
At a=.52N, b>=15/(2N) reduces, after multiplication by positive denominators,
to (13/125)N^2-27N-90>=0. This holds at N=1024 and increases afterward.
Also b<=1/2 because a>=.29N>5 implies a^2-3a-6>0. Thus

             1-UV=b+z(1-b)>=15/(2N)+1/(2N)=8/N.

### 4.2 Derivatives of U

From (3.3), U <= (.35*.77)/(.29^2)=2695/841<13/4. Logarithmic differentiation gives
 U_t=U[1/t-1/(n-t+2)+2/(a+3)+2/(a+2)]>0,
 U_n=U[1/(n-t+2)-1/(a+3)-1/(a+2)]<0.
The signs use n-t+2>t and n-t+2>=a+2. Therefore
 |U_t| <=(13/4)(25/6+400/29)/N=40625/(696N)<60/N,
 |U_n| <=(13/4)(200/29)/N=650/(29N)<23/N.

### 4.3 Derivatives of V and H

First V>=(.29^2)/(.36*.77)=841/2772>3/10. Direct differentiation gives

 V_t=-(n^3-2n^2t+5n^2-10nt+6n+2t^2-8t+2)
                         /[(t+1)^2(n-t+1)^2],
 V_n=(n^2-2nt+2n-3t+1)/[(t+1)(n-t+1)^2].              (4.3)

The first numerator, without its leading minus, is
(n^2+5n)a+6n+2t^2-8t+2>0 in this rectangle. The second is positive since
a>0 and 2n>3t. The corresponding upper bounds are

 |V_t| <= [.52+(5+2*.35^2)/N+6/N^2+2/N^3]/(.24^2*.64^2*N)<25/N,
 |V_n| <= [.52+2/N+1/N^2]/(.24*.64^2*N)<6/N.

Both bracketed expressions decrease with N, so it is enough to insert N=1024;
the first constant is 110127280390625/4947802324992<25 and the second is
8551695625/1610612736<6. All constants are checked as rational integers.
Finally
 H_t=-(n+1)/(n-t+1)^2, H_n=t/(n-t+1)^2.
Their bounds follow from (1+1/1024)/.64^2=640625/262144<5/2 and
.35/.64^2=875/1024<1. The exact forward difference is

 H(n,t)-H(n,t+1)=(n+1)/[(n-t+1)(n-t)]>=1/n>=1/N.

Here t+1 remains inside positive path support, even when outside the displayed
real rectangle at its upper edge. This completes (4.2).

## 5. Complete two-state mixing: actual curvature pays signed covariance

Fix m,s in the band of Section 3. Use the ACTUAL weights

 w_(delta,j)=c_(delta,j) f_(m-delta)(s-j)/p_s^(m).

They sum to one and include both boundary states. Write expectation with
respect to them as E_w. The exact normalized full minor is

 L_s(p^(m))/(p_s^(m))^2
       =1-(E_w U)(E_w V)
       =E_w(1-UV)+Cov_w(U,V).                         (5.1)

Thus the between-state and between-size mixing have NOT been set to zero.
Within these sectors, n changes by at most one and t by at most d. The mean
value theorem, along line segments contained in the rectangle, gives

 range U<=60(d+1)/N, range V<=25(d+1)/N,
 range H<=3(d+1)/N.                                   (5.2)

For a random variable in [l,u], E[(X-l)(u-X)]>=0 implies
Var(X)<=(E X-l)(u-E X)<=(u-l)^2/4. Cauchy--Schwarz then gives
|Cov(X,Y)|<=range(X)range(Y)/4. Applying this to (5.1), not discarding the
adverse sign, proves

 L_s/(p_s^(m))^2 >=8/N-375(d+1)^2/N^2
                >=(8-375/128)/N=649/(128N)>5/N.       (5.3)

The last inequality is actually paid by (3.1), not an unproved affordability
assumption. No local LC condition of A or B is present.

## 6. Shortening the ACTUAL path decreases the ratio

This step connects current history to the deleted leaf forest. It is not a
universal claim that arbitrary vertex deletion moves a mode or lowers ratios.
Fix m=N-2,...,N and central k. At its sectors use (4.1) with t=k-j and
write H^+=H(n,t+1). The same exterior coefficients in the TWO adjacent path
lengths give the exact relations

 p_k^(m-1)/p_k^(m)=E_w H,
 p_(k+1)^(m-1)/p_k^(m)=E_w(V H^+).

Let R_m(k)=p_(k+1)^(m)/p_k^(m). Then

 R_m(k)-R_(m-1)(k)
  = [E_w(V(H-H^+))-Cov_w(V,H)]/(E_w H).                (6.1)

This compares two actual induced forests, not two arbitrary unimodal arrays.
The first term is >=3/(10N). The signed covariance is at most
75(d+1)^2/(4N^2). Since 0<E_w H<=1, (3.1) yields

 R_m(k)-R_(m-1)(k)
 >= [3/10-75/512]/N=393/(2560N)>3/(20N).              (6.2)

In taking the last denominator at most one we first established a positive
numerator. No sign was assumed. Formula (6.1) retains positive middle mass and
all signed state variation. Numerical interval refinement is not used.

## 7. Whole-sequence signs and the joins

For T itself, n in the path kernels is N or N-1. At k<K each active sector
has 0<=t=k-j<=N/4. Its path ratio V is >=1. One explicit lower check is

 (N/2-1)(N/2) - (N/4+1)(3N/4+1)
                         =N^2/16-3N/2-1>0.

The numerator a(a+1) is at least the first product, and
(t+1)(n-t+1) is at most the second: increase n to N and t to N/4 in that
product, which increases for t<=N/2. Terms still below their birth have zero
coefficient or add a nonnegative new term. None reaches its death here.
Therefore p_0<=...<=p_K; in fact the empty-exterior sector makes these strict.

For k>=L, every active sector has t=k-j>=ceil(N/3). When both adjacent path coefficients are positive,
V is increasing in n and decreasing in t. The latter also follows from the
product of the two decreasing nonnegative factors
 (n-2t)/(t+1) and (n-2t+1)/(n-t+1).
A terminal positive coefficient has next ratio zero and is handled separately.
Thus V<=V(N,N/3)=N/(2N+3)<1 in every active sector. No sector can be newly born, because k>=L>d.
A dead sector contributes zero thereafter. Thus p_L>=p_(L+1)>=... .

The strict LC band (5.3) orders all successive ratios from R_N(K-1) through
R_N(L). Together with these initial and final signs it precludes any strict
fall followed by a rise, including the joins and all plateaus. This proves
whole unimodality independently of any external tail theorem.

## 8. Supply the root entrance from the ACTUAL current decline

Let q=|E|. Bipartition by parity of distance in a tree gives q<=2d. Therefore
n(T)=N+q<=N+2d and alpha(T)<=ceil(N/2)+d<=(N+2d+1)/2.
The function a(n-1)/(n+a) increases in n and a when n>1,a>0. Put M=N+2d;
then

 alpha(T)(n(T)-1)/(n(T)+alpha(T))
 <=(M^2-1)/(3M+1)<(M+1)/3.

Consequently beta<=ceil((N+2d+1)/3). Also
h>(n(T)-1)/4>=N/4. For h<=k and k+1<beta, it follows that
k and k+1 lie in [K,L]: in particular k+1<(N+2d+1)/3<=L.
This is just a location calculation, not an application of an unproved
history transfer or an assumption about where a deleted graph's mode lies.

Now use the actual hypothesis p_(k+1)(T)<=p_k(T), i.e. R_N(k)<=1.
By applying (6.2) twice,

 R_(N-2)(k)<=1-3/(10N)<1,
 R_(N-3)(k)<R_(N-2)(k)<1.                            (8.1)

THIS is where current history supplies a new inequality on the proper forests.
It is proved using the shared whole exterior, not inferred from their individual
unimodality. Let l=xN, w=x_(N-1). Then
 C=I(F_(N-2)), H=I(F_(N-3)).
Thus c1<c0 and h_(k+1)<h_k. At s=k+1, (5.3) gives

 (c1^2-c0*c2)/c1^2>=5/N>1/(k+2),

since k>N/4. Hence F_k=(k+1)c1^2-(k+2)c0*c2>0. Every premise of (2.3) has
now been SUPPLIED by the structure and the current nonincrease. We conclude

 q_l>=k c0>0,    Qminus_l>=c0>0,    tau_k>0.           (8.2)

No positive tau was used to obtain (8.1) or any preceding lemma. The signed
root correction in (2.1) can still be negative; (2.2) pays it together with
all H contributions. This proves the root part of A7-PENDANT-ROOT-v1.

## 9. Use the entire actual history, not just a label

Let i be a strict descent index in the central band, so R_N(i)<1. For
s=i+1,...,k+1<=L, (5.3) gives

 R_N(s)<= (1-5/N) R_N(s-1).

Multiplying these actual inequalities proves the versioned bound

 R_N(k+1)<= (1-5/N)^(k+1-i) R_N(i)<1.                 (9.1)

The exponent records the number of steps after the FIRST actual strict
descent. It does not assume intermediate local histories for A or B.
If the first fall is followed by a proposed first rise inside this band,
(9.1) is the contradiction; from L onward Section 7 already forbids a rise.
A current plateau after that first fall cannot arise inside this strict band.
For a standalone current plateau (8.1)--(8.2) still use R_N(k)=1 directly,
without division by zero slack. This proves the promised history connection
for the scoped graph class, not a general all-tree contraction assertion.

## 10. Full adjacent-edge compatibility is retained

For an ACTUAL adjacent pair u,v, put
 C_e=I(T-u-v), D_e=I(T-(N[u] union N[v])),
 B_u=xI(T-N[u]), B_v=xI(T-N[v]), A_u=I(T-u), A_v=I(T-v).
Deleting that edge separates two sides, and their root-absent/forbidden
products show B_u B_v=x^2 C_e D_e. Also P=C_e+B_u+B_v. Exact expansion gives

 L_s(P)=L_s(A_u)+L_s(A_v)-L_s(C_e)+3(B_u)_s(B_v)_s
        -[x^(2s-2)](C_e D_e)+H_uv(s),
 H_uv(s)=sum_(|t-s|>=2)(B_u)_t(B_v)_(2s-t)>=0.        (10.1)

For the pendant tip edge used above, C_e=I(F_(N-2)), D_e=I(F_(N-3)); hence
this identity uses the very same actual residuals. The verifier computes the
ENTIRE H_uv sum on the decisive history positions. It is not dropped or used
as if it supplied an independently free reserve. Section 8's payment is a
separate proved structural argument, not a claim that a sum of identical
L_s identities over all edges would prove its own sign. The ends of a long
path are not themselves an adjacent pair.

## 11. General history-driven attempts and the first unproved arrow

The arbitrary-tree problem remains. Its all-root identity sum q=k tau holds
also when a prospective rebound makes tau<0. Studying only tau>0 would omit
the desired contradiction. Connectedness supplies no discrete intermediate-
value principle: the A6 history-free P66 control already jumps over the whole
root interval. This run does not assert that the same jump is impossible
under History without a proof. No new history-free guard is counted as progress.

For a real first fall i and first later rise j in a HEREDITARY tree, each root
split has an early declining summand E and a late growing summand L. Write
 e_i=-Delta E_i>0,e_j=-Delta E_j>=0,l_i=Delta L_i>=0,l_j=Delta L_j>0.
Whole signs force l_i<e_i and l_j>e_j, so
 l_i e_j-l_j e_i<0.
This is the OLD RSM determinant, including zeros/plateaus, not a new theorem.
Trying to propagate it along an edge using (10.1) has not produced a bound
which makes all such signs incompatible in a general tree. HEREDITARY gives
individual shape, not the magnitudes or length monotonicity (6.2).

The new result excludes actual trees satisfying (3.1), with ANY exterior.
Equivalently a minimum bad connected tree cannot contain a bare pendant path
whose length N is at least 128(alpha(exterior)+2)^2. We have not proved that
all other trees have a paying leaf, another paying root, or a smaller ordinary
bad induced forest. In particular arbitrary short dense branchings need not
satisfy (3.1); no same-order transformation, weighted replacement, or unproved
C/D closure is used to place them there.

This is the first missing arrow: true middle History plus actual arbitrary
adjacency and HEREDITARY must force tau>=0 (or some q in [0,tau]) OUTSIDE the
proved structural gates. General A4-R, A4-T and ORIGINAL stay unproved.

## 12. Verification and provenance boundary

Two non-path material exteriors (P3 rooted at its center, and K1,3 rooted at
its center) are extended by N=2048 and N=3200 new vertices. The completed trees
have 2051 and 3204 vertices, with first falls 567 and 886. For each, all four
F_m arrays, m=N-3,...,N, were computed by three methods: actual iterative
root-state graph DP with carry-free integer encoding; independent vertex
removal with actual-component factorization and a path base; and (3.2) with
small exterior counts. The actual support-deleted mask was also recounted by
both graph algorithms and the exact isolated-tip factor, giving10 complete
array tasks and13151 coefficient comparisons in total. The second and third methods share the binomial path
base, so they are not three independent software stacks. The first DP does
not use the path formula. Every coefficient was compared.

All 1780 claimed central minors, 1335 length comparisons, and 298 qualified
middle-history tip instances were checked by integers. Full history was used
in the power inequality (9.1). Only the proved tip is asserted checked for
root existence, not every root in these long trees. Full graph edges, both
exterior states, four arrays, decisive root budgets, complete covariance and
four entire adjacent-edge H sums are kept in the key certificate.

Literal independent-subset checks on 31 deterministic small graph records
verify 973 root/index formulas and 236 zero selected-mass cases. They retain
7752 occurrences of an available unselected root. These are correctness
controls, not new general-domain coverage or a root-failure census.
The 60 rational rectangle controls check implementation; the all-real proof
is Section 4, not those samples. No arbitrary coefficient grid was refined.

The mounted A6 proof/Gap/Review/Claims/key and receipts were read; its unchanged
root_core.py is reused with attribution. A6's previous entire search was NOT
replayed and its counts are not added. The original final A6 long-connector
proof was not obtained. D6's fixed-edge failure and replacement and the two C6
batches' full scopes were read separately, not used as unproved dependencies.
Same-model review and multiple counting algorithms are not external peer review.
Lean and axiom audit: NOT_RUN. No literature priority or prize claim is made.
