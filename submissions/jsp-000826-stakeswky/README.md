# JSP-000826 / Erdős Problem #993 — scoped research snapshot

This directory records a bounded research snapshot for **JSP-000826 / Erdős Problem #993** as of **2026-09-17**.

- Justin Sun Prize catalog entry: [JSP-000826](https://github.com/TheJustinSunPrize/awards/blob/main/problems/catalog-0801-0900.md#JSP-000826)
- Problem page: [Erdős Problem #993](https://www.erdosproblems.com/993)
- Submitting account: `stakeswky`
- Proposed contributor placeholder, if later needed by the organizers: `RECIPIENT-JSP-000826-A`

## Scope

This is a **scoped computational and structural research record**. It does **not** claim a proof or disproof of Erdős Problem #993. It does not request a change to the catalog status, candidate status, award status, recipient status, or payment status.

The purpose of this initial packet is to give the current research state a public, reviewable timestamp while the full problem remains open.

## Problem

For a forest `F`, let `i_k(F)` be the number of independent sets of `F` having exactly `k` vertices. Erdős Problem #993 asks whether the finite sequence

`i_0(F), i_1(F), ..., i_α(F)`

is always unimodal.

A proof must cover every forest. A disproof requires one explicit forest whose independence sequence is not unimodal.

## Current research snapshot

The current research notes record the following work:

1. **Eight research rounds** have been carried out, combining direct counterexample search, structured search, and analysis of parameterized tree families.
2. The main counterexample-search campaign records approximately **5,989,791 evaluations** with **no counterexample found in the searched space**.
3. Research rounds 7–8 record **185,540 deduplicated structures** after the stated deduplication stage, again with no counterexample found among those structures.
4. A parameterized tree family `T_t` has been isolated for structural study. The current notes contain a derivation of an independence-polynomial decomposition of the form

   `P_t(x) = (1 + x) H(x)^t + x Q(x)^t`.

5. The current notes also record the family invariant

   `α(T_t) = 16t + 1`.

6. Several component sequences arising from this family have been shown in the working notes to satisfy stronger shape properties such as unimodality or log-concavity, but these component facts have **not** yet been assembled into a proof that `P_t` is unimodal for every `t`.
7. **52 registered parameter instances** of the family, together with several directed search tracks, have been checked computationally in the research process without finding a counterexample.

The large search counts above come from bounded and directed computational experiments. They are **not** claimed to exhaust all trees or forests up to any vertex order.

Items 2–7 above are reported here as the state of the submitting research notes. This initial snapshot does not present them as independently reproduced results, and it does not ask the awards repository to certify them.

## What has not been established

The following points remain open in this work:

- No counterexample to Erdős Problem #993 has been found.
- No proof of Erdős Problem #993 has been completed.
- No proof has been completed that the whole parameterized family `T_t` has a unimodal independence sequence for every `t`.
- The finite computations do not imply the universal statement for all forests.
- No complete Lean theorem for the claimed full problem has been successfully kernel-checked.
- No organizer-designated independent verification is claimed.

Therefore the correct mathematical status of JSP-000826 remains **Open**.

## Evidence and reproducibility status

This first snapshot records scope and chronology only. The full search source, configurations, seeds where applicable, deduplication rules, machine-readable outputs, hashes, and Lean sources/logs are **not included in this initial packet**.

Those artifacts should be added in later revisions as fixed, reproducible evidence before any stronger verification or candidate-status request is made. In particular, future evidence should distinguish:

- exhaustive finite checks from heuristic or directed searches;
- proved symbolic identities from experimentally observed identities;
- locally checked code from independently reproduced results;
- a finite Lean certificate from a theorem equivalent to the full Erdős #993 statement.

## Priority and award boundary

This commit and pull request provide a public timestamp for the contents of this research snapshot. They do **not** by themselves establish mathematical priority, exclusive reservation, solver status, formal candidate status, award entitlement, or payment rights. Any such determination belongs to the organizers and requires the repository's published review and verification process.

No existing problem-bank flags, candidate records, award records, recipient profiles, published decisions, or payment records are modified by this submission.

## Assistance disclosure

The research process and preparation of this snapshot used OpenAI ChatGPT assistance. The submission is presented for public intake and review, not as independent verification.
