# Phase 13: global fourth log-concavity minor for forests

Status: **proved mathematically, with a finite computer-assisted classification used only for one bounded residual type classification.** This is not a full proof of Erdős #993 and is not a Lean formalization.

## Theorem

For every finite simple undirected unweighted forest `F`, if `p_k(F)` denotes the number of independent sets of size `k` (with zero outside the support), then

```text
p_4(F)^2 >= p_3(F) p_5(F).
```

Equivalently, the fourth adjacent log-concavity minor

```text
L_4(F) = p_4(F)^2 - p_3(F) p_5(F)
```

is nonnegative for every forest.

The proof extends the signed-sector theorem `E4-S` in
`parallel/window_e/20260920T_round4_pair_compensation_e/PROOF.md` and closes the only residual negative group that can occur when `j=4`.

## 1. Exact signed-pair decomposition

Use the notation already proved in E4-S. Positive objects are ordered pairs of independent sets of sizes `(j,j)` and negative objects have sizes `(j-1,j+1)`. For a pair `(I,J)` write

```text
C = I intersection J,
D = I symmetric_difference J.
```

For every component `Q` of the forest `F[D]`, let its bipartition sizes be `a_Q <= b_Q`. Put

```text
O_D(z) = product_Q (z^a_Q + z^b_Q),
g(D) = [z^(|D|/2)] O_D - [z^(|D|/2-1)] O_D.
```

Then E4-S proves the exact identity

```text
L_j = sum_(D even) g(D) p_(j-|D|/2)(F-N[D]).        (1)
```

Equivalently, before summing over the exterior independent set `C`, each admissible fixed group `(C,D)` has signed surplus `g(D)`.

E4-S also proves that the total signed contribution is nonnegative over the union of these two classes, counting overlap once:

* **A:** every high component (bipartition gap at least two) is a four-vertex claw `K_(1,3)`;
* **B:** there is exactly one high component and it is splittable by the canonical leaf-neighbor operation defined there.

The proof below does not reuse positive capacity without checking collisions.

## 2. What can remain negative when j=4

At `j=4`, every admissible group satisfies

```text
2|C| + |D| = 8,
```

so `|D|` is even and at most eight.

Assume a group has `g(D)<0` and is outside `A union B`.

There cannot be two high components outside class A. Every high tree has at least four vertices, and the only four-vertex high tree is the claw. Thus two high components with `|D|<=8` would have to be two claws, which is class A.

Hence there is exactly one high component `Q`, and it is unsplittable. Only the connected tree `Q` must be classified, and `|Q|<=8`.

The two independent exhaustive programs in this package classify every labeled tree on at most eight vertices by two different generation algorithms. They agree on the following complete statement:

* for orders at most six, every high tree is splittable;
* at order seven, the only unsplittable high tree up to isomorphism is `Q7`: two degree-three centers at distance two, each center having two pendant leaves. Its bipartition sizes are `(2,5)`;
* at order eight, the only unsplittable high tree up to isomorphism is `Q8`: a degree-four center and a degree-three center at distance two through the unique degree-two vertex, with three pendant leaves on the degree-four side and two on the degree-three side. Its bipartition sizes are `(2,6)`.

The Prüfer enumeration checks all `1, 1, 3, 16, 125, 1296, 16807, 262144` labeled trees at orders one through eight. The independent edge-subset enumeration reproduces the same counts and classification.

Now use the parity and size restriction on `D`.

For `Q8`, there is no room for another component. Its orientation polynomial is

```text
z^2 + z^6,
```

so at `|D|/2=4`, both the central and preceding coefficients are zero and `g(D)=0`. It is not a negative group.

For `Q7`, `|D|` must be even. The only possibility outside the already covered smaller cases is `D = Q7 union K1`. Its orientation polynomial is

```text
(z^2+z^5)(1+z) = z^2 + z^3 + z^5 + z^6,
```

hence

```text
g(D) = [z^4]O_D - [z^3]O_D = -1.              (2)
```

Because `|D|=8`, equation `2|C|+|D|=8` forces `C` to be empty.

Therefore **every negative j=4 group outside E4-S is exactly this one residual structural type.**

## 3. Direct compensation for the residual Q7 plus one isolated vertex

Fix such a negative group. In its `Q7` component let

* `x` be the unique degree-two vertex;
* `a,b` be the two degree-three centers adjacent to `x`;
* choose a fixed total order on the vertices of `F`, and let `w` be the least of the four pendant leaves of `Q7`;
* suppose `w` is adjacent to `a` (rename `a,b` if needed);
* let `u` be the isolated vertex of `F[D]` outside `Q7`.

Define a target group by

```text
C' = {w,x},
D' = D minus {a,b,w,x}.
```

The four vertices of `D'` are the other three pendant leaves of `Q7` together with `u`.

This is an admissible group in the original graph. The two vertices `w,x` are nonadjacent. Within the original induced graph `F[D]`, `w` has only neighbor `a`, and `x` has only neighbors `a,b`; all of these removed vertices are absent from `D'`. Thus there are no `C'-D'` edges. The four vertices of `D'` are isolated in `F[D']`.

