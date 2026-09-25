# Order-one reformulations, quantified barriers, and the frontier at n = 32 (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is **not** proved or refuted here. This run was started with the
goal of a complete proof. What follows is the honest outcome: a larger verified range, three new
reformulations with order-one margins, several refuted sufficient conditions, and a quantified
account of why no available route closes 33 <= n < N0. PR #1 stays Draft; `RESEARCH_STATE.json` is not
modified. No novelty, priority or award claim is made.

## Results

1. **Frontier.** The exhaustive check of all 109,972,410,221 trees of order 32 is running (follow-up commit). Forests of order 32 with a non-LC component: all 1,184 distinct
   (non-LC tree, small forest) polynomial pairs pass. Forests of order 32 whose components are all LC
   are strictly LC by the strict Hoggar lemma and the isolated-equality remark of run
   `20260924T092515Z`. Once the tree run completes, this gives strict window LC and unimodality for every forest of order <= 32.
2. **Tilted concavity at the mean (TC)** implies window LC (Lemma 1, AM–GM). It holds at every window
   position of every tree with n <= 25, with minimum normalised slack 1.33 → 2 (stars). Its
   Fourier form is the positivity of one weighted integral of the centred characteristic function.
3. **Darroch's mean–mode relation (DT)**, rho_{k-1} <= lambda_k <= rho_k (coefficient ratios interlace
   the mean-activities), implies TC and LC (Lemma 2). It holds with an **order-one** margin in mean
   units:
   - >= 0.105 on all trees with n <= 16 (0.165–0.25 for n >= 11);
   - >= 0.157 on all forests with at least two components and n <= 13;
   - >= 0.244 on products of non-LC trees;
   - >= 0.202 on structured families and >= 0.237 in an adversarial search on 30 <= n <= 80.

   The LC margin, by contrast, is about 3.4/n.
4. **Refuted or insufficient routes (recorded as negative results):**
   - Joint Darroch interlacing of a vertex split (JDT), the common-interlacer analogue, fails for
     every tree with n = 4, 5 and for 41% of trees with n = 14.
   - |kappa_3| <= kappa_2 holds for all trees n <= 16 at all activities in [e^-4, e^4] (max ratio 0.928),
     but fails for all 308 non-LC trees at activities >= 164 (and from 54.6 on core trees); it cannot
     imply coefficient LC in any case.
   - An activity-local curvature invariant "LC margin >= c / Var_lambda" (true with c ≈ 0.46)
     propagates through the vertex mixture only with Gaussian-precision slope control, which small
     forests do not have.
5. **Quantified analytic barrier.** The true characteristic-function decay constant of trees is
   c_eff ≈ 0.11–0.29, against 1/114244 in the FLNYZ formalization. Even with c = 0.1 proved, a
   Fourier proof of TC needs n of order 10^6 because of the fourth-cumulant term, and uniform O(n)
   cumulant bounds fail on nested hub trees. Exhaustive computation costs a factor 2.95 per order
   (about 5 hours for n = 32 on 4 cores). **So neither the analytic nor the computational side can close
   33 <= n < N0, and every structural induction tried reduces to an O(1/n) local statement that its
   own hypotheses do not control.**

## What would close the problem

Either a uniform explicit near-mode Gaussianity theorem for independent sets in forests valid down
to n = 33, or a closed invariant (preserved by the rooted-tree recursion including products) that
implies DT or TC on the window. The order-one margin of DT suggests working in mean/activity units.
See `NOTE.md`, Section 4.

## Environment note

Lean could not be run: the environment's network policy denies `github.com` release downloads (for
`elan`) and `lakecache.blob.core.windows.net` (the mathlib cache).

## Files

- `NOTE.md`, `VERDICT.json`, `MANIFEST.sha256`.
- `src/`:
  - `cwlc.c` (the exhaustive checker, unchanged from run `20260924T092515Z`);
  - `tcheck.c` (TC, exhaustive);
  - `tiltconc.py`, `dt_slack.py`, `dt_forests.py`, `dt_search.py`, `jdt.py`, `k3k2.py`,
    `k3k2_nonlc.py`, `charfn.py`, `mixture_test.py`, `forest_nonlc32.py`;
  - helpers `modelib.py`, `ip.py`, `ma_forests.py`, `families.py`.
- `logs/`: `tc_n*.log` (with `tc_summary.log`), one log per script above; `cwlc_n32.log` follows.
- `results/`: `forest_nonlc_N32.json`.
