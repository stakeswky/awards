# A complete computer-assisted proof for all B59 mixtures

## 0. Result, route, and evidence boundary

**Theorem (FAMILY-LC).** For every positive integer t and every list of t members
of the exact B59 palette in STATEMENT.md, with arbitrary repetitions, the actual
independent-set polynomials of T_sigma-r and T_sigma are log-concave. Therefore
their coefficients are unimodal, including the convention allowing plateaus.

The proof keeps A=product H_i, Q=product Q_i, and H_i=Q_i+xR_i throughout. It is
not induction on arbitrary pairs of sequences. We use finite certificates for
one/two/three branches, a convolution theorem to turn two/three-branch curvature
into an all-product bound, and a bound on the TOTAL possibly negative mixed
contribution when xQ is added. A rigorously derived parameter compression gives
a finite rational certificate for every 4<=t<=23. An explicit positive-polynomial
argument covers every t>=24. These three intervals exhaust the positive integers.

This is a computer-assisted mathematical proof with an explicit external
mathematical dependency and fully replayable finite computations. It is not a
kernel-checked Lean proof and not external peer review. The general forest
problem is not concluded. Section 12 identifies its separate obstruction.

## 1. Independent sets give the displayed polynomials

For a graph G, define I(G;x) by counting independent subsets as in STATEMENT.md.
If G is a disjoint union of G_1,...,G_m, taking the intersections of an independent
subset with the components is a bijection onto a tuple of independent subsets.
Cardinalities add. Consequently I(G;x)=product I(G_i;x), by distributing the
finite sums. For any vertex v, partition the independent subsets by whether v
is selected. The first class is exactly the independent subsets of G-v. Removing
v from a subset in the second class is a bijection onto the independent subsets
of G-N[v]. Hence

    I(G;x)=I(G-v;x)+x I(G-N[v];x).                         (1.1)

Neither identity defines the count; each follows from a bijection of actual
finite subsets. The empty graph has count polynomial 1. A collection of s
isolated vertices has (1+x)^s because there are binomial(s,k) subsets of size k.

At a small center c_ij of our graph, not selecting the center leaves s_ij leaves
independently available, contributing (1+x)^s_ij; selecting it forces every leaf
absent, contributing x. If u_i is absent, these stars are disjoint and give Q_i.
If u_i is present, all their centers are absent, all S_i leaves are free, and
this case gives x R_i. The entire branch at u_i therefore has H_i=Q_i+xR_i.

In T_sigma-r, not selecting h leaves the t branches independent and gives A;
selecting h forces every u_i absent and gives xQ. Thus I(T_sigma-r;x)=E=A+xQ.
In T_sigma, not selecting h also leaves r free, giving (1+x)A; selecting h
forces both r and all u_i absent, giving xQ. Thus I(T_sigma;x)=P=(1+x)A+xQ.
Every construction step attached a new vertex by exactly one edge. Starting
from {r,h}, this preserves connectedness and absence of cycles and introduces
neither a loop nor a repeated edge. Deleting the leaf r leaves a tree. This
establishes the required graph semantics for every parameter, not just controls.

## 2. Notation, supports, and elementary parameter bounds

All polynomials have nonnegative coefficients. Subscripts denote coefficients,
and coefficients outside a polynomial's support are zero. Coefficientwise
inequalities are denoted by >= below. Put

    z=(1+x)^epsilon A, b=xQ, epsilon in {0,1},
    f=z+b, M=S+t+epsilon, N=S+4t+epsilon.

Every Q_i has positive coefficients exactly at 0..S_i, and every H_i at
0..S_i+1. Both constants are 1. Therefore Q, A, z and f have positive initial
supports 0..S, 0..S+t, 0..M and 0..M respectively. In particular there are no
internal zero coefficients. The positive support of b is 1..S+1, contained
in the support of z because t>=1. Zero extension is harmless at all endpoints.

Every permitted branch satisfies

    3<=S_i<=17, 1<=d_i<=3, S_i>=5d_i-2, S_i+d_i<=18.

These follow from the displayed nine palette rows and are also checked for
all 59 branches. Adding gives

    3t<=S<=17t,
    t<=D<=dbar(t,S):=min(3t, floor((S+2t)/5), 18t-S).       (2.1)

