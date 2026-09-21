# E7-CUT87: a complete one-new-vertex Hall obstruction

Run: `20260921T033413Z_round7_global_one_new`.

**ORIGINAL = NOT_CLOSED. E7-ONE-v1 is REFUTED.** The refutation concerns the complete endpoint relation, not a particular greedy operation. The witness is an actual hereditary forest at a required middle position with actual descent history. Its full independence sequence is nevertheless unimodal. No assertion restricted to an actual minimum *bad* forest is refuted.

The finite computer-assisted part is the complete induced-subforest certificate for one 64-vertex core. The source family, all-target capacity upper bound, and Hall deficiency have written proofs. No billion-edge network enumeration is needed or claimed. No novelty, external peer review, Lean build or axiom audit is claimed.

## 1. Actual objects and the fixed old ledger L7

For a finite simple undirected unweighted forest F, let p_i count its independent i-subsets, with zero padding. Positive objects are ordered independent pairs of sizes (j,j); negative objects have sizes (j-1,j+1). For each pair use

    C = I intersection J,   D = I symmetric_difference J,   U = C union D.

A group is admissible precisely when C is independent, C and D are disjoint and nonadjacent in the ORIGINAL F, and 2|C|+|D|=2j. For a component Q of F[D] with bipartition sizes a_Q,b_Q define

    O_D(z) = product_Q (z^a_Q+z^b_Q),
    A(C,D) = [z^(|D|/2)] O_D,
    B(C,D) = [z^(|D|/2-1)] O_D,
    g(D) = A(C,D)-B(C,D).

Both orientations of a balanced component are counted. Empty products equal one. The correspondence is exact: the two color classes choose which vertices belong exclusively to I and J, and each vertex of C belongs to both. Therefore

    p_j^2-p_(j-1)p_(j+1) = sum_(admissible C,D) g(D).

Order vertices by their fixed labels and sets by their binary masks. Internally cancel the first min(A,B) positive and negative objects by ordered-pair rank, once per group. This leaves demand -g for a negative group and capacity g for a positive group.

A high component has gap |a_Q-b_Q|>=2. A unit has gap one. A pair splitter is an ordered pair (v,w) where w is a leaf IN Q, v its neighbor IN Q, and every component of Q-{v,w} has gap at most one. Use the lexicographically least eligible (v,w).

L7 pays each negative group in the first applicable class below and never pays it a second time:

1. **E4 single high.** There is exactly one high component and it has a pair splitter. Send all demand to (C+{w},D-{v,w}).
2. **Phase13 only at j=4.** The residual D is Q7 plus one isolated vertex, C is empty. In Q7 let x be its degree-two middle vertex, a,b its adjacent degree-three centers, and w the least of its four pendant leaves. Send one unit to ({w,x},D-{a,b,w,x}).
3. **Unified E4/E5 odd gap-two rule.** Every high component is splittable and has gap two. A negative group has no units and an odd number t=2s+1 of highs. For each high use its least splitter and send 2^b Cat_s to its target, where b is the number of balanced components. The case t=1 was already paid in rule 1. This is one rule, not separate old-claw and generalized payments.
4. **E5 two highs.** There are exactly two highs, one of arbitrary shape and gap two, and the other of gap d>=3 with a pair splitter. Cut the latter by its least splitter and send the entire demand to the resulting group. Only negative sources are used; the gap-three case has no negative demand.
5. **E5 ordered four-unit release.** There is exactly one unsplittable gap-two high and no units. Choose the least ordered quadruple W={a<b<c<d}, with a,b in C and c,d outside U, such that W is independent, disjoint and nonadjacent to D, nonadjacent to C-{a,b}, and no original-graph vertex is adjacent to all W. Send the entire demand to (C-{a,b},D union W).

