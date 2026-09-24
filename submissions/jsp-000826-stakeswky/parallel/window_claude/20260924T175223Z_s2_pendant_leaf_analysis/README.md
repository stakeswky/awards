# The pendant-leaf statement (S2): reduction, degree-one lemma, remaining hypothesis (independent Claude window)

**ORIGINAL=NOT_CLOSED.** Erdős #993 is **not** proved or refuted here, and (S2) is proved only
conditionally. This run continues `20260924T143534Z_mode_alignment_route` and
`20260924T150627Z_ma_exhaustive_n26_forests18`. PR #1 stays Draft; `RESEARCH_STATE.json` is not
modified. No novelty, priority or award claim is made.

## Statement studied

(S2): attaching a pendant leaf u at a vertex w of a forest H moves the mode set of the independence
sequence by 0 or +1. With P = I(H), Q = I(H - w), Q' = I(H - N[w]), the new sequence is P + xQ and
P = Q + xQ'.

## Results

1. **Theorem 1 (proved).** With M(P) = [p1, p2], M(Q) = [q1, q2]: if q2 >= p1 - 1 the new sequence is
   nondecreasing up to p1; if q1 <= p2 it is nonincreasing from p2 + 1; if q1 = p2 + 1 =: m + 1 it is
   nonincreasing from m + 1 **iff** Q_m + Q'_m >= Q_{m+2} + Q'_{m+1}, which holds whenever
   Q_m >= Q_{m+2}. In each case the sequence is unimodal and (S2) holds. Verified exactly on all
   188,254 pairs (tree H of order <= 15, any w).
2. **Lemma 2.** In the +1 case, Q_m >= Q_{m+2} is equivalent to gamma >= 2 rise (gamma = concavity gap of Q
   at its mode, rise = Q_{m+1} - Q_m), and the case itself forces rise < phi = Q'_{m-1} - Q'_m. So
   **(Q1): gamma >= 2 phi** suffices.
3. **Lemma 3 (proved).** If w is a leaf of H, the +1 case cannot occur (given (S1) for the smaller
   pair). So the only open case has deg w >= 2.
4. **Corollary 4 (conditional (S2)).** Unimodality + (S1) for smaller forests + (Q1) ⟹ (S2).
5. **Data on the +1 case** (all trees n <= 19, every vertex): the rise into the peak of Q is at most
   0.68 Q/n; the concavity gap is at least 4.0 Q/n; the fall after the peak is at least 7.3 times
   the rise; (Q1) holds with factor >= 3.1; Q never has a peak plateau; deg w = 2 occurs 14 times.
   Right-heavy peaks are common in general (62% of trees at n = 20), so (Q1) is specific to the
   configuration.
6. **(S1) reduces to two inequalities of the same type** ((Q2), (Q3)), holding on all pairs n <= 15
   with ratios >= 6.9 and >= 9.
7. **Theorem 5 (conditional).** (Q1)-(Q3) for all forests ⟹ every forest with a degree-2 support
   vertex is unimodal, and (S1), (S2) hold everywhere. Hub forests (all supports of degree >= 3)
   need a separate alignment argument at a hub or the centre; not done here.
8. **Assessment.** (Q1) is a log-concavity-with-margin statement at one index (the mode of I(H - w))
   plus a slope bound for I(H - N[w]). It does not follow from unimodality or mode positions. The
   pendant-leaf route localises the quantitative core of the problem to the mode; it does not
   remove it.

## Files

- `NOTE.md`: statements, proofs, tables, the remaining hypothesis and the conditional chain.
- `VERDICT.json`.
- `src/`: `thm1_check.py` (exact verification of Theorem 1 and the (S1) configurations),
  `s2_config.py`, `lh_margin.py`, `lh_quant.py` (the +1 configurations and their margins),
  `cwlc_rh.c` (right-heavy peak counts over all trees), `modelib.py`, `ma_forests.py`, `ip.py`.
- `logs/`: `thm1_check_15.log`, `s2_config_16.log`, `lh_margin.log` (n <= 19), `lh_quant.log`
  (n <= 17), `rh_peaks.log`.
- `MANIFEST.sha256`.

## Reproduce

    cd src && python3 thm1_check.py 15 && python3 s2_config.py 16 && python3 lh_margin.py 19 && python3 lh_quant.py 17
    gcc -O3 -march=native -fopenmp -o cwlc_rh cwlc_rh.c && for n in 8 12 16 20 22; do ./cwlc_rh $n 4 | grep PEAK; done
