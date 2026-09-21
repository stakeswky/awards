# C8: exact misalignment loss, a stronger-gate refutation, and an external asymptotic payment theorem

Run: 20260921T123043Z_round8_misalignment_strip.

**ORIGINAL=NOT_CLOSED.** All-size C4-F remains unproved in this project run.
The all-shape large-order conclusion below explicitly depends on an external
preprint discovered in this run. It is not a new discovery of that theorem,
a finite exhaustive solution, or a formal verification claim.

## 1. Actual forests, complete support, and retained premises

F is finite, simple, undirected and unweighted. Let p_j(F) count independent
j-subsets, with p_0=1. For 0<=j<=alpha(F), p_j>0, since subsets of a maximum
independent set exist. Outside this interval coefficients are zero.
Unimodality includes plateaus: a failure requires a strict decline followed
later by a strict rise. History(F,k) requires a strict decline at some i<=k
and no rise from i through k. Current weak decrease alone is a weaker premise.

Write F=X disjoint-union Y, where both are nonempty unions of WHOLE components.
Let A=I(X), B=I(Y), a=alpha(X), b=alpha(Y), and p=A*B. In the cut formulas
assume the complete A,B sequences are unimodal and let u,m be their LAST modes.
A true vertex-minimal ORIGINAL counterexample would supply their unimodality
by smaller order. We do not assume arbitrary unimodal convolution preserves
unimodality, or label ordinary tested graphs HEREDITARY from their whole sequence.

Use the completed graph's n and largest component order M_max to set
h=floor(M_max(n-1)/(4M_max-2))+1 and
beta=ceil(alpha(F)(n-1)/(n+alpha(F))). The project middle means
h<=k and k+1<beta. These are inherited range definitions, not new theorems here.
For k<alpha define mu_k=(k+1)p_(k+1)/p_k,
d_k=k+1-mu_k, e_k=mu_(k+1)-mu_k-1. The true next-decrease budget is

 G_F(k)=(k+1)(k+2)(p_(k+1)-p_(k+2))/p_k=mu_k(d_k-e_k).

No division by d_k or current loss is used. All formulas below retain support
endpoints, including the terminal ratio zero. Component unions, selected-root
conditional availability and symmetric-difference blocks are distinct objects.

## 2. Complete signed convolution and the precise misalignment strip

Set D_j=B_j-B_(j-1), for j=0,...,b+1, including D_0=B_0 and D_(b+1)=-B_b.
Thus D_j>=0 for j<=m, and D_j<=0 for j>m. Define

 P_z=sum_j max(D_j,0) A_(z-j),
 N_z=sum_j max(-D_j,0) A_(z-j).

The exact difference p_z-p_(z-1) is P_z-N_z. In the mode band
m+1<=z<=m+a set q=z-m-1. Since m is the LAST mode,
-D_(m+1)>0, even when m=b and this is the death term. It follows that
N_z>=(-D_(m+1)) A_q>0 and N_(z+1)>=(-D_(m+1)) A_(q+1)>0.
For z<=m no strict decrease can have occurred. For z>m+a, P_z and all later
positive convolutions vanish, so a later rise is impossible. The band is not
an instruction to discard coefficients from any count.

For 0<=l<a let
U_l=sum_(z-j>l) max(D_j,0) A_(z-j),
V_l=sum_(0<=z-j<=l) max(-D_j,0) A_(z-j), W_l=U_l V_l.
Set W_(-1)=W_a=0, r_i=A_(i+1)/A_i for 0<=i<=a, with r_a=0.
Finally C0=P_z A_0 max(0,-D_(z+1)).

Expansion of H_z=P_z N_(z+1)-P_(z+1)N_z over j<=m<t gives terms

 D_j(-D_t)[A_(z-j) A_(z+1-t)-A_(z+1-j) A_(z-t)].       (2.1)

Put R=z-j, S=z-t. Inside 0<=S<R<=a the bracket equals
A_R A_S sum_(S<=l<R)(r_l-r_(l+1)). The case S=-1 contributes C0;
S<-1 or R>a gives zero. R>=q+1>=1, so there are no other lower boundaries.
The case R=a is included by r_a=0. Consequently

 H_z=C0+sum_(l=0)^(a-1)(r_l-r_(l+1)) W_l
    =C0+sum_(i=0)^a(r_i-1)(W_i-W_(i-1)).              (2.2)

The final equality is summation by parts: boundary W's are zero, so subtracting
1 from every ratio does not alter the sum. This is inherited C6/C7 algebra,
not a new all-forest inequality.

