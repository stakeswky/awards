# Round7 exact statements and verdicts

Run `20260921T033413Z_round7_global_one_new`. All graphs are finite simple undirected unweighted forests. Independent-set counts are zero padded; unimodality permits plateaus. ORIGINAL is still NOT_CLOSED.

## E7-ONE-v1 — REFUTED, fixed universal old ledger

Use the exact five-rule L7 and canonical ranking of PROOF section 1. Internally cancel each group once; pay each old source at most once; retain every target's total old incoming load. No E6 or graph-specific alternative flow is included.

Claim tested: for EVERY HEREDITARY forest F and EVERY j with h+1<=j<beta and History(F,j-1), the residual network of ALL unpaid negative (C,D) groups and ALL positive remaining target groups admits a saturating flow when the ONLY edge restriction is

    |(C' union D') minus (C union D)| <= 1.

C may change freely. The vertex set and all edges of F are fixed. HEREDITARY means all proper induced subforests are unimodal, not merely LOCAL. The exact middle boundaries and History definition are those in PROOF section 2. This universal claim is FALSE.

## E7-CUT87-v2 — PROVED with finite complete HEREDITARY certificate

Let F=T_10 disjoint-union K_(1,22), with the explicit 87-vertex labeled edge list in F87_HALL_CUT.json, and j=33. It satisfies HEREDITARY, h22, beta34, first strict descent at k32, and whole unimodality. Its source set S is specified in PROOF section 4.

Every source in S is L7-unpaid, each with deficit one. Demand(S)=1070599167. Every permitted target is in the exact over-set of positive (33,33) pairs with at most one star leaf. That over-set has cardinality 644843761, BEFORE any internal or old occupancy subtraction. Thus actual available capacity is deficient by at least 425755406. This is a bound on a FULL-relation cut, not an optimized exact minimum-cut value and not a smaller-operation negative test.

The same cut survives the separately defined ledger which subsequently adds final E6-JOINT-v2 universal payments, since those rules cannot pay any S source. See PROOF section 6.1. This is not conflated with a claim that mixed old payments all obey one-new permission.

## E7-TWO-S-v1 — PROVED, source-set scope only

For ALL sources (I,J) of this S, fix the first two star leaves z1,z2 and map to (K,K), with K=(I-{star center}) union {z1,z2}. This is an actual simultaneous injection with exactly two new union vertices, distinct diagonal targets and zero L7 old occupancy at every such target. The minimum uniform allowance for THIS source set is exactly two.

No full F87 two-new matching is asserted. No universal two-new theorem is asserted.

## E7-FAMILY-v1 — PROVED, unbounded structural capacity statement

For every integer s>=10, the analogous source family in T_s disjoint-union K_(1,2s+2) at j=3s+3 violates the complete one-new capacity relation by the written exponential-versus-quadratic bound in PROOF section 10. The displayed numerical middle range holds for all s. HEREDITARY and History for all s are NOT asserted: the fully qualified original candidate refutation is s=10 only.

## Preserved boundaries

E4-S, E5-JC-v2, the final E6-JOINT-v2 theorem, and Phase13 L4 are not refuted. The F35 full one-new certificate remains valid and was audited. General middle LC itself is not refuted: L33(F87)>0. Neither ORIGINAL nor the restriction of one-new Hall to actual minimum BAD forests is refuted. No claim of external review, global novelty, Lean or axiom audit.
