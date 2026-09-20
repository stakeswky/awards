# Window B Round2: real equalities; tail-only C1 refutation

**ORIGINAL = NOT_CLOSED.** No original forest counterexample and no universal middle no-rebound proof.

This package executes the actual `Window_B_Round2_Critical_Search.md`, reads A's complete prior proof and the live published A2-C1/A2-C2 claims, and preserves all A/history/top-level state files. All writes are confined to this new B subtree. PR1 remains Draft and unmerged.

## Critical outcomes

- **0 middle negative LC minors** among 57,039 stored-corpus middle positions. The separate small census tested another 90,901 positions, with overlap not added into a fictional combined total.
- **91 distinct actual qualified equality forests** with p_k=p_(k+1), k+1<beta. All lack prior strict descent and strictly decrease next. Equality after prior descent: **0**. Equality followed by growth: **0**.
- **0 original valleys**; full sequences are scanned across plateaus.
- **0 residual U/D position pairs** in five fully profiled material graphs. LOCAL is not HEREDITARY.
- **A2-C1 is refuted globally, but only in the tail here.** The previously published B(8,14) was freshly graph-validated and dual-recounted, then reduced to a connected 212-vertex C1 counterexample. The starting example is credited to kylekaba/erdos-problem-993. This is not an original counterexample or a global-minimum claim.

The 212-vertex witness has alpha=112,h=53,beta=73. At k=100 its exact triple is

    847610821485228731644602571649,
    4522019629839748203096035496,
    68312013275412659728362951.

The C1 integer slack is

    -7776584328545997344597535346898068025648064064490951778.

The complete graph and every coefficient are in `CRITICAL_CASES.json`.

A connected 14-vertex equality example has P=(1,14,78,225,371,371,231,85,16,1), h=4,beta=6 and p_4=p_5. Path19 has p_5=p_6=3003,p_7=1716,h=5,beta=7. Both are actual equality controls, not valleys. Complete edge lists are included.

## What was run

The equality census completed 85,625 generated unlabelled forests through order16. Exactly 84 qualified equalities were found (19 at n14,65 at n16). Explicit larger path/palindromic constructions add seven distinct examples; an elementary infinite-family equality proof is included.

The targeted lanes retain fixed n/fixed k comparisons, recompute n,M,alpha,h,beta for each graph, and separately optimize the next signed decrease only under an actual weak-descent premise. The stored union of search, reduction and material-control records has 4,632 distinct graphs. It is not an all-order census or a claim of historical novelty. The main critical targets remain zero despite those computations.

There were 27 accepted property-preserving deletions in the C1 reduction. Each accepted step was independently counted. Thirteen distinct permitted reductions of the final graph were independently rejected. Only local irreducibility is claimed.

**Verification is scoped:** 164 distinct stored whole-P arrays / 7,943 coefficients were independently recounted at least once, not all ordinary search graphs. Five full vertex profiles give 1,000 dual-recounted A/B arrays / 109,175 entries. Three small material examples also received exhaustive subset enumeration. All actual equality and C1-failure graphs are included in the independent recount set.

Eight final clean-source commands completed successfully, and **22 complete deterministic outputs / 13,643,533 bytes** matched. One earlier outer replay timeout was repaired and was not counted as a completed program. No Lean build, axiom audit or external peer review is claimed.

## Files

`SEARCH_REPORT.md` gives actual coverage, fixed-size comparisons and obstacles. `CLAIM_TESTS.md` identifies the actual A claims and their exact premises. `CRITICAL_CASES.json` contains full graphs and coefficients. `EQUALITY_FAMILIES_PROOF.md` proves explicit equality constructions. `GAP.md`, `REVIEW.md`, `VERDICT.json` and `FEEDBACK_FOR_A.md` preserve the status boundaries. `certificates/VERIFICATION.json` and `EXPECTED_OUTPUTS.json` record completed verification and all expected raw-output hashes.

The Git package contains readable reports, complete decisive cases, compact certificates, and all executable source in the `SOURCE_BUNDLE.part*` files listed in `SOURCE_MANIFEST.json`. Large raw search/A-B/moment files and complete logs are provided in the conversation evidence archive; they are **not falsely described as Git-hosted raw files**.

## Reproduce

Use Python and NetworkX3.6.1 (the actual tested version). Counting uses arbitrary-precision integers and the two unchanged prior graph counters. Reconstruct sources, then use the `certificates` directory from the previous B evidence archive:

```sh
python UNPACK_SOURCE.py
python src/reproduce.py --output ../B_round2_reproduced \
  --old-certificates /path/to/Erdos993_Window_B_20260920/certificates
```

The output directory must not already exist. The previous directory is read-only input for the specifically requested archived-array C1 scan; it is not new search coverage. All other graphs and raw arrays are reconstructed by the supplied source. The prior archive can also be reconstructed with the already published Round1 source package.

The final synchronization receipt is in the delivered conversation archive, with a scoped PR progress comment pointing to the actual commit. A Git commit or successful repository CI is not a proof of ORIGINAL.
