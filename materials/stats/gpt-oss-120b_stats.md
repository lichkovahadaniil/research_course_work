# Statistical Tests: gpt-oss-120b

Primary baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_back`, `plan_scatter`.
`plan_front` baseline comparisons: `plan_front` vs `canonical`, `plan_front` vs `disp_1`, `plan_front` vs `disp_2`, `plan_front` vs `disp_3`, `plan_front` vs `plan_back`, `plan_front` vs `plan_scatter`.

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
| reachability | plan_front -> canonical | 300 | 0.2933 | 0.3067 | 25 | 21 | 0.0133 | 1.1905 | 0.658738 | 1.000000 |
| reachability | plan_front -> disp_1 | 300 | 0.2933 | 0.2967 | 17 | 16 | 0.0033 | 1.0625 | 1.000000 | 1.000000 |
| reachability | plan_front -> disp_2 | 300 | 0.2933 | 0.2667 | 15 | 23 | -0.0267 | 0.6522 | 0.255875 | 1.000000 |
| reachability | plan_front -> disp_3 | 300 | 0.2933 | 0.2233 | 8 | 29 | -0.0700 | 0.2759 | 0.000753 | 0.004517 |
| reachability | plan_front -> plan_back | 300 | 0.2933 | 0.2800 | 17 | 21 | -0.0133 | 0.8095 | 0.627103 | 1.000000 |
| reachability | plan_front -> plan_scatter | 300 | 0.2933 | 0.2767 | 16 | 21 | -0.0167 | 0.7619 | 0.511376 | 1.000000 |
| executability | canonical -> disp_1 | 300 | 0.4300 | 0.4567 | 53 | 45 | 0.0267 | 1.1778 | 0.479692 | 1.000000 |
| executability | canonical -> disp_2 | 300 | 0.4300 | 0.4500 | 57 | 51 | 0.0200 | 1.1176 | 0.630634 | 1.000000 |
| executability | canonical -> disp_3 | 300 | 0.4300 | 0.4233 | 56 | 58 | -0.0067 | 0.9655 | 0.925435 | 1.000000 |
| executability | canonical -> plan_front | 300 | 0.4300 | 0.4767 | 57 | 43 | 0.0467 | 1.3256 | 0.193348 | 0.966740 |
| executability | canonical -> plan_back | 300 | 0.4300 | 0.4500 | 55 | 49 | 0.0200 | 1.1224 | 0.624144 | 1.000000 |
| executability | canonical -> plan_scatter | 300 | 0.4300 | 0.5033 | 59 | 37 | 0.0733 | 1.5946 | 0.031548 | 0.189289 |
| executability | plan_front -> canonical | 300 | 0.4767 | 0.4300 | 43 | 57 | -0.0467 | 0.7544 | 0.193348 | 0.966740 |
| executability | plan_front -> disp_1 | 300 | 0.4767 | 0.4567 | 40 | 46 | -0.0200 | 0.8696 | 0.590036 | 1.000000 |
| executability | plan_front -> disp_2 | 300 | 0.4767 | 0.4500 | 52 | 60 | -0.0267 | 0.8667 | 0.508513 | 1.000000 |
| executability | plan_front -> disp_3 | 300 | 0.4767 | 0.4233 | 40 | 56 | -0.0533 | 0.7143 | 0.125346 | 0.752074 |
| executability | plan_front -> plan_back | 300 | 0.4767 | 0.4500 | 47 | 55 | -0.0267 | 0.8545 | 0.488434 | 1.000000 |
| executability | plan_front -> plan_scatter | 300 | 0.4767 | 0.5033 | 59 | 51 | 0.0267 | 1.1569 | 0.504685 | 1.000000 |
| non_executable_failure | canonical -> disp_1 | 300 | 0.5700 | 0.5433 | 45 | 53 | -0.0267 | 0.8491 | 0.479692 | 1.000000 |
| non_executable_failure | canonical -> disp_2 | 300 | 0.5700 | 0.5500 | 51 | 57 | -0.0200 | 0.8947 | 0.630634 | 1.000000 |
| non_executable_failure | canonical -> disp_3 | 300 | 0.5700 | 0.5767 | 58 | 56 | 0.0067 | 1.0357 | 0.925435 | 1.000000 |
| non_executable_failure | canonical -> plan_front | 300 | 0.5700 | 0.5233 | 43 | 57 | -0.0467 | 0.7544 | 0.193348 | 0.966740 |
| non_executable_failure | canonical -> plan_back | 300 | 0.5700 | 0.5500 | 49 | 55 | -0.0200 | 0.8909 | 0.624144 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 300 | 0.5700 | 0.4967 | 37 | 59 | -0.0733 | 0.6271 | 0.031548 | 0.189289 |
| non_executable_failure | plan_front -> canonical | 300 | 0.5233 | 0.5700 | 57 | 43 | 0.0467 | 1.3256 | 0.193348 | 0.966740 |
| non_executable_failure | plan_front -> disp_1 | 300 | 0.5233 | 0.5433 | 46 | 40 | 0.0200 | 1.1500 | 0.590036 | 1.000000 |
| non_executable_failure | plan_front -> disp_2 | 300 | 0.5233 | 0.5500 | 60 | 52 | 0.0267 | 1.1538 | 0.508513 | 1.000000 |
| non_executable_failure | plan_front -> disp_3 | 300 | 0.5233 | 0.5767 | 56 | 40 | 0.0533 | 1.4000 | 0.125346 | 0.752074 |
| non_executable_failure | plan_front -> plan_back | 300 | 0.5233 | 0.5500 | 55 | 47 | 0.0267 | 1.1702 | 0.488434 | 1.000000 |
| non_executable_failure | plan_front -> plan_scatter | 300 | 0.5233 | 0.4967 | 51 | 59 | -0.0267 | 0.8644 | 0.504685 | 1.000000 |

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
| conditional_reachability | plan_front -> canonical | 143 | 129 | 0.6154 | 0.7132 | 88/55 | 92/37 | 0.0978 | 1.5541 | 0.096474 | 0.578841 |
| conditional_reachability | plan_front -> disp_1 | 143 | 137 | 0.6154 | 0.6496 | 88/55 | 89/48 | 0.0343 | 1.1589 | 0.620241 | 1.000000 |
| conditional_reachability | plan_front -> disp_2 | 143 | 135 | 0.6154 | 0.5926 | 88/55 | 80/55 | -0.0228 | 0.9091 | 0.714293 | 1.000000 |
| conditional_reachability | plan_front -> disp_3 | 143 | 127 | 0.6154 | 0.5276 | 88/55 | 67/60 | -0.0878 | 0.6979 | 0.175024 | 0.875120 |
| conditional_reachability | plan_front -> plan_back | 143 | 135 | 0.6154 | 0.6222 | 88/55 | 84/51 | 0.0068 | 1.0294 | 1.000000 | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 143 | 151 | 0.6154 | 0.5497 | 88/55 | 83/68 | -0.0657 | 0.7629 | 0.287519 | 1.000000 |

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
| plan_length | plan_front -> canonical | 67 | 9.8209 | 10.6716 | 0.8507 | 0.0866 | 0.2031 | 0.101233 | 0.069641 | 0.417847 |
| plan_length | plan_front -> disp_1 | 72 | 10.0694 | 10.1944 | 0.1250 | 0.0124 | 0.1033 | 0.383499 | 0.500000 | 1.000000 |
| plan_length | plan_front -> disp_2 | 65 | 9.2615 | 9.6308 | 0.3692 | 0.0399 | 0.1391 | 0.266385 | 0.328125 | 1.000000 |
| plan_length | plan_front -> disp_3 | 59 | 9.0847 | 9.0678 | -0.0169 | -0.0019 | -0.0578 | 0.658579 | 1.000000 | 1.000000 |
| plan_length | plan_front -> plan_back | 67 | 9.3731 | 10.1045 | 0.7313 | 0.0780 | 0.1827 | 0.139485 | 0.179688 | 0.898438 |
| plan_length | plan_front -> plan_scatter | 67 | 9.5075 | 9.5821 | 0.0746 | 0.0078 | 0.1222 | 0.320963 | 0.500000 | 1.000000 |
| optimality_ratio | canonical -> disp_1 | 62 | 1.1101 | 1.0201 | -0.0900 | -0.0811 | -0.2371 | 0.066670 | 0.011719 | 0.070312 |
| optimality_ratio | canonical -> disp_2 | 62 | 1.1005 | 1.0233 | -0.0772 | -0.0701 | -0.2080 | 0.106676 | 0.047607 | 0.238037 |
| optimality_ratio | canonical -> disp_3 | 50 | 1.0991 | 1.0110 | -0.0882 | -0.0802 | -0.2121 | 0.140120 | 0.125000 | 0.250000 |
| optimality_ratio | canonical -> plan_front | 67 | 1.0933 | 1.0214 | -0.0719 | -0.0658 | -0.1984 | 0.109177 | 0.059814 | 0.238037 |
| optimality_ratio | canonical -> plan_back | 64 | 1.0734 | 1.0956 | 0.0221 | 0.0206 | 0.0463 | 0.712454 | 0.745239 | 0.745239 |
| optimality_ratio | canonical -> plan_scatter | 63 | 1.0993 | 1.0233 | -0.0761 | -0.0692 | -0.2042 | 0.110221 | 0.054688 | 0.238037 |
| optimality_ratio | plan_front -> canonical | 67 | 1.0214 | 1.0933 | 0.0719 | 0.0704 | 0.1984 | 0.109177 | 0.059814 | 0.358887 |
| optimality_ratio | plan_front -> disp_1 | 72 | 1.0152 | 1.0182 | 0.0030 | 0.0030 | 0.0383 | 0.746192 | 0.769531 | 1.000000 |
| optimality_ratio | plan_front -> disp_2 | 65 | 1.0075 | 1.0329 | 0.0255 | 0.0253 | 0.1406 | 0.261118 | 0.289062 | 1.000000 |
| optimality_ratio | plan_front -> disp_3 | 59 | 1.0042 | 1.0011 | -0.0031 | -0.0031 | -0.0919 | 0.483292 | 1.000000 | 1.000000 |
| optimality_ratio | plan_front -> plan_back | 67 | 1.0188 | 1.0786 | 0.0597 | 0.0586 | 0.1697 | 0.169483 | 0.210938 | 1.000000 |
| optimality_ratio | plan_front -> plan_scatter | 67 | 1.0046 | 1.0102 | 0.0056 | 0.0055 | 0.0951 | 0.439235 | 0.500000 | 1.000000 |
| first_failure_step | canonical -> disp_1 | 69 | 10.2899 | 9.5072 | -0.7826 | -0.0761 | -0.0907 | 0.454027 | 0.461600 | 0.923200 |
| first_failure_step | canonical -> disp_2 | 70 | 11.3286 | 10.6857 | -0.6429 | -0.0567 | -0.0664 | 0.580101 | 0.590760 | 0.923200 |
| first_failure_step | canonical -> disp_3 | 67 | 11.2836 | 8.3433 | -2.9403 | -0.2606 | -0.3216 | 0.010553 | 0.010430 | 0.052150 |
| first_failure_step | canonical -> plan_front | 64 | 11.4219 | 9.9688 | -1.4531 | -0.1272 | -0.1547 | 0.220344 | 0.225080 | 0.675240 |
| first_failure_step | canonical -> plan_back | 67 | 9.8806 | 7.1791 | -2.7015 | -0.2734 | -0.3408 | 0.006897 | 0.006740 | 0.040440 |
| first_failure_step | canonical -> plan_scatter | 52 | 9.8269 | 8.0769 | -1.7500 | -0.1781 | -0.2324 | 0.099882 | 0.104110 | 0.416440 |
| first_failure_step | plan_front -> canonical | 64 | 9.9688 | 11.4219 | 1.4531 | 0.1458 | 0.1547 | 0.220344 | 0.225080 | 0.717160 |
| first_failure_step | plan_front -> disp_1 | 48 | 10.2708 | 9.4792 | -0.7917 | -0.0771 | -0.1106 | 0.447338 | 0.463760 | 0.927520 |
| first_failure_step | plan_front -> disp_2 | 50 | 9.7000 | 9.1400 | -0.5600 | -0.0577 | -0.0665 | 0.640353 | 0.655170 | 0.927520 |
| first_failure_step | plan_front -> disp_3 | 58 | 10.0690 | 8.5345 | -1.5345 | -0.1524 | -0.1818 | 0.171568 | 0.179290 | 0.717160 |
| first_failure_step | plan_front -> plan_back | 51 | 9.7059 | 6.8235 | -2.8824 | -0.2970 | -0.3822 | 0.008731 | 0.009250 | 0.055500 |
| first_failure_step | plan_front -> plan_scatter | 39 | 10.7692 | 8.6410 | -2.1282 | -0.1976 | -0.2706 | 0.099229 | 0.104160 | 0.520800 |
| prompt_tokens | canonical -> disp_1 | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_back | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> canonical | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> disp_1 | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> disp_2 | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> disp_3 | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> plan_back | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 300 | 8743.9000 | 8743.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> disp_1 | 300 | 8628.5433 | 8109.4767 | -519.0667 | -0.0602 | -0.1138 | 0.049683 | 0.048760 | 0.094460 |
| completion_tokens | canonical -> disp_2 | 300 | 8628.5433 | 8098.6533 | -529.8900 | -0.0614 | -0.1147 | 0.047807 | 0.047230 | 0.094460 |
| completion_tokens | canonical -> disp_3 | 300 | 8628.5433 | 7817.2400 | -811.3033 | -0.0940 | -0.1957 | 0.000792 | 0.000590 | 0.002950 |
| completion_tokens | canonical -> plan_front | 300 | 8628.5433 | 7580.8400 | -1047.7033 | -0.1214 | -0.2426 | 0.000035 | 0.000030 | 0.000180 |
| completion_tokens | canonical -> plan_back | 300 | 8628.5433 | 7921.9633 | -706.5800 | -0.0819 | -0.1477 | 0.011033 | 0.011040 | 0.044160 |
| completion_tokens | canonical -> plan_scatter | 300 | 8628.5433 | 7939.9867 | -688.5567 | -0.0798 | -0.1410 | 0.015170 | 0.015270 | 0.045810 |
| completion_tokens | plan_front -> canonical | 300 | 7580.8400 | 8628.5433 | 1047.7033 | 0.1382 | 0.2426 | 0.000035 | 0.000030 | 0.000180 |
| completion_tokens | plan_front -> disp_1 | 300 | 7580.8400 | 8109.4767 | 528.6367 | 0.0697 | 0.1235 | 0.033295 | 0.033510 | 0.167550 |
| completion_tokens | plan_front -> disp_2 | 300 | 7580.8400 | 8098.6533 | 517.8133 | 0.0683 | 0.1091 | 0.059846 | 0.060620 | 0.242480 |
| completion_tokens | plan_front -> disp_3 | 300 | 7580.8400 | 7817.2400 | 236.4000 | 0.0312 | 0.0589 | 0.308452 | 0.307750 | 0.447990 |
| completion_tokens | plan_front -> plan_back | 300 | 7580.8400 | 7921.9633 | 341.1233 | 0.0450 | 0.0724 | 0.211075 | 0.212540 | 0.447990 |
| completion_tokens | plan_front -> plan_scatter | 300 | 7580.8400 | 7939.9867 | 359.1467 | 0.0474 | 0.0836 | 0.148585 | 0.149330 | 0.447990 |
| reasoning_completion_tokens | canonical -> disp_1 | 300 | 8628.5433 | 8109.4767 | -519.0667 | -0.0602 | -0.1138 | 0.049683 | 0.048760 | 0.094460 |
| reasoning_completion_tokens | canonical -> disp_2 | 300 | 8628.5433 | 8098.6533 | -529.8900 | -0.0614 | -0.1147 | 0.047807 | 0.047230 | 0.094460 |
| reasoning_completion_tokens | canonical -> disp_3 | 300 | 8628.5433 | 7817.2400 | -811.3033 | -0.0940 | -0.1957 | 0.000792 | 0.000590 | 0.002950 |
| reasoning_completion_tokens | canonical -> plan_front | 300 | 8628.5433 | 7580.8400 | -1047.7033 | -0.1214 | -0.2426 | 0.000035 | 0.000030 | 0.000180 |
| reasoning_completion_tokens | canonical -> plan_back | 300 | 8628.5433 | 7921.9633 | -706.5800 | -0.0819 | -0.1477 | 0.011033 | 0.011040 | 0.044160 |
| reasoning_completion_tokens | canonical -> plan_scatter | 300 | 8628.5433 | 7939.9867 | -688.5567 | -0.0798 | -0.1410 | 0.015170 | 0.015270 | 0.045810 |
| reasoning_completion_tokens | plan_front -> canonical | 300 | 7580.8400 | 8628.5433 | 1047.7033 | 0.1382 | 0.2426 | 0.000035 | 0.000030 | 0.000180 |
| reasoning_completion_tokens | plan_front -> disp_1 | 300 | 7580.8400 | 8109.4767 | 528.6367 | 0.0697 | 0.1235 | 0.033295 | 0.033510 | 0.167550 |
| reasoning_completion_tokens | plan_front -> disp_2 | 300 | 7580.8400 | 8098.6533 | 517.8133 | 0.0683 | 0.1091 | 0.059846 | 0.060620 | 0.242480 |
| reasoning_completion_tokens | plan_front -> disp_3 | 300 | 7580.8400 | 7817.2400 | 236.4000 | 0.0312 | 0.0589 | 0.308452 | 0.307750 | 0.447990 |
| reasoning_completion_tokens | plan_front -> plan_back | 300 | 7580.8400 | 7921.9633 | 341.1233 | 0.0450 | 0.0724 | 0.211075 | 0.212540 | 0.447990 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 300 | 7580.8400 | 7939.9867 | 359.1467 | 0.0474 | 0.0836 | 0.148585 | 0.149330 | 0.447990 |
| raw_completion_tokens | canonical -> disp_1 | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> plan_front | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> plan_back | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | plan_front -> canonical | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | plan_front -> disp_1 | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | plan_front -> disp_2 | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | plan_front -> disp_3 | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | plan_front -> plan_back | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | plan_front -> plan_scatter | 300 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| total_tokens | canonical -> disp_1 | 300 | 17372.4433 | 16853.3767 | -519.0667 | -0.0299 | -0.1138 | 0.049683 | 0.048760 | 0.094460 |
| total_tokens | canonical -> disp_2 | 300 | 17372.4433 | 16842.5533 | -529.8900 | -0.0305 | -0.1147 | 0.047807 | 0.047230 | 0.094460 |
| total_tokens | canonical -> disp_3 | 300 | 17372.4433 | 16561.1400 | -811.3033 | -0.0467 | -0.1957 | 0.000792 | 0.000590 | 0.002950 |
| total_tokens | canonical -> plan_front | 300 | 17372.4433 | 16324.7400 | -1047.7033 | -0.0603 | -0.2426 | 0.000035 | 0.000030 | 0.000180 |
| total_tokens | canonical -> plan_back | 300 | 17372.4433 | 16665.8633 | -706.5800 | -0.0407 | -0.1477 | 0.011033 | 0.011040 | 0.044160 |
| total_tokens | canonical -> plan_scatter | 300 | 17372.4433 | 16683.8867 | -688.5567 | -0.0396 | -0.1410 | 0.015170 | 0.015270 | 0.045810 |
| total_tokens | plan_front -> canonical | 300 | 16324.7400 | 17372.4433 | 1047.7033 | 0.0642 | 0.2426 | 0.000035 | 0.000030 | 0.000180 |
| total_tokens | plan_front -> disp_1 | 300 | 16324.7400 | 16853.3767 | 528.6367 | 0.0324 | 0.1235 | 0.033295 | 0.033510 | 0.167550 |
| total_tokens | plan_front -> disp_2 | 300 | 16324.7400 | 16842.5533 | 517.8133 | 0.0317 | 0.1091 | 0.059846 | 0.060620 | 0.242480 |
| total_tokens | plan_front -> disp_3 | 300 | 16324.7400 | 16561.1400 | 236.4000 | 0.0145 | 0.0589 | 0.308452 | 0.307750 | 0.447990 |
| total_tokens | plan_front -> plan_back | 300 | 16324.7400 | 16665.8633 | 341.1233 | 0.0209 | 0.0724 | 0.211075 | 0.212540 | 0.447990 |
| total_tokens | plan_front -> plan_scatter | 300 | 16324.7400 | 16683.8867 | 359.1467 | 0.0220 | 0.0836 | 0.148585 | 0.149330 | 0.447990 |
| duration_sec | canonical -> disp_1 | 300 | 175.9562 | 168.9305 | -7.0257 | -0.0399 | -0.0692 | 0.231469 | 0.231180 | 0.231180 |
| duration_sec | canonical -> disp_2 | 300 | 175.9562 | 163.8735 | -12.0827 | -0.0687 | -0.1139 | 0.049498 | 0.049900 | 0.099800 |
| duration_sec | canonical -> disp_3 | 300 | 175.9562 | 160.8507 | -15.1055 | -0.0858 | -0.1546 | 0.007841 | 0.007720 | 0.030880 |
| duration_sec | canonical -> plan_front | 300 | 175.9562 | 151.7043 | -24.2519 | -0.1378 | -0.2368 | 0.000053 | 0.000060 | 0.000360 |
| duration_sec | canonical -> plan_back | 300 | 175.9562 | 213.0387 | 37.0825 | 0.2107 | 0.1555 | 0.007462 | 0.005600 | 0.028000 |
| duration_sec | canonical -> plan_scatter | 300 | 175.9562 | 161.0220 | -14.9342 | -0.0849 | -0.1358 | 0.019341 | 0.019210 | 0.057630 |
| duration_sec | plan_front -> canonical | 300 | 151.7043 | 175.9562 | 24.2519 | 0.1599 | 0.2368 | 0.000053 | 0.000060 | 0.000300 |
| duration_sec | plan_front -> disp_1 | 300 | 151.7043 | 168.9305 | 17.2263 | 0.1136 | 0.1744 | 0.002735 | 0.002730 | 0.010920 |
| duration_sec | plan_front -> disp_2 | 300 | 151.7043 | 163.8735 | 12.1692 | 0.0802 | 0.1197 | 0.039043 | 0.039560 | 0.118680 |
| duration_sec | plan_front -> disp_3 | 300 | 151.7043 | 160.8507 | 9.1465 | 0.0603 | 0.1036 | 0.073727 | 0.072990 | 0.145980 |
| duration_sec | plan_front -> plan_back | 300 | 151.7043 | 213.0387 | 61.3344 | 0.4043 | 0.2629 | 0.000008 | 0.000000 | 0.000000 |
| duration_sec | plan_front -> plan_scatter | 300 | 151.7043 | 161.0220 | 9.3178 | 0.0614 | 0.0970 | 0.093908 | 0.094100 | 0.145980 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> canonical | 20 | 0.2933 | 0.3067 | 0.0133 | [-0.0767, 0.1000] | 0.843750 |
| reachability | plan_front -> disp_1 | 20 | 0.2933 | 0.2967 | 0.0033 | [-0.0533, 0.0633] | 1.000000 |
| reachability | plan_front -> disp_2 | 20 | 0.2933 | 0.2667 | -0.0267 | [-0.0833, 0.0233] | 0.429688 |
| reachability | plan_front -> disp_3 | 20 | 0.2933 | 0.2233 | -0.0700 | [-0.1467, -0.0133] | 0.031250 |
| reachability | plan_front -> plan_back | 20 | 0.2933 | 0.2800 | -0.0133 | [-0.0833, 0.0500] | 0.790039 |
| reachability | plan_front -> plan_scatter | 20 | 0.2933 | 0.2767 | -0.0167 | [-0.0600, 0.0267] | 0.577148 |
| executability | plan_front -> canonical | 20 | 0.4767 | 0.4300 | -0.0467 | [-0.1167, 0.0233] | 0.263855 |
| executability | plan_front -> disp_1 | 20 | 0.4767 | 0.4567 | -0.0200 | [-0.0833, 0.0467] | 0.628540 |
| executability | plan_front -> disp_2 | 20 | 0.4767 | 0.4500 | -0.0267 | [-0.0800, 0.0333] | 0.441772 |
| executability | plan_front -> disp_3 | 20 | 0.4767 | 0.4233 | -0.0533 | [-0.1300, 0.0033] | 0.153076 |
| executability | plan_front -> plan_back | 20 | 0.4767 | 0.4500 | -0.0267 | [-0.0900, 0.0400] | 0.496078 |
| executability | plan_front -> plan_scatter | 20 | 0.4767 | 0.5033 | 0.0267 | [-0.0367, 0.0933] | 0.511597 |
| non_executable_failure | plan_front -> canonical | 20 | 0.5233 | 0.5700 | 0.0467 | [-0.0233, 0.1167] | 0.263855 |
| non_executable_failure | plan_front -> disp_1 | 20 | 0.5233 | 0.5433 | 0.0200 | [-0.0467, 0.0833] | 0.628540 |
| non_executable_failure | plan_front -> disp_2 | 20 | 0.5233 | 0.5500 | 0.0267 | [-0.0333, 0.0800] | 0.441772 |
| non_executable_failure | plan_front -> disp_3 | 20 | 0.5233 | 0.5767 | 0.0533 | [-0.0033, 0.1300] | 0.153076 |
| non_executable_failure | plan_front -> plan_back | 20 | 0.5233 | 0.5500 | 0.0267 | [-0.0400, 0.0900] | 0.496078 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.5233 | 0.4967 | -0.0267 | [-0.0933, 0.0367] | 0.511597 |
| conditional_reachability | plan_front -> canonical | 20 | 0.3696 | 0.4954 | 0.1258 | [0.0286, 0.2295] | 0.027344 |
| conditional_reachability | plan_front -> disp_1 | 19 | 0.3890 | 0.4041 | 0.0151 | [-0.0676, 0.0917] | 0.726562 |
| conditional_reachability | plan_front -> disp_2 | 20 | 0.3696 | 0.3783 | 0.0087 | [-0.0817, 0.1045] | 0.859375 |
| conditional_reachability | plan_front -> disp_3 | 19 | 0.3890 | 0.3141 | -0.0749 | [-0.1430, -0.0205] | 0.015625 |
| conditional_reachability | plan_front -> plan_back | 20 | 0.3696 | 0.4122 | 0.0426 | [-0.0600, 0.1572] | 0.466797 |
| conditional_reachability | plan_front -> plan_scatter | 19 | 0.3890 | 0.3806 | -0.0084 | [-0.1107, 0.0921] | 0.875000 |
| plan_length | plan_front -> canonical | 12 | 18.2611 | 19.0249 | 0.7638 | [-0.4185, 2.0397] | 0.298828 |
| plan_length | plan_front -> disp_1 | 11 | 17.1939 | 18.2100 | 1.0160 | [0.0146, 2.1865] | 0.171875 |
| plan_length | plan_front -> disp_2 | 11 | 17.1939 | 17.3084 | 0.1145 | [-0.9273, 1.3707] | 0.876953 |
| plan_length | plan_front -> disp_3 | 10 | 15.9133 | 15.8611 | -0.0522 | [-0.7056, 0.5589] | 0.750000 |
| plan_length | plan_front -> plan_back | 9 | 13.2370 | 14.6794 | 1.4423 | [0.1682, 3.1535] | 0.109375 |
| plan_length | plan_front -> plan_scatter | 9 | 13.2370 | 13.4685 | 0.2315 | [-0.3056, 1.0167] | 0.734375 |
| optimality_ratio | plan_front -> canonical | 12 | 1.0753 | 1.1327 | 0.0574 | [-0.0135, 0.1396] | 0.212891 |
| optimality_ratio | plan_front -> disp_1 | 11 | 1.0720 | 1.1196 | 0.0476 | [-0.0026, 0.1078] | 0.171875 |
| optimality_ratio | plan_front -> disp_2 | 11 | 1.0821 | 1.0936 | 0.0115 | [-0.0455, 0.0799] | 0.742188 |
| optimality_ratio | plan_front -> disp_3 | 10 | 1.0792 | 1.0743 | -0.0049 | [-0.0420, 0.0286] | 0.718750 |
| optimality_ratio | plan_front -> plan_back | 9 | 1.0721 | 1.1678 | 0.0957 | [0.0138, 0.2057] | 0.109375 |
| optimality_ratio | plan_front -> plan_scatter | 9 | 1.0721 | 1.0814 | 0.0093 | [-0.0233, 0.0528] | 0.796875 |
| first_failure_step | plan_front -> canonical | 16 | 9.2427 | 10.1041 | 0.8614 | [-0.5726, 2.4183] | 0.293549 |
| first_failure_step | plan_front -> disp_1 | 15 | 9.3589 | 9.2269 | -0.1320 | [-1.3577, 1.0319] | 0.835938 |
| first_failure_step | plan_front -> disp_2 | 16 | 9.2427 | 9.7946 | 0.5519 | [-1.1963, 2.2441] | 0.551392 |
| first_failure_step | plan_front -> disp_3 | 16 | 9.2427 | 7.5760 | -1.6667 | [-3.3002, -0.0710] | 0.071381 |
| first_failure_step | plan_front -> plan_back | 16 | 9.2427 | 7.5656 | -1.6771 | [-3.7985, 0.5901] | 0.165955 |
| first_failure_step | plan_front -> plan_scatter | 16 | 9.2427 | 7.5774 | -1.6653 | [-3.1365, -0.0325] | 0.062469 |
| prompt_tokens | plan_front -> canonical | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> disp_1 | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> disp_2 | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> disp_3 | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> plan_back | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 8743.9000 | 8743.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| completion_tokens | plan_front -> canonical | 20 | 7580.8400 | 8628.5433 | 1047.7033 | [627.9895, 1464.8900] | 0.000160 |
| completion_tokens | plan_front -> disp_1 | 20 | 7580.8400 | 8109.4767 | 528.6367 | [16.1832, 1070.2379] | 0.072256 |
| completion_tokens | plan_front -> disp_2 | 20 | 7580.8400 | 8098.6533 | 517.8133 | [-283.9892, 1274.1324] | 0.221584 |
| completion_tokens | plan_front -> disp_3 | 20 | 7580.8400 | 7817.2400 | 236.4000 | [-226.8642, 676.8410] | 0.332283 |
| completion_tokens | plan_front -> plan_back | 20 | 7580.8400 | 7921.9633 | 341.1233 | [-404.7605, 1114.3821] | 0.401356 |
| completion_tokens | plan_front -> plan_scatter | 20 | 7580.8400 | 7939.9867 | 359.1467 | [-273.9457, 996.1320] | 0.293289 |
| reasoning_completion_tokens | plan_front -> canonical | 20 | 7580.8400 | 8628.5433 | 1047.7033 | [627.9895, 1464.8900] | 0.000160 |
| reasoning_completion_tokens | plan_front -> disp_1 | 20 | 7580.8400 | 8109.4767 | 528.6367 | [16.1832, 1070.2379] | 0.072256 |
| reasoning_completion_tokens | plan_front -> disp_2 | 20 | 7580.8400 | 8098.6533 | 517.8133 | [-283.9892, 1274.1324] | 0.221584 |
| reasoning_completion_tokens | plan_front -> disp_3 | 20 | 7580.8400 | 7817.2400 | 236.4000 | [-226.8642, 676.8410] | 0.332283 |
| reasoning_completion_tokens | plan_front -> plan_back | 20 | 7580.8400 | 7921.9633 | 341.1233 | [-404.7605, 1114.3821] | 0.401356 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 7580.8400 | 7939.9867 | 359.1467 | [-273.9457, 996.1320] | 0.293289 |
| raw_completion_tokens | plan_front -> canonical | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | plan_front -> disp_1 | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | plan_front -> disp_2 | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | plan_front -> disp_3 | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | plan_front -> plan_back | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 0.0000 | 0.0000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| total_tokens | plan_front -> canonical | 20 | 16324.7400 | 17372.4433 | 1047.7033 | [627.9895, 1464.8900] | 0.000160 |
| total_tokens | plan_front -> disp_1 | 20 | 16324.7400 | 16853.3767 | 528.6367 | [16.1832, 1070.2379] | 0.072256 |
| total_tokens | plan_front -> disp_2 | 20 | 16324.7400 | 16842.5533 | 517.8133 | [-283.9893, 1274.1324] | 0.221584 |
| total_tokens | plan_front -> disp_3 | 20 | 16324.7400 | 16561.1400 | 236.4000 | [-226.8642, 676.8410] | 0.332283 |
| total_tokens | plan_front -> plan_back | 20 | 16324.7400 | 16665.8633 | 341.1233 | [-404.7605, 1114.3821] | 0.401356 |
| total_tokens | plan_front -> plan_scatter | 20 | 16324.7400 | 16683.8867 | 359.1467 | [-273.9457, 996.1320] | 0.293289 |
| duration_sec | plan_front -> canonical | 20 | 151.7043 | 175.9562 | 24.2519 | [8.1901, 41.3798] | 0.011168 |
| duration_sec | plan_front -> disp_1 | 20 | 151.7043 | 168.9305 | 17.2263 | [1.5699, 34.3273] | 0.051737 |
| duration_sec | plan_front -> disp_2 | 20 | 151.7043 | 163.8735 | 12.1692 | [-5.1474, 29.7237] | 0.203339 |
| duration_sec | plan_front -> disp_3 | 20 | 151.7043 | 160.8507 | 9.1465 | [-1.7674, 20.7144] | 0.134333 |
| duration_sec | plan_front -> plan_back | 20 | 151.7043 | 213.0387 | 61.3344 | [27.4357, 106.2729] | 0.000946 |
| duration_sec | plan_front -> plan_scatter | 20 | 151.7043 | 161.0220 | 9.3178 | [-5.2617, 23.1635] | 0.229212 |
