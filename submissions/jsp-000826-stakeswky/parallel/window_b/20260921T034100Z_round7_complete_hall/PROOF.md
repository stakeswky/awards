# B7: a complete one-new-vertex Hall obstruction, with precise ledger scopes

Run: `20260921T034100Z_round7_complete_hall`.
**ORIGINAL = NOT_CLOSED.** The forests below are ordinary finite simple,
undirected, unweighted graphs. The main negative result concerns a proposed
capacity route, not independence-sequence unimodality. Review is internal,
not outside peer review; no novelty or formalization claim is made.

## 1. Objects, histories and three different old ledgers

Let p_i(F) count independent i-subsets, p_0=1, with zero padding. ORIGINAL
fails only if p_i>p_(i+1) and p_j<p_(j+1) for some i<j. Platforms between
these positions remain. History(F,k) requires a strict decrease at some
 i<=k and no increase from that step through k; i=k and i<k are distinguished.
Put mu_k=(k+1)p_(k+1)/p_k, d_k=k+1-mu_k and
 e_k=mu_(k+1)-mu_k-1. Then d_(k+1)=d_k-e_k. The actual next-rise condition
is e_k>d_k, not merely e_k>0. All divisions use positive support.

The reporting endpoints are calculated from the WHOLE graph:
 h=floor(M(n-1)/(4M-2))+1,
 beta=ceil(alpha(n-1)/(n+alpha)),
where M is the largest component order. Middle history means h<=k and
k+1<beta. These inherited endpoints are not new theorems of this package.

At fixed j, positive objects are ordered independent (j,j) pairs and negative
objects are ordered independent (j-1,j+1) pairs. Let C be the intersection,
D the symmetric difference, and U=C union D. Admissibility requires C to be
independent, disjoint and nonadjacent to D in the ORIGINAL graph, and
2|C|+|D|=2j. If Q runs over components of F[D] with side sizes a_Q,b_Q, then

 O_D(z)=product_Q(z^a_Q+z^b_Q),
 g(D)=[z^(|D|/2)]O_D-[z^(|D|/2-1)]O_D.

Balanced components retain BOTH orientations. Match equal numbers internally
once; remaining group demand is -g when g<0 and capacity g when g>0.
The COMPLETE one-new endpoint permission is

 |U_target minus U_source| <= 1.                              (1.1)

There is NO C-growth, frozen-exterior, chosen-operation, or path restriction.
All endpoint pairs must be admissible at the SAME j in the unchanged graph.

The experiments keep three versions separate:

* R0: no old inter-group payments are frozen. All residual negative groups
  after internal cancellation must be taken over. Any proposed old choices
  can be withdrawn; their sources then require a new assignment.
* R5: preserve the universal final E4/E5-JC-v2 ledger. Charge each source once:
  single-high canonical pair splitter, Phase13 only at global j4, unified odd
  all-splittable gap-two rule, two-high rule, ordered four-unit release.
  Use the least eligible original-graph choices. Graph-specific Q13/F35/B6
  alternative flows are NOT cumulative reservations.
* R6: R5 followed by SPACE E6-JOINT-v2, run011858Z: its eligible point,
  mixed/multiple-high and reservoir payments, skipping already-paid sources.
  This is not the different remote0144Z E6-EXIT interface. Reservoirs and
  ordered four-release can introduce more than one new vertex.

A residual ONE flow with R5/R6 preserved does not by itself give a ONE
matching of all original objects. A whole-object ONE schedule must explicitly
retire every incompatible old payment and cover ALL its source demand.
Our negative cut survives even R0, so this distinction cannot rescue it.

## 2. B7-UQ-v1: exact selected-union quotient, without symmetry assumptions

Fix an actual graph, j and any fully specified finite old ledger. Write
Z(U) for the isolated vertices of F[U], and c=2j-|U|. Every admissible group
with selected union U is obtained by choosing C as a c-subset of Z(U) and
putting D=U-C. Conversely each such choice is admissible. Hence the number
of groups is binom(|Z(U)|,c), with zero outside support. Their orientation
polynomials are identical: deleting C removes c singleton factors and leaves
all other components unchanged. Their g values and their pre-reservation
per-group demands/capacities are therefore identical.

