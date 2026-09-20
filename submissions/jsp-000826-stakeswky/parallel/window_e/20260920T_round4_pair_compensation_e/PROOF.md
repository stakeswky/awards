# E4-S: uniform signed-sector compensation

ORIGINAL NOT_CLOSED. This is a scoped theorem for every finite simple undirected unweighted forest and every coefficient index, with a complete finite computer-assisted base in one scalar lemma. No variance estimate or unproved peer claim is used. No novelty or external peer-review claim is made.

## 1. Exact objects and theorem

Let p_j count independent j-sets of the actual forest F, zero outside support. Positive objects are ordered independent pairs of sizes (j,j); negative objects have sizes (j-1,j+1). Write C=I intersect J, D=I symmetric_difference J. An admissible group has C independent, C disjoint D, no C-D edges in F, and 2|C|+|D|=2j. For each component Q of F[D], write a_Q,b_Q for its bipartition sizes. Then

    O_D(z)=product_Q(z^a_Q+z^b_Q),
    g(D)=[z^(|D|/2)]O_D-[z^(|D|/2-1)]O_D

is its exact signed count. Balanced components retain their two orientations. Empty products equal one and coefficients outside support equal zero. In particular

    L_j=p_j^2-p_(j-1)p_(j+1)
       =sum_(D even) g(D) p_(j-|D|/2)(F-N_F[D]).              (1)

Thus all intersections and all original-graph exterior constraints remain present; weights in (1) are actual independent-set counts.

A component's gap is |a_Q-b_Q|. Gaps zero and one are called balanced and unit. A high component has gap at least two. A high component Q is splittable if a leaf w IN Q, with neighbor v, satisfies: every component of Q-{v,w} has gap at most one. Choose the lexicographically first eligible (v,w). Outside neighbors of w in F are not discarded.

Let S_j be the signed sum over the UNION, counting overlap once, of these group classes:

(A) every high component is a four-vertex claw K_(1,3);
(B) there is exactly one high component, and it is splittable.

Arbitrary balanced/unit components are allowed in both classes.

**E4-S: S_j>=0 for every F and j>=0.** Graph size, index, number of claws, branch depths and outside attachments are unrestricted. Stars K_(1,d+1), d>=2, are special cases of splittable components. Non-star components of arbitrary depth can also qualify. The theorem does not assert S_j=L_j.

## 2. One-high-component formula, including zero support

With b balanced components, q units and one high component of gap d>=2, the orientation polynomial, up to a monomial, is 2^b(1+z)^q(1+z^d). Even |D| requires q+d=2m. Its negative excess is 2^b B(d,q), where

    B=max(0,binom(q,m-1)+binom(q,m+1)-2binom(q,m)).            (2)

All out-of-support binomial coefficients are zero. The signed defect before the factor 2^b is zero if d>q+2; it is -1 if d=q+2; otherwise d<=q and, putting t=(q-d)/2, it equals

    binom(q,t)(q+2-d^2)/((t+1)(q-t+1)).                      (3)

These follow by expanding the two coefficients and using adjacent binomial ratios. The first case has both tested coefficients zero; the boundary case has central coefficient zero and adjacent coefficient one. Consequently B>0 implies

    d-1<=m<=(d^2+d-4)/2.                                    (4)

## 3. All-parameter capacity lemma

Put Cat_m=binom(2m,m)/(m+1). For every d>=2,q>=0,d+q=2m,

    (2m-1)B(d,q)<=(d-1)Cat_m.                               (CAP)

The zero-B case is immediate. For d=2,...,10, (4) leaves exactly 165 integer pairs. The supplied standard-library source enumerates this COMPLETE domain, computes each B both by polynomial multiplication and two binomial forms, and verifies the integer inequality. The maxima of (2m-1)B/((d-1)Cat_m), by d=2,...,10, are respectively

    1, 3/4, 1/3, 1/6, 11/130, 5/114,
    209/9135, 39/3256, 9367/1491498.

All 165 rows are generated in the exact replay output. This is a complete finite base, not graph sampling.

For every d>=11, binom(2m-d,m+1)<=binom(2m-d,m-1), so B<=2binom(2m-d,m-1). At d=2 the ratio of this latter binomial to binom(2m,m) is m/(2(2m-1)). Each increment of d multiplies it by (m-d+1)/(2m-d)<=1/2 while in support; outside support it is zero. Therefore

    (2m-1)B/Cat_m <= m(m+1)/2^(d-2).

By (4), 4m(m+1)<=f(d)=(d^2+d-4)(d^2+d-2). For d>=11, f(d)<=(d-1)2^d: the base is 16640<=20480, and at d=x+11,

    2f(d)-f(d+1)=x^4+42x^3+643x^2+4218x+9872>0.

