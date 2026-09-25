# C6: signed cut compensation beyond buffered windows

**ORIGINAL=NOT_CLOSED; general C4-F=NOT_CLOSED.**

Read PROOF.md, GAP.md and REVIEW.md. Two results are supplied:

1. A proved full-support signed next-decline lower bound with an explicit
payment gate, allowing inverse Toeplitz terms and negative local budgets. A
fixed modal donor is available from component unimodality. An automatic payment
entrance for every remaining forest is NOT proved.
2. For every component count r, an explicit forest with no nonempty LC complete
component subunion. This rules out an unconditional component-count shortcut,
not the minimum-bad/HEREDITARY version and not ORIGINAL.

The C4 four-type arbitrary-multiplicity closure is unchanged. The two C5 batches
are distinguished: actual space 173613Z final proof and programs were audited;
remote 173130Z final bodies were not present at the initial head. Provenance and
fresh inherited replay receipts are separate from new C6 results.

## Reproduce new C6 results

Python 3.11 or later, standard library only; do not use the -O flag. From this
directory. The Git delivery contains the source as ordinary readable Python files:

```sh
python sources/targeted_search.py --out certificates/TARGETED_SEARCH.json --steps 250
python sources/verify_material.py --outdir certificates
python sources/verify_lcfree.py --out certificates/LCFREE_REGRESSION.json
python sources/verify_abstract.py --out certificates/ABSTRACT_ALGEBRA.json
python sources/audit_certificate.py --outdir certificates
```

The full conversation archive also contains an optional verified source bundle;
UNPACK_SOURCE.py leaves identical files unchanged. The readable Python sources
need no external API, paid service, hidden dataset or third-party mathematics package.
New output hashes and clean-source replay receipts are in REPLAY.json.
The full graph/weight arrays are in the conversation ZIP and reproducible by
the commands. They are not falsely described as separate raw Git-hosted files.

The new material has 24 counting tasks / 1,906 coefficient entries, plus the
separate LC-free regression's 20 tasks / 3,224 entries. Counts are not a union
of distinct graph shapes. The 97 directed-search evaluations overlap material
checks; abstract tests are not forest coverage. Do not combine these totals.

## Source provenance

sources/inherited_exact.py is copied unchanged from the C4 exact.py. Its old
reconstruction header belongs to that original run; it is NOT a C6 claim of new
source bytes. sources/deletion_balanced.py is copied unchanged from C5 173613Z.
The new drivers, ratio-cut implementation and audit are C6 additions. Hashes in
provenance identify the original archive/standalone files and fresh C4/C5 replays.
The C5 T26 HEREDITARY classification was separately rerun in this task; the new
C6 material script references that proof and does not itself repeat the entire
classification. This guard is not a premise of the new unconditional algebra.

Only this new C6 directory is published. PR #1 must remain Draft and unmerged.
No global novelty, external review, Lean proof or prize entitlement is claimed.
