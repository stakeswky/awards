# C7 entrance tests v1: scopes and exact failure tests

Run: 20260921T033701Z_round7_payment_entrance_audit.
ORIGINAL=NOT_CLOSED; general C4-F=NOT_CLOSED. This is a test interface,
NOT an assertion that any automatic entrance below has been proved.
The space C6-P4 run 012837Z and remote C6-SC run 012701Z are kept distinct.

## Definitions shared by the two claims

F is a finite simple undirected unweighted disconnected forest. X,Y are
nonempty complementary unions of WHOLE components, A=I(X), B=I(Y),
a=alpha(X), b=alpha(Y), all coefficients zero padded. Assume both A,B
whole-unimodal. Let u,m be their LAST modal indices. For an integer k with
h<=k and k+1<beta and actual History(F,k), put z=k+1 and q=z-m-1.
Here h=floor(M_max(n-1)/(4M_max-2))+1 and beta=ceil(alpha(F)(n-1)/(n+alpha(F))).
History means a strict decline at some i<=k and all subsequent differences
through k nonpositive. Do not replace it by a small current d. The formulas
below are for m+1<=z<=m+a; outside this band the inherited elementary
zero-support argument already excludes a subsequent rise.

D_j=B_j-B_(j-1), including j=0,b+1;
P_z=sum_(j<=m) D_j A_(z-j), N_z=sum_(j>m) (-D_j)A_(z-j),
and P_(z+1),N_(z+1) analogously. Both N denominators are positive.
For l=0,...,a-1 set
r_l=A_(l+1)/A_l, r_a=0, c_l=r_l-r_(l+1),
U_l=sum_(j<=m,z-j>l)D_j A_(z-j),
V_l=sum_(j>m,0<=z-j<=l)(-D_j)A_(z-j), W_l=U_l V_l.
Let H_l=max_(0<=i<=l)A_i and T_l=max_(l<i<=a)A_i. Use the inherited envelope
Wbar_l=P_z min(N_z,H_l B_(z-l-1)) if l<q,
Wbar_l=N_z min(P_z,T_l B_(z-l-1)) if l>=q.
All endpoints and adverse terms remain.

Put C0=P_z A_0 max(0,-D_(z+1)),
Dpay=N_(z+1)(p_(z-1)-p_z)+C0,
Jmod=c_(u-1)W_(u-1), Jmax=max({0} union {c_l W_l:c_l>0}),
Splus=sum_(c_l>0)c_l W_l,
Sminus=sum_(c_l<0)(-c_l)W_l,
Ebar=sum_(c_l<0)(-c_l)Wbar_l.

## C7-ENT-v1: automatic-entrance candidates, UNPROVED

For t in {modal,max,all-envelope,all-exact}, respectively define
Pay_t=Dpay+Jmod-Ebar, Dpay+Jmax-Ebar,
Dpay+Splus-Ebar, Dpay+Splus-Sminus.
The primary EVERY-split candidate says: for EVERY F satisfying HEREDITARY
(each proper induced subforest is whole-unimodal), with NO nonempty proper
LC whole-component subunion, EVERY admissible ordered split and k above has
Pay_t>=0. Test each t independently; no one version is silently substituted.
The EXISTS-split candidate instead says for EVERY such F and k there EXISTS
an ordered whole-component split passing the indicated gate or its already
safe outside-mode-band case. One failed split does not refute EXISTS.

Also test the strictly stronger no-H/no-LC-exclusion versions using only
actual F, the two whole-unimodal factors and the history/range premises.
Label these precisely. An ordinary graph with HEREDITARY=UNKNOWN cannot
refute the HEREDITARY version; a graph with an LC component subunion cannot
refute the no-LC-subunion version. An ACTUAL-minimum-bad version has a
further premise and is never refuted merely by a good graph.

A failure certificate needs complete actual graphs, integer coefficient
sequences, ordered component vertex sets, k,h,beta, history, all four Pay
values and full-sequence valley scans. A negative auxiliary Pay is NOT an
original counterexample. Pay_all-exact<0 with the stated history WOULD be
an original counterexample and must receive a second independent graph count.

## C7-LOSS-v1: exact audit identity (inherited algebra, NOT new closure)

Pay_all-exact=N_z*(p_z-p_(z+1)), and
Pay_all-exact-Pay_max=(Splus-Jmax)+(Ebar-Sminus).
Both terms on the latter right side are nonnegative. This separates the
omitted positive supply from artificial envelope excess. It does not prove
that either loss is affordable and is not a replacement for C7-ENT.

B can refute this algebra only by an exact arithmetic mismatch on the stated
objects. For an entrance failure, continue to the full exact signed sum and
record which of the two losses caused failure. Do not clip negative sigma
in the separate R-V computation. Do not apply whole-component interfaces
to original-graph root-absent availability or E's symmetric-difference blocks.

Sources: complete remote C6 PROOF/CLAIMS_FINAL at initial HEAD d9707fe,
PROOF blob 5d92c676381b8a261053b06f52b37c6e08372a22; complete mounted
space C6-P4 proof and its final addendum. No unproved A or D result is used.
No peer receipt, fresh remote-author replay or general proof is asserted here.