The finite envelope below checks ALL integers S in 3t..17t, even if a value
were unattainable. It never assumes that every value is attained. Replacing
D by the upper bound dbar only weakens the coefficient bounds that follow.

## 3. Curvature and the external convolution theorem

For a positive initial-support polynomial g of degree m<=n, say g is ULC(n)
when g_k/binomial(n,k) is log-concave, or equivalently

    k(n-k) g_k^2 >= (k+1)(n-k+1) g_(k-1)g_(k+1)          (3.1)

for 1<=k<m, with zero extension to degree n. It follows that

    g_k^2 >= (1+c_n(k)) g_(k-1)g_(k+1),
    c_n(k)=(n+1)/(k(n-k)), 1<=k<m.                      (3.2)

Indeed (k+1)(n-k+1)-k(n-k)=n+1. This also implies the weaker factorial
log-concavity inequality k g_k^2 >= (k+1)g_(k-1)g_(k+1), since c_n(k)>=1/k.

We use **Liggett's finite-order convolution theorem**, in the precise form
of Theorem 1.1 of Leonid Gurvits, *A short, based on the mixed volume, proof
of Liggett's theorem on the convolution of ultra-logconcave sequences*,
arXiv:0804.1181v1, dated 8 April 2008:

    ULC(n_1) times ULC(n_2) is ULC(n_1+n_2).             (3.3)

Primary source: https://arxiv.org/html/0804.1181v1 , Definition (2) and Theorem
1.1. The original result is T. M. Liggett, JCTA 79 (1997), 315–325. The exact
order-addition statement, nonnegative coefficients, and applicability to order
larger than the degree were checked against this version. We use only positive
initial support, never arbitrary internal-zero sequences.

For completeness, there is no unproved padding issue in our use. For degree
m<n, write c_k=g_k/binomial(n,k)>0 on 0..m. Extend it to m<k<=n by
c_(m+r)=c_m delta^r, with delta>0 no larger than c_m/c_(m-1) when m>=1.
The extension is positive and log-concave, including the join. Multiply by the
binomial coefficients and apply the positive full-support form of (3.3).
Let delta tend to zero for both inputs. Each coefficient and inequality is a
finite polynomial expression and hence continuous. This yields exactly (3.3)
for our zero-padded inputs. Degree-zero inputs are covered by any positive
geometric extension or directly as constant factors. Thus the cited theorem's
support assumptions are met.

## 4. Complete finite branch and block facts

The following finite arithmetic facts are verified by src/verify_blocks.py.
They use the exact B59 list, not the older B21 list.

**B1.** For every permitted branch, Q_i<=R_i/(3/4), that is, 4R_i>=3Q_i
coefficientwise. In addition, for g equal to Q_i or H_i, m=degree(g), and
0<=k<=m, with g_(m+1)=0,

    (m-k-1)g_k <= (k+1)g_(k+1) <= (m+d_i-k)g_k.          (4.1)

**B2.** For EVERY multiset of u=2 or u=3 branches, its products A_u and Q_u
satisfy ULC(S_u+4u) and ULC(S_u+3u), respectively.

**B3.** For EVERY multiset of t=1,2,3 branches, E and P are log-concave.

Here is a fully specified finite procedure, rather than an extrapolation:
Generate B59 in each of the two equivalent ways in STATEMENT.md and compare
sets. Construct each Q_i by multiplying (1+x)^s+x and H_i by adding x(1+x)^S_i.
Compare the branch coefficients with the alternative expansion

    Q_i = sum_{J subset {1,...,d_i}} x^|J| (1+x)^(S_i-sum_{j in J}s_ij).

For B1, multiply both sides by 4 or use the integer form (4.1) at every index.
For each 0<=i_1<=...<=i_u<59, form A_u and Q_u and test the integer differences
in (3.1) for B2, and E_k^2-E_(k-1)E_(k+1), P_k^2-P_(k-1)P_(k+1) for B3.
Missing coefficients are zero. Positive support and exact degree are checked.
The loops inspect every relevant interior coefficient, not just coefficients
near the mode. The numbers of records are exactly

    binomial(59,1)=59,
    binomial(60,2)=1770,
    binomial(61,3)=35990, total 37819.

