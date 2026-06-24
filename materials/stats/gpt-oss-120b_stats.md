# Statistical Tests: gpt-oss-120b

Baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_scatter`.
Extra comparisons: `plan_front` vs `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 300 | 0.1300 | 0.0833 | 4 | 18 | -0.0467 | 0.2222 | 0.004344 | 0.013031 |
| reachability | canonical -> disp_2 | 300 | 0.1300 | 0.0700 | 4 | 22 | -0.0600 | 0.1818 | 0.000534 | 0.002134 |
| reachability | canonical -> disp_3 | 300 | 0.1300 | 0.0400 | 2 | 29 | -0.0900 | 0.0690 | 0.000000 | 0.000002 |
| reachability | canonical -> plan_front | 300 | 0.1300 | 0.1533 | 13 | 6 | 0.0233 | 2.1667 | 0.167068 | 0.167068 |
| reachability | canonical -> plan_scatter | 300 | 0.1300 | 0.0867 | 5 | 18 | -0.0433 | 0.2778 | 0.010622 | 0.021244 |
| reachability | plan_front -> plan_scatter | 300 | 0.1533 | 0.0867 | 3 | 23 | -0.0667 | 0.1304 | 0.000088 | 0.000088 |
| executability | canonical -> disp_1 | 300 | 0.4167 | 0.3733 | 49 | 62 | -0.0433 | 0.7903 | 0.254605 | 0.763815 |
| executability | canonical -> disp_2 | 300 | 0.4167 | 0.3567 | 47 | 65 | -0.0600 | 0.7231 | 0.107782 | 0.431129 |
| executability | canonical -> disp_3 | 300 | 0.4167 | 0.3167 | 42 | 72 | -0.1000 | 0.5833 | 0.006352 | 0.031758 |
| executability | canonical -> plan_front | 300 | 0.4167 | 0.4500 | 60 | 50 | 0.0333 | 1.2000 | 0.390927 | 0.781855 |
| executability | canonical -> plan_scatter | 300 | 0.4167 | 0.4467 | 70 | 61 | 0.0300 | 1.1475 | 0.484720 | 0.781855 |
| executability | plan_front -> plan_scatter | 300 | 0.4500 | 0.4467 | 66 | 67 | -0.0033 | 0.9851 | 1.000000 | 1.000000 |
| non_executable_failure | canonical -> disp_1 | 300 | 0.5833 | 0.6267 | 62 | 49 | 0.0433 | 1.2653 | 0.254605 | 0.763815 |
| non_executable_failure | canonical -> disp_2 | 300 | 0.5833 | 0.6433 | 65 | 47 | 0.0600 | 1.3830 | 0.107782 | 0.431129 |
| non_executable_failure | canonical -> disp_3 | 300 | 0.5833 | 0.6833 | 72 | 42 | 0.1000 | 1.7143 | 0.006352 | 0.031758 |
| non_executable_failure | canonical -> plan_front | 300 | 0.5833 | 0.5500 | 50 | 60 | -0.0333 | 0.8333 | 0.390927 | 0.781855 |
| non_executable_failure | canonical -> plan_scatter | 300 | 0.5833 | 0.5533 | 61 | 70 | -0.0300 | 0.8714 | 0.484720 | 0.781855 |
| non_executable_failure | plan_front -> plan_scatter | 300 | 0.5500 | 0.5533 | 67 | 66 | 0.0033 | 1.0152 | 1.000000 | 1.000000 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 125 | 112 | 0.3120 | 0.2232 | 39/86 | 25/87 | -0.0888 | 0.6337 | 0.143671 | 0.287343 |
| conditional_reachability | canonical -> disp_2 | 125 | 107 | 0.3120 | 0.1963 | 39/86 | 21/86 | -0.1157 | 0.5385 | 0.051141 | 0.153424 |
| conditional_reachability | canonical -> disp_3 | 125 | 95 | 0.3120 | 0.1263 | 39/86 | 12/83 | -0.1857 | 0.3188 | 0.001224 | 0.006121 |
| conditional_reachability | canonical -> plan_front | 125 | 135 | 0.3120 | 0.3407 | 39/86 | 46/89 | 0.0287 | 1.1397 | 0.691757 | 0.691757 |
| conditional_reachability | canonical -> plan_scatter | 125 | 134 | 0.3120 | 0.1940 | 39/86 | 26/108 | -0.1180 | 0.5309 | 0.032001 | 0.128003 |
| conditional_reachability | plan_front -> plan_scatter | 135 | 134 | 0.3407 | 0.1940 | 46/89 | 26/108 | -0.1467 | 0.4658 | 0.008666 | 0.008666 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 21 | 7.1905 | 7.0952 | -0.0952 | -0.0132 | -0.2182 | 0.329257 | 1.000000 | 1.000000 |
| plan_length | canonical -> disp_2 | 17 | 6.7647 | 6.5294 | -0.2353 | -0.0348 | -0.3542 | 0.163485 | 0.500000 | 1.000000 |
| plan_length | canonical -> disp_3 | 10 | 6.8000 | 6.8000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | canonical -> plan_front | 33 | 7.6970 | 7.5152 | -0.1818 | -0.0236 | -0.2365 | 0.183732 | 0.375000 | 1.000000 |
| plan_length | canonical -> plan_scatter | 21 | 7.6667 | 7.2857 | -0.3810 | -0.0497 | -0.4734 | 0.042286 | 0.125000 | 0.625000 |
| plan_length | plan_front -> plan_scatter | 23 | 7.6087 | 7.5217 | -0.0870 | -0.0114 | -0.2085 | 0.328183 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_1 | 21 | 1.0159 | 1.0000 | -0.0159 | -0.0156 | -0.2182 | 0.329257 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 17 | 1.0392 | 1.0000 | -0.0392 | -0.0377 | -0.3542 | 0.163485 | 0.500000 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 10 | 1.0667 | 1.0667 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 33 | 1.0337 | 1.0067 | -0.0269 | -0.0261 | -0.2589 | 0.146759 | 0.250000 | 1.000000 |
| optimality_ratio | canonical -> plan_scatter | 21 | 1.0529 | 1.0000 | -0.0529 | -0.0503 | -0.4621 | 0.046931 | 0.125000 | 0.625000 |
| optimality_ratio | plan_front -> plan_scatter | 23 | 1.0097 | 1.0000 | -0.0097 | -0.0096 | -0.2085 | 0.328183 | 1.000000 | 1.000000 |
| first_failure_step | canonical -> disp_1 | 41 | 3.5366 | 4.0732 | 0.5366 | 0.1517 | 0.1803 | 0.255097 | 0.275950 | 0.827850 |
| first_failure_step | canonical -> disp_2 | 37 | 3.4054 | 3.1351 | -0.2703 | -0.0794 | -0.1246 | 0.453327 | 0.507122 | 1.000000 |
| first_failure_step | canonical -> disp_3 | 49 | 3.9388 | 3.1633 | -0.7755 | -0.1969 | -0.3099 | 0.035026 | 0.040810 | 0.204050 |
| first_failure_step | canonical -> plan_front | 51 | 4.3922 | 4.1569 | -0.2353 | -0.0536 | -0.1033 | 0.463937 | 0.507050 | 1.000000 |
| first_failure_step | canonical -> plan_scatter | 27 | 4.3333 | 3.1481 | -1.1852 | -0.2735 | -0.4074 | 0.044009 | 0.051490 | 0.205960 |
| first_failure_step | plan_front -> plan_scatter | 27 | 4.4074 | 3.1111 | -1.2963 | -0.2941 | -0.5851 | 0.005337 | 0.007700 | 0.007700 |
| prompt_tokens | canonical -> disp_1 | 300 | 8741.9000 | 8741.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 300 | 8741.9000 | 8741.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 300 | 8741.9000 | 8741.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 300 | 8741.9000 | 8741.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 300 | 8741.9000 | 8741.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 300 | 8741.9000 | 8741.9000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> disp_1 | 300 | 1100.6033 | 1020.1467 | -80.4567 | -0.0731 | -0.0844 | 0.144790 | 0.145910 | 0.291820 |
| completion_tokens | canonical -> disp_2 | 300 | 1100.6033 | 902.7967 | -197.8067 | -0.1797 | -0.2181 | 0.000191 | 0.000280 | 0.001120 |
| completion_tokens | canonical -> disp_3 | 300 | 1100.6033 | 1076.1733 | -24.4300 | -0.0222 | -0.0262 | 0.650674 | 0.651110 | 0.651110 |
| completion_tokens | canonical -> plan_front | 300 | 1100.6033 | 1010.2567 | -90.3467 | -0.0821 | -0.1017 | 0.079089 | 0.079060 | 0.237180 |
| completion_tokens | canonical -> plan_scatter | 300 | 1100.6033 | 870.3967 | -230.2067 | -0.2092 | -0.2775 | 0.000002 | 0.000010 | 0.000050 |
| completion_tokens | plan_front -> plan_scatter | 300 | 1010.2567 | 870.3967 | -139.8600 | -0.1384 | -0.1685 | 0.003779 | 0.003800 | 0.003800 |
| reasoning_completion_tokens | canonical -> disp_1 | 300 | 1061.1467 | 1010.7800 | -50.3667 | -0.0475 | -0.0529 | 0.360666 | 0.361980 | 0.723960 |
| reasoning_completion_tokens | canonical -> disp_2 | 300 | 1061.1467 | 895.5200 | -165.6267 | -0.1561 | -0.1819 | 0.001799 | 0.001890 | 0.007560 |
| reasoning_completion_tokens | canonical -> disp_3 | 300 | 1061.1467 | 1065.8867 | 4.7400 | 0.0045 | 0.0051 | 0.930159 | 0.930590 | 0.930590 |
| reasoning_completion_tokens | canonical -> plan_front | 300 | 1061.1467 | 968.0467 | -93.1000 | -0.0877 | -0.1048 | 0.070532 | 0.070850 | 0.212550 |
| reasoning_completion_tokens | canonical -> plan_scatter | 300 | 1061.1467 | 831.6200 | -229.5267 | -0.2163 | -0.2794 | 0.000002 | 0.000010 | 0.000050 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 300 | 968.0467 | 831.6200 | -136.4267 | -0.1409 | -0.1653 | 0.004492 | 0.004500 | 0.004500 |
| raw_completion_tokens | canonical -> disp_1 | 300 | 39.4567 | 9.3667 | -30.0900 | -0.7626 | -0.2469 | 0.000026 | 0.000000 | 0.000000 |
| raw_completion_tokens | canonical -> disp_2 | 300 | 39.4567 | 7.2767 | -32.1800 | -0.8156 | -0.2225 | 0.000143 | 0.000130 | 0.000520 |
| raw_completion_tokens | canonical -> disp_3 | 300 | 39.4567 | 10.2867 | -29.1700 | -0.7393 | -0.2091 | 0.000343 | 0.000170 | 0.000520 |
| raw_completion_tokens | canonical -> plan_front | 300 | 39.4567 | 42.2100 | 2.7533 | 0.0698 | 0.0196 | 0.734915 | 0.738580 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 300 | 39.4567 | 38.7767 | -0.6800 | -0.0172 | -0.0040 | 0.945346 | 0.944640 | 1.000000 |
| raw_completion_tokens | plan_front -> plan_scatter | 300 | 42.2100 | 38.7767 | -3.4333 | -0.0813 | -0.0266 | 0.645741 | 0.649100 | 0.649100 |
| total_tokens | canonical -> disp_1 | 300 | 9842.5033 | 9762.0467 | -80.4567 | -0.0082 | -0.0844 | 0.144790 | 0.145910 | 0.291820 |
| total_tokens | canonical -> disp_2 | 300 | 9842.5033 | 9644.6967 | -197.8067 | -0.0201 | -0.2181 | 0.000191 | 0.000280 | 0.001120 |
| total_tokens | canonical -> disp_3 | 300 | 9842.5033 | 9818.0733 | -24.4300 | -0.0025 | -0.0262 | 0.650674 | 0.651110 | 0.651110 |
| total_tokens | canonical -> plan_front | 300 | 9842.5033 | 9752.1567 | -90.3467 | -0.0092 | -0.1017 | 0.079089 | 0.079060 | 0.237180 |
| total_tokens | canonical -> plan_scatter | 300 | 9842.5033 | 9612.2967 | -230.2067 | -0.0234 | -0.2775 | 0.000002 | 0.000010 | 0.000050 |
| total_tokens | plan_front -> plan_scatter | 300 | 9752.1567 | 9612.2967 | -139.8600 | -0.0143 | -0.1685 | 0.003779 | 0.003800 | 0.003800 |
| duration_sec | canonical -> disp_1 | 300 | 28.1044 | 25.4093 | -2.6951 | -0.0959 | -0.0982 | 0.090074 | 0.090420 | 0.271260 |
| duration_sec | canonical -> disp_2 | 300 | 28.1044 | 22.2457 | -5.8587 | -0.2085 | -0.2122 | 0.000280 | 0.000200 | 0.000800 |
| duration_sec | canonical -> disp_3 | 300 | 28.1044 | 27.9610 | -0.1434 | -0.0051 | -0.0048 | 0.933361 | 0.933950 | 1.000000 |
| duration_sec | canonical -> plan_front | 300 | 28.1044 | 27.2271 | -0.8773 | -0.0312 | -0.0283 | 0.623996 | 0.625470 | 1.000000 |
| duration_sec | canonical -> plan_scatter | 300 | 28.1044 | 22.1745 | -5.9299 | -0.2110 | -0.2269 | 0.000106 | 0.000070 | 0.000350 |
| duration_sec | plan_front -> plan_scatter | 300 | 27.2271 | 22.1745 | -5.0526 | -0.1856 | -0.1710 | 0.003310 | 0.003120 | 0.003120 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> plan_scatter | 20 | 0.1533 | 0.0867 | -0.0667 | [-0.1500, -0.0100] | 0.062500 |
| executability | plan_front -> plan_scatter | 20 | 0.4500 | 0.4467 | -0.0033 | [-0.1167, 0.1000] | 1.000000 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.5500 | 0.5533 | 0.0033 | [-0.1000, 0.1167] | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 19 | 0.1720 | 0.1291 | -0.0429 | [-0.1150, 0.0018] | 0.187500 |
| plan_length | plan_front -> plan_scatter | 4 | 8.2917 | 8.5000 | 0.2083 | [-0.1250, 0.7500] | 1.000000 |
| optimality_ratio | plan_front -> plan_scatter | 4 | 1.0046 | 1.0250 | 0.0204 | [-0.0139, 0.0750] | 1.000000 |
| first_failure_step | plan_front -> plan_scatter | 16 | 4.2062 | 2.8729 | -1.3334 | [-2.0768, -0.6468] | 0.002319 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 8741.9000 | 8741.9000 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| completion_tokens | plan_front -> plan_scatter | 20 | 1010.2567 | 870.3967 | -139.8600 | [-270.7127, -12.4453] | 0.056746 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 968.0467 | 831.6200 | -136.4267 | [-268.1201, -9.0096] | 0.061718 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 42.2100 | 38.7767 | -3.4333 | [-21.3968, 10.0400] | 0.765625 |
| total_tokens | plan_front -> plan_scatter | 20 | 9752.1567 | 9612.2967 | -139.8600 | [-270.7127, -12.4453] | 0.056746 |
| duration_sec | plan_front -> plan_scatter | 20 | 27.2271 | 22.1745 | -5.0526 | [-9.8313, -0.3205] | 0.060364 |
