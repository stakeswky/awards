# Phase 6: minimal component blocks and terminal-spider elimination

**ORIGINAL: NOT_CLOSED. Core elimination: NO_STRUCTURAL_ADVANCE.**
**Small-component normal form: SCOPED_DOMAIN_REDUCTION, conditional on the pinned external census and H2/H3 computation.**

This document proves the scoped propositions below, including a finite, computer-assisted HEREDITARY certificate for one actual 64-vertex tree. It does not prove that a minimum counterexample cannot exist. The first substantive missing elimination is stated in Sections 7 and 10. Same-model review is not independent peer review. No originality or priority is claimed for the classical convolution argument, the bush-tree construction, or the independently derived formulas.

## 1. Original statement, support and minimality

A graph here is finite, simple, undirected and unweighted. For a forest F let

    P(F;x) = sum_{k=0}^{|V(F)|} i_k(F) x^k,

where i_k counts independent vertex subsets of size k. Empty forests, isolated vertices and disconnected forests are included. Set coefficients outside this range to zero. A sequence is unimodal when it is nondecreasing up to a mode and nonincreasing thereafter; peak plateaus are allowed. With Delta p_k = p_{k+1}-p_k, non-unimodality is equivalent to the existence of i<j with Delta p_i<0<Delta p_j. A plateau between these strict signs is not an exception. Trailing zero padding cannot create a later positive difference, so checking through the last nonzero coefficient is equivalent.

Every independence sequence has interval support: taking subsets of a maximum independent set proves positivity at every size from 0 to the independence number. The empty forest has polynomial 1. All coefficients used in computations are exact nonnegative integers.

If ORIGINAL is false, well-ordering gives a forest F with non-unimodal P of least vertex count n, and, among these, least edge count m. Every forest of fewer than n vertices is unimodal, and every forest with n vertices and fewer than m edges is unimodal. In particular:

* HEREDITARY: every proper induced subforest of F is unimodal;
* every nonempty edge deletion F-S is unimodal, by the additional edge minimality;
* no connectedness assumption follows.

For each vertex v write A_v=P(F-v), B_v=xP(F-N[v]). Partitioning independent sets by whether they contain v proves P=A_v+B_v. Both are unimodal under HEREDITARY. Write their full mode intervals as [ell_Av,r_Av] and [ell_Bv,r_Bv], and define

    U = max_v min(r_Av,r_Bv),
    D = min_v max(ell_Av,ell_Bv).

For k<U, at least one vertex decomposition has both differences nonnegative, so Delta P_k>=0. For k>=D, at least one has both differences nonpositive, so Delta P_k<=0. If D<=U+1 there is at most one uncontrolled difference, hence P is unimodal. A true valley in a minimum counterexample must therefore satisfy U<=i<j<D and D>=U+2. The converse is not asserted: a residual position pair is not necessarily a valley. These are inherited reductions, not Phase-6 progress.

## 2. A self-contained convolution lemma and a legal deletion rule

A finite nonnegative sequence p with interval support is log-concave (LC) if p_k^2>=p_{k-1}p_{k+1} for every k. It is unimodal because successive positive ratios p_{k+1}/p_k are nonincreasing.

**Lemma 2.1 (LC times unimodal).** If p is LC with interval support and q is finite, nonnegative and unimodal, then p*q is unimodal.

Proof. Extend sequences by zero to all integer indices. For k<l and a<b, LC gives

    p_{k-a} p_{l-b} >= p_{l-a} p_{k-b}.                 (2.1)

If the right-hand product is positive, its two indices are the outer endpoints of the four indices. The two left-hand indices lie between them and have the same sum. Decreasing successive ratios imply that moving the outer indices inward cannot decrease the product. All intermediate terms are in the support. If the right-hand product is zero, (2.1) follows from nonnegativity.

Put d_j=q_j-q_{j-1}. All strictly positive d_j precede all strictly negative d_j, since q is unimodal, including its leading and trailing zero extensions. Define

    A_k = sum_{a:d_a>0} d_a p_{k-a},
    B_k = sum_{b:d_b<0} (-d_b) p_{k-b}.

The difference (p*q)_k-(p*q)_{k-1} is A_k-B_k. Multiplying (2.1) by d_a(-d_b) and summing gives A_k B_l >= A_l B_k for k<l. If the difference at k were negative and a later difference at l positive, then A_k<B_k and A_l>B_l, forcing A_k B_l < A_l B_k, a contradiction. This also handles zero terms and plateaus. Thus p*q is unimodal. QED.