Under (1.1), two groups with the same U have identical target neighborhoods.
After computing the actual possibly order-sensitive old payments, sum their
remaining demands/capacities by U. There is an integral feasible group flow
if and only if there is an integral feasible flow between these union nodes.
To prove the nontrivial direction, list the actual source groups in each U
with their individual remaining demands, and target groups in each V with
their individual capacities. Split each integer U-to-V flow into integer
pieces by exhausting these source and target lists. Every such group edge
is permitted, since the block U,V is complete bipartite under (1.1).
This construction respects every individual bound and exhausts every source.
The reverse direction just sums actual group flows.

No graph automorphism or invariance of canonical old payments is assumed.
This is an exact reduction, NOT a proof that Hall's inequalities hold.
A negative certificate still needs the complete allowed target neighborhood,
or a PROVED SUPERSET upper bound. An incomplete positive-operation search
is never promoted to a negative cut.

## 3. Independent recovery of E7-CUT87 and the induced F84 reduction

The actual E7-CUT87-v1 interface (run033413Z, blob
a26d1c57321fecc222ecf07f22500836b1b7d13a) was read before this reconstruction.
E supplied the F87 source mechanism; this package independently reconstructs
its graph, all coefficients, the complete hereditary base and capacity bound,
then reduces it. No replay of E7's own code is claimed.

Define H=T(a,b,c) as one central root, three adjacent hubs, and respectively
 a,b,c private two-edge paths at those hubs. All a,b,c>=1. Put S=a+b+c.
There are 2S+4 core vertices, alpha(H)=S+3, and the highest two coefficients
are
 p_(S+3)(H)=1,
 p_(S+2)(H)=b0=(2^a+a)+(2^b+b)+(2^c+c).                       (3.1)

The graph recurrence is
 I_H=product_t[(1+2x)^t+x(1+x)^t]+x(1+2x)^S,
where t ranges over a,b,c. It proves (3.1); all complete arrays are also
computed by the unchanged rooted DP and separate centroid-deletion counter.

Let F=H disjoint-union K_(1,L), with star center s and L leaves, and set
 j=S+3. Fix J to contain s, all three core hubs and every distal arm vertex.
For each nonempty subset A_i of the arms at each hub, let I contain s,
the central core root, and the proximal vertex on chosen arms, the distal
vertex on all other arms. Then |I|=j-1, |J|=j+1, and both are independent.
There are exactly

 N=(2^a-1)(2^b-1)(2^c-1)                                    (3.2)

distinct such pairs and distinct (C,D) groups. Their D graph is connected
T(|A_1|,|A_2|,|A_3|), with bipartition gap two. Its orientation polynomial
has zero central coefficient and preceding coefficient one: g=-1.
Internal cancellation pays none of these sources.

Every D-leaf is a distal arm vertex. Deleting it and its support removes
one entire two-edge arm, leaving a connected gap-two graph. Thus the high
component is UNSPLITTABLE in E4's exact sense. Primary R5 rules cannot pay it.
More strongly, EVERY unused original-graph vertex has a neighbor in C:
unused proximal vertices meet common distal tips, and unused star leaves
meet the common star center. This blocks every eligible E6 point replacement.
It also blocks both release rules: if a neighbor in C is retained, the
fresh vertex conflicts with it; if that neighbor is released, independence
of the released/fresh set fails. Multiple-high rules do not apply.
Consequently every source in (3.2) is unpaid in R0, R5 AND the specified R6.

### 3.1 ALL allowed targets are covered by an overgenerous count

No source uses any star leaf. Therefore EVERY target allowed by (1.1) for
ANY source in (3.2) uses at most ONE star leaf. Grant even more capacity:
allow every core vertex, ignore the particular source's missing core vertices,
ignore internal cancellation, and ignore ALL previous target occupancy.
Count ALL raw positive (j,j) pairs in this target SUPERSET.

If no star leaf is used, each set chooses a core j-set, or the star center
and a core (j-1)-set. There are (1+b0)^2 pairs. For one specified star leaf,
its presence in both sets contributes b0^2. Its presence in exactly one set
contributes b0(b0+1) for each of two orders. Thus

 B=(1+b0)^2+L(3b0^2+2b0).                                  (3.3)