For an exact integer interpretation put
positive_i=A_i max(D_(z-i),0), negative_i=A_i max(-D_(z-i),0).
When i<=q, positive_i=0, U_i=P_z and

 W_i-W_(i-1)=P_z negative_i.

When i>q, negative_i=0, V_i=N_z, and

 W_i-W_(i-1)=-N_z positive_i.                          (2.3)

Both formulas include i=a under W_a=0. In particular W_q=P_z N_z;
W increases weakly through q and decreases weakly afterwards. Equations(2.3)
show that each difference of W is divisible by A_i. Thus each summand

 t_i=(r_i-1)(W_i-W_(i-1))

is the integer (A_(i+1)-A_i) times an actual integer signed-difference mass.
This does not replace real graph weights by freely chosen probabilities.

Since A is unimodal, r_i-1>=0 before u and <=0 at and after u. Hence t_i<=0
only on the following strip, where in fact every t_i is nonpositive:

 I=[q+1,u-1] if q<u-1; I=[u,q] if q>u-1; I=empty otherwise.

Define Loss=-sum_(i in I)t_i and Outside=sum_(i not in I)t_i. Both are
nonnegative, with no small or negative term omitted. The strip loss is exactly

 q>=u:    Loss=P_z sum_(i=u)^q (A_i-A_(i+1))(B_(z-i-1)-B_(z-i));
 q<u-1:  Loss=N_z sum_(i=q+1)^(u-1) (A_(i+1)-A_i)(B_(z-i)-B_(z-i-1)).  (2.4)

These are full weighted sums of real adjacent coefficient differences, not
upper bounds. At alignment q=u-1 the loss is zero, recovering C7 without
assuming that a general history is aligned.

Writing ell_z=p_(z-1)-p_z, the exact payment identity is

 N_z ell_(z+1)=N_(z+1) ell_z+C0+Outside-Loss.           (2.5)

The desired statement is a sign of this TOTAL. Naming its terms or proving
(2.4) is not itself a proof that the total is nonnegative.

## 3. Earlier descent: a ledger which spends each contribution once

For consecutive z=s,...,t in the mode band, divide (2.5) by the positive
N_z N_(z+1) and telescope:

 ell_(t+1)/N_(t+1)=ell_s/N_s
     +sum_(z=s)^t (C0_z+Outside_z-Loss_z)/(N_z N_(z+1)). (3.1)

Thus the coefficient multiplier transporting the initial loss is
N_(t+1)/N_s. Every intermediate supply and loss occurs exactly once. A plateau
ell_z=0 presents no division problem. Taking just the positive initial loss
without the intervening signed ledger would be invalid. Equation(3.1) is an
accounting tool, not a bound on the cumulative bill for arbitrary forests.

The other old Pay tests remain separate. Let Splus,Sminus be the complete
positive and absolute-negative sums of (r_l-r_(l+1))W_l, Ebar the C6 upper
negative bill, and Jmodal,Jmax the fixed modal and largest single donors.
With Dpay=N_next ell+C0,
Pay_modal=Dpay+Jmodal-Ebar, Pay_max=Dpay+Jmax-Ebar,
Pay_all_envelope=Dpay+Splus-Ebar, Pay_exact=Dpay+Splus-Sminus.
Then
Pay_exact-Pay_max=(Splus-Jmax)+(Ebar-Sminus)>=0.
This separates omitted positive supply from envelope overcharge; it does not
show either is affordable. None is conflated with strip loss or local sigma.

## 4. An actual failure of descent-only payment in BOTH orientations

The exact graph is specified, without any floating reconstruction, in
certificates/KEY_CERTIFICATE.json and in the successful search's saved graph.
Its two components have orders226 and212 but are NOT the old B226/B212 trees.
They were changed by real subtree reattachments. The completed parameters are

 n=438, M_max=226, alpha=229, h=110, beta=151,
 k=137, z=138, u=71, m=66, q=71, I=[71].

The first strict decrease is at k=137 itself. A,B,p are all unimodal and
non-LC. Their negative LC indices are, respectively,109,102,209.
The complete C5 window fails in both directions: at the whole-product mode137,
its unavoidable internal minor is109 in the forward window [27,119], and102
in the reversed window [18,110]. The reduction to modal windows is used only
after the full product has been counted and found unimodal, not in a circular
proof that a hypothetical minimum bad product is unimodal.

C0=0. Exact rational comparisons give

 Loss/(N_next ell) > 2.2743 forward,
 Loss/(N_next ell) > 2.2467 reversed.