The index is unchanged:

```text
2|C'| + |D'| = 4 + 4 = 8.
```

The target orientation polynomial is

```text
(1+z)^4 = 1+4z+6z^2+4z^3+z^4,
```

so its surplus is

```text
g(D') = 6-4 = 2.                                (3)
```

Each residual source has deficit exactly one by (2). It remains to prove that the positive capacity in (3) has not already been spent by E4-S and that multiple residual sources cannot overload it.

## 4. No target overload

Fix a target `(C',D')` of the above form: two vertices in `C'`, four isolated vertices in `D'`, and no `C'-D'` edges.

### 4.1 E4-S sources that can use this target

Suppose an E4-S class-B negative source maps in one leaf-neighbor step to this target. Its old `D` has six vertices. If the deleted high component leaves `t` singleton components and there are `q` other singleton components, then

```text
t+q=4.
```

Because deleting the chosen leaf `w` and its neighbor `v` leaves only singleton components inside the high component, connectivity forces that high component to be the star `K_(1,t+1)` centered at `v`.

Its orientation polynomial, including the `q=4-t` other units, is

```text
(z+z^(t+1))(1+z)^q.
```

For the only possible high values `t=2,3,4`, its signed defects at the relevant center are respectively

```text
0, -1, 0.
```

Thus the only negative E4-S source that can spend capacity from a four-unit target is

```text
K_(1,4) union K1,
```

and its deficit is one.

Such a source is represented, relative to the six target vertices, by one removed center having four edges into the target: one edge to the promoted vertex in `C'` and three edges to vertices of `D'`.

Two distinct such star sources cannot use the same target. Their two distinct centers together with the six target vertices would form a subgraph with eight vertices and eight distinct edges. A forest on eight vertices has at most seven edges.

### 4.2 Residual sources that can use this target

A residual `Q7 union K1` source has two removed centers. Relative to the same six target vertices, each removed center has exactly three incident target edges. One of the centers is adjacent to both vertices of `C'` and one vertex of `D'`; the other is adjacent to the middle vertex `x` and two vertices of `D'`.

The center adjacent to both vertices of `C'` is unique if it exists: two common neighbors of two nonadjacent vertices would make a 4-cycle in `F`.

If two distinct residual sources used the same target, they would therefore share this common-neighbor center and have two distinct second centers. The union would contain the six target vertices plus three removed centers, hence nine vertices, and the three centers contribute `3+3+3=9` distinct target-incidence edges. A forest on nine vertices has at most eight edges. Contradiction.

Therefore at most one residual source uses a fixed target.

### 4.3 A star source and a residual source cannot coexist

If both types used the same target, the star center is distinct from both residual centers: a valid residual center has exactly the three target incidences prescribed by the induced `Q7` structure, whereas the star center has four.

The union would have the six target vertices and three removed centers, hence nine vertices. The residual source contributes six target-incidence edges and the star source contributes four more, for ten distinct edges. This cannot be a subgraph of a forest.

Hence a four-unit target receives **at most one deficit-one source in total** from the old E4-S matching plus the new residual class. Its surplus is two by (3), so the combined matching has spare capacity.

## 5. Conclusion

Every negative `j=4` group is either

1. already in E4-S classes A or B, whose total deficit is matched there; or
2. the unique residual type `Q7 union K1`, whose deficit is matched to a four-unit target without overloading any E4-S target.

All unmatched group surplus is nonnegative. Summing over all admissible groups gives

```text
L_4(F) = p_4(F)^2 - p_3(F)p_5(F) >= 0
```

for every finite simple undirected unweighted forest `F`.

This proof handles zero coefficients and plateaus because it is an integer signed-count injection/capacity argument; no division by a coefficient is used.

## 6. Consequence for the project

Phase 11 proved the corresponding global minor at `k=3`, and earlier work covers `k=1,2`. This phase adds `k=4`. Therefore any failure of the project’s stronger prefix log-concavity condition `PREFIX_BETA` must occur at index

```text
k >= 5.
```

This does **not** prove the full independent-set sequence is log-concave, and it does **not** prove Erdős #993. A non-log-concave position at a later index would still not by itself be an original counterexample; an original counterexample must have a genuine decrease followed later by a genuine increase in the whole independent-set sequence.

## 7. Evidence boundary

The finite classification is the only new computer-assisted part of this phase. It was run twice with independent generators:

* Prüfer-sequence generation of every labeled tree through order eight;
* direct `(n-1)`-edge subset generation inside `K_n`, retaining exactly the connected acyclic graphs.

Both executions completed and produced identical order-by-order totals and the same unsplittable-high counts: 630 labeled `Q7` copies at order seven and 3360 labeled `Q8` copies at order eight, with no other unsplittable high tree through order eight.

No new Lean build or axiom audit was run. Review in this phase is same-model self-review, not independent external peer review. No novelty, priority, organizer acceptance, solver status, or prize entitlement is claimed.
