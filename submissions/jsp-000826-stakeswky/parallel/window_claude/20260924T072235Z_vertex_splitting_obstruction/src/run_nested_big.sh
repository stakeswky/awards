#!/bin/zsh
cd /tmp/e993/research
while [ ! -f stepf_big.sentinel ]; do sleep 30; done
for m in 17 18 19 20 21 22 23 24 25 26; do
  s=$(date +%s); ./stepcn $m 3 2 8 nested > stepcn_n$m.out 2>&1; echo "exit=$? n=$m elapsed=$(( $(date +%s) - s ))s" >> stepcn_n$m.out
done
for N in 14 15 16 17 18 19 20 21; do
  s=$(date +%s); ./stepfn $N 3 2 8 nested > stepfn_N$N.out 2>&1; echo "exit=$? N=$N elapsed=$(( $(date +%s) - s ))s" >> stepfn_N$N.out
done
echo DONE > nested_big.sentinel
