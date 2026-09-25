# A9: an explicit finite-order version of the large-forest argument

Run: `20260921T161559Z_round9_effective_cutoff`.

**ORIGINAL = NOT_CLOSED.** This is a written quantitative proof with exact
arithmetic certificates, not a Lean build or independent external peer review.
The sufficiently-large forest theorem and the root/centroid/Fourier strategy
are due to Fang, Lu, Nevo, Yao and Zheng [FLNYZ, arXiv:2609.20961v1,
17 September 2026]. The present work makes that strategy effective with
conservative explicit constants. Its main replacement is a finite-frequency
Gaussian comparison that avoids an uneffectivized CLT-to-characteristic-function
step. No claim of global novelty or authorship of the external theorem is made.

## 1. Statements, distributions and all quantifiers

F is any finite simple undirected unweighted forest, possibly disconnected,
on n vertices. Let i_j(F) count independent j-subsets, i_0=1, and extend by
zero outside 0,...,alpha(F). For every lambda in K=[1/4,12], give an independent
set I probability lambda^|I|/Z_F(lambda), and put

 X=|I|, mu=E X, sigma^2=Var X, pi_j=Pr(X=j),
 chi(t)=E exp(it(X-mu)/sigma).

These are total-size moments at fixed activity, NOT the fixed-rank extension
moments denoted mu_k in earlier windows. For n>0, sigma^2>0.

**A9-EFFECTIVE-v1.** For every integer n>=2^77, every such F, and every
lambda in K for which mu=j is an integer, define

 E(n)=2^199 n^(-1/4)+2^154 n^(-1/15992)
       +2^207 n^(-1/1999)+2^211 n^(-1/7996)+2^11/n+2^(-167).

Then

 |sigma^3(2 pi_j-pi_(j-1)-pi_(j+1))-1/sqrt(2 pi)| <= E(n).       (1.1)

The pi without an index in 2 pi is the circle constant. Every other pi_j is a
probability. All constants are independent of the forest, its degree sequence,
its components, its root choices, its index, and its activity within K.

**A9-CUTOFF-v1.** One explicit choice is

                N_LC=N_unimodal=2^2600000.                    (1.2)

For every n>=N_LC, every n-vertex forest has

 i_j^2>i_(j-1)i_(j+1) whenever n/5<=j<=17 alpha(F)/25,          (1.3)

and its whole independence sequence is unimodal, allowing plateaus.
In fact E(n)<1/128. This cutoff is not asserted minimal or useful for brute-force
coverage. No complete argument for the orders below it is provided.

The 17/25 endpoint is the paper's interval; the external Central.lean inspected
at commit b2a1d3ed uses the narrower 64/95. We prove the numerical comparison
for 17/25 below instead of assuming the two statements coincide. The code's
`max 1000 N1` is not used to replace N1 by 1000.

## 2. Effective contraction on the entire activity/root domain

Use the descendant rooted-tree quantities of [FLNYZ, Section 4]. If the
children of v have odds r_i and occupation probabilities q_i, then

 r_v=lambda product_i(1+r_i)^(-1), q_v=r_v/(1+r_v),
 y_v=log(lambda/r_v)=sum_i log(1+r_i)>=0.

Define delta_v to be the occupied-root minus absent-root mean of TOTAL size
in this descendant tree, and gamma_v the corresponding variance difference.
Differentiating with lambda d/dlambda, or conditioning on all child roots,
gives exactly

 delta_v=1-sum_i q_i delta_i,
 gamma_v=-sum_i q_i gamma_i-sum_i q_i(1-q_i)delta_i^2.           (2.1)

Root-selected counts include the root; all unselected-root configurations,
including those in which the root could still be added, remain in these laws.

Choose the fixed rational parameters

 p=1999/1000, rho=999/1000, C0=1000,
 a=2-2/p=1998/1999, u=1/(1-a)=1999, b0=199/200.                (2.2)

For every y>=0, lambda in K, r=lambda exp(-y), q=r/(1+r), we prove

             y q^p/log(1+r) <= rho.                          (2.3)

At exponent 2, log(1+r)=-log(1-q)>=q+q^2/2, so

 y q^2/log(1+r)<=yr/(1+3r/2)<=b0.

The last inequality is equivalent to lambda exp(-y)(y-3b0/2)<=b0.
The left side is at most 12 exp(-1-3b0/2), by differentiating it on y>=0;
its maximum is at y=1+3b0/2. This is smaller than b0 because the exact
rational certificate verifies

 (199/200) sum_(h=0)^20 (997/400)^h/h! > 12,                  (2.4)

and the positive series is a lower bound for exp(997/400).
At exponent 3/2, log(1+r)>=q gives

 y q^(3/2)/log(1+r)<=sqrt(12) y exp(-y/2)<=2 sqrt(12)/e<3.

The last inequality uses sqrt(12)<4 and e>8/3, both with elementary rational
certificates. Geometric interpolation has weights 1/500 and 499/500, hence

 y q^p/log(1+r) <=3^(1/500) b0^(499/500)<rho,                 (2.5)

where the final inequality is exactly the integer/rational comparison

                3(199/200)^499 < (999/1000)^500.

At y=0 the numerator is zero. All other y are covered by these analytic
inequalities, not by a grid or finite root samples. This is an explicit
instance of the paper's Lemma 4.2.

## 3. Root mean and variance perturbations with numbers

