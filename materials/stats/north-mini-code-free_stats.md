# Statistical Tests: cohere/north-mini-code:free

Baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_scatter`.
Extra comparisons: `plan_front` vs `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 299 | 0.1204 | 0.1237 | 19 | 18 | 0.0033 | 1.0556 | 1.000000 | 1.000000 |
| reachability | canonical -> disp_2 | 299 | 0.1204 | 0.1171 | 18 | 19 | -0.0033 | 0.9474 | 1.000000 | 1.000000 |
| reachability | canonical -> disp_3 | 299 | 0.1204 | 0.1505 | 24 | 15 | 0.0301 | 1.6000 | 0.199591 | 0.798363 |
| reachability | canonical -> plan_front | 299 | 0.1204 | 0.1639 | 27 | 14 | 0.0435 | 1.9286 | 0.059584 | 0.297919 |
| reachability | canonical -> plan_scatter | 299 | 0.1204 | 0.1237 | 18 | 17 | 0.0033 | 1.0588 | 1.000000 | 1.000000 |
| reachability | plan_front -> plan_scatter | 300 | 0.1667 | 0.1267 | 14 | 26 | -0.0400 | 0.5385 | 0.080690 | 0.080690 |
| executability | canonical -> disp_1 | 299 | 0.5920 | 0.6856 | 78 | 50 | 0.0936 | 1.5600 | 0.016671 | 0.066683 |
| executability | canonical -> disp_2 | 299 | 0.5920 | 0.6656 | 81 | 59 | 0.0736 | 1.3729 | 0.075551 | 0.226652 |
| executability | canonical -> disp_3 | 299 | 0.5920 | 0.7023 | 75 | 42 | 0.1104 | 1.7857 | 0.002928 | 0.014641 |
| executability | canonical -> plan_front | 299 | 0.5920 | 0.6421 | 74 | 59 | 0.0502 | 1.2542 | 0.224630 | 0.226652 |
| executability | canonical -> plan_scatter | 299 | 0.5920 | 0.6589 | 80 | 60 | 0.0669 | 1.3333 | 0.107988 | 0.226652 |
| executability | plan_front -> plan_scatter | 300 | 0.6433 | 0.6600 | 71 | 66 | 0.0167 | 1.0758 | 0.732684 | 0.732684 |
| non_executable_failure | canonical -> disp_1 | 299 | 0.4080 | 0.3144 | 50 | 78 | -0.0936 | 0.6410 | 0.016671 | 0.066683 |
| non_executable_failure | canonical -> disp_2 | 299 | 0.4080 | 0.3344 | 59 | 81 | -0.0736 | 0.7284 | 0.075551 | 0.226652 |
| non_executable_failure | canonical -> disp_3 | 299 | 0.4080 | 0.2977 | 42 | 75 | -0.1104 | 0.5600 | 0.002928 | 0.014641 |
| non_executable_failure | canonical -> plan_front | 299 | 0.4080 | 0.3579 | 59 | 74 | -0.0502 | 0.7973 | 0.224630 | 0.226652 |
| non_executable_failure | canonical -> plan_scatter | 299 | 0.4080 | 0.3411 | 60 | 80 | -0.0669 | 0.7500 | 0.107988 | 0.226652 |
| non_executable_failure | plan_front -> plan_scatter | 300 | 0.3567 | 0.3400 | 66 | 71 | -0.0167 | 0.9296 | 0.732684 | 0.732684 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 177 | 206 | 0.2034 | 0.1845 | 36/141 | 38/168 | -0.0189 | 0.8859 | 0.697479 | 1.000000 |
| conditional_reachability | canonical -> disp_2 | 177 | 199 | 0.2034 | 0.1759 | 36/141 | 35/164 | -0.0275 | 0.8359 | 0.511892 | 1.000000 |
| conditional_reachability | canonical -> disp_3 | 177 | 211 | 0.2034 | 0.2133 | 36/141 | 45/166 | 0.0099 | 1.0617 | 0.900294 | 1.000000 |
| conditional_reachability | canonical -> plan_front | 177 | 193 | 0.2034 | 0.2591 | 36/141 | 50/143 | 0.0557 | 1.3695 | 0.219688 | 1.000000 |
| conditional_reachability | canonical -> plan_scatter | 177 | 198 | 0.2034 | 0.1919 | 36/141 | 38/160 | -0.0115 | 0.9302 | 0.796207 | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 193 | 198 | 0.2591 | 0.1919 | 50/143 | 38/160 | -0.0671 | 0.6793 | 0.117132 | 0.117132 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 18 | 7.4444 | 7.4444 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| plan_length | canonical -> disp_2 | 17 | 9.7647 | 9.3529 | -0.4118 | -0.0422 | -0.3223 | 0.202548 | 0.500000 | 1.000000 |
| plan_length | canonical -> disp_3 | 21 | 10.4286 | 9.7619 | -0.6667 | -0.0639 | -0.3002 | 0.184200 | 0.250000 | 1.000000 |
| plan_length | canonical -> plan_front | 22 | 9.4091 | 8.3636 | -1.0455 | -0.1111 | -0.2132 | 0.328695 | 1.000000 | 1.000000 |
| plan_length | canonical -> plan_scatter | 19 | 7.8421 | 7.8947 | 0.0526 | 0.0067 | 0.2294 | 0.330565 | 1.000000 | 1.000000 |
| plan_length | plan_front -> plan_scatter | 24 | 8.0000 | 8.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_1 | 18 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 17 | 1.1033 | 1.0706 | -0.0327 | -0.0296 | -0.3465 | 0.172358 | 0.500000 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 21 | 1.1249 | 1.0762 | -0.0487 | -0.0433 | -0.3203 | 0.157678 | 0.250000 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 22 | 1.0697 | 1.0000 | -0.0697 | -0.0652 | -0.2132 | 0.328695 | 1.000000 | 1.000000 |
| optimality_ratio | canonical -> plan_scatter | 19 | 1.0000 | 1.0058 | 0.0058 | 0.0058 | 0.2294 | 0.330565 | 1.000000 | 1.000000 |
| optimality_ratio | plan_front -> plan_scatter | 24 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| first_failure_step | canonical -> disp_1 | 16 | 9.5625 | 11.1875 | 1.6250 | 0.1699 | 0.1079 | 0.672153 | 0.681641 | 1.000000 |
| first_failure_step | canonical -> disp_2 | 18 | 12.8333 | 13.5556 | 0.7222 | 0.0563 | 0.0480 | 0.841067 | 0.863525 | 1.000000 |
| first_failure_step | canonical -> disp_3 | 19 | 13.7895 | 11.8947 | -1.8947 | -0.1374 | -0.1480 | 0.527101 | 0.538757 | 1.000000 |
| first_failure_step | canonical -> plan_front | 14 | 11.6429 | 12.2857 | 0.6429 | 0.0552 | 0.0388 | 0.886681 | 0.910156 | 1.000000 |
| first_failure_step | canonical -> plan_scatter | 13 | 10.3077 | 11.1538 | 0.8462 | 0.0821 | 0.0666 | 0.814221 | 0.848633 | 1.000000 |
| first_failure_step | plan_front -> plan_scatter | 11 | 18.6364 | 10.0909 | -8.5455 | -0.4585 | -0.7858 | 0.026216 | 0.027344 | 0.027344 |
| prompt_tokens | canonical -> disp_1 | 299 | 9196.3411 | 9220.9197 | 24.5786 | 0.0027 | 0.0111 | 0.847246 | 0.848040 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 299 | 9196.3411 | 9085.3913 | -110.9498 | -0.0121 | -0.0491 | 0.396543 | 0.403940 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 299 | 9196.3411 | 9467.4080 | 271.0669 | 0.0295 | 0.1125 | 0.052779 | 0.055190 | 0.275950 |
| prompt_tokens | canonical -> plan_front | 299 | 9196.3411 | 9216.4749 | 20.1338 | 0.0022 | 0.0089 | 0.877895 | 0.904470 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 299 | 9196.3411 | 9344.8829 | 148.5418 | 0.0162 | 0.0628 | 0.278077 | 0.278780 | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 300 | 9212.2267 | 9340.2067 | 127.9800 | 0.0139 | 0.0565 | 0.328185 | 0.309770 | 0.309770 |
| completion_tokens | canonical -> disp_1 | 299 | 47556.8997 | 49828.3512 | 2271.4515 | 0.0478 | 0.0634 | 0.273974 | 0.273930 | 1.000000 |
| completion_tokens | canonical -> disp_2 | 299 | 47556.8997 | 49662.2742 | 2105.3746 | 0.0443 | 0.0617 | 0.287093 | 0.288170 | 1.000000 |
| completion_tokens | canonical -> disp_3 | 299 | 47556.8997 | 44761.9632 | -2794.9365 | -0.0588 | -0.0778 | 0.179379 | 0.179530 | 0.897650 |
| completion_tokens | canonical -> plan_front | 299 | 47556.8997 | 48914.5619 | 1357.6622 | 0.0285 | 0.0402 | 0.487749 | 0.488130 | 1.000000 |
| completion_tokens | canonical -> plan_scatter | 299 | 47556.8997 | 47248.0870 | -308.8127 | -0.0065 | -0.0087 | 0.880682 | 0.880440 | 1.000000 |
| completion_tokens | plan_front -> plan_scatter | 300 | 48768.1300 | 47110.9433 | -1657.1867 | -0.0340 | -0.0486 | 0.400526 | 0.402270 | 0.402270 |
| reasoning_completion_tokens | canonical -> disp_1 | 299 | 47543.4916 | 49819.5117 | 2276.0201 | 0.0479 | 0.0636 | 0.272618 | 0.272450 | 1.000000 |
| reasoning_completion_tokens | canonical -> disp_2 | 299 | 47543.4916 | 49651.3813 | 2107.8896 | 0.0443 | 0.0618 | 0.286131 | 0.287130 | 1.000000 |
| reasoning_completion_tokens | canonical -> disp_3 | 299 | 47543.4916 | 44749.8829 | -2793.6087 | -0.0588 | -0.0778 | 0.179285 | 0.179550 | 0.897750 |
| reasoning_completion_tokens | canonical -> plan_front | 299 | 47543.4916 | 48899.9766 | 1356.4849 | 0.0285 | 0.0402 | 0.487782 | 0.488140 | 1.000000 |
| reasoning_completion_tokens | canonical -> plan_scatter | 299 | 47543.4916 | 47235.6154 | -307.8763 | -0.0065 | -0.0087 | 0.880956 | 0.881000 | 1.000000 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 300 | 48753.5933 | 47098.5133 | -1655.0800 | -0.0339 | -0.0486 | 0.400695 | 0.402580 | 0.402580 |
| raw_completion_tokens | canonical -> disp_1 | 299 | 13.4080 | 8.8395 | -4.5686 | -0.3407 | -0.0349 | 0.546976 | 0.570435 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 299 | 13.4080 | 10.8930 | -2.5151 | -0.1876 | -0.0172 | 0.766540 | 0.795220 | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 299 | 13.4080 | 12.0803 | -1.3278 | -0.0990 | -0.0098 | 0.865791 | 0.875970 | 1.000000 |
| raw_completion_tokens | canonical -> plan_front | 299 | 13.4080 | 14.5853 | 1.1773 | 0.0878 | 0.0088 | 0.878989 | 0.884710 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 299 | 13.4080 | 12.4716 | -0.9365 | -0.0698 | -0.0070 | 0.903096 | 0.908205 | 1.000000 |
| raw_completion_tokens | plan_front -> plan_scatter | 300 | 14.5367 | 12.4300 | -2.1067 | -0.1449 | -0.0181 | 0.753496 | 0.756330 | 0.756330 |
| total_tokens | canonical -> disp_1 | 299 | 56753.2408 | 59049.2709 | 2296.0301 | 0.0405 | 0.0643 | 0.266766 | 0.266540 | 1.000000 |
| total_tokens | canonical -> disp_2 | 299 | 56753.2408 | 58747.6656 | 1994.4247 | 0.0351 | 0.0589 | 0.309583 | 0.310880 | 1.000000 |
| total_tokens | canonical -> disp_3 | 299 | 56753.2408 | 54229.3712 | -2523.8696 | -0.0445 | -0.0711 | 0.219969 | 0.219890 | 1.000000 |
| total_tokens | canonical -> plan_front | 299 | 56753.2408 | 58131.0368 | 1377.7960 | 0.0243 | 0.0411 | 0.477999 | 0.477580 | 1.000000 |
| total_tokens | canonical -> plan_scatter | 299 | 56753.2408 | 56592.9699 | -160.2709 | -0.0028 | -0.0046 | 0.937019 | 0.937590 | 1.000000 |
| total_tokens | plan_front -> plan_scatter | 300 | 57980.3567 | 56451.1500 | -1529.2067 | -0.0264 | -0.0452 | 0.434155 | 0.436430 | 0.436430 |
| duration_sec | canonical -> disp_1 | 299 | 253.0097 | 253.7298 | 0.7201 | 0.0028 | 0.0040 | 0.944799 | 0.946430 | 1.000000 |
| duration_sec | canonical -> disp_2 | 299 | 253.0097 | 247.5240 | -5.4857 | -0.0217 | -0.0321 | 0.579613 | 0.579640 | 1.000000 |
| duration_sec | canonical -> disp_3 | 299 | 253.0097 | 224.0953 | -28.9144 | -0.1143 | -0.1493 | 0.010330 | 0.009920 | 0.049600 |
| duration_sec | canonical -> plan_front | 299 | 253.0097 | 247.8006 | -5.2091 | -0.0206 | -0.0289 | 0.617538 | 0.616610 | 1.000000 |
| duration_sec | canonical -> plan_scatter | 299 | 253.0097 | 244.2632 | -8.7465 | -0.0346 | -0.0456 | 0.431471 | 0.431290 | 1.000000 |
| duration_sec | plan_front -> plan_scatter | 300 | 247.1164 | 243.5469 | -3.5695 | -0.0144 | -0.0193 | 0.737777 | 0.738180 | 0.738180 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> plan_scatter | 20 | 0.1667 | 0.1267 | -0.0400 | [-0.0800, -0.0033] | 0.085938 |
| executability | plan_front -> plan_scatter | 20 | 0.6433 | 0.6600 | 0.0167 | [-0.0433, 0.0800] | 0.678864 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.3567 | 0.3400 | -0.0167 | [-0.0800, 0.0433] | 0.678864 |
| conditional_reachability | plan_front -> plan_scatter | 20 | 0.2114 | 0.1752 | -0.0362 | [-0.0797, 0.0060] | 0.128906 |
| plan_length | plan_front -> plan_scatter | 6 | 11.3333 | 11.2778 | -0.0556 | [-0.2500, 0.0833] | 1.000000 |
| optimality_ratio | plan_front -> plan_scatter | 6 | 1.0714 | 1.0686 | -0.0029 | [-0.0179, 0.0093] | 1.000000 |
| first_failure_step | plan_front -> plan_scatter | 16 | 8.4899 | 5.6086 | -2.8813 | [-6.1947, 0.2271] | 0.113037 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 9212.2267 | 9340.2067 | 127.9800 | [-149.7212, 401.3932] | 0.368286 |
| completion_tokens | plan_front -> plan_scatter | 20 | 48768.1300 | 47110.9433 | -1657.1867 | [-5174.1079, 1752.7248] | 0.380466 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 48753.5933 | 47098.5133 | -1655.0800 | [-5167.7252, 1750.1586] | 0.380354 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 14.5367 | 12.4300 | -2.1067 | [-12.9567, 9.5401] | 0.729980 |
| total_tokens | plan_front -> plan_scatter | 20 | 57980.3567 | 56451.1500 | -1529.2067 | [-4989.5991, 1852.8975] | 0.410986 |
| duration_sec | plan_front -> plan_scatter | 20 | 247.1164 | 243.5469 | -3.5695 | [-30.9873, 23.6147] | 0.807058 |
