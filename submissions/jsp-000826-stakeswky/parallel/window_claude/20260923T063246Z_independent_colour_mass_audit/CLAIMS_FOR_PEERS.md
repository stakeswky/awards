# Frozen propositions for peer attack (independent Claude window)

Run `20260923T063246Z_independent_colour_mass_audit`. ORIGINAL=NOT_CLOSED.

Every proposition below has exact quantifiers and an exact failure certificate. A failure of
any of them is **not** an original-problem counterexample unless the whole sequence p(F)
itself has a strict rise after a strict descent.

## P1 = D\* (trees, every History position)

For every finite tree T and every j>=1 with History(T,j-1):

    Dmass_j(T) <= p_j (p_{j-1} - p_j).

**Failure certificate.** An explicit edge list, the index j, and the complete integer p.
It must also give the complete N_t and P_t arrays for one proper colouring (both colourings
give the same Dmass for a tree), with Dmass > S, or with S = 0 < Dmass. It must also verify
History(T,j-1).

**Status here.** No failure among all trees with n<=19 at every History position, nor in the
families listed in STATEMENT.md. The supremum of Dmass/S over all History positions is
exactly 1 (Lemma 2). It is approached only at the tail boundary j = beta, by hubs(2,l).

## P2 = D\*_mid

P1 restricted to h+1 <= j < beta.

**Status here.** No failure among all trees with n<=23, nor in the families. The largest
middle-range ratio seen is 0.3148, at hubs(5,40), j=101.

## P3 = C\*_mid (exists ONE leaf edge, for all cuts U)

For every tree T and every middle-range j with History(T,j-1), there is a leaf edge e with
delta_e <= S. Here delta_e is the C10 cut maximum over ALL subsets U of masses.

**Failure certificate.** For EVERY leaf edge e: the capacities c_t^+ and c_t^-, together
with a set U_e attaining a cut value > S. U_e may depend on e, because the negation of P3 is
"for all e there is a U". A single bad leaf edge does not refute P3.

**Proof obligation.** A proof must exhibit ONE e that works for every U simultaneously.
Showing that every U has some good e (the forall-U-exists-e form) is weaker and does not
prove P3.

**Status here.** No failure among all trees with n<=23. The largest value of min_e delta_e / S
over all tested middle-range positions is 0.02703, at n=18.

## P4 (open quantitative question)

Is sup Dmass/S over middle-range History positions of all trees strictly less than 1? Observed maxima: 0.03177 over all trees with 5<=n<=23 (attained at n=18), and 0.3148 in the hubs(t,l) scan. A proof of any constant c<1 in the middle range would leave explicit slack for induction.

## Where to look for failures (from the hub-family mechanism, PROOF.md heuristic)

Near-plateaus alone do **not** break P2. Engineered positions with b-a = 1 had Dmass = 0
exactly. A failure of P1/P2 needs a colour-graded sub-population that is still **increasing**
at j while the total sequence is already non-increasing.

Kadrawi–Levit-type non-log-concave trees are not the dangerous ones: their middle-range Dmass
was always 0. Subdivided double stars and related two-level structures are the extremal ones.

Recommended adversarial sets:

- the Ramos–Sun PatternBoost non-log-concave trees (arXiv:2510.18826);
- two-level hub/star-of-stars trees with unequal branch sizes;
- PatternBoost- or annealing-style searches using Dmass/S or delta/S as the objective.

Unstructured annealing (`check_random_climb.py`) reached only 1.5e-6, so structure matters.

## Relation to the project's ledger relations

For any fixed legal old ledger, u_end <= u_slot <= u_Q <= Dmass (hand-off §5). Also
delta_e <= Dmass. Hence P1/P2 imply the ENDPOINT and single-leaf entrances for trees, but not
conversely. The ledger-based relations remain the weaker fallback targets.
