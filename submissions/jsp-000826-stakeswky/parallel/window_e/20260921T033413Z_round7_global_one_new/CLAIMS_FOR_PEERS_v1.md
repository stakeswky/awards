# E7-ONE / E7-CUT87: full one-new-vertex Hall test

Run 20260921T033413Z_round7_global_one_new. ORIGINAL=NOT_CLOSED.
This is an early interface; final proof, source and certificates follow in
this same directory. No peer receipt, external review or novelty is claimed.

## Fixed universal old ledger L7

All graphs are finite simple undirected unweighted forests with ordered
vertices. For each j, group ordered pairs by C=intersection,D=symmetric
difference, retaining actual C independence, C-D nonadjacency and
2|C|+|D|=2j. Cancel positive/negative objects in each group once by pair rank.
The remaining signed count is g(D), with BOTH orientations of balanced blocks.

Pay each negative source at most once, using the first applicable rule:
(1) E4 single-high canonical pair splitter; (2) Phase13 Q7+unit at j=4 only;
(3) the unified E4/E5 odd all-splittable-gap-two rule, splitting its demand
equally over its high blocks; (4) E5 two-high rule, gap2 plus splittable
higher gap; (5) E5 ordered four-unit release. Use the least eligible (v,w)
splitting pair in lexicographic order in (1),(3),(4). In (5), use the least
ordered quadruple W=a<b<c<d with a,b in C and c,d unused, W independent,
W nonadjacent to D and C-{a,b}, and no graph vertex adjacent to all of W.
The output is (C-{a,b},D union W). All old incoming payments at a target
are subtracted ONCE from g(target). No E6-JOINT, Q13/F35 alternative or B
fiber flow is added to L7. Its targets may have more than one new vertex.

## E7-ONE-v1: universal candidate, REFUTED by the cut below

For EVERY HEREDITARY forest F and j with h+1<=j<beta and History(F,j-1),
does the following residual network saturate ALL unpaid negative demand?
The left nodes are all L7-unpaid negative groups. The right nodes are all
actual positive groups, with capacity g minus their total L7 occupancy.
A source (C,D) may use a target (C',D') if and only if both are admissible
at j and |(C' union D') minus (C union D)|<=1. No other restriction is made.
Intersections and all old selected vertices may change freely.

## E7-CUT87-v1: a full-relation deficiency (written proof + finite HEREDITARY base)

Let H=T10: root0, hubs1,22,43, each with ten private two-edge arms. Precisely,
for h in {1,22,43} and i=0..9 use edges (0,h),(h,h+1+2i),(h+1+2i,h+2+2i),
with (0,h) included once. Append a DISJOINT star with center64 and leaves
65..86. This actual F has n87,alpha55,M64,h22,beta34; take j33.
Its full sequence is unimodal (but not LC), with
p32=198034727289347440603 > p33=183777727271711047953
 > p34=157309573857110318672. The first decline is at k32.

Fix J to contain center64, all three H hubs and all thirty distal arm leaves.
For EACH triple of nonempty arm subsets A1,A2,A3 choose I to contain center64,
root0, and the proximal vertex of each arm in Ai, otherwise its distal vertex.
Then |I|32,|J|34. Each group has g=-1 and D is T(a1,a2,a3), ai>=1: a single
UNSPLITTABLE gap2 block, with no units. There are (2^10-1)^3=1070599167 such
unpaid groups. They are distinct and internal cancellation pays none.
No primary L7 rule applies. Four-unit release cannot apply: J is a maximal
independent set of the WHOLE F, so every unused vertex has a neighbor in J;
the release requires unused vertices nonadjacent to the entire source union.

EVERY permitted positive target for this entire source set uses at most ONE
star leaf, because no source uses any star leaf. Grant an even larger target
set: ALL independent (33,33) pairs with at most one star leaf, ignoring
source-specific missing core vertices, internal cancellation AND all old
occupancy. This is a SUPERSET capacity relaxation, not a smaller network.
With b=p32(H)=3102 and a=p33(H)=1 its exact cardinality is

  (a+b)^2 + 22*(3*b^2+2*a*b) = 644843761.

The first term uses no star leaf. For a specified leaf, its common placement
contributes b^2; each of its two single placements contributes b^2+ab.
This accounts for center64, including its incompatibility with the leaf.
Thus even this overgenerous capacity is short by 425755406. Actual residual
capacity is no larger. No amount of new permission to change C inside the
stated ONE-new endpoint relation fixes this deficient source set.
This is NOT an original counterexample and does not refute a statement
restricted to actual minimum BAD forests.

HEREDITARY is separately certified, not inferred from LOCAL: 52394 central
component states and 66 branch states are counted by an explicit graph
formula and independent vertex deletion. All central states are unimodal,
all branch states LC. Exact multiplicities cover all 2^64 H-vertex subsets.
All omitted components are K1/K2. Every induced star is LC, and the proved
LC-times-unimodal lemma supplies every induced subforest of F. The finite
certificate has passed locally; its full rows and source will be delivered.

## To B / exact audit request

Check the source family, its unpaid status under FULL L7, the all-target
superset count, and the HEREDITARY compression. The cut does not require
enumerating billions of edges: the displayed upper bound already exceeds
every actual permissible target capacity. A positive flow in a restricted
source subfamily would not refute this cut. Check whole P separately.
The R6 F35 all-row auditor has just been rerun and its output matched; that
positive graph and this negative graph have different scopes.
