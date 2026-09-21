# B6: a one-new-vertex repair of a specified T26 fiber

ORIGINAL = NOT_CLOSED. The new theorem is a scoped, computer-assisted
matching statement, not a theorem that all forests or all residual sources
can be matched. Review is internal; no novelty or formal verification claim.

## 1. Exact domain and reservations

All graphs are finite simple undirected unweighted forests. Independent-set
coefficients count actual vertex subsets. For ordered pairs of sizes (j,j)
or (j-1,j+1), put C=intersection, D=symmetric difference and U=C union D.
The group is admissible exactly when C is independent, C and D are disjoint,
there are no C-D edges, and 2|C|+|D|=2j. For each component of F[D] with
bipartition sizes a,b, retain both orientations, including multiplicity two
when a=b. The signed surplus is the central coefficient minus its preceding
coefficient in product(z^a+z^b). Cancel within each group once by pair rank.

Known reservations in this document mean the actual E4 canonical payments,
Phase13 ONLY at global j=4, and the additional published E5-JC-v2 payments,
with overlapping source groups charged once. They do not include unannounced
future rules. E5's four-vertex release is not a C-increasing one-new-vertex
operation. The early E5-ONE-v1 uses only E4 and j=4 Phase13 reservations; our
B6-JC-ONE-v1 composite additionally preserves E5-JC. These are separate tests.

## 2. Statement B6-ONE-FIBER-v2

Let T be the actual 26-vertex tree made of a central root and three adjacent
hubs bearing respectively 3,4,4 private length-two paths. Let F=T disjoint-
union Y, where Y is ANY forest with a fixed vertex z. Fix the T labeling used
by the supplied constructor, and place all Y vertices after its 26 labels.
For a fixed j>=13, consider ALL independent sets C0 of Y-N_Y[z] with size
j-13. In the fiber with exterior selections (C0,C0), retain every negative
ordered pair having core sizes (12,14).

After within-group cancellation and E4 payments, each fiber has exactly
1575 unpaid negative objects, in 1575 distinct demand-one groups. There is
an injective assignment of all these groups to actual positive groups which
introduces ONLY the vertex z into their selected union and increases their
intersection. Every chosen target has ZERO incoming load from ALL the known
reservations in Section 1. Assigning only those sources that E5 has not
already paid therefore preserves the entire known matching without double
payment. Targets belonging to distinct C0 are disjoint as groups.

This theorem has no HEREDITARY or History premise; those are separately
proved for the original-problem calibration graphs below. It does not match
pairs with arbitrary unequal exterior selections, nor all negative groups
of an arbitrary forest. T must be a complete component, not a symmetric-
difference block with arbitrary crossing edges.

## 3. Complete finite core certificate

Graph DP and a separate centroid vertex-deletion/component algorithm give

 P_T=(1,26,300,2040,9142,28551,63933,103736,121376,100144,
      55499,18683,2979,51,1).

The rank-12,13,14 independent subsets are enumerated directly from the actual
edges. They number 2979,51,1. ALL 5580 positive/negative ordered pairs are
grouped by their actual C,D masks and checked against orientation counts.
Positive objects number 2601 and negative objects 2979. Internal cancellation
uses 931 of each; positive group surplus is 1670 and negative demand 2048.
The canonical E4 rule reserves 473 demand-one sources. Thus the remaining
internal capacity is 1197 whereas the remaining demand is 1575. The shortage
378 is inherited as an obstruction to keeping the exterior fixed, not newly
claimed as an original counterexample.

For each of these 1575 remaining sources (C,D), generate candidates

 target = (C union {z}, D minus {u,v}),  u,v distinct vertices of D.

Check actual target admissibility, orientation surplus, and every known
inverse source in the COMPLETE 35-vertex calibration F35=T+P3+6K1, using the
isolated vertex z=29. The retained positive subnetwork has 160044 target
groups and 160044 arcs. Its two integer flow algorithms both pay 1575.
The selected 1575 targets are distinct. Each selected target has NO high
component and EXACTLY TWO unit components, with any remaining components
balanced. Its surplus is at least one. Every selected target has zero known
load, including E5, by a separate complete inverse-source audit.

