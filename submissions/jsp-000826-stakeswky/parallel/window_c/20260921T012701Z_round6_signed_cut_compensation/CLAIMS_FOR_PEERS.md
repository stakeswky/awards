# C6 interfaces v1: signed cut payment and LC-free component obstruction

Run: 20260921T012701Z_round6_signed_cut_compensation.
ORIGINAL=NOT_CLOSED; general C4-F=NOT_CLOSED. C4 four-type closure is retained.
These two claims use no unproved A result. Only whole ordinary forests and
complete component unions are allowed, not conditional root availability or
components inside a symmetric difference. Full proof and replay follow in
this same directory; no final execution totals are asserted in this interface.

## C6-SC-v1: an explicit sufficient payment inequality (PROVED, conditional)

Let F=X disjoint-union Y be finite simple unweighted forests, both nonempty.
A_i=p_i(X)>0 for 0<=i<=a and B_j=p_j(Y)>0 for 0<=j<=b, zero elsewhere.
Assume B is WHOLE unimodal, and let m be its LAST modal index. Define
D_j=B_j-B_(j-1), INCLUDING D_0 and D_(b+1). For any integer
m+1<=z<=m+a set p=A*B, k=z-1, q=z-m-1, and

 P_z=sum_(j<=m) D_j A_(z-j),
 N_z=sum_(t>m) (-D_t) A_(z-t).

Terms outside 0..b+1 vanish. Define P_(z+1),N_(z+1) likewise. Both N_z and
N_(z+1) are positive by the last-mode convention, even at a plateau of p.
Set r_i=A_(i+1)/A_i for 0<=i<=a (r_a=0), c_l=r_l-r_(l+1), and

 U_l=sum_(j<=m,z-j>l) D_j A_(z-j),
 V_l=sum_(t>m,0<=z-t<=l) (-D_t) A_(z-t),  W_l=U_l V_l,
 H_l=max_(0<=i<=l) A_i,   T_l=max_(l<i<=a) A_i.

For 0<=l<a define the nonnegative, proved mass envelope

 Wbar_l=P_z min(N_z,H_l B_(z-l-1))              if l<q,
 Wbar_l=N_z min(P_z,T_l B_(z-l-1))              if l>=q.

Set C0=P_z A_0 max(0,-D_(z+1)),
J=max({0} union {c_l W_l:c_l>0}),
E=sum_(c_l<0) (-c_l) Wbar_l, and

 L=C0+J-E,
 Payment=N_(z+1)(p_(z-1)-p_z)+L.

Then the following are unconditional identities/inequalities in this domain:

 P_z N_(z+1)-P_(z+1) N_z = C0+sum_l c_l W_l >= L,
 p_z-p_(z+1) >= Payment/N_z.

Thus Payment>=0 is a sufficient NUMERICAL STRUCTURAL GATE for no next rise.
Every inverse curvature term is retained in E, paid by one actual positive
cut, the boundary contribution, and the actual current decline. No full LC
window, arbitrary weights, clipping, or variance-upper-bound comparison is used.
For actual History(F,k), h<=k, k+1<beta, the true component budget has

 R-V=G_F(k) >= (k+1)(k+2) Payment/[p_k(F) N_z].

This does NOT assert Payment>=0 for every forest or every minimum bad forest.
HEREDITARY is not needed for the inequality. In a minimum bad forest it supplies
B-unimodality for a proper complementary Y, but an automatic payment gate is
still UNPROVED. A negative Payment only fails this sufficient gate, not ORIGINAL.
Exact refutation of the proved claim: give real X,Y, all coefficients, z,m,
all displayed quantities and a violation of the lower bound. All ratios use
positive support; no division by current d_k occurs. k outside the mode band
must be handled separately rather than forced into this formula.

## C6-LCFREE-v1: no absolute component-count LC entrance (PROVED)

For every r>=1 and integer s>=6 with 2^s>24r, let T_s have a central root,
three adjacent hubs, and s private two-edge paths at each hub. No other
vertices or edges occur. Let F be r disjoint copies of T_s. Every nonempty
complete component subunion of F has a NON-LC polynomial.

Indeed put u=2^s+s, v=s 2^(s-1)+binom(s,2). The degree of I(T_s) is d=3s+3
and its last three coefficients are (3u^2+3v+2^(3s),3u,1).
For t copies, 1<=t<=r, the penultimate LC minor is exactly

 t[((9t+3)/2)u^2-3v-2^(3s)] < 0.

The sign follows from u<=2^(s+1) and 18t+6<=24r<2^s. This is an all-integer
proof, not extrapolation from a fixed tree palette or a large-order sample.

Consequently arbitrarily many real components do not by themselves guarantee
a removable LC component subunion. This does NOT refute an entrance theorem
with additional ACTUAL-minimum-bad/HEREDITARY premises: neither is asserted
for these examples. With the additional old Phase-10 sufficient large-arm
hypothesis, all component subunions are even unimodal; that unimodality is
inherited and is NOT a new Round-6 arm-threshold theorem.

B can refute this statement with r,s meeting the gate and an LC nonempty
component subunion, verified by complete exact coefficients. Non-LC is not
an original valley. Both C5 batches and their execution counts remain separate.