The right-hand bound grows by 2d/(d-1)>2, so induction proves it for all d>=11. This establishes CAP on the entire infinite remaining domain.

It follows that whenever t>=d and t-d is even, with N=q+t,

    B(d,q)<=Cat_(N/2)(t-1)/(N-1).                            (5)

Indeed CAP gives the t=d case; Catalan numbers are nondecreasing and (t-1)/(q+t-1) is nondecreasing for q>=0. N>=2, so no zero denominator is introduced.

## 4. Single splittable high block: actual targets and incoming multiplicity

For a negative group in class B, use its canonical splitter and set

    C'=C union {w}, D'=D minus {v,w}.                         (6)

This is admissible in the ORIGINAL graph: w had no neighbor in C; its only neighbor inside its D-component was v; and there were no edges to other D-components. The index is preserved because 2|C'|+|D'|=2j. The graph itself is unchanged.

Suppose Q-{v,w} has t unit and b0 balanced components. The contributions of adjacent v,w to the side difference cancel. Balanced branches contribute zero, units contribute +1 or -1. Thus t>=d and t-d is even. If the other original D-components supplied q units and b balanced components, the target has N=q+t units, b'=b+b0 balanced components and no high component. Its exact surplus is 2^b' Cat_(N/2). By (5), incoming excess from this source is at most

    2^b B(d,q)<=2^b' Cat_(N/2)(t-1)/(N-1).                  (7)