Products and the constructed graphs are invariant under permuting branches,
so sorting a branch list loses no case; repetitions are retained by weak
inequalities on the indices. B2 covers 37760 block multisets. The run checks
2,723,570 block ULC inequalities and 2,874,321 prefix LC inequalities.

All these comparisons passed on the fresh source. A second execution constructs
Q_i by the subset formula and multiplies via positional integer encoding rather
than coefficient-by-coefficient convolution. Its branch and full-multiset
coefficient hashes agree with the first execution. For positional multiplication,
choose base B=2^w with B>sum(a)sum(b). Each product coefficient is at most that
product of sums and hence strictly below B, so there are no carries. Evaluating
the two polynomials at B, multiplying integers, and reading base-B digits therefore
recovers exactly the convolution. This proves the alternative algorithm's
correctness; a matching hash alone is not used as a mathematical lemma.

Files certificates/blocks-primary.json and blocks-replay.json identify the
complete finite domains and results. The source reconstructs every coefficient
and comparison; these are replayable finite certificates, not opaque trusted
assertions. The computational trust boundary is ordinary exact Python integer
arithmetic and the reviewed finite loops, not Lean kernel verification.

## 5. From two/three-branch blocks to arbitrary products

For any t>=2, an even t is a sum of twos. An odd t>=3 is three plus a sum of
twos. Partition the ACTUAL list of t branches into these groups. B2 applies to
each group, irrespective of its members or their repetitions. Apply (3.3)
repeatedly; the orders add. For every t>=2,

    A is ULC(S+4t),  Q is ULC(S+3t).

The polynomial 1+x is ULC(1). A further application of (3.3), or no extra factor
when epsilon=0, gives

    z=(1+x)^epsilon A is ULC(N), N=S+4t+epsilon.          (5.1)

Thus z obeys (3.2) with this N; Q is log-concave; and b=xQ is log-concave after
zero extension. Shifting by one does not change an interior log-concavity
inequality, while the new support boundary has zero on the right-hand product.
This is the required all-product result. It says nothing about closure of an
arbitrary pair (a,q), and it never presupposes log-concavity or unimodality of
z+b. In particular the v4 counterexample does not satisfy these premises.

## 6. Exact product identities for adjacent coefficient ratios

For a polynomial g positive on 0..m define its birth rate

    lambda_g(k)=(k+1)g_(k+1)/g_k, 0<=k<=m,

including lambda_g(m)=0. Let G=product_i g_i, of degree sum_i m_i. For any
supported k, the exact identity

    lambda_G(k)
      = sum_{j_1+...+j_t=k} [product_i (g_i)_(j_i)/G_k]
                             * sum_i lambda_(g_i)(j_i)  (6.1)

holds, with indices in the respective supports. To prove it, multiply the
right side by G_k. The summand for i becomes (j_i+1)(g_i)_(j_i+1) times all
other coefficients. Reindex l_i=j_i+1. For every allocation of k+1 among the
factors, the contributions from all possible i sum to
sum_i l_i=k+1; terms with l_i=0 contribute zero. This is (k+1)G_(k+1).
The bracketed weights are nonnegative and sum to one by the product formula.

Apply (4.1) termwise inside (6.1). For Q, the summed degree is S; for A it is
S+t. A factor 1+x has exact rate 1-j. Using nonnegativity to clip lower bounds,
for every supported k we obtain

    max(0,S-t-k) <= lambda_Q(k) <= S+D-k <= S+dbar-k,
    max(0,S+epsilon-k) <= lambda_z(k)
                         <= M+D-k <= M+dbar-k.           (6.2)

Unlike a general shape assumption, these bounds have been proved for the
specific products from the branch inequalities, for every number of factors.

B1 also gives H_i=Q_i+xR_i >= (1+3x/4)Q_i. Multiplication preserves a
coefficientwise inequality for nonnegative coefficients. Therefore

    z >= A >= (1+3x/4)^t Q.                              (6.3)

This retains the quantitative relation lost by the failed broad insertion
argument. In particular it is much stronger than merely A>=Q.

