# Review, repairs and final mathematical judgment

Reviewer type: **SAME_MODEL_SELF_REVIEW**. No second agent, outside referee,
organizer, or peer-review service participated. Different counting algorithms
and fresh executions do not constitute independent mathematical peer review.

Final overall judgment: **NOT_CLOSED**. Sections 1-8 of PROOF_ATTEMPT.md and
the conditional implication in section 9 are accepted with their stated scope
in this self-review. The graph-structural assertion RSM is UNRESOLVED. No full
ORIGINAL proof/counterexample or Lean verification is accepted.

## A. Dependency audit

| Step | Exact premises | Established reason | Limitation |
|---|---|---|---|
| Independent-set recurrence | Any finite simple graph, any vertex | Partition and deletion bijection, proof section 2 | Counting identity, not a shape closure |
| Smaller forests unimodal | Hypothetical globally least counterexample | Well-ordering and strictly smaller orders, section 1 | Not inferred from sampled deletions |
| Mode intervals and joint signs | Every A_v,B_v nonzero unimodal; same P | Finite monotonicity argument, section 3 | Does not prove D<=U+1 |
| D<=U+1 implies unimodal | Previous premises and this inequality | Overlap and one-comparison cases treated separately | No infinite graph certificate for the inequality |
| No isolated/K2 component | Minimality and the proved adjacent-mode criterion | (1+c x) times a unimodal smaller polynomial | Does not establish connectedness |
| Rooted messages and common factors | Actual rooted forest | Subset bijections; acyclicity separates branches | Never applied to arbitrary shape-only pairs |
| Count sums over vertices | Actual independent subsets | Double counting, section 5 | No conclusion from average signs to one shared vertex |
| Unique early/late roles | An actual valley and unimodal split | Negative-before-positive exclusion, section 6 | Necessary, not a constructor of a valley |
| Opposite selected leaf/support roles | Previous premises; actual C,H; C unimodal | Mode relation of (1+x)C and xC, section 7 | Such roles alone do not contradict a tree |
| Q<0 for every split | Actual valley, polarized split | Exact identity with one strict term, section 8 | Negative Q alone is not a valley |
| RSM would imply ORIGINAL | The precise unproved RSM in STATEMENT section 4 | Minimum counterexample contradiction, section 9 | RSM remains the first unproved bridge |

## B. Findings and repairs

**R1 / critical / top-level status.** An all-vertex numerical criterion cannot
be promoted to a forest theorem merely by defining U,D. No argument excluded
D>=U+2. Resolution: use PROOF_ATTEMPT.md, not MAIN_PROOF.md; keep ORIGINAL
NOT_CLOSED. The residual signed-minor bridge is labeled UNRESOLVED everywhere.
This mathematical gap remains; documentation is not represented as a repair
of the missing inequality.

**R2 / major / auxiliary scope.** The initial tempting 'choose any leaf'
strengthening fails. At vertex 4 of tree-11 the two maxima are 7 and 9. All
47 whole/specified-deletion counts were recomputed in two algorithms. The
whole sequence is unimodal, vertex 0 is good, and U=D=8. Resolution: retract
ONLY the every-leaf assertion under LOCAL; do not refute existence of a good
vertex, J, a minimum-counterexample theorem, or ORIGINAL. All proper induced
forests of tree-11 were NOT enumerated.

**R3 / major / insufficient structural information.** C,H, C+xH, (1+x)C,
xH,xC being unimodal together with H<=C do not close leaf insertion for
abstract sequences. The exact retained example has a valley at 2,3 but cannot
be a forest (it would require eight edges on six vertices). Resolution: reject
this shape-only closure; retain actual branch products, roots and the common
component factor in RSM. It is not a valid graph counterexample.

**R4 / major / unlocalized minor assertion.** A real seven-vertex star has
Q=-5 at i=1,j=2, even though every proper induced forest is unimodal. Its whole
sequence is unimodal and U=D=3. Resolution: the unlocalized all-leaf inequality
is explicitly REFUTED. The residual RSM assertion never uses those indices,
and its truth is NOT inferred from this exclusion. The proposed quantitative
bridge is still unresolved, not 'repaired and proved'. The two actual whole
slopes are positive; negative Q is not a counterexample criterion.

**R5 / major / platforms and endpoints.** A chosen mode instead of the whole
interval, or checking only D<U, would miss allowed plateaus. Resolution: section
3 proves both D<=U and D=U+1, and section 7 proves the separate single-maximum
and multi-maximum cases for the leaf relation. All arrays keep zero padding.
Finite common-sum regression covers 1,028 overlap groups and 3 adjacent groups;
these tests supplement the proof, not replace it.

