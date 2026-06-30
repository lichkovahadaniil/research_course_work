# Statistical Tests: nemotron-3-super

Primary baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_back`, `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 300 | 0.1667 | 0.1933 | 15 | 7 | 0.0267 | 2.1429 | 0.133801 | 0.535202 |
| reachability | canonical -> disp_2 | 300 | 0.1667 | 0.1900 | 17 | 10 | 0.0233 | 1.7000 | 0.247789 | 0.743366 |
| reachability | canonical -> disp_3 | 300 | 0.1667 | 0.1533 | 12 | 16 | -0.0133 | 0.7500 | 0.571588 | 0.783057 |
| reachability | canonical -> plan_front | 300 | 0.1667 | 0.2233 | 24 | 7 | 0.0567 | 3.4286 | 0.003327 | 0.019961 |
| reachability | canonical -> plan_back | 300 | 0.1667 | 0.1867 | 20 | 14 | 0.0200 | 1.4286 | 0.391528 | 0.783057 |
| reachability | canonical -> plan_scatter | 300 | 0.1667 | 0.2100 | 18 | 5 | 0.0433 | 3.6000 | 0.010622 | 0.053110 |
| executability | canonical -> disp_1 | 300 | 0.1800 | 0.2133 | 20 | 10 | 0.0333 | 2.0000 | 0.098737 | 0.394949 |
| executability | canonical -> disp_2 | 300 | 0.1800 | 0.2000 | 18 | 12 | 0.0200 | 1.5000 | 0.361595 | 0.598773 |
| executability | canonical -> disp_3 | 300 | 0.1800 | 0.1567 | 11 | 18 | -0.0233 | 0.6111 | 0.264931 | 0.598773 |
| executability | canonical -> plan_front | 300 | 0.1800 | 0.2267 | 23 | 9 | 0.0467 | 2.5556 | 0.020062 | 0.120370 |
| executability | canonical -> plan_back | 300 | 0.1800 | 0.2100 | 24 | 15 | 0.0300 | 1.6000 | 0.199591 | 0.598773 |
| executability | canonical -> plan_scatter | 300 | 0.1800 | 0.2200 | 19 | 7 | 0.0400 | 2.7143 | 0.028959 | 0.144796 |
| non_executable_failure | canonical -> disp_1 | 300 | 0.8200 | 0.7867 | 10 | 20 | -0.0333 | 0.5000 | 0.098737 | 0.394949 |
| non_executable_failure | canonical -> disp_2 | 300 | 0.8200 | 0.8000 | 12 | 18 | -0.0200 | 0.6667 | 0.361595 | 0.598773 |
| non_executable_failure | canonical -> disp_3 | 300 | 0.8200 | 0.8433 | 18 | 11 | 0.0233 | 1.6364 | 0.264931 | 0.598773 |
| non_executable_failure | canonical -> plan_front | 300 | 0.8200 | 0.7733 | 9 | 23 | -0.0467 | 0.3913 | 0.020062 | 0.120370 |
| non_executable_failure | canonical -> plan_back | 300 | 0.8200 | 0.7900 | 15 | 24 | -0.0300 | 0.6250 | 0.199591 | 0.598773 |
| non_executable_failure | canonical -> plan_scatter | 300 | 0.8200 | 0.7800 | 7 | 19 | -0.0400 | 0.3684 | 0.028959 | 0.144796 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 54 | 64 | 0.9259 | 0.9062 | 50/4 | 58/6 | -0.0197 | 0.7733 | 0.752577 | 1.000000 |
| conditional_reachability | canonical -> disp_2 | 54 | 60 | 0.9259 | 0.9500 | 50/4 | 57/3 | 0.0241 | 1.5200 | 0.706046 | 1.000000 |
| conditional_reachability | canonical -> disp_3 | 54 | 47 | 0.9259 | 0.9787 | 50/4 | 46/1 | 0.0528 | 3.6800 | 0.368545 | 1.000000 |
| conditional_reachability | canonical -> plan_front | 54 | 68 | 0.9259 | 0.9853 | 50/4 | 67/1 | 0.0594 | 5.3600 | 0.169290 | 1.000000 |
| conditional_reachability | canonical -> plan_back | 54 | 63 | 0.9259 | 0.8889 | 50/4 | 56/7 | -0.0370 | 0.6400 | 0.543110 | 1.000000 |
| conditional_reachability | canonical -> plan_scatter | 54 | 66 | 0.9259 | 0.9545 | 50/4 | 63/3 | 0.0286 | 1.6800 | 0.699488 | 1.000000 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 43 | 9.5581 | 8.8372 | -0.7209 | -0.0754 | -0.1807 | 0.242750 | 0.437500 | 1.000000 |
| plan_length | canonical -> disp_2 | 40 | 8.0250 | 7.9750 | -0.0500 | -0.0062 | -0.1581 | 0.323475 | 1.000000 | 1.000000 |
| plan_length | canonical -> disp_3 | 34 | 8.9118 | 8.2353 | -0.6765 | -0.0759 | -0.1623 | 0.350904 | 0.750000 | 1.000000 |
| plan_length | canonical -> plan_front | 43 | 9.1163 | 8.5116 | -0.6047 | -0.0663 | -0.1650 | 0.285547 | 0.500000 | 1.000000 |
| plan_length | canonical -> plan_back | 36 | 9.7500 | 8.7222 | -1.0278 | -0.1054 | -0.2320 | 0.172729 | 0.250000 | 1.000000 |
| plan_length | canonical -> plan_scatter | 45 | 9.4000 | 8.6000 | -0.8000 | -0.0851 | -0.2007 | 0.185121 | 0.375000 | 1.000000 |
| optimality_ratio | canonical -> disp_1 | 43 | 1.0605 | 1.0149 | -0.0455 | -0.0429 | -0.1675 | 0.278285 | 0.406250 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 40 | 1.0050 | 1.0000 | -0.0050 | -0.0050 | -0.1581 | 0.323475 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 34 | 1.0529 | 1.0088 | -0.0441 | -0.0419 | -0.1565 | 0.368224 | 0.750000 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 43 | 1.0419 | 1.0000 | -0.0419 | -0.0402 | -0.1707 | 0.269247 | 0.500000 | 1.000000 |
| optimality_ratio | canonical -> plan_back | 36 | 1.0722 | 1.0046 | -0.0676 | -0.0630 | -0.2270 | 0.181905 | 0.250000 | 1.000000 |
| optimality_ratio | canonical -> plan_scatter | 45 | 1.0578 | 1.0044 | -0.0533 | -0.0504 | -0.1993 | 0.188187 | 0.375000 | 1.000000 |
| first_failure_step | canonical -> disp_1 | 2 | 6.0000 | 6.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| first_failure_step | canonical -> disp_2 | 3 | 9.3333 | 23.0000 | 13.6667 | 1.4643 | 0.5768 | 0.422993 | 0.750000 | 1.000000 |
| first_failure_step | canonical -> disp_3 | 4 | 8.2500 | 8.2500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| first_failure_step | canonical -> plan_front | 1 | 8.0000 | 8.0000 | 0.0000 | 0.0000 | NA | NA | 1.000000 | 1.000000 |
| first_failure_step | canonical -> plan_back | 1 | 8.0000 | 4.0000 | -4.0000 | -0.5000 | NA | NA | 1.000000 | 1.000000 |
| first_failure_step | canonical -> plan_scatter | 1 | 4.0000 | 7.0000 | 3.0000 | 0.7500 | NA | NA | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_1 | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_back | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> disp_1 | 300 | 12949.6333 | 12643.2967 | -306.3367 | -0.0237 | -0.0687 | 0.235082 | 0.234840 | 0.704520 |
| completion_tokens | canonical -> disp_2 | 300 | 12949.6333 | 13055.8833 | 106.2500 | 0.0082 | 0.0247 | 0.668840 | 0.667720 | 0.704520 |
| completion_tokens | canonical -> disp_3 | 300 | 12949.6333 | 13816.0567 | 866.4233 | 0.0669 | 0.2135 | 0.000259 | 0.000260 | 0.001560 |
| completion_tokens | canonical -> plan_front | 300 | 12949.6333 | 12654.3100 | -295.3233 | -0.0228 | -0.0663 | 0.252092 | 0.251830 | 0.704520 |
| completion_tokens | canonical -> plan_back | 300 | 12949.6333 | 11984.0100 | -965.6233 | -0.0746 | -0.1789 | 0.002131 | 0.001970 | 0.009850 |
| completion_tokens | canonical -> plan_scatter | 300 | 12949.6333 | 12517.8433 | -431.7900 | -0.0333 | -0.0991 | 0.087000 | 0.087220 | 0.348880 |
| reasoning_completion_tokens | canonical -> disp_1 | 300 | 4866.8600 | 4123.6167 | -743.2433 | -0.1527 | -0.1024 | 0.077082 | 0.077720 | 0.159280 |
| reasoning_completion_tokens | canonical -> disp_2 | 300 | 4866.8600 | 4044.6833 | -822.1767 | -0.1689 | -0.1121 | 0.053147 | 0.052970 | 0.159280 |
| reasoning_completion_tokens | canonical -> disp_3 | 300 | 4866.8600 | 2838.7767 | -2028.0833 | -0.4167 | -0.2971 | 0.000000 | 0.000000 | 0.000000 |
| reasoning_completion_tokens | canonical -> plan_front | 300 | 4866.8600 | 4237.3533 | -629.5067 | -0.1293 | -0.0881 | 0.127999 | 0.127770 | 0.159280 |
| reasoning_completion_tokens | canonical -> plan_back | 300 | 4866.8600 | 3953.6967 | -913.1633 | -0.1876 | -0.1356 | 0.019499 | 0.019200 | 0.096000 |
| reasoning_completion_tokens | canonical -> plan_scatter | 300 | 4866.8600 | 4052.7767 | -814.0833 | -0.1673 | -0.1193 | 0.039676 | 0.039820 | 0.159280 |
| raw_completion_tokens | canonical -> disp_1 | 300 | 8082.7733 | 8519.6800 | 436.9067 | 0.0541 | 0.0436 | 0.450611 | 0.507340 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 300 | 8082.7733 | 9011.2000 | 928.4267 | 0.1149 | 0.0934 | 0.106736 | 0.129330 | 0.646650 |
| raw_completion_tokens | canonical -> disp_3 | 300 | 8082.7733 | 10977.2800 | 2894.5067 | 0.3581 | 0.3092 | 0.000000 | 0.000000 | 0.000000 |
| raw_completion_tokens | canonical -> plan_front | 300 | 8082.7733 | 8416.9567 | 334.1833 | 0.0413 | 0.0340 | 0.556890 | 0.564420 | 1.000000 |
| raw_completion_tokens | canonical -> plan_back | 300 | 8082.7733 | 8030.3133 | -52.4600 | -0.0065 | -0.0055 | 0.924783 | 1.000000 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 300 | 8082.7733 | 8465.0667 | 382.2933 | 0.0473 | 0.0406 | 0.482644 | 0.547270 | 1.000000 |
| total_tokens | canonical -> disp_1 | 300 | 22764.6833 | 22458.3467 | -306.3367 | -0.0135 | -0.0687 | 0.235082 | 0.234840 | 0.704520 |
| total_tokens | canonical -> disp_2 | 300 | 22764.6833 | 22870.9333 | 106.2500 | 0.0047 | 0.0247 | 0.668840 | 0.667720 | 0.704520 |
| total_tokens | canonical -> disp_3 | 300 | 22764.6833 | 23631.1067 | 866.4233 | 0.0381 | 0.2135 | 0.000259 | 0.000260 | 0.001560 |
| total_tokens | canonical -> plan_front | 300 | 22764.6833 | 22469.3600 | -295.3233 | -0.0130 | -0.0663 | 0.252092 | 0.251830 | 0.704520 |
| total_tokens | canonical -> plan_back | 300 | 22764.6833 | 21799.0600 | -965.6233 | -0.0424 | -0.1789 | 0.002131 | 0.001970 | 0.009850 |
| total_tokens | canonical -> plan_scatter | 300 | 22764.6833 | 22332.8933 | -431.7900 | -0.0190 | -0.0991 | 0.087000 | 0.087220 | 0.348880 |
| duration_sec | canonical -> disp_1 | 300 | 92.5973 | 89.4913 | -3.1060 | -0.0335 | -0.0624 | 0.280797 | 0.281150 | 0.765480 |
| duration_sec | canonical -> disp_2 | 300 | 92.5973 | 89.0343 | -3.5630 | -0.0385 | -0.0754 | 0.192304 | 0.191370 | 0.765480 |
| duration_sec | canonical -> disp_3 | 300 | 92.5973 | 95.6245 | 3.0272 | 0.0327 | 0.0665 | 0.250106 | 0.249990 | 0.765480 |
| duration_sec | canonical -> plan_front | 300 | 92.5973 | 90.3637 | -2.2336 | -0.0241 | -0.0445 | 0.441719 | 0.441550 | 0.765480 |
| duration_sec | canonical -> plan_back | 300 | 92.5973 | 215.4544 | 122.8571 | 1.3268 | 0.8993 | 0.000000 | 0.000000 | 0.000000 |
| duration_sec | canonical -> plan_scatter | 300 | 92.5973 | 86.2852 | -6.3121 | -0.0682 | -0.1324 | 0.022571 | 0.022370 | 0.111850 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 20 | 0.1667 | 0.1933 | 0.0267 | [-0.0200, 0.0733] | 0.375000 |
| reachability | canonical -> disp_2 | 20 | 0.1667 | 0.1900 | 0.0233 | [0.0033, 0.0500] | 0.125000 |
| reachability | canonical -> disp_3 | 20 | 0.1667 | 0.1533 | -0.0133 | [-0.0500, 0.0100] | 1.000000 |
| reachability | canonical -> plan_front | 20 | 0.1667 | 0.2233 | 0.0567 | [0.0133, 0.1233] | 0.031250 |
| reachability | canonical -> plan_back | 20 | 0.1667 | 0.1867 | 0.0200 | [-0.0533, 0.0933] | 0.578125 |
| reachability | canonical -> plan_scatter | 20 | 0.1667 | 0.2100 | 0.0433 | [0.0100, 0.0867] | 0.062500 |
| executability | canonical -> disp_1 | 20 | 0.1800 | 0.2133 | 0.0333 | [-0.0133, 0.0767] | 0.226562 |
| executability | canonical -> disp_2 | 20 | 0.1800 | 0.2000 | 0.0200 | [-0.0100, 0.0533] | 0.324219 |
| executability | canonical -> disp_3 | 20 | 0.1800 | 0.1567 | -0.0233 | [-0.0700, 0.0067] | 0.500000 |
| executability | canonical -> plan_front | 20 | 0.1800 | 0.2267 | 0.0467 | [0.0033, 0.1100] | 0.093750 |
| executability | canonical -> plan_back | 20 | 0.1800 | 0.2100 | 0.0300 | [-0.0500, 0.1033] | 0.512695 |
| executability | canonical -> plan_scatter | 20 | 0.1800 | 0.2200 | 0.0400 | [0.0067, 0.0767] | 0.058594 |
| non_executable_failure | canonical -> disp_1 | 20 | 0.8200 | 0.7867 | -0.0333 | [-0.0767, 0.0133] | 0.226562 |
| non_executable_failure | canonical -> disp_2 | 20 | 0.8200 | 0.8000 | -0.0200 | [-0.0533, 0.0100] | 0.324219 |
| non_executable_failure | canonical -> disp_3 | 20 | 0.8200 | 0.8433 | 0.0233 | [-0.0067, 0.0700] | 0.500000 |
| non_executable_failure | canonical -> plan_front | 20 | 0.8200 | 0.7733 | -0.0467 | [-0.1100, -0.0033] | 0.093750 |
| non_executable_failure | canonical -> plan_back | 20 | 0.8200 | 0.7900 | -0.0300 | [-0.1033, 0.0500] | 0.512695 |
| non_executable_failure | canonical -> plan_scatter | 20 | 0.8200 | 0.7800 | -0.0400 | [-0.0767, -0.0067] | 0.058594 |
| conditional_reachability | canonical -> disp_1 | 6 | 0.7833 | 0.8056 | 0.0222 | [-0.0333, 0.1000] | 1.000000 |
| conditional_reachability | canonical -> disp_2 | 5 | 0.9400 | 1.0000 | 0.0600 | [0.0000, 0.1400] | 0.500000 |
| conditional_reachability | canonical -> disp_3 | 5 | 0.9400 | 1.0000 | 0.0600 | [0.0000, 0.1400] | 0.500000 |
| conditional_reachability | canonical -> plan_front | 6 | 0.7833 | 0.8333 | 0.0500 | [0.0000, 0.1167] | 0.500000 |
| conditional_reachability | canonical -> plan_back | 5 | 0.9400 | 0.9690 | 0.0290 | [-0.0619, 0.1257] | 0.625000 |
| conditional_reachability | canonical -> plan_scatter | 5 | 0.9400 | 1.0000 | 0.0600 | [0.0000, 0.1400] | 0.500000 |
| plan_length | canonical -> disp_1 | 5 | 11.4333 | 9.7350 | -1.6983 | [-5.1333, 0.1051] | 0.750000 |
| plan_length | canonical -> disp_2 | 5 | 11.4333 | 9.6500 | -1.7833 | [-5.2833, 0.0000] | 0.500000 |
| plan_length | canonical -> disp_3 | 5 | 11.4333 | 9.6500 | -1.7833 | [-5.4000, 0.0500] | 1.000000 |
| plan_length | canonical -> plan_front | 5 | 11.4333 | 9.6462 | -1.7872 | [-5.2949, 0.0000] | 0.500000 |
| plan_length | canonical -> plan_back | 5 | 11.4333 | 9.6669 | -1.7664 | [-5.3000, 0.0310] | 0.750000 |
| plan_length | canonical -> plan_scatter | 5 | 11.4333 | 9.6508 | -1.7825 | [-5.3381, 0.0000] | 0.500000 |
| optimality_ratio | canonical -> disp_1 | 5 | 1.1233 | 1.0117 | -0.1116 | [-0.3422, 0.0140] | 0.750000 |
| optimality_ratio | canonical -> disp_2 | 5 | 1.1233 | 1.0033 | -0.1200 | [-0.3533, 0.0000] | 0.500000 |
| optimality_ratio | canonical -> disp_3 | 5 | 1.1233 | 1.0050 | -0.1183 | [-0.3600, 0.0050] | 1.000000 |
| optimality_ratio | canonical -> plan_front | 5 | 1.1233 | 1.0031 | -0.1203 | [-0.3541, 0.0000] | 0.500000 |
| optimality_ratio | canonical -> plan_back | 5 | 1.1233 | 1.0066 | -0.1167 | [-0.3533, 0.0062] | 0.750000 |
| optimality_ratio | canonical -> plan_scatter | 5 | 1.1233 | 1.0043 | -0.1190 | [-0.3560, 0.0000] | 0.500000 |
| first_failure_step | canonical -> disp_1 | 5 | 8.5400 | 4.7667 | -3.7733 | [-7.0000, -0.9133] | 0.125000 |
| first_failure_step | canonical -> disp_2 | 4 | 9.6750 | 14.5625 | 4.8875 | [-4.7500, 20.6250] | 0.875000 |
| first_failure_step | canonical -> disp_3 | 4 | 8.4250 | 6.7500 | -1.6750 | [-4.8750, 0.2500] | 0.500000 |
| first_failure_step | canonical -> plan_front | 5 | 6.6400 | 7.4400 | 0.8000 | [-0.8000, 3.0000] | 0.875000 |
| first_failure_step | canonical -> plan_back | 5 | 6.6400 | 5.9714 | -0.6686 | [-1.5371, 0.2000] | 0.375000 |
| first_failure_step | canonical -> plan_scatter | 3 | 7.7333 | 6.5000 | -1.2333 | [-5.0000, 1.5000] | 0.750000 |
| prompt_tokens | canonical -> disp_1 | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> plan_front | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> plan_back | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| completion_tokens | canonical -> disp_1 | 20 | 12949.6333 | 12643.2967 | -306.3367 | [-979.3914, 339.9676] | 0.384544 |
| completion_tokens | canonical -> disp_2 | 20 | 12949.6333 | 13055.8833 | 106.2500 | [-362.0068, 575.0348] | 0.664413 |
| completion_tokens | canonical -> disp_3 | 20 | 12949.6333 | 13816.0567 | 866.4233 | [425.3743, 1303.3521] | 0.001549 |
| completion_tokens | canonical -> plan_front | 20 | 12949.6333 | 12654.3100 | -295.3233 | [-1102.3213, 413.0793] | 0.479706 |
| completion_tokens | canonical -> plan_back | 20 | 12949.6333 | 11984.0100 | -965.6233 | [-1994.1210, 27.8887] | 0.078838 |
| completion_tokens | canonical -> plan_scatter | 20 | 12949.6333 | 12517.8433 | -431.7900 | [-1211.1104, 232.6603] | 0.299881 |
| reasoning_completion_tokens | canonical -> disp_1 | 20 | 4866.8600 | 4123.6167 | -743.2433 | [-1667.4366, 192.6298] | 0.133553 |
| reasoning_completion_tokens | canonical -> disp_2 | 20 | 4866.8600 | 4044.6833 | -822.1767 | [-1561.3005, -155.4728] | 0.034058 |
| reasoning_completion_tokens | canonical -> disp_3 | 20 | 4866.8600 | 2838.7767 | -2028.0833 | [-2870.8360, -1212.9561] | 0.000122 |
| reasoning_completion_tokens | canonical -> plan_front | 20 | 4866.8600 | 4237.3533 | -629.5067 | [-1521.9662, 319.1461] | 0.196404 |
| reasoning_completion_tokens | canonical -> plan_back | 20 | 4866.8600 | 3953.6967 | -913.1633 | [-1777.6783, -160.2552] | 0.040283 |
| reasoning_completion_tokens | canonical -> plan_scatter | 20 | 4866.8600 | 4052.7767 | -814.0833 | [-1634.0164, 26.6415] | 0.077169 |
| raw_completion_tokens | canonical -> disp_1 | 20 | 8082.7733 | 8519.6800 | 436.9067 | [-928.4267, 1802.2400] | 0.595337 |
| raw_completion_tokens | canonical -> disp_2 | 20 | 8082.7733 | 9011.2000 | 928.4267 | [-109.2267, 2020.6933] | 0.128662 |
| raw_completion_tokens | canonical -> disp_3 | 20 | 8082.7733 | 10977.2800 | 2894.5067 | [1802.2400, 4041.3867] | 0.000122 |
| raw_completion_tokens | canonical -> plan_front | 20 | 8082.7733 | 8416.9567 | 334.1833 | [-1297.7133, 1802.2400] | 0.695679 |
| raw_completion_tokens | canonical -> plan_back | 20 | 8082.7733 | 8030.3133 | -52.4600 | [-1634.0933, 1585.9400] | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 20 | 8082.7733 | 8465.0667 | 382.2933 | [-983.0400, 1693.0133] | 0.651161 |
| total_tokens | canonical -> disp_1 | 20 | 22764.6833 | 22458.3467 | -306.3367 | [-979.3914, 339.9676] | 0.384544 |
| total_tokens | canonical -> disp_2 | 20 | 22764.6833 | 22870.9333 | 106.2500 | [-362.0068, 575.0348] | 0.664413 |
| total_tokens | canonical -> disp_3 | 20 | 22764.6833 | 23631.1067 | 866.4233 | [425.3743, 1303.3521] | 0.001549 |
| total_tokens | canonical -> plan_front | 20 | 22764.6833 | 22469.3600 | -295.3233 | [-1102.3213, 413.0793] | 0.479706 |
| total_tokens | canonical -> plan_back | 20 | 22764.6833 | 21799.0600 | -965.6233 | [-1994.1210, 27.8887] | 0.078838 |
| total_tokens | canonical -> plan_scatter | 20 | 22764.6833 | 22332.8933 | -431.7900 | [-1211.1104, 232.6603] | 0.299881 |
| duration_sec | canonical -> disp_1 | 20 | 92.5973 | 89.4913 | -3.1060 | [-9.7318, 3.1082] | 0.366291 |
| duration_sec | canonical -> disp_2 | 20 | 92.5973 | 89.0343 | -3.5630 | [-10.1335, 3.6473] | 0.328314 |
| duration_sec | canonical -> disp_3 | 20 | 92.5973 | 95.6245 | 3.0272 | [-2.2185, 8.2689] | 0.281103 |
| duration_sec | canonical -> plan_front | 20 | 92.5973 | 90.3637 | -2.2336 | [-11.1567, 5.7982] | 0.624119 |
| duration_sec | canonical -> plan_back | 20 | 92.5973 | 215.4544 | 122.8571 | [99.0635, 153.6856] | 0.000002 |
| duration_sec | canonical -> plan_scatter | 20 | 92.5973 | 86.2852 | -6.3121 | [-14.8834, 1.5527] | 0.157701 |

