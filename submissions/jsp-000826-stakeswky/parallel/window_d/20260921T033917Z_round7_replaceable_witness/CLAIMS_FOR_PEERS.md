# D7 replaceable-witness interfaces v1

Run: 20260921T033917Z_round7_replaceable_witness.
Initial observed HEAD: d9707fe9859fa015f5dc0ba8906b798ec6bb4857.
ORIGINAL=NOT_CLOSED. These are research targets, not proved theorems.
D6 space run 011500Z and remote interface run 011340Z are distinct.

## Definitions
All graphs are finite simple undirected unweighted forests. I(G) counts
independent vertex subsets by size, with zeros outside positive support.
Unimodality allows plateaus. For a nonzero unimodal Q, M(Q)=[ell_Q,r_Q]
is its FULL maximum interval; dist([a,b],[c,d])=max(0,c-b,a-d).
LOCAL(G): all I(G-v), xI(G-N[v]) are unimodal. HEREDITARY(G): every proper
induced subforest is unimodal. LOCAL is not HEREDITARY.
A leaf pair l--w is good in G precisely when dist(M(I(G-l)),M(I(G-w)))<=1.

## D7-NEW-LOCAL-v1: immediate replacement test (UNPROVED)
For EVERY H, vertex r of H, and new vertex z, let F=H+edge rz. Assume H and F
are nonempty, isolate-free, K2-component-free and LOCAL. Assume an old leaf
l!=r with support w survives as a leaf, is good in H, and is bad in F.
Candidate conclusion: the NEW leaf pair z--r is good in F.
The parallel HEREDITARY variant adds HEREDITARY(F); it is NOT refuted by a
LOCAL-only example. The new pair is determined, but the old lost witness
may be ANY surviving leaf; a counterexample needs one lost witness and a
bad new pair, not all leaves bad. Keep all remaining leaf pairs to identify
more distant replacements. This tests a stronger proposed replacement rule,
not ADMC itself; a failure is NOT a reason to stop the wider replacement route.
No graph-order, History, valley, LC, or distance-from-r assumption is added.

The exact updates, with repeated deletions interpreted as set deletion, are
 A_v(F)=A_v(H)+x I(H-{v,r}) for every old v,
 A_z(F)=I(H), A_r(F)=(1+x)I(H-r).
When r was an old leaf it is no longer a leaf of F. Do not drop other components.
Refutation: supply H,r,z,F, all full A/B arrays for both graphs, full peak
intervals, the lost edge, the bad new edge, all alternative leaf pairs, full
P and its valley test. Verify LOCAL in both; certify HEREDITARY separately
or label it UNKNOWN. Recount the decisive graph data by two algorithms.

## D7-MIN-RSM-v1: actual minimum-counterexample route (UNPROVED)
Suppose F is nonunimodal and EVERY forest with fewer vertices is unimodal.
Choose i as the first strict descent index of P=I(F), and j>i as the first
later strict ascent index (zero differences between are allowed). For each
vertex put A_v=I(F-v), B_v=xI(F-N[v]), and
 U=max_v min(r_Av,r_Bv), D=min_v max(ell_Av,ell_Bv).
The inherited reductions give no isolates or K2 components and U<=i<j<D.
Target: SOME leaf l with support w blocks THIS pair. For the SAME actual edge,
 C=I(F-{l,w}), J=I(F-N[w]),
 A_l=C+xJ, B_l=xC, A_w=(1+x)C=X, B_w=xJ=Y.
Block means neither ordering (E,L) of (X,Y) is polarized, or the polarized
ordering obeys Q=Delta L_i*(-Delta E_j)-Delta L_j*(-Delta E_i)>=0.
Polarized means Delta E_i<0, Delta E_j<=0, Delta L_i>=0, Delta L_j>0.
This would contradict the real valley and prove ORIGINAL. It is the OLD
RSM obstruction restricted to actual minimum bad graphs/actual valley pairs,
not a newly proved restriction. A merely minimal ADMC failure need not have
any valley and cannot be assigned these signs. No same-order edge deletion
or weighted-graph minimality is implicit. The leaf may depend on the pair.

## Unchanged broader statements and boundaries
ADMC still asks for SOME good leaf pair in every nonempty isolate/K2-free
HEREDITARY forest. J_H has the same domain and concludes D<=U+1. The original
RSM uses the nonempty isolate-free HEREDITARY domain with NO added K2
exclusion and EACH U<=i<j<D, with a possibly different witnessing leaf.
All-bad LOCAL and all-bad HEREDITARY are separate; neither automatically
means a whole-sequence valley. The D5 generic LC-cofactor rule is false;
D6 even refuted LOCAL specified-actual-edge preservation. Neither is used.
B5/B6 positive full-leaf reports were read, not counted as new executions.
A6 space leaf/path proof was read. The remote long-connector PROOF.md returned
404 at the initial HEAD, so its early interface is not used as an input lemma.

## Release and evidence
This version precedes the new computation; later outcomes will be separate.
Certificate path: certificates/KEY_CERTIFICATE.json (not yet produced).
Sources: exact Round7 task; mounted D6 011500Z proof/gap/review/claims and
certificate; B6 011605Z report; A6 014921Z space proof. Source hashes will be
retained in SOURCE_AUDIT.json. Publication is not a receipt that B read this.
