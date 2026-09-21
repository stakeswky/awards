# A7 peer interface v1: history paid at a long pendant path

Run: 20260921T034427Z_round7_history_root. ORIGINAL and general A4-T/A4-R
remain NOT_CLOSED/UNPROVED. This immutable early interface is not final replay.
The main new assertion below is a scoped structural assertion under audit,
not an assertion that every tree supplies its length condition.

## A7-PENDANT-ROOT-v1 (written derivation; final audit in progress)

Let E be ANY nonempty finite simple unweighted connected tree with specified
vertex v, d=alpha(E). Attach a bare pendant path v,x1,...,xN, with all xi new,
xN a leaf, and each other xi degree two. Assume N>=128(d+2)^2. Put T=E+path,
F_m=E plus the first m new path vertices and p^(m)=I(F_m). No unimodality,
log-concavity or HEREDITARY hypothesis on E or its states is needed.
For the completed T compute h=floor(n(n-1)/(4n-2))+1 and
beta=ceil(alpha(T)(n-1)/(n+alpha(T))). For EACH h<=k, k+1<beta with
p_(k+1)(T)<=p_k(T), the actual leaf xN is a compensating root:

 q_xN=k[(k+2)p_k(F_(N-2))-(k+1)p_(k+1)(F_(N-2))]>0,
 Qminus_xN=tau-q_xN>=p_k(F_(N-2))>0,
 tau=(k+1)(k+2)(p_(k+1)(T)-p_(k+2)(T)).

The current nonincrease follows from actual History, not from an assumption
that tau>=0. In the central band K=floor(N/4), L=ceil(N/3)+d, all m=N-3..N
satisfy L_s(p^(m))/(p_s^(m))^2>=5/N for K<=s<=L. Also for m=N-2..N,

 p_(k+1)^(m)/p_k^(m) - p_(k+1)^(m-1)/p_k^(m-1) >=3/(20N)

for each central k. These proved-coefficient goals supply the actual leaf
premises rather than imposing them on arbitrary HEREDITARY graphs.
In particular, starting at a first strict decline i inside the band, the
FULL history obeys for i<=k, k+1<=L,

 p_(k+2)(T)/p_(k+1)(T) <= (1-5/N)^(k+1-i)*p_(i+1)(T)/p_i(T)<1.

Prefix and tail signs from the same exact kernels give WHOLE unimodality.
All boundary-state mass remains: p^(m)=A*f_m+B*f_(m-1), A=I(E-v),
B=xI(E-N[v]), f_m(t)=binom(m-t+1,t). Neither B nor any mixed covariance is
removed. A signed covariance bound is paid by explicit path curvature;
no increasingly fine numerical grid supplies a missing graph premise.
Full proof will include the derivative constants and support/endpoint joins.

Exact refutation: give the completed graph, specified E,v,N, full p and the
leaf deletion arrays, actual k, all gate checks and a violation. A short
chain outside the gate or a bad other root does not refute this statement.
This graph class overlaps the distinct INTERFACE_ONLY A6 long-connector
claim; root existence and the history contraction above were not its claims.
We do not certify that interface's original 64 constant or merge its records.

## A7-R-v1 (unchanged A4-R, UNPROVED)

For EVERY finite connected HEREDITARY tree T and EACH h<=k,k+1<beta with
History(T,k), does SOME root r have Qplus>=0 and Qminus>=0? Here History
means there is i<=k with Delta_i<0 and all Delta_i,...,Delta_k<=0;
HEREDITARY means ALL proper induced forests are unimodal, not only LOCAL.
With a=I(T-r), j=I(T-N[r]),
 Qplus=k[(k+2)j_k-(k+1)j_(k+1)],
 Qminus=(k+1)(k+2)(a_(k+1)-a_(k+2))+(k+2)j_k-2(k+1)j_(k+1).
Refutation requires ALL roots fail at the SAME qualified k and a separate
HEREDITARY proof. Preserve full graph/coefficient arrays and the whole valley
test. A true ORIGINAL rebound additionally needs p_(k+2)>p_(k+1).
P66/P142 lack History at their failing positions and refute neither target.
No discrete intermediate-value principle or general no-jump claim is assumed.

Sources read: exact Round7 task; mounted A6 leaf/history final package
run20260921T014921Z; remote A6 long-connector directory, which contains ONLY
its early interface at d9707fe9; D6 actual fixed-edge proof and both C6 scopes.
Initial live HEAD d9707fe9859fa015f5dc0ba8906b798ec6bb4857. All writes remain
in this unique A7 directory. Later audits/statuses append without altering v1.
No external review, Lean, novelty or peer receipt is asserted.
