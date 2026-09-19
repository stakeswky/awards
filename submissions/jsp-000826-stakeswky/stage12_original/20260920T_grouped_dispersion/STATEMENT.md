# Results: grouped bound refuted; an all-length LC family proved

**ORIGINAL NOT_CLOSED. Exact BARRIER remains unresolved.**
**General core: NO_STRUCTURAL_ADVANCE.**

The user-facing Phase-10 separator estimate grouped root-selection states by the number of selected branching vertices. This sufficient estimate is stronger than the exact no-rebound condition. For its notation, the exact grouping error is

    E_group = sum_s pi_s(h_g-r_s)(r_s-l_g) >= 0,
    grouped slack = (p_(k+1)-p_(k+2))/p_k - E_group.

The universal stronger estimate is FALSE. The precise exact condition is NOT refuted.

## Actual counterexamples to the grouped estimate

1. Take 58 disjoint copies of the claw and 58 copies of the subdivided claw. This forest has 638 vertices. At k=206<beta-1=247 it strictly decreases twice, yet E_group>=14695949545/10^12 exceeds its next normalized decrease, which is less than 0.01299734. It is LC and HEREDITARY; the latter follows from complete induced-subset checks of the two small base trees and LC convolution.
2. Take a backbone path on 204 vertices, alternating A and B. At each A attach three new leaves; at each B attach three private two-edge paths. This connected tree has 1122 vertices, alpha=714 and beta=436. At k=363 it has p_363>p_364>p_365 and U=D=363. Its grouping error is in [7692939575,7692944726]/10^12, while its next normalized decrease is in (740577,740578)/10^8. Thus the grouped sufficient inequality fails strictly inside the middle domain. Its whole sequence is LC. HEREDITARY remains UNKNOWN for this connected witness.

Neither graph is an ORIGINAL, exact BARRIER, PREFIX_BETA, J_H or RSM counterexample. Neither refutes a version restricted to actual non-unimodal minimal counterexamples. No global minimality is claimed.

## Continued exact route: all backbone lengths

Let F_r be the connected construction above with 2r backbone roots, r>=1. A whole-graph transfer gives P_0=1, P_1=T and P_r=T P_(r-1)-D P_(r-2), with fixed explicit polynomials T and D. Pairing the sine-recurrence roots gives

    P_r = T^(r mod 2) product_j [T^2-c_j D],
    c_j=4cos^2(j*pi/(r+1)) in [0,4].

Every coefficient and every LC minor of every factor is positive throughout [0,4], by the complete 39-entry positive Bernstein certificate. T is LC too. Convolution closure therefore proves that EVERY F_r is LC, and so is any finite disjoint union of these F_r trees. This is an all-parameter proof, not extrapolation from finite lengths. Arbitrary attachments or arbitrary non-LC cofactors are not covered. No novelty claim.

## Verification and remaining gap

Two fixed whole-graph sequences are independently recounted. All 8837 compressed root-state classes are covered, with all 26511 relevant coefficient entries independently checked. All 3520 vertex A/B arrays are computed; 48 selected A/B arrays are independently recounted. The exact full coefficients and rational sign evidence are reproducible from source. Three programs were freshly rerun and six complete deterministic outputs matched all bytes.

The general missing implication is still: actual arbitrary forest compatibility implies the EXACT plateau-safe no-rebound condition. Refining groups to singleton states merely recovers that condition; it does not prove it. Concurrent remote private-arm and global-L3 work is preserved. No external census replay, original forest counterexample, full ORIGINAL proof, Lean build, axiom audit or independent external review is claimed.
