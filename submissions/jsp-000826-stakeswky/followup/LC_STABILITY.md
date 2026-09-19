# A log-concave perturbation lemma and the 24-branch threshold

Date: 2026-09-17. Status: written derivation with exact algebra and finite
computation, not Lean-formalized and not externally peer reviewed. No global
novelty, priority, or solution of the full Erdos #993 problem is claimed.

## Scope of the result

Use the edge r--h construction and exactly the palette from
[HETEROGENEOUS.md](HETEROGENEOUS.md):

- (d,s)=(1,s), 3<=s<=17;
- (d,s)=(2,s), 4<=s<=8;
- (d,s)=(3,5).

With t independently chosen branches from these 21 types, put

    Q_i=((1+x)^s_i+x)^d_i, R_i=(1+x)^(d_i*s_i), H_i=Q_i+xR_i,
    a=product_i H_i, q=product_i Q_i, b=xq,
    E=a+b, C=(1+x)a, P=C+b.

**Both E and P are log-concave, hence unimodal, for every integer t>=24.**
This conclusion is uniform over every permitted mixture, not just equal
branches. A complete finite calculation additionally verifies E and P for
all mixtures with 1<=t<=4. Thus the unresolved heterogeneous range under
these results is 5<=t<=23. The previously recorded all-t identical-(3,5)
result is unchanged.

The distinguished r/h corridor has been checked for all mixtures at t=1..4.
Its previous general threshold t>=47 is unchanged: the present LC argument
does not assert the corridor theorem at every t>=24. In particular, proving
P unimodal does not automatically establish a particular certificate for it.

## 1. The previous proof is valid but discards useful terms

[THRESHOLD_REFINEMENT.md](THRESHOLD_REFINEMENT.md) lower-bounded
(z[k]+b[k])^2 merely by z[k]^2. Here we also use log-concavity of b. The
improvement is in a sufficient argument; no old graph count is corrected or
retracted.

### Local stability lemma

Let z0,z1,z2,b0,b1,b2 be nonnegative real numbers, and k>=1. Suppose

    k*z1^2 >= (k+1)*z0*z2,
    b1^2 >= b0*b2,
    k*b0 <= z0,  k*b2 <= z2.

Then

    (z1+b1)^2 >= (z0+b0)*(z2+b2).

**Proof.** Put p=z0*z2, u=z0*b2, v=z2*b0, and w=b0*b2. Ordinary
log-concavity of z (implied by the first assumption) and of b gives

    (z1*b1)^2 >= p*w = u*v >= min(u,v)^2.

All quantities are nonnegative, so z1*b1>=min(u,v). Expanding the desired
margin and using the two central-square bounds yields

    (z1+b1)^2 - (z0+b0)*(z2+b2)
       >= p/k + 2*min(u,v) - u - v
        = p/k - |u-v|.

The endpoint assumptions imply 0<=u,v<=p/k; hence |u-v|<=p/k. This also
handles zero endpoints without dividing by z0 or z2. QED.

Neither the log-concavity assumption on b nor the strengthened assumption on
z may simply be deleted. The test file contains explicit rejection controls.
Finite test cases exercise the implementation; they are not the proof of this
universally quantified lemma.

## 2. Common coefficient bounds

The inherited palette checker recomputes every Q_i,H_i,R_i and confirms:

    k*Q_i[k]^2 >= (k+1)*Q_i[k-1]*Q_i[k+1],
    k*H_i[k]^2 >= (k+1)*H_i[k-1]*H_i[k+1],
    4*R_i >= 3*Q_i, Q_i' <= 18*Q_i.

Polynomial comparisons are coefficientwise. Positive continuous support and
the classical factorial-log-concavity convolution closure imply that a,q,C
are factorial-log-concave. Therefore b=xq is log-concave. The convolution
closure is an existing mathematical result, not established by our palette
tests: see Liggett's convolution theorem, Gurvits arXiv:0804.1181, and the
ULC-infinity discussion in Aravinda--Marsiglietti--Melbourne,
arXiv:2104.05054. A finite-support coupling proof is also in the previous v2
manuscript; its general family theorem is not Lean-formalized.

The coefficient inequalities imply

    a >= (1+3x/4)^t q, q' <= 18t*q.

Iterating the derivative comparison and retaining terms j>=1 gives

    a[n] >= F_t(n)*b[n],
    F_t(n)=sum_(j=1)^min(t,n) binom(t,j)*(3/4)^j
                              *(n-1)_(j-1)/(18t)^(j-1).

The falling factorial (m)_r=m*(m-1)*...*(m-r+1), with (m)_0=1.
If b[n]=0 the bound is automatic. There is no division by an absent
coefficient. It applies to C[n] as well because C>=a.

The local stability lemma now only needs F_t(k-1)>=k and F_t(k+1)>=k.
The old proof demanded a larger product bound; that distinction is what
lowers the threshold.

## 3. Five terms suffice for the entire infinite range t>=24

Let J_t(k) denote the first five usable terms of F_t(k-1). For an integer
k>=2 the polynomial expression using (k-2)_(j-1) agrees with this truncation:
terms whose j exceeds k-1 have a zero falling-factorial factor. Every usable
falling factorial is nonnegative.