Sources sharing this target are NOT assumed unique. Fix the actual (C',D'). A possible deleted center v lies outside C' union D' and has exactly one neighbor w in C'; the old C had no neighbor in v. In a forest, v meets each D'-component at most once, or there would be a cycle through its internal path. Hence v determines w, Q (all D'-components it meets plus v,w), and the entire source. The canonical rule can only remove candidates.

Contract every unit component of F[D'] and retain all possible source centers and only their edges to the contracted unit components. The result is an actual forest. If there are N unit vertices and center v meets t_v of them, its edge bound gives

    sum_v(t_v-1)<=N-1.                                     (8)

Every counted t_v>=2. Balanced components may be discarded in this incidence graph; no favorable sign is assumed about their original objects. Summing (7) and using (8) proves that the TOTAL incoming negative excess fits the target's positive surplus. This is a graph-derived multiplicity bound, not a choice of arbitrary weights.

## 5. Arbitrarily many claws, without reusing capacity

In class A, up to a monomial and factor 2^b, O_D=(1+z^2)^t(1+z)^q. Here q is even. If q>=2 its central defect is nonnegative. Indeed (1+z^2)^t(1+z)^2 has coefficients binom(t+1,l) at 2l and 2binom(t,l) at 2l+1; adjacent ratios prove symmetry and weak increase to the midpoint. Products of symmetric unimodal sequences are symmetric unimodal: decompose each into a nonnegative sum of centered interval indicators and count convolutions of intervals. This covers the remaining (1+z)^(q-2) factor.

If q=0,t even the defect is 2^b binom(t,t/2)>=0. If q=0,t=2s+1 it is -2^b binom(2s+1,s). The t=1 case was already paid in Section 4 and is not counted again.

For t>=3, normalize EACH of its t claws using its center and smallest leaf by (6). Each target has 2s remaining claws and two singleton units, and its surplus is

    2^b[binom(2s,s)-binom(2s,s-1)]=2^b Cat_s.

The t target surpluses sum to the source's deficit because t Cat_s=binom(2s+1,s).

Targets from distinct source groups or claw choices cannot collide. The two singleton units must share the deleted center; two vertices of a forest have at most one common neighbor. That center's unique neighbor in C' recovers the promoted leaf and thus the source. All eligibility conditions are checked after recovery.

These targets still contain at least two claws, whereas Section 4 targets have no high component. The two collections of spent positive capacities are disjoint.

## 6. An explicit matching, rather than existence of some balanced pair

Order independent sets by binary vertex mask and ordered pairs lexicographically. Within each group match the first min(positive count,negative count) objects by rank. This leaves exactly -g(D) excess negative objects or g(D) unused positive objects.

For class B, route leftover negative objects to (6). At each target order all incoming objects by source center and pair rank, and map them to its unused positive objects in rank order. Sections 4's inequalities prove enough capacity. For negative class-A groups with at least three claws, concatenate the unused positive objects of their t targets in center order and match by rank; the cardinalities are equal and each target has only one source. The two target domains are disjoint.

Every image belongs to an admissible actual group and is an independent (j,j) pair. The maps are finite explicitly defined injections; no efficient running-time claim is needed. This proves E4-S for all forests and all indices.

## 7. Connection and exact remaining gap

Use the project's already established complete-graph prefix h=floor(M(n-1)/(4M-2))+1 and tail beta=ceil(alpha(n-1)/(n+alpha)). A first rise after an earlier strict descent has h+1<=j<beta and p_(j-1)>=p_j<p_(j+1), so L_j<0. Minimality supplies HEREDITARY (every proper induced subforest unimodal), but HEREDITARY was not needed in E4-S.

Let R_j sum ALL groups outside the compensated sector, retaining signs and actual exterior counts. Then L_j=S_j+R_j, S_j>=0. A first rebound must therefore have an outside negative group: an unsplittable high component, or several high components with at least one not a four-vertex claw.

The first unproved bound is R_j>=-S_j at every necessary middle/history position. Positive capacity already spent above may not be spent again. No general forest range has been newly eliminated merely by restating this necessary restriction. Unrestricted middle LC and ORIGINAL remain NOT_CLOSED.

## 8. Remaining obstruction in an unbounded middle/history/HEREDITARY family

Let Q be the 13-vertex spider with four length-three arms. Its sides have sizes 5,8 and polynomial (1,13,66,168,227,160,58,12,1). No leaf-neighbor deletion is a splitter: it removes one vertex from each color and leaves a connected gap-three component.

For every r>=33 take F_r=Q disjoint_union rP_3, j=r+11. Then n=3r+13,alpha=2r+8,M=13. The inequalities

    alpha(n-1)-j(n+alpha)=r^2-28r-135>0,
    13(3r+12)<50(r+10)

give h+1<=j<beta. Let D contain Q and one P_3 leaf, and C contain r+4 other P_3 leaves. They form an admissible group, with O_D=(z^5+z^8)(1+z) and g(D)=-1. Every leaf-neighbor normalization inside Q still has g=-1; a positive target is not obtained.

Write A_r=(1+3x+x^2)^r. Its coefficients strictly decrease after r. In P_Q A_r, the four indices j-2 through j+1 remain strictly after r under every shift 0..8 and within support, so p_(j-2)>p_(j-1)>p_j>p_(j+1). This is actual earlier descent, not an arbitrary chosen position.

Every induced subforest of Q is LC, verified by complete dual counts of all 8192 vertex subsets. Induced subgraphs of P_3 are LC. The convolution argument below proves every induced subforest of F_r LC for every r. Thus HEREDITARY holds, but these graphs are NOT minimum bad forests or original counterexamples: the whole sequence is LC.

## 9. Naive iteration overloads a target, including in the middle

Let H have edges 01,02,03,34,45,46,67,68. At j=3 the two groups (C={2},D={3,4,5,6}) and (C={},D={0,2,3,4,5,6}) each have negative excess one. Repeatedly choosing the lexicographically first leaf-neighbor pair (v,w) in a high component and applying (6) until the first positive target sends both to (C'={2,3},D'={5,6}). Their paths are (4,3) and (0,2),(4,3). The target D' is an edge, with surplus one. The incoming load two exceeds capacity one.

For every r>=30, append rP_3, add the same r+6 P_3 leaves to C in sources and target, and take j=r+9. Here n=3r+9,alpha=2r+6,M=9, and

    alpha(n-1)-j(n+alpha)=r^2-26r-87>0,
    9(3r+8)<34(r+8).

The positions are in the required middle and, since alpha(H)=6, the same shifted-tail argument supplies strict descent. Complete dual counts of all 512 induced H-subsets and convolution prove HEREDITARY for every r. At r=30: n=99,h=26,beta=40,j=39.

This refutes only the specified naive iterative routing rule, not all possible routing and not ORIGINAL. It does not contradict the canonical SPLITTING-LEAF rule and its multiplicity proof above.

## 10. Convolution fact used for the obstruction families

For completeness, a nonnegative interval-supported LC sequence a has nonnegative 2-by-2 minors in its Toeplitz matrix T(a)_(r,c)=a_(c-r): decreasing consecutive ratios show that the product of two middle coefficients dominates that of the two outer coefficients of equal index sum; zero endpoints cause no negative minor. Conversely the adjacent Toeplitz minor is a_k^2-a_(k-1)a_(k+1).

T(a*b)=T(a)T(b). Expanding any 2-by-2 minor and pairing opposite orders of intermediate indices gives the 2-by-2 Cauchy-Binet sum of products of nonnegative minors, so convolution preserves LC. Each sum is finite by finite supports.

For strictness, at index k choose l in the positive support of a with k-l in that of b. The intermediate adjacent indices l,l+1 contribute the positive term L_l(a)L_(k-l)(b), using zero-padded endpoint minors as well; all other terms are nonnegative. Since (1,3,1) has strictly positive adjacent minors, its r-fold convolution is strictly LC. Symmetry about the integer midpoint r then gives strict decrease after r. This justifies the all-r history assertions, not merely the finite representative checks.