## 7. A bound for the total negative mixed contribution

For a sequence g let Delta_k(g)=g_k^2-g_(k-1)g_(k+1). Fix an interior index k
of z, so z_(k-1),z_k,z_(k+1)>0. Suppose b is nonnegative and log-concave, and

    z_k^2 >= (1+c) X, X=z_(k-1)z_(k+1), c>=0.

Set u=b_(k-1)/z_(k-1) and v=b_(k+1)/z_(k+1). Expanding gives

    Delta_k(z+b) = Delta_k(z)+Delta_k(b)
                    +2z_k b_k-z_(k-1)b_(k+1)-z_(k+1)b_(k-1).

Log-concavity gives Delta_k(b)>=0 and z_k b_k>=sqrt(X b_(k-1)b_(k+1))
=X sqrt(uv). The other two cross terms are Xv and Xu. Consequently

    Delta_k(z+b) >= X [c-(sqrt(u)-sqrt(v))^2].            (7.1)

This controls the total cross contribution. It does NOT assume every mixed
term is nonnegative. We have even discarded extra positive curvature in
z_k b_k, so proving the displayed sufficient bound is safe.

If u,v>0 and r=v/u, then for r<=1 and r>=ell>=0,

    (sqrt(u)-sqrt(v))^2 <= u*(max(0,1-sqrt(ell)))^2;

for r>=1 and 1/r>=w>=0,

    (sqrt(u)-sqrt(v))^2 <= v*(max(0,1-sqrt(w)))^2.         (7.2)

These follow by factoring out sqrt(u) or sqrt(v) and monotonicity of the square
on 0..1. If ell>1 the r<=1 case is impossible, and its bound can be set to zero;
the corresponding statement holds for w>1. Zero-neighbor cases are treated
explicitly in the next section. Equations (7.1)–(7.2) are the new mixed-term
mechanism used below.

## 8. Complete rational envelope for 4<=t<=23

Fix t in this interval, any integer S in 3t..17t, and put d=dbar(t,S).
For 1<=j<=S+1 define the following positive rational number:

    L_j = max(0,S-t-j+1)/j
          + sum_{a=1}^{min(t,j)} binomial(t,a)(3/4)^a
               (j-1)_(a-1) / (S+d-j+2)^(overline{a-1}). (8.1)

Here (v)_r=v(v-1)...(v-r+1), v^(overline r)=v(v+1)...(v+r-1), and both
empty products equal 1. Every denominator is positive: S+d-j+2>=d+1>0.
We claim

    z_j >= L_j b_j, 1<=j<=S+1.                         (8.2)

Divide (6.3) at degree j by b_j=q_(j-1)>0. The zero-shift contribution is
q_j/q_(j-1)>=max(0,S-t-j+1)/j by (6.2), including j=S+1 where q_j=0.
For 1<=a<=min(t,j), repeatedly invert the positive upper bounds

    q_(l+1)/q_l <= (S+d-l)/(l+1), j-a<=l<=j-2.

Their product gives
q_(j-a)/q_(j-1) >= (j-1)_(a-1)/(S+d-j+2)^(overline{a-1}).
Every such l is between 0 and S-1. Multiplying by the binomial coefficient
and (3/4)^a and adding proves (8.2). No term has been assigned the wrong sign;
dropped contributions are nonnegative.

For each epsilon and every 2<=k<M, put

    c=(N+1)/(k(N-k)),
    ell = (k+1) max(0,S-t-k+1) max(0,S-t-k+2)
             / [(k-1)(M+d-k)(M+d-k+1)],                 (8.3)

and define

    w = (k-1)(S+epsilon-k)(S+epsilon-k+1)
           / [(k+1)(S+d-k+1)(S+d-k+2)]                 (8.4)

when S+epsilon-k>0, and w=0 otherwise. All denominators used are positive.
For (8.4) the positivity condition implies S+d-k+1>0. For (8.3), k<M and
d>=t give strictly positive factors. Also 0<k<N because M<N for t>0.

When both neighbors of b are positive, use the exact identity

    r=v/u = (k+1)/(k-1)
              * lambda_Q(k-1)lambda_Q(k-2)
                   / [lambda_z(k)lambda_z(k-1)].       (8.5)

