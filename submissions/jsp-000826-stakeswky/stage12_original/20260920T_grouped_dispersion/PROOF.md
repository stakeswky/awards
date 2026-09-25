# Grouped dispersion is not a universal forest inequality

**ORIGINAL: NOT_CLOSED. Exact BARRIER: UNRESOLVED.**
**Selected-branch-count grouped sufficient bound: REFUTED, including on a connected tree.**
**Separate scoped theorem: an explicit alternating decorated-path family is log-concave for every length.**

This is a continuation of the user-facing Phase-10 separator proof, especially its equations (4.1)--(4.4). That artifact is distinct from the concurrent repository Phase-10 arbitrary-core proof. At recovery the actual remote HEAD was `b7e76b0737428c08e549ffd2b274122d67772b1a`, whose state records a global third-minor result. Those remote files are not reset or replaced. No novelty or external-review claim is made here.

## 1. Target and the two different inequalities

For a finite simple undirected unweighted forest F let p_k be the number of independent k-sets. Empty and disconnected forests are included. The positive support is 0,...,alpha, since subsets of a maximum independent set realize every smaller size. ORIGINAL forbids a negative adjacent difference followed later by a positive one; zeros and peak plateaus are allowed.

The external Basit--Galvin Theorem 1.3 supplies weak decrease from

    beta = ceil(alpha(n-1)/(n+alpha)).

It is used only to specify the inherited middle domain and the implication back to ORIGINAL. Neither the counterexample arithmetic nor the family log-concavity proof below depends on an external tree census.

Let C be ALL vertices of degree at least three. For each independent S subset C put

    q_S(x) = x^|S| I(F[V \ (C union N(S))]; x).

Here N(S) is the actual open neighborhood in F. The remaining graph is a disjoint union of paths, so q_S is log-concave (LC), including its initial shift. The partition by selected branch vertices is exact: P_F=sum_S q_S. It retains the entire forest, not only a chosen local core.

At k, write a_s=q_s[k], b_s=q_s[k+1], c_s=q_s[k+2]. For active states a_s>0, set

    pi_s=a_s/p_k, r_s=b_s/a_s, u=sum pi_s r_s,
    V=sum pi_s(r_s-u)^2,
    K=sum pi_s(r_s^2-c_s/a_s) >= 0.

For the states with a_s=0 retain birth masses

    B=sum b_s/p_k, Z=sum c_s/p_k.

Then R=p_(k+1)/p_k=u+B, and

    p_(k+2)/p_k=u^2+V-K+Z.

Consequently the EXACT no-rebound inequality is

    V+Z <= K+u+B-u^2.                                    (E)

Its exact slack is

    S_k := K+u+B-u^2-V-Z = (p_(k+1)-p_(k+2))/p_k.          (1)

On the premise R<=1 and k+1<beta, proving (E) for every forest would propagate weak decrease to the known tail, including across plateaus, and would imply ORIGINAL. This universal implication remains unproved.

The Phase-10 SUFFICIENT bound is different. Group active states by g=|S|. Write W_g for group mass, u_g for its conditional mean, and l_g,h_g for its minimum and maximum ratio. Define

    Vhat = sum_g W_g[(h_g-u_g)(u_g-l_g)+(u_g-u)^2].

The proposed stronger certificate is

    Vhat+Z <= K+u+B-u^2.                                 (G)

The inequality V<=Vhat is always valid; (G) is not. The examples below refute (G), not (E). They do not refute a statement whose additional premise is that F is an actual non-unimodal minimum counterexample.

## 2. Exact identification of the grouping error

For any group with a real variable r in [l,h] and mean m,

    (h-m)(m-l)-Var(r) = E[(h-r)(r-l)].

This follows by expanding both sides as (h+l)m-hl-E[r^2]. The law of total variance, including the between-group contribution, therefore gives

    Vhat = V + E_group,
    E_group = sum_s pi_s(h_g-r_s)(r_s-l_g) >= 0.           (2)

Substituting (1) proves

    grouped certificate slack = S_k - E_group.            (3)

