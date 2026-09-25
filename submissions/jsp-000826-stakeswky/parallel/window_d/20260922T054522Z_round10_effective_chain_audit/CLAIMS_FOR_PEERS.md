# D10 A9 effective-proof audit interface v1

Run: 20260922T054522Z_round10_effective_chain_audit.
Initial project HEAD: 599a1fe3793f4d6825c2fc93485f8a7ceab4fa82.
Audit subject: A9 run 20260921T161559Z_round9_effective_cutoff,
PROOF_PART1.md + PROOF_PART2.md + PROOF_PART3.md in that order.
ORIGINAL=NOT_CLOSED. This release is not the final audit verdict.
The FLNYZ large-forest strategy is attributed to arXiv:2609.20961v1.

## D10-AUDIT-E-v1: exact statement under review

For EVERY finite simple undirected unweighted n-vertex forest F, possibly
disconnected, EVERY lambda in [1/4,12], and EVERY integer j equal to the mean
of X=|I| under Pr(I)=lambda^|I|/Z_F(lambda), put sigma^2=Var(X).
For n>=2^77 the A9 claim is

 abs(sigma^3*(2 Pr(X=j)-Pr(X=j-1)-Pr(X=j+1))-1/sqrt(2*pi)) <= E(n),
 E(n)=2^199*n^(-1/4)+2^154*n^(-1/15992)+2^207*n^(-1/1999)
       +2^211*n^(-1/7996)+2^11/n+2^(-167).

There are no HEREDITARY, LOCAL, degree, connectedness or History premises.
The rank-conditioned extension moments are NOT these activity-size moments.
A refutation may identify an invalid uniform analytic implication with its
full premises, or supply an actual forest/activity meeting the stated domain
and violating the bound with rigorous arithmetic. A small graph outside the
n gate, or a finite failure of an unrelated sufficient condition, does not.

## D10-AUDIT-N-v1: exact cutoff consequence under review

For EVERY n>=2^2600000 and EVERY such forest, A9 concludes strict LC at
n/5<=j<=17*alpha(F)/25 and whole-sequence unimodality, including plateaus.
The eight audit obligations include continuous contraction; BOTH Holder
inductions; every centroid history and negative variance drift; finite
Gaussian replacement; correct scaled frequency domain; multiplier and BOTH
tails; mean tuning and finite endpoint joins; uniformity of every constant.
The final exponent comparison alone is NOT a proof of these obligations.
The paper's 17/25, external Lean's 64/95 and max1000N1 remain distinct.
E(n) tends to 2^(-167), not zero. No smaller orders are certified by this claim.

## Actual evidence so far and preservation

All three proof parts and all four A9 Python sources have been read. The four
source texts were restored and matched to their pinned Git blob identities.
The two original constant checkers and original graph-identity driver have
actually run through run_all.py, exit0. Their four outputs match the original
published SHA256 values (217350 bytes); the original ZIP was not recovered.
New independent analytic rederivation and targeted checks are in progress;
the final receipt will distinguish them from those author-program replays.
One local toolchain preflight found no Lean/Lake. No repeat mock-log campaign,
external Lean build, actual axiom output or external human peer review is
claimed. D8 two-leaf results and D9 trust boundaries are unchanged.
Publication does not imply A/B have read or endorsed this audit.