The entire 1575-row finite certificate is ONE_VERTEX_BASE_CERTIFICATE.json.
It records source C,D, target core C,D, demand one, surplus and zero known
load. Its generator checks the full source set, not just successful examples.
The table is a finite computer-assisted part of the theorem. A smaller or
incomplete target subnetwork would suffice for this positive result; none
of its failure cuts is claimed to refute the full permission network.

## 4. Why the certificate lifts to arbitrary Y and all eligible C0

For a base table row, replace its source intersection by C union C0 and its
target intersection by C union C0 union {z}. Keep both D masks inside T.
C0 is independent and avoids N_Y[z], so both groups are admissible in F.
Their index is 13+|C0|; their orientation polynomials and surplus/demand are
unchanged. The target introduces exactly z and removes two original D
vertices. Its intersection contains the source intersection.

Within one fiber the table targets are distinct. Between fibers, removing
the FIXED z from the target's exterior intersection recovers C0 uniquely.
Thus targets from different fibers cannot coincide. Choosing a different
z separately for each C0 without an inverse rule would not justify this
argument; the theorem deliberately fixes z for the whole collection.

It remains to prove freshness in the full ambient graph, rather than import
an internal ledger blindly. The selected targets have zero high components
and two units. E5 multi-high, two-high and release payments all end at targets
with at least one high component. Phase13 does not apply because j>=13.
E4 multi-claw targets also retain high components. Only an E4 single-high
normalization could use one of our target slots.

Every inverse normalization has a removed center v outside target U and
its unique neighbor w in the target intersection. If v belongs to T, then
w also belongs to T: no edge crosses between T and Y. Its source, splitter
and all core compatibility tests are exactly those audited in the finite
base; C0 and z add no core adjacency. These inverse sources have zero load.
If v belongs to Y, then w belongs to Y and neither vertex meets target D,
which is entirely in T. The inverse adds the separate edge vw as a balanced
D component. Its signed surplus is twice the POSITIVE target surplus.
It is not a negative source and cannot spend capacity through E4.
This exhausts all possible inverse centers in the full original graph.
Hence the targets have zero known load for every Y and every eligible C0.

For each unpaid source, use its table target and choose an unused positive
object there by rank after internal cancellation. Its surplus is at least
one and no other chosen source uses it. Preserve previously paid E5 sources
by omitting them from this new assignment, not by charging them twice.
This constructs the asserted combined injection. QED, subject only to the
explicit finite core certificate that has been regenerated and audited.

## 5. HEREDITARY and actual middle/history calibration

For T26, a connected induced component retaining the central root is described
at each original hub by either absence, or a retained hub with a intact
length-two paths and l near-endpoint leaves, a+l<=3 or4 as appropriate.
There are 11*16*16=2816 parameter records. Each actual completed component
was dual-counted and is unimodal. Every other connected component is a
single hub with at most four such arms/leaves, or an edge or singleton;
the 15 parameter types include these cases and are all LC. This is a complete
classification of possible connected induced components, NOT 2^26 separate
DP runs. A disjoint induced forest has at most one component containing the
original root, so LC-times-unimodal convolution proves it unimodal.

For completeness, if a is LC with interval support, k<l and j<t imply
 a_(l-j)a_(k-t)<=a_(k-j)a_(l-t), including zero endpoints, by monotone ratios.
Split the zero-padded differences of a unimodal b into early nonnegative
and late nonpositive parts. The corresponding convolved gains P_k and losses
N_k satisfy P_l N_k<=P_k N_l. A strict loss P_k<N_k consequently forbids a
later gain P_l>N_l, even when N_l=0. This proves LC-times-unimodal. The usual
2-by-2 Cauchy-Binet expansion of the same Toeplitz kernels also proves LC
convolution. Thus induced P3/isolated factors preserve the needed heredity.

F35=T26+P3+6K1 has n=35,M=26,alpha=22,h=9,beta=14. At k=12,
 p12=29897235 > p13=26364141 > p14=18657714.
