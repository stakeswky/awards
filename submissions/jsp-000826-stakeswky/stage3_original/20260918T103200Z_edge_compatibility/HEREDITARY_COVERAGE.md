# Complete proper-induced-subset coverage for the finite witnesses

This verifies HEREDITARY for specified graphs only. It does not enumerate all
smaller forests, imply GLOBAL-MINIMAL, or establish a universal theorem about
U,D. The exact algorithm is src/hereditary.py, independently checked on small
graphs by src/coverage_regression.py.

## 1. Signature semantics
Root every component of the input forest at its least-numbered vertex. A
rooted-tree signature is the sorted tuple of the signatures of its children;
a leaf has signature (). A forest signature is a sorted tuple of rooted-tree
signatures. Equal signatures construct isomorphic unweighted forests by
recursively making one new vertex for each rooted-tree node. Root locations
are inherited from the original rooting, not necessarily the least label in
the surviving induced component. Different signatures may describe the same
UNROOTED isomorphism type; no minimal or unique unrooted-type count is claimed.

For a subtree rooted at v, the algorithm retains two disjoint states:
A: v omitted, with a forest signature;
P: v retained, with a pair (children of the component containing v, all other
components). Each entry stores its exact subset multiplicity and one actual
original-vertex mask. Counts are not estimated or sampled.

## 2. Coverage and multiplicity proof (H1)
For a leaf there is exactly one absent choice (the empty set) and one present
choice (the singleton). Assume recursively that each child has the complete
and disjoint classification of its vertex subsets. A subset below v is
uniquely determined by whether v is included and by a choice of one subset in
each disjoint child subtree. Thus the transition considers every subset once.

If v is omitted, each child's surviving components remain separate. If v is
retained and a child root is retained, its root component is attached as one
child of v; that child's other components remain separate. If that child root
is omitted, all its components remain separate. These are precisely the
edges of the induced forest: there are no cross-child edges in a tree.
Sorting signatures merges isomorphic rooted descriptions but never omits a
choice. Multiplicities multiply for disjoint child choices and add for merged
entries. Actual witness masks combine by disjoint union (bitwise OR).

Induction proves both the semantic correctness of every signature and exact
coverage. The checksum that absent and present each contain
2^(subtree_order-1) subsets is a useful assertion, NOT a substitute for this
induction. Combining original connected components uses the same disjoint
product rule. Therefore the final total multiplicity is 2^n. Exactly one
subset has n vertices (V itself), so entries of order below n cover exactly
2^n-1 proper subsets. This establishes coverage independently of the numerical
unimodality tests.

## 3. Why counting one representative per signature suffices
An isomorphism maps independent k-sets bijectively to independent k-sets, so
all subsets assigned the same signature have the same complete coefficient
sequence. For every retained signature the program reconstructs an actual
forest and counts it by two algorithms. It also counts the stored ORIGINAL
subset mask by both algorithms and compares the entire arrays. The recurrence
proof ensures this representative is not standing in for unrelated graphs.

The first counter uses absent/present rooted dynamic programming and ordinary
integer convolution. The second branches on vertex exclusion versus closed-
neighborhood removal, splits disconnected components and uses no-carry
positional integer multiplication for convolution. Every coefficient is
compared; a_0,a_1,a_2 are checked against the graph. All coefficients through
each subset's order, including trailing zeros, are retained. The unimodality
test detects any negative difference followed later by a positive difference;
flat differences do not hide a valley.

The algorithms share basic graph validation and input representation; they
are independent counting algorithms, not independent people or theorem
provers. Their correctness is justified by independent-set partitions and
component products. This is computer-assisted finite verification, not Lean.

## 4. Independently enumerated coverage regression
For every one of the six main-batch graphs of order at most 12, and five
separate small regression forests, coverage_regression.py enumerates EVERY
vertex mask. It constructs the induced rooted-component signature directly
from that mask, without the compressed transition rule. The complete Counter
of signatures/multiplicities is compared with the compressed result. Every
mask is also recounted by all three methods: DP, deletion, and direct
independent-subset enumeration. This checked 9,573 subset occurrences.

The separate controls are the empty forest, three isolated vertices, K2, P3,
and P4 disjoint union P3. They test empty components, isolated vertices and
nonconnected multiplication; they are not silently counted among the 60 main
records. Five invalid graph inputs were rejected, and four zero/plateau/shift
sequence controls passed. These regressions supplement the coverage proof;
they do not extend the finite witness theorem to arbitrary order.

## 5. Exact completed finite coverage (H2)

| Graph | Order | Proper subset occurrences | Proper signature entries |
|---|---:|---:|---:|
| tree-11 | 23 | 8,388,607 | 22,174 |
| star7-minor-control | 7 | 127 | 12 |
| join-0-0-length1 | 10 | 1,023 | 103 |
| join-0-0-length3 | 12 | 4,095 | 285 |
| join-0-1-length1 | 12 | 4,095 | 241 |
| P4 | 4 | 15 | 6 |
| double-star22 | 6 | 63 | 17 |
| Total occurrences | | 8,398,025 | 22,838 |

All proper sequences in these covered sets are unimodal. The per-graph
30-second and 100,000-intermediate-signature limits were not reached. Other
main-batch graphs are HEREDITARY UNKNOWN, not assumed true.

The 23-vertex result upgrades the premise verification of an EXISTING bad-leaf
witness. Its leaf 4 has conditional modes 7 and 9 despite full HEREDITARY,
but the whole graph is unimodal, vertex 0 has modes 8 and 8, and U=D=8.
It refutes the every-leaf strengthening, not J_H, RSM, ORIGINAL, or the
existence of at least one good vertex. No smallest-order claim is made.
