#!/bin/zsh
# Re-run every Python check cited in WINDOW_LC_PROGRESS.md section 9, one log + exit code per run.
cd /tmp/e993/research
run() { local name=$1; shift; local s=$(date +%s); nice -n 10 "$@" > pylogs/$name.log 2>&1; echo "exit=$? elapsed=$(( $(date +%s) - s ))s cmd=$*" > pylogs/$name.exit; }
run c1_trees_4_12        python3 quant_scheme_lm.py 1 trees 4 12
run c2_forest_2K1        python3 c2_forest_fail.py
for c in 1 5/4 4/3 3/2; do run cscan_c${c/\//_} python3 cscan.py $c 2 14; done
run norm_scan_2_14       python3 norm_scan.py 2 14
run ulc_nonlc            python3 ulc_scheme.py nonlc
run ulc_forests_2_13     python3 ulc_scheme.py forests 2 13
run c32_nonlc            python3 quant_scheme_lm.py 3/2 nonlc
run c32_trees_4_16       python3 quant_scheme_lm.py 3/2 trees 4 16
run c32_families         python3 step_broad.py 3/2 families
run c32_randforests      python3 step_broad.py 3/2 forests 3000
run anatomy_trees        python3 step_anatomy.py trees 5 14
run canonical_trees      python3 step_canonical.py trees 5 15
run canonical_forests    python3 step_canonical.py forests 3 12
run rules_trees          python3 step_rules.py trees 5 15
run rules_forests        python3 step_rules.py forests 4 12
run support_exc          python3 step_support_exc.py
run tr_forests_2_13      python3 quant_scheme_tr.py 3/2 forests 2 13
run tr_forests_noptr     python3 quant_scheme_tr.py 3/2 forests 2 13 noptr
run isolated_TR          python3 step_isolated.py 60 26
run isolated_TRnu        python3 step_isolated.py 60 30 nu noptr
run star_scan_150        python3 star_scan.py 150
run star_fail_160        python3 star_fail_detail.py 160
run spider_90            python3 spider_step.py 90
run smallest_fail        python3 smallest_fail.py
run nested_trees_4_16    python3 step_nested.py trees 4 16
run nested_forests_2_12  python3 step_nested.py forests 2 12
run nested_stress        python3 nested_stress.py
run nested_adv           python3 nested_adv.py
run closed_form          python3 closed_form_checks.py
run nonlc_structure      python3 wlc_ratio_nonlc.py
echo DONE > pylogs/ALL.sentinel
