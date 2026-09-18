# ORIGINAL proof attempt: minimum counterexample and residual slopes

**NOT_CLOSED. There is no complete ORIGINAL proof or legal counterexample in
this run.** Sections 1-8 give proved reductions from actual independent subsets.
Section 9 identifies the first unproved structural bridge. Section 10 retains
failed strengthenings and distinguishes their scopes. Computations in section
11 are bounded checks, not a substitute for section 9. All mathematical review
here is SAME_MODEL_SELF_REVIEW.

## 1. Definitions, support, and the minimum-counterexample setup

Use the unweighted forest and independent-set definitions in STATEMENT.md.
For a forest on n vertices, a_0=1, a_1=n, and

    a_2=binomial(n,2)-|E|.

The last formula holds because a pair is not independent precisely when it is
an edge. If alpha is the largest independent-set size, all counts at 0..alpha
are positive: any k-subset of a fixed maximum independent set is independent.
Counts past alpha are zero. We always keep the full list through n.

For any finite sequence, unimodality is equivalent to the absence of indices
i<j with Delta_i<0<Delta_j. One direction follows from the peak definition.
For the converse, if there is no negative difference, choose the last index.
Otherwise take the first negative difference at q. All earlier differences are
nonnegative, and absence of a later positive difference makes all differences
from q onward nonpositive. Choose peak q. Zero differences cause no problem.

The empty forest has the single coefficient 1 and is unimodal. Suppose a
counterexample exists. Choose one with the least vertex count n. Then n>0 and
EVERY forest on fewer than n vertices has unimodal counts, regardless of
connectedness or whether it is a subgraph of the chosen forest. Any proper
induced subgraph is such a smaller forest. This is a valid strong-induction
premise obtained from the hypothetical minimum; it does not assume the full
polynomial is unimodal. We do not assume the counterexample is connected.

## 2. Actual graph decompositions and rooted messages

Partition the independent subsets of F according to whether they contain v.
Those not containing v are exactly the independent subsets of F-v. Removing v
from a subset containing v is a bijection onto independent subsets of F-N[v];
its size decreases by one. Therefore

    I(F;x)=I(F-v;x)+x I(F-N[v];x)=A_v+B_v.               (2.1)

This proves, rather than defines, the counting recurrence. Both underlying
deleted forests are smaller; in the minimum-counterexample setup their counts
are unimodal. Multiplication by x shifts a unimodal nonzero sequence by one and
keeps its shape (with a leading zero), so B_v is also unimodal.

For a disjoint union, intersecting an independent set with each component is a
bijection onto a tuple of independent subsets, with sizes adding. Distributing
the finite sums gives the product of component polynomials. This identity does
NOT say that a product of arbitrary unimodal polynomials is unimodal.

For a rooted tree, let Z0,Z1 count the independent subsets with its root absent
or present, including the root in the size for Z1. Once the root is absent,
child subtrees are independent choices; once present, child roots must be
absent. Thus the actual child messages give

    Z0=product_child(Z0_child+Z1_child),
    Z1=x product_child Z0_child.                       (2.2)

For a leaf these are 1 and x. These identities describe every finite rooted
tree recursively, since deleting its root separates its child subtrees.
Other components must still be multiplied into both conditional polynomials.
We do not cancel such a factor in any coefficient or mode comparison.

## 3. Complete finite-sequence joint-bound lemma

Let C be a nonnegative, nonzero, unimodal finite sequence, extended by zero
outside its displayed support. Its maximum is positive. All indices attaining
that maximum form an interval [ell,r]: monotonicity on either side of a peak
precludes a smaller value between two maxima. On the full integer index range,

    Delta C_k>=0 for k<r; Delta C_k<=0 for k>=ell.       (3.1)

Inside the maximum interval the differences are zero. Before/after it the
signs follow from unimodality; zero padding respects these signs.

Suppose nonzero unimodal A_v,B_v, indexed by a nonempty finite set, all sum to
the same polynomial P. Define u_v,d_v,U,D as in STATEMENT.md. If k<U, choose a
vertex attaining U. Then k<r_Av and k<r_Bv. By (3.1) both differences are
nonnegative, hence Delta P_k>=0. If k>=D, choose a vertex attaining D. Then
k>=ell_Av and k>=ell_Bv, so Delta P_k<=0. These witnesses can be different.

If D<=U, the signs overlap on D<=k<U and force all those differences to zero.
For k<D the nonnegative bound applies; for k>=D the nonpositive bound applies.
Thus D is a valid peak. If D=U+1, all comparisons except Delta P_U have the
required signs. When Delta P_U>=0 choose peak U+1; when it is negative choose
peak U. Equality allows either. This proves the entire D<=U+1 criterion,
including plateaus and endpoints, without assuming P is unimodal.

