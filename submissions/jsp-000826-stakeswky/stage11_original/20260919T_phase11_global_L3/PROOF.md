# Proof that `L_3(F) >= 0` for every forest

## 1. Exact coefficients through degree four

Let `F` have `n` vertices and `m` edges. Put

- `s = sum_v binom(deg(v),2)`, the number of unordered adjacent edge pairs;
- `t` equal to the number of three-edge subsets whose union is connected.

Because `F` is a forest,

`t = sum_v binom(deg(v),3) + sum_{uv in E(F)} (deg(u)-1)(deg(v)-1)`.

The first three nontrivial coefficients are

`p_2 = binom(n,2)-m`,

`p_3 = binom(n,3)-m(n-2)+s`,

and

`p_4 = binom(n,4)-m binom(n-2,2)+binom(m,2)+(n-4)s-t`.        (1)

The formula for `p_4` is ordinary inclusion-exclusion on the edges contained
in a four-set. A single edge occurs in `binom(n-2,2)` four-sets. A pair of
adjacent edges occurs in `n-3` four-sets, while a pair of disjoint edges occurs
in exactly one. This gives `binom(m,2)+(n-4)s`. Three edges can occur in one
four-set exactly when they form a connected three-edge tree, giving the `-t`
term. Four forest edges cannot lie on four vertices.

Write

`A = binom(n,3)-m(n-2)`,
`P = binom(n,2)-m`,
`B = binom(n,4)-m binom(n-2,2)+binom(m,2)`.

Then

`L_3 = (A+s)^2 - P(B+(n-4)s-t)`.                           (2)

Since a forest has `m<=n-1`, `P>=0`. Also `t>=0`. Therefore

`L_3 >= f(s) := (A+s)^2-P(B+(n-4)s)`.                     (3)

## 2. The worst allowed `s` for `n>=12`

Always `0<=s<=binom(m,2)`, because every adjacent edge pair is an edge pair.
The derivative of the quadratic `f` is

`f'(s)=2s+2A-P(n-4)`.

At `s<=binom(m,2)`, it is enough to prove

`m(m-1)+2A-P(n-4) <= 0`.                                  (4)

After multiplying by six, (4) is equivalent to

`n(6m+n^2-9n+8)-6m(m-1) >= 0`.                            (5)

For fixed `n` the left side of (5) is concave in `m`, so on
`0<=m<=n-1` its minimum is at an endpoint. The endpoint values are

`n(n-8)(n-1)` and `(n-6)(n-2)(n-1)`.

Thus (5) holds for every `n>=8`, hence in particular for `n>=12`. Therefore
`f` is nonincreasing throughout the allowed interval and

`L_3 >= f(binom(m,2)) =: g(n,m)`.                          (6)

## 3. The worst allowed `m` for `n>=12`

Put `u=n-1-m`, so `0<=u<=n-1`. Direct expansion gives

`g(n,n-1-u)-g(n,n-1) = u B_n(u)/24`,                     (7)

where

`B_n(u) = 5n^4 - 2n^3u - 40n^3 + 24n^2u + 115n^2`
`         - 12nu^2 - 70nu - 140n + 6u^3 + 24u^2 + 54u + 60`.

We show `B_n(u)>=0`. Its derivative is twice

`H_n(u) = -n^3+12n^2-12nu-35n+9u^2+24u+27`.

`H_n` is convex in `u`, hence its maximum on `[0,n-1]` occurs at an endpoint.
At the endpoints,

`H_n(0) = -(n^3-12n^2+35n-27)`,

`H_n(n-1) = -(n^3-9n^2+17n-12)`.

Both parenthesized polynomials are positive for `n>=12`: at `n=12` they are
positive, and their derivatives are positive for all later `n`. Hence
`H_n(u)<0` on the whole interval, so `B_n` is decreasing. Its minimum is

`B_n(n-1) = (n-2)(n-1)(3n^2-11n+12) > 0`.                (8)

Thus `g(n,m)>=g(n,n-1)`. A final expansion factors as

`g(n,n-1) = (n-12)(n-3)(n-2)^2(n-1)^2 / 144`.            (9)

This is nonnegative for every `n>=12`. Equations (3), (6), (7), and (9)
therefore prove `L_3>=0` for every forest of order at least 12.

## 4. Orders at most 11

The finite certificate `src/check_l3.py` uses NetworkX 3.6.1
`nonisomorphic_trees`, which implements enumeration of non-isomorphic free
trees. It forms every multiset of tree isomorphism classes with total order at
most 11. The resulting forest counts are

`1,2,3,6,10,20,37,76,153,329,710` for orders `1,...,11`, a total of 1,347.

For every forest it computes the complete independence polynomial in two ways:

1. rooted-tree dynamic programming followed by component convolution;
2. literal enumeration of all vertex subsets of the assembled forest.

The two complete polynomials agree. The program separately recomputes
`p_2,p_3,p_4` from (1) and checks them against the literal count. All 1,347
forests satisfy `L_3>=0`. The compact result file records 10,342 compared
coefficient entries and fixed hashes of the generated record stream.

This finite computation is not Lean formalization and not independent external
peer review. It is only the finite base needed after the written all-`n>=12`
argument.

## 5. Consequence for the remaining original problem

The repository already proves the `k=1,2` initial minors. This run adds `k=3`.
Therefore, if `PREFIX_BETA` fails for a forest, its first negative minor must
have index at least 4. By the earlier ratio argument, any genuine valley in an
independence sequence must force a negative log-concavity minor before the
Basit--Galvin tail boundary. Hence a genuine counterexample to Erdős #993
cannot obtain its necessary prefix-LC break at indices 1, 2, or 3.

This does not control indices `4,...,beta-1`; ORIGINAL remains open.
