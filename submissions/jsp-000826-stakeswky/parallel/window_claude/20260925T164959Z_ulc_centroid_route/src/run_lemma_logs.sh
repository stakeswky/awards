#!/bin/bash
# Re-run every lemma search with fixed seeds and save its output (4 jobs at a time).
# Outputs go to ./tlogs; the committed copies are in ../logs.
cd "$(dirname "$0")"
jobs_list=(
 "python3 lemma_search.py > tlogs/lemma_search.log 2>&1"
 "python3 lemma_search2.py > tlogs/lemma_search2.log 2>&1"
 "python3 lemma_climb.py 1 > tlogs/lemma_climb_s1.log 2>&1"
 "python3 lemma_climb.py 2 > tlogs/lemma_climb_s2.log 2>&1"
 "python3 lemma_climb.py 3 > tlogs/lemma_climb_s3.log 2>&1"
 "python3 lemma_climb.py 4 > tlogs/lemma_climb_s4.log 2>&1"
 "python3 lemma_climb_ulc.py 1 > tlogs/lemma_climb_ulc_s1.log 2>&1"
 "python3 lemma_climb_ulc.py 2 > tlogs/lemma_climb_ulc_s2.log 2>&1"
 "python3 lemma_climb_ulc.py 3 > tlogs/lemma_climb_ulc_s3.log 2>&1"
 "python3 lemma_climb_ulc.py 4 > tlogs/lemma_climb_ulc_s4.log 2>&1"
 "python3 lemma_climb_ulc23.py 11 > tlogs/lemma_climb_ulc23_s11.log 2>&1"
 "python3 lemma_climb_ulc23.py 12 > tlogs/lemma_climb_ulc23_s12.log 2>&1"
 "python3 lemma_climb_ulc23.py 13 > tlogs/lemma_climb_ulc23_s13.log 2>&1"
 "python3 lemma_climb_ulc23.py 14 > tlogs/lemma_climb_ulc23_s14.log 2>&1"
 "python3 lemma_fg.py 1 > tlogs/lemma_fg_s1.log 2>&1"
 "python3 lemma_fg.py 2 > tlogs/lemma_fg_s2.log 2>&1"
 "python3 lemma_fg.py 3 > tlogs/lemma_fg_s3.log 2>&1"
 "python3 lemma_fg.py 4 > tlogs/lemma_fg_s4.log 2>&1"
)
for j in "${jobs_list[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge 4 ]; do sleep 5; done
  bash -c "$j" &
done
wait
echo done > tlogs/ALL_DONE