This identity holds with the birth masses present. Thus (G) requires that a nonnegative overestimate error be no larger than the next actual decrease. Merely establishing a variance upper bound does not establish this extra requirement. This also explains why many successful small tests need not extend to larger cores.

## 3. First explicit counterexample: a 638-vertex forest

Let A be the four-vertex claw (one center and three leaves), and B the seven-vertex subdivided claw (one center and three private two-edge paths). Their polynomials are

    a(x)=(1+x)^3+x = (1,4,3,1),
    b(x)=(1+2x)^3+x(1+x)^3 = (1,7,15,11,1).

Take 58 disjoint copies of each. This forest has n=638, alpha=406, beta=248. Its branch-vertex set consists of the 116 centers. At k=206 the whole coefficients satisfy p_206>p_207>p_208.

For i selected A centers and j selected B centers, the exact multiplicity and sector are

    m_(i,j)=binom(58,i)binom(58,j),
    q_(i,j)=m_(i,j) x^(i+j)
               (1+x)^(3(58-i+j)) (1+2x)^(3(58-j)).       (4)

All raw states in a count class have the same full polynomial and ratio. Multiplicity is retained, so collapsing such classes preserves V, K, group endpoints, and every group weight. The 3481 count classes cover all 2^116 raw states. This is a proved compression for this family, not an arbitrary-core finite-state claim.

The certificate proves, using outward rational intervals,

    0.014695949545 <= E_group <= 0.014695952794,
    0.01299733 < S_206 < 0.01299734.

All displayed terminating decimals denote exact rationals. Thus E_group>S_206 and (G) fails. Both component polynomials are LC; moreover every induced subgraph of each of the two small component trees is LC, as certified by complete literal checks of their 16+128 induced subsets. LC convolution closure then proves HEREDITARY for this 638-vertex forest without any external census. It is NOT an original counterexample.

This example alone refutes a universal all-forest (G), but the next section removes any reliance on disconnectedness or small whole components.

## 4. A connected 1122-vertex counterexample to (G)

### 4.1 Actual graph and exact state compression

For r>=1 define F_r as follows. Start with a path on 2r vertices, alternating types A and B, beginning with A and ending with B. Attach three new leaves to each A root; attach three disjoint new two-edge paths to each B root. No other edges are added. It is a finite simple unweighted connected tree, with

    n=11r, |E|=11r-1, alpha=7r.

For the upper independence bound, delete all backbone edges: the components have maximum independent-set sizes 3 and 4. The bound is attained in F_r by choosing all A leaves, all B roots, and all far B leaves. All B roots are mutually nonadjacent.

Its branch-vertex set C is exactly the 2r backbone vertices. Fix i selected A roots and j selected B roots. The only remaining restrictions among the roots are independence on the backbone path. Their number m_r(i,j) can be computed by a two-state recurrence:

    absent_new = absent_old + present_old,
    present_new = activity_of_this_type * absent_old.

The initial pair is (1,0). Keeping two formal type variables gives every coefficient m_r(i,j), with no graph-state omission. Equivalently,

    m_r(i,j)=binom(r-i,j)binom(r-j,i)  for i+j<=r,          (5)

and zero otherwise. One proof of (5) verifies the two-vertex transfer recurrence using Pascal's identity; an independent alternating-path DP also verifies each multiplicity in the native certificate. The proof and compression do not require (5): the two-state polynomial recurrence alone supplies exact multiplicities.

Every such choice has the same remainder polynomial, so

    P_r(x)=sum_(i+j<=r) m_r(i,j) x^(i+j)
                (1+x)^(3(r-i+j)) (1+2x)^(3(r-j)).        (6)

This retains every backbone compatibility and every attached vertex. It is not a construction from arbitrary weighted arrays.

For r=102, there are 204 branch vertices and 5356 (i,j) classes. They cover exactly

    5034645418285014325766435419644478339818233

actual independent backbone selections, the Fibonacci number F_206. The group g in (G) is still i+j, NOT the finer (i,j) class. Compressing identical-ratio states does not change the proposed inequality.

### 4.2 Strict violation in the actual middle interval

For F_102 the exact integers give

    n=1122, alpha=714, beta=436, k=363,
    p_363>p_364>p_365,
    U=D=363.