This follows by expressing b_(k+1)/b_(k-1)=q_k/q_(k-2) and
z_(k-1)/z_(k+1) in terms of their two successive rates. Applying the lower Q
and upper z bounds in (6.2) yields r>=ell. Applying upper Q and positive lower
z bounds yields 1/r>=w. If a lower z bound is zero, w=0 remains valid.

Here are all boundary cases, including those where (8.5) cannot be divided:
for k>=2, b_(k-1)>0 exactly when k<=S+2, and b_(k+1)>0 exactly when k<=S.
If both vanish, the mixed loss is zero. If only the latter vanishes, v=0,
r=0 and ell=0, and the first case of (7.2) holds as an equality in its square
factor. There is no case u=0<v. Thus no undefined birth rate outside Q's
support is used. If k+1>S+1, the second case is simply omitted.

By (8.2), u<=1/L_(k-1) when this neighbor is nonzero and v<=1/L_(k+1)
when that neighbor is nonzero. It follows from (7.1)–(7.2) that each interior
inequality for f follows from these two rationally checkable conditions:

    (max(0,1-sqrt(ell)))^2 <= c L_(k-1)  if k-1<=S+1,
    (max(0,1-sqrt(w)))^2   <= c L_(k+1)  if k+1<=S+1.    (8.6)

They are sufficient together, not a claim that both cases of (7.2) happen
simultaneously. We allow extra unnecessary checks rather than drop a case.

### Exact elimination of square roots

For rational W>=0 and R>0, (max(0,1-sqrt(W)))^2<=R is immediate when W>=1.
For 0<=W<1 it is equivalent to

    a=1+W-R <=0, OR [a>0 and a^2<=4W].                 (8.7)

This follows by expanding the square and only squaring an inequality with a
nonnegative left side. Thus (8.6) involves no floating-point decisions.
The primary checker clears all positive denominators in (8.7). The replay
checker instead uses R>=1+W or

    (1-W)^2+R^2-2R(1+W)<=0.

This is the expanded polynomial a^2-4W, with the same necessary sign split.

### Finite domain, reconstruction, and completed certificate

src/verify_envelope.py visits exactly

    t=4,...,23;
    S=3t,...,17t;
    epsilon=0,1;
    k=2,...,S+t+epsilon-1.

