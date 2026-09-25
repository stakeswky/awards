#!/bin/zsh
cd /tmp/e993/research
while [ ! -f stepc_big.sentinel ]; do sleep 30; done
for N in 21 22 23; do
  s=$(date +%s)
  ./stepf $N 3 2 8 > stepf_c32_N$N.out 2>&1
  echo "exit=$? N=$N elapsed=$(( $(date +%s) - s ))s" >> stepf_c32_N$N.out
done
echo DONE > stepf_big.sentinel
