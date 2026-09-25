# Phase 9: aggregate compensation and the remaining no-rebound barrier

**ORIGINAL NOT_CLOSED.** A scoped uniform family proof is complete, while the
general core is **NO_STRUCTURAL_ADVANCE**. No original forest counterexample,
full-forest proof, Lean build or independent external review is claimed.

Read STATEMENT.md, PROOF_ATTEMPT.md, GAP.md and REVIEW.md. SOURCES.md documents
recovery and external dependencies. VERDICT.json keeps scoped and original
status distinct. The starting HEAD was 9dca96ce3c373af30be2bff51f44f1ca8d08c64e;
PR #1 must remain Draft and unmerged.

## Main result
For the whole tree T(a1,...,at) defined in PROOF_ATTEMPT, total-mass control of
a nonnegative perturbation localizes the mode of a log-concave root-absent
polynomial. This proves unimodality in the explicit unbounded region (6.3),
including all equal groups with a>=16(t+1). The three-equal-group family
T(a,a,a) is handled for EVERY a>=1 by an infinite argument plus 25 exact finite
checks. An actual LC disconnected factor is allowed; arbitrary attached
exteriors or non-LC products are not. No global novelty is asserted.

For general forests, available-vertex moments give a plateau-safe sufficient
barrier, but its required variance bound is still unproved. A fixed 288-graph
stress surface has 428 nonvacuous middle descent tests and no barrier violation;
these are not actual U/D residual pairs or universal coverage.

## Reproduce using standard-library Python
Run without -O, since assertions are checks. In the delivery ZIP, src/ and
inputs/ already exist. In the compact Git package run UNPACK_SOURCE.py first.
The only omitted native input in Git is the full prior inventory. Reconstruct
it from the supplied Phase8 delivery (or use the input in this delivery ZIP):

    python3 -S -B src/build_inputs.py /path/to/Erdos993_Phase8

Then run:

    python3 -S -B src/compensation.py
    python3 -S -B src/regressions.py
    python3 -S -B src/directed_barrier.py
    python3 -S -B src/diagnostics.py
    python3 -S -B src/compact.py
    python3 -S -B src/replay.py

No network, additional Python packages, paid service or user-machine access
is required for these computations. build_inputs reads the prior full graph
codes, not a fresh old counting sweep. The source and compact evidence are
Git-hosted through an exact source bundle with hashes. The delivery ZIP contains
native source, prior input, every raw output and every actual replay log.
Raw arrays and the full prior inventory omitted from Git are not represented
as hosted by a hash alone. Reproduction of the mathematical family theorem
(compensation.py) requires no historical inventory at all.

No recurring/background work is installed by this run. All processes complete
within the current task. The publication receipt records only observed writes
and readbacks. Repository CI is not a mathematical certificate.