This is the sufficient direction of classical discrete strong unimodality (Keilson--Gerber, 1971). The elementary proof is supplied rather than treating an unproved general product-unimodality assertion as an input.

For a disjoint union F=A disjoint-union B, independent subsets are uniquely pairs of independent subsets in the two parts. Therefore P(F)=P(A)P(B).

**Proposition 2.2 (LC-block deletion).** Let A be a nonempty proper union of connected components of a non-unimodal forest F. If P(A) is LC, then B=F-V(A) is a strictly vertex-smaller non-unimodal forest.

Indeed, if B were unimodal, Lemma 2.1 would make F unimodal. This is a genuine elimination rule: it produces a smaller bad forest, not merely a smaller good forest. The valley indices of B need not be those of F; the conclusion concerns its complete sequence.

**Corollary 2.3.** Every nonempty proper component block of a minimum counterexample is non-LC. The entire forest is also non-LC, since LC implies unimodal. This statement concerns arbitrary component blocks, not only individual components or only small components.

A path on l vertices has polynomial

    a_l(x) = sum_k binom(l-k+1,k) x^k,     a_0=1.

Choosing k nonadjacent path positions and subtracting 0,1,...,k-1 from their ordered labels is a bijection with k-subsets of an (l-k+1)-set. Its positive consecutive coefficient ratio is

    ((l-2k+1)(l-2k))/((k+1)(l-k+1)).

Both factors (l-2k+1)/(l-k+1) and (l-2k)/(k+1) are nonincreasing over the applicable nonnegative range. Thus a_l is LC. No path component can occur in a minimum counterexample: remove it by Proposition 2.2 if other components remain; if it is the entire forest, it is already unimodal. This includes isolated vertices and K2.

The two-term polynomial 1+cx for c>0 is LC. Consequently multiplying any unimodal polynomial by any number of factors 1+x or 1+2x preserves unimodality. This observation will remove only detached isolated vertices and edges in Section 6; no product of arbitrary unimodal factors is assumed unimodal.

## 3. Conditional small-component normal form: at most two, at most 247 index cases

External input is pinned to scinet-ai/math-number-theory at commit
fafb35784d4235c9e5dd701fd3b2c1f4955ae9ec. The prior component-30 audit is retained. Its input states:

1. Every tree of order <=30 is unimodal, and exactly 149 such tree types are non-LC (2 of order 26, 19 of order 28, 7 of order 29, 121 of order 30).
2. In this ordered bank S, H2 is the set of non-LC unordered pair multisets. All 11,175 pair products are unimodal and |H2|=97.
3. Among all triples whose every two-element deletion belongs to H2, none has a non-LC product: H3 is empty. Repetitions are allowed. The published program checks 10,823 extensions of H2, of which 111 meet the hereditary-pair condition; all 111 are LC.
4. The previously audited finite-basis argument excludes every forest whose components all have order <=30.

The large tree census and complete H2/H3 computation were NOT rerun in this task. Three banked tree sequences and two H2 products were freshly recounted from their actual graphs by two algorithms. This does not establish census completeness or freshly certify all of H2/H3. Source and index definitions were read; selected inputs and exact blob identities are in sources/selected_external_trees.json and INPUTS.md.

**Theorem 3.1 (conditional).** A minimum counterexample has at least one component of order >=31, at most two components of order <=30, and its small-component multiset is one of

    empty; a singleton from S; a pair from H2.

Proof. At least one large component follows from input 4. Each small component is a nonempty proper block, so Corollary 2.3 makes its polynomial non-LC and input 1 places it in S. Every small pair is also a proper block, so a pair must be in H2. If three small components existed, their union would still be proper because a large component remains. This triple is non-LC by Corollary 2.3 and all its pair deletions belong to H2; it would belong to H3, contradicting input 3. QED.

There are at most 1+149+97=247 small index multisets. This is not a count of distinct polynomials, whole forests, boundary profiles, or all remaining cases. It neither bounds the number of large components nor their order or shape. Mixed small/large proper blocks must also be non-LC, but no finite classification of those blocks is established.

