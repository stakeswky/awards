# C8 peer interface v1 — misalignment payment and an actual stronger-gate failure

Run: 20260921T123043Z_round8_misalignment_strip.
ORIGINAL=NOT_CLOSED. No finite all-size closure, priority, external review or Lean claim.
Objects are finite simple undirected unweighted forests. Only WHOLE component
subunions are used. This is distinct from remote C7-033701 and space C7-043500.

## Shared exact definitions

Let F=X disjoint-union Y, with both blocks nonempty and their whole coefficient
sequences A=(A_0,...,A_a), B=(B_0,...,B_b) unimodal. Zero-pad all coefficients.
Let u,m be the LAST modes, z=k+1, q=z-m-1. In 0<=q<a put
D_j=B_j-B_(j-1), INCLUDING j=0,b+1;
P_z=sum_j max(D_j,0) A_(z-j), N_z=sum_j max(-D_j,0) A_(z-j),
and define P_next,N_next at z+1. Both N's are positive.
For 0<=l<a define U_l=sum_(z-j>l) max(D_j,0) A_(z-j),
V_l=sum_(0<=z-j<=l) max(-D_j,0) A_(z-j), W_l=U_l V_l.
Use W_(-1)=W_a=0, r_i=A_(i+1)/A_i for i=0..a, including r_a=0.
Let t_i=(r_i-1)(W_i-W_(i-1)); C0=P_z A_0 max(0,-D_(z+1)).
I=[q+1,u-1] if q<u-1, I=[u,q] if q>u-1, otherwise I is empty.
Loss=-sum_(i in I)t_i>=0; Outside=sum_(i not in I)t_i>=0.
With p=A*B and ell=p_(z-1)-p_z, the inherited signed identity is

    N_z(p_z-p_(z+1))=N_next ell+C0+Outside-Loss.

A current plateau ell=0 is allowed. History is an actual earlier strict decline
with no subsequent increase through k, not an approximation to equality.
The middle conditions use the COMPLETED graph:
h=floor(M_max(n-1)/(4M_max-2))+1, beta=ceil(alpha(n-1)/(n+alpha)),
h<=k and k+1<beta. No history is imposed on either block.

## C8-LARGE-PAY-v1 — external-dependent, all-shape asymptotic payment

There exists an absolute N_LC such that for every forest F of order n>=N_LC,
every ordered complete-component split with whole-unimodal A,B, and every
project-middle index k in the above mode band with ell>=0,

    N_next ell+C0+Outside-Loss
      = N_z [L_z+p_z ell]/p_(z-1)
      >= N_z L_z/p_(z-1) > 0,

where L_z=p_z^2-p_(z-1)p_(z+1). Thus all actual allocations satisfy
R-V=G_F(k)>=z(z+1)L_z/p_(z-1)^2>0.

Dependency: Fang, Lu, Nevo, Yao and Zheng, arXiv:2609.20961v1 (17 Sep 2026),
Theorem 1.2: every sufficiently large n-vertex forest is strictly LC for
n/5<=j<=17alpha(F)/25. The project middle lies wholly in that interval:
z>=h+1>n/5 and z<beta implies z<2alpha/3<17alpha/25, since alpha>=n/2.
This is an application of an EXTERNAL preprint theorem, not a new proof of that
theorem and not an assumption that the project's G is already nonnegative.
The threshold is not numeric in the retrieved paper. No finite graph in this
run is certified to exceed it. All sizes below it remain unresolved here.
The preprint's root-moment, uniform CLT and all-frequency/Fourier argument is
separate from the cut identity; an ordinary variance upper bound alone would
not supply the sign. No automatic alignment or full component-LC window is used.

Refutation must distinguish failure of our algebra/range inclusion from a
failure of the external theorem. A finite numerical failure without a justified
n>=N_LC cannot refute this existential-threshold statement.

## C8-DESC-ONLY-v1 — an ACTUAL stronger entrance is false

The strengthening Loss<=N_next ell, even allowing a choice of orientation,
is false for actual whole-unimodal non-LC components with real middle History.
The exact two components in certificates/STRIP_SEARCH_2.json have orders226,212.
Their union has n438,alpha229,M_max226,h110,beta151. At k137,z138,
the first strict decline is at137 (NOT an earlier-history position).
Their modes are71,66, so I is the one-index strip [71], or [66] when reversed.
Both whole components and the product are non-LC but unimodal; both C5 full
window orientations fail. C0=0. Exact Loss/(N_next ell) is approximately
2.274385020367648 in one direction and2.246763304329081 in the other.
Both directions therefore fail the descent-only gate. Complete payment,
Pay_modal, Pay_max, Pay_all_envelope and Pay_exact remain positive.

HEREDITARY=UNKNOWN for this ordinary graph. This does NOT refute a version
restricted to actual minimum ORIGINAL counterexamples or proved HEREDITARY.
It does NOT refute C8-LARGE-PAY or ORIGINAL. It demonstrates why the actual
Outside must be retained. The graph is not the historical B226/B212 pair:
its full saved edges, not its component orders, determine its identity.
The final certificate will include complete edges, coefficients, strip rows,
all four old Pay values, actual allocation weights and a second graph recount.
No assertion is made that another window has read this interface.
