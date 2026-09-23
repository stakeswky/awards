# Statements

Run `20260923T063246Z_independent_colour_mass_audit` (independent Claude window).
ORIGINAL=NOT_CLOSED. Nothing here proves Erdős #993 or gives a counterexample.

## Definitions (as in the project hand-off)

F is a finite simple undirected unweighted forest with n vertices; p_r is the number of
independent r-sets (p_0=1, zero outside the support); alpha is the independence number;
M is the largest component order.

    h = floor(M(n-1)/(4M-2)) + 1,     beta = ceil(alpha(n-1)/(n+alpha)).

History(F,k): there is i<=k with p_i > p_{i+1} >= p_{i+2} >= ... >= p_{k+1}.
With j=k+1: b=p_{j-1}, a=p_j, c=p_{j+1}, and S = a(b-a).
The project's remaining middle range is h+1 <= j < beta together with History(F,j-1).

Fix a proper 2-colouring (L,R). f_r(l) counts independent r-sets with exactly l vertices in L.

    N_t = sum_l f_{j-1}(l) f_{j+1}(t-l),   P_t = sum_l f_j(l) f_j(t-l),
    Dmass_j = sum_t max(N_t - P_t, 0).

For a tree, the two colourings give the same Dmass (the global swap reverses t).
delta_e is the exact C10 leaf-edge deficit (leaf u, support v, K=F-{u,v}, J=F-N[v]):

    delta_e = max_U { sum_{t in U}(N_t-P_t) - sum_{t in U, t+1 notin U} c_t^+ - sum_{t in U, t-1 notin U} c_t^- }.

U ranges over all subsets of masses.

Useful rewriting. Let X = sum_t max(P_t - N_t, 0). Since sum_t N_t = bc and sum_t P_t = a^2,

    Dmass - S = X - b(a-c).

So Dmass <= S is equivalent to X <= b(a-c), which is strictly stronger than c <= a.
In the language of polynomial sequences, Dmass=0 means that F_r(z) = sum_l f_r(l) z^l is
z-log-concave (q-log-concave) at j.

## Conjectures tested (unproved)

**D\* (trees, all History positions).** For every finite tree T and every j>=1 with
History(T,j-1): Dmass_j(T) <= S_j(T).

D\* at every History position implies unimodality of T. D\* gives c<=a, so History(T,j) holds,
and induction from the first strict descent finishes the argument. Proving D\* is therefore
at least as hard as the tree case of #993. D\* is proposed as a cleaner, stronger induction
hypothesis, not as an easier route.

**D\*_mid.** The same as D\*, restricted to the middle range h+1 <= j < beta. This is the
project's "automatic colour-mass entrance" (E9/E10) for trees.

**C\*_mid.** For every tree T and every middle-range j with History(T,j-1), there is ONE leaf edge
e with delta_e <= S (exists e, for all U). This is the Round-11 C target for trees.

Forests with several components are **not** covered. Each component's colouring may be flipped,
so a forest version must quantify over colourings.

## Proved statements (PROOF.md)

**Lemma 1 (deletion identity; every finite simple graph).** For all j>=1,

    sum_v T_v - p_{j-1} p_j = (n-2j) p_{j-1} (p_j - p_{j+1}),
    T_v = A^v_{j-1}(A^v_j - A^v_{j+1}) - B^v_{j-2}(B^v_{j-1} - B^v_j),

where A^v_i = p_i(G-v) and B^v_i = p_i(G-N[v]). It holds for graphs with cycles, so it carries no
forest-specific sign information. This confirms the Round-10 coordinator remark.

**Lemma 2 (subdivided double star).** Let l>=3 and let T=hubs(2,l) be the centre joined to two
hubs, each hub carrying l leaves (n=2l+3). Put j=l+1 and A=C(2l+1,l+1). Then:

1. the first strict descent of p(T) is at index l, so History(T,j-1) holds;
2. alpha=2l+1 and beta=l+1=j, so j is the tail boundary and lies outside the middle range;
3. a=A+2, b=A+2l, and S=(A+2)(2l-2);
4. Dmass_j=0 for l=3, and Dmass_j = 2A(l^2-2l-4)/(l+2) for l>=4.

Hence

    Dmass/S = A(l^2-2l-4) / ((A+2)(l^2+l-2)) < 1,   and   Dmass/S -> 1 as l -> infinity.

**Corollary (the constant in D\* is sharp).** For every eps>0 some tree has a History position
with Dmass > (1-eps)S. So "Dmass <= S" cannot be strengthened to "Dmass <= cS" with c<1
uniformly over all History positions. The extremal positions sit at j=beta, however, so the best
constant for D\*_mid is unknown. The largest value observed in the tested sets is 0.31479
(hubs(5,40), j=101).

## Computational claims (exact integer arithmetic; see results/ and provenance/)

| Claim | Coverage | Outcome |
|---|---|---|
| D\*_mid and C\*_mid | all 23,942,354 free trees with 5<=n<=23 (orders n<=4 have an empty middle range) and every middle-range History position (8,586,082 positions) | no violation; no plateau (S=0) position occurs; max Dmass/S = 0.03177 and max over positions of min_e delta_e/S = 0.02703, both at n=18 |
| D\* at all History positions | every free tree with n<=19 (2,807,336 positions) | no violation; for every odd n from 11 to 19 the maximum is attained by hubs(2,(n-3)/2) at j=beta, equal to the Lemma 2 value (e.g. 7/32 at n=11) |
| D\* in families | hubs(t,l) with t<=6 and l<=40; 49,786 hub-variant trees (n<=80); 5,958 Kadrawi–Levit-type core trees (n<=90) | no violation; largest middle-range ratios are 0.3148, 0.1553 and 0 respectively |
| D\*_mid and C\*_mid at engineered near-ties | the 400 smallest (b-a)n/a positions among 62,455 in 62,688 hub-variant trees (n<=95) | no violation; b-a is as small as 1 and Dmass=0 exactly in 40 positions |
| Boundary claims (strict increase through h and through ceil(n/4); no rise from beta on) | all 1,346,021 free trees with 4<=n<=20 | no violation |

All counts above are taken from the primary run's outputs in `results/`; SHA256 of every output is in
`provenance/RUN_RECEIPT.json` (status PASS, 10/10 steps, tree counts equal to OEIS A000055 for every swept order).