## Disp 3 vs All Orders

`reachability` is the primary metric. Each non-`disp_3` order is used as the baseline and `disp_3` is the compared order; negative mean differences mean lower reachability for `disp_3`.

Primary test: problem-level paired sign-flip permutation test with bootstrap 95% CI over problems. Holm adjustment is applied across the six problem-level comparisons within this model.

| comparison | n problems | baseline mean | disp_3 mean | mean diff | 95% CI | p perm | p perm Holm | empirical best baseline |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| canonical -> disp_3 | 20 | 0.1667 | 0.1533 | -0.0133 | [-0.0500, 0.0100] | 1.000000 | 1.000000 |  |
| disp_1 -> disp_3 | 20 | 0.1933 | 0.1533 | -0.0400 | [-0.0767, -0.0133] | 0.015625 | 0.093750 |  |
| disp_2 -> disp_3 | 20 | 0.1900 | 0.1533 | -0.0367 | [-0.0767, -0.0067] | 0.062500 | 0.250000 |  |
| plan_front -> disp_3 | 20 | 0.2233 | 0.1533 | -0.0700 | [-0.1467, -0.0133] | 0.031250 | 0.156250 | yes |
| plan_back -> disp_3 | 20 | 0.1867 | 0.1533 | -0.0333 | [-0.1000, 0.0133] | 0.406250 | 0.812500 |  |
| plan_scatter -> disp_3 | 20 | 0.2100 | 0.1533 | -0.0567 | [-0.1233, -0.0067] | 0.062500 | 0.250000 |  |

Additional analysis: run-level exact McNemar tests on paired `(problem, run)` reachability outcomes.

| comparison | n | baseline | disp_3 | b | c | risk diff | matched OR | p | p Holm |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| canonical -> disp_3 | 300 | 0.1667 | 0.1533 | 12 | 16 | -0.0133 | 0.7500 | 0.571588 | 0.571588 |
| disp_1 -> disp_3 | 300 | 0.1933 | 0.1533 | 5 | 17 | -0.0400 | 0.2941 | 0.016901 | 0.050903 |
| disp_2 -> disp_3 | 300 | 0.1900 | 0.1533 | 3 | 14 | -0.0367 | 0.2143 | 0.012726 | 0.050903 |
| plan_front -> disp_3 | 300 | 0.2233 | 0.1533 | 4 | 25 | -0.0700 | 0.1600 | 0.000104 | 0.000622 |
| plan_back -> disp_3 | 300 | 0.1867 | 0.1533 | 10 | 20 | -0.0333 | 0.5000 | 0.098737 | 0.197474 |
| plan_scatter -> disp_3 | 300 | 0.2100 | 0.1533 | 4 | 21 | -0.0567 | 0.1905 | 0.000911 | 0.004553 |