Both denominators are strictly positive. This refutes the actual-forest
strengthening that current descent ALONE always pays the strip, even after
choosing an orientation of this two-component forest. It is not merely one
failed split. The next coefficient decreases by about2.1179866%, and the whole
original sequence is unimodal. Outside pays the shortfall: all four old Pay
values and the true total are positive in both orientations.

HEREDITARY is UNKNOWN for this new graph. It does NOT refute a statement
restricted to true minimum ORIGINAL counterexamples or proven HEREDITARY.
Its component non-LC status does exclude nonempty proper LC component subunions,
but that is not the missing hereditary premise. No global minimality or local
irreducibility is claimed. No arbitrary-array failure is called an actual forest.

The tail control T26 disjoint-union K2 gives the complementary caution:
H=-654 and Outside+C0<Loss, while
5958*101=102*5906-654. This failure of OUTSIDE-only payment is in the TAIL,
not a project-middle refutation. The actual middle T26+B212 determinant-378,
the inherited T26-squared no-automatic-alignment guard, and a current plateau
are independently retained by the material audit.

## 5. An external result supplies total payment for all sufficiently large forests

### 5.1 Precise outside dependency, not a claimed new discovery

Fang, Lu, Nevo, Yao and Zheng, *Unimodality of Independence Polynomials for
Sufficiently Large Forests*, arXiv:2609.20961v1, submitted17 September2026,
Theorem1.2 proves the following statement:

 There is an absolute integer N_LC such that every n-vertex forest with
 n>=N_LC satisfies L_j=p_j^2-p_(j-1)p_(j+1)>0 whenever
 n/5<=j<=17alpha(F)/25.                                (EXT)

Source: https://arxiv.org/html/2609.20961v1 ; version/metadata:
https://arxiv.org/abs/2609.20961 . This is an external PREPRINT dependency.
The paper's full mathematical argument was read in HTML, including the final
remarks which explicitly retain the all-size problem. It does not give a
numeric N_LC. The cited Lean repository returned404 through the GitHub connector;
no formal source was obtained and no Lean build or axiom audit was run.
EXTERNAL_AUDIT.md records the scope. We do not claim the authors' theorem as ours.

### 5.2 Why this is an independent sign argument, not a variance shortcut

The external proof bounds changes under actual rooted-tree conditioning,
then proves a central limit theorem uniform over ALL forests and fugacities
lambda in[1/4,12]. Crucially it also proves an all-frequency bound on the
characteristic function, with variance comparable to n by positive absolute
constants. A CLT or variance upper bound alone would not give adjacent signs.

Here is the sign-passing step in explicit form. Write
b_j=p_j lambda^j/Z_F(lambda), let the random SIZE have mean z and variance s^2,
and let chi(t) be the characteristic function of (SIZE-z)/s. These are NOT
the project's extension mean mu_k or allocation weights. Fourier inversion gives

 s^3(2b_z-b_(z-1)-b_(z+1))
   =(1/(2pi)) integral_(-pi*s)^(pi*s)
       chi(t) 2s^2(1-cos(t/s)) dt.                     (5.1)

