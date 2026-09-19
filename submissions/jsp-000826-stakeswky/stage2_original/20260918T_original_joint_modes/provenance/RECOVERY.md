# Recovery, attribution and bounded source check

## Uploaded instructions

Read 00_READ_FIRST.md first, then prompts/01_MASTER.md; read 02_REVIEW.md and
03_REPAIR_AND_DELIVER.md as internal requirements. DESIGN_NOTES.md and the
manifest were read too. The six manifest-listed files matched their byte sizes
and SHA-256 values; archive hash and details are in prompt_manifest.json.
The zip had no Files-parsed text; the mounted archive was extracted locally.

## Repository observations

Repository stakeswky/awards, branch jsp-000826-research-snapshot.
Initial actual HEAD: 36467feaa5bd486979077b97ad2bac5a75805986.
PR #1: open, draft true, merged false.
Main/base: f4e7173d89dfe91022a185427d63452c8ffbf6ae.
The initial actual HEAD matched the uploaded design anchor. Read the actual
CONTRIBUTING.md, RESEARCH_PROTOCOL.md, RESEARCH_STATE.json,
closure_v5/{STATEMENT.md,MAIN_PROOF.md,REVIEW.md,VERDICT.json}, with section 12
of the mathematical proof read explicitly, not recovered from the PR summary.
The root tree and ancestor directory listings contain no applicable AGENTS.md.
The run creates a new directory, not overwriting an older phase-2 run.

Relevant original blob identities:
CONTRIBUTING.md: 327cae68686135bb540fec54fdae36f579db056a
RESEARCH_PROTOCOL.md: 32a1f2e37f6df29757e11f6c8018128290292de6
RESEARCH_STATE.json: e9b241bdda4adbb5351dc12af0bbb6a13c2cbc2b
closure_v5/STATEMENT.md: 7a23052ed57cb03a2126d7deb11e89b177e341de
closure_v5/MAIN_PROOF.md: 21d88992d72845ff1b5fe047776c3b2f9c44e608
closure_v5/REVIEW.md: f92f54c6c7252c3f83e5c103a14110bfe1ee89c8
closure_v5/VERDICT.json: b71a0aa6c0ea2df05a90954bc2daf0315a07bbe7
closure_v5/src/verify_graphs.py: 00d735e981e93e25ffc53c1111d50e3794fef23d

The v5 graphs.json fetch returned 404. This blocks reading that omitted raw
file, not reconstructing its stated old25/new30 control: committed source
contains the exact edges, which were read and recounted. Old finite corridor
or Lean claims are not dependencies here; the sequence criterion is rederived
from definitions. The historical FAMILY certificates were not fully rerun.

A local git clone attempt failed: 'Could not resolve host: github.com'.
GitHub connector reads succeeded. Connector publication is attempted separately;
a failed clone is not treated as evidence that write permissions are absent.
See the actual publication receipt for final head and concurrency checks.

## Bounded primary-source check (not a proof dependency)

Original page: https://www.erdosproblems.com/993 and the non-www form.
Live fetches returned internal errors; forum fetch returned 403. Search text
was not substituted for a verified latest global solution status.

Grace M.X. Li, 'Unimodality of independence polynomials of two family of trees',
arXiv:2603.03025v1 (3 March 2026):
https://arxiv.org/html/2603.03025v1
The introduction, definitions and precise restricted T_{3,m,n} / T*_{3,m,n}
statements (m,n>=1, Theorems 1.4 and 1.5) were read in the HTML. The entire
proofs were NOT independently verified or used as dependencies. The statements
are about specified tree families, not an accepted proof of every forest.
A Springer article at DOI 10.1007/s00373-026-03054-4 concerning log-concavity
breaks was also opened; it was not used to infer non-unimodality or as a proof
dependency. Search-only repository/AI claims were not independently verified.
No exhaustive literature review, global originality or current solved/unsolved
status determination is asserted by this bounded check.

## Attribution and trust boundary

Research and writing were assisted by OpenAI ChatGPT. Review is same-model
self-review. The old25/new30 control originates in the pinned project source;
its attribution and earlier scope are retained. No outside theorem or B59
curvature/ULC bound is imported into the new reductions. Computation trusts
ordinary Python integer arithmetic and reviewed source; it is not Lean kernel
verification. Repository content remains subject to its existing licenses.
No credentials, user-machine data, paid APIs, new cloud services or personal
records were accessed or published.
