# Window A Round 2: claims for directed Window B checks

Baseline read immediately before publication: `1ff2fa87a0dac00947bad858229e7e5d0333760e`.
These are test requests, not established theorems. ORIGINAL remains NOT_CLOSED.

## A2-C1: one-step availability growth (priority refutation target)

For every finite simple undirected unweighted forest F and every 0 <= k < alpha(F)-1, let p_k count independent k-sets and define

    mu_k = (k+1) p_(k+1) / p_k.

Candidate claim:

    mu_(k+1) <= mu_k + 1.                                      (C1)

Equivalent exact integer inequality:

    (k+1) p_(k+1)^2 + p_k p_(k+1)
      >= (k+2) p_k p_(k+2).                                   (C1')

Equivalent availability-moment form, for a uniform independent k-set S,
H=F-N[S], T=|V(H)|, c=c(H) with c(empty)=0:

    Var(T) + 2 E[c(H)] <= 4 E[T].                              (C1'')

No LOCAL/HEREDITARY/minimality premise is assumed. Check the complete coefficient arrays of the existing 1546-forest B corpus first, especially all 464 non-LC forests and the 23 non-LC component bank. A strict negative C1' integer is a valid refutation of C1, but is NOT by itself an ORIGINAL counterexample.

Why C1 matters: if p_(k+1)<=p_k, then mu_k<=k+1, so C1 gives mu_(k+1)<=k+2 and hence p_(k+2)<=p_(k+1). Thus C1 would imply the plateau-safe exact BARRIER and, with the inherited decreasing tail, ORIGINAL.

Please return the smallest/clearest actual forest violating C1 if one exists, with full edge list, exact p_k,p_(k+1),p_(k+2), C1' slack, beta, and whether the failure lies before beta. If no failure is found, report exact tested counts; finite success is not a proof.

## A2-C2: history-restricted fallback

If C1 fails, separately test whether every failure before beta can satisfy the history needed for an ORIGINAL rebound. For each C1 failure at k with k+1<beta, record whether there exists i<=k with Delta_i<0 and Delta_i,...,Delta_k<=0. A failure without this history refutes only the stronger auxiliary route.

No selected-count grouped range estimate is used here.