At each positive group allocate incoming negative objects to unused positive objects in rule-number, source-mask, target-mask and pair-rank order. The E4/E5 and Phase13 capacity proofs give feasibility of this fixed old ledger. Only their proved universal rules are used. E6-JOINT, its reservoir operation, the B fixed-component table, and graph-specific Q13/F35 alternative flows are NOT additional payments in L7.

For every positive target T let o(T) be the SUM of all L7 incoming payments, including every actual inverse source, and r(T)=g(T)-o(T). In particular, r is not reset to g. No automorphism-invariance of this canonical old ledger is presumed.

## 2. The complete universal candidate and what a negative cut must prove

E7-ONE-v1 asks whether, for every HEREDITARY forest and every j with

    h+1<=j<beta,   History(F,j-1),
    h=floor(M(n-1)/(4M-2))+1,
    beta=ceil(alpha(n-1)/(n+alpha)),

the following residual network pays all L7-unpaid negative groups. Here M is the largest COMPLETE component order. HEREDITARY means every proper induced subforest is unimodal. History means some earlier-or-current difference is strictly negative and all differences from it through j-1 are nonpositive.

A source (C,D) is connected to a positive target (C',D') EXACTLY when both are admissible at j and

    |(C' union D') minus (C union D)| <= 1.              (ONE)

There is no other endpoint restriction: C may increase or decrease; selected vertices may be discarded; colors may be changed; any actual unused vertex may be introduced. An operation subnetwork is not substituted for (ONE).

For any set S of unpaid negative groups, a feasible flow would require

    sum_(T in N(S)) r(T) >= sum_(s in S) -g(s).         (Hall)

We will specify S and a set R containing ALL of N(S). We then upper-bound its residual capacity by counting even more positive objects:

    sum_(T in N(S)) r(T) <= sum_(T in R) r(T)
       <= sum_(T in R) A(T).                           (2.1)

This keeps all old occupancy in the real network: o(T)>=0 only makes its capacity smaller. The last quantity is a deliberately overgenerous upper relaxation, not an exact remaining-capacity total and not a claim that old occupancy is zero. If this UPPER bound is already deficient, the full network is deficient.

Equivalently, in the standard source/sink flow network put precisely S and R on the source side of a cut. All allowed S-to-target arcs remain inside that side. Its finite capacity is at most total demand minus demand(S) plus the displayed upper bound, strictly less than total demand. We do not claim the exact minimum-cut value.

## 3. The ordinary forest F87

Define H=T_10. It has central root 0, hubs 1,22,43, and ten private paths of length two from each hub. Its edges are, for h in {1,22,43},

    (0,h),
    (h,h+1+2i), (h+1+2i,h+2+2i),  i=0,...,9.

The edge (0,h) occurs once. There are no other core edges. Append a DISJOINT star with center c=64 and 22 leaves 65,...,86. The completed forest is F87. The full edge list and whole coefficient array are in `certificates/F87_HALL_CUT.json`.

More generally the analogous core T_s has 6s+4 vertices. A hub absent permits each private edge's empty or either-singleton choices; a hub present forbids its adjacent proximal vertices. Classifying by the central root gives the actual count

    I(T_s;x) = ((1+2x)^s+x(1+x)^s)^3 + x(1+2x)^(3s).   (3.1)

Thus alpha(T_s)=3s+3. Write u=2^s+s and v=s2^(s-1)+binom(s,2). The last three coefficients in (3.1) are

    3u^2+3v+2^(3s),  3u,  1.

For s=10 they are 1076964787,3102,1. The star has polynomial (1+x)^22+x. Multiplication is justified by independent choices in COMPLETE disjoint components.

Tree DP, vertex deletion and formula (3.1) give the same whole arrays. In F87,

    n=87, alpha=55, M=64, h=22, beta=34, j=33,
    p31=197103846420707117472,
    p32=198034727289347440603,
    p33=183777727271711047953,
    p34=157309573857110318672.