For each j=1,...,5,

    binom(t,j)/t^(j-1) = (t/j!)*product_(i=1)^(j-1)(1-i/t)

is nondecreasing for real t>=24. Each factor is positive and nondecreasing.
Consequently, for every integer t>=24 and integer k>=2,

    F_t(k-1) >= J_t(k) >= J_24(k).

Exact polynomial expansion gives

    J_24(k)-k = G(k)/6115295232,
    G(k)=1771*k^4 + 230230*k^3 + 25810301*k^2
                       -4051151998*k +105841916328.

At integers k=2,...,42, the accompanying certificate gives all 41 exact
positive values. For the unbounded remainder, substitution k=43+r gives

    G(43+r)=3725220144 +8847286*r +75157445*r^2
                         +534842*r^3 +1771*r^4.

All five coefficients are positive. Hence G(k)>0 for every real k>=43;
in particular this covers every remaining integer. This proves, without
extrapolating any parameter scan,

    F_t(k-1)>k   for ALL integers t>=24 and k>=2.

Using k+2 in the same inequality also gives F_t(k+1)>k+2>k. The new proof
does not need a degree cutoff, the old t>=70 tail, or numerical testing of
infinitely many t. The 60 extra scalar tests in the certificate are only
implementation regressions; positivity and monotonicity supply the infinite
steps.

## 4. Applying the lemma to actual graph counts

Take z=a or C and f=z+b. Factorial log-concavity of z, log-concavity of b,
and the preceding endpoint bounds establish the local lemma's hypotheses
at every interior k>=2. Therefore both E and P are log-concave there.

At k=1, E counts the tree obtained by removing r, and P counts the original
tree. For a tree with N vertices the first three coefficients are
1,N,(N-1)(N-2)/2; the stronger margin is

    N^2 - 2*(N-1)*(N-2)/2 = 3*N-2 > 0.

The supports are continuous and positive. At their boundaries a zero next
coefficient makes the LC inequality immediate. For t>=24, deg(b)=sum d_i*s_i+1
is less than deg(a)=sum d_i*s_i+t, so no unsupported tail is left untreated.
This completes the stated uniform LC/unimodality theorem.

A bound failure at t=23 is a limitation of this argument, NOT a graph
counterexample and NOT a proof that the threshold 24 is optimal.

## 5. Complete finite prefix, not all small trees

The source enumerates every nondecreasing type-index tuple of lengths 1..4.
Permuting branches about the hub gives an isomorphic tree, so this covers all
mixtures in that parameter range. Counts are:

| branches t | type multisets |
| --- | ---: |
| 1 | 21 |
| 2 | 231 |
| 3 | 1771 |
| 4 | 10626 |
| total | 12649 |

A separate recursive tuple generator checks the coverage and exact order.
For every entry, E and P are LC and the r/h splits satisfy D<=U+1. Counts are
compared between explicit coefficient products, expanded-tree packed integer
DP, and deletion/closed-neighborhood recursion. Both selected splits are
reconstructed by deletion and compared coefficient by coefficient.

This is a finite computational proof for these palette mixtures, not a
Lean certificate, not an exhaustive search of all trees on at most 78
vertices, and not a novel-tree count. In particular the 2002 choices at t=2,3
repeat an earlier parameter range. The 10647 choices at t=1,4 are not claimed
to be globally or cross-history new.

## 6. Direct search and the distinction between partial and full corridors

Separate from the finite prefix are 256 deterministic bounded probes outside
the palette and four controls (the known 26-vertex non-LC tree and three
threshold controls). No original counterexample was found. Each original
count and its selected conditional counts undergo the same three-route
checking. The resulting raw log has 12909 records and 12909 within-batch
unlabelled structures. Cross-history novelty is not claimed.

There are 46 outside probes with a gap of at least 2 when only the root/hub
(or hub alone) is used. This does not refute the all-vertex corridor. Full
message calculations for these 46 graphs give 42 gaps of 0 and four gaps of
1. The selected U/D witness vertices are independently deleted and recounted:
92 splits, 30338 coefficients. Full message statistics cover 8799 vertices;
we do not call this an independent recount of all 8799 splits.

## 7. Reproduction and trust boundary

From this directory, use Python 3.10+ without -O and new output paths:

    python3 test_stability.py
    python3 stability_certificate.py --out /tmp/stability24-certificate.json
    python3 small_palette_study.py --out /tmp/stability24-study
    python3 small_palette_study.py --coverage /tmp/stability24-study/trials.jsonl
    python3 audit_stability_frontier.py --log /tmp/stability24-study/trials.jsonl --out /tmp/stability24-frontier

The study supports --start/--end for bounded chunks. The joiner checks contiguous
coverage 1..12909 and never treats an incomplete/empty run as complete.
One interrupted exploratory chunk is explicitly excluded from completed counts.
All completed data, excluded-run identity, and replay receipts are retained in
the conversation archive. Public source regenerates the full raw records; the
raw log itself is not represented as Git-hosted when only its summary is in Git.

No fresh Lean build occurred in this checkpoint. The previous finite Lean
source-publication and official-toolchain replay gap remains open. The present
argument still needs external mathematical review and full formalization.