In particular k+1=364<436, so this is a genuine middle weak-descent premise. There is no U/D residual pair, and no actual valley. The ratios, for interpretation only, are approximately 0.9993074655 and 0.9925890946. The full positive-support sequence has 715 coefficients; every coefficient is retained in CONNECTED_WITNESS.json and independently recomputed.

The following RATIONAL statements are certified:

    7692939575 / 10^12 <= E_group <= 7692944726 / 10^12,
    740577 / 10^8 < S_363 < 740578 / 10^8.

Hence E_group>0.0076929 whereas S_363<0.0074058. Thus

    grouped slack = S_363-E_group < -0.0002871 < 0.

This is a strict counterexample to the universal grouped sufficient inequality on a connected tree. Birth masses B=Z=0 here because all sector supports already contain the three tested indices. The implementation verifies this; it does not impose zero births in general.

The decisive computation does not add thousands of floating-point fractions. Each nonnegative term in (2) is bounded below and above by adjacent multiples of 10^-12 using integer division. All individual bounds are then summed. The rational interval remains strictly on the wrong side of (G). A second direct calculation of K, Vhat and u, with outward intervals, independently certifies a negative upper bound for the original (G) slack.

For each compressed class, all three required coefficients are computed twice. Method one differentiates H=(1+x)^L(1+2x)^M to obtain

 (t+1)h_(t+1)=(L+2M-3t)h_t+2(L+M-t+1)h_(t-1),
 h_(-1)=0, h_0=1.

Method two uses the direct binomial convolution sum

    h_t=sum_v binom(L,t-v)binom(M,v)2^v.

Every division is exact and all entries match. The COMPLETE P is separately recounted from the actual graph by rooted DP and by vertex deletion/component splitting, and matches the transfer recurrence in the next section. All 1122 vertices' A/B mode data are computed. The 24 full A/B arrays at 12 material vertices are additionally independently recounted. HEREDITARY for this connected tree remains UNKNOWN; it is not inferred from LOCAL or whole-tree LC.

## 5. Continuing the exact route: the entire F_r family is LC

After refuting (G), we do not infer anything adverse about ORIGINAL. Instead the exact structure supplies a complete all-parameter result, including for the example above.

**Theorem. For every integer r>=1, P_r is log-concave with positive interval support. In particular F_r is unimodal. Any finite disjoint union of arbitrary F_r trees is LC as well.**

### 5.1 Derive a genuine two-root transfer recurrence

Put L=(1+x)^3 and M=(1+2x)^3. The A-root absent/present polynomials are L,x; the B-root polynomials are M,xL. Keeping the state of the last B root, one complete pair has transfer matrix

    [[M(L+x), ML],
     [xL^2,   xL^2]].

Its trace and determinant are

    T=M(L+x)+xL^2
      =1+11x+45x^2+90x^3+94x^4+51x^5+14x^6+x^7,
    D=x^2 M L^2
      =x^2+12x^3+63x^4+190x^5+363x^6+456x^7
          +377x^8+198x^9+60x^10+8x^11.

The initial vector is (1,0), so P_0=1 and P_1=T. The matrix's characteristic identity yields

    P_r=T P_(r-1)-D P_(r-2) for r>=2.                    (7)

This is a recurrence for the whole actual tree, not a recurrence assuming that sums or differences preserve LC.

### 5.2 Exact factorization for every r

The monic polynomials f_0(z)=1, f_1(z)=z,
f_r(z)=z f_(r-1)(z)-f_(r-2)(z) satisfy

    f_r(2 cos theta)=sin((r+1)theta)/sin(theta).

This follows by the sine addition identity and induction. Thus f_r has the r distinct roots 2cos(j*pi/(r+1)), j=1,...,r. Pairing opposite roots and homogenizing the polynomial identity gives

 P_r = T^(r mod 2) product_(j=1)^floor(r/2)
         [T^2 - c_j D],
 c_j=4 cos^2(j*pi/(r+1)) in [0,4].                       (8)

The identity is polynomial in T,D; no division by a potentially zero polynomial is used. It remains to prove LC for T and every real-parameter factor R_c=T^2-cD, 0<=c<=4.