The full sequence has its unique mode at 32 and no strict descent followed by a strict rise. Its only negative adjacent LC minor is at index 54. In particular 23<=33<34 and p32>p33>p34. History(F87,32) is true with first strict descent at 32; it is NOT a test with a strict descent before 32. The middle minor is

    L33=2621494482359105116011587156552543650993 > 0.

The boundary beta uses the inherited Basit--Galvin Theorem 1.3; the project prefix supplies h. For this witness the actual history and full sequence are independently counted, not inferred from those boundary theorems.

## 4. A billion genuinely unpaid negative groups

In every source fix J to consist of the star center c, all three hubs, and all thirty distal arm endpoints. Then |J|=34. It is a MAXIMAL independent set of the WHOLE F87: every vertex outside J has a neighbor in J. It is not a maximum independent set of F87, whose independence number is 55.

For each hub choose a nonempty subset A_i of its ten arms. Define I to contain c and root 0, and, on each arm, its proximal vertex if the arm is in A_i and its distal vertex otherwise. Then |I|=32 and I is independent. Let a_i=|A_i|>=1.

The intersection C consists of c and all distal vertices on unchosen arms. The symmetric difference is the connected tree T(a_1,a_2,a_3) on root 0, the three hubs, and both endpoints of the chosen arms. With a=a_1+a_2+a_3 its color classes have sizes a+1 and a+3. Hence

    O_D(z)=z^(a+1)+z^(a+3),
    [z^(a+2)]O_D=0, [z^(a+1)]O_D=1,
    g(D)=-1.                                          (4.1)

Each source therefore has exactly one negative object, no positive object and no internal cancellation. Distinct choices of the three subsets give distinct groups; J is fixed and recoverable. The number of sources is

    N=(2^10-1)^3 = 1070599167.                         (4.2)

Every one remains UNPAID under the entire L7 ledger. There is a single gap-two high and no units. All its leaves are distal arm endpoints, because each hub still has at least one arm and root 0 has degree three. Deleting a leaf and its proximal neighbor removes one vertex from each color and leaves a connected gap-two tree. It never leaves only balanced/unit components. Thus the block is unsplittable and rule 1 does not apply. Rules 2,3,4 fail their index or block-count hypotheses.

Rule 5 cannot apply either. In fact each unused core proximal vertex is adjacent to a common distal vertex, and each unused star leaf is adjacent to common center c. Thus EVERY unused vertex has a neighbor in C. The release requires its fresh vertices to be nonadjacent to D and C minus the two demoted common vertices, and also nonadjacent to those demoted vertices because W must be independent. It would require no neighbor in C union D at all, impossible here. This is stronger than just testing one proposed quadruple.

The source check is independent of all canonical tie-breaking. The exact old payment to S is zero. There are no competing graph-specific alternative payments in this ledger.

For a compact certificate, sort 1<=a_1<=a_2<=a_3<=10. These give 220 parameter orbits, each weighted by

    (3!/product multiplicity_of_equal_a!) product_i binom(10,a_i).

The weights sum to (4.2). Each representative's original C,D, independence, color sizes, lack of splitter and unused-to-C adjacency are checked in `F87_SOURCE_ORBITS.csv`. The theorem accounts for all labeled choices by the displayed binomial counting; 220 is not the number of actual sources. No positive orbit-flow lifting is needed for this negative cut.

## 5. An upper bound that includes EVERY permitted target

No source in S uses a star leaf. Consequently, under (ONE), the union of a permitted target can contain at most ONE star leaf. This remains true even if it completely changes C, removes center c, changes all core choices, or uses an arbitrary endpoint operation.

Let R be ALL admissible positive groups whose union contains at most one star leaf. It contains every permitted target for S. To bound sum A(T), count all ordered independent pairs of sizes (33,33) with at most one star leaf. Grant arbitrary core independent sets, even when they introduce more than one new core vertex relative to a source. Also grant all positive objects that internal cancellation or the old ledger actually used. This only increases the upper bound in (2.1).

Put a=p33(H)=1 and b=p32(H)=3102.

