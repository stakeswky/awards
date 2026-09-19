# Phase 8: position-aware log-concavity and the missing middle

**ORIGINAL: NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** The unrestricted prefix
claim is neither proved nor refuted. All statements below distinguish a
written uniform argument, a failed auxiliary shortcut, and finite checking.
No global novelty or independent peer-review claim is made.

## 1. Target, support, and the two tail boundaries

Let F be a finite simple undirected unweighted forest, with n vertices. Let
p_k count independent k-vertex subsets, let alpha be their largest possible
size, and put P(x)=sum_(k=0)^alpha p_k x^k. All p_0,...,p_alpha are positive:
subsets of a maximum independent set realize every smaller size. Empty and
disconnected forests are allowed. Coefficients outside the support are zero.

ORIGINAL asks whether every such P is unimodal, allowing plateaus. Equivalently
there is no pair i<j with Delta p_i=p_(i+1)-p_i<0<Delta p_j. Appended zero
coefficients do not create a later rise. All computational valley tests scan
the COMPLETE support, not only the ranking window.

We use two external decreasing-tail theorems, not new results of this run:

    b0   = ceil((2 alpha-1)/3),
    beta = ceil(alpha(n-1)/(n+alpha)).

For the empty graph set b0=beta=0. The Levit--Mandrescu theorem applies to
Konig--Egervary graphs, hence forests, and gives weak decrease from b0.
Basit--Galvin Theorem 1.3 gives weak decrease from beta for ANY graph. Its
proof uses the Fisher--Ryan and Zykov inequalities, not an assumption that
all independence polynomials are log-concave. Theorem 1.3 and that proof were
read in the primary paper. See SOURCES.md. We do not prove its ingredients
anew or apply only a random-tree/asymptotic version.

Forests are bipartite, so alpha>=n/2. For n>0 this implies beta<=b0 (the
unrounded inequality is equivalent to (alpha-1)(2 alpha-n)>=0). Thus the
sharper bound can only shorten the range where a later increase is possible.
A true valley necessarily has j<beta, without any minimality or HEREDITARY
premise. Values of beta and b0 are always computed from the actual complete
forest, not from a selected component with the exterior removed.

Define the log-concavity minor

    L_k(F) = p_k^2-p_(k-1)p_(k+1).

## 2. A sufficient prefix statement, and what a counterexample would require

Consider the following proposed stronger statement, named PREFIX_BETA:

    For every finite unweighted forest F and 1<=k<beta(F), L_k(F)>=0.

**Proposition 2.1.** PREFIX_BETA implies ORIGINAL.

For a fixed forest, those inequalities make p_0,...,p_beta log-concave, hence
unimodal: their consecutive positive ratios are nonincreasing. From beta
onward the sequence is already weakly decreasing. Appending this tail cannot
introduce a second rise after a descent. Small beta and the empty graph are
included. This argument does NOT say that every product of unimodal
component polynomials is unimodal.

**Proposition 2.2.** If F has a true valley at i<j, some k with i<k<=j<beta
satisfies L_k(F)<0.

Indeed r_i=p_(i+1)/p_i<1 and r_j=p_(j+1)/p_j>1. If all intermediate successive
ratios were nonincreasing, this would be impossible. Thus r_k>r_(k-1) for
some i<k<=j, exactly L_k<0. The tail theorem gives j<beta.

Consequently a prefix-LC violation is a necessary symptom of an original
counterexample, but is NOT itself an original counterexample. If discovered,
its full sequence must still be tested. PREFIX_BETA remains UNPROVED and
UNREFUTED here; the same is true for the stronger range 1<=k<b0. No finite
absence is substituted for this universal statement.

## 3. Exact independent-set pair partition, retaining the actual exterior

A pair in p_k^2 consists of two ORDERED independent k-sets A,B. A pair in
p_(k-1)p_(k+1) consists of ordered independent sets of the indicated unequal
sizes. Let C=A intersection B, and S=A symmetric-difference B. Then |S|=2r,
|C|=k-r in either case. There is no edge from C to S, and C is independent.
Thus C is an independent (k-r)-set in the actual graph F-N[S]. Conversely,
any such C and an ordered proper two-coloring of F[S] reconstruct a unique
pair. Edges joining different components of F[S] do not exist; all remaining
original vertices and components stay in F-N[S].

For each connected component of F[S], let a_j,b_j be its bipartition sizes.
For an isolated vertex use (1,0). Put

    h_S(z) = product_j (z^a_j+z^b_j),
    w(S)   = [z^r]h_S(z)-[z^(r-1)]h_S(z).

Each component has exactly two labeled colorings, including a singleton;
when a_j=b_j their two choices give coefficient 2, not one. The exponent
records the first color-class size. An empty S has h=1 and w=1.
The preceding bijection proves the exact identity

    L_k(F) = sum_(S subset V, |S|=2r even)
               w(S) * i_(k-r)(F-N[S]).                         (3.1)

