# Global edge attempt: proved identities, missing contradiction

**ORIGINAL NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** All conclusions below have their stated premises. No theorem about arbitrary sums or products of unimodal sequences is assumed.

## 1. Recovery and dependency check
The initial live branch HEAD was 0fa61cd78b271690c60e7ec7b838b1b6fcc7aeaf. The three requested statement/proof/review/verdict chains were read at that HEAD, including the earlier compact polynomial table and relevant coverage/replay certificates. Stage 2 has its gap in proof section 9, not a separate GAP.md.

The latest edge_minimal PROOF_ATTEMPT.md states that further endpoint budgets exist, but does not give their formulas or derivations. Its compact replay receipt supplies no such derivation. We therefore do NOT import an unspecified stronger inequality as established. Section 2 supplies explicit budgets and proofs afresh. Historical archived scalar experiments are not used as current evidence.

The Stage-2 minimum-counterexample, mode-interval and polarization proofs were checked where used. The edge_compatibility proof gives the correct OR, not an AND. Edge_minimal uses the necessary lexicographic premise for F-e and smaller-order minimality for F/e. Contracting an edge of a simple forest cannot create a cycle or parallel edges: a common neighbor of its endpoints would already form a triangle. The actual contraction counted in the new source is not represented as induced deletion.

## 2. Endpoint budgets, global slack and honest telescoping
For an edge uv, the independent k-sets containing u and those containing v are disjoint. Their complement consists exactly of independent k-sets containing neither, counted by (C_uv)_k. Consequently

    (B_u)_k+(B_v)_k = P_k-(C_uv)_k.                 (2.1)

Summing complete equalities over edges gives

    sum_v d(v)(B_v)_k = m P_k - sum_e (C_e)_k.       (2.2)

The slack also counts sum_S e(F-S) over independent k-sets S. The inherited vertex count sum_v (B_v)_k=kP_k therefore gives

    sum_v (2-d(v))(B_v)_k
      = (2k-m)P_k + sum_e (C_e)_k.                  (2.3)

For an isolate-free forest the left side is the sum at leaves minus the sum of (d(v)-2)(B_v)_k at vertices of degree at least three. This is not an unweighted degree average. The coefficients and their differences depend on v; the inequality 2m<2n does not decide the sign of these weighted sums.

Now assume a real valley Delta P_i=-s<0<Delta P_j=t, i<j, and the inherited polarized splits. For selected-early v put a_v=-Delta B_v(i)>=s, b_v=-Delta B_v(j)>=0. For selected-late v put c_v=Delta B_v(i)>=0, d_v=Delta B_v(j)>=t. The subscripted d_v here is a slope, not the degree d(v).

An early B is nonincreasing throughout i..j+1. Hence B_i>=a+b, and B_(i+1),B_j>=b, by telescoping the actual coefficients and using nonnegativity at j+1. A late B is nondecreasing throughout that interval. Hence B_(i+1),B_j>=c and B_(j+1)>=c+d. Define

    L_v = a_v+b_v if early, otherwise 0;
    M_v = b_v if early, otherwise c_v;
    R_v = 0 if early, otherwise c_v+d_v.

Equation (2.1) and these lower bounds imply, for EVERY edge uv,

    L_u+L_v <= P_i,
    M_u+M_v <= min(P_(i+1),P_j),
    R_u+R_v <= P_(j+1).                             (2.4)

Summing (2.4) gives the corresponding degree-weighted bounds, with right sides multiplied by m. The all-vertex identity also gives

    sum_v L_v <= i P_i,
    sum_v M_v <= min((i+1)P_(i+1), j P_j),
    sum_v R_v <= (j+1)P_(j+1).                      (2.5)

All these bounds follow from full coefficient monotonicity, not by subtracting neighboring coefficient inequalities. Zero slopes and plateaus are allowed. They supply necessary budgets but no incompatibility theorem for every forest.

## 3. Exact double count of all edge-deletion corrections
Write W_k=sum_e (Z_e)_k. A term of Z_uv is an independent (k-2)-set S avoiding N[u] union N[v], together with the two endpoints. The set T=S union {u,v} induces exactly the edge uv. Conversely every k-set inducing exactly one edge has a unique such edge and a unique remaining S. Therefore

    W_k = #{T subset V: |T|=k and e(F[T])=1}.        (3.1)