If no star leaf is used, each of the two star selections is empty or {c}. The count is

    a^2+2ab+b^2=(a+b)^2=9628609.

For a specified star leaf z, used at least once, the five possible star pair states are

    ({z},{z}), ({z},empty), (empty,{z}), ({z},{c}), ({c},{z}).

Their contributions are respectively b^2,ba,ab,b^2,b^2. These retain the original incompatibility of z and c inside either independent set; no graph edge is removed. There are 22 choices of z, each used by a disjoint class. Therefore

    U=(a+b)^2+22(3b^2+2ab)
     =9628609+22*28873416
     =644843761.                                      (5.1)

A second coefficient calculation in the verifier uses the two-variable polynomial

    (1+x)(1+y)+22(x+y+3xy)

for these star-pair states, multiplied by I_H(x)I_H(y), and obtains exactly (5.1). This is a superset count, NOT the actual remaining capacity of R. In particular no reverse old source has been ignored in order to increase the real remaining capacity; the proof is valid for every nonnegative old occupancy simultaneously.

## 6. Complete-relation Hall failure

Combining (2.1), (4.2) and (5.1),

    sum_(T in N(S)) r(T) <= 644843761
        < 1070599167 = sum_(s in S) -g(s).

The certified deficiency is at least

    1070599167-644843761 = 425755406.                   (6.1)

Thus E7-ONE-v1 is false on this actual graph, with ALL of its hereditary, middle and history premises (HEREDITARY is established below). It is not merely a failure of source-local reachability, a frozen-C rule, a C-growing path or a small operational subnetwork. All allowed target groups were included by the necessary star-leaf restriction, and the counted upper relaxation gave them more rather than less capacity.

This also rules out any FULL injection from all negative (32,34) pairs to positive (33,33) pairs obeying one-new-vertex permission, independently of L7: restricting such an injection to S would contradict the same count. It does not rule out an unrestricted injection, and it does not make F87 nonunimodal. It only proves that some source must receive an image using at least two new union vertices.

### 6.1 Adding E6-JOINT first does not remove this cut

This is a SEPARATE residual-ledger corollary, not a change to E7-ONE-v1. Start with L7 and then the final 011858Z E6-JOINT-v2 universal payments, each source only once. Every source in S still has every unused vertex adjacent to C. E6 point replacement requires a fresh vertex nonadjacent to C and so is unavailable. E6 bulk release requires every fresh vertex to be nonadjacent both to retained common vertices and to demoted common vertices (the latter belong to its independent W); it too is impossible. The several-high rule does not apply to a single high. Hence no E6 universal rule pays S. Its additional target occupancies can only decrease the left side of (2.1), so the same deficient cut remains. Graph-specific alternatives are still excluded. This does not infer a full one-new arrangement from a mixed ledger containing multiple-new-vertex old payments.

## 7. Complete HEREDITARY certificate for the 64-vertex core

The certificate does not infer HEREDITARY from the 2n local deletions and does not test a random set of induced subgraphs. It covers every one of the 2^64 core vertex subsets using the following exact decomposition.

### 7.1 Each branch state and the omitted components

When a hub is present in an induced vertex set, let a count its arms with BOTH endpoints present and l count its arms with only the proximal endpoint present. Then a,l>=0, a+l<=10. The hub's connected branch component has polynomial

    P_(a,l)=(1+x)^l(1+2x)^a + x(1+x)^a,
    A_(a,l)=(1+x)^l(1+2x)^a.                           (7.1)

The second polynomial counts choices when that hub is forbidden. Distal-only endpoints are isolated components and are NOT silently deleted from the whole induced polynomial: their factors (1+x) remain separately. When a hub is absent, each arm contributes an isolated edge, isolated vertex or empty graph. These omitted factors are all LC.

There are 66 pairs (a,l). Every P_(a,l) is counted by (7.1) and by independent vertex deletion on its explicit graph; all 66 are LC. A present-hub state represents exactly

    binom(10,a) binom(10-a,l) 2^(10-a-l)