A further conditional consequence is that a disconnected minimum counterexample has at least 57 vertices: it needs a large component (>=31) and every other component has order >=26. The connected case is still possible from order 31. These lower bounds are not a complete finite search or a minimum-counterexample discovery.

## 4. Why the same block criterion cannot bound the number of large components

For k>=1 let H_k have a central vertex joined to three hubs, each hub carrying k disjoint pendant paths of length two. It has 6k+4 vertices. Define

    s_k=(1+2x)^k+x(1+x)^k,
    p_k=P(H_k)=s_k^3+x(1+2x)^(3k).

The formula partitions on the central vertex; each hub is absent or present. All factors count actual unweighted choices.

Put d=3k+3, a=2^k+k, b=k*2^(k-1)+binom(k,2). The three top coefficients of p_k are

    (p_k)_d=1,
    (p_k)_(d-1)=3a,
    (p_k)_(d-2)=2^(3k)+3a^2+3b.

For the r-fold disjoint union, write c_j=[x^j]p_k^r. Its top LC minor is

    c_(rd-1)^2-c_(rd-2)c_(rd)
       = r * (((9r+3)/2)*a^2 - 2^(3k) - 3b).          (4.1)

It follows by selecting one or two factors that contribute below their top degree. Since a<=2^(k+1), the right-hand side is negative whenever 2^k>18r+6. For any requested r>=1 choose an integer k with 2^k>=32(r+1). Then (4.1) is negative for every 1<=j<=r in place of r.

**Proposition 4.1.** For every r there exists an actual forest of r components, each larger than 30 vertices, such that every nonempty component block is non-LC.

The construction is r identical copies of H_k above. Every block is some p_k^j, and k>=6 ensures each component has >=40 vertices. This is a uniform proof, not an extrapolation from a fixed sample size.

This proposition shows only that the block non-LC criterion and a lower component-order bound cannot by themselves give a bound on the number of large components. It does NOT assert HEREDITARY or non-unimodality of this unbounded family, and does not disprove any statement that uses all minimum-counterexample premises. The bush construction is a familiar non-LC-tree type; no global novelty is claimed. Fourteen finite parameter checks, including complete all-vertex recounts, verify the formula and have no valleys. They are arithmetic controls, not added all-forest coverage.

## 5. A structure that must occur in every remaining minimum counterexample

A branching vertex has degree at least three. A terminal-spider center v is a branching vertex such that all but at most one of the components reached through its neighbors are pendant paths ending in leaves. In particular v has at least two such arms; the possible exceptional branch is the true exterior, not a discarded variable.

**Lemma 5.1.** Every non-path finite tree has a terminal-spider center.

Proof. If it has one branching vertex, all branches at that vertex are paths ending in leaves. Otherwise root the tree at a branching vertex and choose a branching vertex farthest from that root. No descendant branch contains another branching vertex, by maximality. Each descendant branch is a path ending in a leaf. The only possible non-path direction goes toward the root, and there are at least two descendant arms because the selected vertex has degree >=3. QED.

Every component of a minimum counterexample is non-LC and hence not a path, so Lemma 5.1 applies to each large component (and to every small component as well). This proves a mandatory structure for the complete remaining domain. It does not prove that this structure is reducible. Its number of arms, arm lengths and exterior size are unbounded.

## 6. A HEREDITARY counterexample to a tempting terminal-center shortcut

Consider H_10 from Section 4. Give the central vertex label 0 and its hubs labels 1,2,3. For hub h=1,2,3 and t=0,...,9 put m=4+20(h-1)+2t and add edges (h,m),(m,m+1), in addition to (0,h). This gives 64 vertices and 63 edges, a finite simple unweighted tree.

Full exact sequences show:

    P(H_10) is unimodal, with U=20 and D=21;
    at each terminal center h=1,2,3:
        A_h has its unique mode at 21,
        B_h has its unique mode at 19.

These are all its terminal-spider centers. At vertex 0 every direction contains another branching vertex, so vertex 0 is not terminal. The top LC minor of P is -1,067,342,383, so P is non-LC but remains unimodal. The full graph, full P, all A/B polynomials (losslessly pooled), all modes and all vertex labels are in certificates/NATIVE_CERTIFICATE.json; the unpooled witness is reproducible from src/check_hereditary64.py.

It is essential to check HEREDITARY rather than infer it from these vertex polynomials. The following is a COMPLETE finite compression of arbitrary induced subsets of this one graph.