Uniform variance growth implies s tends to infinity. The external frequency
bound gives |chi(t)|<=exp(-c' t^2) on this integration interval, with one c'>0
for all forests. Also 0<=2s^2(1-cos(t/s))<=t^2. Uniform CLT gives
chi(t)->exp(-t^2/2) uniformly on every fixed compact interval. Domination by
t^2 exp(-c't^2) makes the real integral in (5.1) converge uniformly to
(1/(2pi)) integral_R t^2 exp(-t^2/2) dt=1/sqrt(2pi)>0.
Thus for sufficiently large n, 2b_z>b_(z-1)+b_(z+1), and arithmetic-geometric
mean implies b_z^2>b_(z-1)b_(z+1). The powers of lambda and Z cancel, yielding
L_z>0. The external mean-range proof supplies a fugacity with mean z throughout
(EXT). This explains the sign input used here; the uniform probabilistic lemmas
are still explicitly external dependencies, not new bounds checked by sampling.

### 5.3 The ENTIRE project middle is inside (EXT)

A nonempty forest is bipartite, so one bipartition class in each component
supplies alpha(F)>=n/2. For a project-middle index z=k+1,

 z>=h+1 > (n-1)/4+1 > n/5.                             (5.2)

Indeed M_max/(4M_max-2)>1/4 and floor(x)+1>x. For the upper endpoint,
z<ceil(alpha(n-1)/(n+alpha)) with z integral implies

 z<alpha(n-1)/(n+alpha) <= 2alpha(n-1)/(3n)
    <2alpha/3<17alpha/25.                              (5.3)

No estimate on component shapes or sizes relative to one another is used.
Thus (EXT) covers every project-middle index of every sufficiently large
forest, not just an aligned one or one with a fully LC component window.

### 5.4 C8-LARGE-PAY: the required TOTAL comparison

For n>=N_LC, a project-middle index z, any ordered whole-component partition
with unimodal factors, and any current ell=p_(z-1)-p_z>=0 in the mode band,
the elementary exact relation

 p_z-p_(z+1)=[L_z+p_z ell]/p_(z-1)                     (5.4)

and (2.5) give

 N_next ell+C0+Outside-Loss
    =N_z [L_z+p_z ell]/p_(z-1)
    >=N_z L_z/p_(z-1)>0.                              (5.5)

This is the promised payment of the ENTIRE real strip with a strict reserve.
It does not claim descent or Outside pays by itself. It uses an independently
proved forest-specific coefficient sign (EXT), not the assumption that G>=0.
Under actual History it forbids the next rise, including when current ell=0.
It applies simultaneously to every complete partition meeting the factor
premise. In a true minimal bad forest that premise follows from minimality;
no local History is transmitted and no choice of partition is the argument.

For the original budget this yields the numerical-in-coefficients bound

 G_F(k)>=z(z+1)L_z/p_(z-1)^2>0.                        (5.6)

This is a strict ASYMPTOTIC all-shape corollary of the external theorem.
No specific finite certificate in this run is known to satisfy n>=N_LC;
there are ZERO claimed finite verifications of that threshold. The actual438
example and all other finite controls are counted directly and do not rely
on the unknown size gate. A finite smaller counterexample, were it found,
would not automatically refute (EXT).

## 6. Reconciliation with the actual allocation budgets

For every uniform independent j-set of a forest Z, let its residual in the
ORIGINAL Z have T vertices and c components. Double-counting extensions gives
E T=mu_Z(j); since the residual is a forest, |E|=T-c and
2p_2(residual)=T^2-3T+2c. Therefore

 sigma_Z(j)=4mu-Var(T)-2E c
           =mu+mu^2-(j+1)(j+2)p_(j+2)(Z)/p_j(Z).

At a support endpoint T=c=mu=sigma=0. For each supported allocation i in F=X⊔Y,
w_i=A_i B_(k-i)/p_k(F). Conditional independence and total variance give

 R=sum_i w_i(sigma_X(i)+sigma_Y(k-i))+mu_F d_F,
 V=Var_w(mu_X(i)+mu_Y(k-i)), R-V=G_F(k).                (6.1)

All allocations, terminal ratios and negative local sigmas remain. These w_i
are not replaced by the positive/negative D weights. Equations(5.5)-(5.6)
prove a bound for the actual(6.1) through a separate coefficient sign theorem.
Refinement changes R and V by the same amount; it cannot create the reserve.

In the new438 control at k137 the exact fractions give approximately
R=406.28103759357356, V=0.009365888476824458,
G=406.27167170509676. Its negative-local-sigma mass is ZERO. The old, distinct
B212+B226 control at k137 has negative mass about4.796811890175476e-28 and
signed negative contribution about-5.2440508666508325e-31. These are retained,
not transferred to the new example to fabricate coverage.

## 7. Genuine limitations, countercontrols and next missing implication

The C7 nonforest guard is preserved: its initial coefficients match P34
through rank9 and it passes the recorded scalar bounds, but its square has
a valley. The first three coefficients force a34-vertex forest with33 edges
and sum_v binom(deg(v),2)=32. Connectivity and
sum_v(deg(v)-1)(deg(v)-2)=0 force a path; the coefficient at rank10 disagrees
with P34. It is therefore not a forest and has no HEREDITARY status. Its
negative exact strip payment refutes only the relaxed array model.

This run does NOT supply a numeric N_LC or exhaust all smaller forests.
It does NOT prove modal/max/upper-envelope gates are automatic, even for
large n: (EXT) pays the exact total, not arbitrary stronger surrogates.
It does NOT refute the minimum-bad or HEREDITARY descent-only strengthening,
because the438 forest has no such proof and is itself good.
It does NOT add a new decorated graph family, lower an arm threshold, or
claim the new preprint as a project discovery.

The unresolved finite arrow is: for every remaining actual minimum bad forest
below the unspecified external threshold, derive
Loss<=N_next ell+C0+Outside from its actual graph/induced-subforest compatibility,
or supply a complete legal original counterexample. The existence of an
asymptotic threshold does not identify this finite range computationally.
The prior C4/C5/C6 and C7 aligned-position results remain at exactly their
proved scopes. ORIGINAL and all-size C4-F are consequently NOT_CLOSED here.
