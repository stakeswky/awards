#!/bin/zsh
# Re-run the small C checks (previously interactive) into logs, after the long runs finish.
cd /tmp/e993/research
while [ ! -f nested_big.sentinel ]; do sleep 30; done
{
  echo "== checksum cross-check n=12 (wlc, wlc3, stepc must agree)"
  ./wlc 12 1 0 | grep -o "trees=[0-9]*\|checksum=[0-9]*" | tr '\n' ' '; echo
  ./wlc3 12 2 | grep -o "trees=[0-9]*\|checksum=[0-9]*" | tr '\n' ' '; echo
  ./stepc 12 3 2 2 | tail -1
  echo "== c=1 cross-check with Python (single failure at n=9)"
  for m in 8 9 10 11 12; do ./stepc $m 1 1 4 | tail -2; done
  echo "== forests c=1 (T-r), orders 6..14"
  for N in 7 8 10 11 13 14 15; do ./stepf $N 1 1 4 | tail -1; done
} > clogs/crosscheck.log 2>&1; echo "exit=$?" > clogs/crosscheck.exit
for m in $(seq 4 24); do ./stepc $m 3 2 8 > clogs/stepc_c32_n$m.out 2>&1; echo "exit=$? n=$m" >> clogs/stepc_c32_n$m.out; done
for N in $(seq 5 20); do ./stepf $N 3 2 8 > clogs/stepf_c32_N$N.out 2>&1; echo "exit=$? N=$N" >> clogs/stepf_c32_N$N.out; done
echo DONE > clogs/ALL.sentinel