endpoint subsets. The factor two distinguishes distal-only from empty in every remaining arm, although they have the same central connected component. Those different omitted isolated factors are handled by the LC-times-unimodal lemma, not equated to one another. A missing hub is an additional state of weight 4^10, P=A=1.

### 7.2 Root present

With the root present, take an unordered triple of these 67 states. There are

    binom(69,3)=52394

triples. For the component containing root 0, its exact polynomial is

    product_i P_i + x product_i A_i.                   (7.2)

Each representative graph is reconstructed and counted separately by vertex deletion with connected-component factorization. All 1,141,296 coefficient entries of these 52,394 arrays agree with (7.2), and all arrays are unimodal. There are 103 non-LC arrays; they are retained rather than excluded.

Multiply the three state weights by 1,3 or 6 according to equalities among the three states. The sum is

    (2*4^10)^3=2^63=9223372036854775808.

This counts every labeled subset with the root present once. The factors outside the root component are only K1/K2 and therefore LC. Their product with the unimodal root-component polynomial is unimodal by Section 8.

### 7.3 Root absent

There are another 2^63 subsets with the root absent. Every nontrivial branch component is one of the 66 LC graphs in (7.1); all remaining components are K1/K2. Repeated application of the LC-times-unimodal lemma gives unimodality of the whole induced forest. The absent-root cases require no assumption that products of arbitrary unimodal polynomials are unimodal.

Thus all 2^64 vertex subsets, including the whole core and the empty subset, are covered. This is complete combinatorial compression with exact weights, not 2^64 independent DP executions. The independently generated CSV contains every one of the 52,394 central cases, not only the exceptional cases.

### 7.4 Independent replay categories

`hereditary_core.cpp` uses checked integer coefficients and 128-bit products. It computes (7.1),(7.2) and separately counts the actual graph by vertex deletion for EVERY representative. It outputs both classification tables and their complete totals. `verify_cut.py` then independently checks the entire central table using Python arbitrary-precision integers: all index triples occur exactly once, all weights and formula coefficients match, and every recorded unimodality/LC flag is recomputed.

These are two graph/formula algorithms with an additional full-table audit, not outside peer review. Their deterministic outputs and source hashes are supplied; the proof of coverage is the preceding decomposition.

## 8. The elementary convolution facts needed for HEREDITARY

### 8.1 LC times unimodal is unimodal

Let a be a nonnegative log-concave sequence with positive interval support 0,...,d; let b be nonnegative unimodal with positive interval support 0,...,e. Zero-pad both. Let m be the last mode of b, D_t=b_t-b_(t-1), including D_0 and D_(e+1). Then D_t>=0 for t<=m and D_t<=0 for t>m. For c=a*b write

    f_k=c_k-c_(k-1)=sum_t D_t a_(k-t).

For k<=m, all nonzero terms have nonnegative D_t, hence f_k>=0. For k>=m+d+1, all active D_t are nonpositive, hence f_k<=0. In the middle put q=k-m, 0<=q<=d, and lambda=a_(q+1)/a_q>=0, with a_(d+1)=0.

For t<=m, i=k-t>=q; decreasing LC ratios give a_(i+1)<=lambda a_i, including right-support zeros. For t>m, i<=q-1 and a_(i+1)>=lambda a_i. This last inequality also holds at i=-1 because a_0>=0=lambda a_-1, and at i<=-2 by zero padding. Multiplying by the corresponding signs of D_t and summing yields

    f_(k+1)<=lambda f_k.

Consequently after the first negative f, no later positive f can occur, including through zeros. Together with the initial and terminal signs this proves c unimodal. Constant and empty-polynomial graph cases are included.

In particular one can multiply a unimodal central polynomial by any number of LC factors. To know that a product of LC factors is LC one may use the standard 2x2 Toeplitz-minor argument, but that stronger assertion is not necessary for the repeated LC-times-unimodal applications here.