For one vertex, overlapping mode intervals give d_v<=u_v. Disjoint adjacent
intervals give d_v=u_v+1. Therefore distance at most one gives

    D<=d_v<=u_v+1<=U+1.

This proves the single-vertex-to-joint implication. It does not establish
existence of such a vertex in any untested forest.

## 4. Necessary restrictions on a minimum counterexample

For the hypothetical F in section 1, every split satisfies the hypotheses of
section 3. Any valley pair i<j must therefore satisfy

    U<=i<j<D, and in particular D>=U+2.                (4.1)

Indeed a negative difference cannot occur below U, and a positive one cannot
occur at or above D. Both valley indices lie in the unresolved interval.

We also need two elementary component exclusions. If C is nonzero and
unimodal, then (1+c x)C is unimodal for any positive c. To see this without a
convolution-closure assumption, C and c x C are individually unimodal and their
mode intervals are [ell,r] and [ell+1,r+1], with distance at most one. Apply
section 3 to this single sum. If F had an isolated vertex, its polynomial would
be (1+x) times a smaller forest polynomial and hence unimodal. If it had a
single-edge component, the corresponding factor would be 1+2x, giving the same
contradiction. Thus neither kind of component occurs in a minimum counterexample.
This is not a reduction of all forests to connected trees.

Every nonempty forest with no isolated vertices has a leaf: take a longest
simple path in one nontrivial component. An additional neighbor at an endpoint
would either extend that path or create a cycle. Thus a leaf-support split is
available in the setup used below.

## 5. All-vertex count identities and their limitation

Count pairs (S,v) where S is an independent k-set. For B_v the vertex v belongs
to S, so each S occurs k times; for A_v it does not, so S occurs n-k times.
Consequently, for every k,

    sum_v B_(v,k)=k a_k, sum_v A_(v,k)=(n-k)a_k.        (5.1)

Subtracting neighboring identities gives

    sum_v Delta B_(v,k)=(k+1)a_(k+1)-k a_k,
    sum_v Delta A_(v,k)=(n-k-1)a_(k+1)-(n-k)a_k.        (5.2)

These exact identities retain all vertices and disconnected components. They
are checked coefficient by coefficient in the diagnostic source. They do not,
by themselves, forbid a sign change inside [U,D); the k-dependent terms prevent
an unproved argument from average signs to one shared vertex.

## 6. Unique early/late roles at every vertex

Assume Delta P_i<0<Delta P_j with i<j and a unimodal split P=A+B. At i at least
one summand has negative difference. Call it E. Unimodality prevents E from
having a positive difference later, so Delta E_j<=0. The other summand L must
then have Delta L_j>0. That positive later difference prevents L from having
a negative difference at i, so Delta L_i>=0. The roles are unique: the summand
positive at j cannot also be negative at i.

The maximum interval of E ends by i, since it has already strictly decreased
there; the maximum interval of L starts at or after j+1, since it is strictly
increasing at j. Therefore

    r_E<=i, ell_L>=j+1, dist(M(E),M(L))>=j+1-i>=2.      (6.1)

This conclusion applies to EVERY actual vertex split of a minimum
counterexample. Call a vertex selected-late when its B_v is L, otherwise
selected-early. This is a consequence of an assumed real valley, not a tested
property which can manufacture such a valley.

## 7. Leaf-support structure, including opposite selected roles

Let ell be a leaf with neighbor w and put

    C=I(F-{ell,w};x), H=I(F-N[w];x).

Partitioning on w after removing ell, and noticing that ell becomes an isolated
vertex when w is absent, gives all four actual conditional polynomials:

    A_ell=C+xH,       B_ell=xC,
    A_w=(1+x)C=:X,    B_w=xH=:Y,
    P=(1+x)C+xH.                                    (7.1)

For clarity about realizability, remove ell,w. Let T_1,...,T_s be the components
which contain other neighbors of w, rooted at those neighbors; let R be the
polynomial of components of F not containing w. Two different neighbors cannot
remain connected after w is removed, or F would contain a cycle. Hence

    C=R product_t I(T_t),
    H=R product_t I(T_t-root_t).                       (7.2)

A zero number of branches gives empty product 1. The graphs T_t, the root
choices and R are real objects. Merely requiring H<=C and some unimodal shapes
loses this product relation; section 10 gives an explicit failure of that loss.

We also prove the modal fact needed to compare A_w with B_ell. If C has a
unique maximum at m, (1+x)C increases weakly up to m and decreases weakly after
m+1, and its maximum lies among m,m+1. Strictness of C's maximum rules out any
extra equal maximum outside those positions. If C has a plateau [ell_C,r_C]
with ell_C<r_C and maximum c, the coefficients of (1+x)C equal 2c exactly on
[ell_C+1,r_C]; elsewhere at least one summand is strictly below c. Thus in both
cases the mode intervals of (1+x)C and xC are at distance at most one. This
argument also covers a constant C using zero padding.

