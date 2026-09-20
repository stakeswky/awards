# Statements tested and scope of conclusions

## ORIGINAL

F is a finite simple undirected unweighted forest, possibly empty or disconnected. p_k counts independent k-subsets, p_0=1. Alpha is the last positive coefficient. There must be a peak m with p_0<=...<=p_m>=...>=p_n. A refutation requires actual indices i<j with p_i>p_(i+1) and p_j<p_(j+1). The scan retains zero differences between i and j; it never identifies non-log-concavity or a first plateau followed by growth as an original failure. Positive support is padded by zeros through n for the separate definition-based scan.

Outcome: no original failure; NOT_CLOSED.

## A prior prefix theorem: integer regression, not a new proof claim

A's complete proof `Window_A_Proof_and_Gap.md` was read. Its short extension-count proof uses

    mu_(k+1) = mu_k - 1 + (Var(T)-2 E[e(F-N[S])])/mu_k,
    E[e(F-N[S])] <= (1-1/M)mu_k,

and obtains the LOWER bound mu_k>=n-3k+2k/M. It does not prove an upper bound that forbids rebounds. The rooted charge proof and the exact exterior/component products were also read. No root-charge coefficient positivity is silently interpreted as log-concavity.

Every completed graph uses its newly computed M=max component order and tests

    M(k+1)p_(k+1) >= [M(n-3k)+2k]p_k.

There were zero failures. This is a regression check of the actual published theorem, not a finite-data proof of universality or external peer review. The inherited Basit-Galvin theorem gives beta=ceil(alpha(n-1)/(n+alpha)) and a nonincreasing tail from beta. Its actual whole-graph scope was verified in the primary paper's HTML version. No theorem on connected graphs is improperly applied only to individual components.

Use h=floor(M(n-1)/(4M-2))+1. A first descent and later first rise must satisfy h<=i<j<beta. Thus the necessary middle negative minor is at h+1<=j<beta. This necessary condition is not sufficient.

## A2-C1: exact published claim

Source: A `20260920T0323Z_middle_bridge/CLAIMS_FOR_B.md`, blob `38eaa9926194035bb1f66afb3dc4afcac8a8cfeb`, first published at 05470e82 and reread at 7cecd228.

For every forest and 0<=k<alpha-1, A requested testing

    mu_(k+1) <= mu_k+1,
    C1_k=(k+1)p_(k+1)^2+p_k p_(k+1)-(k+2)p_k p_(k+2) >=0.

There is no LOCAL, HEREDITARY or minimality premise. This universal claim is **REFUTED**, by the attributed actual B(8,14) and its locally reduced 212-vertex descendant. Both failures are outside k+1<beta and are not original counterexamples. No claim of a new literature discovery is made.

As requested, the previous 1,546 stored arrays and 23 non-LC bank arrays were scanned first: respectively 357,666 and 4,356 C1 indices, with zero failures. These are archived-array checks, not fresh whole-graph recounts. New stored-corpus checks found 44 C1 failures, all tail-only. Every such stored failure graph was independently recounted in the final audit.

## A2-C2: history check

A requested that every C1 failure with k+1<beta record whether there is i<=k with Delta_i<0 and all Delta_i,...,Delta_k<=0. There were **0 middle C1 failures**, so nonvacuous failure-history tests for A2-C2 are **0**. This is not a proof of C2 or of history-restricted no-rebound.

## Exact BARRIER and equalities

For 0<=k<beta-1, p_(k+1)<=p_k would imply p_(k+2)<=p_(k+1). This sufficient route is not assumed true. A failure beginning with equality and no earlier strict descent would refute only this stronger history-free statement unless a later/earlier true valley is also shown.

The stored graph union has 16,035 strict-descent premises and 91 exact equality premises. No next-step rise was found. All 91 equalities lack earlier strict descent and have a strict next decrease. Middle equalities after a prior descent: **0**. Tail equalities and synthetic numerical tests are not substituted for them.

The previously refuted selected-count grouped-range estimate was not used.

## U/D and conditional graphs

Only the five fully profiled material graphs receive full U,D labels. All are LOCAL. The raw residual-pair sets and the refined max(h,U)<=i<j<min(beta,D) sets are empty. Unchecked vertices in other graphs do not create full U/D coverage. HEREDITARY is not claimed. There were no non-unimodal conditional forests to extract as original candidates.

Later A status files must not substitute for actual proof text. At the intermediate head 7cecd228, the new A PROOF_ATTEMPT.md contained a file-retrieval error string rather than the claimed decomposition proof. It was not used as a proved theorem or as an additional test target. The complete prior A proof and the explicit actual C1/C2 claim file were available and used.
