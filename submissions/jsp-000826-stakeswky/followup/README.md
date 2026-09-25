# Reproducible heterogeneous-branch follow-up

Date: 2026-09-17. Original problem counterexamples: **0**. This is a restricted written theorem and a bounded computational study, not a solution of Erdos #993.

## New mathematical scope

[The proof note](HETEROGENEOUS.md) extends the v2 identical-branch argument to arbitrary mixtures of 21 explicitly listed branch types, provided the number of branches is at least 70. It proves log-concavity of the full polynomial and one mixed deletion polynomial, together with the two distinguished root/hub decompositions' corridor condition. It does not prove the heterogeneous assertion for all smaller branch counts or for unrestricted branches.

The derivation uses a classical factorial-log-concavity convolution theorem. Base inequalities and the two positive-coefficient polynomial identities are reconstructed by the supplied integer code. This is **not a Lean formalization**, has not received external peer review, and carries no global novelty claim.

## Recorded experiment

| Stage | Records | Vertex range |
| --- | ---: | --- |
| Complete unordered multisets of 2 or 3 types from the 21-type palette | 2,002 | 12-59 |
| Deterministic irregular branch probes | 1,200 | 9-249 |
| Four large mixtures checking the theorem boundary | 4 | 907-926 |
| Total | 3,206 | 9-926 |

The final four records are proof regression controls, not new counterexample searches. There are 3,201 distinct unlabelled structures within this batch; no claim is made that they are globally new or absent from all earlier rounds. All original sequences and all checked conditional sequences were unimodal. No counterexample to the conditional corridor target was found.

The explicit branch formula and a full expanded-graph DP compared all 173,320 original coefficients. The separate deletion/closed-neighbourhood recurrence then checked every record and 6,412 root/hub decompositions, comprising 677,989 conditional coefficients. All-vertex metadata in the small records comes from the main message algorithm; it is not claimed to have been independently recomputed for every vertex by the deletion checker. The large records use only the root and hub.

Eight tests passed, including direct subset controls, 9,840 short sequences with plateaus, and rejection of invalid trees and altered coefficients. A deterministic full generation replay reproduced the same raw-log hash. Two incomplete, time-limited audit attempts were excluded; five disjoint completed audit segments cover exactly indices 1 through 3,206.

## Reproduce from this Git branch

Only Python 3.10+ standard-library modules are needed; no network, model API, C++ compiler, historical archive, or Lean runtime is required. Run without `-O` (both scripts reject disabled assertions). From this directory:

```bash
python3 test_branch_study.py
python3 branch_study.py --out /tmp/erdos993-hetero-new
python3 audit_study.py --log /tmp/erdos993-hetero-new/trials.jsonl --out /tmp/erdos993-hetero-audit.json
```

The generation output directory must not exist; choose a fresh name. The audit output is explicitly chosen by the caller and should also be a new path. The expected SHA-256 of generated `trials.jsonl` is:

```
5bab426336001c5b9f50a79beaf96e76057a1ce7de2ca8aa70b4748f8956a53f
```

For bounded tool runtimes, audit using these non-overlapping `--start`/`--end` ranges and separate output paths: 1-2002, 2003-2402, 2403-2802, 2803-3202, 3203-3206. `--stride 1` is the default and checks every selected record. A non-default stride is sampling, not a full audit. The checker rejects empty coverage. Readers who segment a new audit must check exact range coverage themselves; the supplied summary describes the completed recorded run.

[Study summary](results/summary.json), [audit summary](results/audit-summary.json), and [test log](results/tests.log) preserve the recorded counts and hashes. Complete raw records and per-segment receipts are in the accompanying conversation evidence archive; they are not stored in this Git branch. Unlike the historical v2 archive, all source needed to regenerate this new study is included here.

## Verification boundary

Different algorithms were developed and run in the same session, not by different research teams. The v2 Lean logs remain historical evidence for the finite 14-vertex certificate and generic sequence lemmas; **no fresh Lean build or new family Lean theorem was performed in this follow-up**. Repository CI, if run, is not a mathematical review. No main-branch, catalog, eligibility, candidate, award, recipient, or payment changes are requested.