**R6 / major / vacuous evidence.** Every stress graph has D-U<=1. Therefore
there are no graph cases with two residual indices. Resolution: every summary
states that RSM has NO nonvacuous graph test here. The 1,662 abstract valley-pair
regressions exercise the polarization/minor algebra but are not graph evidence
for RSM. No additional random budget was added to conceal this limitation.

**R7 / major / inherited LC failure.** The old certificate file
closure_v5/certificates/graphs.json was not Git-hosted (404). Resolution: recover
the exact graph from committed verify_graphs.py, retaining its source SHA;
recompute every old25/new30 vertex split in two algorithms. The old bound
failure (A_13=1, B_13=4), new triples and mixed contribution -800 are explicitly
asserted by current source. The new30 LC difference remains -219 and the graph
remains unimodal. FAMILY and ORIGINAL are not refuted by this control.

**R8 / minor / coefficient bookkeeping label.** The initial regression summary
used 'padded_comparisons' for (n+1)(2n+1) stored, padded coefficient slots. Those
are not all the same as the shorter raw DP/deletion arrays being compared.
Resolution: rename to stored_padded_coefficient_slots (21,149). Preserve the
initial logs and source hashes in review/pre_repair_hashes.json. This changes
no graph count or theorem. The final source and all affected evidence were
rerun; only final-source logs support the final receipt.

**R9 / reproducibility / compact evidence.** Repeated leaf vertices share full
polynomials; storing only maxima would lose material information. Resolution:
certificates/material_compact.json stores all 74 distinct zero-padded
polynomials, with explicit lookup IDs for all 85 vertices of the four material
graphs and their whole polynomials. check_compact.py roundtrips EVERY whole/A/B
array and mode pair. Full raw arrays remain in the conversation archive and
are reproducible from the committed source. Compression is not a hash-only
check or a statistical certificate.

**R10 / formal status.** The fresh `lean --version` command failed with
command-not-found, exit 127. There is no top-level ORIGINAL Lean source even
apart from the missing executable. Resolution: ORIGINAL_FORMAL
NOT_ESTABLISHED, environment probe BLOCKED, build and axiom audit NOT_RUN.
No PARTIAL/VERIFIED label is assigned to written finite-sequence proofs. FAMILY
formal status is inherited unchanged, not freshly tested.

**R11 / provenance and literature.** The original page/forum could not be
fetched live. The Li paper's restricted statements were read from the precise
v1 HTML, not promoted from an abstract into an all-forest theorem. Resolution:
no external theorem is used as a mathematical dependency; no latest global
solution status, novelty, or independent endorsement is claimed.

**R12 / publication.** Concurrent work must not be overwritten and PR #1 must
remain Draft. Resolution: add a uniquely named research subdirectory; retain
old current_work and append this run to state; re-read HEAD before non-force
publication; record actual resulting SHA/readbacks and CI separately. Until a
write succeeds the local verdict is LOCAL_ONLY. CI is never a premise in the
mathematical dependency table. Actual outcome is in PUBLICATION_RECEIPT.json.

## C. Fresh replay and limits

The final six Python source files were copied to a fresh temporary directory,
with standard-library-only `-S -B` executions. Four commands (diagnostics,
material, reductions, compact encoding) exited zero. The complete parsed JSON
AND bytes of the fixed inputs, diagnostics, material, reductions and compact
material matched. Summary comparison ignored only elapsed wall time. Source
hashes, commands, exit codes and log paths are in certificates/CLEAN_REPLAY.json.

There were no excluded stress records or ORIGINAL candidates. The exhaustive
0..5 labeled-forest regression and 128 star induced masks have exactly the
stated finite domains. The 193 stress records are not exhaustive and are not
claimed isomorphism-deduplicated or globally new. The 512 MB planning value was
an intended working-memory budget, not a measured peak-memory claim. No memory
benchmark was performed. Graph orders stayed within the planned bound, and
completed commands did not reach their time limits. No external worker was
started; the clean temporary directory was removed on completion.

## D. Final decision

original_math: NOT_CLOSED.
original_formal: NOT_ESTABLISHED.
family_math: historical PROVED_COMPUTER_ASSISTED, source-pinned, no new replay.
family_formal: historical NOT_ESTABLISHED, unchanged.
Proved reductions: PASS_WITH_SCOPE under this SAME_MODEL_SELF_REVIEW.
RSM, J and existential corridor L: UNRESOLVED.
Outside mathematical review: NOT_PERFORMED.
