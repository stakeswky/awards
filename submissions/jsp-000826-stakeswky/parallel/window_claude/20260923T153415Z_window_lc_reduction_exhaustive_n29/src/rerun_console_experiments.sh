#!/bin/zsh
# Re-runs the console-only experiments of this attempt and stores their outputs (exit codes in *.exit).
cd "$(dirname "$0")"
OUT=../logs/rerun
run() { local name=$1; shift; "$@" > $OUT/$name.log 2>&1; echo $? > $OUT/$name.exit; }
run e1_forests_two_components     python3 exp_g123.py e1 16
run e2_anchors_n4_17              python3 exp_g123.py e2 17
run e3_population_turning         python3 exp_g123.py e3 18
run tail_bound                    python3 exp_more.py tail 18
run e2_anchors_n18_19             python3 exp_more.py e2 19
run anchors_small_total           python3 anchors_small.py
run f3_three_components           python3 exp_more.py f3 13
run s1_condition                  python3 exp_s1.py 18
run wlc_structured_families       python3 exp_wlc.py
run wlc_forests_nonlc             python3 forest_wlc.py
echo DONE > $OUT/ALL_DONE