For an arbitrary selected vertex subset, examine each hub's ten arms. If that hub is retained, let a be the number of arms retaining both middle and far vertices, and b the number retaining the middle vertex only. Then a,b>=0 and a+b<=10. Arms retaining only the far vertex contribute isolated vertices. The hub with its retained attached arms has

    X_(a,b)=(1+x)^b (1+2x)^a        (hub absent),
    Y_(a,b)=x(1+x)^a                (hub present),
    M_(a,b)=X_(a,b)+Y_(a,b).

If a hub is deleted, each of its ten arms contributes only an isolated vertex, an isolated edge, or nothing. Thus all components omitted from this reduction have factors 1+x or 1+2x, not arbitrary unimodal factors.

There are sum_{a=0}^{10}(11-a)=66 attached-hub types. At most three hubs are retained. They are interchangeable under actual graph automorphisms, so reduced types are multisets of size 0,1,2,3, numbering respectively

    1, 66, 2211, 50116; total 52394.

For each multiset Q there are two reduced polynomials:

    root absent: product_{t in Q} M_t;
    root present in the induced vertex set:
        product_{t in Q} M_t + x product_{t in Q} X_t.  (6.1)

Here 'root present' means the central vertex belongs to the induced graph; its independent-set membership is still summed over by the two terms. This is not conditioning on selecting the root into an independent set.

These formulas cover EVERY subset of the original 64 vertices: deleted and retained hubs, every arm-retention pattern, and both central-vertex states were exhausted in the classification. Conversely each reduced type is realizable; the detached factors contain all ignored selected vertices. The finite program checks all 104,788 reduced polynomials in (6.1), not just connected ones. Every one is unimodal. Multiplication by the omitted isolated-vertex/edge factors preserves unimodality by Lemma 2.1. Hence every induced subforest, including every proper one, is unimodal: HEREDITARY is proved for H_10.

For arithmetic verification, every compressed product is computed both by nested convolution and by carry-free integer packing. For the latter, choose a base 2^w larger than the product of the two coefficient sums; this strictly exceeds every convolution coefficient, so integer multiplication cannot carry into the next coefficient. Each attached-hub type is independently recounted from an actual graph. The whole H_10 and all 128 A/B polynomials are also checked by a different vertex-deletion recurrence, not only by the hub formula. As a semantic regression, every one of the 1024 induced subsets of H_1 is checked by literal independent-subset enumeration against the reduction mapping and both graph algorithms.

This refutes the stronger assertion that every HEREDITARY, non-LC, non-path forest must have a terminal-spider center whose A/B mode gap is at most one. It does not refute an assertion restricted to actual non-unimodal minimum counterexamples: H_10 has no valley and D-U=1. In particular it refutes neither J_H nor RSM nor ORIGINAL. The arithmetic certificate is for this fixed 64-vertex tree, not every forest of order <=64 and not all H_k.

## 7. Direct elimination with the real exterior: exact identity, missing sign step

After the shortcut fails, retain the actual exterior. Let v be a terminal-spider center with pendant arm lengths l_1,...,l_t. Remove v and all arm vertices to obtain G, retaining every other original component. If v has an exterior neighbor w, put M=P(G), N=P(G-w); if it has no exterior neighbor, put N=M=P(G). With a_l=P(path_l), b_l=a_(l-1), direct counting gives

    P(F)=M product_j a_(l_j) + xN product_j b_(l_j).    (7.1)

In particular these are the actual A_v and B_v, with all exterior factors intact. Fix one arm of length l and put

    E=M product_{j != chosen} a_(l_j),
    L=xN product_{j != chosen} b_(l_j).

Then the original, arm-deleted and first-edge-cut forests have polynomials

    original P = a_l E + b_l L,
    arm-deleted R = E+L,
    edge-cut P_cut = a_l(E+L),
    Q = P_cut-P = (a_l-b_l)L.                         (7.2)

All are actual forests. The arm-deleted forest has fewer vertices; the edge cut has the same vertices and fewer edges. Also a_l-b_l=x a_(l-2) for l>=2, and equals x for l=1, by the path-endpoint recurrence. Thus Q is coefficientwise nonnegative. This says nothing about the sign of its adjacent differences.

