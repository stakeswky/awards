# Phase-3 review and repair record

Review type: SAME_MODEL_SELF_REVIEW. No independent external mathematician,
second agent, organizer or outside service reviewed this run. A second
counting algorithm and a clean rerun are not external peer review.

Final mathematical classification: NOT_CLOSED. The evidence verifies scoped
necessary conditions and finite witnesses; it does not verify ORIGINAL.

## R1. Critical: missing implication to ORIGINAL
Paths: PROOF_ATTEMPT sections 3.3 and 5; GAP.md.
The edge formulas and mixed-edge disjunction do not exclude all simultaneous
real-forest configurations. No proof of J_H or new RSM estimate was found.
Resolution: explicitly retain the first gap, use PROOF_ATTEMPT rather than
MAIN_PROOF, set NO_STRUCTURAL_ADVANCE, and do not use CI or counts as a proof.
This is an unresolved mathematical gap, not a repaired theorem.

## R2. Major: LOCAL is not HEREDITARY
Paths: src/edge_diagnostics.py; src/hereditary.py; src/integrate.py.
The main counter establishes LOCAL only. Its material file intentionally
keeps HEREDITARY UNKNOWN; the later independent coverage stage supplies seven
positive certificates. The integration stage matches IDs AND full n/edge
inputs before assigning that premise. All other 53 graphs remain UNKNOWN.
No global-minimality conclusion is made. The 23-vertex graph is not minimal
in any counterexample sense: its whole sequence is unimodal.

## R3. Major: a multiplicity checksum alone is insufficient
Paths: HEREDITARY_COVERAGE sections 1-3; src/hereditary.py.
A total of 2^n would not by itself prove distinct subset coverage. The repair
is an explicit structural induction: included/omitted root cases, all child
subsets in disjoint vertex sets, exact retained versus separated components,
and component products. Equal signatures reconstruct isomorphic forests.
Every signature representative AND its actual subset mask have full arrays
recounted. This is the reason the finite HEREDITARY assertion is accepted.

## R4. Verification strengthening and a code bookkeeping repair
Paths: src/coverage_regression.py, src/hereditary.py main.
Add an independent direct-enumeration check of the complete signature
multiplicity distribution, not just maxima or total counts. It passes on
all six main graphs of order <=12 and five separate basic forest controls;
9,573 subset occurrences have full coefficients checked in THREE algorithms.
Invalid simple-forest inputs and plateau/zero-shift controls are tested.

The pre-repair hereditary runner would stop on a candidate without listing
unvisited requested inputs. It now records those inputs as NOT_RUN with the
candidate-stop reason. No such candidate occurred in either execution, so
no mathematical count or completed result changed. The original source/data
hashes and original logs are retained under review/ and logs/. The final
source was rerun after this change; full deterministic outputs matched.

## R5. Major: auxiliary quantifiers and controls
Paths: STATEMENT sections 2-3; certificates/bad_leaf_hereditary.json.
The old bad leaf is now a valid refutation of the stronger EVERY-leaf claim
under HEREDITARY. It is not a refutation of an existential good-vertex claim,
J_H, RSM or ORIGINAL. Its vertex 0 is good and U=D=8. The seven-vertex star's
negative Q at (1,2) is off residual, U=D=3. The new30 control is non-log-concave
but unimodal. These separations are explicitly asserted by src/integrate.py.
RSM is not silently strengthened to one leaf for all pairs or weakened to one
bad leaf; its K2 premise is not changed.

## R6. Edge semantics and signs
Paths: PROOF_ATTEMPT sections 2-3; src/edge_diagnostics.py analyze.
There is no both-endpoints-selected class. Y already includes x. The other
component factor R is counted and retained; actual side masks exclude the
crossing edge. All displayed equalities are checked as full integer arrays.
Endpoint-removal injection bounds coefficients, not differences.
For E3, s,t>0 give strict same-role signs; the mixed-edge conclusion is an OR,
not two simultaneous inequalities. Entire mode intervals, not chosen modes,
are used. No claim that all edges alternate is made. Deletion/contraction is
not allowed to preserve the indices or hypotheses without proof.

## R7. Nonvacuous tests and finite scope
Paths: certificates/integrated_summary.json; GAP.md.
All main graphs have D-U<=1. Residual graphs, pairs and eligible RSM tests are
zero. No new search extension was made after this outcome. E3 has no actual
valley witness in this run. The 56 new input records are not asserted globally
new, pairwise nonisomorphic, or an exhaustive order range. Signature totals
are rooted-entry occurrences, not unique unrooted types across graphs.
No universal inference is accepted from any finite table.

## R8. Clean replay and formal separation
Path: certificates/CLEAN_REPLAY.json.
The final six Python sources and fixed controls were copied to a clean
TemporaryDirectory. Four standard-library commands with -S -B completed.
Every generated JSON output was compared both as complete parsed JSON and as
all bytes, not only by hash. The temporary directory was removed. Exact
source hashes, command lines, versions, exit codes and logs are retained.

No complete ORIGINAL Lean source, build or transitive axiom audit exists.
The Lean environment was NOT_PROBED in this run; Stage-2's failed probe is
not represented as a current probe. FAMILY is inherited, not replayed or
extended. No external theorem from a search abstract is used.

## R9. Publication and parallel work
Paths: provenance/recovery.json and the post-write PUBLICATION_RECEIPT.json
in the delivery archive. The observed initial remote HEAD is 5169aa0...;
the frozen reference is source material, not live execution. Container git
clone failed on DNS; authenticated GitHub connector reads succeeded. This
failure is not represented as absence of GitHub access or a clean worktree.

The publication procedure uses a new scoped subtree, an append-only run entry
in state, a fresh remote-head check and a non-force ref update. Existing
current_work is preserved as data. The actual outcome is recorded only after
successful publication and readbacks. PR must remain Draft and unmerged.
Repository checks cannot alter this review's mathematical classification.

## R10. Failed transport detected before branch publication
An attempted compressed-source blob had a different Git byte identity from
the intended packet. It was rejected before creating any reachable tree or
updating a branch. The actual tested native source tree was uploaded instead;
its Git tree identity matches the local six-file tree exactly. The rejected
blob identity is retained in archive provenance/REJECTED_TRANSPORT.json.
This is a publication repair, not a mathematical improvement or a new test.

## Decision
E1-E3: accepted with their written premises and necessary-only conclusions.
H1/H2: accepted as a computer-assisted finite coverage proof and auxiliary
witness; independent outside validation remains separate.
J_H and RSM: UNRESOLVED. ORIGINAL: NOT_CLOSED. ORIGINAL_FORMAL:
NOT_ESTABLISHED. Structural progress: NO_STRUCTURAL_ADVANCE.
