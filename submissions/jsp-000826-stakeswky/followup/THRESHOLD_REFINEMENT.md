# Restricted heterogeneous theorem: thresholds 45 and 47

Date: 2026-09-17. Status: written proof with exact rational certificates; not Lean formalized and not externally peer reviewed. No novelty, priority, award, or full Erdos #993 solution is claimed.

This supplements [HETEROGENEOUS.md](HETEROGENEOUS.md). It does not overwrite the historical t>=70 proof.

## Statement and scope

Use exactly the 21 permitted branch types and the edge r--h construction in that document:

- (d,s)=(1,s), 3<=s<=17;
- (d,s)=(2,s), 4<=s<=8;
- (d,s)=(3,5).

For arbitrary mixtures of these types:

1. E=a+xq and P=(1+x)a+xq are log-concave, hence unimodal, for every integer t>=45.
2. The two r/h decompositions satisfy D<=U+1 for every integer t>=47.

Here a=product H_i, q=product Q_i, Q_i=((1+x)^s_i+x)^d_i, R_i=(1+x)^(d_i*s_i), and H_i=Q_i+xR_i. There are t branches, not t vertices. We do NOT claim these thresholds are optimal, nor does a failed bound below them provide a counterexample. For t<45 heterogeneous mixtures remain unresolved by this result; the specific identical-(3,5) family retains its earlier separate all-t result.

## 1. Verified hypotheses and the stronger bound

The existing palette checker re-expands every Q_i,H_i,R_i and verifies factorial log-concavity of Q_i,H_i, and the coefficientwise inequalities

    H_i >= (1+3x/4)Q_i,   Q_i' <= 18Q_i.

Classical factorial-log-concavity convolution closure implies that a and C=(1+x)a are factorial-log-concave. This closure is an external mathematical lemma, not a theorem proved by our finite tests (Liggett 1997; related convolution results: Gurvits, arXiv:0804.1181; Kahn--Neiman, arXiv:0907.0243). Its finite-support argument is recorded in the preceding manuscript. The products satisfy

    a >= (1+3x/4)^t q,   q' <= 18t q.

Put b=xq. Repeated coefficient comparisons from the derivative inequality give, for 1<=j<=min(t,k),

    q[k-j] >= (k-1)_(j-1) q[k-1]/(18t)^(j-1).

The notation (u)_r denotes u(u-1)...(u-r+1), with (u)_0=1. Taking ALL usable terms, not only the first three, yields

    a[k] >= F_t(k)b[k],
    F_t(k)=sum_{j=1}^{min(t,k)} binom(t,j)(3/4)^j
                              (k-1)_(j-1)/(18t)^(j-1).

The same lower bound applies to C because C>=a. If b[k]=0 the comparison is automatic; no absent coefficient is divided by. This is an exact coefficient inequality for every mixture, not an approximation to its coefficients.

## 2. Finite integer domain covers every smaller mixture

For this palette, deg(Q_i)<=17 and deg(H_i)<=18. Thus deg(a)<=18t and deg(P)<=18t+1, regardless of the chosen mixture.

For each t=45,...,69, the certificate checks

    F(k-1)F(k+1) >= k(F(k-1)+F(k+1)+1)             (I)

for EVERY k=2,...,18t+1. One endpoint beyond the possibly nontrivial interior is harmless. For every t=47,...,69 it also checks

    F(k-1)^2 >= k(2F(k-1)+1),                     (II)
    F(k)>k+1 for k=1,...,18t+2.                   (III)

Consequently this finite certificate covers all branch multisets at these t, without enumerating those multisets. It covers a bound whose assumptions hold for every one of them.

The exact integer representation is F_t(k)=N_t(k)/D_t, where

    D_t=4(72t)^(t-1),
    N_t(k)=sum_j binom(t,j)3^j (k-1)_(j-1)(72t)^(t-j).

The checker evaluates N by integer falling factorials. A separate implementation evaluates F by successive rational summand ratios; it compares all 25,700 values, not a sample. Conditions (I)-(III) use integer cross multiplication, with positive D_t. The records include 25,650 (I) checks and 24,012 (II) checks. All required inequalities pass.

For t>=70 the preceding all-parameter proof already applies. Its two positive bivariate coefficient tables are regenerated and checked again. The first-three-term lower bound is no greater than F. Hence the finite ranges above and the prior infinite tail together cover the claimed infinite sets of t. No extrapolation from t=69 is made.

## 3. Why (I) proves log-concavity

Take z=a or C, and f=z+b. At k>=2, factorial log-concavity gives

    f[k]^2 >= z[k]^2 >= (1+1/k)z[k-1]z[k+1].

The coefficient bound gives

    f[k-1]f[k+1] <= (1+1/F(k-1))(1+1/F(k+1))z[k-1]z[k+1].

Condition (I) says the last multiplier is at most 1+1/k. This proves the desired inequality. Zero-support endpoints hold directly. For k=1, f is an independence polynomial of a tree on N vertices (E deletes r, P retains r), so its first coefficients are 1,N,(N-1)(N-2)/2. The stronger inequality has positive margin N^2-2f[2]=3N-2. All supported coefficients are positive. Thus E and P are log-concave, and hence unimodal, throughout t>=45.

## 4. Why (II)-(III) prove the r/h corridor

Let m be the rightmost mode of a. Every H_i has first coefficient between 5 and 19; hence a[1]<=19t and a[2]>=25*binom(t,2)>19t for t>=47. Its leading coefficient is 1 and the preceding coefficient exceeds 1. Therefore 2<=m<deg(a).

Factorial log-concavity gives

    a[m] >= m*a[m-2]/(m-1),
    a[m+2] <= (m+1)*a[m]/(m+2).

By (III), E[m-2]<E[m] and E[m+2]<E[m]. At m=2 use E[0]=1; terms outside the support are zero. Since E is now known unimodal, its modes lie in {m-1,m,m+1}. If E has a mode at m or m+1, the r split (E,xa) already has modes at distance at most one.

Otherwise E has its unique mode at m-1. Then b[m-1]>b[m] and

    a[m]<(1+1/F(m-1))*a[m-1].

The first inequality places all modes of log-concave b at or before m-1. Factorial log-concavity and (II) imply

    a[m+1] < m/(m+1)*(1+1/F(m-1))^2*a[m-1] <= a[m-1].

Therefore C[m]>C[m+1], and its earliest mode is at most m. The h split (C,b) supplies D<=m; the r split supplies U>=m-1. This proves D<=U+1, including possible plateaus. No statement about other vertex splits is asserted.

## 5. Method failures and reproducibility

At t=44, (I) fails for k=34,...,49. At t=46, (II) fails at k=40,41. These are failures of this uniform lower-bound argument only. They do not refute either graph property below the published thresholds.

Run from this directory, without Python -O, using fresh output directories:

    python3 threshold_certificate.py --out /tmp/erdos993-threshold-new
    python3 continued_probe.py --out /tmp/erdos993-probes-new
    python3 test_threshold.py

`threshold_summary.json` records per-t hashes and exact coverage. The complete bound rows are regenerated by the source. `probe_summary.json` identifies all 134 completed graph records: 128 outside-palette probes, plus six theorem-boundary controls. The deterministic generator reconstructs all graph inputs and coefficients; its raw log is hash-bound. No original counterexample was found.

These are same-session computations and a written argument. This round performed no fresh Lean build and no third-party review. Repository CI is not mathematical certification. The unresolved general tree/forest problem remains separate.