Now suppose a real valley occurs at i<j. Opposite early/late roles for A_w and
B_ell would force their modes to be separated by at least two by (6.1), which
contradicts the preceding modal fact. They have the SAME role. Since A_w and
B_w have opposite roles, B_ell and B_w have OPPOSITE roles. All leaves at a
common support therefore have the same selected role. For a single-edge
component B_ell=B_w, giving another check on its exclusion in section 4.

This is a necessary graph-structural restriction, NOT a contradiction for
arbitrary trees: opposite roles across leaf edges can coexist. No claim that a
tree cannot carry such roles is used to finish the proof.

## 8. Signed-minor obstruction forced by an actual valley

For a polarized pair E,L as in section 6 put

    e_i=-Delta E_i>0, e_j=-Delta E_j>=0,
    l_i=Delta L_i>=0, l_j=Delta L_j>0.

Then Delta P_i=l_i-e_i and Delta P_j=l_j-e_j. Direct expansion, with no division
and hence no omitted zero-denominator case, gives

    Q = l_i e_j-l_j e_i
      = Delta P_i*e_j - Delta P_j*e_i < 0.             (8.1)

The first term is nonpositive and the second strictly negative. Thus every
vertex split, and in particular every leaf-support split, has a negative Q
when the whole sequence actually descends and later ascends at these indices.
A nonnegative Q at just one polarized split blocks that pair of valley indices;
a split which cannot be polarized also blocks it by section 6.

The converse is false: E=[3,2,1] and L=[1,4,8] have Q(0,1)=-1 but their sum
[4,6,9] is increasing. Consequently a negative minor is never called an
ORIGINAL counterexample. It is a necessary condition used to try to exclude
minimum counterexamples.

## 9. FIRST UNPROVED BRIDGE: residual real-forest signed minor

The exact RSM assertion, all its quantifiers, and the branch-product formula
are in STATEMENT.md section 4. It is UNRESOLVED. There is no proof here that a
suitable leaf-support split exists or has nonnegative Q for each residual pair
U<=i<j<D. The real branch relation (7.2) has not yielded the needed inequality.

The downstream implication has no remaining gap other than that assertion:
if a minimum counterexample existed, sections 1-4 would give HEREDITARY, no
isolated vertices, a leaf, D>=U+2 and a valley pair inside [U,D). RSM would select
one leaf-support split. Sections 6 and 8 force that very split to be polarized
and have Q<0, contradicting both alternatives in RSM. ORIGINAL would follow.

This is a conditional implication, not an ORIGINAL proof. No certificate in
this run establishes RSM. In fact all diagnostic graphs satisfy D<=U+1, so
they provide NO nonvacuous test of its difficult residual case. The simpler
universal joint inequality J also remains unproved. We have not hidden either
assertion in an induction hypothesis, claimed it follows from the definition
of U,D, or claimed that refuting it would refute ORIGINAL.

## 10. Failed strengthenings, with exact scope

### 10.1 An arbitrary leaf cannot be chosen under LOCAL

The certificate tree-11 is a 23-vertex tree with edges

    0-1, 0-17, 0-22, 1-2, 1-3, 1-15, 1-16,
    2-4, 2-5, 2-6, 2-10, 2-14, 2-18,
    3-8, 3-9, 3-20, 3-21, 6-7, 8-13, 9-11, 9-12, 18-19.

Its full coefficients through order 23 are

    [1,23,231,1359,5287,14516,29219,44068,50306,43483,
     28198,13441,4542,1022,136,8,0,0,0,0,0,0,0,0].

At leaf 4, M(A_4)=[7,7], M(B_4)=[9,9]. Every specified deletion polynomial is
unimodal, but this leaf is not a good vertex. Thus the assertion 'under LOCAL,
every leaf is good' is false. The maximum of the whole sequence is at 8;
U=D=8, and vertex 0 has both conditional maxima at 8. Neither L, J nor ORIGINAL
is refuted. No claim about ALL proper induced subforests, ALL smaller forests,
or global minimality was tested for this witness. The full A/B arrays of every
vertex are retained in certificates/material.json. Git also hosts the lossless polynomial table
certificates/material_compact.json, with all whole and A/B counts for this graph.

### 10.2 An unlocalized slope-minor inequality fails in a real forest

For the star with center 0 and leaves 1,...,6, any leaf-support split has
C=(1+x)^5, H=1, X=(1+x)^6, Y=x. At i=1,j=2, Y is early and X late:

    Delta Y_1=-1, Delta Y_2=0,
    Delta X_1=9,  Delta X_2=5,  Q(Y,X;1,2)=-5.