Fix an independent r-set S instead, where r=k-2. An edge uv is admissible precisely when both endpoints lie outside N[S]. Thus

    W_(r+2) = sum_(S independent, |S|=r) e(F-N[S]).  (3.2)

Let q(S)=|V(F-N[S])| and let kappa(S) be the number of its connected components, with kappa(empty)=0. Since this residual graph is a forest, e(F-N[S])=q(S)-kappa(S). Define the actual counting statistic

    K_r = sum_(S independent, |S|=r) kappa(S).

Count pairs (S,v) with v outside N[S]. They correspond to an independent (r+1)-set with one distinguished vertex, so sum_S q(S)=(r+1)P_(r+1). This proves

    W_(r+2) = (r+1)P_(r+1) - K_r.                  (3.3)

In particular W_2=n-c=m. Here c includes every original component, including isolated vertices. No component factor has disappeared.

There is a second exact count. Among the unordered pairs of available vertices, an adjacent pair contributes to (3.2). A nonadjacent pair extends S to an independent (r+2)-set. Each such larger independent set occurs binom(r+2,2) times. Hence

    W_(r+2) = sum_S binom(q(S),2)
              - binom(r+2,2)P_(r+2).              (3.4)

Equivalently, with K(x)=sum_r K_r x^r, W(x)=x^2(P'(x)-K(x)). Equation (3.3) is an exact calculation, not an assumption that K is unimodal or has monotone differences.

### Blocked-extension budget using all edges at a support
For each vertex v put T_v=x A_v-B_v. Its k-th coefficient counts independent (k-1)-sets in F-v that have at least one neighbor of v; adding v becomes legal after deleting all edges at v. Each subset counted by an incident Z_e is one of these, and different incident edges give disjoint subsets with exactly one internal edge. Therefore

    sum_(e incident v) (Z_e)_k <= (T_v)_k.          (3.5)

Globally sum_v (T_v)_k=(n-k+1)P_(k-1)-kP_k. To identify the slack, count pairs (S,v) with S independent and v blocked. The set S union {v} induces a star plus isolated vertices. A set inducing one edge has two possible centers; a set inducing a star with at least two edges has exactly one. If Sstar_k counts the latter sets, then

    (n-k+1)P_(k-1)-kP_k = 2W_k+Sstar_k.            (3.6)

This proves the explicit coefficient budget

    0 <= W_k <= min((k-1)P_(k-1),
                    ((n-k+1)P_(k-1)-kP_k)/2),     (3.7)

for k>=2. The proof of (3.5)-(3.6) does not difference any inequalities.

### Why these sums do not finish the OR argument
In a LEX-MINIMAL valley every edge must satisfy Delta Z_e(i)>=s OR Delta Z_e(j)<=-t. Set E_L to the edges satisfying the first branch and E_R to its complement. Only the E_R edges are then required to satisfy the second branch. Contributions of E_R at i and E_L at j are not controlled by that partition.

For k>=1, (3.3), with K_(-1)=0, gives the exact difference

    Delta W_k = k P_k-(k-1)P_(k-1)-(K_(k-1)-K_(k-2)).

K_r>=0 gives no sign for its difference. Likewise (3.7) cannot be differenced as an inequality. Neither (3.3) nor (3.6) eliminates all possible E_L,E_R partitions. Introducing K or Sstar is NOT claimed to replace the old gap by a solved or smaller one.

## 4. Complete rooted products over stars and over the forest
These are polynomial identities, not two-index scalar assignments.

For a nonisolated v, delete v and let M_w=I(T_w), X_w=I(T_w-w) on each branch rooted at its neighbor w. Let R be the polynomial of other original components. Direct independent choices give

    A_v=R product_w M_w,
    B_v=x R product_w X_w,
    C_vw=R X_w product_(z != w) M_z.

Multiplying these displayed actual products, each M_z appears exactly d(v)-1 times. Thus

    x product_(w neighbor v) C_vw
      = B_v A_v^(d(v)-1).                          (4.1)

R occurs to power d(v) on both sides by construction; there is no inference about coefficients after canceling it.

A global identity follows. Suppose F is isolate-free and has c components. For each directed edge w->v let M_(w->v) count the component on the w side after cutting that edge. For one connected component, the product of all C_e contains each directed M_(w->v) exactly d(v)-1 times, the same multiplicity as in product_v A_v^(d(v)-1), if the other-component factors are temporarily written separately, not discarded.

Now fix an original component t with n_t vertices and m_t edges. On the left of the full-forest product, its whole polynomial occurs as an outside-component factor m-m_t times. In product_v A_v^(d(v)-1) it occurs 2(m-m_t)-(n-n_t) times. Because m-m_t=(n-n_t)-(c-1), multiplying by P^(c-1) makes these exponents equal. This verifies EVERY factor's multiplicity and proves

    product_e C_e = P^(c-1) product_v A_v^(d(v)-1). (4.2)

All exponents are nonnegative under the stated no-isolates hypothesis. This is checked on genuinely disconnected inputs as well as trees. Combining (4.2) with the inherited full identity C_e Z_e=B_u B_v gives

    P^(c-1) product_v A_v^(d(v)-1) product_e Z_e
      = product_v B_v^d(v).                       (4.3)

None of (4.1)-(4.3) says a product of unimodal polynomials is unimodal. Coefficients of these products involve entire convolutions, not only positions i,j.

### A checked obstruction to a ratio shortcut, not to RSM
The identity C Z=B_u B_v does NOT imply equality, or one fixed inequality direction, for adjacent coefficient-ratio products. On the actual eleven-vertex forest in the compact certificate, take edges

    0-1,0-2,0-3,1-4; 5-6,5-7,5-8,5-9,6-10.

It is the disjoint union of two trees of orders five and six. All 2047 proper induced subsets were checked in two algorithms; HEREDITARY is verified. There are no isolates or K2 components. Its U=D=4 and P is unimodal.

The cross product

    B_u[k+1] B_v[k+1] C[k] Z[k]
      - B_u[k] B_v[k] C[k+1] Z[k+1]

is -7408 at edge 0-1,k=2, and +42471 at edge 1-4,k=4. All eight coefficients are positive in both comparisons. Full polynomials, not just these numbers, are retained. This rejects only an UNLOCALIZED constant-direction ratio shortcut. Neither position pair supplies a residual valley, and no mode-restricted inequality, J_H, RSM or ORIGINAL is thereby refuted.

## 5. Potential and orientation attempt
Fix a genuine valley with positive s,t. A natural common linear functional is

    Lambda(Q)=t Delta Q_i+s Delta Q_j,
    phi_v=Lambda(B_v).

It annihilates P. Selected-early vertices have phi_v=-t a_v-s b_v<0; selected-late vertices have phi_v=t c_v+s d_v>0. The exact vertex count yields

    sum_v phi_v = t P_i+s P_j+st(j-i)>0.            (5.1)

This follows by substituting P_(i+1)=P_i-s and P_(j+1)=P_j+t into sum_v Delta B_v(k)=(k+1)P_(k+1)-kP_k.

On an edge, Lambda(C_e)=-phi_u-phi_v. For a mixed edge the first OR branch bounds t(c-a) from above by -st, whereas the second bounds s(d-b) from below by st. The other term in t(c-a)+s(d-b) remains uncontrolled. We have not derived a sign for that sum or a strict potential comparison along every edge. Choosing another common lambda is not justified by the current inequalities.

Even a strictly increasing potential along a chosen orientation of a finite tree would not alone contradict acyclicity: finite directed paths may end at sinks. A proof must rule out the terminal vertices too. No such boundary condition was obtained. Equation (5.1) is not a zero-divergence law. No abstract scalar assignment is presented as graph evidence.

## 6. Leaf/support consequences and the genuinely missing neighboring-edge step
Let l be a leaf and w its support. Keep C=I(F-{l,w}), H=I(F-N[w]). Then B_l=xC, B_w=xH, A_l=C+xH, A_w=(1+x)C and Z_lw=x B_w. Since every independent set of F-N[w] also belongs to F-{l,w},

    (B_w)_k <= (B_l)_k                             (6.1)

by a size-preserving injection, equivalently replacing selected w by l.

If l is selected-early and w selected-late at the valley, the mode interval of C ends by i-1. Thus Delta C_i<=0 and Delta C_j<=0. Substituting the inherited edge formulas gives

    a_l <= c_w+s,   d_w >= b_l+t.                   (6.2)

Telescoping early B_l and late B_w across the WHOLE interval and using (6.1) at j+1 gives

    B_l(i) >= B_l(j+1)+a_l+b_l
            >= B_w(i)+c_w+d_w+a_l+b_l.

Adding B_w(i) and applying (2.1) yields the stronger endpoint budget

    a_l+b_l+c_w+d_w+2B_w(i) <= P_i.                 (6.3)

Here i>=1, since P_1=n>=P_0 for every nonempty possible counterexample. Because the support is late, Delta Z_lw(j)=Delta B_w(j-1)>=0. The edge-deletion OR must therefore use the other branch:

    Delta B_w(i-1) >= s.                           (6.4)

If l is selected-late and w selected-early, the mode interval of C starts at or after j. Thus Delta C_i>=0 and

    a_w >= c_l+s.                                  (6.5)

No sign for Delta C_j is asserted in this case. A mode can start exactly at j; its difference at j need not be positive. This handles plateaus without choosing an arbitrary mode.

Crucially, deleting a leaf edge gives F-l together with an isolated leaf, so

    I(F-lw)=(1+x)I(F-l),  F/lw is isomorphic to F-l.

HEREDITARY already makes I(F-l) unimodal, and the read Stage-2 adjacent-mode proof shows that multiplication by 1+x preserves it. Thus leaf-edge deletion/contraction adds no independent information beyond these premises. Additional leverage would have to come from the other incident edges or the branch products (4.1), not from reusing the leaf-edge OR under a stronger label.

The incident-edge budget (3.5), star identity (4.1), and inequalities (6.2)-(6.5) were combined in the attempted route. They did not force an eligible leaf with Q>=0. Higher-neighbor-selection terms in T_w have nonnegative coefficients, but no proved difference comparison permits replacing T_w by its one-edge part. RSM remains unproved.

## 7. Actual finite discovery and verification, not closure
The fixed plan uses paired rooted-star hubs, joins of the old bad-leaf tree and branch grafts targeted at currently good vertices. It is not an extension of B59, a random-tree batch or an exhaustive graph-order claim. There are 243 admitted exact-edge-list-distinct records, maximum order 50, with every full P independently recounted. No candidate produced a valley, failed LOCAL, or reached D>=U+2. The two prescribed graft rounds chose identical best seeds; deduplication removed all repeated second-round proposals. No budget extension followed the result.

The seven controls and four selected discovery records retain every full P,A,B,C,H,Z, edge-deletion and contraction array. The small-control HEREDITARY checks enumerate all proper masks; large checks of A/B are not promoted to HEREDITARY. The inherited old23 proof remains historical evidence, not a freshly run 2^23-mask check.

Primary counting uses directed root messages with coefficient packing in base 2^(n+2). Every intermediate represented coefficient counts choices on disjoint subsets of the n input vertices and is at most 2^n, so there is no digit carry. The second algorithm uses vertex-deletion recurrence on strictly smaller masks and ordinary polynomial convolution. The independent one-edge DP tracks root selection and zero/one induced edge, and checks every W coefficient. Small direct subset counts check the component and star interpretations. Invalid forest and plateau regressions are separate from discovery counts.

The old30 control still has LC defect 54^2-3135=-219 and is unimodal. A real non-LC forest has not been relabeled a counterexample. All claimed graph material contains complete edge sets and complete zero-padded sequences. Fresh replay compares full JSON and bytes, not only hashes. None of these finite facts proves a universal inequality in the unobserved residual interval.

## 8. Where the ORIGINAL chain still stops
Assume ORIGINAL fails. Choose an order-then-edge-minimum counterexample. The checked inherited reductions give HEREDITARY, no isolated or K2 component, and a valley U<=i<j<D. The newly written results above must hold for that forest.

The next needed step is still a proof that all these real-forest conditions cannot coexist. It has NOT been supplied. Alternatively J_H would force D<=U+1, or RSM would force one leaf's Q>=0; neither assertion is proved or refuted here. The written identities have not excluded a new general portion of the original residual domain. A new name for the correction statistics would not change that fact.

Therefore the final classification is NOT_CLOSED / NO_STRUCTURAL_ADVANCE, not GAP_REDUCED and not AUXILIARY_ROUTE_REFUTED. No complete ORIGINAL Lean source or independent peer review exists for this run.