Fix a hypothetical true valley Delta P_i=-s<0 and Delta P_j=t>0 of a lex-minimum counterexample. To retain this same pair after the cut, one would need

    Delta Q_i < s  and  Delta Q_j > -t.               (7.3)

Conversely lex-minimality forces Delta Q_i>=s OR Delta Q_j<=-t for every such cut. A valley in a different position after an operation would also suffice, but requires an independent complete-sequence argument. Proving R or P_cut unimodal does not establish an elimination: that is already required by minimality. Coefficientwise Q>=0 does not supply (7.3); differencing destroys that order.

**Unproved elimination claim.** From the actual minimum-counterexample premises and a mandatory terminal-spider structure, construct an operation yielding a vertex-smaller non-unimodal forest, a lex-smaller non-unimodal forest, or a contradiction to those premises, for every possible arm multiset and actual exterior (including all other components and all internal vertex conditions).

No such universal operation or contradiction is established. The failure is at mandatory structure -> reducibility, not at the existence of the terminal structure or at exact graph counting. This is a specialization of the earlier all-shared-cut residual incompatibility, not a proof that the old first gap has been reduced.

## 8. One fixed directed round after the auxiliary failure

The native source uses nine specified seeds targeting the missing step: H_10, asymmetric hub counts, larger exterior hubs, path-core variants, four-hub variants, a two-large-component forest, a large component with the selected H2 pair, and two large components with one small banked tree. Each seed is expanded once at a specified terminal center and arm by arm deletion, leaf deletion, arm extension, first-edge cut, or moving the arm to the true exterior neighbor. Exterior components are never discarded. Repeated graph/marked-position/operation expansions are forbidden, and exact forest canonical encodings identify repeated isomorphism types.

The completed round has 54 proposals and 54 distinct forest types within this run, 45 distinct marked operations, maximum order 167. Twenty-four are disconnected and twelve have at least two components of order >=31. Every whole P and every A/B polynomial is independently recounted: 54 whole sequences and 10,164 vertex-conditional arrays. The exact terminal formulas are checked at 246 actual centers. All complete sequences, including modified-graph valleys, are tested. Three HEREDITARY labels follow from the H_10 certificate and two proper induced deletions; the other 51 remain UNKNOWN.

All 54 are unimodal and LOCAL, with maximum D-U=1. Actual residual graphs, residual pairs, eligible nonvacuous RSM tests and original counterexamples are all zero. These are finite diagnostic findings, not proof of absence in the remaining domain. The 14 separate coefficient-identity controls from Section 4 are not disjoint new coverage and are not added to this count. No finite UNSAT or universal finite-state compression was attempted.

## 9. What is preserved and what is not claimed

The Phase-5 exact defect partition, shared multi-edge identities and lossless root/vertex boundary profiles remain valid with their original premises. Their universal residual incompatibility remains unproved. The separate component-30 theorem retains its pinned external dependency. The B59 FAMILY proof is unchanged and was not freshly replayed or formally extended.

No ORIGINAL Lean proof, fresh top-level Lean build, transitive axiom audit, external peer review, prize eligibility or global novelty is established. No actual original counterexample was found, so shrinking and global minimality of such a counterexample were not performed. A local failure of an auxiliary lemma is not an original counterexample.

## 10. Complete-chain audit and exact stopping point

Established chain:

    ORIGINAL false
      -> lexicographically minimum bad forest
      -> every proper component block non-LC
      -> conditional small part in 247 index cases, at least one large component
      -> every component non-path
      -> terminal-spider structure in every large component
      -> exact whole-forest identities with the real exterior.

**Missing arrow:** these identities and all minimum-counterexample premises -> a legal elimination or a contradiction for every remaining exterior and arm configuration.

Without this arrow there is no complete coverage proof and no implication back to ORIGINAL. The old remaining domain contained actual minimum-counterexample residual configurations with at least one >=31 component. The newly excluded configurations are those having an LC proper component block, in particular (conditionally) three or more small components or a small singleton/pair outside the bank/H2. The remaining domain still includes a single large tree and forests with arbitrarily many large non-LC components plus zero, one or two permitted small components, subject to all inherited minimality conditions. It is not a finite list.

Final classification: **ORIGINAL NOT_CLOSED; SCOPED_DOMAIN_REDUCTION for the conditional component normal form; NO_STRUCTURAL_ADVANCE on the core residual elimination.**
