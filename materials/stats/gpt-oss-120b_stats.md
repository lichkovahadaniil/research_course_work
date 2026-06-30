# Statistical Tests: gpt-oss-120b

Primary baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_back`, `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 300 | 0.3067 | 0.2967 | 27 | 30 | -0.0100 | 0.9000 | 0.791366 | 1.000000 |
| reachability | canonical -> disp_2 | 300 | 0.3067 | 0.2667 | 18 | 30 | -0.0400 | 0.6000 | 0.111403 | 0.557014 |
| reachability | canonical -> disp_3 | 300 | 0.3067 | 0.2233 | 17 | 42 | -0.0833 | 0.4048 | 0.001547 | 0.009283 |
| reachability | canonical -> plan_front | 300 | 0.3067 | 0.2933 | 21 | 25 | -0.0133 | 0.8400 | 0.658738 | 1.000000 |
| reachability | canonical -> plan_back | 300 | 0.3067 | 0.2800 | 20 | 28 | -0.0267 | 0.7143 | 0.312327 | 1.000000 |
| reachability | canonical -> plan_scatter | 300 | 0.3067 | 0.2767 | 20 | 29 | -0.0300 | 0.6897 | 0.252870 | 1.000000 |
| executability | canonical -> disp_1 | 300 | 0.4300 | 0.4567 | 53 | 45 | 0.0267 | 1.1778 | 0.479692 | 1.000000 |
| executability | canonical -> disp_2 | 300 | 0.4300 | 0.4500 | 57 | 51 | 0.0200 | 1.1176 | 0.630634 | 1.000000 |
| executability | canonical -> disp_3 | 300 | 0.4300 | 0.4233 | 56 | 58 | -0.0067 | 0.9655 | 0.925435 | 1.000000 |
| executability | canonical -> plan_front | 300 | 0.4300 | 0.4767 | 57 | 43 | 0.0467 | 1.3256 | 0.193348 | 0.966740 |
| executability | canonical -> plan_back | 300 | 0.4300 | 0.4500 | 55 | 49 | 0.0200 | 1.1224 | 0.624144 | 1.000000 |
| executability | canonical -> plan_scatter | 300 | 0.4300 | 0.5033 | 59 | 37 | 0.0733 | 1.5946 | 0.031548 | 0.189289 |
| non_executable_failure | canonical -> disp_1 | 300 | 0.5700 | 0.5433 | 45 | 53 | -0.0267 | 0.8491 | 0.479692 | 1.000000 |
| non_executable_failure | canonical -> disp_2 | 300 | 0.5700 | 0.5500 | 51 | 57 | -0.0200 | 0.8947 | 0.630634 | 1.000000 |
| non_executable_failure | canonical -> disp_3 | 300 | 0.5700 | 0.5767 | 58 | 56 | 0.0067 | 1.0357 | 0.925435 | 1.000000 |
| non_executable_failure | canonical -> plan_front | 300 | 0.5700 | 0.5233 | 43 | 57 | -0.0467 | 0.7544 | 0.193348 | 0.966740 |
| non_executable_failure | canonical -> plan_back | 300 | 0.5700 | 0.5500 | 49 | 55 | -0.0200 | 0.8909 | 0.624144 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 300 | 0.5700 | 0.4967 | 37 | 59 | -0.0733 | 0.6271 | 0.031548 | 0.189289 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 129 | 137 | 0.7132 | 0.6496 | 92/37 | 89/48 | -0.0635 | 0.7457 | 0.293922 | 0.301310 |
| conditional_reachability | canonical -> disp_2 | 129 | 135 | 0.7132 | 0.5926 | 92/37 | 80/55 | -0.1206 | 0.5850 | 0.052354 | 0.209416 |
| conditional_reachability | canonical -> disp_3 | 129 | 127 | 0.7132 | 0.5276 | 92/37 | 67/60 | -0.1856 | 0.4491 | 0.002965 | 0.017792 |
| conditional_reachability | canonical -> plan_front | 129 | 143 | 0.7132 | 0.6154 | 92/37 | 88/55 | -0.0978 | 0.6435 | 0.096474 | 0.289421 |
| conditional_reachability | canonical -> plan_back | 129 | 135 | 0.7132 | 0.6222 | 92/37 | 84/51 | -0.0910 | 0.6624 | 0.150655 | 0.301310 |
| conditional_reachability | canonical -> plan_scatter | 129 | 151 | 0.7132 | 0.5497 | 92/37 | 83/68 | -0.1635 | 0.4909 | 0.006335 | 0.031673 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 62 | 10.5484 | 9.5161 | -1.0323 | -0.0979 | -0.2327 | 0.071742 | 0.039062 | 0.234375 |
| plan_length | canonical -> disp_2 | 62 | 10.5323 | 9.6452 | -0.8871 | -0.0842 | -0.2098 | 0.103622 | 0.051270 | 0.256348 |
| plan_length | canonical -> disp_3 | 50 | 9.4200 | 8.4400 | -0.9800 | -0.1040 | -0.2042 | 0.155197 | 0.250000 | 0.500000 |
| plan_length | canonical -> plan_front | 67 | 10.6716 | 9.8209 | -0.8507 | -0.0797 | -0.2031 | 0.101233 | 0.069641 | 0.278564 |
| plan_length | canonical -> plan_back | 64 | 9.8281 | 10.2344 | 0.4062 | 0.0413 | 0.0783 | 0.533258 | 0.568237 | 0.568237 |
| plan_length | canonical -> plan_scatter | 63 | 10.2857 | 9.4127 | -0.8730 | -0.0849 | -0.2028 | 0.112555 | 0.092773 | 0.278564 |
| optimality_ratio | canonical -> disp_1 | 62 | 1.1101 | 1.0201 | -0.0900 | -0.0811 | -0.2371 | 0.066670 | 0.011719 | 0.070312 |
| optimality_ratio | canonical -> disp_2 | 62 | 1.1005 | 1.0233 | -0.0772 | -0.0701 | -0.2080 | 0.106676 | 0.047607 | 0.238037 |
| optimality_ratio | canonical -> disp_3 | 50 | 1.0991 | 1.0110 | -0.0882 | -0.0802 | -0.2121 | 0.140120 | 0.125000 | 0.250000 |
| optimality_ratio | canonical -> plan_front | 67 | 1.0933 | 1.0214 | -0.0719 | -0.0658 | -0.1984 | 0.109177 | 0.059814 | 0.238037 |
| optimality_ratio | canonical -> plan_back | 64 | 1.0734 | 1.0956 | 0.0221 | 0.0206 | 0.0463 | 0.712454 | 0.745239 | 0.745239 |
| optimality_ratio | canonical -> plan_scatter | 63 | 1.0993 | 1.0233 | -0.0761 | -0.0692 | -0.2042 | 0.110221 | 0.054688 | 0.238037 |
| first_failure_step | canonical -> disp_1 | 69 | 10.2899 | 9.5072 | -0.7826 | -0.0761 | -0.0907 | 0.454027 | 0.461600 | 0.923200 |
| first_failure_step | canonical -> disp_2 | 70 | 11.3286 | 10.6857 | -0.6429 | -0.0567 | -0.0664 | 0.580101 | 0.590760 | 0.923200 |
| first_failure_step | canonical -> disp_3 | 67 | 11.2836 | 8.3433 | -2.9403 | -0.2606 | -0.3216 | 0.010553 | 0.010430 | 0.052150 |
| first_failure_step | canonical -> plan_front | 64 | 11.4219 | 9.9688 | -1.4531 | -0.1272 | -0.1547 | 0.220344 | 0.225080 | 0.675240 |
| first_failure_step | canonical -> plan_back | 67 | 9.8806 | 7.1791 | -2.7015 | -0.2734 | -0.3408 | 0.006897 | 0.006740 | 0.040440 |
| first_failure_step | canonical -> plan_scatter | 52 | 9.8269 | 8.0769 | -1.7500 | -0.1781 | -0.2324 | 0.099882 | 0.104110 | 0.416440 |
| prompt_tokens | canonical -> disp_1 | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_back | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> disp_1 | 300 | 8628.5433 | 8109.4767 | -519.0667 | -0.0602 | -0.1138 | 0.049683 | 0.048760 | 0.094460 |
| completion_tokens | canonical -> disp_2 | 300 | 8628.5433 | 8098.6533 | -529.8900 | -0.0614 | -0.1147 | 0.047807 | 0.047230 | 0.094460 |
| completion_tokens | canonical -> disp_3 | 300 | 8628.5433 | 7817.2400 | -811.3033 | -0.0940 | -0.1957 | 0.000792 | 0.000590 | 0.002950 |
| completion_tokens | canonical -> plan_front | 300 | 8628.5433 | 7580.8400 | -1047.7033 | -0.1214 | -0.2426 | 0.000035 | 0.000030 | 0.000180 |
| completion_tokens | canonical -> plan_back | 300 | 8628.5433 | 7921.9633 | -706.5800 | -0.0819 | -0.1477 | 0.011033 | 0.011040 | 0.044160 |
| completion_tokens | canonical -> plan_scatter | 300 | 8628.5433 | 7939.9867 | -688.5567 | -0.0798 | -0.1410 | 0.015170 | 0.015270 | 0.045810 |
| reasoning_completion_tokens | canonical -> disp_1 | 300 | 8628.5433 | 8109.4767 | -519.0667 | -0.0602 | -0.1138 | 0.049683 | 0.048760 | 0.094460 |
| reasoning_completion_tokens | canonical -> disp_2 | 300 | 8628.5433 | 8098.6533 | -529.8900 | -0.0614 | -0.1147 | 0.047807 | 0.047230 | 0.094460 |
| reasoning_completion_tokens | canonical -> disp_3 | 300 | 8628.5433 | 7817.2400 | -811.3033 | -0.0940 | -0.1957 | 0.000792 | 0.000590 | 0.002950 |
| reasoning_completion_tokens | canonical -> plan_front | 300 | 8628.5433 | 7580.8400 | -1047.7033 | -0.1214 | -0.2426 | 0.000035 | 0.000030 | 0.000180 |
| reasoning_completion_tokens | canonical -> plan_back | 300 | 8628.5433 | 7921.9633 | -706.5800 | -0.0819 | -0.1477 | 0.011033 | 0.011040 | 0.044160 |
| reasoning_completion_tokens | canonical -> plan_scatter | 300 | 8628.5433 | 7939.9867 | -688.5567 | -0.0798 | -0.1410 | 0.015170 | 0.015270 | 0.045810 |
| raw_completion_tokens | canonical -> disp_1 | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> plan_front | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> plan_back | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| total_tokens | canonical -> disp_1 | 300 | 17372.4433 | 16853.3767 | -519.0667 | -0.0299 | -0.1138 | 0.049683 | 0.048760 | 0.094460 |
| total_tokens | canonical -> disp_2 | 300 | 17372.4433 | 16842.5533 | -529.8900 | -0.0305 | -0.1147 | 0.047807 | 0.047230 | 0.094460 |
| total_tokens | canonical -> disp_3 | 300 | 17372.4433 | 16561.1400 | -811.3033 | -0.0467 | -0.1957 | 0.000792 | 0.000590 | 0.002950 |
| total_tokens | canonical -> plan_front | 300 | 17372.4433 | 16324.7400 | -1047.7033 | -0.0603 | -0.2426 | 0.000035 | 0.000030 | 0.000180 |
| total_tokens | canonical -> plan_back | 300 | 17372.4433 | 16665.8633 | -706.5800 | -0.0407 | -0.1477 | 0.011033 | 0.011040 | 0.044160 |
| total_tokens | canonical -> plan_scatter | 300 | 17372.4433 | 16683.8867 | -688.5567 | -0.0396 | -0.1410 | 0.015170 | 0.015270 | 0.045810 |
| duration_sec | canonical -> disp_1 | 300 | 175.9562 | 168.9305 | -7.0257 | -0.0399 | -0.0692 | 0.231469 | 0.231180 | 0.231180 |
| duration_sec | canonical -> disp_2 | 300 | 175.9562 | 163.8735 | -12.0827 | -0.0687 | -0.1139 | 0.049498 | 0.049900 | 0.099800 |
| duration_sec | canonical -> disp_3 | 300 | 175.9562 | 160.8507 | -15.1055 | -0.0858 | -0.1546 | 0.007841 | 0.007720 | 0.030880 |
| duration_sec | canonical -> plan_front | 300 | 175.9562 | 151.7043 | -24.2519 | -0.1378 | -0.2368 | 0.000053 | 0.000060 | 0.000360 |
| duration_sec | canonical -> plan_back | 300 | 175.9562 | 213.0387 | 37.0825 | 0.2107 | 0.1555 | 0.007462 | 0.005600 | 0.028000 |
| duration_sec | canonical -> plan_scatter | 300 | 175.9562 | 161.0220 | -14.9342 | -0.0849 | -0.1358 | 0.019341 | 0.019210 | 0.057630 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 20 | 0.3067 | 0.2967 | -0.0100 | [-0.0833, 0.0767] | 0.880859 |
| reachability | canonical -> disp_2 | 20 | 0.3067 | 0.2667 | -0.0400 | [-0.1267, 0.0400] | 0.425781 |
| reachability | canonical -> disp_3 | 20 | 0.3067 | 0.2233 | -0.0833 | [-0.1833, 0.0100] | 0.140625 |
| reachability | canonical -> plan_front | 20 | 0.3067 | 0.2933 | -0.0133 | [-0.1000, 0.0767] | 0.843750 |
| reachability | canonical -> plan_back | 20 | 0.3067 | 0.2800 | -0.0267 | [-0.0733, 0.0233] | 0.363281 |
| reachability | canonical -> plan_scatter | 20 | 0.3067 | 0.2767 | -0.0300 | [-0.1067, 0.0533] | 0.545898 |
| executability | canonical -> disp_1 | 20 | 0.4300 | 0.4567 | 0.0267 | [-0.0500, 0.1067] | 0.588623 |
| executability | canonical -> disp_2 | 20 | 0.4300 | 0.4500 | 0.0200 | [-0.0533, 0.0900] | 0.668091 |
| executability | canonical -> disp_3 | 20 | 0.4300 | 0.4233 | -0.0067 | [-0.1000, 0.0767] | 0.946716 |
| executability | canonical -> plan_front | 20 | 0.4300 | 0.4767 | 0.0467 | [-0.0233, 0.1167] | 0.263855 |
| executability | canonical -> plan_back | 20 | 0.4300 | 0.4500 | 0.0200 | [-0.0400, 0.0733] | 0.591064 |
| executability | canonical -> plan_scatter | 20 | 0.4300 | 0.5033 | 0.0733 | [-0.0033, 0.1500] | 0.101929 |
| non_executable_failure | canonical -> disp_1 | 20 | 0.5700 | 0.5433 | -0.0267 | [-0.1067, 0.0500] | 0.588623 |
| non_executable_failure | canonical -> disp_2 | 20 | 0.5700 | 0.5500 | -0.0200 | [-0.0900, 0.0533] | 0.668091 |
| non_executable_failure | canonical -> disp_3 | 20 | 0.5700 | 0.5767 | 0.0067 | [-0.0767, 0.1000] | 0.946716 |
| non_executable_failure | canonical -> plan_front | 20 | 0.5700 | 0.5233 | -0.0467 | [-0.1167, 0.0233] | 0.263855 |
| non_executable_failure | canonical -> plan_back | 20 | 0.5700 | 0.5500 | -0.0200 | [-0.0733, 0.0400] | 0.591064 |
| non_executable_failure | canonical -> plan_scatter | 20 | 0.5700 | 0.4967 | -0.0733 | [-0.1500, 0.0033] | 0.101929 |
| conditional_reachability | canonical -> disp_1 | 19 | 0.4951 | 0.4041 | -0.0910 | [-0.1959, 0.0088] | 0.113281 |
| conditional_reachability | canonical -> disp_2 | 20 | 0.4954 | 0.3783 | -0.1170 | [-0.2507, 0.0111] | 0.119141 |
| conditional_reachability | canonical -> disp_3 | 19 | 0.5214 | 0.3141 | -0.2073 | [-0.3346, -0.0850] | 0.006836 |
| conditional_reachability | canonical -> plan_front | 20 | 0.4954 | 0.3696 | -0.1258 | [-0.2295, -0.0286] | 0.027344 |
| conditional_reachability | canonical -> plan_back | 20 | 0.4954 | 0.4122 | -0.0832 | [-0.1943, 0.0387] | 0.189453 |
| conditional_reachability | canonical -> plan_scatter | 19 | 0.5214 | 0.3806 | -0.1408 | [-0.2847, -0.0057] | 0.067383 |
| plan_length | canonical -> disp_1 | 11 | 18.2999 | 18.2100 | -0.0899 | [-1.5970, 1.4754] | 0.867188 |
| plan_length | canonical -> disp_2 | 12 | 18.6082 | 17.9911 | -0.6172 | [-1.3698, 0.1485] | 0.164062 |
| plan_length | canonical -> disp_3 | 10 | 16.9299 | 15.8611 | -1.0688 | [-2.3088, -0.1400] | 0.062500 |
| plan_length | canonical -> plan_front | 12 | 19.0249 | 18.2611 | -0.7638 | [-2.0397, 0.4185] | 0.298828 |
| plan_length | canonical -> plan_back | 10 | 15.6299 | 15.6114 | -0.0185 | [-0.8515, 0.6533] | 0.976562 |
| plan_length | canonical -> plan_scatter | 10 | 15.6299 | 14.5217 | -1.1082 | [-2.4127, -0.0356] | 0.148438 |
| optimality_ratio | canonical -> disp_1 | 11 | 1.1447 | 1.1196 | -0.0252 | [-0.1248, 0.0736] | 0.687500 |
| optimality_ratio | canonical -> disp_2 | 12 | 1.1461 | 1.0990 | -0.0470 | [-0.1012, 0.0016] | 0.125000 |
| optimality_ratio | canonical -> disp_3 | 10 | 1.1526 | 1.0743 | -0.0783 | [-0.1645, -0.0090] | 0.070312 |
| optimality_ratio | canonical -> plan_front | 12 | 1.1327 | 1.0753 | -0.0574 | [-0.1396, 0.0135] | 0.212891 |
| optimality_ratio | canonical -> plan_back | 10 | 1.1610 | 1.1601 | -0.0009 | [-0.0443, 0.0387] | 0.972656 |
| optimality_ratio | canonical -> plan_scatter | 10 | 1.1610 | 1.0823 | -0.0786 | [-0.1671, -0.0058] | 0.101562 |
| first_failure_step | canonical -> disp_1 | 15 | 9.8369 | 9.2269 | -0.6100 | [-1.7354, 0.5506] | 0.319458 |
| first_failure_step | canonical -> disp_2 | 16 | 10.1041 | 9.7946 | -0.3094 | [-1.9771, 1.5454] | 0.751648 |
| first_failure_step | canonical -> disp_3 | 16 | 10.1041 | 7.5760 | -2.5281 | [-4.2000, -1.0512] | 0.003662 |
| first_failure_step | canonical -> plan_front | 16 | 10.1041 | 9.2427 | -0.8614 | [-2.4183, 0.5726] | 0.293549 |
| first_failure_step | canonical -> plan_back | 16 | 10.1041 | 7.5656 | -2.5385 | [-4.2904, -0.7244] | 0.019348 |
| first_failure_step | canonical -> plan_scatter | 16 | 10.1041 | 7.5774 | -2.5267 | [-4.4537, -0.6533] | 0.024628 |
| prompt_tokens | canonical -> disp_1 | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> plan_front | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> plan_back | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| completion_tokens | canonical -> disp_1 | 20 | 8628.5433 | 8109.4767 | -519.0667 | [-1075.6715, 22.2318] | 0.088171 |
| completion_tokens | canonical -> disp_2 | 20 | 8628.5433 | 8098.6533 | -529.8900 | [-1117.5039, 82.1195] | 0.110170 |
| completion_tokens | canonical -> disp_3 | 20 | 8628.5433 | 7817.2400 | -811.3033 | [-1218.2876, -371.8300] | 0.002544 |
| completion_tokens | canonical -> plan_front | 20 | 8628.5433 | 7580.8400 | -1047.7033 | [-1464.8900, -627.9895] | 0.000160 |
| completion_tokens | canonical -> plan_back | 20 | 8628.5433 | 7921.9633 | -706.5800 | [-1340.9330, -47.5266] | 0.052200 |
| completion_tokens | canonical -> plan_scatter | 20 | 8628.5433 | 7939.9867 | -688.5567 | [-1284.2442, -103.0848] | 0.039032 |
| reasoning_completion_tokens | canonical -> disp_1 | 20 | 8628.5433 | 8109.4767 | -519.0667 | [-1075.6715, 22.2318] | 0.088171 |
| reasoning_completion_tokens | canonical -> disp_2 | 20 | 8628.5433 | 8098.6533 | -529.8900 | [-1117.5039, 82.1195] | 0.110170 |
| reasoning_completion_tokens | canonical -> disp_3 | 20 | 8628.5433 | 7817.2400 | -811.3033 | [-1218.2876, -371.8300] | 0.002544 |
| reasoning_completion_tokens | canonical -> plan_front | 20 | 8628.5433 | 7580.8400 | -1047.7033 | [-1464.8900, -627.9895] | 0.000160 |
| reasoning_completion_tokens | canonical -> plan_back | 20 | 8628.5433 | 7921.9633 | -706.5800 | [-1340.9330, -47.5266] | 0.052200 |
| reasoning_completion_tokens | canonical -> plan_scatter | 20 | 8628.5433 | 7939.9867 | -688.5567 | [-1284.2442, -103.0848] | 0.039032 |
| raw_completion_tokens | canonical -> disp_1 | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | canonical -> plan_front | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | canonical -> plan_back | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| total_tokens | canonical -> disp_1 | 20 | 17372.4433 | 16853.3767 | -519.0667 | [-1075.6715, 22.2318] | 0.088171 |
| total_tokens | canonical -> disp_2 | 20 | 17372.4433 | 16842.5533 | -529.8900 | [-1117.5039, 82.1195] | 0.110170 |
| total_tokens | canonical -> disp_3 | 20 | 17372.4433 | 16561.1400 | -811.3033 | [-1218.2876, -371.8300] | 0.002544 |
| total_tokens | canonical -> plan_front | 20 | 17372.4433 | 16324.7400 | -1047.7033 | [-1464.8900, -627.9895] | 0.000160 |
| total_tokens | canonical -> plan_back | 20 | 17372.4433 | 16665.8633 | -706.5800 | [-1340.9330, -47.5266] | 0.052200 |
| total_tokens | canonical -> plan_scatter | 20 | 17372.4433 | 16683.8867 | -688.5567 | [-1284.2442, -103.0848] | 0.039032 |
| duration_sec | canonical -> disp_1 | 20 | 175.9562 | 168.9305 | -7.0257 | [-19.7289, 5.7558] | 0.311136 |
| duration_sec | canonical -> disp_2 | 20 | 175.9562 | 163.8735 | -12.0827 | [-27.6076, 4.2929] | 0.167236 |
| duration_sec | canonical -> disp_3 | 20 | 175.9562 | 160.8507 | -15.1055 | [-30.7850, 1.0253] | 0.086746 |
| duration_sec | canonical -> plan_front | 20 | 175.9562 | 151.7043 | -24.2519 | [-41.3798, -8.1901] | 0.011168 |
| duration_sec | canonical -> plan_back | 20 | 175.9562 | 213.0387 | 37.0825 | [2.3064, 83.6516] | 0.078547 |
| duration_sec | canonical -> plan_scatter | 20 | 175.9562 | 161.0220 | -14.9342 | [-31.9642, 1.7236] | 0.106258 |