Yet P=[1,7,15,20,15,6,1,0] is unimodal, and its differences at 1 and 2 are 8
and 5, both positive. All 128 induced vertex subsets were counted by DP,
deletion and subset enumeration; 127 are proper. This satisfies HEREDITARY for
THIS graph, not a global minimality premise. It refutes the unlocalized
all-leaf minor inequality. U=D=3, so the indices 1,2 are outside the residual
interval and the example does NOT refute RSM. Residual localization is essential
and was retained before any final claim.

### 10.3 Shape-only leaf insertion fails for abstract sequences

Take C=[1,6,7,8,9,8,1] and H=[1,4,1]. H<=C coefficientwise and each of
C,H,C+xH,(1+x)C,xH,xC is unimodal. However

    (1+x)C+xH=[1,8,17,16,17,17,9,1]

has the valley 17>16<17. This rejects that precise ABSTRACT shape-only closure
claim. It cannot be a forest example: C_1=6 and C_2=7 would require
binomial(6,2)-7=8 edges, impossible in a forest on six vertices. No graph is
silently assigned to the two sequences. The real-product constraint (7.2)
remains in the unresolved assertion.

### 10.4 The inherited non-log-concavity control remains a non-counterexample

The old25 graph and the five-vertex attachment at root 2 are reconstructed from
closure_v5/src/verify_graphs.py at the pinned baseline. The new30 coefficients
through degree 17 are

    [1,30,406,3295,17975,69985,201395,437256,723946,916415,
     882241,636509,334599,121770,27779,3135,54,1],

followed by zeros through order 30. Its LC difference at 16 is 54^2-3135=-219,
but its maximum is at 9 and it is unimodal. For the root-2 split, A at indices
15,16,17 is (1935,50,1) and B is (1200,4,0): the two LC contributions are 565
and 16, and the mixed contribution is -800. Their sum is -219. The old split
has A_13=1 and B_13=4, incompatible with the previous B59 dominance bound.
This failure has not been erased or treated as an ORIGINAL counterexample.
The missing Git-hosted graphs.json was not pretended to exist: these exact
edges were recovered from the committed source, and all counts were freshly
recomputed, including every vertex split in both old25 and new30.

## 11. What the exact computations do, and do not, establish

The diagnostic plan fixed the graph generator, seed, budgets and stop rules
before execution. The 193 stress records are not an exhaustive or globally
novel set. All 15,499 whole and specified deletion counts were computed by
rooted forest DP AND independent vertex-deletion recursion, comparing full
integer arrays, not only maxima/hashes. The implementations also use different
multiplication algorithms. The recurrence uses positional integer encoding
with base exceeding the product of coefficient sums, so no coefficient can
carry into another digit. The recurrence strictly reduces the active mask;
component splits and isolated-vertex binomials are justified by section 2.

All simple labeled graphs on 0..5 vertices were enumerated by edge subsets,
with cycle-containing inputs rejected. This covers every labeled forest of
those orders; it is not an isomorphism-deduplicated claim. There are
1,1,2,7,38,291 accepted inputs. Every whole and specified deletion count also
agreed with direct enumeration of all independent subsets. This is regression
coverage, not the infinite structural step in section 9.

Four material graphs (tree-11, old25, new30, star7) had every one of their 174
whole/specified-deletion counts rerun. The star's full induced-subset audit and
two abstract controls are separate. Finite sequence regressions exercise the
proved algebraic lemmas, including multiple decompositions with the same sum;
they are not substitutes for the written proofs. Fresh clean-source replays
compare the full deterministic JSON outputs. See certificates/CLEAN_REPLAY.json.

Every stress graph was unimodal and had at least one good vertex; max(D-U)=1.
There were no ORIGINAL candidates, no excluded graphs, and no graph exercising
a residual interval with two indices. These facts do not verify L, J or RSM
beyond the exact stated inputs. No arbitrary additional samples were added.

## 12. Formal, literature and publication boundaries

No B59 theorem, external convolution theorem or unverified literature claim
is a dependency of sections 1-8. A bounded primary-source check read the
statement and restricted theorems of Grace M.X. Li's arXiv:2603.03025v1; they
are not a theorem about every forest and were not used in this proof attempt.
Live original-problem page/forum fetches failed. The run therefore makes no
claim about a globally verified latest solution status or novelty.

The fresh Lean command probe returned command-not-found/127. No top-level
ORIGINAL Lean source, build or transitive axiom audit was produced. This is
NOT_ESTABLISHED, not formal verification of the reductions or ORIGINAL.
The inherited FAMILY math/formal boundary is unchanged and source-pinned.

The delivered package records exact source, inputs, full counts, review and
actual replay logs. Git hosts a compact reconstructible subset identified in
README.md; the large full diagnostic JSON is in the conversation archive and
can be regenerated. Publication receipts identify actual commits separately.
PR #1 must remain Draft and unmerged. Repository checks do not certify any
mathematical statement. No external reviewer, organizer endorsement, global
priority or award claim is asserted.
