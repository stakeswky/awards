# Proof attempt: lexicographic minimality and edge budgets

Status: ORIGINAL NOT_CLOSED.

Choose a counterexample minimal first by |V| and then by |E|. Then for every edge uv, both F-uv and F/uv are unimodal: F-uv has the same number of vertices but fewer edges, while F/uv has fewer vertices.

Let C=I(F-{u,v}), H=I(F-(N[u]∪N[v])), and Z=x^2 H. Partitioning independent sets gives

I(F-uv)=P+Z,
I(F/uv)=C+xH,
CZ=B_uB_v.

If ΔP_i=-s<0<ΔP_j=t with i<j, unimodality of P+Z implies for every edge

ΔZ_i>=s OR ΔZ_j<=-t.

A separate counting injection gives for every k:
(B_u)_k+(B_v)_k<=P_k,
since independent k-sets containing u or v are disjoint classes inside all independent k-sets.

Combining these coefficient budgets with the earlier polarization variables yields extra endpoint inequalities. They reject the tested scalar relaxation that satisfied the earlier slope-only constraints. However, no argument proves that all real-forest residual configurations are impossible. The first unproved bridge therefore remains J_H, with RSM as an unresolved alternative.
