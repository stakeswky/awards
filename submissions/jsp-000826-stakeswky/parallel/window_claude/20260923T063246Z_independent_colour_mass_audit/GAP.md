# Gaps and first unproved arrows

ORIGINAL=NOT_CLOSED. No legal non-unimodal forest was found. This run adds no new
unconditional forest order or family to the covered range.

## First unproved arrow for each route touched here

| Route | Proved or checked | First unproved step |
|---|---|---|
| D\* (trees, all History positions) | Constant 1 is sharp (Lemma 2); no failure for n<=19 or in the families | A structural inequality X <= b(a-c) for general trees, where X = sum_t max(P_t-N_t,0) |
| D\*_mid (automatic colour-mass entrance) | No failure for n<=23 or in the families | Same inequality restricted to h+1<=j<beta; no constant c<1 is proved |
| C\*_mid (one leaf edge controls every cut) | No failure for n<=23 | Existence of one leaf edge e with delta_e<=S for every tree; not attempted as a proof here |
| Forest version | Not tested | Must quantify over per-component colourings; the product/convolution step is unproved |

## Coverage limits of the computations

- The exhaustive middle-range sweep stops at n=23. n=24 (39,299,897 trees) was started in an
  exploratory session and deliberately stopped; it is not reported as covered.
- The all-position D\* sweep stops at n=19.
- No middle-range plateau (S=0 after an earlier strict descent) occurred in any tested set, so
  the plateau case has **no** empirical test here. Yet it is the most delicate case: there
  Dmass=0 exactly, or some delta_e=0, is required.
- Families are finite parameter windows (listed in STATEMENT.md). They are not limits.
- HEREDITARY is not established for family trees with n>=30. For the n<=23 trees it holds
  conditionally, via the project's component-order-30 exclusion and Reynolds' n<=29
  enumeration. The propositions tested do not require H; a failure would need H checked
  before being used against H-conditional versions.

## Evidence-level limits

- **Implementation.** New independent implementation, not an author-program replay. Material
  computations are cross-checked by second algorithms: literal enumeration, Edmonds–Karp
  max-flow, and the project's own coordinator polynomial code (see REVIEW.md).
- **Review.** This is a cross-model check (Anthropic Claude; the project windows used OpenAI
  ChatGPT), not an independent human or external peer review.
- **Not reviewed.** The A9 written proof (2^2600000 cutoff) was not in the hand-off package
  and was not reviewed here.
- **Lean.** Not run. The external FLNYZ Lean repository was not built, and no axiom audit was
  performed.
- **Replay.** The clean-source replay covers sweep orders n<=21 plus every other step, byte
  for byte. Orders n=22 and n=23 come from the single primary run. An earlier exploratory run
  with pre-release scripts reported identical aggregate counts for them (see
  provenance/EXPLORATORY_RUN.json); that is a repeated execution, not a byte-level replay.