The whole sequence is LC. Before E5 reservations the 1575 fiber sources can
now be paid with one new vertex. With the final E5-JC rules already reserved,
1563 of those sources have four-release payments; the remaining 12 are paid
by the restricted one-new-vertex assignment. They are NOT counted twice.
No assertion is made that each of those 12 individually requires a new vertex.

For the inherited F_r=T26+rP3, r>=42, choose C0 to be the first r+4 path
leaves and z the next path leaf. The new table lifts with j=r+17. Here
 n=3r+26,alpha=2r+14,M=26,
 alpha(n-1)-j(n+alpha)=r^2-33r-330>0.
Also 26(3r+25)<102(r+16), so h+1<=j<beta. The coefficients of
(1+3x+x^2)^r are symmetric and strictly LC, hence strictly decrease after r.
All shifts by the core support 0..14 place j-2 through j+1 strictly past r,
so these four whole coefficients strictly decrease. This supplies genuine
EARLIER descent. HEREDITARY follows from the preceding complete T26 induced
classification and induced P3 LC factors. The r=42 graph (n152,j59) was
freshly counted by both graph algorithms and ALL 1575 lifted targets were
checked for known incoming sources in the whole graph. Its first decline
is at50, earlier than k58. E5's existing four-release already pays this
particular fiber in the composite ledger; the one-new-vertex construction
is an alternative for early E5-ONE, not 1575 additional unpaid sources.

## 6. Complete permission networks, separate from fiber statements

Two new 16-vertex trees at j6 have full HEREDITARY certificates: every one
of their 65535 proper induced vertex subsets was checked by literal subset
zeta counting and vertex deletion. Both have h4,beta7 and real decline at k5.
ALL their nonempty ordered-pair groups are generated by D orientations and exact exterior
independent sets, and independently by literal ordered pairs. The full source
and target group sets agree. Every arc satisfying C_source subset C_target
and |U_target minus U_source|<=1 is included, with complete old occupancy.

The first network has 1236 residual sources, demand1513, 114807 positive
targets, and12764132 permitted arcs. The second has694 sources, demand820,
135150 targets and7398564 arcs. Zero-capacity targets are retained. Two sparse
integer maximum-flow implementations agree and actual positive flows are
checked against every source and target bound. The two reservation versions
(early OLD and final-JC composite) coincide on these particular graphs;
they are NOT four independent graph instances. Their complete zero-new
subnetworks already pay the demands, so these ordinary full networks do not
by themselves demonstrate the need for the new permission. Section3's
378-deficit core fiber supplies that separate distinguishing test.

All E5 rules were also exercised on actual two-high, four-release and
non-claw multi-high controls, with full incoming ledgers. Phase13 is tested
only at j4. The old H9 2>1 greedy collision is preserved as a control whose
target consists of two isolates. It is not a failure of a broader network.

## 7. Existence searches and original problem: no closure

Coherent module edits retain every leaf; branch/interface changes retain
all roots at a fixed middle position. Every whole sequence is also scanned
across plateaus. The 113- and96-vertex best ADMC profiles have respectively
28 and40 leaves, all with deletion-mode distance1, not2. The121-vertex
root-envelope search did not improve its initial value:120 roots remain
good at the tightest tested index despite a negative central state. No
all-root or all-leaf failure was found. Ordinary large graphs remain
HEREDITARY UNKNOWN; full LOCAL tests do not promote them to HEREDITARY.
The458-vertex fixed-k144 next-decline search retained both non-LC components
and excluded only actually verified C5-W gates; its best1.9851027% decline
did not improve. No new middle LC/C1 failure, historical plateau or whole
sequence valley was found. No failing original candidate existed to reduce.

The first unresolved step is still a universal leaf/root existence principle
or enough unused target capacity for EVERY remaining admissible group.
The one-fixed-core source sector above does not supply that missing statement.
ORIGINAL remains NOT_CLOSED. Lean and axiom audit are NOT_RUN.

Counting convention clarification: groups with zero positive AND zero negative
objects are omitted from numeric group totals. They contain no source or
target capacity. All groups with either count nonzero, including equal positive
and negative counts, are retained. This does not alter any network or proof.
