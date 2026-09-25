#!/bin/bash
# cwlc_vec3 (and -DSTATS) against cwlc_lean for n = 4..22 at four thresholds THR = 2^T:
# T = 32 (fast path only), T = 1 and T = n/2 (every tree through the exact fallback),
# T = 4n/5 (mixed: some trees fast, some exact). RESULT lines without timing must be identical.
set -u
for n in $(seq 4 22); do
  L=$(./cwlc_lean $n 1 | grep '^RESULT' | sed 's/ seconds=.*//')
  for T in 32 1 $((n/2)) $(( (4*n)/5 )); do
    for b in cwlc_vec3 cwlc_vec3s; do
      out=$(./$b $n 1 $(( (n-1)/2 )) $T)
      V=$(echo "$out" | grep '^RESULT' | sed 's/ seconds=.*//')
      B=$(echo "$out" | grep -o 'exact_fallback_trees=[0-9]*')
      if [ "$L" = "$V" ]; then echo "n=$n T=$T $b identical $B"; else echo "n=$n T=$T $b DIFFERENT $B"; echo " lean: $L"; echo " $b: $V"; fi
    done
  done
done
