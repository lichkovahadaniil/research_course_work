# Statistical Tests: nemotron-3-super

Baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_scatter`.
Extra comparisons: `plan_front` vs `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 170 | 0.1941 | 0.2059 | 17 | 15 | 0.0118 | 1.1333 | 0.860050 | 1.000000 |
| reachability | canonical -> disp_2 | 170 | 0.1941 | 0.2176 | 16 | 12 | 0.0235 | 1.3333 | 0.571588 | 1.000000 |
| reachability | canonical -> disp_3 | 170 | 0.1941 | 0.1529 | 13 | 20 | -0.0412 | 0.6500 | 0.296206 | 1.000000 |
| reachability | canonical -> plan_front | 170 | 0.1882 | 0.3235 | 33 | 10 | 0.1353 | 3.3000 | 0.000606 | 0.003031 |
| reachability | canonical -> plan_scatter | 168 | 0.1905 | 0.2083 | 17 | 14 | 0.0179 | 1.2143 | 0.720100 | 1.000000 |
| reachability | plan_front -> plan_scatter | 169 | 0.3195 | 0.2071 | 12 | 31 | -0.1124 | 0.3871 | 0.005402 | 0.005402 |
| executability | canonical -> disp_1 | 170 | 0.6471 | 0.6235 | 36 | 40 | -0.0235 | 0.9000 | 0.731009 | 1.000000 |
| executability | canonical -> disp_2 | 170 | 0.6471 | 0.6176 | 31 | 36 | -0.0294 | 0.8611 | 0.625407 | 1.000000 |
| executability | canonical -> disp_3 | 170 | 0.6471 | 0.5882 | 34 | 44 | -0.0588 | 0.7727 | 0.308168 | 1.000000 |
| executability | canonical -> plan_front | 170 | 0.6412 | 0.7000 | 43 | 33 | 0.0588 | 1.3030 | 0.301872 | 1.000000 |
| executability | canonical -> plan_scatter | 168 | 0.6488 | 0.5833 | 29 | 40 | -0.0655 | 0.7250 | 0.228400 | 1.000000 |
| executability | plan_front -> plan_scatter | 169 | 0.6982 | 0.5799 | 33 | 53 | -0.1183 | 0.6226 | 0.039854 | 0.039854 |
| non_executable_failure | canonical -> disp_1 | 170 | 0.3529 | 0.3765 | 40 | 36 | 0.0235 | 1.1111 | 0.731009 | 1.000000 |
| non_executable_failure | canonical -> disp_2 | 170 | 0.3529 | 0.3824 | 36 | 31 | 0.0294 | 1.1613 | 0.625407 | 1.000000 |
| non_executable_failure | canonical -> disp_3 | 170 | 0.3529 | 0.4118 | 44 | 34 | 0.0588 | 1.2941 | 0.308168 | 1.000000 |
| non_executable_failure | canonical -> plan_front | 170 | 0.3588 | 0.3000 | 33 | 43 | -0.0588 | 0.7674 | 0.301872 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 168 | 0.3512 | 0.4167 | 40 | 29 | 0.0655 | 1.3793 | 0.228400 | 1.000000 |
| non_executable_failure | plan_front -> plan_scatter | 169 | 0.3018 | 0.4201 | 53 | 33 | 0.1183 | 1.6061 | 0.039854 | 0.039854 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 110 | 108 | 0.3000 | 0.3426 | 33/77 | 37/71 | 0.0426 | 1.2160 | 0.562418 | 1.000000 |
| conditional_reachability | canonical -> disp_2 | 110 | 107 | 0.3000 | 0.3645 | 33/77 | 39/68 | 0.0645 | 1.3382 | 0.387056 | 1.000000 |
| conditional_reachability | canonical -> disp_3 | 110 | 100 | 0.3000 | 0.2600 | 33/77 | 26/74 | -0.0400 | 0.8198 | 0.542141 | 1.000000 |
| conditional_reachability | canonical -> plan_front | 110 | 120 | 0.3000 | 0.4667 | 33/77 | 56/64 | 0.1667 | 2.0417 | 0.010353 | 0.051765 |
| conditional_reachability | canonical -> plan_scatter | 110 | 99 | 0.3000 | 0.3636 | 33/77 | 36/63 | 0.0636 | 1.3333 | 0.377546 | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 120 | 99 | 0.4667 | 0.3636 | 56/64 | 36/63 | -0.1030 | 0.6531 | 0.132562 | 0.132562 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 18 | 9.5000 | 8.3333 | -1.1667 | -0.1228 | -0.2357 | 0.331333 | 1.000000 | 1.000000 |
| plan_length | canonical -> disp_2 | 21 | 9.8571 | 8.7143 | -1.1429 | -0.1159 | -0.2498 | 0.265805 | 0.250000 | 1.000000 |
| plan_length | canonical -> disp_3 | 13 | 7.5385 | 7.4615 | -0.0769 | -0.0102 | -0.2774 | 0.337049 | 1.000000 | 1.000000 |
| plan_length | canonical -> plan_front | 22 | 9.7273 | 9.0455 | -0.6818 | -0.0701 | -0.1446 | 0.504973 | 1.000000 | 1.000000 |
| plan_length | canonical -> plan_scatter | 18 | 8.2778 | 8.0000 | -0.2778 | -0.0336 | -0.2899 | 0.235514 | 0.500000 | 1.000000 |
| plan_length | plan_front -> plan_scatter | 23 | 9.3478 | 9.1304 | -0.2174 | -0.0233 | -0.2556 | 0.233212 | 0.500000 | 0.500000 |
| optimality_ratio | canonical -> disp_1 | 18 | 1.0778 | 1.0000 | -0.0778 | -0.0722 | -0.2357 | 0.331333 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 21 | 1.0856 | 1.0068 | -0.0788 | -0.0726 | -0.2581 | 0.250786 | 0.250000 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 13 | 1.0085 | 1.0000 | -0.0085 | -0.0085 | -0.2774 | 0.337049 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 22 | 1.0684 | 1.0191 | -0.0493 | -0.0461 | -0.1594 | 0.462843 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> plan_scatter | 18 | 1.0220 | 1.0000 | -0.0220 | -0.0216 | -0.3114 | 0.204019 | 0.500000 | 1.000000 |
| optimality_ratio | plan_front -> plan_scatter | 23 | 1.0314 | 1.0164 | -0.0150 | -0.0145 | -0.2485 | 0.246015 | 0.500000 | 0.500000 |
| first_failure_step | canonical -> disp_1 | 1 | 4.0000 | 6.0000 | 2.0000 | 0.5000 | NA | NA | 1.000000 | 1.000000 |
| first_failure_step | canonical -> disp_2 | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | canonical -> disp_3 | 2 | 17.0000 | 4.0000 | -13.0000 | -0.7647 | -0.7071 | 0.500000 | 1.000000 | 1.000000 |
| first_failure_step | canonical -> plan_front | 1 | 3.0000 | 4.0000 | 1.0000 | 0.3333 | NA | NA | 1.000000 | 1.000000 |
| first_failure_step | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | plan_front -> plan_scatter | 2 | 40.0000 | 1.0000 | -39.0000 | -0.9750 | -1.9698 | 0.219409 | 0.500000 | 0.500000 |
| prompt_tokens | canonical -> disp_1 | 170 | 9988.0941 | 10117.6118 | 129.5176 | 0.0130 | 0.1099 | 0.153864 | 0.155090 | 0.775450 |
| prompt_tokens | canonical -> disp_2 | 170 | 9988.0941 | 9897.2529 | -90.8412 | -0.0091 | -0.0790 | 0.304291 | 0.303780 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 170 | 9988.0941 | 10029.7118 | 41.6176 | 0.0042 | 0.0343 | 0.655241 | 0.652270 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 170 | 9988.0941 | 9950.8529 | -37.2412 | -0.0037 | -0.0311 | 0.685887 | 0.689490 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 168 | 10008.6905 | 9905.0893 | -103.6012 | -0.0104 | -0.0878 | 0.256993 | 0.259200 | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 169 | 9960.8698 | 9895.3432 | -65.5266 | -0.0066 | -0.0575 | 0.455560 | 0.457930 | 0.457930 |
| completion_tokens | canonical -> disp_1 | 170 | 26458.4353 | 25303.9765 | -1154.4588 | -0.0436 | -0.0440 | 0.566703 | 0.566190 | 0.924900 |
| completion_tokens | canonical -> disp_2 | 170 | 26460.4529 | 23741.2176 | -2719.2353 | -0.1028 | -0.1005 | 0.192071 | 0.191860 | 0.767440 |
| completion_tokens | canonical -> disp_3 | 170 | 26460.4529 | 24690.2000 | -1770.2529 | -0.0669 | -0.0570 | 0.458130 | 0.456950 | 0.924900 |
| completion_tokens | canonical -> plan_front | 170 | 26460.3882 | 24171.4941 | -2288.8941 | -0.0865 | -0.0782 | 0.309529 | 0.308300 | 0.924900 |
| completion_tokens | canonical -> plan_scatter | 168 | 26771.6250 | 22534.9464 | -4236.6786 | -0.1583 | -0.1446 | 0.062685 | 0.061490 | 0.307450 |
| completion_tokens | plan_front -> plan_scatter | 169 | 24313.5976 | 22402.4852 | -1911.1124 | -0.0786 | -0.0763 | 0.322368 | 0.320000 | 0.320000 |
| reasoning_completion_tokens | canonical -> disp_1 | 170 | 26055.3824 | 24910.3765 | -1145.0059 | -0.0439 | -0.0438 | 0.568515 | 0.568360 | 0.913740 |
| reasoning_completion_tokens | canonical -> disp_2 | 170 | 26057.4000 | 23379.5647 | -2677.8353 | -0.1028 | -0.1006 | 0.191372 | 0.190650 | 0.762600 |
| reasoning_completion_tokens | canonical -> disp_3 | 170 | 26057.4000 | 24295.2706 | -1762.1294 | -0.0676 | -0.0571 | 0.457321 | 0.456870 | 0.913740 |
| reasoning_completion_tokens | canonical -> plan_front | 170 | 26057.3353 | 23282.1765 | -2775.1588 | -0.1065 | -0.0931 | 0.226445 | 0.228870 | 0.762600 |
| reasoning_completion_tokens | canonical -> plan_scatter | 168 | 26363.7738 | 22044.9464 | -4318.8274 | -0.1638 | -0.1495 | 0.054273 | 0.055040 | 0.275200 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 169 | 23419.0178 | 21915.3846 | -1503.6331 | -0.0642 | -0.0615 | 0.425494 | 0.428330 | 0.428330 |
| raw_completion_tokens | canonical -> disp_1 | 170 | 403.0529 | 393.6000 | -9.4529 | -0.0235 | -0.0041 | 0.957019 | 0.945150 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 170 | 403.0529 | 361.6529 | -41.4000 | -0.1027 | -0.0182 | 0.812479 | 0.794570 | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 170 | 403.0529 | 394.9294 | -8.1235 | -0.0202 | -0.0040 | 0.958760 | 0.978230 | 1.000000 |
| raw_completion_tokens | canonical -> plan_front | 170 | 403.0529 | 889.3176 | 486.2647 | 1.2065 | 0.0821 | 0.285982 | 0.341130 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 168 | 407.8512 | 490.0000 | 82.1488 | 0.2014 | 0.0376 | 0.627004 | 0.711540 | 1.000000 |
| raw_completion_tokens | plan_front -> plan_scatter | 169 | 894.5799 | 487.1006 | -407.4793 | -0.4555 | -0.0707 | 0.359304 | 0.485760 | 0.485760 |
| total_tokens | canonical -> disp_1 | 170 | 36135.8412 | 35076.3824 | -1059.4588 | -0.0293 | -0.0400 | 0.602304 | 0.604280 | 0.774820 |
| total_tokens | canonical -> disp_2 | 170 | 36137.8588 | 33326.9471 | -2810.9118 | -0.0778 | -0.1018 | 0.186293 | 0.185790 | 0.743160 |
| total_tokens | canonical -> disp_3 | 170 | 36137.8588 | 34026.6647 | -2111.1941 | -0.0584 | -0.0667 | 0.385754 | 0.387410 | 0.774820 |
| total_tokens | canonical -> plan_front | 170 | 36137.7941 | 33293.5588 | -2844.2353 | -0.0787 | -0.0964 | 0.210734 | 0.211270 | 0.743160 |
| total_tokens | canonical -> plan_scatter | 168 | 36465.9286 | 31594.6190 | -4871.3095 | -0.1336 | -0.1637 | 0.035276 | 0.035190 | 0.175950 |
| total_tokens | plan_front -> plan_scatter | 169 | 33440.7751 | 31457.4142 | -1983.3609 | -0.0593 | -0.0771 | 0.317795 | 0.318200 | 0.318200 |
| duration_sec | canonical -> disp_1 | 170 | 494.6782 | 546.3344 | 51.6562 | 0.1044 | 0.0998 | 0.194816 | 0.200420 | 0.601260 |
| duration_sec | canonical -> disp_2 | 170 | 495.4661 | 472.7988 | -22.6673 | -0.0457 | -0.0479 | 0.533105 | 0.535160 | 0.601260 |
| duration_sec | canonical -> disp_3 | 170 | 495.4661 | 588.0383 | 92.5722 | 0.1868 | 0.1560 | 0.043507 | 0.042320 | 0.211600 |
| duration_sec | canonical -> plan_front | 170 | 495.7771 | 594.5331 | 98.7559 | 0.1992 | 0.1529 | 0.047749 | 0.048190 | 0.211600 |
| duration_sec | canonical -> plan_scatter | 168 | 498.1240 | 552.9859 | 54.8619 | 0.1101 | 0.0854 | 0.269980 | 0.271640 | 0.601260 |
| duration_sec | plan_front -> plan_scatter | 169 | 596.9032 | 551.2667 | -45.6364 | -0.0765 | -0.0738 | 0.338504 | 0.341970 | 0.341970 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> plan_scatter | 20 | 0.2832 | 0.1907 | -0.0925 | [-0.1913, -0.0038] | 0.092285 |
| executability | plan_front -> plan_scatter | 20 | 0.6803 | 0.5811 | -0.0993 | [-0.2039, 0.0016] | 0.094208 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.3197 | 0.4189 | 0.0993 | [-0.0016, 0.2039] | 0.094208 |
| conditional_reachability | plan_front -> plan_scatter | 20 | 0.3387 | 0.2917 | -0.0471 | [-0.1627, 0.0596] | 0.458008 |
| plan_length | plan_front -> plan_scatter | 8 | 16.2292 | 15.5833 | -0.6458 | [-1.6458, -0.0625] | 0.250000 |
| optimality_ratio | plan_front -> plan_scatter | 8 | 1.1021 | 1.0604 | -0.0418 | [-0.1132, -0.0024] | 0.250000 |
| first_failure_step | plan_front -> plan_scatter | 5 | 22.8667 | 6.9000 | -15.9667 | [-27.6333, -4.3000] | 0.250000 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 10025.2282 | 9960.1905 | -65.0377 | [-285.7200, 142.2498] | 0.575851 |
| completion_tokens | plan_front -> plan_scatter | 20 | 25302.2250 | 23337.0375 | -1965.1874 | [-5368.4876, 1353.3628] | 0.281710 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 24359.5008 | 22822.0355 | -1537.4653 | [-4977.4576, 1721.2852] | 0.399151 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 942.7242 | 515.0020 | -427.7222 | [-1379.9781, 286.7888] | 0.469955 |
| total_tokens | plan_front -> plan_scatter | 20 | 34446.8657 | 32409.5406 | -2037.3251 | [-5874.6536, 1756.1443] | 0.331163 |
| duration_sec | plan_front -> plan_scatter | 20 | 627.4491 | 575.7516 | -51.6975 | [-140.6180, 47.6185] | 0.310873 |
