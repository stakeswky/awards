# Self-review and second implementations

What was checked, how, and what could still be wrong.

## Correctness of the computation pipeline

| Component | Primary method | Second method / check | Coverage |
|---|---|---|---|
| Free trees | WROM level-sequence generator | Counts equal OEIS A000055; pairwise non-isomorphism via AHU canonical forms rooted at the centre(s) | Counts n<=23 (the sweep asserts them in the receipt); non-isomorphism n<=12 |
| Bivariate counts f_r(l) | Rooted DP with Kronecker big-integer packing. Carry-free: every coefficient is at most 2^n, below 2^W with W=n+2 bits per slot | Literal enumeration of all independent sets | Every tree n<=12 (986 trees, 7,911 rows) |
| Same | Same | Project coordinator code `third_party/graph_primitives.py`: dict-based rooted recursion, and vertex-deletion recursion for n<=16 | Deterministic sample of middle-range trees, n=14..20 |
| Leaf capacities c_t^+/c_t^- | Formula from K=F-{u,v} and J=F-N[v] | Literal enumeration of source pairs. Every image is checked to be a valid target, the images are injective across both exchange types, and each exchange moves mass by exactly 1 | Every tree n<=10, every j, every leaf |
| delta_e | Two-state cut DP over masses | Edmonds–Karp max-flow on the aggregated mass network | The same small cases, plus every leaf of the sampled middle-range positions |
| Published values | This implementation | Assertions against the hand-off/C10 numbers for F14, G25, T26 and F56 | All four reproduced exactly |
| hubs(2,l) closed form | DP values | Exact rational identity from Lemma 2 | l=3..80 |

All comparisons are exact integer or `Fraction` comparisons. Floats appear only in printed
summaries.

## Conventions that could silently change results

- **Colour class.** L is the class of the root. For trees Dmass is invariant under the global
  swap. Forests would need every per-component colouring and are not tested.
- **History.** Implemented as: a strict descent at some i<=j-1, and no rise from i to j. For the
  tested (unimodal) trees this is exactly j-1 >= first strict descent.
- **Middle range.** h+1<=j<beta with M=n for trees. The boundary claims used here (strict
  increase through h, no rise from beta on) were re-checked on every tree n<=20. These checks
  are not proofs.
- **Plateau handling.** S=0 counts as a violation whenever Dmass>0, or whenever every
  delta_e>0. No such position occurred.

## Reproducibility

- `src/run_all.py` runs every step with fixed parameters and seeds. Aggregation is ordered.
  Outputs contain no timings; timings live only in `provenance/RUN_RECEIPT.json`.
- `src/replay.py` copies only `src/` into a new directory, reruns everything, and compares every
  output byte for byte. See `provenance/REPLAY.json`.
- The hand-off package's Round-10 coordinator audit (`evidence/Erdos993_Round10_Audit`) was
  replayed separately with its own `replay.py`. Its three outputs were byte-identical to the
  packaged receipt (`provenance/ROUND10_COORDINATOR_REPLAY.json`).

## Known weaknesses

- **Search limits.** Exhaustive coverage stops at n=23 (middle range) and n=19 (all positions).
  Families are finite windows. The only unstructured search, annealing, is weak.
- **Plateau cases.** None was encountered, so the criteria are untested exactly where they are
  tightest.
- **Heuristic only.** The hub-family mechanism in PROOF.md is a leading-order heuristic. Only
  Lemma 2 is exact.
- **Correlated errors.** One author wrote both the implementation and the checks. The coordinator
  code comparison and literal enumeration reduce, but do not remove, that risk.
