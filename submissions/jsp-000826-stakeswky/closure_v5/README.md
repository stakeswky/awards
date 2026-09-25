# B59 all-parameter proof package

**FAMILY-LC and FAMILY:** complete computer-assisted mathematical proof for all
positive branch counts and every repeated mixture of the 59 permitted branches.
**ORIGINAL:** not closed. **Lean:** no top-level proof/build/axiom audit completed.
**Review:** same-model self-review, not independent external peer review.

Read STATEMENT.md, MAIN_PROOF.md, REVIEW.md and VERDICT.json in that order.
The proof is not a new cutoff: its three pieces cover t=1..3, every t=4..23,
and all t>=24. Two/three-branch finite-order ULC certificates and a proved
product-rate compression control the total negative mixed contribution.

## Reproduction

Python 3.13.5 was used. The proof checkers need only the Python standard library
and are written for Python 3.10+. Use no optimization flag. From this directory:

```
python src/run_checks.py --out /tmp/erdos993-clean-replay
```

The output path must be new or empty. The driver copies clean source, executes
all finite certificates and cross-checks, and does not install or claim to run
Lean. The delivered archive contains the actual graph-inputs.json and fresh logs.

For a compact repository checkout that omits the raw graph inputs, reconstruct
them first with the recorded Python 3.13.5 and deterministic generator:

```
mkdir -p certificates
python src/verify_graphs.py --generate --inputs certificates/graph-inputs.json --out /tmp/erdos993-graphs.json
python src/run_checks.py --out /tmp/erdos993-clean-replay
```

Individual checkers also accept explicit output paths. They reject a failed
inequality; passing source hashes alone does not count as mathematics.

## Fresh results

The final source was copied to a fresh runtime directory. Forty-six commands
with `-S -B` exited zero. Both arithmetic implementations agree on the full
37,819 multiset prefix, the 37,760 two/three-branch blocks, all 20 middle-range
parameter slices, and the infinite-tail finite certificate. The middle box has
1,322,020 interior records and 2,424,400 required nonzero-neighbor comparisons.
All denominators and finite/infinite coverage steps are proved in MAIN_PROOF.

The side check uses 176 explicit trees/forests and their one-vertex and
closed-neighborhood deletions, totaling 10,064 counts. It finds no original
counterexample. The supplied 25-to-30 vertex LC counterexample was freshly
recounted and remains unimodal. These are not substitutes for the family proof.

The full conversation archive contains raw graph inputs, exact per-slice
certificates, fresh command logs, source hashes, retained development failures,
and the actual failed Lean probe. The compact Git publication may contain only
source, full proof, review, and compact verification records; raw bytes absent
there are not claimed as Git-hosted. All omitted finite records are reconstructible.

## Publication scope

Only submissions/jsp-000826-stakeswky/ on the existing research branch is in
scope. Keep PR #1 Draft and unmerged. No original-problem solution, priority,
award eligibility, or external endorsement is asserted. Exact post-write Git
verification belongs in PUBLICATION_RECEIPT.json in the delivered archive.