Terms with invalid independent-set sizes are zero. This proof includes every
proper-induced-subforest exterior; it does not replace one by arbitrary
nonnegative arrays. The identity is uniform in the forest and k. Seven small
actual-forest controls check it by exact enumeration in src/pairing.py.

## 4. The proposed block-by-block injection is false inside the prefix

One might try to prove each term of (3.1) nonnegative, equivalently balance
pairs while preserving the union and intersection. That fails even before
BOTH tail boundaries.

Use the six-vertex star F=K_(1,5), center 0, leaves 1,...,5. Its actual sequence is

    P=(1,6,10,10,5,1),   alpha=5,   beta=b0=3.

At k=2 take S={0,1,2,3}, C=empty. Then F[S] is a claw, h_S=z+z^3. There are
zero colorings with two vertices in each class and one with first-class size
one. Thus w(S)=-1. The exterior multiplier at k-r=0 equals one. This block
has one ordered pair of sizes (1,3) and no balanced (2,2) pair, so a
union/intersection-preserving injection cannot exist in this block.

There are binom(5,3)=10 negative blocks at k=2. Their total negative mass is
10; all positive blocks together contribute 50. The FULL minor is

    L_2=10^2-6*10=40>0.

The tree is unimodal and prefix-LC. This is an actual counterexample to the
TERMWISE nonnegativity / fixed-union injection shortcut, NOT to PREFIX_BETA,
ORIGINAL, J_H, RSM, or a claim restricted to true minimal counterexamples.
A valid proof via (3.1) must compare different blocks or otherwise control
positive and negative contributions globally. We continue that attempt next.

## 5. A uniform low-index compensation bound

We can perform the aggregate comparison at k=2 without assuming termwise
positivity. For a forest with n>=3 vertices and m edges put

    s = sum_v binom(deg(v),2).

Counting pairs gives p_2=binom(n,2)-m. Inclusion-exclusion on triples gives

    p_3=binom(n,3)-m(n-2)+s.                                (5.1)

An edge belongs to n-2 triples. Two distinct edges can lie in one triple only
when they share an endpoint; each such pair contributes once. A forest has
no triangle, so there is no third-order triangle correction. This proves
(5.1), including disconnected forests and isolates.

Substitution, with p_1=n, yields

    L_2 = n^2(n^2-1)/12 - nm + m^2 - ns.                    (5.2)

There are at most binom(m,2) pairs of incident edges, so s<=binom(m,2).
Also m<=n-1. Therefore

    L_2 >= n^2(n^2-1)/12 - nm/2 - (n-2)m^2/2
        >= (n-1)(n-2)(n^2-3n+6)/12 > 0.                   (5.3)

For fixed n>=3 the intermediate expression is decreasing for m>=0, so the
second inequality follows by substituting m=n-1. An n-vertex star attains
equality: every edge pair shares its center. Thus the displayed lower bound
is sharp at this index. Cases n<=2 and the k=1 inequality are direct from
their coefficients. No claim that this elementary low-index bound is new to
the literature is made.

The program checks the identities and sharp bound on stars and paths of
orders 3,...,29 (54 controls). The proof, not these checks, covers all n.
This does not settle minors k=3,...,beta-1 or constitute a new full-forest
unimodality domain reduction relative to the previous minimal-counterexample
work.

## 6. A second uniform but short initial range

A union bound over the edges gives for 1<=k<=n

    p_k >= binom(n,k)-m binom(n-2,k-2)
        >= binom(n,k) * (1-k(k-1)/n),                     (6.1)

where m<=n-1; for k=1 use the direct count. Independently
p_(k-1)<=binom(n,k-1) and p_(k+1)<=binom(n,k+1).
For k>=2 assume

    n >= 2 k(k-1)(k+1).                                  (6.2)

Writing t=k(k-1)/n gives 0<=t<=1/(2(k+1)). Consequently

    (1-t)^2 >= 1-2t >= k/(k+1)
              >= k(n-k)/((k+1)(n-k+1))
              = binom(n,k-1)binom(n,k+1)/binom(n,k)^2.

The lower bound (6.1) is nonnegative here, so it may be squared. Combining
these inequalities proves L_k>=0 under (6.2). This is a uniform sparse-graph
estimate, not an interpolation of test data. Thirty-two exact rational
parameter checks are arithmetic controls only.

This initial range grows only on the scale n^(1/3); beta for forests grows
linearly with n. It leaves a large middle range. The crude upper bounds on
neighboring coefficients do not supply the compensation required by (3.1)
through that range. No universal sign conclusion outside (6.2) is inferred.

## 7. Position-aware actual-forest exploration

### 7.1 Re-read the old data, not new graph coverage