It uses d=min(3t,(S+2t)//5,18t-S); this is the proved bound (2.1), not an
empirical maximum of sampled mixtures. It generates (8.1) as a rational sum
and checks (8.6) using (8.7). The first summand of the sum over a is 3t/4;
successive summands obey

    term_a/term_(a-1)
       = 3(t-a+1)(j-a+1)/(4a(S+d-j+a)).                 (8.8)

The second implementation evaluates (8.1) over the common denominator
4^u product_{h=0}^{u-2}(B+h), u=min(t,j), B=S+d-j+2, using explicit binomial,
falling, and rising products. The term a numerator before adding the leading
fraction is

    binomial(t,a)3^a 4^(u-a)
       product_{v=j-a+1}^{j-1}v * product_{h=a-1}^{u-2}(B+h).

The leading fraction is incorporated with an additional denominator j.
Hence the two implementations reconstruct the SAME (8.1) by different arithmetic
paths. All canonical rational L_j hashes and all condition-domain hashes agree.

The complete finite box contains 1,322,020 interior (t,S,epsilon,k) records.
Every required nonzero-neighbor condition passed in BOTH implementations.
No mixture is left unchecked by the compression: its t,S satisfy (2.1), its
actual D is bounded by d, and all bounds (6.2), (8.2)–(8.5) have already been
proved uniformly for its ACTUAL factorization. Each coefficient index belongs
to one of the checked interior cases or one of the explicit boundaries.
The certificate is therefore universal over mixtures, not statistical evidence.

Combining (5.1), (7.1), and the complete certificate proves Delta_k(f)>=0
for every 2<=k<M, both epsilon values, and all 4<=t<=23.

## 9. An infinite tail for every t>=24

This section gives the infinite argument, not extrapolation from the finite box.
By (6.2) and S+D<=18t, Q'<=18t Q coefficientwise. Equivalently,
q_(l+1)/q_l <=18t/(l+1) for supported adjacent coefficients. From (6.3), for
1<=j<=S+1,

    z_j >= F_t(j)b_j,
    F_t(j)=sum_{a=1}^{min(t,j)} binomial(t,a)(3/4)^a
                       (j-1)_(a-1)/(18t)^(a-1).       (9.1)

This is proved exactly as (8.2), now omitting the nonnegative zero-shift term
and replacing the birth-rate upper bound by 18t. Outside b's support the
coefficient inequality holds because b_j=0.

For positive integer j, F_t(j) is nondecreasing in j. Each existing falling
product is nondecreasing, and terms newly present are nonnegative. For a fixed
term a<=t, its factor depending on t can be written

    binomial(t,a)/t^(a-1)
       = t/a! * product_{v=1}^{a-1}(1-v/t).

Every factor is nonnegative and nondecreasing as the integer t increases in
t>=a, and new terms are nonnegative. Therefore F_t(j)>=F_24(j) for t>=24.
These are proofs for every integer parameter, not checks up to a cutoff.

The exact computation in src/verify_tail.py verifies, by both direct summation
and recurrence,

    F_24(k-1)>k, 2<=k<=110.                             (9.2)

There are exactly 109 rational comparisons, recorded with full values and
margins in certificates/tail.json. To cover all remaining k, retain only the
first three nonnegative summands of F_t(j):

    Ltail_t(j)=3t/4 + (j-1)(t-1)/64
                    +(j-1)(j-2)(t-1)(t-2)/(4608t).

For t=24 and k=111+u, direct expansion gives the identity

    110592 [Ltail_24(k-1)-k]
          =3672+38954u+506u^2.                         (9.3)

All coefficients are positive and u>=0. Thus F_24(k-1)>k for all k>=111.
The source checks the exact polynomial coefficients, not evaluations at finitely
many large u. Together with (9.2), monotonicity in t, and monotonicity in j,

    F_t(k-1)>k and F_t(k+1)>k
         for every t>=24 and every k>=2.               (9.4)

For an interior index of z, (5.1) gives at least c=1/k in (7.1).
Equations (9.1) and (9.4) give 0<=u,v<=1/k, including zero neighbors. Hence

    (sqrt(u)-sqrt(v))^2 <= max(u,v) <=1/k.

Apply (7.1). This proves Delta_k(f)>=0 for every 2<=k<M and every t>=24,
for both epsilon values. Infinite t and infinite k have both been covered.

## 10. Boundary coefficients and the final conclusion

For t=1,2,3, B3 directly includes every interior coefficient of E and P. For
t>=4, Sections 8 and 9 cover every 2<=k<M. It remains to check k=1.
For either ACTUAL tree let its vertex count be v. There is one empty independent
set and v independent singletons. The only non-independent pairs are the v-1
edges, so

    f_0=1, f_1=v, f_2=binomial(v,2)-(v-1)=(v-1)(v-2)/2.

Consequently f_1^2>=f_0 f_2 for every positive integer v (indeed their difference
is (v^2+3v-2)/2>0 for v>=1). The support endpoints k=0 and k=M have zero in
the adjacent product outside the support, and further zero coefficients present
in the full 0..|V| count list preserve log-concavity.

We have now covered all positive integers t with no gap:

| t | Actual complete argument |
|---|---|
| 1,2,3 | All 37819 multisets and all interior coefficients, B3 |
| 4,...,23 | All-product block curvature + proved compression + full rational envelope |
| 24 and every larger integer | The same product structure + (9.1)–(9.4) + positive polynomial |

Thus E and P are log-concave for every permitted list of branches. To finish
without silently assuming a unimodality theorem, on their positive support
log-concavity says f_(k+1)/f_k <= f_k/f_(k-1). The successive ratios are
nonincreasing, so they can change from >=1 to <=1 at most once. Choose the
cut at that change (or an endpoint if all ratios are on one side). Coefficients
are nondecreasing before the cut and nonincreasing after it. Equal ratios of
one give allowed plateaus. Appending the remaining zero counts preserves this
property. With the graph-count identities of Section 1, this proves FAMILY-LC
and FAMILY exactly as stated. QED.

## 11. What the computation proves, and the v4 adversarial control

The finite computations used in this proof are integer/rational statements
B1–B3, (8.6) on the full derived box, and (9.2)–(9.3). They have finite,
explicitly bounded domains, and the checker contains no random step or float
comparison in those dependencies. The algorithms implement finite products,
binomial sums, integer inequalities, and proven denominator clearing. The
accompanying clean-source replay and hash comparison are evidence of execution;
they do not replace the derivations of coverage or graph semantics.

The separate src/verify_graphs.py is corroboration and direct ORIGINAL checking,
not an extra assumption in the proof. Its forest DP returns at each root the
polynomials for absent/present root states; multiplying child states follows
the independent-subset bijection of Section 1. Its second algorithm uses (1.1)
on induced subgraphs, splitting components and handling edgeless subgraphs by
binomial coefficients. Each deletion strictly decreases the number of vertices,
so the recursion terminates and (1.1) proves its correctness by induction. Masks
represent subsets of explicitly stored labeled vertices without duplication.
A third algorithm enumerates every subset once for small whole-graph controls.
The mathematical graph correspondence was already proved for all parameters.

The uploaded v4 example was read and freshly recomputed. Its 25-vertex input,
rooted at vertex 2, has split coefficients a_13=1 and q_12=4, so it fails even
a>= (1+3x/4)q at coefficient 13. After inserting the (3) branch it has 30
vertices and independent-set coefficients

    [1,30,406,3295,17975,69985,201395,437256,723946,916415,
     882241,636509,334599,121770,27779,3135,54,1].

At k=16 the LC difference is 54^2-3135=-219. For its root split, the triples
at indices 15,16,17 are a=(1935,50,1) and b=(1200,4,0), giving

    Delta(a)=565, Delta(b)=16, cross contribution=-800,
    565+16-800=-219.

The sequence is nevertheless unimodal, with its maximum at index 9. It is
neither an ORIGINAL counterexample nor a permitted FAMILY mixture. Our proof
uses quantitative (6.3), which this input does not possess. No inference from
shape-only closure or from individual nonnegative cross terms remains in the
main proof. The full edges and split counts are in certificates/graphs.json.

## 12. ORIGINAL and formalization are separate

No general forest proof follows from Section 10. An arbitrary rooted forest's
pair (I(F-v),I(F-N[v])) need not have the factored B59 representation, finite
block curvature, or (6.3). We have proved no reduction into that representation.
Also a product of arbitrary unimodal sequences need not be unimodal; no
unproved tree-to-forest step is being used.

One precise remaining SUFFICIENT extension, not assumed true, is this:
for every nonempty forest whose smaller induced forests have unimodal counts,
there exists a vertex v such that the mode intervals of I(F-v) and
x I(F-N[v]) have distance at most one. This would complete induction through
(1.1). Indeed overlapping intervals give a common peak; adjacent disjoint
intervals give two neighboring possible peaks, with the sum increasing before
these and decreasing afterwards, so the one remaining comparison cannot make
a descent followed by an ascent. We have NOT proved that such a vertex always
exists. This is the exact missing existence assertion in that possible
extension, not a premise smuggled into FAMILY. Other ORIGINAL proof routes or
an explicit unweighted counterexample remain possible.

The bounded side check used 176 stored graph records and checked the whole
count sequence plus every one-vertex-deleted and closed-neighborhood-deleted
forest, 10064 counts altogether, using two algorithms. It found no nonunimodal
forest. No completeness or novelty beyond those actual inputs is claimed.

There is no Lean theorem proving this all-parameter FAMILY statement in this
package, and no fresh transitive axiom audit. The local Lean executable was
absent, and one bounded attempt to obtain the pinned official 4.31.0 toolchain
failed at DNS resolution. More importantly, the complete new proof has not
been translated into kernel-checkable sources: in particular graph semantics,
ULC convolution, the finite certificate checker, and their final composition
are still formalization obligations. The old 14-vertex certificate and
lc_stability_nat are not substituted for these obligations. See formal/STATUS.md.