### 8.2 Every induced subgraph of a star is LC

An induced subgraph omitting the center is edgeless and has a binomial polynomial. When the center is present and t leaves remain, its polynomial is (1+x)^t+x. Its first two relevant LC minors are

    L1=(t^2+5t+2)/2,
    L2=t(t-1)(t^2-t+4)/12.

They are nonnegative, with support-end cases interpreted directly for t=0,1. At indices >=3 the tested coefficients are those of (1+x)^t and satisfy the binomial LC inequality. Thus every induced star is LC. K1 and K2 have linear positive polynomials and are LC as well.

### 8.3 Applying these facts to F87

Every induced subforest of F87 is the disjoint union of an induced H64, proved unimodal in Section 7, and an induced star, proved LC above. Their actual polynomials multiply. Section 8.1 proves every such sequence unimodal. In particular HEREDITARY(F87) is established with no external component-order theorem and no presumption of ORIGINAL.

## 9. What allowing two new vertices really repairs

The deficiency is not an impossibility of all exterior changes. For the ENTIRE source set S, fix star leaves z1=65,z2=66 and define

    K=(I-{c}) union {z1,z2},
    (I,J) -> (K,K).                                   (9.1)

K is independent in the ORIGINAL F87 and has size 31+2=33. Exactly two vertices of its union were absent from the source union. The image recovers I by deleting these two fixed leaves and restoring c; J is fixed. Thus (9.1) is a simultaneous injection for ALL 1,070,599,167 sources, not an existence claim for individual sources.

Every image group has C'=K,D'=empty and surplus one. Its internal negative count is zero. Every output of the L7 rules has nonempty D': a pair splitter leaves at least two vertices of a high component; the multi/two-high rules retain components; Phase13 leaves four units; release enlarges D. Consequently ALL old inverse-source sets at these diagonal targets are empty and o(T)=0 exactly. This is not a scan of a selected subset of inverse centers.

The new targets are distinct and do not consume any old target capacity. Since (ONE) cannot pay S while (9.1) can, the least uniform new-vertex allowance for this source SET is exactly two.

This does NOT prove a two-new matching for every negative group of F87, much less for arbitrary forests. It is the scoped repair of the complete-relation counterexample set, not a substitute for the still missing global connection. The F35 full one-new matching and this F87 two-new source repair are different graphs and different arrangements and are never added together.

## 10. An unbounded version of the capacity obstruction, with its precise boundary

The counting obstruction itself is not special to s=10. In T_s disjoint-union K_(1,2s+2), take j=3s+3 and the same family of nonempty subsets of the s arms at each hub. Its unpaid demand is (2^s-1)^3. The same COMPLETE target relaxation has capacity

    U_s=(54s+63)(2^s+s)^2+(12s+18)(2^s+s)+1.

For every integer s>=10, (2^s-1)^3>U_s. Here is an all-parameter proof. Put q=2^s. Induction gives s/q<=1/64 and 13s+19+1/q<=q. Therefore

    U_s <= (56s+66)q^2+(13s+19)q+1 <= (56s+67)q^2.

Also (q-1)^3 >= (31q/32)^3 > (9/10)q^3. At s=10, (9/10)q>56s+67, and doubling its left side preserves this inequality when s increases by one. This proves the strict deficiency for all s>=10. The comparison coefficients follow directly from (65/64)^2(54s+63)<=56s+66 and (65/64)(12s+18)<=13s+19.

The whole-graph numerical boundaries also satisfy h+1<=j<beta throughout this region: alpha=5s+5,n=8s+7,M=6s+4, and

    alpha(n-1)-j(n+alpha)=(s-6)(s+1)>0,
    (j-1)(4M-2)-M(n-1)=24s^2+22s+4>0.

HEREDITARY and History for EVERY s>=10 are NOT claimed here. The complete full-premise refutation uses s=10, for which they are proved and recounted above. The all-s result is a separate structural capacity theorem and cannot upgrade the finite hereditary classification to unbounded coverage. The two-new map (9.1) works for this specified source family whenever two star leaves exist.

