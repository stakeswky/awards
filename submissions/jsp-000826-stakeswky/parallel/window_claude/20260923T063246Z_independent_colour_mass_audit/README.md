# Independent Claude window: colour-mass entrance audit and assessment

Run: `20260923T063246Z_independent_colour_mass_audit` (window `claude`, independent of windows A–E).

**ORIGINAL=NOT_CLOSED.** This is a research record. It does not prove Erdős #993, does not give a
counterexample, and makes no award, priority or eligibility claim. PR #1 stays Draft and
unmerged. The shared `RESEARCH_STATE.json`, other windows' directories, main, and all catalog and
award records are untouched.

This work used Anthropic Claude (Claude Code). The project windows used OpenAI ChatGPT, so this is
a cross-model reconstruction. It is **not** an independent human or external peer review.

## What is here

| File | Content |
|---|---|
| `STATEMENT.md` | Definitions; the tested propositions D\*, D\*_mid and C\*_mid; Lemma 1, Lemma 2 and the Corollary; coverage table |
| `PROOF.md` | Proofs of Lemma 1 (deletion identity holds for all graphs) and Lemma 2 (exact Dmass/S for hubs(2,l), so the constant 1 is sharp), plus a clearly labelled heuristic |
| `CLAIMS_FOR_PEERS.md` | Frozen, falsifiable propositions with exact failure certificates, and where to search |
| `GAP.md` | First unproved arrows; coverage and evidence limits |
| `REVIEW.md` | Second implementations and cross-checks; conventions; known weaknesses |
| `ASSESSMENT_AND_NEXT_STEPS.md` | Independent assessment of the project state and proposed priorities |
| `SOURCES.md` | Inputs read, with hashes; external sources, split into first-hand and sub-agent-reported |
| `VERDICT.json` | Machine-readable status |
| `src/` | Complete source (standard-library Python); `run_all.py` runs everything |
| `results/` | Every output of the primary run, logs included. Key certificates: `results/KEY_CERTIFICATES.json` and `results/sweep_witness_nXX.json` |
| `provenance/` | `RUN_RECEIPT.json` (primary run; its output paths are relative to `results/`), `REPLAY.json` (clean-source replay), `ROUND10_COORDINATOR_REPLAY.json`, `EXPLORATORY_RUN.json` |

## Main outcomes (exact arithmetic)

1. **Middle range, all trees n<=23.** No tree with n<=23 violates Dmass<=S (D\*_mid) or
   "exists e, delta_e<=S" (C\*_mid) at any middle-range History position. That is 8,586,082
   positions across 23,942,354 trees. The largest Dmass/S at any order is 0.03177, at n=18.
2. **All History positions, all trees n<=19.** No tree with n<=19 violates Dmass<=S at any History
   position, tails included. The supremum over History positions is exactly 1, attained in the
   limit by the subdivided double star hubs(2,l) at j=beta (Lemma 2).
3. **Families.** hubs(t,l), 49,786 hub variants, and 5,958 Kadrawi–Levit-type core trees give no
   violation. The largest middle-range ratio is 0.3148. Engineered near-plateaus with b-a=1 have
   Dmass=0 exactly.
4. **Boundary claims.** Strict increase through h and through ceil(n/4), and no rise from beta on,
   hold for all trees n<=20.
5. **Round-10 coordinator audit.** Its replay from the hand-off package matched the packaged receipt
   byte for byte.

## Reproduce

Python 3.10 or newer, standard library only, no network:

    python src/run_all.py --out <new empty directory> --maxn 23
    python src/replay.py --reference <that directory> --workdir <another new directory> --maxn 21

`--maxn 23` takes about half an hour on a 10-core machine; `--maxn 21` takes a few minutes. Compare
outputs with `provenance/RUN_RECEIPT.json`, which records the SHA256 of every result file.
