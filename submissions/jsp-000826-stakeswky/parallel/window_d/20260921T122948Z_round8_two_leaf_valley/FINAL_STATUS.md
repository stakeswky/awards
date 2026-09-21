# D8 final mathematical status

Run: 20260921T122948Z_round8_two_leaf_valley.
ORIGINAL=NOT_CLOSED. No new ORIGINAL graph-domain exclusion.
The early CLAIMS_FOR_PEERS.md remains unchanged.

## Actual result

The two-leaf deletion square and its full forest-path determinant factorization
have a written proof. All actual off-path branches and exterior component
factors are retained. The unresolved step is from that convolution identity,
together with actual minimum-counterexample premises, to a blocking two-rank
leaf comparison at the first real valley. No existence theorem was obtained.
Summing old negative RSM minors only repeats the assumed valley.

An exact NON-GRAPH guard refutes a weaker relaxation which retains only the
commuting square, the coefficientwise path-sign and proper marked-subset
unimodality. Its total polynomial is
(1,8,23,32,30,29,30,24,12,3), with first descent 3 and first rebound 5;
both formal leaf-support RSM minors are -4. The exterior array R starts
(1,4,4,4,6,...), impossible for a four-vertex graph because R_4=6>1.
The guard does NOT supply actual rooted-branch factors or HEREDITARY and
refutes none of ADMC, J_H, RSM or ORIGINAL.

## Exact execution boundary

Seven fixed actual graph controls, 211 two-leaf pairs, 1034 requested
mask arrays and 11711 integer coefficients were checked by two graph
recurrences. Four tiny graphs also had all 384 retained masks checked by
independent-subset enumeration. Actual valleys and nonempty U/D residual
pairs are both zero; these are identity regressions, not nonvacuous RSM tests.

D7's 2928/2929-point control is separate: all 4807 leaf metadata rows and
ten stored polynomial arrays were audited; only 13 selected complete arrays,
31592 coefficients, were freshly recounted by the inherited native DP and
deletion algorithms. The full old D7 runner/all 50 orbits were NOT rerun.
Both large HEREDITARY labels remain UNKNOWN.

Final sources were copied into a clean directory, recompiled and run.
Three JSON outputs, 904504 bytes in total, matched as all bytes AND complete
parsed JSON. No Lean build, axiom audit or outside peer review was performed.

## Late peer/external reading

C8's actual interface was read and preserved. The official arXiv abstract
and HTML statements of Fang, Lu, Nevo, Yao and Zheng, arXiv:2609.20961v1
(17 September 2026), were checked: they state unimodality for all sufficiently
large forests and central strict log-concavity. This is external progress,
not a new D8 proof. The entire paper/Lean was not independently audited here,
and no numerical threshold was derived. It does not supply our remaining
rank-specific leaf argument or a verified finite completion.
The subsequent A8 interface commit was detected and preserved, not assumed
as a proved input to D8.

## Publication scope

This status and the early interface are the public research record here.
The full proof, separate gap/review, exact source, complete result tables,
input hashes and executable replay are delivered as conversation artifacts.
Do NOT describe those raw source/table bytes as Git-hosted: source publication
was blocked by the tool safety-state layer. A preceding malformed source blob
was rejected by byte identity before any tree/ref referenced it.
No force update, shared-state change, other-window overwrite or main change
was made. PR #1 must remain Draft and unmerged. No B8 receipt is presumed.