This calculation includes the incompatibility between star center and leaf.
It also has an independent graph-count check: if A=I(H+K1), B1=I(H+K2),
then the count is A_j^2+L(B1_j^2-A_j^2). Both auxiliary actual graph arrays
are independently counted, rather than treating arbitrary polynomials as
forests. Equation (3.3) is an UPPER bound on all actual remaining capacity,
not an exact enumeration of the source-specific union of neighborhoods.
Therefore N>B proves a full-permission Hall deficiency of at least N-B,
even when all old payments can be withdrawn. No restricted subnetwork cut
is used anywhere in this argument.

### 3.2 The two certified whole-graph instances

E's instance is a=b=c=10,L=22: n87,M64,alpha55,h22,beta34,j33.
It has N=1,070,599,167 and B=644,843,761, shortage at least425,755,406.
Its first strict decrease is at k32, and its full sequence is unimodal.

The B reduction is a=9,b=c=10,L=21:

 F84=T(9,10,10) disjoint-union K_(1,21),
 n=84, M=62, alpha=53, h=21, beta=33, j=32, k=31,
 N=534,776,319, B=429,100,861,
 N-B=105,675,458 > 0.                                      (3.4)

It satisfies a GENUINE EARLIER decrease: first strict decline at30<31, and

 p30 > p31=33,534,211,151,446,546,481
     > p32=30,595,046,539,745,874,243
     > p33=25,657,020,176,639,860,373.

The complete sequence is unimodal, not an ORIGINAL counterexample. The
history, endpoints and all integers are recalculated from F84, not inherited
from F87. In the F87 labeling remove vertices20,21 (one complete arm), then
vertex86 (one star leaf). The intermediate F85 and final F84 both preserve
the full Hall cut and actual middle history. INDUCED_EMBEDDING.json supplies
the full vertex map and independently checks both induced edge sets.

An exact reduction census covers all 4,840 tuples
1<=a<=b<=c<=10, 1<=L<=22, with full arrays dual-counted. Exactly three meet
THIS cut inequality and middle/history premises; the least order in THIS
BOX is84. This is not a global minimum Hall-counterexample assertion and
not a minimal ORIGINAL counterexample. Two accepted deletion steps are
reported, not three claimed single-vertex-preserving steps.

## 4. Complete finite HEREDITARY proof for the cut instances

It is insufficient to know LOCAL. Here is the complete induced-component
classification for T(10,10,10). For each hub, either it is absent, or it is
present with a intact two-edge paths and l proximal-only leaves, a+l<=10.
There are67 branch states including absence. An unordered triple of these
states describes the component retaining the central root; there are
binom(69,3)=52,394 records. Each actual connected graph is dual-counted and
unimodal. There are103 non-LC records, so LC is not silently assumed.
Every nonroot hub component has one of66 (a,l) types, all verified LC.
Other detached components are edges or isolated vertices.

The exact number of original induced subsets represented by one absent hub
state is 4^10. A present (a,l) state has multiplicity
 binom(10,a)binom(10-a,l)2^(10-a-l).
These weights sum to2^21. Multiplying the three weights and the exact
permutation multiplicity of the unordered triple gives2^63 root-present
subsets in total. Root absence gives the other2^63. Thus all2^64 core
subsets are covered, not merely whole-vertex deletions. The records count
root components, not2^64 separate DP runs; detached edges/isolates are handled
by the following convolution argument. Every induced star is another star
plus isolated vertices; star types through22 leaves are independently LC.

For completeness, an interval-supported nonnegative LC sequence a has
 a_(l-j)a_(k-t)<=a_(k-j)a_(l-t) for k<l,j<t, including zero boundaries,
by decreasing adjacent ratios. Split a unimodal sequence's zero-padded
first differences into early gains and later losses. Convolving yields
P_l N_k<=P_k N_l; a strict earlier loss therefore forbids a later gain,
including zero terms. Hence LC times unimodal is unimodal. The same
2-by-2 minors and finite Cauchy--Binet expansion prove LC convolution.

An induced forest contains at most one component retaining the original
central root; all its other components are LC. The finite classification
and convolution proof give HEREDITARY of F87. F84 and every reduction-box
graph are induced subforests of F87, so every proper induced subforest is
also covered. All whole-graph arrays and all leaf/root conditional arrays
of F87 and F84 are independently counted as an additional check.

This establishes ALL premises of the universal HEREDITARY/middle/history
ONE proposals. It does not refute a different assertion restricted to
actual minimum BAD forests: these graphs are explicitly good.

