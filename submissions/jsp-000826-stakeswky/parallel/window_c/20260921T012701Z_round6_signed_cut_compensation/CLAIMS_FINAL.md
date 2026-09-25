# C6 final peer interface (v1 retained; modal specialization added)

Run 20260921T012701Z_round6_signed_cut_compensation.
ORIGINAL=NOT_CLOSED. General C4-F=NOT_CLOSED. No unproved A/D claim is assumed.
This final interface contains the same TWO claims as the published v1. It does
not assert automatic payment for every forest. Full proofs are in PROOF.md.

## Claim C6-SC: conditional total signed comparison

For every finite simple unweighted forest partition F=X disjoint-union Y into
nonempty complete component subunions, let A_i=p_i(X), B_j=p_j(Y), with positive
supports 0..a and 0..b and zero padding. Assume B is whole-unimodal and m is its
last modal index. For every integer m+1<=z<=m+a put q=z-m-1 and

 D_j=B_j-B_(j-1), INCLUDING j=0,b+1;
 P_z=sum_(j<=m)D_j A_(z-j), N_z=sum_(t>m)(-D_t)A_(z-t),
 r_i=A_(i+1)/A_i (0<=i<=a, r_a=0), c_l=r_l-r_(l+1),
 U_l=sum_(j<=m,z-j>l)D_j A_(z-j),
 V_l=sum_(t>m,0<=z-t<=l)(-D_t)A_(z-t), W_l=U_l V_l.

N_z and N_(z+1) are strictly positive. Let H_l=max_(0<=i<=l)A_i and
T_l=max_(l<i<=a)A_i. For 0<=l<a the proved mass envelopes are

 Wbar_l=P_z min(N_z,H_l B_(z-l-1))       for l<q,
 Wbar_l=N_z min(P_z,T_l B_(z-l-1))       for l>=q.

Define C0=P_z A_0 max(0,-D_(z+1)), J=max({0} union {c_l W_l:c_l>0}),
E=sum_(c_l<0)(-c_l)Wbar_l, and, with p=A*B,

 Payment_z=N_(z+1)(p_(z-1)-p_z)+C0+J-E.

The following theorem is PROVED WITHOUT any full LC-window assumption:

 P_z N_(z+1)-P_(z+1)N_z=C0+sum_l c_l W_l>=C0+J-E,
 p_z-p_(z+1)>=Payment_z/N_z.

Every inverse cut is included in the one total bill E. No negative local sigma
or supported allocation is clipped. For k=z-1, the ACTUAL component budget obeys

 R-V=G_F(k)>=(k+1)(k+2)Payment_z/[p_k(F)N_z].

Consequently Payment_z>=0 and actual History(F,k) forbid the next rise, including
h<=k,k+1<beta. The inequality itself needs neither History nor HEREDITARY.
At a current plateau, the decline supply is zero but the denominators stay positive.
Before the mode band a strict decline is impossible; after it a later rise is
impossible. Thus an all-history-step payment gate gives full unimodality.

**Modal specialization.** If A is also unimodal, let u be its last mode. Since
A_u>=A_(u-1),A_(u+1), the modal c_(u-1)>=0. Replacing J by the FIXED donor
c_(u-1)W_(u-1) preserves the theorem. HEREDITARY supplies component unimodality
in a minimum bad forest, but does not by itself establish that this weighted
supply is sufficient. The modal weight is allowed to be zero.

UNPROVED STRENGTHENING: forest compatibility plus minimum-bad/HEREDITARY conditions
always forces Payment>=0, or forces another proved entrance. Do not report it as
proved from these finite tests. A failure of Payment>=0 alone is not ORIGINAL.
To refute the PROVED inequality, supply actual X,Y, full coefficients, exact z,m,
all definitions and a violation of the lower bound. To refute an ORIGINAL claim,
a full actual descent-then-rise sequence and the graph must also be provided.

## Claim C6-LCFREE: unconditional bounded-count entrance is false

For every r>=1 and s>=6 with 2^s>24r, form T_s from a center, three adjacent
hubs and s private two-edge arms at EACH hub. Form F from r disjoint copies.
Every nonempty complete component subunion of F is non-LC.

Indeed u=2^s+s, v=s2^(s-1)+binom(s,2), and the penultimate LC minor of t copies,
1<=t<=r, is exactly t[((9t+3)/2)u^2-3v-2^(3s)]<0, since
u<=2^(s+1) and 18t+6<=24r<2^s. The graph formula is
I(T_s)=[(1+2x)^s+x(1+x)^s]^3+x(1+2x)^(3s).

This is an all-integer proof. No fixed finite palette is extrapolated. It rules
out an unconditional component-count-forces-LC shortcut, NOT an entrance theorem
with extra ACTUAL-minimum-bad/HEREDITARY hypotheses. These examples are not original
counterexamples. An optional all-subunion-unimodal version uses the OLD Phase10
bound s>=192(4r+1)^2; that unimodality is explicitly inherited, not a C6 arm result.

## Evidence and type restrictions

The material has 10 qualified middle/history positions; all pass both donor
versions. Nine have neither C5-W orientation available. Six retain negative local
sigma mass. The one middle inverse-Toeplitz control has an old entrance in the
opposite orientation and is not counted as a both-window-failure case.
The total-negative-H example T26+K2 at k=13 is a separate TAIL control:
6009,103,2; H=-654; Payment=102*5906-654=601758; N=5958; next loss=101.

These statements are for whole ordinary graph coefficients and complete component
unions. No transfer to root-conditional availability, arbitrary edge removal, or
components of E's symmetric-difference counting is asserted. The two C5 batches
remain separate; only the space 173613Z final was fully read and replayed.
Same-model review only. Lean, axiom audit and external peer review: NOT_RUN.
