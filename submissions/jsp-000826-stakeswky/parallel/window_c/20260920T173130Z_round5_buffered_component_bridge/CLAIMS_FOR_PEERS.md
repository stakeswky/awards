# Window C, Round 5: buffered-band bridge (version 1)

ORIGINAL = NOT_CLOSED. General C4-F = NOT_CLOSED. The four-type C4 closure
is retained unchanged. These two claims do not assume A4-R or any unproved
connected-tree theorem. They concern whole component unions, not rooted
conditional availability or components of an independent-pair symmetric difference.

## C5-BAND-v1 — buffered log-concavity band (written proof)

Let X,Y be actual finite simple unweighted forests and F=X disjoint-union Y.
Write A_i=p_i(X), B_i=p_i(Y), d=alpha(X), s=alpha(Y), with zero padding.
Assume B is unimodal. Choose integers 0<=a<=b<=d such that
A_(i+1)>=A_i for every 0<=i<a, and A_(i+1)<=A_i for every b<=i<d.
Put L=max(0,a-s), U=min(d,b+s). Assume

    A_i^2 >= A_(i-1) A_(i+1)  for every L<i<U.

Then the WHOLE independence sequence of F is unimodal. In particular, for
any actual complete-component partition, all supported History(F,k) positions
satisfy R_budget>=V, equivalently e_k<=d_k when k<alpha(F). This includes
h<=k and k+1<beta but does not require those extra range restrictions.

Proof mechanism: the sequence A cut to [L,U], zero elsewhere, is LC. Its
convolution with B is unimodal (the signed single-crossing proof is in the
final proof body). It agrees EXACTLY with A*B on coefficient indices
[a,b+s]. Before a the original convolution is nondecreasing; from b+s it is
nonincreasing. These three pieces cover every coefficient, including plateaus.
The cutoff sequence is an algebraic comparison device, NOT a graph count,
and no allocation is deleted from any R or V computation.

In a vertex-minimal bad forest, every proper complementary Y is unimodal.
Thus every proper nonempty complete subunion X must have a negative LC minor
inside the band above for EACH admissible a,b. One may take a,b to be the
first and last modal indices of X, since X is then itself a proper forest.
This is stronger than requiring some LC failure anywhere in X, but it is
not a claim that every forest automatically passes the band test.

Exact refutation: give actual X,Y, their full integer polynomials, a,b, all
premise checks and a strict descent followed by a rise in A*B. A negative
minor outside [L,U], or a failed premise, is not a refutation.

## C5-CORE-EXTERIOR-v1 — arbitrary new cores and uncoated complement

Let C be ANY nonempty finite simple unweighted forest on q vertices. At core
vertex v attach t_v private length-two paths with distinct new vertices and
no further edges; t_v are positive integers. Call the whole decorated forest X.
Let M=sum_v t_v (arm count, NOT largest component order), t=min_v t_v, and

    eps = (1 + (3/2) * 2^(-floor(t/8)))^q - 1.

Let Y be ANY whole finite forest whose sequence is unimodal and put s=alpha(Y).
If

    M>=48q,  s<=floor(M/24),  M*eps<=1,

then X disjoint-union Y is unimodal and satisfies the same real budget
comparison at every genuine descent-history position as C5-BAND-v1.
No restrictions on the core shapes, the number of components, or Y's shape
are added. Y need not be LC or decorated, and its local sigma may be negative.
The attachment pattern on X and the three numeric gates MUST be met.

The proof uses the actual core subset expansion

    I_X(x)=sum_(S independent in C)
        x^|S| (1+x)^(sum_(v in S)t_v) (1+2x)^(M-sum_(v in S)t_v).

The nonempty-S part is at most eps times (1+2x)^M coefficientwise for
ceil(M/3)<=i<=floor(3M/4). Binomial curvature proves strict LC on this band.
The early part increases to a=floor(M/2). The existing Basit--Galvin tail
starts no later than b=ceil(2(M+q)/3). The gates place the entire required
buffer [a-s,b+s] in the proved LC band, so C5-BAND applies. This proves the
signed budget, not a claim that a variance upper bound must be affordable.

For any fixed q,s all shapes are allowed, and equal arms

    t_v=T>=128(q+s+1)^2

satisfy the gates (a sufficient explicit region, not a minimum threshold).
In a true vertex-minimal counterexample, Y-unimodality is supplied by
minimality, so a proper whole-component subunion X meeting these gates is
excluded even when every proper complete component subunion is non-LC.
This does not prove that every remaining forest has such an X.

Exact refutation: supply C and all its edges, the t_v, the completed X and Y,
full coefficients, the three rational gates and a valley. Failure of the
band for a graph outside the gates does not refute this theorem or ORIGINAL.

## Decisive controls and provenance

Initial exact polynomial checks include the core K1,3 with arms
[96,192,192,192], plus T26. Both components and the whole product are non-LC;
the buffer is [322,465] and the gates pass. A separate diagnostic uses
T(128,128,128) plus B239: C5-BAND passes while local B239 sigma at 113 is
negative. Final graph recounts, full allocations and receipts are delivered
in certificates/; at initial interface publication those final raw bytes
are not yet asserted to be Git-hosted or fully replayed.

Sources: actual Round-5 task and common baseline; unchanged C4 exact graph
counts and LC-times-unimodal proof; actual A4 report for non-circular scope;
Basit and Galvin, arXiv:2006.12562v2, Theorem 1.3 (official HTML read).
The private-arm core expansion is inherited from Phase 10; the new use here
is the buffered window and arbitrary uncoated whole complementary forest.
Proof/novelty status: written derivation, SAME_MODEL_SELF_REVIEW; no global
novelty claim, external review, Lean build or axiom audit. Final source and
certificate hashes are to be recorded in MANIFEST.json, not guessed here.
