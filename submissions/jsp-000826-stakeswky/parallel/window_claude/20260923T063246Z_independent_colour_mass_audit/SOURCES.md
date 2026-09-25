# Sources and access levels

## Inputs actually read

**Hand-off package** `Erdos993_Project_Summary_20260923` (packaged 2026-09-23; Round-10
baseline). All 36 files match the SHA256 values in its `MANIFEST.json`
(manifest SHA256 `e82fc39bcb134c2cd1a6ecf18584ecd2b71fac91d914ab444db9383eba274993`). Read in
full:

- the overview, the original-problem statement, the progress summary, the working protocol,
  the technical notes, the coordinator start prompt, and `STATUS_SNAPSHOT.json`;
- the historical coordinator audits for Rounds 5 through 11;
- the four Round-11 task prompts and the Round-11 common protocol;
- `evidence/Erdos993_Round10_Audit/*`: source code, results and receipt. This was also
  replayed (`provenance/ROUND10_COORDINATOR_REPLAY.json`).

The A9 proof, the C10/E10 full papers and the author archives are **not** in the package and
were not read.

**Repository** `stakeswky/awards`, branch `jsp-000826-research-snapshot`, read at
`af71b798342cec6e5169fb1d7900a37942acd082`:

| File | SHA256 |
|---|---|
| `submissions/jsp-000826-stakeswky/RESEARCH_PROTOCOL.md` | `21da4392252bb4d8ddc44f6c361f1f56f8c4c261dfc5b20526630619d1893484` |
| `submissions/jsp-000826-stakeswky/RESEARCH_STATE.json` | `8d9663931b1fed209a8488129200d84e10c248cd58add4602736405d540915dd` (read, **not modified**) |
| `submissions/jsp-000826-stakeswky/README.md` | `4670f9b33c03b86fe5c1cc7899a0d927542f2fac3e79e6434943e2ac88f16eec` |

The directory `parallel/window_a/20260921T161559Z_round9_effective_cutoff/` was read only as a
layout and format reference.

**Vendored code.** `src/third_party/graph_primitives.py` is a byte-identical copy of the
hand-off package file `evidence/Erdos993_Round10_Audit/src/graph_primitives.py` (SHA256
`e44127ffac665fbdfd01a3398d86864da09a9ca4248d73a9497d7aa6bc04a0ed`). It is the project
coordinator's own polynomial code, used here only as a second implementation.

## External sources

### Read first-hand on 2026-09-23 (web fetch of the public pages)

- **Fang, Lu, Nevo, Yao, Zheng**, *Unimodality of Independence Polynomials for Sufficiently
  Large Forests*, arXiv:2609.20961v1 (17 Sep 2026); abstract and HTML. Confirmed:
  - Theorem 1.1 is existential ("There is an absolute positive integer N0 such that …"), and no
    explicit N0 is given;
  - Theorem 1.2 gives central strict log-concavity for n/5 <= k <= 17 alpha/25 when n is
    sufficiently large;
  - Proposition 8.2 gives increase through ceil(n/4);
  - the decreasing tail from ceil((2 alpha - 1)/3) is attributed to Levit–Mandrescu;
  - §9: "the original conjecture for trees and forests of all sizes remains open";
  - the acknowledgement of the "Odin Automatic AI Research Agent".
- **erdosproblems.com/993**: status "FALSIFIABLE – Open, but could be disproved with a finite
  counterexample"; last edited 01 Feb 2026; 7 comments; 1 proof claim.
- **B. Reynolds**, Zenodo record 19100781, v3 (2026-03-18): unimodality verified for all
  8,691,747,673 trees with n <= 29; the conjecture is stated to remain open.

### Reported by a web-search sub-agent, not re-read first-hand

- **Basit–Galvin**, arXiv:2006.12562: Theorem 1.3 gives the tail from
  ceil(alpha(n-1)/(n+alpha)) for all graphs; the tree initial segment is
  ceil((n-alpha+1)/4).
- **Kadrawi–Levit**, arXiv:2305.01784: exactly two non-log-concave trees on 26 vertices, both
  failing at the tail. The first ends …, 2979, 51, 1, consistent with the project's T26.
- **Galvin**, arXiv:2502.10654: families failing log-concavity near alpha(1 - 1/(16 log alpha)).
- **Ramos–Sun**, arXiv:2510.18826: PatternBoost finds many non-log-concave trees on 27–101
  vertices.
- An erdosproblems forum comment reports exhaustive checks through n = 32. **Unverified.**
- google-deepmind/formal-conjectures has no merged Erdős 993 file (open PR).

## Execution environment

Everything was run on a local macOS workstation through Claude Code, with the Python 3.14
standard library only and no network access during computation. The exact versions are in
`provenance/RUN_RECEIPT.json`. No paid APIs were used.