## 5. B7-CUT-TWO-v1: exactly two fresh vertices for THIS cut family

Fix two distinct star leaves x,y. For the fixed-J source family of Section3,
put K=(I-{s}) union {x,y} and send the negative pair (I,J) to (K,K).
Since I has size j-1, K has size j. Removing the star center makes the two
leaves compatible, and the unchanged core selection remains independent.
Exactly two new union vertices are introduced. Different I give different
K; removing x,y and adding s recovers I, while J was fixed. Thus the map is
injective. The target group has D'=empty and surplus one, and none of the
pinned universal R5/R6 payments targets an empty symmetric difference.
There is no old occupancy to reuse.

Together with (3.4), this proves that the least allowance for this SPECIFIC
source collection is exactly two, in the raw or pinned residual schedules.
It is NOT a complete matching for every negative pair of F84 or F87, and
not a universal two-new-vertex theorem. No artificial slack objects are used.

## 6. F21 and two connected21-point graphs: positive full-source certificates

The old SPACE E6 F21 graph has the13-point four-arm length-three spider,
an isolated vertex13, common vertex14, six neighbors15..20, and edge0--15.
At j8 its group C={14},D={0,...,13} has no E6 point/release entrance.
This fact alone never established a Hall deficit.

B7 enumerates every possible U and C in the exact quotient of Section2.
An independent literal enumeration of ALL ordered rank(8,8)/(7,9) pairs
agrees with every quotient row and checks omitted zero-object rows.
Every actual negative group's canonical R5/R6 payments are independently
recomputed using the recovered original E6 Python rules; all target loads
are summed before subtraction. Reservoir nonentry is established by its
actual size bound or exhaustive actual choices, not a heuristic failure.

A positive integral union flow is lifted explicitly to actual C,D groups,
with every source demand and every used target bound checked. The flow
uses a SUBNETWORK of (1.1). It is not claimed to enumerate all permitted
edges, and its existence needs no such enumeration. F21 has a full R0
ZERO-new-vertex matching. Its blocked source is actually sent to
 C'={10,12,13}, D'={1,2,3,4,5,6,7,8,9,14},
encoded as C'=13312,D'=17406 in the exact certificate. The stored masks,
not this displayed set expansion, are authoritative and directly checked.
It changes the common selection, with no new union vertex. In particular
this source's structural nonentry is not a full endpoint Hall obstruction.

Two connected new variants add edge13--0 or13--2, respectively. All three
graphs have complete2^21 induced-subset zeta/deletion certificates, with
zero nonunimodal induced subsets. Their j8 histories and whole polynomials
are retained. R0/R5/R6 demands are respectively:

 F21:       1,215,031 / 50,076 / 49,494,
 C21_v0:    1,302,056 /    224 /     11,
 C21_v2:      959,442 / 99,576 / 74,497.

All are paid. These are three graphs and nine ledger cases, not nine graphs.
The incomplete greedy ZERO subnetworks for F21 R5/R6 are explicitly retained
as unsuccessful algorithms, NOT full-permission negative cuts. R0 has no
frozen old payments; R5/R6 positive residual flows do not retire any payment
unless a separate complete takeover schedule is stated.

## 7. A new connected35-point whole-object ONE instance

This is NOT the old disconnected F35. Start with T26 and append bridge27,
hub26 and leaves28..34, with edges0--27--26 and26--i for28<=i<=34.
The complete tree has n35,M35,alpha22,h9,beta14,j13, and
 p12=19,708,924 > p13=16,550,937 > p14=11,091,783.
It contains the actual induced T26, so the old2979>2601 source-set argument
rules out any whole-object ZERO-new matching, regardless of old reservations.

The E6 orbit generator and independent auditor were adapted to retain the
new connecting edge. There is NO pruning that assumes a disconnected core.
The exact graph automorphism group consists of arm permutations, swapping
the equal four-arm branches, and seven exterior leaf permutations; its
order is34,836,480. Exhaustive status-multiset enumeration gives all groups,
and its complete weighted positive/negative totals agree with the actual
whole p13^2 and p12*p14. Source completeness is proved by the status-multiset
bijection, not just this aggregate equality.

