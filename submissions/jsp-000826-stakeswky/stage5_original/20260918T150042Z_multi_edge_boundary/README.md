# Phase 5 — multi-edge compatibility and actual boundaries

**ORIGINAL NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** No original forest
counterexample or strict reduction of the first mathematical gap was found.
PR #1 is research-only and must remain Draft and unmerged.

Read STATEMENT.md, PROOF_ATTEMPT.md, GAP.md and REVIEW.md. VERDICT.json separates
mathematical, formal, finite-execution and publication status. This package
is not a prize claim, top-level proof, or assertion of independent review.

## What this run adds
Exact shared edge-defect formulas; actual partial-star squares; a lossless
root/vertex profile recurrence with true external completion; an actual
9-to-8 partial-cut mode reversal; two root-message-equivalent 9-vertex trees
with different internal profiles; a bounded search with nonrepeated
representative seeds and exact whole-sequence valley scores.
None proves a contradiction for the unobserved residual case. Its graph,
pair and eligible RSM counts are all zero.

## Reproduce using the standard library
From this directory, using Python 3.13 (the receipt records the actual version):

```sh
python -S -B src/checks.py --out certificates
python -S -B src/boundary.py --out certificates
python -S -B src/search.py --out certificates
python -S -B src/regressions.py --out certificates
python -S -B src/compact.py --out certificates
python -S -B src/replay.py
```

The first five commands reconstruct ALL deterministic raw outputs, including
those not stored natively on GitHub. replay.py copies only source/input files
to a fresh directory, runs those commands again, and compares 13 complete
outputs byte-for-byte and as parsed JSON. Assertions are intentionally active;
do not run Python with -O. No network, paid API, user-machine process, Lean
installation or third-party Python dependency is required.

PackedForest in forest.py is inherited without modification from the pinned
Stage-4 source. It evaluates polynomials by integer packing with base 2^(n+2).
Every intermediate coefficient counts choices from disjoint subsets of at
most n vertices, so it is at most 2^n and cannot carry across that base. The
separate vertex-deletion counter uses ordinary coefficient tuples and
schoolbook convolution. Small interaction controls additionally enumerate
actual vertex subsets and their exact induced edge sets.

## Exact hosted versus archive coverage
Native Git content includes these proof/review documents, complete sources
and fixed edge-list seeds, compact JSON summaries, the complete clean replay
receipt, provenance, and certificates/NATIVE_EVIDENCE.json. The latter stores
full edge lists and complete P for 16 material records; all A/B for old23 and
the two rooted9 graphs; both rooted9 joint profiles; and all arrays in the
mode-reversal witness. Its polynomial references index complete arrays with
trailing zeros retained. The decoder verifies every represented array.

The larger interaction_material.json, discovery_records.json,
discovery_material.json, discovery_attempts.json and boundary_witness.json,
along with all failed/initial/repaired logs and pre-repair source/output
snapshots, are in the downloadable Phase-5 delivery archive, NOT all hosted
as raw Git files. The published native sources regenerate them exactly.
A summary or hash is not represented as a substitute for their bytes.
The initial search revision's 141 labeled records are NOT added to the final
122 accepted forest types. The archive preserves both runs separately.

The post-write PUBLICATION_RECEIPT.json is an archive receipt created only
after real publication/readback. Its final SHA is not guessed inside the
commit that it describes. Repository CI is separate from mathematical proof.

## Attribution and baseline
Initial live HEAD: eb4ab96170356a4846d15315af40d1bbde998f59.
The four prior ORIGINAL rounds, current protocol/state and applicable
contribution instructions were read. Scope repair and source/data blobs were
checked against live Git identities. Earlier work is preserved, not rebased
away. OpenAI ChatGPT assisted this research and same-model review. First-party
scripts follow the repository MIT license; documentation/data follow its
LICENSE-CONTENT. No global novelty, organizer acceptance or prize entitlement
is asserted. See provenance/recovery.json for exact provenance boundaries.
