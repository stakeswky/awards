# JSP-000826 / Erdos #993 — research progress

Research account: `stakeswky`. Date: 2026-09-17.

**This is a research record, not a solution submission. No counterexample to the full tree/forest problem or universal proof is claimed.** Catalog, eligibility, candidate, award, recipient, and payment records are unchanged.

## Current packet

- [v2 progress and verification scope](progress/v2-2026-09-17.md)
- [Artifact identities and evidence levels](evidence/v2-manifest.json)
- [Recorded Lean target/axiom output](evidence/lean-v2-core.log)

The earlier chronology-only snapshot remains in Git at commit `1bd0f79d639439571b240fd3c0163d609b486bdb`. This update supersedes its statements that the specified parameter family had no general proof and that no finite Lean certificate had been run. It does not supersede the unsolved status of the full problem in this work.

## Mathematical scope

For a finite forest F, i_k(F) counts independent vertex sets of size k. A disproof needs a legal forest and exact indices i < j with i_i(F) > i_(i+1)(F) and i_j(F) < i_(j+1)(F). Failure of log-concavity or of a weighted sequence is not enough. A disconnected forest counterexample must not be advertised as a tree counterexample.

The specified family T_t has level sizes 1, 1, t, 3t, 15t. Put S=(1+x)^5+x, Q=S^3, H=Q+x(1+x)^15. Its polynomial is P_t=(1+x)H^t+xQ^t. The v2 working proof establishes log-concavity of this family for positive integer t using an unbounded inequality argument and exact finite certificates. That family proof is **not** a Lean theorem for all t and has not received external peer review.

The recorded Lean run checks a separate 14-vertex tree, its actual independent-set counts, an auxiliary leaf-alignment counterexample, and general sequence lemmas. It does **not** check Erdos #993.

## Evidence limitations

The archive and source hashes identify the conversation's research artifacts. This public progress packet is not the complete v2 archive: a checksum is not a public download or an independently reproduced proof. Full historical logs and the complete 176-module Lean source tree are not represented as uploaded here. The third-round full-data archive remains unavailable in the supplied materials. Later additions must identify precisely what can be replayed from this branch alone.

All historical evaluation counts include repeated graphs and/or relabellings. No new exhaustive vertex-order bound is claimed. This work used OpenAI ChatGPT assistance; different implementations developed in the same session are not external independent verification.

## Attribution and award boundary

Proposed contributor placeholder, only if subsequently needed by organizers: `RECIPIENT-JSP-000826-A`. No unconfirmed personal identity or private contact/payment data is included. A timestamp does not establish priority, exclusive reservation, solver status, or award entitlement.

This progress remains on the existing draft research PR. No upstream submission, merge to main, or prize-status change is requested by these files.
