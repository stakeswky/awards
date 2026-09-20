# Gap, self-review and source-access record

## Verdict

ORIGINAL = NOT_CLOSED; C4-F = NOT_CLOSED.
Exact partition/refinement conservation = PROVED (written proof).
Four-type, all-multiplicities closure = PROVED_COMPUTER_ASSISTED.
General arbitrary-component budget comparison = UNPROVED.
Legal original counterexample = NONE FOUND IN THIS RUN.
Lean build and axiom audit = NOT_RUN. Review = SAME_MODEL_SELF_REVIEW,
not an independent external reviewer. No global novelty claim.

## The smallest remaining statement

For a disconnected forest F whose every proper induced subforest is unimodal,
and an actual History(F,k) with h<=k and k+1<beta, prove

    E_w[sum_i sigma_i] + mu_F d_F >= Var_w(sum_i mu_i)

when there is no proper LC component subunion. All local tails, signed
increments, support endpoints, original vertices/edges, and real coefficient
weights must remain. This package proves that comparison for its explicit
palette class, not for arbitrary remaining non-LC component types.

For the exact variance, an existential choice of partition does not weaken
the missing statement: R_P-V_P is the same for every partition. The signed
kernel and adjacent-weight recurrence have been proved and audited, but no
uniform compensation from HEREDITARY has been obtained in the general case.

## Review of logical dependencies

The graph construction in Section 6 retains every vertex and edge. Full
polynomials have three agreeing counts. Section 5 proves LC-times-unimodal
with interval support and handles all boundary zeros and plateaus. Section 7
uses multisets and verifies each candidate's entire coefficient sequence,
not merely the failure or success of LC. Section 8 is an induction for all
component counts: an LC blocker is removed and the strictly smaller complement
is already known unimodal; if no blocker exists the finite residual list is
complete. No finite sample is extrapolated without this induction.

For an actual minimum bad forest, HEREDITARY is used only to make a proper
complement unimodal. It is not attributed to the ordinary tested large graphs.
No root-absent polynomial is substituted for original-graph conditional
availability. Arbitrary attachments and arbitrary new non-LC exterior factors
are not covered by the unconditional palette theorem. The minimum-bad-graph
blocker exclusion does allow arbitrary OTHER components under its explicit
minimality premise.

The exact accounting theorem is not advertised as a new forest inequality.
No new variance upper bound substitutes for the required budget comparison.
At B212+B226, k=137, the actual values are approximately

    E sigma = 405.6494667090553,
    mu*d = 14.598497403561991,
    R_budget = 420.24796411261724,
    V = 0.01079084903676148,
    G = 420.2371732635805,
    probability of a negative local sigma = 4.796811890175476e-28,
    signed negative local contribution = -5.2440508666508325e-31.

The exact rationals determine every sign; these decimals are only display.
This known pair is a fresh reproduction/control, not a new graph discovery.
Its e is about -2.9416674 and next decline about 2.19247%; it is not near a
rebound just because current d is small. No historical B batch counts are added.

## Actual repairs during this run

A budget-driver assertion initially assumed both the first strict descent
and the following position would be in the requested middle range. For
T26+T26 the following position k=17 has k+1=beta=18 and is not qualified.
The driver was corrected to compute and save range_qualified for each record,
retain that record as a boundary control, and count only 19 qualified positions.
The entire budget driver and later clean replay were rerun. The failed
assertion was a test-classification assumption, not a failed forest theorem.

A display-only helper hit Python's integer-string digit limit when reading
an exact fraction exceeding 4,300 digits. It was rerun with the digit limit
disabled. Verification drivers already use exact unbounded integers and
serialize long fractions as numerator/denominator strings. No coefficients
or signs were rounded or replaced to bypass this limit.

The 212-vertex identity is fixed by the sourced arm list
[6,7,7,7,8,8,8,8,8,8,8,8,8] and by its full coefficient hash, not by its order
alone. The 226 and 212 sources stay distinct. The full graph identifiers and
source checks are in the scripts and compact palette receipt.

## Sources actually obtained

The initial and pre-publication research head was
b8831d70a30a23bc081f91b41bbfa94972a61b85. The repository RESEARCH_PROTOCOL.md,
RESEARCH_STATE.json and live PR #1 metadata were read. PR was Draft/unmerged.
The state had ORIGINAL unresolved; its old A2 C1 status was not taken as the
current truth in place of the later A3 refutation notice.

The complete Window_C_Round4_Component_Closure.md was read from the Library.
Its shared Round-4 ZIP was located, but materialization failed with
"This Project file does not have an authorized raw-byte materialization path."
Reading the ZIP as text returned no content. ROUND4_RESEARCH_BRIEF.md and
ROUND4_COMMON_PROTOCOL.md were not obtained as readable individual files.
Their contents are not claimed read. This is an incomplete required-source
recovery, not a reason to stop the mathematical work possible from the full
Window C task and the repository protocol.

A3 CLAIMS_FOR_B.md was read at
parallel/window_a/20260920T053053Z_a57c4c_round3_slack_barrier/,
blob 7b7873fe7b736c6dd8b8f92faa4f5f12745d3c6f. It supplies the exact definitions,
not an established U_var<=R theorem. Its remote directory did not contain the
full A3 proof. This run independently derives the signed/refinement formulas;
it does not claim byte restoration or quote an unavailable V_TV proof.

B212 was read from parallel/window_b/20260920T0325Z_critical_middle/
CRITICAL_CASES.json, blob b5896a5d1fc48482b26f840d61eaa58bda2bfa0a.
B226 came from Library Window_B_Round2_C1_for_A.md with its actual graph and
complete polynomial. The B3 report and feedback supplied the previous
B212+B226 budget control and kept the two historical batches separate.
The explicit tree formula is also consistent with the B3 support-obstruction
note, but that note's theorem is not used as a unimodality proof here.

The Phase-10 arbitrary-core private-arm proof was read for scope comparison.
It requires explicit large-arm hypotheses, including a>=24; our palette uses
at most eight arms at a hub, so that displayed sufficient theorem is not
being silently reused as the justification. The earlier component-order-30
external census is not a dependency of the present certificate.

## Attribution and publication

The B239 homogeneous bush and small non-LC tree constructions are inherited
research examples; no discovery credit is claimed. The original problem is
the independent-set-sequence problem recorded as Erdős #993. Basit--Galvin's
existing beta boundary is inherited for range labels, not proved here.
The minimum LC-subunion obstruction is an inherited research idea; this run
supplies a self-contained convolution proof and a new run-specific blocker
certificate. All source programs and this proof were written in this run
with OpenAI ChatGPT assistance. No organizer acceptance, prize entitlement,
external peer review or formal proof is asserted.

Git publication is limited to this new Window C directory. Large regenerated
raw data are delivered in the conversation archive, not falsely called raw
Git-hosted files. Only actual successful tool receipts establish publication.
