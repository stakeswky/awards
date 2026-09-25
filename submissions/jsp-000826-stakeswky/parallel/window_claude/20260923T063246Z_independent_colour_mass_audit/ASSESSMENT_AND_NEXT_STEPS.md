# Independent assessment of the project state and proposed next steps

Written by an independent Claude window from the 2026-09-23 hand-off package (Round-10
baseline; Round-11 tasks assigned, no Round-11 results) and the branch head `af71b798`.
These are recommendations, not decisions. ORIGINAL=NOT_CLOSED.

## 1. Summary judgement

- The hand-off package describes its own status accurately. No overclaim was found. Its
  evidence-level and quantifier discipline is strong.
- **Periphery solid, core unmoved.** Restricted families and conditional tools keep
  accumulating. The core question has not narrowed since Round 4: in the middle range, after a
  real descent, why can there be no rise?
- **Entrance criterion changed four times.** The successive criteria were: complete one-point
  permission, then Dmass, then delta_e, then the ENDPOINT deficit u_end. Each successor is
  weaker (u_end <= u_slot <= u_Q <= Dmass; delta_e <= Dmass). None is proved for general
  forests.
- **Consequence.** Retreating to ever weaker ledger relations does not by itself supply the
  missing structural inequality.

## 2. Result-by-result view

| Result | Assessment |
|---|---|
| A9 explicit cutoff 2^2600000 | Genuinely new relative to FLNYZ, whose Theorem 1.1 is existential (verified in the arXiv HTML). It rests on a same-model audit only (D10). The whole cutoff comes from one error term, 2^154·n^(-1/15992). Even a rate n^(-1/2) with constant 2^20 would still require n > 10^17, while exhaustive enumeration reaches n<=29 (Reynolds, Zenodo 19100781) or perhaps 32 (a forum claim, unverified). So lowering the cutoff cannot close the problem |
| Restricted families (B59, 280 types, components <=30, C6-P4, A7 long paths, four-type closure) | Real and useful for constraining a minimal counterexample; narrow |
| Front "increasing through ceil(n/4)" | Overlaps FLNYZ Proposition 8.2 and should cite it. The M-dependent h refines it. beta is Basit–Galvin Theorem 1.3, which the project already cites |
| Global L3/L4 | Real, local |
| Dmass, delta_e, u_end criteria | Exact, well-defined sufficient conditions with correct conditional theorems. No general entrance |
| Refutations of over-strong claims | Valuable negative knowledge |

## 3. New evidence from this run (details in STATEMENT/PROOF/results)

- **No failures.** The strongest colour-mass entrance, Dmass <= S (D\*_mid), and the
  single-leaf entrance (C\*_mid) survived every tree with n<=23. That is 8,586,082 middle-range
  History positions.
- **Beyond the middle range.** D\* also survived every History position of every tree with
  n<=19, including tails, and all tested families.
- **Sharp constant.** The ratio Dmass/S has supremum exactly 1 over History positions (Lemma 2,
  hubs(2,l)). The extremal positions all sit at the tail boundary j = beta. The middle-range
  maximum observed is 0.3148.
- **Near-ties do not break Dmass <= S.** Positions with b-a = 1 have Dmass = 0 exactly. Heuristic
  mechanism: a positive colour part can exceed S only if a colour-graded sub-population is still
  increasing at j while the total is not.
- **Non-log-concave trees are harmless here.** Kadrawi–Levit-type non-LC trees had Dmass = 0 at
  every middle-range position.

## 4. Proposed priorities

### P0 — cheap, high value

1. **Build the external Lean project.** Build junwei-lu/Erdos_993_Tree_Independent_Set_Unimodality
   (Lean v4.29.1) on a machine that has Lean, run the axiom check, and record statement
   correspondence. The ChatGPT sandbox has no Lean, which is why every round logged NOT_RUN.
2. **Adopt a lemma harness.** Every new entrance proposition should pass exhaustive trees
   (n<=23 here), structured families, and the Ramos–Sun non-LC trees before a round is spent
   proving it. `src/` of this run is a starting point.
3. **Commit raw outputs every round.** Author-program replays have been 0 in every recent round
   because archives could not be materialized. Each window should commit its raw outputs and
   sources to its own parallel directory before finishing.

### P1 — mathematics

| Window | Proposal |
|---|---|
| C+E (merge) | Make D\* (or D\*_mid) the organising target. Prove it first on closed-form classes (hubs(t,l), star-of-stars, caterpillars, spiders), guided by the sharp family hubs(2,l). Then look for a general "colour-graded sub-population" decomposition in which mixed second differences are dominated by each sub-population's own descent. Keep the ledger relations as fallbacks |
| B | Stop near-plateau attacks on Dmass (shown ineffective). Search specifically for a colour-graded sub-population that still increases at j while the total does not. Use PatternBoost or annealing with Dmass/S and delta/S as objectives. Test the Ramos–Sun trees and multi-component forests (every colouring) |
| A | Stop lowering the cutoff for closure purposes (quantified above). Write A9 as a standalone note for external review. If the analytic line continues, target a colour-graded (bivariate) local limit theorem giving D\* for large n, the analogue of FLNYZ Theorem 1.2 |
| D | Replace same-model re-audits with an actual Lean build, plus cross-model or human review of A9 |

### P2 — positioning

- Cite FLNYZ Proposition 8.2 for the ceil(n/4) front.
- Record which external enumeration the component-order-30 closure depends on. The public record
  verified here is Reynolds, n<=29.
- Possible write-ups: the A9 effective-constant note (coordinate with FLNYZ), and D\* together
  with the sharp family and the computational evidence.

## 5. Provenance note on the external theorem

The FLNYZ paper states that "The Odin Automatic AI Research Agent was used to find the initial
proof". The erdosproblems.com proof-claim thread (not re-read here) was reported by a
sub-agent to mention ChatGPT-6. If attribution matters for any award-related decision, this
discrepancy should be resolved from primary sources. This run makes no award, priority or
eligibility claim.
