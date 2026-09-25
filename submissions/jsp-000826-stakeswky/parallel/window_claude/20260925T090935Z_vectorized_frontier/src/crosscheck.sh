#!/bin/bash
# Cross-check cwlc_vec, cwlc_vec2 and cwlc_vec2 -DSTATS against cwlc_lean for n = 4..24 (1 thread):
# the RESULT lines without the timing field must be identical.
set -u
for n in $(seq 4 24); do
  L=$(./cwlc_lean $n 1 | grep '^RESULT' | sed 's/ seconds=.*//')
  for b in cwlc_vec cwlc_vec2 cwlc_vec2s; do
    V=$(./$b $n 1 | grep '^RESULT' | sed 's/ seconds=.*//')
    if [ "$L" = "$V" ]; then echo "n=$n $b identical"; else echo "n=$n $b DIFFERENT"; echo " lean: $L"; echo " $b: $V"; fi
  done
done
