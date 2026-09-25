# Window E Round 6: exterior-changing interfaces v1

ORIGINAL=NOT_CLOSED. This is an early interface, not a peer-review receipt.
The actual starting head is e9d5986c1c3216465f4cc8608db2ddad08e31d9c.
The E5 final v2 proof has been read. All eight E5 RUN_ALL outputs were freshly
replayed and compared byte-for-byte, separately from new Round-6 work.

## Objects and the fixed old ledger

F is a finite simple unweighted forest, j>=0. A group (C,D) is admissible when
C is independent, C and D are disjoint and nonadjacent in F, and
2|C|+|D|=2j. Its signed count g(D) is the central-minus-preceding coefficient
of the actual bipartition-orientation polynomial. First cancel objects inside
each group. Pay each old negative source ONCE using E4, Phase13 (j=4 only),
E5 generalized-gap-two, E5 two-high and E5 four-unit release rules in that
order, skipping already paid sources. Fix lexicographic choices in the old
rules. Capacities are g(D)>0 minus ALL these old payments, never reset to g(D).
The scoped Q13 extra flow is used only on its exact published inputs and must
be included in a certificate whenever those inputs are tested.

## E6-ONE-v1: full one-new-vertex relation (UNPROVED candidate)

For every HEREDITARY F and j with h+1<=j<beta and History(F,j-1), form a
bipartite capacity network. Left nodes are ALL remaining negative groups,
with demand -g(D). Right nodes are ALL actual positive groups with remaining
old-ledger capacity. An edge (C,D)->(C',D') exists exactly when

  |(C' union D') minus (C union D)| <= 1.

Both endpoints must be admissible at the SAME j in the unchanged F. There is
NO C-growing, union-shrinking, greedy-path or frozen-exterior requirement.
Question: does this network always saturate the left demand?

A refutation must give an actual full-premise graph and an exact deficient
cut including ALL targets permitted by this relation and their prior loads.
Failure of a smaller operation network is not a refutation. A deficiency
refutes only this stronger capacity route; it refutes ORIGINAL only if the
complete coefficient sequence also has a strict descent followed by a rise.
A proof would imply L_j>=0 and exclude a minimum counterexample's first rise.
Neither this full Hall bound nor the existence of an appropriate slack-object
reserve for the weaker no-rebound inequality is asserted.

## E6-EXIT-v1: one-new-vertex exits (proposed scoped theorem under audit)

Fix an actual vertex labeling and a public partial function phi(x)=w. Consider
negative groups having an odd number t of gap-two high components, no unit
components, arbitrary balanced components, and at least one unsplittable high
component. For EACH high component use its E5 canonical splitting-leaf repair
if it is splittable. Otherwise require a majority-side leaf w in that component
Q and an UNUSED actual x compatible with C and D-w, with either:

(SLIDE) x is adjacent to w in F; or
(TAG) phi(x)=w and no vertex of F is adjacent both to x and to any vertex of Q-w.

Choose one eligible exit canonically per unsplittable Q. The new operation is
(C,D)->(C,D-w+x); it introduces exactly ONE vertex. The old splitting operation
introduces none. With b balanced components and t=2s+1, send 2^b Cat_s to each
of the t resulting targets. Its total equals 2^b binom(t,s), the source demand.
Skip every source already paid by the fixed old ledger.

Proposed inverse proof: the new target has exactly two unit components, one
nontrivial Q-w and the singleton x. For SLIDE, their unique connecting vertex
recovers w and has NO C-neighbor; for TAG there is no connector and phi recovers
w. Old single/gap-two normalization into that target would require a connector
with exactly one C-neighbor, so its old load is zero. Old two-high/release and
Phase13 targets have different signatures. Splitting targets from the new
sources retain an unsplittable high component and cannot have an old all-
splittable source. Forest acyclicity controls inverse uniqueness. The final
proof must check every collision, including between SLIDE, TAG and splitting.

Tests should report source overlap, actual used x, every reverse center,
remaining old capacity and total load; per-source legality is insufficient.
The exit condition is NOT claimed to follow from HEREDITARY or history.

## Scope and next evidence

T26+P3+6 isolated vertices is a required whole-graph exterior control. A detail
that must not be lost: once E5 release is fully instantiated, many of the 1575
post-E4 fiber sources are ALREADY paid. A new one-point alternative for all
1575 may not be counted as 1575 additional payments. Exact incremental and
alternative ledgers will be delivered separately.

Sources: mounted E5 final v2 PROOF SHA256
8f72f2bf5d9a7aecbc8a1f3f85afb9493052df041d8770686072fedd6daca129;
v2 interface SHA256 cd97187d75f5e6268fe6537c2c2e2ea03b428d2549a89a966f1dea57856237c1.
No independent review, Lean build, axiom audit or novelty claim.