### 5.3 A finite coefficient proof valid for all real c in [0,4]

Let A_i=[x^i]T^2, B_i=[x^i]D, inserting zeros. Every coefficient of R_c is at least its coefficient at c=4, and

 R_4=(1,22,207,1122,3941,9510,16258,19996,17790,
      11406,5173,1584,298,28,1),

which is strictly positive. For each internal index i, the LC minor is a quadratic

    f_i(c)=q0_i+q1_i c+q2_i c^2,
    q0_i=A_i^2-A_(i-1)A_(i+1),
    q1_i=-2A_iB_i+A_(i-1)B_(i+1)+B_(i-1)A_(i+1),
    q2_i=B_i^2-B_(i-1)B_(i+1).

Writing t=c/4 in [0,1], we have the exact identity

 f_i(4t)=b0_i(1-t)^2+2b1_i t(1-t)+b2_i t^2,
 (b0_i,b1_i,b2_i)=(q0_i,q0_i+2q1_i,q0_i+4q1_i+16q2_i).

All the coefficients are positive, as the COMPLETE table shows:

| i | b0 | b1 | b2 |
|---|---:|---:|---:|
|1|273|275|277|
|2|18781|18465|18165|
|3|484177|462989|443097|
|4|5565349|5199793|4861261|
|5|31214870|28685248|26367322|
|6|89552700|81495620|74160604|
|7|134344820|121908828|110610196|
|8|106252444|96916356|88409724|
|9|44331130|41067476|38069166|
|10|9588601|9124585|8692825|
|11|998382|982430|967502|
|12|43556|44004|44452|
|13|486|486|486|

Since the three basis terms are nonnegative and not all zero, f_i(c)>0 for EVERY c in the interval. T itself has the six positive internal minors [76, 1035, 3870, 4246, 1285, 145], so it too is LC. This is finite symbolic coefficient arithmetic with a proof of the real-parameter compression, not sampling values of c or r.

### 5.4 Convolution closure finishes the theorem

For a nonnegative LC sequence with interval support, decreasing adjacent ratios give nonnegative 2-by-2 minors of its Toeplitz matrix. The Toeplitz matrix of a convolution is a product of these matrices. The 2-by-2 Cauchy--Binet expansion proves LC closure; the sums relevant to a fixed index are finite. Interval support of the product follows from positivity. This recalls the classical convolution argument without assuming arbitrary unimodal convolution closure.

Apply this closure to all the factors in (8), and to T when r is odd. Every finite r is covered; r=0 is the identity polynomial. This proves the theorem and the disjoint-union corollary. In particular the failure of (G) above happens on an LC sequence, not merely on a sequence not yet classified. Arbitrary extra attachments or arbitrary non-LC disjoint factors do not follow from this theorem.

## 6. What remains for the actual general inequality

Equation (E), with all births and real exterior compatibility retained, is still the desired general sufficient no-rebound step. The false inference was replacing V by Vhat and treating the resulting stronger estimate as a universal structural law.

In these examples, grouping by the TWO type counts (i,j) instead of their sum makes each group constant-ratio and eliminates E_group. That repairs the estimate for these constructed sectors; it is not a proof of (E) for arbitrary graphs, where group curvature, means and newly appearing states remain coupled. Refining all the way to singleton states simply recovers (E), not a new proof of it.

The transfer/factorization argument is a genuine solution for a whole unbounded family after the auxiliary failure. Its repeated two-type backbone is a substantive hypothesis. No proof extends its factorization to arbitrary cores, arbitrary uncovered external branches, or arbitrary non-LC large components. The general first missing connection remains actual forest compatibility -> the exact no-rebound bound (E), or another legal minimum-counterexample elimination. The existing J_H/RSM and external-census restrictions are unchanged.

Final status: GROUPED_BOUND_REFUTED; SCOPED_ALL_LENGTH_LC_THEOREM; ORIGINAL_NOT_CLOSED; GENERAL_CORE_NO_STRUCTURAL_ADVANCE. The number of probe graphs is not used as a substitute for this status. No global minimality, full order census, fresh Lean build, transitive axiom audit, independent peer review, or prize claim is made.
