# Exact statements and scope

This package gives a computer-assisted mathematical proof of FAMILY-LC and hence
FAMILY. It does not give a Lean proof or solve ORIGINAL. See VERDICT.json.

## Standard graph and counting semantics

A finite simple undirected graph is a finite vertex set V and a set of unordered
two-element subsets of V called edges. A forest is such a graph with no cycle.
The empty graph, isolated vertices, and disconnected forests are included.
An independent set is a subset U of V containing no edge. Define

    i_k(G) = |{ U subset V : |U|=k and U contains no edge }|,
    I(G;x) = sum_{k=0}^{|V|} i_k(G) x^k.

These are actual unweighted subset counts, not definitions through a recurrence.
Write i_k=0 outside 0..|V|. A finite sequence a_0,...,a_n is unimodal if some
m in 0..n satisfies a_0<=...<=a_m>=...>=a_n. Equalities are permitted.
Log-concavity means a_k^2>=a_{k-1}a_{k+1} at every interior index. For the positive
initial support occurring here, log-concavity implies unimodality.

## The palette B59

The following disjoint rows enumerate all permitted sorted branch tuples:

| Tuple | Inclusive range | Count |
|---|---|---:|
| (s) | 3<=s<=17 | 15 |
| (2,b) | 6<=b<=14 | 9 |
| (3,b) | 5<=b<=13 | 9 |
| (4,b) | 4<=b<=12 | 9 |
| (5,b) | 5<=b<=11 | 7 |
| (6,b) | 6<=b<=10 | 5 |
| (7,b) | 7<=b<=9 | 3 |
| (8,8) | one tuple | 1 |
| (5,5,5) | one tuple | 1 |

Total: 59. A second equivalent generator uses d=1,2,3, nondecreasing entries in
2..17, and accepts precisely: d=1 with entry at least 3; d=2 with first entry 2
and second 6..14, first entry 3 and second 5..13, or first entry a in 4..8 and
second a..16-a; d=3 with all entries 5. The checker compares the two sets.

## Actual FAMILY graphs

Choose any positive integer t and any ordered list sigma=(s_1,...,s_t) of members
of B59; repetitions are allowed. Begin with the edge {r,h}. For each i, attach a
fresh vertex u_i to h. For each entry s_ij of s_i, attach a fresh center c_ij to
u_i, and attach s_ij distinct fresh leaves to c_ij. No other edges are present.
Call this tree T_sigma and call its induced subgraph deleting r, T_sigma-r.
All added vertices are new, so the construction produces a simple tree.

Put S_i=sum_j s_ij, d_i=length(s_i), S=sum_i S_i, D=sum_i d_i. The respective
vertex counts are 2+t+D+S and 1+t+D+S. Define explicit polynomials

    Q_i = product_j ((1+x)^(s_ij)+x),  R_i=(1+x)^S_i,  H_i=Q_i+x R_i,
    A=product_i H_i, Q=product_i Q_i,
    E=A+xQ, P=(1+x)A+xQ.

MAIN_PROOF proves, from independent subsets, I(T_sigma-r;x)=E and I(T_sigma;x)=P.
The graph-to-polynomial identities are part of the theorem, not assumptions.

**FAMILY:** For every t>=1 and every such sigma, both actual independent-set
count sequences are unimodal.

**FAMILY-LC (proved strengthening):** Under exactly the same quantifiers, both
actual count sequences are log-concave. This strengthens, but does not redefine,
the requested FAMILY statement.

## ORIGINAL — a separate, unresolved target in this package

For every finite simple undirected forest F, the sequence i_0(F),...,i_|V|(F) is
unimodal; alternatively, disprove this by providing an actual unweighted forest
and exact counts with i<j, a_i>a_(i+1), and a_j<a_(j+1).

FAMILY is a restricted class of connected trees. Its closure is not a claim that
all forests are covered. Neither the 25-to-30 vertex non-log-concavity control
nor any failed sufficient inequality is an ORIGINAL counterexample.
