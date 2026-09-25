#!/bin/bash
# Compare cwlc_lean (n = 4..25, 1 thread) with the committed cwlc logs of run 20260924T092515Z:
# trees, nonunimodal, nonLC and checksum must agree. usage: crosscheck_cwlc.sh REFLOGDIR
set -u
REF=$1
for n in $(seq 4 25); do
  f() { grep '^RESULT' | grep -o 'trees=[0-9]*\|nonunimodal=[0-9]*\|nonLC=[0-9]*\|checksum=[0-9]*' | tr '\n' ' '; }
  A=$(./cwlc_lean $n 1 | f); B=$(f < $REF/cwlc_n$n.log)
  if [ "$A" = "$B" ]; then echo "n=$n identical $A"; else echo "n=$n DIFFERENT lean: $A cwlc: $B"; fi
done
