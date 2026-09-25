# A10 structure-sensitive interfaces v1

Run: 20260922T055330Z_round10_core_profile. ORIGINAL=NOT_CLOSED.
These are written derivations under final analytic and executable audit, not
completed replay receipts. A9's 2^2600000 theorem is retained unchanged.
All graphs below are finite simple undirected unweighted forests. No
HEREDITARY, LOCAL, component LC, or root-budget positivity is assumed.

## A10-PROFILE-v1: a finite structural sufficient condition

Choose H such that its intersection with each original component is empty or
connected. Every component A_i of F-H has order m_i<=B, B>=1. It then touches
at most one H vertex. Empty-core original components are included among A_i.
Let beta_v=max({m_i:A_i touches v} union {0}), w_v=1+3 beta_v.
Fix a centroid decomposition of the induced forest H, with node (A,v) for a
connected core region A and its chosen centroid v. Orient A away from v. Set

 D_A=sum_(z in A) w_z,
 Gamma_Av=4 sum_(z in A) beta_z^2
       +sum_(oriented edges x->y in A)(sum_(z below y) w_z)^2,
 U=sum_nodes D_A^2, W=sum_nodes Gamma_Av^2, V=sqrt(W)+U,
 nu=(sum_i m_i^2)/4+U, v0=n/8192.

Root-conditioning in ANY actual reveal history obeys
 q(1-q)delta^2<=D_A^2 and q(1-q)gamma^2<=Gamma_Av^2.
The off-core degrees/counts are arbitrary. Indeed sqrt(q)t<=3 for
 t=sum off-core child occupation probabilities, uniformly for lambda in
[1/4,12]. This bounds their aggregate influence without assuming each such
child contribution nonnegative or omitting a rare occupied core state.
Centroid reveals consequently give Var(M)<=U and
 E|S-sigma^2|<=sqrt(W)+U, while v0<=sigma^2<=nu.
S has BOTH its centered martingale part and negative variance drift.

Put eta=min(1/2,n/(65536 nu)). For ANY real T>0 with
 T^2<=v0/B^2 and eta*T^2>=1/2, define

 Phi=9B/sqrt(v0)+B*V*T^6/(18*v0^(3/2))
          +V*T^5/(30*v0)+U/v0+1/(8*v0)
          +(2T/eta)*exp(-eta*T^2).

Then, for EVERY lambda in [1/4,12] whose SIZE mean is an integer j,

 |sigma^3(2Pr(X=j)-Pr(X=j-1)-Pr(X=j+1))-1/sqrt(2pi)|<=Phi.

If n>=1000 and Phi<1/3, the WHOLE independence sequence is unimodal;
central strict LC holds on n/5<=j<=17alpha/25. Current descent/history then
gives the true next-step sign, but not necessarily a compensating root.

Key analytic change from A9: for |t|<=sigma/B, Gaussian block replacement
retains damping from all other blocks. Together with E(M-mu)=0 this gives

 |chi(t)-exp(-t^2/2)| <= B/sigma*|t|^3*exp(-t^2/3)
   +B*V/sigma^3*|t|^3+V/(2sigma^2)*t^2
   +U/(2sigma^2)*t^2*exp(-t^2/2).

All histories, including S=0, are averaged. The lattice multiplier and BOTH
full-frequency tails are retained. No full coefficient sign is an input to
Phi. More accurate certified graph profiles may replace v0,nu,U,W,eta;
any such replacement must be separately proved, not read from a grid.

Refutation must supply a real forest, its full H/B/decomposition data,
activity and violated bound, or a gap in the displayed analytic chain.
Phi>=1/3 merely fails this sufficient gate. It is NOT an original valley.

## A10-CORE-v1: a paid polynomial structural exclusion

Let R=|H| and ell=ceil(log2(2B)). For EVERY H/F/B as above,

 n>=2^96 * B^5 * ell^3 * (R+1)^3

implies complete unimodality. The proof uses
 U<=32B^2 R^2, W<=128B^4 R^6, V<=64B^2(R+1)^3,
 T=2^12 sqrt(B ell), eta0=1/(65536B).
All six error contributions are then below 1/128 in total. This is a
structural theorem, not a replacement universal cutoff or a claim that every
remaining tree satisfies the gate.

If H is empty, the sharper sufficient condition is
 n>=2^40 * B^3 * ell.
Thus a bad forest with largest component order B must satisfy the strict
reverse inequality. More generally, if deleting s specified vertices leaves
components of order<=B, taking their componentwise connected hull gives
R<=s(B+1). Hence every bad forest must satisfy, for EVERY such separator,

 n<2^96 * B^5 * ell^3 * (1+s(B+1))^3.

A hull is only used as a reveal core, NEVER deleted as an allegedly LC factor.
Arbitrary off-core shapes and their original attachment edges remain present.
No minimum-bad graph is assumed connected. No B9 catalog completeness is used.

Sources: A9 actual mounted full proof/archive, remote PROOF_PART1/2/3;
Fang--Lu--Nevo--Yao--Zheng's attributed root/centroid/Fourier method.
E9 space012308Z full color-mass proof read, but its unproved gate is not used.
B9 space161538Z full proof/source currently unreadable/materialization denied;
its finite tables are not silently certified or used as lemmas.
Initial live HEAD599a1fe3; only this new A10 directory may be written.
No Lean build, independent external review, global novelty or peer receipt
is asserted by this early publication. Final bounds and tests follow separately.
