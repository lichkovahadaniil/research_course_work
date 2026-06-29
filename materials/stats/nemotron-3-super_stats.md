# Statistical Tests: nemotron-3-super

Primary baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_scatter`.
`plan_front` baseline comparisons: `plan_front` vs `canonical`, `plan_front` vs `disp_1`, `plan_front` vs `disp_2`, `plan_front` vs `disp_3`, `plan_front` vs `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 300 | 0.1667 | 0.1933 | 15 | 7 | 0.0267 | 2.1429 | 0.133801 | 0.401402 |
| reachability | canonical -> disp_2 | 300 | 0.1667 | 0.1900 | 17 | 10 | 0.0233 | 1.7000 | 0.247789 | 0.495577 |
| reachability | canonical -> disp_3 | 300 | 0.1667 | 0.1533 | 12 | 16 | -0.0133 | 0.7500 | 0.571588 | 0.571588 |
| reachability | canonical -> plan_front | 300 | 0.1667 | 0.2233 | 24 | 7 | 0.0567 | 3.4286 | 0.003327 | 0.016634 |
| reachability | canonical -> plan_scatter | 300 | 0.1667 | 0.2100 | 18 | 5 | 0.0433 | 3.6000 | 0.010622 | 0.042488 |
| reachability | plan_front -> canonical | 300 | 0.2233 | 0.1667 | 7 | 24 | -0.0567 | 0.2917 | 0.003327 | 0.013308 |
| reachability | plan_front -> disp_1 | 300 | 0.2233 | 0.1933 | 7 | 16 | -0.0300 | 0.4375 | 0.093140 | 0.186279 |
| reachability | plan_front -> disp_2 | 300 | 0.2233 | 0.1900 | 6 | 16 | -0.0333 | 0.3750 | 0.052479 | 0.157436 |
| reachability | plan_front -> disp_3 | 300 | 0.2233 | 0.1533 | 4 | 25 | -0.0700 | 0.1600 | 0.000104 | 0.000519 |
| reachability | plan_front -> plan_scatter | 300 | 0.2233 | 0.2100 | 8 | 12 | -0.0133 | 0.6667 | 0.503445 | 0.503445 |
| executability | canonical -> disp_1 | 300 | 0.1800 | 0.2133 | 20 | 10 | 0.0333 | 2.0000 | 0.098737 | 0.296211 |
| executability | canonical -> disp_2 | 300 | 0.1800 | 0.2000 | 18 | 12 | 0.0200 | 1.5000 | 0.361595 | 0.529862 |
| executability | canonical -> disp_3 | 300 | 0.1800 | 0.1567 | 11 | 18 | -0.0233 | 0.6111 | 0.264931 | 0.529862 |
| executability | canonical -> plan_front | 300 | 0.1800 | 0.2267 | 23 | 9 | 0.0467 | 2.5556 | 0.020062 | 0.100308 |
| executability | canonical -> plan_scatter | 300 | 0.1800 | 0.2200 | 19 | 7 | 0.0400 | 2.7143 | 0.028959 | 0.115837 |
| executability | plan_front -> canonical | 300 | 0.2267 | 0.1800 | 9 | 23 | -0.0467 | 0.3913 | 0.020062 | 0.080246 |
| executability | plan_front -> disp_1 | 300 | 0.2267 | 0.2133 | 12 | 16 | -0.0133 | 0.7500 | 0.571588 | 1.000000 |
| executability | plan_front -> disp_2 | 300 | 0.2267 | 0.2000 | 9 | 17 | -0.0267 | 0.5294 | 0.168638 | 0.505913 |
| executability | plan_front -> disp_3 | 300 | 0.2267 | 0.1567 | 5 | 26 | -0.0700 | 0.1923 | 0.000192 | 0.000961 |
| executability | plan_front -> plan_scatter | 300 | 0.2267 | 0.2200 | 11 | 13 | -0.0067 | 0.8462 | 0.838820 | 1.000000 |
| non_executable_failure | canonical -> disp_1 | 300 | 0.8200 | 0.7867 | 10 | 20 | -0.0333 | 0.5000 | 0.098737 | 0.296211 |
| non_executable_failure | canonical -> disp_2 | 300 | 0.8200 | 0.8000 | 12 | 18 | -0.0200 | 0.6667 | 0.361595 | 0.529862 |
| non_executable_failure | canonical -> disp_3 | 300 | 0.8200 | 0.8433 | 18 | 11 | 0.0233 | 1.6364 | 0.264931 | 0.529862 |
| non_executable_failure | canonical -> plan_front | 300 | 0.8200 | 0.7733 | 9 | 23 | -0.0467 | 0.3913 | 0.020062 | 0.100308 |
| non_executable_failure | canonical -> plan_scatter | 300 | 0.8200 | 0.7800 | 7 | 19 | -0.0400 | 0.3684 | 0.028959 | 0.115837 |
| non_executable_failure | plan_front -> canonical | 300 | 0.7733 | 0.8200 | 23 | 9 | 0.0467 | 2.5556 | 0.020062 | 0.080246 |
| non_executable_failure | plan_front -> disp_1 | 300 | 0.7733 | 0.7867 | 16 | 12 | 0.0133 | 1.3333 | 0.571588 | 1.000000 |
| non_executable_failure | plan_front -> disp_2 | 300 | 0.7733 | 0.8000 | 17 | 9 | 0.0267 | 1.8889 | 0.168638 | 0.505913 |
| non_executable_failure | plan_front -> disp_3 | 300 | 0.7733 | 0.8433 | 26 | 5 | 0.0700 | 5.2000 | 0.000192 | 0.000961 |
| non_executable_failure | plan_front -> plan_scatter | 300 | 0.7733 | 0.7800 | 13 | 11 | 0.0067 | 1.1818 | 0.838820 | 1.000000 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 54 | 64 | 0.9259 | 0.9062 | 50/4 | 58/6 | -0.0197 | 0.7733 | 0.752577 | 1.000000 |
| conditional_reachability | canonical -> disp_2 | 54 | 60 | 0.9259 | 0.9500 | 50/4 | 57/3 | 0.0241 | 1.5200 | 0.706046 | 1.000000 |
| conditional_reachability | canonical -> disp_3 | 54 | 47 | 0.9259 | 0.9787 | 50/4 | 46/1 | 0.0528 | 3.6800 | 0.368545 | 1.000000 |
| conditional_reachability | canonical -> plan_front | 54 | 68 | 0.9259 | 0.9853 | 50/4 | 67/1 | 0.0594 | 5.3600 | 0.169290 | 0.846448 |
| conditional_reachability | canonical -> plan_scatter | 54 | 66 | 0.9259 | 0.9545 | 50/4 | 63/3 | 0.0286 | 1.6800 | 0.699488 | 1.000000 |
| conditional_reachability | plan_front -> canonical | 68 | 54 | 0.9853 | 0.9259 | 67/1 | 50/4 | -0.0594 | 0.1866 | 0.169290 | 0.677158 |
| conditional_reachability | plan_front -> disp_1 | 68 | 64 | 0.9853 | 0.9062 | 67/1 | 58/6 | -0.0790 | 0.1443 | 0.056758 | 0.283788 |
| conditional_reachability | plan_front -> disp_2 | 68 | 60 | 0.9853 | 0.9500 | 67/1 | 57/3 | -0.0353 | 0.2836 | 0.340174 | 1.000000 |
| conditional_reachability | plan_front -> disp_3 | 68 | 47 | 0.9853 | 0.9787 | 67/1 | 46/1 | -0.0066 | 0.6866 | 1.000000 | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 68 | 66 | 0.9853 | 0.9545 | 67/1 | 63/3 | -0.0307 | 0.3134 | 0.361878 | 1.000000 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 43 | 9.5581 | 8.8372 | -0.7209 | -0.0754 | -0.1807 | 0.242750 | 0.437500 | 1.000000 |
| plan_length | canonical -> disp_2 | 40 | 8.0250 | 7.9750 | -0.0500 | -0.0062 | -0.1581 | 0.323475 | 1.000000 | 1.000000 |
| plan_length | canonical -> disp_3 | 34 | 8.9118 | 8.2353 | -0.6765 | -0.0759 | -0.1623 | 0.350904 | 0.750000 | 1.000000 |
| plan_length | canonical -> plan_front | 43 | 9.1163 | 8.5116 | -0.6047 | -0.0663 | -0.1650 | 0.285547 | 0.500000 | 1.000000 |
| plan_length | canonical -> plan_scatter | 45 | 9.4000 | 8.6000 | -0.8000 | -0.0851 | -0.2007 | 0.185121 | 0.375000 | 1.000000 |
| plan_length | plan_front -> canonical | 43 | 8.5116 | 9.1163 | 0.6047 | 0.0710 | 0.1650 | 0.285547 | 0.500000 | 1.000000 |
| plan_length | plan_front -> disp_1 | 51 | 9.1373 | 9.2157 | 0.0784 | 0.0086 | 0.1140 | 0.419625 | 0.562500 | 1.000000 |
| plan_length | plan_front -> disp_2 | 51 | 8.6078 | 8.5686 | -0.0392 | -0.0046 | -0.0880 | 0.532411 | 1.000000 | 1.000000 |
| plan_length | plan_front -> disp_3 | 42 | 8.6190 | 8.6190 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | plan_front -> plan_scatter | 55 | 9.0182 | 9.0182 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_1 | 43 | 1.0605 | 1.0149 | -0.0455 | -0.0429 | -0.1675 | 0.278285 | 0.406250 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 40 | 1.0050 | 1.0000 | -0.0050 | -0.0050 | -0.1581 | 0.323475 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 34 | 1.0529 | 1.0088 | -0.0441 | -0.0419 | -0.1565 | 0.368224 | 0.750000 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 43 | 1.0419 | 1.0000 | -0.0419 | -0.0402 | -0.1707 | 0.269247 | 0.500000 | 1.000000 |
| optimality_ratio | canonical -> plan_scatter | 45 | 1.0578 | 1.0044 | -0.0533 | -0.0504 | -0.1993 | 0.188187 | 0.375000 | 1.000000 |
| optimality_ratio | plan_front -> canonical | 43 | 1.0000 | 1.0419 | 0.0419 | 0.0419 | 0.1707 | 0.269247 | 0.500000 | 1.000000 |
| optimality_ratio | plan_front -> disp_1 | 51 | 1.0039 | 1.0126 | 0.0087 | 0.0086 | 0.1358 | 0.336962 | 0.500000 | 1.000000 |
| optimality_ratio | plan_front -> disp_2 | 51 | 1.0039 | 1.0013 | -0.0026 | -0.0026 | -0.0880 | 0.532411 | 1.000000 | 1.000000 |
| optimality_ratio | plan_front -> disp_3 | 42 | 1.0048 | 1.0071 | 0.0024 | 0.0024 | 0.0423 | 0.785247 | 1.000000 | 1.000000 |
| optimality_ratio | plan_front -> plan_scatter | 55 | 1.0036 | 1.0048 | 0.0012 | 0.0012 | 0.0307 | 0.820949 | 1.000000 | 1.000000 |
| first_failure_step | canonical -> disp_1 | 2 | 6.0000 | 6.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| first_failure_step | canonical -> disp_2 | 3 | 9.3333 | 23.0000 | 13.6667 | 1.4643 | 0.5768 | 0.422993 | 0.750000 | 1.000000 |
| first_failure_step | canonical -> disp_3 | 4 | 8.2500 | 8.2500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| first_failure_step | canonical -> plan_front | 1 | 8.0000 | 8.0000 | 0.0000 | 0.0000 | NA | NA | 1.000000 | 1.000000 |
| first_failure_step | canonical -> plan_scatter | 1 | 4.0000 | 7.0000 | 3.0000 | 0.7500 | NA | NA | 1.000000 | 1.000000 |
| first_failure_step | plan_front -> canonical | 1 | 8.0000 | 8.0000 | 0.0000 | 0.0000 | NA | NA | 1.000000 | 1.000000 |
| first_failure_step | plan_front -> disp_1 | 4 | 6.0000 | 5.7500 | -0.2500 | -0.0417 | -0.0870 | 0.872889 | 1.000000 | 1.000000 |
| first_failure_step | plan_front -> disp_2 | 3 | 4.3333 | 4.6667 | 0.3333 | 0.0769 | 0.1325 | 0.839872 | 1.000000 | 1.000000 |
| first_failure_step | plan_front -> disp_3 | 2 | 4.5000 | 6.0000 | 1.5000 | 0.3333 | 0.4243 | 0.655958 | 1.000000 | 1.000000 |
| first_failure_step | plan_front -> plan_scatter | 1 | 4.0000 | 8.0000 | 4.0000 | 1.0000 | NA | NA | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_1 | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> canonical | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> disp_1 | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> disp_2 | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> disp_3 | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 300 | 9815.0500 | 9815.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> disp_1 | 300 | 12949.6333 | 12643.2967 | -306.3367 | -0.0237 | -0.0687 | 0.235082 | 0.234840 | 0.704520 |
| completion_tokens | canonical -> disp_2 | 300 | 12949.6333 | 13055.8833 | 106.2500 | 0.0082 | 0.0247 | 0.668840 | 0.667720 | 0.704520 |
| completion_tokens | canonical -> disp_3 | 300 | 12949.6333 | 13816.0567 | 866.4233 | 0.0669 | 0.2135 | 0.000259 | 0.000260 | 0.001300 |
| completion_tokens | canonical -> plan_front | 300 | 12949.6333 | 12654.3100 | -295.3233 | -0.0228 | -0.0663 | 0.252092 | 0.251830 | 0.704520 |
| completion_tokens | canonical -> plan_scatter | 300 | 12949.6333 | 12517.8433 | -431.7900 | -0.0333 | -0.0991 | 0.087000 | 0.087220 | 0.348880 |
| completion_tokens | plan_front -> canonical | 300 | 12654.3100 | 12949.6333 | 295.3233 | 0.0233 | 0.0663 | 0.252092 | 0.251830 | 0.755490 |
| completion_tokens | plan_front -> disp_1 | 300 | 12654.3100 | 12643.2967 | -11.0133 | -0.0009 | -0.0028 | 0.961278 | 0.961460 | 1.000000 |
| completion_tokens | plan_front -> disp_2 | 300 | 12654.3100 | 13055.8833 | 401.5733 | 0.0317 | 0.0978 | 0.091303 | 0.093530 | 0.374120 |
| completion_tokens | plan_front -> disp_3 | 300 | 12654.3100 | 13816.0567 | 1161.7467 | 0.0918 | 0.2961 | 0.000001 | 0.000000 | 0.000000 |
| completion_tokens | plan_front -> plan_scatter | 300 | 12654.3100 | 12517.8433 | -136.4667 | -0.0108 | -0.0327 | 0.572049 | 0.575060 | 1.000000 |
| reasoning_completion_tokens | canonical -> disp_1 | 300 | 4866.8600 | 4123.6167 | -743.2433 | -0.1527 | -0.1024 | 0.077082 | 0.077720 | 0.159280 |
| reasoning_completion_tokens | canonical -> disp_2 | 300 | 4866.8600 | 4044.6833 | -822.1767 | -0.1689 | -0.1121 | 0.053147 | 0.052970 | 0.159280 |
| reasoning_completion_tokens | canonical -> disp_3 | 300 | 4866.8600 | 2838.7767 | -2028.0833 | -0.4167 | -0.2971 | 0.000000 | 0.000000 | 0.000000 |
| reasoning_completion_tokens | canonical -> plan_front | 300 | 4866.8600 | 4237.3533 | -629.5067 | -0.1293 | -0.0881 | 0.127999 | 0.127770 | 0.159280 |
| reasoning_completion_tokens | canonical -> plan_scatter | 300 | 4866.8600 | 4052.7767 | -814.0833 | -0.1673 | -0.1193 | 0.039676 | 0.039820 | 0.159280 |
| reasoning_completion_tokens | plan_front -> canonical | 300 | 4237.3533 | 4866.8600 | 629.5067 | 0.1486 | 0.0881 | 0.127999 | 0.127770 | 0.511080 |
| reasoning_completion_tokens | plan_front -> disp_1 | 300 | 4237.3533 | 4123.6167 | -113.7367 | -0.0268 | -0.0183 | 0.750852 | 0.750240 | 1.000000 |
| reasoning_completion_tokens | plan_front -> disp_2 | 300 | 4237.3533 | 4044.6833 | -192.6700 | -0.0455 | -0.0276 | 0.632767 | 0.633850 | 1.000000 |
| reasoning_completion_tokens | plan_front -> disp_3 | 300 | 4237.3533 | 2838.7767 | -1398.5767 | -0.3301 | -0.2135 | 0.000259 | 0.000250 | 0.001250 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 300 | 4237.3533 | 4052.7767 | -184.5767 | -0.0436 | -0.0273 | 0.637070 | 0.638290 | 1.000000 |
| raw_completion_tokens | canonical -> disp_1 | 300 | 8082.7733 | 8519.6800 | 436.9067 | 0.0541 | 0.0436 | 0.450611 | 0.507340 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 300 | 8082.7733 | 9011.2000 | 928.4267 | 0.1149 | 0.0934 | 0.106736 | 0.129330 | 0.517320 |
| raw_completion_tokens | canonical -> disp_3 | 300 | 8082.7733 | 10977.2800 | 2894.5067 | 0.3581 | 0.3092 | 0.000000 | 0.000000 | 0.000000 |
| raw_completion_tokens | canonical -> plan_front | 300 | 8082.7733 | 8416.9567 | 334.1833 | 0.0413 | 0.0340 | 0.556890 | 0.564420 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 300 | 8082.7733 | 8465.0667 | 382.2933 | 0.0473 | 0.0406 | 0.482644 | 0.547270 | 1.000000 |
| raw_completion_tokens | plan_front -> canonical | 300 | 8416.9567 | 8082.7733 | -334.1833 | -0.0397 | -0.0340 | 0.556890 | 0.564420 | 1.000000 |
| raw_completion_tokens | plan_front -> disp_1 | 300 | 8416.9567 | 8519.6800 | 102.7233 | 0.0122 | 0.0117 | 0.839676 | 0.912280 | 1.000000 |
| raw_completion_tokens | plan_front -> disp_2 | 300 | 8416.9567 | 9011.2000 | 594.2433 | 0.0706 | 0.0620 | 0.283881 | 0.326400 | 1.000000 |
| raw_completion_tokens | plan_front -> disp_3 | 300 | 8416.9567 | 10977.2800 | 2560.3233 | 0.3042 | 0.2822 | 0.000002 | 0.000010 | 0.000050 |
| raw_completion_tokens | plan_front -> plan_scatter | 300 | 8416.9567 | 8465.0667 | 48.1100 | 0.0057 | 0.0051 | 0.930330 | 1.000000 | 1.000000 |
| total_tokens | canonical -> disp_1 | 300 | 22764.6833 | 22458.3467 | -306.3367 | -0.0135 | -0.0687 | 0.235082 | 0.234840 | 0.704520 |
| total_tokens | canonical -> disp_2 | 300 | 22764.6833 | 22870.9333 | 106.2500 | 0.0047 | 0.0247 | 0.668840 | 0.667720 | 0.704520 |
| total_tokens | canonical -> disp_3 | 300 | 22764.6833 | 23631.1067 | 866.4233 | 0.0381 | 0.2135 | 0.000259 | 0.000260 | 0.001300 |
| total_tokens | canonical -> plan_front | 300 | 22764.6833 | 22469.3600 | -295.3233 | -0.0130 | -0.0663 | 0.252092 | 0.251830 | 0.704520 |
| total_tokens | canonical -> plan_scatter | 300 | 22764.6833 | 22332.8933 | -431.7900 | -0.0190 | -0.0991 | 0.087000 | 0.087220 | 0.348880 |
| total_tokens | plan_front -> canonical | 300 | 22469.3600 | 22764.6833 | 295.3233 | 0.0131 | 0.0663 | 0.252092 | 0.251830 | 0.755490 |
| total_tokens | plan_front -> disp_1 | 300 | 22469.3600 | 22458.3467 | -11.0133 | -0.0005 | -0.0028 | 0.961278 | 0.961460 | 1.000000 |
| total_tokens | plan_front -> disp_2 | 300 | 22469.3600 | 22870.9333 | 401.5733 | 0.0179 | 0.0978 | 0.091303 | 0.093530 | 0.374120 |
| total_tokens | plan_front -> disp_3 | 300 | 22469.3600 | 23631.1067 | 1161.7467 | 0.0517 | 0.2961 | 0.000001 | 0.000000 | 0.000000 |
| total_tokens | plan_front -> plan_scatter | 300 | 22469.3600 | 22332.8933 | -136.4667 | -0.0061 | -0.0327 | 0.572049 | 0.575060 | 1.000000 |
| duration_sec | canonical -> disp_1 | 300 | 92.5973 | 89.4913 | -3.1060 | -0.0335 | -0.0624 | 0.280797 | 0.281150 | 0.765480 |
| duration_sec | canonical -> disp_2 | 300 | 92.5973 | 89.0343 | -3.5630 | -0.0385 | -0.0754 | 0.192304 | 0.191370 | 0.765480 |
| duration_sec | canonical -> disp_3 | 300 | 92.5973 | 95.6245 | 3.0272 | 0.0327 | 0.0665 | 0.250106 | 0.249990 | 0.765480 |
| duration_sec | canonical -> plan_front | 300 | 92.5973 | 90.3637 | -2.2336 | -0.0241 | -0.0445 | 0.441719 | 0.441550 | 0.765480 |
| duration_sec | canonical -> plan_scatter | 300 | 92.5973 | 86.2852 | -6.3121 | -0.0682 | -0.1324 | 0.022571 | 0.022370 | 0.111850 |
| duration_sec | plan_front -> canonical | 300 | 90.3637 | 92.5973 | 2.2336 | 0.0247 | 0.0445 | 0.441719 | 0.441550 | 1.000000 |
| duration_sec | plan_front -> disp_1 | 300 | 90.3637 | 89.4913 | -0.8724 | -0.0097 | -0.0173 | 0.764263 | 0.766060 | 1.000000 |
| duration_sec | plan_front -> disp_2 | 300 | 90.3637 | 89.0343 | -1.3294 | -0.0147 | -0.0285 | 0.621842 | 0.621290 | 1.000000 |
| duration_sec | plan_front -> disp_3 | 300 | 90.3637 | 95.6245 | 5.2608 | 0.0582 | 0.1082 | 0.061883 | 0.061380 | 0.306900 |
| duration_sec | plan_front -> plan_scatter | 300 | 90.3637 | 86.2852 | -4.0785 | -0.0451 | -0.0853 | 0.140640 | 0.141660 | 0.566640 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> canonical | 20 | 0.2233 | 0.1667 | -0.0567 | [-0.1233, -0.0133] | 0.031250 |
| reachability | plan_front -> disp_1 | 20 | 0.2233 | 0.1933 | -0.0300 | [-0.0767, 0.0033] | 0.375000 |
| reachability | plan_front -> disp_2 | 20 | 0.2233 | 0.1900 | -0.0333 | [-0.1000, 0.0067] | 0.500000 |
| reachability | plan_front -> disp_3 | 20 | 0.2233 | 0.1533 | -0.0700 | [-0.1467, -0.0133] | 0.031250 |
| reachability | plan_front -> plan_scatter | 20 | 0.2233 | 0.2100 | -0.0133 | [-0.0467, 0.0133] | 0.625000 |
| executability | plan_front -> canonical | 20 | 0.2267 | 0.1800 | -0.0467 | [-0.1100, -0.0033] | 0.093750 |
| executability | plan_front -> disp_1 | 20 | 0.2267 | 0.2133 | -0.0133 | [-0.0600, 0.0267] | 0.664062 |
| executability | plan_front -> disp_2 | 20 | 0.2267 | 0.2000 | -0.0267 | [-0.0967, 0.0167] | 0.773438 |
| executability | plan_front -> disp_3 | 20 | 0.2267 | 0.1567 | -0.0700 | [-0.1467, -0.0133] | 0.031250 |
| executability | plan_front -> plan_scatter | 20 | 0.2267 | 0.2200 | -0.0067 | [-0.0433, 0.0233] | 0.875000 |
| non_executable_failure | plan_front -> canonical | 20 | 0.7733 | 0.8200 | 0.0467 | [0.0033, 0.1100] | 0.093750 |
| non_executable_failure | plan_front -> disp_1 | 20 | 0.7733 | 0.7867 | 0.0133 | [-0.0267, 0.0600] | 0.664062 |
| non_executable_failure | plan_front -> disp_2 | 20 | 0.7733 | 0.8000 | 0.0267 | [-0.0167, 0.0967] | 0.773438 |
| non_executable_failure | plan_front -> disp_3 | 20 | 0.7733 | 0.8433 | 0.0700 | [0.0133, 0.1467] | 0.031250 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.7733 | 0.7800 | 0.0067 | [-0.0233, 0.0433] | 0.875000 |
| conditional_reachability | plan_front -> canonical | 6 | 0.8333 | 0.7833 | -0.0500 | [-0.1167, 0.0000] | 0.500000 |
| conditional_reachability | plan_front -> disp_1 | 6 | 1.0000 | 0.9722 | -0.0278 | [-0.0833, 0.0000] | 1.000000 |
| conditional_reachability | plan_front -> disp_2 | 6 | 1.0000 | 0.8333 | -0.1667 | [-0.5000, 0.0000] | 1.000000 |
| conditional_reachability | plan_front -> disp_3 | 6 | 1.0000 | 0.8333 | -0.1667 | [-0.5000, 0.0000] | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 6 | 1.0000 | 0.8333 | -0.1667 | [-0.5000, 0.0000] | 1.000000 |
| plan_length | plan_front -> canonical | 5 | 9.6462 | 11.4333 | 1.7872 | [0.0000, 5.2949] | 0.500000 |
| plan_length | plan_front -> disp_1 | 6 | 11.2051 | 11.2792 | 0.0741 | [0.0000, 0.1510] | 0.500000 |
| plan_length | plan_front -> disp_2 | 5 | 9.6462 | 9.6500 | 0.0038 | [0.0000, 0.0115] | 1.000000 |
| plan_length | plan_front -> disp_3 | 5 | 9.6462 | 9.6500 | 0.0038 | [-0.1385, 0.1500] | 1.000000 |
| plan_length | plan_front -> plan_scatter | 5 | 9.6462 | 9.6508 | 0.0046 | [-0.0718, 0.0857] | 1.000000 |
| optimality_ratio | plan_front -> canonical | 5 | 1.0031 | 1.1233 | 0.1203 | [0.0000, 0.3541] | 0.500000 |
| optimality_ratio | plan_front -> disp_1 | 6 | 1.0998 | 1.1070 | 0.0072 | [0.0000, 0.0168] | 0.500000 |
| optimality_ratio | plan_front -> disp_2 | 5 | 1.0031 | 1.0033 | 0.0003 | [0.0000, 0.0008] | 1.000000 |
| optimality_ratio | plan_front -> disp_3 | 5 | 1.0031 | 1.0050 | 0.0019 | [-0.0092, 0.0150] | 1.000000 |
| optimality_ratio | plan_front -> plan_scatter | 5 | 1.0031 | 1.0043 | 0.0013 | [-0.0048, 0.0086] | 1.000000 |
| first_failure_step | plan_front -> canonical | 5 | 7.4400 | 6.6400 | -0.8000 | [-3.0000, 0.8000] | 0.875000 |
| first_failure_step | plan_front -> disp_1 | 4 | 9.0500 | 4.1250 | -4.9250 | [-9.5000, -0.3500] | 0.250000 |
| first_failure_step | plan_front -> disp_2 | 6 | 5.8667 | 3.7917 | -2.0750 | [-5.4167, 0.3500] | 0.500000 |
| first_failure_step | plan_front -> disp_3 | 4 | 5.8000 | 4.5000 | -1.3000 | [-4.0500, 0.6500] | 0.750000 |
| first_failure_step | plan_front -> plan_scatter | 6 | 4.7000 | 5.0833 | 0.3833 | [-2.0333, 2.9167] | 0.781250 |
| prompt_tokens | plan_front -> canonical | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> disp_1 | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> disp_2 | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> disp_3 | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 9815.0500 | 9815.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| completion_tokens | plan_front -> canonical | 20 | 12654.3100 | 12949.6333 | 295.3233 | [-413.0793, 1102.3213] | 0.479706 |
| completion_tokens | plan_front -> disp_1 | 20 | 12654.3100 | 12643.2967 | -11.0133 | [-410.1891, 370.6902] | 0.958046 |
| completion_tokens | plan_front -> disp_2 | 20 | 12654.3100 | 13055.8833 | 401.5733 | [-131.9071, 1005.2536] | 0.203728 |
| completion_tokens | plan_front -> disp_3 | 20 | 12654.3100 | 13816.0567 | 1161.7467 | [526.2108, 1847.6519] | 0.002232 |
| completion_tokens | plan_front -> plan_scatter | 20 | 12654.3100 | 12517.8433 | -136.4667 | [-723.6687, 405.2374] | 0.660250 |
| reasoning_completion_tokens | plan_front -> canonical | 20 | 4237.3533 | 4866.8600 | 629.5067 | [-319.1461, 1521.9662] | 0.196404 |
| reasoning_completion_tokens | plan_front -> disp_1 | 20 | 4237.3533 | 4123.6167 | -113.7367 | [-832.0394, 588.7813] | 0.759298 |
| reasoning_completion_tokens | plan_front -> disp_2 | 20 | 4237.3533 | 4044.6833 | -192.6700 | [-1135.6171, 726.8195] | 0.705639 |
| reasoning_completion_tokens | plan_front -> disp_3 | 20 | 4237.3533 | 2838.7767 | -1398.5767 | [-2368.1298, -509.7378] | 0.005943 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 4237.3533 | 4052.7767 | -184.5767 | [-1139.1218, 708.0803] | 0.704782 |
| raw_completion_tokens | plan_front -> canonical | 20 | 8416.9567 | 8082.7733 | -334.1833 | [-1802.2400, 1297.7133] | 0.695679 |
| raw_completion_tokens | plan_front -> disp_1 | 20 | 8416.9567 | 8519.6800 | 102.7233 | [-825.7033, 1037.6533] | 0.912598 |
| raw_completion_tokens | plan_front -> disp_2 | 20 | 8416.9567 | 9011.2000 | 594.2433 | [-764.5867, 2020.6933] | 0.481445 |
| raw_completion_tokens | plan_front -> disp_3 | 20 | 8416.9567 | 10977.2800 | 2560.3233 | [1243.1000, 4082.9933] | 0.001465 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 8416.9567 | 8465.0667 | 48.1100 | [-1221.0033, 1358.9926] | 1.000000 |
| total_tokens | plan_front -> canonical | 20 | 22469.3600 | 22764.6833 | 295.3233 | [-413.0793, 1102.3213] | 0.479706 |
| total_tokens | plan_front -> disp_1 | 20 | 22469.3600 | 22458.3467 | -11.0133 | [-410.1891, 370.6902] | 0.958046 |
| total_tokens | plan_front -> disp_2 | 20 | 22469.3600 | 22870.9333 | 401.5733 | [-131.9071, 1005.2536] | 0.203728 |
| total_tokens | plan_front -> disp_3 | 20 | 22469.3600 | 23631.1067 | 1161.7467 | [526.2108, 1847.6519] | 0.002232 |
| total_tokens | plan_front -> plan_scatter | 20 | 22469.3600 | 22332.8933 | -136.4667 | [-723.6687, 405.2374] | 0.660250 |
| duration_sec | plan_front -> canonical | 20 | 90.3637 | 92.5973 | 2.2336 | [-5.7982, 11.1567] | 0.624119 |
| duration_sec | plan_front -> disp_1 | 20 | 90.3637 | 89.4913 | -0.8724 | [-6.8613, 4.7513] | 0.789757 |
| duration_sec | plan_front -> disp_2 | 20 | 90.3637 | 89.0343 | -1.3294 | [-7.7790, 6.3540] | 0.743114 |
| duration_sec | plan_front -> disp_3 | 20 | 90.3637 | 95.6245 | 5.2608 | [-0.8656, 11.2857] | 0.112795 |
| duration_sec | plan_front -> plan_scatter | 20 | 90.3637 | 86.2852 | -4.0785 | [-10.3239, 1.8609] | 0.216339 |
