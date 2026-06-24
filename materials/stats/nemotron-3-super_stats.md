# Statistical Tests: nemotron-3-super

Baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_scatter`.
Extra comparisons: `plan_front` vs `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 100 | 0.1500 | 0.1500 | 9 | 9 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| reachability | canonical -> disp_2 | 100 | 0.1500 | 0.1700 | 10 | 8 | 0.0200 | 1.2500 | 0.814529 | 1.000000 |
| reachability | canonical -> disp_3 | 100 | 0.1500 | 0.1500 | 8 | 8 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| reachability | canonical -> plan_front | 100 | 0.1500 | 0.3200 | 22 | 5 | 0.1700 | 4.4000 | 0.001514 | 0.007569 |
| reachability | canonical -> plan_scatter | 100 | 0.1500 | 0.1300 | 7 | 9 | -0.0200 | 0.7778 | 0.803619 | 1.000000 |
| reachability | plan_front -> plan_scatter | 100 | 0.3200 | 0.1300 | 4 | 23 | -0.1900 | 0.1739 | 0.000311 | 0.000311 |
| executability | canonical -> disp_1 | 100 | 0.6900 | 0.6100 | 21 | 29 | -0.0800 | 0.7241 | 0.322236 | 0.966709 |
| executability | canonical -> disp_2 | 100 | 0.6900 | 0.6300 | 20 | 26 | -0.0600 | 0.7692 | 0.461391 | 0.966709 |
| executability | canonical -> disp_3 | 100 | 0.6900 | 0.5400 | 16 | 31 | -0.1500 | 0.5161 | 0.039986 | 0.159944 |
| executability | canonical -> plan_front | 100 | 0.6900 | 0.6800 | 20 | 21 | -0.0100 | 0.9524 | 1.000000 | 1.000000 |
| executability | canonical -> plan_scatter | 100 | 0.6900 | 0.5200 | 13 | 30 | -0.1700 | 0.4333 | 0.013718 | 0.068591 |
| executability | plan_front -> plan_scatter | 100 | 0.6800 | 0.5200 | 20 | 36 | -0.1600 | 0.5556 | 0.044047 | 0.044047 |
| non_executable_failure | canonical -> disp_1 | 100 | 0.3100 | 0.3900 | 29 | 21 | 0.0800 | 1.3810 | 0.322236 | 0.966709 |
| non_executable_failure | canonical -> disp_2 | 100 | 0.3100 | 0.3700 | 26 | 20 | 0.0600 | 1.3000 | 0.461391 | 0.966709 |
| non_executable_failure | canonical -> disp_3 | 100 | 0.3100 | 0.4600 | 31 | 16 | 0.1500 | 1.9375 | 0.039986 | 0.159944 |
| non_executable_failure | canonical -> plan_front | 100 | 0.3100 | 0.3200 | 21 | 20 | 0.0100 | 1.0500 | 1.000000 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 100 | 0.3100 | 0.4800 | 30 | 13 | 0.1700 | 2.3077 | 0.013718 | 0.068591 |
| non_executable_failure | plan_front -> plan_scatter | 100 | 0.3200 | 0.4800 | 36 | 20 | 0.1600 | 1.8000 | 0.044047 | 0.044047 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 70 | 61 | 0.2286 | 0.2459 | 16/54 | 15/46 | 0.0173 | 1.1005 | 0.839342 | 1.000000 |
| conditional_reachability | canonical -> disp_2 | 70 | 63 | 0.2286 | 0.2698 | 16/54 | 17/46 | 0.0413 | 1.2473 | 0.688361 | 1.000000 |
| conditional_reachability | canonical -> disp_3 | 70 | 54 | 0.2286 | 0.2778 | 16/54 | 15/39 | 0.0492 | 1.2981 | 0.538671 | 1.000000 |
| conditional_reachability | canonical -> plan_front | 70 | 68 | 0.2286 | 0.4706 | 16/54 | 32/36 | 0.2420 | 3.0000 | 0.004061 | 0.020305 |
| conditional_reachability | canonical -> plan_scatter | 70 | 52 | 0.2286 | 0.2500 | 16/54 | 13/39 | 0.0214 | 1.1250 | 0.831606 | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 68 | 52 | 0.4706 | 0.2500 | 32/36 | 13/39 | -0.2206 | 0.3750 | 0.014519 | 0.014519 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 6 | 7.0000 | 7.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | canonical -> disp_2 | 7 | 7.4286 | 7.4286 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | canonical -> disp_3 | 7 | 7.4286 | 7.4286 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | canonical -> plan_front | 10 | 8.1000 | 8.1000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | canonical -> plan_scatter | 6 | 7.3333 | 7.3333 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | plan_front -> plan_scatter | 9 | 7.6667 | 7.6667 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_1 | 6 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 7 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 7 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 10 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> plan_scatter | 6 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | plan_front -> plan_scatter | 9 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| first_failure_step | canonical -> disp_1 | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | canonical -> disp_2 | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | canonical -> disp_3 | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | canonical -> plan_front | 1 | 3.0000 | 4.0000 | 1.0000 | 0.3333 | NA | NA | 1.000000 | 1.000000 |
| first_failure_step | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | plan_front -> plan_scatter | 2 | 40.0000 | 1.0000 | -39.0000 | -0.9750 | -1.9698 | 0.219409 | 0.500000 | 0.500000 |
| prompt_tokens | canonical -> disp_1 | 100 | 9960.1600 | 10123.3200 | 163.1600 | 0.0164 | 0.1494 | 0.138371 | 0.142740 | 0.713700 |
| prompt_tokens | canonical -> disp_2 | 100 | 9960.1600 | 9973.6400 | 13.4800 | 0.0014 | 0.0132 | 0.895217 | 0.891590 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 100 | 9960.1600 | 9967.3100 | 7.1500 | 0.0007 | 0.0067 | 0.946347 | 0.932350 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 100 | 9960.1600 | 9881.2200 | -78.9400 | -0.0079 | -0.0839 | 0.403757 | 0.431290 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 100 | 9960.1600 | 9862.8800 | -97.2800 | -0.0098 | -0.1092 | 0.277478 | 0.283813 | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 100 | 9881.2200 | 9862.8800 | -18.3400 | -0.0019 | -0.0206 | 0.837126 | 0.831909 | 0.831909 |
| completion_tokens | canonical -> disp_1 | 100 | 36999.8600 | 33874.8000 | -3125.0600 | -0.0845 | -0.0965 | 0.336962 | 0.337800 | 0.337800 |
| completion_tokens | canonical -> disp_2 | 100 | 36999.8600 | 32287.4400 | -4712.4200 | -0.1274 | -0.1439 | 0.153269 | 0.155870 | 0.311740 |
| completion_tokens | canonical -> disp_3 | 100 | 36999.8600 | 29827.3400 | -7172.5200 | -0.1939 | -0.1946 | 0.054495 | 0.055180 | 0.165540 |
| completion_tokens | canonical -> plan_front | 100 | 36999.8600 | 28838.4400 | -8161.4200 | -0.2206 | -0.2436 | 0.016644 | 0.017050 | 0.068200 |
| completion_tokens | canonical -> plan_scatter | 100 | 36999.8600 | 26608.9900 | -10390.8700 | -0.2808 | -0.3061 | 0.002844 | 0.002580 | 0.012900 |
| completion_tokens | plan_front -> plan_scatter | 100 | 28838.4400 | 26608.9900 | -2229.4500 | -0.0773 | -0.0769 | 0.443863 | 0.442730 | 0.442730 |
| reasoning_completion_tokens | canonical -> disp_1 | 100 | 36773.1000 | 33699.4100 | -3073.6900 | -0.0836 | -0.0953 | 0.342730 | 0.344140 | 0.344140 |
| reasoning_completion_tokens | canonical -> disp_2 | 100 | 36773.1000 | 32129.6100 | -4643.4900 | -0.1263 | -0.1443 | 0.152093 | 0.154910 | 0.309820 |
| reasoning_completion_tokens | canonical -> disp_3 | 100 | 36773.1000 | 29795.0200 | -6978.0800 | -0.1898 | -0.1895 | 0.060993 | 0.061380 | 0.184140 |
| reasoning_completion_tokens | canonical -> plan_front | 100 | 36773.1000 | 27821.7700 | -8951.3300 | -0.2434 | -0.2623 | 0.010106 | 0.010140 | 0.040560 |
| reasoning_completion_tokens | canonical -> plan_scatter | 100 | 36773.1000 | 26562.1400 | -10210.9600 | -0.2777 | -0.3019 | 0.003222 | 0.003430 | 0.017150 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 100 | 27821.7700 | 26562.1400 | -1259.6300 | -0.0453 | -0.0447 | 0.655941 | 0.659180 | 0.659180 |
| raw_completion_tokens | canonical -> disp_1 | 100 | 226.7600 | 175.3900 | -51.3700 | -0.2265 | -0.0181 | 0.856511 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 100 | 226.7600 | 157.8300 | -68.9300 | -0.3040 | -0.0248 | 0.804401 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 100 | 226.7600 | 32.3200 | -194.4400 | -0.8575 | -0.0850 | 0.397498 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> plan_front | 100 | 226.7600 | 1016.6700 | 789.9100 | 3.4835 | 0.1036 | 0.302941 | 0.500000 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 100 | 226.7600 | 46.8500 | -179.9100 | -0.7934 | -0.0776 | 0.439892 | 1.000000 | 1.000000 |
| raw_completion_tokens | plan_front -> plan_scatter | 100 | 1016.6700 | 46.8500 | -969.8200 | -0.9539 | -0.1333 | 0.185432 | 0.500000 | 0.500000 |
| total_tokens | canonical -> disp_1 | 100 | 46570.8100 | 43998.1200 | -2572.6900 | -0.0552 | -0.0782 | 0.435818 | 0.437490 | 0.437490 |
| total_tokens | canonical -> disp_2 | 100 | 46570.8100 | 42261.0800 | -4309.7300 | -0.0925 | -0.1302 | 0.195844 | 0.198430 | 0.396860 |
| total_tokens | canonical -> disp_3 | 100 | 46570.8100 | 39794.6500 | -6776.1600 | -0.1455 | -0.1802 | 0.074606 | 0.074720 | 0.224160 |
| total_tokens | canonical -> plan_front | 100 | 46570.8100 | 38474.1900 | -8096.6200 | -0.1739 | -0.2385 | 0.018997 | 0.019450 | 0.077800 |
| total_tokens | canonical -> plan_scatter | 100 | 46570.8100 | 36471.8700 | -10098.9400 | -0.2169 | -0.2928 | 0.004229 | 0.003850 | 0.019250 |
| total_tokens | plan_front -> plan_scatter | 100 | 38474.1900 | 36471.8700 | -2002.3200 | -0.0520 | -0.0683 | 0.496223 | 0.495900 | 0.495900 |
| duration_sec | canonical -> disp_1 | 100 | 384.1684 | 386.4816 | 2.3132 | 0.0060 | 0.0064 | 0.949100 | 0.952160 | 1.000000 |
| duration_sec | canonical -> disp_2 | 100 | 384.1684 | 371.2508 | -12.9176 | -0.0336 | -0.0360 | 0.719676 | 0.722190 | 1.000000 |
| duration_sec | canonical -> disp_3 | 100 | 384.1684 | 366.8080 | -17.3604 | -0.0452 | -0.0445 | 0.656959 | 0.658560 | 1.000000 |
| duration_sec | canonical -> plan_front | 100 | 384.1684 | 350.9097 | -33.2587 | -0.0866 | -0.0874 | 0.384200 | 0.393340 | 1.000000 |
| duration_sec | canonical -> plan_scatter | 100 | 384.1684 | 295.5429 | -88.6255 | -0.2307 | -0.2671 | 0.008830 | 0.007470 | 0.037350 |
| duration_sec | plan_front -> plan_scatter | 100 | 350.9097 | 295.5429 | -55.3668 | -0.1578 | -0.2068 | 0.041245 | 0.041410 | 0.041410 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> plan_scatter | 20 | 0.3200 | 0.1300 | -0.1900 | [-0.3200, -0.0700] | 0.012207 |
| executability | plan_front -> plan_scatter | 20 | 0.6800 | 0.5200 | -0.1600 | [-0.3100, -0.0100] | 0.080322 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.3200 | 0.4800 | 0.1600 | [0.0100, 0.3100] | 0.080322 |
| conditional_reachability | plan_front -> plan_scatter | 19 | 0.4070 | 0.2412 | -0.1658 | [-0.3123, -0.0333] | 0.031250 |
| plan_length | plan_front -> plan_scatter | 6 | 15.5000 | 14.8889 | -0.6111 | [-1.6111, 0.0000] | 0.500000 |
| optimality_ratio | plan_front -> plan_scatter | 6 | 1.0881 | 1.0492 | -0.0389 | [-0.1103, 0.0000] | 0.500000 |
| first_failure_step | plan_front -> plan_scatter | 3 | 28.1111 | 4.5333 | -23.5778 | [-45.4000, 1.0000] | 0.500000 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 9881.2200 | 9862.8800 | -18.3400 | [-201.9903, 171.9747] | 0.875000 |
| completion_tokens | plan_front -> plan_scatter | 20 | 28838.4400 | 26608.9900 | -2229.4500 | [-8637.4655, 4123.3677] | 0.513929 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 27821.7700 | 26562.1400 | -1259.6300 | [-7723.6925, 5093.0920] | 0.713362 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 1016.6700 | 46.8500 | -969.8200 | [-2532.0200, 93.6000] | 0.500000 |
| total_tokens | plan_front -> plan_scatter | 20 | 38474.1900 | 36471.8700 | -2002.3200 | [-8448.2930, 4318.3312] | 0.557144 |
| duration_sec | plan_front -> plan_scatter | 20 | 350.9097 | 295.5429 | -55.3668 | [-107.7958, -5.6647] | 0.052309 |
