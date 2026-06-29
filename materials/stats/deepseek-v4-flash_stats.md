# Statistical Tests: deepseek/deepseek-v4-flash

Baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_scatter`.
Extra comparisons: `plan_front` vs `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 300 | 0.6267 | 0.6433 | 57 | 52 | 0.0167 | 1.0962 | 0.701811 | 1.000000 |
| reachability | canonical -> disp_2 | 300 | 0.6267 | 0.6233 | 54 | 55 | -0.0033 | 0.9818 | 1.000000 | 1.000000 |
| reachability | canonical -> disp_3 | 300 | 0.6267 | 0.4433 | 24 | 79 | -0.1833 | 0.3038 | 0.000000 | 0.000000 |
| reachability | canonical -> plan_front | 300 | 0.6267 | 0.5933 | 42 | 52 | -0.0333 | 0.8077 | 0.353328 | 1.000000 |
| reachability | canonical -> plan_scatter | 300 | 0.6267 | 0.5867 | 41 | 53 | -0.0400 | 0.7736 | 0.256442 | 1.000000 |
| reachability | plan_front -> plan_scatter | 300 | 0.5933 | 0.5867 | 47 | 49 | -0.0067 | 0.9592 | 0.918778 | 0.918778 |
| executability | canonical -> disp_1 | 300 | 0.6333 | 0.6567 | 59 | 52 | 0.0233 | 1.1346 | 0.569220 | 1.000000 |
| executability | canonical -> disp_2 | 300 | 0.6333 | 0.6333 | 54 | 54 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| executability | canonical -> disp_3 | 300 | 0.6333 | 0.4667 | 27 | 77 | -0.1667 | 0.3506 | 0.000001 | 0.000005 |
| executability | canonical -> plan_front | 300 | 0.6333 | 0.6133 | 45 | 51 | -0.0200 | 0.8824 | 0.610068 | 1.000000 |
| executability | canonical -> plan_scatter | 300 | 0.6333 | 0.6067 | 44 | 52 | -0.0267 | 0.8462 | 0.475152 | 1.000000 |
| executability | plan_front -> plan_scatter | 300 | 0.6133 | 0.6067 | 46 | 48 | -0.0067 | 0.9583 | 0.917923 | 0.917923 |
| non_executable_failure | canonical -> disp_1 | 300 | 0.3667 | 0.3433 | 52 | 59 | -0.0233 | 0.8814 | 0.569220 | 1.000000 |
| non_executable_failure | canonical -> disp_2 | 300 | 0.3667 | 0.3667 | 54 | 54 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| non_executable_failure | canonical -> disp_3 | 300 | 0.3667 | 0.5333 | 77 | 27 | 0.1667 | 2.8519 | 0.000001 | 0.000005 |
| non_executable_failure | canonical -> plan_front | 300 | 0.3667 | 0.3867 | 51 | 45 | 0.0200 | 1.1333 | 0.610068 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 300 | 0.3667 | 0.3933 | 52 | 44 | 0.0267 | 1.1818 | 0.475152 | 1.000000 |
| non_executable_failure | plan_front -> plan_scatter | 300 | 0.3867 | 0.3933 | 48 | 46 | 0.0067 | 1.0435 | 0.917923 | 0.917923 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 190 | 197 | 0.9895 | 0.9797 | 188/2 | 193/4 | -0.0098 | 0.5133 | 0.685364 | 1.000000 |
| conditional_reachability | canonical -> disp_2 | 190 | 190 | 0.9895 | 0.9842 | 188/2 | 187/3 | -0.0053 | 0.6631 | 1.000000 | 1.000000 |
| conditional_reachability | canonical -> disp_3 | 190 | 140 | 0.9895 | 0.9500 | 188/2 | 133/7 | -0.0395 | 0.2021 | 0.039882 | 0.199410 |
| conditional_reachability | canonical -> plan_front | 190 | 184 | 0.9895 | 0.9674 | 188/2 | 178/6 | -0.0221 | 0.3156 | 0.168895 | 0.667131 |
| conditional_reachability | canonical -> plan_scatter | 190 | 182 | 0.9895 | 0.9670 | 188/2 | 176/6 | -0.0224 | 0.3121 | 0.166783 | 0.667131 |
| conditional_reachability | plan_front -> plan_scatter | 184 | 182 | 0.9674 | 0.9670 | 178/6 | 176/6 | -0.0004 | 0.9888 | 1.000000 | 1.000000 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 136 | 20.2794 | 20.2941 | 0.0147 | 0.0007 | 0.0038 | 0.964544 | 0.982980 | 1.000000 |
| plan_length | canonical -> disp_2 | 133 | 20.8947 | 20.7068 | -0.1880 | -0.0090 | -0.0584 | 0.501932 | 0.535000 | 1.000000 |
| plan_length | canonical -> disp_3 | 109 | 18.8807 | 18.8807 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | canonical -> plan_front | 136 | 21.8824 | 21.2132 | -0.6691 | -0.0306 | -0.1877 | 0.030346 | 0.027670 | 0.138350 |
| plan_length | canonical -> plan_scatter | 135 | 21.3556 | 21.7259 | 0.3704 | 0.0173 | 0.0859 | 0.319889 | 0.340440 | 1.000000 |
| plan_length | plan_front -> plan_scatter | 129 | 20.1783 | 20.8062 | 0.6279 | 0.0311 | 0.1699 | 0.055847 | 0.056860 | 0.056860 |
| optimality_ratio | canonical -> disp_1 | 136 | 1.1412 | 1.1285 | -0.0128 | -0.0112 | -0.0549 | 0.523080 | 0.537180 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 133 | 1.1361 | 1.1253 | -0.0108 | -0.0095 | -0.0584 | 0.501965 | 0.530210 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 109 | 1.1128 | 1.1046 | -0.0082 | -0.0074 | -0.0277 | 0.773109 | 0.779770 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 136 | 1.1305 | 1.0974 | -0.0332 | -0.0293 | -0.1635 | 0.058666 | 0.051060 | 0.255300 |
| optimality_ratio | canonical -> plan_scatter | 135 | 1.1224 | 1.1391 | 0.0167 | 0.0148 | 0.0628 | 0.466826 | 0.485840 | 1.000000 |
| optimality_ratio | plan_front -> plan_scatter | 129 | 1.0995 | 1.1293 | 0.0299 | 0.0272 | 0.1461 | 0.099391 | 0.102560 | 0.102560 |
| first_failure_step | canonical -> disp_1 | 50 | 17.2200 | 21.0400 | 3.8200 | 0.2218 | 0.2332 | 0.105592 | 0.106980 | 0.427920 |
| first_failure_step | canonical -> disp_2 | 53 | 18.9811 | 17.1321 | -1.8491 | -0.0974 | -0.1173 | 0.397181 | 0.402930 | 1.000000 |
| first_failure_step | canonical -> disp_3 | 77 | 16.7273 | 13.0000 | -3.7273 | -0.2228 | -0.2817 | 0.015692 | 0.015670 | 0.078350 |
| first_failure_step | canonical -> plan_front | 64 | 16.2812 | 17.1562 | 0.8750 | 0.0537 | 0.0544 | 0.665021 | 0.672290 | 1.000000 |
| first_failure_step | canonical -> plan_scatter | 61 | 16.5410 | 16.2131 | -0.3279 | -0.0198 | -0.0236 | 0.854673 | 0.863450 | 1.000000 |
| first_failure_step | plan_front -> plan_scatter | 67 | 15.9403 | 15.4776 | -0.4627 | -0.0290 | -0.0355 | 0.772434 | 0.780950 | 0.780950 |
| prompt_tokens | canonical -> disp_1 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> disp_1 | 300 | 13194.2267 | 12196.1500 | -998.0767 | -0.0756 | -0.2317 | 0.000076 | 0.000090 | 0.000360 |
| completion_tokens | canonical -> disp_2 | 300 | 13194.2267 | 12024.6133 | -1169.6133 | -0.0886 | -0.2514 | 0.000018 | 0.000020 | 0.000100 |
| completion_tokens | canonical -> disp_3 | 300 | 13194.2267 | 13863.2800 | 669.0533 | 0.0507 | 0.1434 | 0.013575 | 0.013270 | 0.039810 |
| completion_tokens | canonical -> plan_front | 300 | 13194.2267 | 12774.7433 | -419.4833 | -0.0318 | -0.0897 | 0.121212 | 0.122550 | 0.245100 |
| completion_tokens | canonical -> plan_scatter | 300 | 13194.2267 | 13125.1800 | -69.0467 | -0.0052 | -0.0141 | 0.806874 | 0.807000 | 0.807000 |
| completion_tokens | plan_front -> plan_scatter | 300 | 12774.7433 | 13125.1800 | 350.4367 | 0.0274 | 0.0687 | 0.235348 | 0.235600 | 0.235600 |
| reasoning_completion_tokens | canonical -> disp_1 | 300 | 12623.0133 | 11624.7533 | -998.2600 | -0.0791 | -0.2331 | 0.000069 | 0.000080 | 0.000320 |
| reasoning_completion_tokens | canonical -> disp_2 | 300 | 12623.0133 | 11457.7333 | -1165.2800 | -0.0923 | -0.2516 | 0.000018 | 0.000020 | 0.000100 |
| reasoning_completion_tokens | canonical -> disp_3 | 300 | 12623.0133 | 13308.5400 | 685.5267 | 0.0543 | 0.1474 | 0.011170 | 0.010830 | 0.032490 |
| reasoning_completion_tokens | canonical -> plan_front | 300 | 12623.0133 | 12212.7633 | -410.2500 | -0.0325 | -0.0882 | 0.127492 | 0.128870 | 0.257740 |
| reasoning_completion_tokens | canonical -> plan_scatter | 300 | 12623.0133 | 12552.4300 | -70.5833 | -0.0056 | -0.0145 | 0.801685 | 0.802170 | 0.802170 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 300 | 12212.7633 | 12552.4300 | 339.6667 | 0.0278 | 0.0668 | 0.248222 | 0.249350 | 0.249350 |
| raw_completion_tokens | canonical -> disp_1 | 300 | 571.2133 | 571.3967 | 0.1833 | 0.0003 | 0.0017 | 0.976798 | 0.977300 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 300 | 571.2133 | 566.8800 | -4.3333 | -0.0076 | -0.0401 | 0.487576 | 0.491320 | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 300 | 571.2133 | 554.7400 | -16.4733 | -0.0288 | -0.1527 | 0.008606 | 0.008440 | 0.042200 |
| raw_completion_tokens | canonical -> plan_front | 300 | 571.2133 | 561.9800 | -9.2333 | -0.0162 | -0.0738 | 0.202270 | 0.207960 | 0.831840 |
| raw_completion_tokens | canonical -> plan_scatter | 300 | 571.2133 | 572.7500 | 1.5367 | 0.0027 | 0.0125 | 0.828877 | 0.829100 | 1.000000 |
| raw_completion_tokens | plan_front -> plan_scatter | 300 | 561.9800 | 572.7500 | 10.7700 | 0.0192 | 0.0838 | 0.147654 | 0.149740 | 0.149740 |
| total_tokens | canonical -> disp_1 | 300 | 23426.2767 | 22428.2000 | -998.0767 | -0.0426 | -0.2317 | 0.000076 | 0.000090 | 0.000360 |
| total_tokens | canonical -> disp_2 | 300 | 23426.2767 | 22256.6633 | -1169.6133 | -0.0499 | -0.2514 | 0.000018 | 0.000020 | 0.000100 |
| total_tokens | canonical -> disp_3 | 300 | 23426.2767 | 24095.3300 | 669.0533 | 0.0286 | 0.1434 | 0.013575 | 0.013270 | 0.039810 |
| total_tokens | canonical -> plan_front | 300 | 23426.2767 | 23006.7933 | -419.4833 | -0.0179 | -0.0897 | 0.121212 | 0.122550 | 0.245100 |
| total_tokens | canonical -> plan_scatter | 300 | 23426.2767 | 23357.2300 | -69.0467 | -0.0029 | -0.0141 | 0.806874 | 0.807000 | 0.807000 |
| total_tokens | plan_front -> plan_scatter | 300 | 23006.7933 | 23357.2300 | 350.4367 | 0.0152 | 0.0687 | 0.235348 | 0.235600 | 0.235600 |
| duration_sec | canonical -> disp_1 | 300 | 112.7854 | 105.4029 | -7.3824 | -0.0655 | -0.1678 | 0.003938 | 0.003790 | 0.015160 |
| duration_sec | canonical -> disp_2 | 300 | 112.7854 | 101.4734 | -11.3120 | -0.1003 | -0.2577 | 0.000011 | 0.000010 | 0.000050 |
| duration_sec | canonical -> disp_3 | 300 | 112.7854 | 117.3112 | 4.5258 | 0.0401 | 0.1032 | 0.074865 | 0.073830 | 0.221490 |
| duration_sec | canonical -> plan_front | 300 | 112.7854 | 109.5795 | -3.2059 | -0.0284 | -0.0682 | 0.238737 | 0.238390 | 0.476780 |
| duration_sec | canonical -> plan_scatter | 300 | 112.7854 | 112.1437 | -0.6416 | -0.0057 | -0.0135 | 0.815922 | 0.816080 | 0.816080 |
| duration_sec | plan_front -> plan_scatter | 300 | 109.5795 | 112.1437 | 2.5642 | 0.0234 | 0.0531 | 0.358842 | 0.356900 | 0.356900 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> plan_scatter | 20 | 0.5933 | 0.5867 | -0.0067 | [-0.0733, 0.0533] | 0.922363 |
| executability | plan_front -> plan_scatter | 20 | 0.6133 | 0.6067 | -0.0067 | [-0.0733, 0.0533] | 0.922852 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.3867 | 0.3933 | 0.0067 | [-0.0533, 0.0733] | 0.922852 |
| conditional_reachability | plan_front -> plan_scatter | 20 | 0.9645 | 0.9430 | -0.0215 | [-0.0877, 0.0291] | 0.593750 |
| plan_length | plan_front -> plan_scatter | 20 | 29.7725 | 30.2472 | 0.4747 | [-0.1561, 1.0839] | 0.160034 |
| optimality_ratio | plan_front -> plan_scatter | 20 | 1.1637 | 1.1842 | 0.0205 | [-0.0008, 0.0422] | 0.084015 |
| first_failure_step | plan_front -> plan_scatter | 15 | 15.0558 | 13.8408 | -1.2150 | [-4.5579, 1.6065] | 0.507263 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| completion_tokens | plan_front -> plan_scatter | 20 | 12774.7433 | 13125.1800 | 350.4367 | [-518.6958, 1166.6555] | 0.442095 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 12212.7633 | 12552.4300 | 339.6667 | [-528.3967, 1153.8208] | 0.454939 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 561.9800 | 572.7500 | 10.7700 | [-3.5169, 24.6502] | 0.159943 |
| total_tokens | plan_front -> plan_scatter | 20 | 23006.7933 | 23357.2300 | 350.4367 | [-518.6958, 1166.6555] | 0.442095 |
| duration_sec | plan_front -> plan_scatter | 20 | 109.5795 | 112.1437 | 2.5642 | [-5.4949, 10.3186] | 0.542824 |
