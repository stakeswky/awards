#!/bin/zsh
cd /tmp/e993/research
for m in 25 26 27 28 29 30; do
  s=$(date +%s)
  ./stepc $m 3 2 8 > stepc_c32_n$m.out 2>&1
  echo "exit=$? n=$m elapsed=$(( $(date +%s) - s ))s" >> stepc_c32_n$m.out
done
echo DONE > stepc_big.sentinel