The four Phase-7 complete coefficient streams contain 8,882 distinct forests,
6,818 non-LC. Fresh positional inspection gives zero breaks at k<b0 and zero
at k<beta. The sharper beta is strictly smaller than b0 in 4,055 records.
This re-reads coefficients and graph identities; it is not a replay of the
previous independent-set DP and is not added to new graph counts.

### 7.2 Complete the previously omitted LC-input bank pairs

The existing bank has 13 LC trees. The 91 unordered pair multisets, including
repetition, were skipped as a heuristic in Phase 7. Here all 91 are checked
at every pair of actual rooted-tree isomorphism classes under the declared
order bound. Rooted isomorphism, not equal root polynomials, justifies this
finite compression, including all internal vertices after completion.
The actual bridge formula is

    P_join=P_S P_T-B_s(S)B_t(T).

All 11,628 distinct joined trees are legal and their complete P is recounted
by rooted DP and a separate vertex-deletion algorithm. Forty-three are
non-LC, showing that LC inputs do not guarantee an LC BRIDGE join. None has
a break before either tail bound, a true valley, or a residual pair. This
closes only the omitted finite bank-pair surface, not all LC-tree joins.

### 7.3 New unequal-depth grammar and whole-subtree changes

The second lane uses seed 2026091908, an order cap 384, 116 accepted founders,
and six generations of width 18. Founders use mixed depth, unequal pendant
lengths, and a few long branches among many short branches. At some centers
one root-state polynomial ends before beta, creating a concrete change in
which counting contribution is available. This is a targeting device, not a
claim that disappearance causes a valley.

Operations replace a whole rooted side by another actual motif, subdivide an
edge, transplant a whole side to a distant vertex, duplicate a branch, cut an
edge, cross-graft actual subtrees, or attach a mixed spider. They are not
repeated expansions of the previously recorded marked wedge operations.
All actual exteriors and other components are retained when specified by the
operation; nothing is canceled from a sign comparison. Each result is
validated as a simple unweighted forest. Selection preserves multiple shape
classes instead of only one highest score.

The full original valley score remains the primary incident test. A second
exact rational score targets negative minors strictly before beta; n-scaling
is a selection heuristic, not a distance or probability. Every full P and
all-vertex U/D are computed regardless of score. Any original or conditional
nonunimodality would stop ordinary expansion for exact diagnosis. A prefix
failure alone would be an auxiliary incident, not proof of ORIGINAL false.

The lane produced 958 distinct forests, maximum order 376: 813 connected and
145 disconnected. Thirty-eight have at least two >=31 components. Of the
fixed heterogeneous product constructions, 21 two-component, 14 three-component
and 2 four-component forests were accepted. Six-component proposals exceeded
the cap; NO six-component coverage is claimed. Other disconnected records
come from cut operations. There are 354 order exclusions and 50 duplicate
proposals. The source records 1,080 distinct marked operation slots over 108
expanded seeds; some have no legal remote destination and do not yield a
graph proposal. Actual proposal accounting is in the stream and summary.

There are 226 non-LC results, all tail-only. None has prefix failure, an
original valley or a residual pair. HEREDITARY remains UNKNOWN for every new
graph. No actual counterexample was found, so no global or greedy minimality
claim is applicable.

## 8. Verification and final logical chain

The combined 12,586 graphs are mutually nonisomorphic and none is in the
supplied Phase-7 canonical inventory. This is not a global earlier-history
novelty claim. Every full P was dual-recounted. The 3,065,560 A/B array
occurrences were COMPUTED; only 24 selected material graphs had every A/B
additionally recounted by the second graph algorithm (8,452 arrays). Complete
P, edges, all mode intervals and conditional hashes are retained for every
record; full A/B arrays are retained for those materials and are regenerable
for all others. Finite checks do not certify HEREDITARY.

At the time of final delivery the CLEAN_REPLAY receipt records the actual
fresh-copy executions, exact hashes and complete-output comparisons. It is
not mathematical closure, an external review, or a Lean proof.

The attempted top-level chain is

    ORIGINAL counterexample -> a true valley before beta
      -> some negative minor at k<beta
      -> exact actual-forest pair decomposition (3.1).

We can prove the sum nonnegative at k=1,2 and under (6.2), but NOT for all
remaining k<beta. The first substantive missing connection on this route is
an aggregate compensation inequality through the unrestricted middle, or a
direct no-rebound argument not requiring full prefix-LC. Termwise positivity
cannot supply it. The existing minimum-counterexample terminal-elimination
route also remains incomplete.

No unbounded class of the OLD remaining minimal-counterexample domain has
been newly ruled out here. The 247 small index classes and their external
census/H2/H3 dependency are preserved; they do not bound large components.
J_H and RSM remain unresolved. FAMILY is inherited unchanged, with no fresh
Lean build or axiom audit. Final status: NOT_CLOSED / NO_STRUCTURAL_ADVANCE.
