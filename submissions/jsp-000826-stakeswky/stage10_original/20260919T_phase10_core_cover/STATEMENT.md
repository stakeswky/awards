# Phase 10: result and boundaries

**ORIGINAL: NOT_CLOSED. Unrestricted BARRIER: UNPROVED.**
**New scoped result: an arbitrary-core private-arm unimodality theorem.**
It is a real sufficient theorem for whole forests, including certain products
of arbitrarily many non-LC large components, not a theorem for all forests.

Let C be a finite core on q>=1 vertices and H a nonempty vertex cover of size
h. Let r=q-h. At each v in H attach a_v private two-edge paths, and write
M=sum a_v and a=min a_v. C may have arbitrary shape and arbitrary component
count; if it is a forest, the completed graph is an unweighted forest.

PROOF.md proves that the full sequence is unimodal if

    a>=24, M>=24q,
    2*5^r*(M+r+1)^(r+1)*[(1+(3/2)*2^(-floor(a/6)))^h-1] < 1.

The proof keeps the actual core and every exterior vertex; it controls each
middle-range coefficient relative to Q=(1+x)^r(1+2x)^M, including a rigorous
lower bound for every nonzero baseline difference. It covers early growth,
the entire middle, and the known Basit--Galvin decreasing tail. It does not
assume that the completed polynomial or its root-absent part is unimodal.

A uniform sufficient corollary is ALL equal integer a>=192(q+1)^2, for every
q, core shape and cover. Hence t disjoint T(a,a,a) trees are unimodal for
ALL t>=1 and a>=192(4t+1)^2. Each component in that range is provably non-LC.
This does not assume general closure of unimodality under multiplication.
The constants are not optimized; smaller parameters can meet the first test.

Arbitrary *uncoated* attachments remain outside the theorem unless the cover
and all hypotheses are rechecked on the completed graph. No argument shows
that every hypothetical minimal counterexample belongs to the new class.

The finite search did not impose these arm hypotheses. It produced 233
within-run distinct forests, all absent from the supplied 21,756-type
Phase7/8/9 inventory. Thirty were free-core seeds; 101 arose by whole-subtree
relocation; 54 had one/two-site attached exteriors; 48 combined 2..7 actually
non-LC large components. Maximum search order was 535. All 1,240 middle
weak-descent tests passed; no prefix failure, true valley or U/D residual pair.
Every P was dual-recounted, every vertex A/B computed (83,710 arrays); 12
materials had 5,920 A/B and 2,930 edge-neighborhood independent recounts.
HEREDITARY stays UNKNOWN. This is not an order census or all-shape coverage.

Four separate theorem controls have three full counting checks each, with
maximum order 4,616. That largest control has two non-LC components of order
2,308 each. Those four are not added as disjoint new search coverage; no
all-vertex A/B recount is claimed for them. Exact root/size-allocation mixture
identities are checked in five materials, with 10,626 literal subset/root
controls. These identities are not a universal variance bound.

Fresh clean replay: six programs, ten complete output files compared using
all bytes; no fields excluded. Source, data and logs accompany the delivery.
No full ORIGINAL proof, counterexample, global minimum, fresh Lean build,
axiom audit, independent external review or priority claim. Previous work,
external census dependencies and the 247-small-index-only limit are retained.