For a descendant u below v, let Q_v(u) be the product of child occupation
probabilities on the v-to-u path, excluding v and including u. Q_v(v)=1.
Set S(v)=sum_u Q_v(u)^p. Induction gives

 S(v)=1+sum_i q_i^p S(i)
 <=1+sum_i q_i^p(1+C0 y_i)
 <=1+(1+C0 rho)sum_i log(1+r_i)=1+C0 y_v.                    (3.1)

Here q_i^p<=q_i<=log(1+r_i), and 1+C0 rho=C0. Unrolling (2.1) for delta
has signed terms (-1)^distance Q_v(u). Holder therefore gives, for m=|T_v|,

 |delta_v|<=m^(1-1/p)(1+1000 y_v)^(1/p).

Since q_v(1-q_v)<=12 exp(-y_v), 2/p<2, and
sup_(y>=0) exp(-y)(1+y)^2=4/e<=4, it follows that

 q_v(1-q_v)delta_v^2
 <=12*10^6*4*m^a < 2^26 m^a.                                (3.2)

For the variance recurrence take G=1 and the admissible upper coefficient
L=1/2. Because q<=q*=12/13, u-1>=26, u-p>=26 and (12/13)^26<1/4,

 q^u(1+y)/log(1+r)
 <=q*^(u-1)+rho q*^(u-p)<1/2.                                (3.3)

The forcing term has an explicit u-th-root bound:

 [q^u(1+1000 y)^(2u/p)/log(1+r)]^(1/u)
 <=r^((u-1)/u)(1+1000 y)^(2/p)
 <=12 exp(-y/2)*2000(1+y)^2 <=384000.                       (3.4)

For the first step use log(1+r)>=q and q<=r. For the second, (u-1)/u>=1/2,
1000^(2/p)=1000^(1+1/1999)<2000, and 2/p<2. For the third,
exp(-y/2)(1+y)^2<=16, as differentiation gives its maximum at y=3.
Thus the paper's constant H may explicitly be (384000)^1999; no search
for a maximum or implicit compactness constant remains.

For 0<x<=1, 1-exp(-x)>=x/2. With 1/2<log 2<1 this proves

 1-2^(-1/u)>=1/(4u).

Since 4*1999*384000=3070464000<2^32, we can choose C1=2^32.
Apply Holder with conjugate exponents u and 1/a to the two sums in (2.1).
Using (3.3) for the first and (3.4) for the second proves by induction

 |gamma_v| <= C1 m^a(1+y_v)^(1/u).                          (3.5)

In detail, the induction step is at most

 [C1*2^(-1/u)+384000] y_v^(1/u)(sum_i |T_i|)^a
 <=C1 y_v^(1/u)m^a <=C1(1+y_v)^(1/u)m^a.

Leaves have gamma=0. The estimate includes arbitrary numbers and sizes of
children. Finally log(1+y)<=y and 2/u<1 give

 q_v(1-q_v)gamma_v^2
 <=12*C1^2 m^(2a) exp(-y_v)(1+y_v)^(2/u)
 <=12*2^64 m^(2a)<2^68 m^(2a).                              (3.6)

Equations (3.2),(3.6) are the fully numerical version of Proposition 4.1.
The unweighted gamma need not be small; it is the weighted square which is
bounded. No sign of delta or gamma is assumed.

## 4. Centroid decomposition keeps both random moments

In each component larger than an integer b>=1 reveal a deterministically
chosen centroid. If it is absent delete it; if occupied count its 1 and
remove its closed neighborhood. The conditional law on what remains is
again the hard-core law at the SAME lambda. Independent components stay
independent. Every child component has at most half its parent's size,
including in the occupied case. Stop at component order at most b.

Let M=E(X | all reveals), S=Var(X | all reveals). At a reveal in a component
of order m_j, with root indicator xi_j, write q_j,delta_j,gamma_j for its
actual conditional rooted-tree quantities. With the pre-reveal filtration,

 Delta M_j=delta_j(xi_j-q_j),
 Delta S_j=gamma_j(xi_j-q_j)-q_j(1-q_j)delta_j^2.               (4.1)

The negative term is the full variance drift, not an omitted state mass.
There are at most n reveals; pad by zero increments to make the length fixed.
Martingale orthogonality is therefore applicable without a limiting argument.

Along every possible history, charge m_j^(a-1) to its processed vertices.
Component halving along a vertex's chain gives

 sum_j m_j^a <= n b^(-1/u)/(1-2^(-1/u)).

At depth h, the processed components are disjoint and of order at most n2^-h;
since 2a>1 this also gives

 sum_j m_j^(2a) <= n^(2a)/(1-2^(-(2a-1))).                   (4.2)

The statements hold for disconnected original forests as well. We use

 2^26/(1-2^(-1/u)) <=4u*2^26<2^39,
 1/(1-2^(-(2a-1)))<4,

where 2a-1>1/2 and 2^(-1/2)<3/4 justify the second estimate.
Combining (3.2),(3.6),(4.1),(4.2) yields the explicit pair

 E(M-mu)^2 <=2^39 n b^(-1/u),
 E|S-sigma^2| <=2^35 n^a+2^39 n b^(-1/u).                   (4.3)

The first follows by summing conditional variances of Delta M. For the second,
the centered gamma martingale has second moment at most 2^70 n^(2a), hence
first absolute moment at most 2^35 n^a; its accumulated drift is bounded by
the first charge sum. Random variance and mean mixing are both retained.
Total variance also gives E S<=sigma^2 exactly.

