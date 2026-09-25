# Same-model review: Phase 13 global L4

## Verdict

The claimed scoped theorem is supported:

```text
For every finite simple undirected unweighted forest F,
p_4(F)^2 >= p_3(F) p_5(F).
```

`ORIGINAL` remains **NOT_CLOSED**. No Lean build or axiom audit was run. This review is same-model self-review, not independent external review.

## Dependency audit

The proof depends on the already published E4-S signed-sector theorem in
`parallel/window_e/20260920T_round4_pair_compensation_e/PROOF.md`.
E4-S supplies both the exact signed-pair decomposition and a capacity-respecting matching for classes A and B. Phase 13 does not reinterpret E4-S as a proof of the full minor; it analyzes the complement at the fixed index `j=4`.

At `j=4`, `2|C|+|D|=8`, so every relevant `D` has even order at most eight. If a negative group outside E4-S had two high components, each would have at least four vertices; equality forces two four-vertex claws, which is class A. Therefore the only possible uncovered negative group has exactly one unsplittable high component of order at most eight.

The bounded connected-tree classification is complete rather than sampled. Two different generators were executed:

1. every Prüfer sequence through order eight;
2. every `(n-1)`-edge subset of `K_n`, retaining exactly the trees.

They agree on every order total and on the unsplittable-high counts. The totals also agree with Cayley's `n^(n-2)` values. No high unsplittable tree occurs through order six. The only structural type at order seven is Q7; the only type at order eight is Q8.

The algebra then leaves only `Q7 union K1` as a negative uncovered `D`: Q8 has `g=0`. The residual source has `C=empty`, deficit one, and maps to an admissible four-unit target with surplus two.

## Capacity collision audit

The main possible logical failure would be spending a positive target already used by E4-S. The proof handles this explicitly.

For a four-unit target, any one-step E4-S source must have a high component that becomes only singleton components after deleting the splitter. Connectivity forces that component to be a star. The three possible sizes yield defects `0,-1,0`; only `K_(1,4) union K1` is negative and can consume one unit of this target's surplus.

Two such star sources cannot share a target because their incidence subgraph would have eight edges on eight vertices. Two distinct residual sources cannot share a target because the common-neighbor center is unique, and two second centers would give nine edges on nine vertices. A star and a residual source cannot coexist because their combined incidence subgraph would have ten edges on nine vertices. All are impossible in a forest.

Thus a residual source never competes with an E4-S star source for the same target, and there is at most one residual source. The target surplus two is sufficient.

## Boundary checks

* The proof is division-free and does not assume positive coefficients at the tested index.
* Plateaus are allowed; the theorem is a weak log-concavity inequality.
* The theorem is about ordinary unweighted forests only.
* A later log-concavity failure would not by itself be an Erdős #993 counterexample.
* No finite sample is extrapolated to large forests: the only finite enumeration classifies the bounded local component forced by `|D|<=8`.
* The new theorem moves the unresolved prefix index from `k>=4` to `k>=5`; it does not close the general middle no-rebound barrier.

## Reproduction receipts

Executed locally in a clean working directory during this run:

```text
python3 VERIFY_PRUFER.py
python3 VERIFY_EDGE_ENUM.py
```

Recorded source/output SHA-256 values are in `certificates/PRUFER.json` and `certificates/EDGE_ENUM.json`.

No Lean command was executed. Repository CI, if successful, is repository-integrity evidence only and is not a mathematical or formal-proof certificate.
