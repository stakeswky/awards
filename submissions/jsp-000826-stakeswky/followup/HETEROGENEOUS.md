# Heterogeneous branches: a restricted positive theorem

Date: 2026-09-17. Status: written derivation with exact algebraic checks; not a Lean proof, not external peer review, and no global novelty claim. This is not a solution of Erdos #993.

## Statement

Start from an edge r--h. For each i=1,...,t attach a new vertex u_i to h, then d_i new vertices to u_i, then s_i new leaves to each of those d_i vertices. Choose every pair (d_i,s_i), independently and with repetitions allowed, from

```
P = {(1,s): 3 <= s <= 17}
  union {(2,s): 4 <= s <= 8}
  union {(3,5)}.
```

There are 21 permitted branch types. For every integer t >= 70, the resulting unweighted tree has a log-concave, hence unimodal, independence sequence. The two decompositions at r and h also satisfy the corridor criterion. The branch types need not be identical.

This excludes an infinite family not restricted to the identical (3,5) branches of the v2 family. It does NOT establish the heterogeneous assertion for every t < 70, or for any branch outside P. Finite examples below that threshold are tests only. Nor does this establish novelty relative to all published work.

## 1. Exact counting and common hypotheses

Put R_i=(1+x)^(d_i s_i), Q_i=((1+x)^s_i+x)^d_i, H_i=Q_i+x R_i, and

```
a = product_i H_i,   q = product_i Q_i,   b=xq,
E=a+b,   C=(1+x)a,   P=C+b.
```

Conditioning on h gives P. At r the two parts are E,xa; at h they are C,b. The graph has

```
n = 2 + sum_i (1+d_i+d_i s_i).
```

The supplied checker constructs the coefficients directly from binomial coefficients. For each of the 21 types it verifies, including all supported indices,

```
k Q_i[k]^2 >= (k+1) Q_i[k-1] Q_i[k+1],
k H_i[k]^2 >= (k+1) H_i[k-1] H_i[k+1],
4 R_i >= 3 Q_i,     Q_i' <= 18 Q_i
```

where polynomial comparisons are coefficientwise. Each Q_i and H_i has positive continuous support and constant coefficient 1. The factorial-log-concavity convolution closure (the classical ULC-infinity closure) implies that a, q and C are factorial-log-concave. In particular they are log-concave; b is also log-concave by a one-place shift. The general closure theorem is not a new result of this project; a finite-support coupling proof is recorded in the v2 manuscript, Section 2. Historical reference: Liggett (1997), with related finite-order convolution proof by Gurvits, arXiv:0804.1181.

## 2. The identical-branch assumption is unnecessary

The important two bounds survive taking DIFFERENT factors:

```
a >= (1+3x/4)^t q,
q' = sum_i Q_i' product_(j != i) Q_j <= 18t q.
```

Consequently the first three nonzero terms of the binomial expansion give

```
a[k] >= L_t(k) b[k],
L_t(k) = 3t/4 + (k-1)(t-1)/64
           + (k-1)(k-2)(t-1)(t-2)/(4608t).
```

Indeed q'<=18t q gives q[k-2]>=(k-1)q[k-1]/(18t), and a second application gives q[k-3]>=(k-1)(k-2)q[k-1]/(18t)^2. Multiply by the binomial terms for one, two and three factors, respectively. At k=1,2 the corresponding falling factorial is zero. No out-of-support coefficient is divided by. Since C>=a, the same relative bound holds with C in place of a.

For t>=70, L_t(k)>k+1 for all integers k>=1. The first two terms suffice: their slope in k is (t-1)/64>1 and their value at k=1 is 3t/4>2.

## 3. Unbounded algebraic bounds

Let M(t,k)=4608t L_t(k), an integer polynomial. The checker independently expands both expressions

