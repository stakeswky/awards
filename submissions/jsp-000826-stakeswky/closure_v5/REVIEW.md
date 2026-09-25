# Adversarial review and repaired delivery

Review type: same-model self-review, in the same task and environment. There was
no separate reviewing agent, organizer verification, or external peer review.
Two exact algorithms are algorithmic cross-checks, not independent reviewers.

## Dependency audit

| Claim | Exact premises and quantifiers | Justification | Used by |
|---|---|---|---|
| Actual counts E/P | Every finite list from B59 | Independent-subset bijections, MAIN_PROOF 1 | Final graph theorem |
| Positive supports and D bound | Every branch and every positive t | Palette rows, addition of inequalities, section 2 | All divisions and compression |
| ULC convolution | Positive initial support, finite order at least degree | Checked Gurvits v1 Theorem 1.1; explicit padding argument | Product curvature |
| B1 rates and dominance | All 59 branches; every supported index | Exact finite coefficients, two constructions | Product identity and L bounds |
| B2 finite curvature | Every two/three-branch multiset; A and Q | Complete integer certificate, two multiplication algorithms | All t>=2 grouping |
| Grouping | Every list of t>=2 branches | Even t: pairs; odd t: one triple plus pairs | z curvature and b LC |
| Birth-rate identity | Every product of positive initial-support factors | Explicit reindexing of weighted sum | All ratio bounds |
| Mixed-loss lemma | z has curvature, b is LC, neighbors nonnegative | Full Delta expansion and square-root inequality | Both parameter zones |
| Compressed finite envelope | Every t=4..23, S=3t..17t, epsilon=0/1, 2<=k<M | Derived sufficient inequalities and full rational comparison | Middle interval |
| Infinite tail | Every t>=24 and k>=2 | Termwise monotonicity; 109 exact checks; polynomial identity | Infinite interval |
| k=1 and endpoints | Actual finite trees, positive initial support | Count empty sets, vertices and nonedges; zero extension | Final LC |
| LC implies unimodal | Positive initial support, then zeros | Nonincreasing successive ratios | FAMILY |

No arrow assumes that E or P is already unimodal. There is no claim that a
single arbitrary sequence-pair insertion preserves the conditions. Grouping
actual factors supplies the all-list theorem directly, without such a claim.

## Findings, attacks, and resolutions

**R1 — Missing explicit route to log-concavity of b.** Merely saying that each
Q_i is factorial-log-concave would require an additional convolution argument.
The final source checks the finite-order ULC certificate for BOTH A-blocks and
Q-blocks. Section 5 now applies the same checked order-addition theorem to Q,
then shifts it to b. All 2,723,570 A/Q block inequalities were freshly rerun by
both multiplication algorithms. Resolved; downstream mixed-lemma premises hold.

**R2 — The full tree is not the deleted-leaf tree.** Reusing epsilon=0 curvature
or rate bounds for P without modification would be invalid. Sections 2, 5,
6 and 8 retain epsilon throughout, using M=S+t+epsilon, N=S+4t+epsilon and lower
z-rate S+epsilon-k. Both epsilon values and all indices are in the finite box.
Resolved by explicit separate quantification; no E-only certificate is promoted.

**R3 — Division outside support and negative denominators.** At k=S+1 or S+2,
q_k may vanish and its birth rate cannot be divided as in an interior formula.
Section 8 handles these cases directly with v=0, ell=0. When both neighbors
vanish the loss is zero. The second ratio bound is used only when
S+epsilon-k>0; otherwise w=0. Every denominator used is proved positive.
The finite loops omit exactly zero b-neighbors, not failed comparisons. Resolved.

**R4 — Squaring can introduce an incorrect requirement.** The square-root
elimination keeps the sign split 1+W-R<=0 before squaring. A regression checks
negative-left-side cases and exact rational-square boundaries. The second
implementation expands the comparison polynomial instead of using the first
cleared-denominator expression. The illustrative t=4,S=12,epsilon=1,k=9 case
also shows why a negative left side must not be squared unconditionally. Resolved.

**R5 — Finite coverage is not a count of sampled mixtures.** Every allowed list
has 3t<=S<=17t and D<=min(3t,floor((S+2t)/5),18t-S). Sections 6–8 prove the bounds
for the actual product using only these inequalities. The full over-covering
integer box, not a sampled subset of attainable totals, was checked. Sorting
branch lists for B2/B3 preserves products and includes repeated members.
1,322,020 interior records and 2,424,400 nonzero-neighbor conditions passed in
each arithmetic implementation. All 20 slices were checked for completeness.
Resolved; no parameter threshold or mixture is left uncovered.

**R6 — Infinite extrapolation.** The last interval is not inferred from the
finite envelope. Section 9 proves both monotonicities algebraically. The
identity after k=111+u has coefficients 3672,38954,506, all strictly positive.
The k=2..110 prefix was separately computed as 109 exact fractions by two
formulas. Resolved; no finite search substitutes for infinite t or k.

**R7 — The v4 obstruction must survive review.** The actual 25-vertex input
and 30-vertex output were recounted through DP and deletion recursion. The
output has Delta_16=-219 but no descent followed by ascent. The input fails
the quantitative product bound at coefficient 13. Thus it refutes shape-only
LC insertion, not this product-family theorem or ORIGINAL. The negative cross
contribution -800 was explicitly retained, not silently discarded. Resolved.

**R8 — One checker regression had a wrong expected count.** The first small
labeled-forest regression expected 335 total input graphs; enumeration found
340. All coefficient comparisons had passed. The exact per-order counts for
n=0,1,2,3,4,5 are 1,1,2,7,38,291, summing to 340. The expectation was corrected
and all nine tests rerun. The initial failure log is retained under review/.
This was a test bookkeeping error, not a failed FAMILY inequality. Resolved.

**R9 — An interrupted development replay was not a complete certificate.** A
combined development command timed out after completed t<=20 replay slices.
The missing slices were completed, and the FINAL proof source was then copied
to a fresh directory without cached modules. Forty-six fresh commands, using
Python 3.13.5 with -S -B, exited zero; all slices, graphs, tests, and aggregation
were rerun there. Only completed files are in the final fresh receipt. Old or
interrupted logs are not credited as full runs. Resolved.

**R10 — Formal verification and ORIGINAL scope.** No executable Lean was found;
a version/compilation probe failed to launch, and a bounded official-toolchain
download failed with DNS error. No complete top-level Lean source or axiom audit
exists for the new theorem. These are substantive uncompleted obligations,
not a claim that installing Lean would by itself formalize the proof. ORIGINAL
also lacks the general-forest existence or representation step described in
MAIN_PROOF 12. No limited-family or non-LC control is substituted. Unresolved,
and reported independently from the accepted mathematical FAMILY proof.

## Final review judgments

- family_math: ACCEPT as a complete computer-assisted proof of FAMILY-LC and
  FAMILY, conditional only on the stated standard mathematical theorem and
  ordinary trust in the reviewed exact computation. No new mathematical gap
  was found in the complete candidate or repaired dependency chain.
- family_formal: NOT_ESTABLISHED; top-level build and axiom audit NOT_RUN.
- original_math: NOT_CLOSED; no proof or legal nonunimodal forest produced.
- original_formal: NOT_ESTABLISHED.

This acceptance is self-review, not an external endorsement, organizer decision,
novelty determination, or award qualification. All publication must retain that
boundary and keep PR #1 Draft and unmerged.