After primary E4/E5 pair-normalization payments, keep a SUPER-demand including
sources that the ordered four-release may already have paid. It consists
of129,178 source orbits,1,858,229,877 actual group occurrences, with total
weighted demand4,253,107,121. The certificate pays all of it. On118,233 USED
target orbits it checks

 capacity       113,109,333,156,
 old envelope       565,656,312,
 new flow         4,253,107,121,
 unused balance 108,290,569,723.

The old envelope counts all valid inverse centers without the canonical
restriction, and conservatively reserves the whole capacity of a possible
ordered-release target. It is an invariant UPPER bound, not an assumption
that the order-sensitive old matching is itself invariant. The independent
auditor checks all source rows, target rows, original-graph operation witnesses,
colored-tree stabilizers and all35 possible inverse centers per used target.

For clarity, a quotient edge has an actual endpoint-operation witness. Its
full automorphism orbit is biregular on the source/target vertex orbits.
Spreading its integer quotient flow uniformly over this edge orbit gives
a fractional actual-group flow with correct per-group margins. All actual
group demands and capacities are integer. The finite augmenting-path/min-cut
argument converts the feasible fractional flow to an integral group flow;
rank selection among the available ordered objects realizes an injection.
The upper envelope leaves sufficient capacity at EVERY actual target even
if canonical old occupancy varies inside its orbit. No billions-of-pairs
literal enumeration or explicit integral object list is claimed.

There are TWO alternative schedules. R5 keeps ordered four-release payments
and drops the already-paid portion of the super-flow. To obtain a full
ONE matching, retire those four-release payments and retain the ENTIRE
super-flow, including all retired sources; leave their former target slots
reserved and unused. Retained primary pair normalizations introduce no new
vertex. Internal rank matches also introduce none. The new operations add
at most one vertex. This proves a whole-object ONE schedule, hence R0
feasibility. It is not the sum of two concurrent schedules. No R6 extension
for this connected35 instance was tested or claimed.

HEREDITARY is established independently by28,160 root-component records:
2,816 exact retained-core profiles times10 possible connected exterior states
(bridge absent, bridge alone, or bridge/hub with0..7 leaves). Every root
component is unimodal by two graph algorithms. Nonroot hub/star components
are LC. The Section4 convolution lemma completes the induced-forest proof.
Thus this is a full-premise connected instance whose least whole-object
fresh-vertex allowance is exactly one, distinct from both F21 and F84.

## 8. All roots, all leaves, peer gates and original problem

The final material deck includes F21, the two connected21 graphs, connected35,
T26 with an attached16-vertex path (42vertices), F87 and F84. The42-point
HEREDITARY proof uses47,872 complete connected induced root/path-prefix
records and LC detached path/hub components. Its middle k13 has true earlier
decline at12. All material root and leaf arrays are dual-counted; F21 has an
isolate and is excluded from the ADMC domain, while the disconnected Hall
graphs are not assigned the connected-tree A4-R premise.

Two new fixed68-point searches retain full root envelopes and full leaf
minima at actual middle indices. They find neither all-root nor all-leaf
failure. Ordinary larger edited graphs remain HEREDITARY UNKNOWN. All whole
sequences are independently counted and checked across platforms. Negative
conditions are not discarded by filtering nonunimodal conditional forests.

The actual published D7-NEW-LOCAL-v1 was tested on119 leaf-addition transitions.
No surviving old witness was lost, so the new rule's QUALIFYING-premise count
is ZERO, not119 successful implication tests. D7-MIN-RSM has zero actual
minimum-bad/valley instances. C7's four gates and exact loss identities were
checked on eight ordered split/position instances; two T26+T26 cases meet
its primary no-LC-proper-subunion domain. The six Hall-graph controls have an
LC star factor and are NOT in that narrower domain. No gate failed.
A7-R retains A4-R's existing quantifiers. The distinct A7 large pendant-path
length gate was NOT tested by these short-path material graphs.

No all-root, all-leaf, middle negative-LC/C1, history plateau, e>d under
middle History or whole-sequence valley was found. The full ONE capacity
proposal, in contrast, is REFUTED on the actual full-premise graphs above.
The first open ORIGINAL step remains a true middle no-rebound argument or
a legal forest valley, possibly via root/leaf existence or a less restrictive
capacity/signed-slack route. The ONE failure does not settle those alternatives.