## 11. The inherited complete F35 certificate was actually audited

Before using the Round6 baseline, this run obtained the original 011858Z ZIP bytes, read its full final proof/review/gap/claims, and checked the source manifest and final captured-run receipt. It did NOT substitute the remote 0144Z EXIT draft for E6-JOINT-v2. The original complete source/flow/target CSV files have respectively 11,702,637; 31,599,830; and 13,586,217 bytes. The original unchanged independent C++ auditor was compiled and rerun in this task.

It checked every one of 399,155 source orbits, every one of 340,754 used target orbits, all operation witnesses, source/target weights, all old inverse-source candidates and the conservation equations. Its 918-byte output matches the inherited audit hash. The checked totals are

    represented source groups           7746986152,
    super-demand and paid flow         21337568904,
    used target total capacity        529230632968,
    old occupancy ENVELOPE                339424416,
    conservative remaining capacity   507553639648.

The envelope is an UPPER reservation, not exact actual old payments. There were 11,926,390 inverse-vertex scan iterations, namely 35 for each used target representative, not that many new graphs. Whole F35 coefficient arrays were also freshly compared by two graph algorithms.

The lifting proof was read and checked: the source classifier and occupancy envelope, not necessarily the canonical old matching, are invariant under the stated automorphism group. An orbit of an ACTUAL legal endpoint edge is biregular. A quotient flow can be spread over its edge orbit to give feasible fractional actual-group marginals. Integer-demand/capacity flow integrality then gives an integer actual-group matching. This is not an unsupported inference from an orbit total.

The two old schedules remain distinct:

* Preserve old two-new release, then remove super-demand assignments of already-paid sources. This proves a one-new RESIDUAL flow, not that every old edge used one new vertex.
* Retire old two-new release and let the ENTIRE super-demand flow take over its sources while retaining the old target reservation. This gives the FULL F35 one-new matching.

They are alternatives, never simultaneous payments. This run reran the unchanged certificate AUDITOR, not the old optimizer or the whole E5 history. F35 being positive does not contradict the complete-relation negative F87 cut.

## 12. What remains of ORIGINAL

E7-CUT87 refutes the universal HEREDITARY/middle/History ONE-new sufficient route. It does not settle a version limited to ACTUAL vertex-minimal original counterexamples. F87 has no valley and has an LC star component, so one cannot assign it that stronger bad/minimal premise.

The two-new repair pays S and leaves other F87 source sets unaddressed. No global two-new Hall bound or arbitrary-exterior injection is proved. The weaker no-rebound inequality

    L_j >= p_j(p_j-p_(j-1))

also remains unproved for arbitrary forests at all necessary history positions. No numerical right-hand side has been renamed as an unconstructed object reserve.

The research consequence is to stop treating a universal one-new endpoint bound under HEREDITARY/History as a theorem to be proved. A valid continuation must use additional actual-minimum-bad information, or a wider permission with a proved collective capacity bound, or a genuinely structural signed no-rebound estimate. No new forest-order interval is claimed excluded from ORIGINAL merely by this auxiliary refutation.

## Sources and attribution

The exact original task and Round7 coordination notes were read from Project Files. E4/E5 final universal rules and Phase13 at j=4 are retained with their existing hypotheses; R6 011858Z final source and audit tables are separate from the remote 0144Z interface. H64/T_s is an inherited tree construction; novelty of that construction or its non-LC tail is not claimed. The new theorem here is the full one-new endpoint Hall obstruction with an actual fully certified premise instance and the stated source-set repair.

Basit and Galvin, *On the independent set sequence of a tree*, arXiv:2006.12562v2, Theorem 1.3, supplies only the inherited tail boundary. Its official HTML was read in this task. It is not used to replace any Project proof or to certify current global solution status. The elementary LC-times-unimodal argument needed here is proved in Section 8.