```
G1=M(t,k-1)M(t,k+1)
   -4608tk [M(t,k-1)+M(t,k+1)+4608t],
G2=M(t,k-1)^2 -4608tk [2M(t,k-1)+4608t].
```

After substituting t=70+s, k=2+r, every one of the 25 nonzero coefficients in each expression is strictly positive. The whole coefficient tables are emitted to symbolic.json. Thus for ALL t>=70, k>=2, not merely sampled values,

```
L(k-1)L(k+1) >= k[L(k-1)+L(k+1)+1],          (I)
L(k-1)^2 >= k[2L(k-1)+1].                   (II)
```

The script tests these identities by integer polynomial operations. The mathematical implication from positive coefficients to positivity on nonnegative arguments is elementary and is used explicitly, not inferred from numerical evaluations.

## 4. Log-concavity of both mixtures

Take z=a or C and f=z+b. At an interior index k>=2 factorial log-concavity and (I) give

```
f[k]^2 >= z[k]^2 >= (1+1/k)z[k-1]z[k+1]
  >= (1+1/L(k-1))(1+1/L(k+1))z[k-1]z[k+1]
  >= f[k-1]f[k+1].
```

At an endpoint with a zero next coefficient the required inequality is immediate. The support of b ends before that of z when t>=70.

At k=1, E is the independence polynomial of the (n-1)-vertex tree obtained by deleting r, and P is that of the n-vertex tree. For any N-vertex tree its first three coefficients are 1, N, (N-1)(N-2)/2. Hence the stronger margin at k=1 is

```
N^2 - 2 * (N-1)(N-2)/2 = 3N-2 > 0.
```

This proves log-concavity of E and P, for the entire stated infinite family.

## 5. Two root splits cover the corridor

Let m be the rightmost mode of a. We have 2<=m<deg(a): a[1]<=19t while a[2]>=25*binom(t,2)>19t; the coefficient just before the leading 1 is greater than 1. Factorial log-concavity then gives

```
a[m] >= m*a[m-2]/(m-1),
a[m+2] <= (m+1)*a[m]/(m+2).
```

With L(k)>k+1, these bounds show E[m-2]<E[m] and E[m+2]<E[m]. For m=2 use E[0]=1 directly; an out-of-support coefficient is zero. As E is unimodal, every mode of E lies in {m-1,m,m+1}.

If E has a mode at m or m+1, the r split (E,xa) has modes at distance at most one, which suffices. Otherwise E has its unique mode at m-1. Then b[m-1]>b[m] and a[m]<(1+1/L(m-1))a[m-1]. The first inequality places every mode of b at or before m-1. Applying factorial log-concavity of a and (II) gives

```
a[m+1] < m/(m+1)*(1+1/L(m-1))^2*a[m-1] <= a[m-1].
```

Thus C[m]>C[m+1], so C's earliest mode is at most m. The h split supplies D<=m, while the r split supplies U>=m-1. Therefore D<=U+1. This argument allows mode plateaus and does not assert anything about all other vertex splits.

## 6. Computation and scope

Run `python3 branch_study.py --out NEW_DIRECTORY` without -O. It emits every graph, coefficient list, parameter choice and diagnosis. The 2,002 small-palette records exhaust unordered type multisets of lengths 2 and 3 within this finite palette. The 1,200 irregular records are deterministic bounded probes, not a completeness claim. Four t=70,71 mixtures are theorem regression controls, not new counterexample searches.

Every graph polynomial is compared coefficient by coefficient between explicit list-convolution formulas and an expanded-graph packed-integer DP. The script's all-vertex diagnostics are from its message implementation, not an independently audited all-vertex theorem. `audit_study.py` separately rebuilds every graph using deletion/closed-neighbourhood recursion, or the specified sampling scope when invoked accordingly.

The proof is a generalization of the v2 inequalities and uses a classical convolution theorem. The exact checks are not a Lean formalization or a third-party mathematical review. Reproducible code cannot by itself certify that a written statement matches its intended graph family.
