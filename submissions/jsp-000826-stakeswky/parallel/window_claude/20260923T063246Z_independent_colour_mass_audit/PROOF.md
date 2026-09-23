# Proofs (Lemma 1, Lemma 2, Corollary) and a heuristic remark

Scope: only the two lemmas and the corollary stated in STATEMENT.md are proved here. D\*,
D\*_mid and C\*_mid are **not** proved. ORIGINAL=NOT_CLOSED.

## Lemma 1 (deletion identity, all finite simple graphs)

Let G have n vertices. Write I_s for the family of independent s-sets and p_s = |I_s|.

**Claim A.** For every vertex v, a pair (I,J) of independent sets of G lies in G-v exactly when
v is in neither I nor J. Hence

    sum_v p_s(G-v) p_t(G-v) = sum_{(I,J) in I_s x I_t} (n - |I u J|).

**Claim B.** The map (I',J') -> (I'+v, J'+v) is a bijection. Its domain is the set of pairs of
independent (s-1)- and (t-1)-sets of G-N[v]. Its range is the set of pairs in I_s x I_t that both
contain v. Hence

    sum_v p_{s-1}(G-N[v]) p_{t-1}(G-N[v]) = sum_{(I,J) in I_s x I_t} |I n J|.

**Combining.** |I u J| + |I n J| = |I| + |J|, so for each pair the two contributions combine to
n - |I| - |J|. Expanding T_v and applying Claims A and B with (s,t)=(j-1,j) and (j-1,j+1):

    sum_v T_v = sum_{I_{j-1} x I_j} (n-2j+1) - sum_{I_{j-1} x I_{j+1}} (n-2j)
              = (n-2j+1) p_{j-1} p_j - (n-2j) p_{j-1} p_{j+1}
              = p_{j-1} p_j + (n-2j) p_{j-1} (p_j - p_{j+1}).

No property of forests is used. `check_bounds.py` additionally verifies the identity by literal
enumeration on 60 random general graphs (seed 7), most of which contain cycles. ∎

## Lemma 2 (hubs(2,l) at j=l+1)

Colour the centre and all 2l leaves L, and the two hubs R. Let x mark L-vertices and y mark
R-vertices. Conditioning on the centre gives

    Z(x,y) = ((1+x)^l + y)^2 + x(1+x)^{2l} = (1+x)^{2l+1} + 2y(1+x)^l + y^2.

So g_r(m), the number of independent r-sets containing exactly m hubs, is

    g_r(0) = C(2l+1, r),   g_r(1) = 2 C(l, r-1),   g_r(2) = [r=2],

and p_r = g_r(0) + g_r(1) + g_r(2). Put A = C(2l+1,l+1) = C(2l+1,l). Then C(2l+1,l+2) = A l/(l+2).
Throughout, l>=3, so g_r(2) = 0 for r in {l, l+1, l+2}.

**(1) History.** p_l - p_{l+1} = 2(C(l,l-1) - C(l,l)) = 2(l-1) > 0.

For 1 <= r <= l-1, first note that C(2l+1,r+1) - C(2l+1,r) = C(2l+1,r)(2l-2r)/(r+1). Vandermonde
gives C(2l+1,r) >= (l+1)C(l,r-1). Therefore this difference is at least
(l+1)C(l,r-1)(2/(r+1)) > 2C(l,r-1), which dominates the possible decrease of 2C(l,r-1).

The g(2) terms change p_2 - p_1 by +1. They change p_3 - p_2 by -1, which is absorbed because
C(2l+1,2)(2l-4)/3 >= 14 > 2l+1 when l=3, and the gap only grows with l.

Hence p increases strictly up to index l and first descends strictly at l. So History(T,l) holds.

**(2) Tail boundary.** The L-class is independent, so alpha >= 2l+1. A set with one hub has at most
1+l vertices, and a set with two hubs has at most 2, so alpha = 2l+1. With n=2l+3,

    beta = ceil((2l+1)(2l+2)/(4l+4)) = ceil(l + 1/2) = l+1 = j.

**(3) The three terms.**

    a = p_{l+1} = A + 2C(l,l) = A+2,
    b = p_l = A + 2C(l,l-1) = A+2l,
    S = a(b-a) = (A+2)(2l-2).

**(4) Mass classes.** An r-set with m hubs has r-m vertices in L. Every pair counted by N or P has
total size 2j. So its mass is t = 2j - mu, where mu is the total number of hubs in the pair, and
the mass classes are exactly mu = 0, ..., 4.

- mu=0: N-P = C(2l+1,l)C(2l+1,l+2) - A^2 = A^2(l/(l+2) - 1) < 0.
- mu=1: N = g_l(0)g_{l+2}(1) + g_l(1)g_{l+2}(0) = 0 + 2l·A l/(l+2), and P = 2g_{l+1}(0)g_{l+1}(1) = 4A.
  So N-P = 2A(l^2-2l-4)/(l+2).
- mu=2: N = g_l(1)g_{l+2}(1) + g_l(0)g_{l+2}(2) + g_l(2)g_{l+2}(0) = 0, and P = g_{l+1}(1)^2 + 0 = 4.
  So N-P = -4.
- mu=3,4: every product contains a factor g_r(2) with r in {l, l+1, l+2}, so N = P = 0.

The only possible positive class is mu=1. Hence Dmass = max(0, 2A(l^2-2l-4)/(l+2)). This is 0 for
l=3, where l^2-2l-4 = -1, and positive for l>=4. It is an integer because A l/(l+2) = C(2l+1,l+2).
Dividing by S:

    Dmass/S = A(l^2-2l-4) / ((A+2)(l+2)(l-1)) = A(l^2-2l-4) / ((A+2)(l^2+l-2)).

This is < 1 because l^2-2l-4 < l^2+l-2 and A < A+2, and it tends to 1 because A -> infinity. ∎

`check_hubs_closed_form.py` asserts items (1)-(4) and the exact rational identity for every
l = 3..80 by direct computation. That is a finite check of the proved formula, not the proof.

**Corollary.** Take l large. Dmass/S exceeds any fixed c<1 at a History position, so the constant 1
in D\* is optimal over all History positions. Since j=beta there, this does not decide the optimal
constant of D\*_mid. ∎

## Heuristic remark (NOT a proof): why hub trees stay below S

The following is a leading-order analysis. Its only purpose is to explain the numbers.

Take hubs(t,l) with tl even and j = tl/2+1. Let A_r = C(tl+1,r) be the hub-free population, which
is tied at j-1 and j. Let B_r = t C(l(t-1), r-1) be the one-hub population, which is already past
its mode. Write rho_A = A_{j+1}/A_j. To leading order, the mu=1 class contributes

    N_1 - P_1 - A(B_{j-1} - B_j) = A[(B_{j+1} - B_j) - (1-rho_A)B_{j-1}],

which is <= 0 whenever B_{j+1} <= B_j. The resulting ratio estimate is

    (1-rho_B) - (1-rho_A)/(1-rho_B) - rho_B(rho_B - rho_B')/(1-rho_B),   rho_B = B_j/B_{j-1} ≈ 1 - 2/t.

This gives 0.182 for hubs(5,16), against the observed 0.18196.

Interpretation: a positive colour part can exceed S only if some colour-graded sub-population is
still **increasing** at j while the total is not increasing. That is also the only way a genuine
valley could form. This suggests a precise adversarial target for counterexample searches (see
CLAIMS_FOR_PEERS.md), and a decomposition to try in a proof of D\*.
