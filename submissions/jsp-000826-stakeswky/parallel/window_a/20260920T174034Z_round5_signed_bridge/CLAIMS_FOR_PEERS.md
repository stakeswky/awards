# A5 peer interface, version 1

ORIGINAL and A4-T are NOT_CLOSED. C1_GLOBAL is REFUTED. A4-R-v1 remains an
UNPROVED existential statement. Path32 refutes universal entry to A4-Q, not
A4-R. This file does not assert that HEREDITARY supplies the conditions below.

## Domain and history

F is a finite simple unweighted forest; the primary target T is connected.
p_i counts independent i-sets and is zero outside its positive support.
History(T,k) means some i<=k has p_(i+1)<p_i and all differences from i to k
are nonpositive. Recompute h=floor(M(n-1)/(4M-2))+1 and
beta=ceil(alpha(n-1)/(n+alpha)) from the complete graph.
HEREDITARY means ALL proper induced subforests are unimodal, not merely LOCAL.

## A5-FM-v1: full-middle-mass signed certificate (PROVED CONDITIONAL)

Choose any actual root r and s=k+1. Let a_i=p_i(T-r),
b_i=p_(i-1)(T-N[r]), so p_i=a_i+b_i. All external branches remain.
Assume a_s,b_s>0, and define

    c0=1-a_(s-1)*a_(s+1)/a_s^2,
    c1=1-b_(s-1)*b_(s+1)/b_s^2,
    x=a_(s-1)/a_s-b_(s-1)/b_s,
    y=a_(s+1)/a_s-b_(s+1)/b_s.

Choose rational certified bounds c0>=l0, c1>=l1,
x in [xL,xU], y in [yL,yU]. Neither l0 nor l1 is assumed nonnegative.
Let m=min(xL*yL,xL*yU,xU*yL,xU*yU), and

    B=(a_s+b_s)*(a_s*l0+b_s*l1)+a_s*b_s*m.

Then the complete minor L_s=p_s^2-p_(s-1)*p_(s+1) satisfies L_s>=B.
Consequently, if p_(s-1),p_s>0,

    1-p_(s+1)/p_s >= 1-p_s/p_(s-1)+B/(p_(s-1)*p_s).    (F)

In particular B>=p_s*(p_s-p_(s-1)) certifies the next nonincrease.
B may be negative: the existing descent pays part of the negative minor.
No division by the current descent d is used. For zero middle state mass,
use the original undivided quadratic expansion, NOT these ratios.

Proof: expand the complete minor and collect it as
L_s=p_s*(a_s*c0+b_s*c1)+a_s*b_s*x*y. A bilinear function on a closed rectangle
attains its minimum at a corner. Substitute the certified lower bounds and
rearrange the exact identity p_(s+1)/p_s=p_s/p_(s-1)-L_s/(p_(s-1)*p_s).
This proves the inequality, not the existence of a certificate for every T.
Both middle masses are retained; negative local curvature and negative cross
contribution are allowed. Bounds must be certified from actual proper-forest
counts or a structural theorem, never assumed because tests passed.

A false numerical instance of (F) satisfying its bounds refutes this lemma.
A graph lacking any chosen certificate does NOT refute ORIGINAL.
If a genuine middle-History graph has p_(k+2)>p_(k+1), it DOES refute ORIGINAL,
independently of this sufficient test.

## A5-R-audit-v1: unchanged A4-R existence test (UNPROVED)

For each connected HEREDITARY T and each h<=k,k+1<beta with History(T,k),
A4-R asks for at least one r with both original-graph raw budgets nonnegative:

    Qplus_r=k*((k+2)*j_k-(k+1)*j_(k+1)),
    Qminus_r=(k+1)*(k+2)*(a_(k+1)-a_(k+2))
              +(k+2)*j_k-2*(k+1)*j_(k+1),
    j_i=p_i(T-N[r]).

Test ALL roots before refuting existence. One bad root is not a refutation.
A failure without a HEREDITARY proof tests only the stronger no-H version.
Return the complete graph, coefficients, all root arrays, indices and premise
certificate. A4-Q failure and A4-R failure must be recorded separately.

Priority controls: Path32 at k9; the 239-vertex rewired middle graph;
separate B212/B226 certificates; and a real middle point with a negative
local LC minor or negative complete root-state raw budget. No B batch counts
are merged. Same-model replay is not external peer review or Lean.

Sources: actual A4-R file in the remote 20260920T150118Z_d99a9c directory;
A4 final archive SHA256 28316283fe54781a955def03dd41a74301fcde8111483b94b13d8ccfde9d057e.
This version is immutable; subsequent statuses and results are appended.
