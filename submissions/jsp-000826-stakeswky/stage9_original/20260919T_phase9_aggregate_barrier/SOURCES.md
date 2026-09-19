# Sources and provenance

Observed live HEAD: 9dca96ce3c373af30be2bff51f44f1ca8d08c64e.
PR #1 was open, Draft and unmerged; base main f4e7173d89dfe91022a185427d63452c8ffbf6ae.
The actual RESEARCH_PROTOCOL and RESEARCH_STATE were read before research.
The mounted Phase8 RESEARCH_STATE.snapshot bytes have Git blob identity
576785c28655e89c4261639d47dd15047f2a702b, matching the live state.
Phase8 proof, gap, review, statement and sources were read from the mounted
archive; the live stage proof blob is cross-checked in the delivery receipt.
Prior branch instructions restrict publication to the submission research
subtree and preserve PR Draft status; CONTRIBUTING requires English public text.

The full supplied Phase8 archive, including its Phase7 canonical inventory,
provides exact historical graph codes. build_inputs.py reconstructs their
union. Input source hashes are in inputs/PRIOR_PROVENANCE.json. Membership is
compared using complete canonical strings, not just polynomial equality or
hashes. These comparisons are not a replay of old independence-set counting.
Only absence from these two supplied inventories is claimed, not from all
previous sessions or the mathematical literature.

The unchanged engine.py and forest_exact.py come from the supplied Phase8
source (which retained the previous native research engine). Their identities
are recorded in NATIVE_CERTIFICATE and CLEAN_REPLAY. New source implements
availability moments, exact finite compensation checks and the directed
stress surface. No third-party program was copied into the new source.

Primary mathematical input:
Abdul Basit and David Galvin, On the independent set sequence of a tree,
Electronic Journal of Combinatorics 28(3) (2021), P3.23;
arXiv:2006.12562v2, https://arxiv.org/html/2006.12562.
Theorem 1.3 and its proof give beta=ceil(alpha(n-1)/(n+alpha)) for every graph.
The current task re-read that result in HTML. It is not a new tail theorem,
not an asymptotic random-tree statement, and not restricted to connected graphs.

Context, not a general-forest input:
Grace M. X. Li, Unimodality of independence polynomials of two family of trees,
arXiv:2603.03025v1, https://arxiv.org/html/2603.03025v1.
That paper proves the stated T_(3,m,n) and modified families. The present
proof of a different explicitly defined parameter region is self-contained;
no general theorem is imported from that paper. The familiar subdivided-star
and bush constructions are not claimed as new graph inventions. A targeted
literature search was insufficient to establish global novelty; none is claimed.

The new written branch-LC calculation, Toeplitz convolution argument,
compensation bound, graph correspondence and infinite-parameter estimates are
fully stated in PROOF_ATTEMPT. Classical convolution facts have prior pedigree
(e.g. Hoggar 1974; Keilson--Gerber 1971); this work asserts no novelty for them.
The finite three-equal-hub remainder is checked in native source and a fresh
copy replay, not inferred from status files or repository CI.

Retained external input: scinet-ai/math-number-theory at
fafb35784d4235c9e5dd701fd3b2c1f4955ae9ec remains the earlier component-30/H2/H3
census dependency. Its complete computation was NOT rerun. Neither that result
nor the 247-small-index normal form covers arbitrary large external components.
The new exact graph tests and compensation proof do not depend on that census.

The container cannot resolve github.com for a direct clone. Connected GitHub
reads/writes work. A local inspected clone is not claimed. Public writes use
a child of the live HEAD and a non-force update after a second HEAD check.
All computation ran in the current task container, with no user machine,
paid service or continuing background worker. Review is same-model self-review,
not independent peer review. OpenAI ChatGPT assisted the research.
