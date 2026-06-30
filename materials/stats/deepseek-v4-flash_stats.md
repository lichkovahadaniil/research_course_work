# Statistical Tests: deepseek/deepseek-v4-flash

Primary baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_back`, `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 300 | 0.6267 | 0.6433 | 57 | 52 | 0.0167 | 1.0962 | 0.701811 | 1.000000 |
| reachability | canonical -> disp_2 | 300 | 0.6267 | 0.6233 | 54 | 55 | -0.0033 | 0.9818 | 1.000000 | 1.000000 |
| reachability | canonical -> disp_3 | 300 | 0.6267 | 0.4433 | 24 | 79 | -0.1833 | 0.3038 | 0.000000 | 0.000000 |
| reachability | canonical -> plan_front | 300 | 0.6267 | 0.5933 | 42 | 52 | -0.0333 | 0.8077 | 0.353328 | 1.000000 |
| reachability | canonical -> plan_back | 300 | 0.6267 | 0.5833 | 45 | 58 | -0.0433 | 0.7759 | 0.236902 | 1.000000 |
| reachability | canonical -> plan_scatter | 300 | 0.6267 | 0.5867 | 41 | 53 | -0.0400 | 0.7736 | 0.256442 | 1.000000 |
| executability | canonical -> disp_1 | 300 | 0.6333 | 0.6567 | 59 | 52 | 0.0233 | 1.1346 | 0.569220 | 1.000000 |
| executability | canonical -> disp_2 | 300 | 0.6333 | 0.6333 | 54 | 54 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| executability | canonical -> disp_3 | 300 | 0.6333 | 0.4667 | 27 | 77 | -0.1667 | 0.3506 | 0.000001 | 0.000006 |
| executability | canonical -> plan_front | 300 | 0.6333 | 0.6133 | 45 | 51 | -0.0200 | 0.8824 | 0.610068 | 1.000000 |
| executability | canonical -> plan_back | 300 | 0.6333 | 0.5867 | 46 | 60 | -0.0467 | 0.7667 | 0.206498 | 1.000000 |
| executability | canonical -> plan_scatter | 300 | 0.6333 | 0.6067 | 44 | 52 | -0.0267 | 0.8462 | 0.475152 | 1.000000 |
| non_executable_failure | canonical -> disp_1 | 300 | 0.3667 | 0.3433 | 52 | 59 | -0.0233 | 0.8814 | 0.569220 | 1.000000 |
| non_executable_failure | canonical -> disp_2 | 300 | 0.3667 | 0.3667 | 54 | 54 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| non_executable_failure | canonical -> disp_3 | 300 | 0.3667 | 0.5333 | 77 | 27 | 0.1667 | 2.8519 | 0.000001 | 0.000006 |
| non_executable_failure | canonical -> plan_front | 300 | 0.3667 | 0.3867 | 51 | 45 | 0.0200 | 1.1333 | 0.610068 | 1.000000 |
| non_executable_failure | canonical -> plan_back | 300 | 0.3667 | 0.4133 | 60 | 46 | 0.0467 | 1.3043 | 0.206498 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 300 | 0.3667 | 0.3933 | 52 | 44 | 0.0267 | 1.1818 | 0.475152 | 1.000000 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 190 | 197 | 0.9895 | 0.9797 | 188/2 | 193/4 | -0.0098 | 0.5133 | 0.685364 | 1.000000 |
| conditional_reachability | canonical -> disp_2 | 190 | 190 | 0.9895 | 0.9842 | 188/2 | 187/3 | -0.0053 | 0.6631 | 1.000000 | 1.000000 |
| conditional_reachability | canonical -> disp_3 | 190 | 140 | 0.9895 | 0.9500 | 188/2 | 133/7 | -0.0395 | 0.2021 | 0.039882 | 0.239292 |
| conditional_reachability | canonical -> plan_front | 190 | 184 | 0.9895 | 0.9674 | 188/2 | 178/6 | -0.0221 | 0.3156 | 0.168895 | 0.833913 |
| conditional_reachability | canonical -> plan_back | 190 | 176 | 0.9895 | 0.9943 | 188/2 | 175/1 | 0.0048 | 1.8617 | 1.000000 | 1.000000 |
| conditional_reachability | canonical -> plan_scatter | 190 | 182 | 0.9895 | 0.9670 | 188/2 | 176/6 | -0.0224 | 0.3121 | 0.166783 | 0.833913 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 136 | 20.2794 | 20.2941 | 0.0147 | 0.0007 | 0.0038 | 0.964544 | 0.982980 | 1.000000 |
| plan_length | canonical -> disp_2 | 133 | 20.8947 | 20.7068 | -0.1880 | -0.0090 | -0.0584 | 0.501932 | 0.535000 | 1.000000 |
| plan_length | canonical -> disp_3 | 109 | 18.8807 | 18.8807 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | canonical -> plan_front | 136 | 21.8824 | 21.2132 | -0.6691 | -0.0306 | -0.1877 | 0.030346 | 0.027670 | 0.166020 |
| plan_length | canonical -> plan_back | 130 | 20.4000 | 20.8077 | 0.4077 | 0.0200 | 0.1382 | 0.117662 | 0.125880 | 0.629400 |
| plan_length | canonical -> plan_scatter | 135 | 21.3556 | 21.7259 | 0.3704 | 0.0173 | 0.0859 | 0.319889 | 0.340440 | 1.000000 |
| optimality_ratio | canonical -> disp_1 | 136 | 1.1412 | 1.1285 | -0.0128 | -0.0112 | -0.0549 | 0.523080 | 0.537180 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 133 | 1.1361 | 1.1253 | -0.0108 | -0.0095 | -0.0584 | 0.501965 | 0.530210 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 109 | 1.1128 | 1.1046 | -0.0082 | -0.0074 | -0.0277 | 0.773109 | 0.779770 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 136 | 1.1305 | 1.0974 | -0.0332 | -0.0293 | -0.1635 | 0.058666 | 0.051060 | 0.306360 |
| optimality_ratio | canonical -> plan_back | 130 | 1.1304 | 1.1479 | 0.0175 | 0.0155 | 0.0974 | 0.268908 | 0.299840 | 1.000000 |
| optimality_ratio | canonical -> plan_scatter | 135 | 1.1224 | 1.1391 | 0.0167 | 0.0148 | 0.0628 | 0.466826 | 0.485840 | 1.000000 |
| first_failure_step | canonical -> disp_1 | 50 | 17.2200 | 21.0400 | 3.8200 | 0.2218 | 0.2332 | 0.105592 | 0.106980 | 0.534900 |
| first_failure_step | canonical -> disp_2 | 53 | 18.9811 | 17.1321 | -1.8491 | -0.0974 | -0.1173 | 0.397181 | 0.402930 | 1.000000 |
| first_failure_step | canonical -> disp_3 | 77 | 16.7273 | 13.0000 | -3.7273 | -0.2228 | -0.2817 | 0.015692 | 0.015670 | 0.094020 |
| first_failure_step | canonical -> plan_front | 64 | 16.2812 | 17.1562 | 0.8750 | 0.0537 | 0.0544 | 0.665021 | 0.672290 | 1.000000 |
| first_failure_step | canonical -> plan_back | 62 | 17.9194 | 15.7903 | -2.1290 | -0.1188 | -0.1299 | 0.310468 | 0.316130 | 1.000000 |
| first_failure_step | canonical -> plan_scatter | 61 | 16.5410 | 16.2131 | -0.3279 | -0.0198 | -0.0236 | 0.854673 | 0.863450 | 1.000000 |
| prompt_tokens | canonical -> disp_1 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_back | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> disp_1 | 300 | 13194.2267 | 12196.1500 | -998.0767 | -0.0756 | -0.2317 | 0.000076 | 0.000090 | 0.000450 |
| completion_tokens | canonical -> disp_2 | 300 | 13194.2267 | 12024.6133 | -1169.6133 | -0.0886 | -0.2514 | 0.000018 | 0.000020 | 0.000120 |
| completion_tokens | canonical -> disp_3 | 300 | 13194.2267 | 13863.2800 | 669.0533 | 0.0507 | 0.1434 | 0.013575 | 0.013270 | 0.053080 |
| completion_tokens | canonical -> plan_front | 300 | 13194.2267 | 12774.7433 | -419.4833 | -0.0318 | -0.0897 | 0.121212 | 0.122550 | 0.367650 |
| completion_tokens | canonical -> plan_back | 300 | 13194.2267 | 13115.2900 | -78.9367 | -0.0060 | -0.0164 | 0.777126 | 0.777130 | 1.000000 |
| completion_tokens | canonical -> plan_scatter | 300 | 13194.2267 | 13125.1800 | -69.0467 | -0.0052 | -0.0141 | 0.806874 | 0.807000 | 1.000000 |
| reasoning_completion_tokens | canonical -> disp_1 | 300 | 12623.0133 | 11624.7533 | -998.2600 | -0.0791 | -0.2331 | 0.000069 | 0.000080 | 0.000400 |
| reasoning_completion_tokens | canonical -> disp_2 | 300 | 12623.0133 | 11457.7333 | -1165.2800 | -0.0923 | -0.2516 | 0.000018 | 0.000020 | 0.000120 |
| reasoning_completion_tokens | canonical -> disp_3 | 300 | 12623.0133 | 13308.5400 | 685.5267 | 0.0543 | 0.1474 | 0.011170 | 0.010830 | 0.043320 |
| reasoning_completion_tokens | canonical -> plan_front | 300 | 12623.0133 | 12212.7633 | -410.2500 | -0.0325 | -0.0882 | 0.127492 | 0.128870 | 0.386610 |
| reasoning_completion_tokens | canonical -> plan_back | 300 | 12623.0133 | 12548.4067 | -74.6067 | -0.0059 | -0.0155 | 0.788329 | 0.788910 | 1.000000 |
| reasoning_completion_tokens | canonical -> plan_scatter | 300 | 12623.0133 | 12552.4300 | -70.5833 | -0.0056 | -0.0145 | 0.801685 | 0.802170 | 1.000000 |
| raw_completion_tokens | canonical -> disp_1 | 300 | 571.2133 | 571.3967 | 0.1833 | 0.0003 | 0.0017 | 0.976798 | 0.977300 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 300 | 571.2133 | 566.8800 | -4.3333 | -0.0076 | -0.0401 | 0.487576 | 0.491320 | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 300 | 571.2133 | 554.7400 | -16.4733 | -0.0288 | -0.1527 | 0.008606 | 0.008440 | 0.050640 |
| raw_completion_tokens | canonical -> plan_front | 300 | 571.2133 | 561.9800 | -9.2333 | -0.0162 | -0.0738 | 0.202270 | 0.207960 | 1.000000 |
| raw_completion_tokens | canonical -> plan_back | 300 | 571.2133 | 566.8833 | -4.3300 | -0.0076 | -0.0369 | 0.523341 | 0.530010 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 300 | 571.2133 | 572.7500 | 1.5367 | 0.0027 | 0.0125 | 0.828877 | 0.829100 | 1.000000 |
| total_tokens | canonical -> disp_1 | 300 | 23426.2767 | 22428.2000 | -998.0767 | -0.0426 | -0.2317 | 0.000076 | 0.000090 | 0.000450 |
| total_tokens | canonical -> disp_2 | 300 | 23426.2767 | 22256.6633 | -1169.6133 | -0.0499 | -0.2514 | 0.000018 | 0.000020 | 0.000120 |
| total_tokens | canonical -> disp_3 | 300 | 23426.2767 | 24095.3300 | 669.0533 | 0.0286 | 0.1434 | 0.013575 | 0.013270 | 0.053080 |
| total_tokens | canonical -> plan_front | 300 | 23426.2767 | 23006.7933 | -419.4833 | -0.0179 | -0.0897 | 0.121212 | 0.122550 | 0.367650 |
| total_tokens | canonical -> plan_back | 300 | 23426.2767 | 23347.3400 | -78.9367 | -0.0034 | -0.0164 | 0.777126 | 0.777130 | 1.000000 |
| total_tokens | canonical -> plan_scatter | 300 | 23426.2767 | 23357.2300 | -69.0467 | -0.0029 | -0.0141 | 0.806874 | 0.807000 | 1.000000 |
| duration_sec | canonical -> disp_1 | 300 | 112.7854 | 105.4029 | -7.3824 | -0.0655 | -0.1678 | 0.003938 | 0.003790 | 0.018950 |
| duration_sec | canonical -> disp_2 | 300 | 112.7854 | 101.4734 | -11.3120 | -0.1003 | -0.2577 | 0.000011 | 0.000010 | 0.000060 |
| duration_sec | canonical -> disp_3 | 300 | 112.7854 | 117.3112 | 4.5258 | 0.0401 | 0.1032 | 0.074865 | 0.073830 | 0.221490 |
| duration_sec | canonical -> plan_front | 300 | 112.7854 | 109.5795 | -3.2059 | -0.0284 | -0.0682 | 0.238737 | 0.238390 | 0.476780 |
| duration_sec | canonical -> plan_back | 300 | 112.7854 | 129.3625 | 16.5771 | 0.1470 | 0.1382 | 0.017270 | 0.006370 | 0.025480 |
| duration_sec | canonical -> plan_scatter | 300 | 112.7854 | 112.1437 | -0.6416 | -0.0057 | -0.0135 | 0.815922 | 0.816080 | 0.816080 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 20 | 0.6267 | 0.6433 | 0.0167 | [-0.0533, 0.0900] | 0.733398 |
| reachability | canonical -> disp_2 | 20 | 0.6267 | 0.6233 | -0.0033 | [-0.0733, 0.0733] | 1.000000 |
| reachability | canonical -> disp_3 | 20 | 0.6267 | 0.4433 | -0.1833 | [-0.2533, -0.1100] | 0.000275 |
| reachability | canonical -> plan_front | 20 | 0.6267 | 0.5933 | -0.0333 | [-0.1000, 0.0300] | 0.388062 |
| reachability | canonical -> plan_back | 20 | 0.6267 | 0.5833 | -0.0433 | [-0.1000, 0.0200] | 0.222168 |
| reachability | canonical -> plan_scatter | 20 | 0.6267 | 0.5867 | -0.0400 | [-0.1200, 0.0367] | 0.391968 |
| executability | canonical -> disp_1 | 20 | 0.6333 | 0.6567 | 0.0233 | [-0.0533, 0.1000] | 0.622925 |
| executability | canonical -> disp_2 | 20 | 0.6333 | 0.6333 | 0.0000 | [-0.0633, 0.0733] | 1.000000 |
| executability | canonical -> disp_3 | 20 | 0.6333 | 0.4667 | -0.1667 | [-0.2367, -0.0967] | 0.000610 |
| executability | canonical -> plan_front | 20 | 0.6333 | 0.6133 | -0.0200 | [-0.0800, 0.0400] | 0.600159 |
| executability | canonical -> plan_back | 20 | 0.6333 | 0.5867 | -0.0467 | [-0.1033, 0.0133] | 0.172852 |
| executability | canonical -> plan_scatter | 20 | 0.6333 | 0.6067 | -0.0267 | [-0.1067, 0.0500] | 0.577881 |
| non_executable_failure | canonical -> disp_1 | 20 | 0.3667 | 0.3433 | -0.0233 | [-0.1000, 0.0533] | 0.622925 |
| non_executable_failure | canonical -> disp_2 | 20 | 0.3667 | 0.3667 | 0.0000 | [-0.0733, 0.0633] | 1.000000 |
| non_executable_failure | canonical -> disp_3 | 20 | 0.3667 | 0.5333 | 0.1667 | [0.0967, 0.2367] | 0.000610 |
| non_executable_failure | canonical -> plan_front | 20 | 0.3667 | 0.3867 | 0.0200 | [-0.0400, 0.0800] | 0.600159 |
| non_executable_failure | canonical -> plan_back | 20 | 0.3667 | 0.4133 | 0.0467 | [-0.0133, 0.1033] | 0.172852 |
| non_executable_failure | canonical -> plan_scatter | 20 | 0.3667 | 0.3933 | 0.0267 | [-0.0500, 0.1067] | 0.577881 |
| conditional_reachability | canonical -> disp_1 | 20 | 0.9833 | 0.9767 | -0.0066 | [-0.0465, 0.0400] | 0.875000 |
| conditional_reachability | canonical -> disp_2 | 20 | 0.9833 | 0.9811 | -0.0023 | [-0.0243, 0.0230] | 1.000000 |
| conditional_reachability | canonical -> disp_3 | 19 | 0.9825 | 0.9249 | -0.0575 | [-0.0987, -0.0193] | 0.031250 |
| conditional_reachability | canonical -> plan_front | 20 | 0.9833 | 0.9645 | -0.0188 | [-0.0688, 0.0333] | 0.562500 |
| conditional_reachability | canonical -> plan_back | 20 | 0.9833 | 0.9833 | 0.0000 | [-0.0500, 0.0500] | 1.000000 |
| conditional_reachability | canonical -> plan_scatter | 20 | 0.9833 | 0.9430 | -0.0404 | [-0.1045, 0.0042] | 0.250000 |
| plan_length | canonical -> disp_1 | 20 | 29.9733 | 30.2434 | 0.2701 | [-0.4901, 1.0495] | 0.505798 |
| plan_length | canonical -> disp_2 | 20 | 29.9733 | 29.9124 | -0.0609 | [-0.7849, 0.6834] | 0.873474 |
| plan_length | canonical -> disp_3 | 19 | 29.1473 | 29.2132 | 0.0659 | [-0.7427, 0.9631] | 0.888794 |
| plan_length | canonical -> plan_front | 20 | 29.9733 | 29.7725 | -0.2008 | [-0.9742, 0.6306] | 0.635193 |
| plan_length | canonical -> plan_back | 20 | 29.9733 | 30.1819 | 0.2086 | [-0.7106, 1.1885] | 0.684296 |
| plan_length | canonical -> plan_scatter | 20 | 29.9733 | 30.2472 | 0.2739 | [-0.2769, 0.9079] | 0.409302 |
| optimality_ratio | canonical -> disp_1 | 20 | 1.1792 | 1.1789 | -0.0003 | [-0.0388, 0.0336] | 0.987442 |
| optimality_ratio | canonical -> disp_2 | 20 | 1.1792 | 1.1720 | -0.0072 | [-0.0402, 0.0250] | 0.678253 |
| optimality_ratio | canonical -> disp_3 | 19 | 1.1827 | 1.1819 | -0.0007 | [-0.0342, 0.0323] | 0.968689 |
| optimality_ratio | canonical -> plan_front | 20 | 1.1792 | 1.1637 | -0.0155 | [-0.0471, 0.0157] | 0.354980 |
| optimality_ratio | canonical -> plan_back | 20 | 1.1792 | 1.1816 | 0.0024 | [-0.0305, 0.0372] | 0.898041 |
| optimality_ratio | canonical -> plan_scatter | 20 | 1.1792 | 1.1842 | 0.0049 | [-0.0171, 0.0269] | 0.671112 |
| first_failure_step | canonical -> disp_1 | 13 | 15.6737 | 18.9462 | 3.2725 | [0.4661, 6.3654] | 0.060059 |
| first_failure_step | canonical -> disp_2 | 13 | 15.6737 | 15.6038 | -0.0699 | [-2.3646, 2.0826] | 0.952393 |
| first_failure_step | canonical -> disp_3 | 14 | 15.3704 | 13.3043 | -2.0661 | [-4.6750, 0.9303] | 0.186035 |
| first_failure_step | canonical -> plan_front | 15 | 15.4457 | 13.7224 | -1.7233 | [-4.0645, 0.6782] | 0.187805 |
| first_failure_step | canonical -> plan_back | 15 | 15.4457 | 13.5187 | -1.9270 | [-4.6432, 0.5332] | 0.186829 |
| first_failure_step | canonical -> plan_scatter | 14 | 15.3704 | 13.7682 | -1.6023 | [-4.0237, 0.6173] | 0.206787 |
| prompt_tokens | canonical -> disp_1 | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> plan_front | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> plan_back | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| completion_tokens | canonical -> disp_1 | 20 | 13194.2267 | 12196.1500 | -998.0767 | [-1539.1305, -488.0190] | 0.001125 |
| completion_tokens | canonical -> disp_2 | 20 | 13194.2267 | 12024.6133 | -1169.6133 | [-1757.5248, -619.1089] | 0.000458 |
| completion_tokens | canonical -> disp_3 | 20 | 13194.2267 | 13863.2800 | 669.0533 | [-24.1972, 1373.0960] | 0.076359 |
| completion_tokens | canonical -> plan_front | 20 | 13194.2267 | 12774.7433 | -419.4833 | [-1118.3350, 293.7450] | 0.272194 |
| completion_tokens | canonical -> plan_back | 20 | 13194.2267 | 13115.2900 | -78.9367 | [-784.8115, 582.4095] | 0.832716 |
| completion_tokens | canonical -> plan_scatter | 20 | 13194.2267 | 13125.1800 | -69.0467 | [-541.6707, 366.8735] | 0.775499 |
| reasoning_completion_tokens | canonical -> disp_1 | 20 | 12623.0133 | 11624.7533 | -998.2600 | [-1533.8032, -493.9331] | 0.001040 |
| reasoning_completion_tokens | canonical -> disp_2 | 20 | 12623.0133 | 11457.7333 | -1165.2800 | [-1748.7260, -614.3182] | 0.000452 |
| reasoning_completion_tokens | canonical -> disp_3 | 20 | 12623.0133 | 13308.5400 | 685.5267 | [-6.6323, 1387.5985] | 0.069330 |
| reasoning_completion_tokens | canonical -> plan_front | 20 | 12623.0133 | 12212.7633 | -410.2500 | [-1102.8846, 292.1844] | 0.275934 |
| reasoning_completion_tokens | canonical -> plan_back | 20 | 12623.0133 | 12548.4067 | -74.6067 | [-781.9740, 590.8915] | 0.841604 |
| reasoning_completion_tokens | canonical -> plan_scatter | 20 | 12623.0133 | 12552.4300 | -70.5833 | [-543.0490, 361.4376] | 0.770365 |
| raw_completion_tokens | canonical -> disp_1 | 20 | 571.2133 | 571.3967 | 0.1833 | [-21.5693, 17.9602] | 0.989418 |
| raw_completion_tokens | canonical -> disp_2 | 20 | 571.2133 | 566.8800 | -4.3333 | [-24.3102, 13.3937] | 0.686283 |
| raw_completion_tokens | canonical -> disp_3 | 20 | 571.2133 | 554.7400 | -16.4733 | [-27.8005, -5.1566] | 0.010941 |
| raw_completion_tokens | canonical -> plan_front | 20 | 571.2133 | 561.9800 | -9.2333 | [-26.6472, 9.0400] | 0.344376 |
| raw_completion_tokens | canonical -> plan_back | 20 | 571.2133 | 566.8833 | -4.3300 | [-16.6736, 8.5734] | 0.516373 |
| raw_completion_tokens | canonical -> plan_scatter | 20 | 571.2133 | 572.7500 | 1.5367 | [-12.8767, 15.8500] | 0.839737 |
| total_tokens | canonical -> disp_1 | 20 | 23426.2767 | 22428.2000 | -998.0767 | [-1539.1305, -488.0190] | 0.001125 |
| total_tokens | canonical -> disp_2 | 20 | 23426.2767 | 22256.6633 | -1169.6133 | [-1757.5247, -619.1089] | 0.000458 |
| total_tokens | canonical -> disp_3 | 20 | 23426.2767 | 24095.3300 | 669.0533 | [-24.1972, 1373.0960] | 0.076359 |
| total_tokens | canonical -> plan_front | 20 | 23426.2767 | 23006.7933 | -419.4833 | [-1118.3350, 293.7450] | 0.272194 |
| total_tokens | canonical -> plan_back | 20 | 23426.2767 | 23347.3400 | -78.9367 | [-784.8115, 582.4095] | 0.832716 |
| total_tokens | canonical -> plan_scatter | 20 | 23426.2767 | 23357.2300 | -69.0467 | [-541.6707, 366.8735] | 0.775499 |
| duration_sec | canonical -> disp_1 | 20 | 112.7854 | 105.4029 | -7.3824 | [-12.9268, -0.9320] | 0.030003 |
| duration_sec | canonical -> disp_2 | 20 | 112.7854 | 101.4734 | -11.3120 | [-15.9470, -6.5643] | 0.000221 |
| duration_sec | canonical -> disp_3 | 20 | 112.7854 | 117.3112 | 4.5258 | [-2.3845, 11.6097] | 0.231077 |
| duration_sec | canonical -> plan_front | 20 | 112.7854 | 109.5795 | -3.2059 | [-10.7827, 5.0186] | 0.447796 |
| duration_sec | canonical -> plan_back | 20 | 112.7854 | 129.3625 | 16.5771 | [-0.4972, 38.7005] | 0.136906 |
| duration_sec | canonical -> plan_scatter | 20 | 112.7854 | 112.1437 | -0.6416 | [-5.8589, 4.5749] | 0.817469 |
