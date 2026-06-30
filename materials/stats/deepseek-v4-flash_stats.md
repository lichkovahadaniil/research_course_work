# Statistical Tests: deepseek/deepseek-v4-flash

Primary baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_back`, `plan_scatter`.
`plan_front` baseline comparisons: `plan_front` vs `canonical`, `plan_front` vs `disp_1`, `plan_front` vs `disp_2`, `plan_front` vs `disp_3`, `plan_front` vs `plan_back`, `plan_front` vs `plan_scatter`.

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
| reachability | plan_front -> canonical | 300 | 0.5933 | 0.6267 | 52 | 42 | 0.0333 | 1.2381 | 0.353328 | 1.000000 |
| reachability | plan_front -> disp_1 | 300 | 0.5933 | 0.6433 | 52 | 37 | 0.0500 | 1.4054 | 0.137368 | 0.686840 |
| reachability | plan_front -> disp_2 | 300 | 0.5933 | 0.6233 | 54 | 45 | 0.0300 | 1.2000 | 0.421523 | 1.000000 |
| reachability | plan_front -> disp_3 | 300 | 0.5933 | 0.4433 | 24 | 69 | -0.1500 | 0.3478 | 0.000003 | 0.000020 |
| reachability | plan_front -> plan_back | 300 | 0.5933 | 0.5833 | 49 | 52 | -0.0100 | 0.9423 | 0.842382 | 1.000000 |
| reachability | plan_front -> plan_scatter | 300 | 0.5933 | 0.5867 | 47 | 49 | -0.0067 | 0.9592 | 0.918778 | 1.000000 |
| executability | canonical -> disp_1 | 300 | 0.6333 | 0.6567 | 59 | 52 | 0.0233 | 1.1346 | 0.569220 | 1.000000 |
| executability | canonical -> disp_2 | 300 | 0.6333 | 0.6333 | 54 | 54 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| executability | canonical -> disp_3 | 300 | 0.6333 | 0.4667 | 27 | 77 | -0.1667 | 0.3506 | 0.000001 | 0.000006 |
| executability | canonical -> plan_front | 300 | 0.6333 | 0.6133 | 45 | 51 | -0.0200 | 0.8824 | 0.610068 | 1.000000 |
| executability | canonical -> plan_back | 300 | 0.6333 | 0.5867 | 46 | 60 | -0.0467 | 0.7667 | 0.206498 | 1.000000 |
| executability | canonical -> plan_scatter | 300 | 0.6333 | 0.6067 | 44 | 52 | -0.0267 | 0.8462 | 0.475152 | 1.000000 |
| executability | plan_front -> canonical | 300 | 0.6133 | 0.6333 | 51 | 45 | 0.0200 | 1.1333 | 0.610068 | 1.000000 |
| executability | plan_front -> disp_1 | 300 | 0.6133 | 0.6567 | 51 | 38 | 0.0433 | 1.3421 | 0.203117 | 1.000000 |
| executability | plan_front -> disp_2 | 300 | 0.6133 | 0.6333 | 51 | 45 | 0.0200 | 1.1333 | 0.610068 | 1.000000 |
| executability | plan_front -> disp_3 | 300 | 0.6133 | 0.4667 | 25 | 69 | -0.1467 | 0.3623 | 0.000006 | 0.000038 |
| executability | plan_front -> plan_back | 300 | 0.6133 | 0.5867 | 47 | 55 | -0.0267 | 0.8545 | 0.488434 | 1.000000 |
| executability | plan_front -> plan_scatter | 300 | 0.6133 | 0.6067 | 46 | 48 | -0.0067 | 0.9583 | 0.917923 | 1.000000 |
| non_executable_failure | canonical -> disp_1 | 300 | 0.3667 | 0.3433 | 52 | 59 | -0.0233 | 0.8814 | 0.569220 | 1.000000 |
| non_executable_failure | canonical -> disp_2 | 300 | 0.3667 | 0.3667 | 54 | 54 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| non_executable_failure | canonical -> disp_3 | 300 | 0.3667 | 0.5333 | 77 | 27 | 0.1667 | 2.8519 | 0.000001 | 0.000006 |
| non_executable_failure | canonical -> plan_front | 300 | 0.3667 | 0.3867 | 51 | 45 | 0.0200 | 1.1333 | 0.610068 | 1.000000 |
| non_executable_failure | canonical -> plan_back | 300 | 0.3667 | 0.4133 | 60 | 46 | 0.0467 | 1.3043 | 0.206498 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 300 | 0.3667 | 0.3933 | 52 | 44 | 0.0267 | 1.1818 | 0.475152 | 1.000000 |
| non_executable_failure | plan_front -> canonical | 300 | 0.3867 | 0.3667 | 45 | 51 | -0.0200 | 0.8824 | 0.610068 | 1.000000 |
| non_executable_failure | plan_front -> disp_1 | 300 | 0.3867 | 0.3433 | 38 | 51 | -0.0433 | 0.7451 | 0.203117 | 1.000000 |
| non_executable_failure | plan_front -> disp_2 | 300 | 0.3867 | 0.3667 | 45 | 51 | -0.0200 | 0.8824 | 0.610068 | 1.000000 |
| non_executable_failure | plan_front -> disp_3 | 300 | 0.3867 | 0.5333 | 69 | 25 | 0.1467 | 2.7600 | 0.000006 | 0.000038 |
| non_executable_failure | plan_front -> plan_back | 300 | 0.3867 | 0.4133 | 55 | 47 | 0.0267 | 1.1702 | 0.488434 | 1.000000 |
| non_executable_failure | plan_front -> plan_scatter | 300 | 0.3867 | 0.3933 | 48 | 46 | 0.0067 | 1.0435 | 0.917923 | 1.000000 |

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
| conditional_reachability | plan_front -> canonical | 184 | 190 | 0.9674 | 0.9895 | 178/6 | 188/2 | 0.0221 | 3.1685 | 0.168895 | 0.844475 |
| conditional_reachability | plan_front -> disp_1 | 184 | 197 | 0.9674 | 0.9797 | 178/6 | 193/4 | 0.0123 | 1.6264 | 0.531736 | 1.000000 |
| conditional_reachability | plan_front -> disp_2 | 184 | 190 | 0.9674 | 0.9842 | 178/6 | 187/3 | 0.0168 | 2.1011 | 0.330883 | 1.000000 |
| conditional_reachability | plan_front -> disp_3 | 184 | 140 | 0.9674 | 0.9500 | 178/6 | 133/7 | -0.0174 | 0.6404 | 0.569542 | 1.000000 |
| conditional_reachability | plan_front -> plan_back | 184 | 176 | 0.9674 | 0.9943 | 178/6 | 175/1 | 0.0269 | 5.8989 | 0.121994 | 0.731964 |
| conditional_reachability | plan_front -> plan_scatter | 184 | 182 | 0.9674 | 0.9670 | 178/6 | 176/6 | -0.0004 | 0.9888 | 1.000000 | 1.000000 |

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
| plan_length | plan_front -> canonical | 136 | 21.2132 | 21.8824 | 0.6691 | 0.0315 | 0.1877 | 0.030346 | 0.027670 | 0.138350 |
| plan_length | plan_front -> disp_1 | 141 | 19.8227 | 20.2340 | 0.4113 | 0.0208 | 0.1248 | 0.140763 | 0.148600 | 0.297200 |
| plan_length | plan_front -> disp_2 | 133 | 19.8421 | 20.2256 | 0.3835 | 0.0193 | 0.1142 | 0.189993 | 0.203440 | 0.297200 |
| plan_length | plan_front -> disp_3 | 109 | 17.3853 | 18.0734 | 0.6881 | 0.0396 | 0.1910 | 0.048645 | 0.047760 | 0.191040 |
| plan_length | plan_front -> plan_back | 126 | 19.0079 | 19.9841 | 0.9762 | 0.0514 | 0.2460 | 0.006632 | 0.003310 | 0.019860 |
| plan_length | plan_front -> plan_scatter | 129 | 20.1783 | 20.8062 | 0.6279 | 0.0311 | 0.1699 | 0.055847 | 0.056860 | 0.191040 |
| optimality_ratio | canonical -> disp_1 | 136 | 1.1412 | 1.1285 | -0.0128 | -0.0112 | -0.0549 | 0.523080 | 0.537180 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 133 | 1.1361 | 1.1253 | -0.0108 | -0.0095 | -0.0584 | 0.501965 | 0.530210 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 109 | 1.1128 | 1.1046 | -0.0082 | -0.0074 | -0.0277 | 0.773109 | 0.779770 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 136 | 1.1305 | 1.0974 | -0.0332 | -0.0293 | -0.1635 | 0.058666 | 0.051060 | 0.306360 |
| optimality_ratio | canonical -> plan_back | 130 | 1.1304 | 1.1479 | 0.0175 | 0.0155 | 0.0974 | 0.268908 | 0.299840 | 1.000000 |
| optimality_ratio | canonical -> plan_scatter | 135 | 1.1224 | 1.1391 | 0.0167 | 0.0148 | 0.0628 | 0.466826 | 0.485840 | 1.000000 |
| optimality_ratio | plan_front -> canonical | 136 | 1.0974 | 1.1305 | 0.0332 | 0.0302 | 0.1635 | 0.058666 | 0.051060 | 0.255300 |
| optimality_ratio | plan_front -> disp_1 | 141 | 1.1149 | 1.1273 | 0.0124 | 0.0111 | 0.0741 | 0.380395 | 0.400130 | 0.800260 |
| optimality_ratio | plan_front -> disp_2 | 133 | 1.1084 | 1.1222 | 0.0138 | 0.0124 | 0.0754 | 0.386432 | 0.408900 | 0.800260 |
| optimality_ratio | plan_front -> disp_3 | 109 | 1.0845 | 1.1153 | 0.0308 | 0.0284 | 0.1444 | 0.134523 | 0.153360 | 0.460080 |
| optimality_ratio | plan_front -> plan_back | 126 | 1.0977 | 1.1493 | 0.0515 | 0.0469 | 0.2102 | 0.019826 | 0.010720 | 0.064320 |
| optimality_ratio | plan_front -> plan_scatter | 129 | 1.0995 | 1.1293 | 0.0299 | 0.0272 | 0.1461 | 0.099391 | 0.102560 | 0.410240 |
| first_failure_step | canonical -> disp_1 | 50 | 17.2200 | 21.0400 | 3.8200 | 0.2218 | 0.2332 | 0.105592 | 0.106980 | 0.534900 |
| first_failure_step | canonical -> disp_2 | 53 | 18.9811 | 17.1321 | -1.8491 | -0.0974 | -0.1173 | 0.397181 | 0.402930 | 1.000000 |
| first_failure_step | canonical -> disp_3 | 77 | 16.7273 | 13.0000 | -3.7273 | -0.2228 | -0.2817 | 0.015692 | 0.015670 | 0.094020 |
| first_failure_step | canonical -> plan_front | 64 | 16.2812 | 17.1562 | 0.8750 | 0.0537 | 0.0544 | 0.665021 | 0.672290 | 1.000000 |
| first_failure_step | canonical -> plan_back | 62 | 17.9194 | 15.7903 | -2.1290 | -0.1188 | -0.1299 | 0.310468 | 0.316130 | 1.000000 |
| first_failure_step | canonical -> plan_scatter | 61 | 16.5410 | 16.2131 | -0.3279 | -0.0198 | -0.0236 | 0.854673 | 0.863450 | 1.000000 |
| first_failure_step | plan_front -> canonical | 64 | 17.1562 | 16.2812 | -0.8750 | -0.0510 | -0.0544 | 0.665021 | 0.672290 | 1.000000 |
| first_failure_step | plan_front -> disp_1 | 61 | 15.1803 | 20.7377 | 5.5574 | 0.3661 | 0.3796 | 0.004345 | 0.004840 | 0.029040 |
| first_failure_step | plan_front -> disp_2 | 61 | 16.8689 | 18.4426 | 1.5738 | 0.0933 | 0.1019 | 0.429046 | 0.434640 | 1.000000 |
| first_failure_step | plan_front -> disp_3 | 87 | 14.5287 | 13.1264 | -1.4023 | -0.0965 | -0.1224 | 0.256946 | 0.264750 | 1.000000 |
| first_failure_step | plan_front -> plan_back | 68 | 17.8088 | 16.7647 | -1.0441 | -0.0586 | -0.0644 | 0.597023 | 0.600610 | 1.000000 |
| first_failure_step | plan_front -> plan_scatter | 67 | 15.9403 | 15.4776 | -0.4627 | -0.0290 | -0.0355 | 0.772434 | 0.780950 | 1.000000 |
| prompt_tokens | canonical -> disp_1 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_back | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> canonical | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> disp_1 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> disp_2 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> disp_3 | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> plan_back | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 300 | 10232.0500 | 10232.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> disp_1 | 300 | 13194.2267 | 12196.1500 | -998.0767 | -0.0756 | -0.2317 | 0.000076 | 0.000090 | 0.000450 |
| completion_tokens | canonical -> disp_2 | 300 | 13194.2267 | 12024.6133 | -1169.6133 | -0.0886 | -0.2514 | 0.000018 | 0.000020 | 0.000120 |
| completion_tokens | canonical -> disp_3 | 300 | 13194.2267 | 13863.2800 | 669.0533 | 0.0507 | 0.1434 | 0.013575 | 0.013270 | 0.053080 |
| completion_tokens | canonical -> plan_front | 300 | 13194.2267 | 12774.7433 | -419.4833 | -0.0318 | -0.0897 | 0.121212 | 0.122550 | 0.367650 |
| completion_tokens | canonical -> plan_back | 300 | 13194.2267 | 13115.2900 | -78.9367 | -0.0060 | -0.0164 | 0.777126 | 0.777130 | 1.000000 |
| completion_tokens | canonical -> plan_scatter | 300 | 13194.2267 | 13125.1800 | -69.0467 | -0.0052 | -0.0141 | 0.806874 | 0.807000 | 1.000000 |
| completion_tokens | plan_front -> canonical | 300 | 12774.7433 | 13194.2267 | 419.4833 | 0.0328 | 0.0897 | 0.121212 | 0.122550 | 0.367650 |
| completion_tokens | plan_front -> disp_1 | 300 | 12774.7433 | 12196.1500 | -578.5933 | -0.0453 | -0.1252 | 0.030932 | 0.030770 | 0.123080 |
| completion_tokens | plan_front -> disp_2 | 300 | 12774.7433 | 12024.6133 | -750.1300 | -0.0587 | -0.1522 | 0.008826 | 0.008740 | 0.043700 |
| completion_tokens | plan_front -> disp_3 | 300 | 12774.7433 | 13863.2800 | 1088.5367 | 0.0852 | 0.2357 | 0.000057 | 0.000060 | 0.000360 |
| completion_tokens | plan_front -> plan_back | 300 | 12774.7433 | 13115.2900 | 340.5467 | 0.0267 | 0.0732 | 0.205610 | 0.206250 | 0.412500 |
| completion_tokens | plan_front -> plan_scatter | 300 | 12774.7433 | 13125.1800 | 350.4367 | 0.0274 | 0.0687 | 0.235348 | 0.235600 | 0.412500 |
| reasoning_completion_tokens | canonical -> disp_1 | 300 | 12623.0133 | 11624.7533 | -998.2600 | -0.0791 | -0.2331 | 0.000069 | 0.000080 | 0.000400 |
| reasoning_completion_tokens | canonical -> disp_2 | 300 | 12623.0133 | 11457.7333 | -1165.2800 | -0.0923 | -0.2516 | 0.000018 | 0.000020 | 0.000120 |
| reasoning_completion_tokens | canonical -> disp_3 | 300 | 12623.0133 | 13308.5400 | 685.5267 | 0.0543 | 0.1474 | 0.011170 | 0.010830 | 0.043320 |
| reasoning_completion_tokens | canonical -> plan_front | 300 | 12623.0133 | 12212.7633 | -410.2500 | -0.0325 | -0.0882 | 0.127492 | 0.128870 | 0.386610 |
| reasoning_completion_tokens | canonical -> plan_back | 300 | 12623.0133 | 12548.4067 | -74.6067 | -0.0059 | -0.0155 | 0.788329 | 0.788910 | 1.000000 |
| reasoning_completion_tokens | canonical -> plan_scatter | 300 | 12623.0133 | 12552.4300 | -70.5833 | -0.0056 | -0.0145 | 0.801685 | 0.802170 | 1.000000 |
| reasoning_completion_tokens | plan_front -> canonical | 300 | 12212.7633 | 12623.0133 | 410.2500 | 0.0336 | 0.0882 | 0.127492 | 0.128870 | 0.386610 |
| reasoning_completion_tokens | plan_front -> disp_1 | 300 | 12212.7633 | 11624.7533 | -588.0100 | -0.0481 | -0.1276 | 0.027829 | 0.027610 | 0.110440 |
| reasoning_completion_tokens | plan_front -> disp_2 | 300 | 12212.7633 | 11457.7333 | -755.0300 | -0.0618 | -0.1540 | 0.008077 | 0.007930 | 0.039650 |
| reasoning_completion_tokens | plan_front -> disp_3 | 300 | 12212.7633 | 13308.5400 | 1095.7767 | 0.0897 | 0.2378 | 0.000049 | 0.000060 | 0.000360 |
| reasoning_completion_tokens | plan_front -> plan_back | 300 | 12212.7633 | 12548.4067 | 335.6433 | 0.0275 | 0.0725 | 0.210189 | 0.211430 | 0.422860 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 300 | 12212.7633 | 12552.4300 | 339.6667 | 0.0278 | 0.0668 | 0.248222 | 0.249350 | 0.422860 |
| raw_completion_tokens | canonical -> disp_1 | 300 | 571.2133 | 571.3967 | 0.1833 | 0.0003 | 0.0017 | 0.976798 | 0.977300 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 300 | 571.2133 | 566.8800 | -4.3333 | -0.0076 | -0.0401 | 0.487576 | 0.491320 | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 300 | 571.2133 | 554.7400 | -16.4733 | -0.0288 | -0.1527 | 0.008606 | 0.008440 | 0.050640 |
| raw_completion_tokens | canonical -> plan_front | 300 | 571.2133 | 561.9800 | -9.2333 | -0.0162 | -0.0738 | 0.202270 | 0.207960 | 1.000000 |
| raw_completion_tokens | canonical -> plan_back | 300 | 571.2133 | 566.8833 | -4.3300 | -0.0076 | -0.0369 | 0.523341 | 0.530010 | 1.000000 |
| raw_completion_tokens | canonical -> plan_scatter | 300 | 571.2133 | 572.7500 | 1.5367 | 0.0027 | 0.0125 | 0.828877 | 0.829100 | 1.000000 |
| raw_completion_tokens | plan_front -> canonical | 300 | 561.9800 | 571.2133 | 9.2333 | 0.0164 | 0.0738 | 0.202270 | 0.207960 | 0.898440 |
| raw_completion_tokens | plan_front -> disp_1 | 300 | 561.9800 | 571.3967 | 9.4167 | 0.0168 | 0.0798 | 0.167927 | 0.172190 | 0.898440 |
| raw_completion_tokens | plan_front -> disp_2 | 300 | 561.9800 | 566.8800 | 4.9000 | 0.0087 | 0.0422 | 0.465458 | 0.488200 | 0.976400 |
| raw_completion_tokens | plan_front -> disp_3 | 300 | 561.9800 | 554.7400 | -7.2400 | -0.0129 | -0.0623 | 0.281492 | 0.289410 | 0.898440 |
| raw_completion_tokens | plan_front -> plan_back | 300 | 561.9800 | 566.8833 | 4.9033 | 0.0087 | 0.0373 | 0.518753 | 0.528230 | 0.976400 |
| raw_completion_tokens | plan_front -> plan_scatter | 300 | 561.9800 | 572.7500 | 10.7700 | 0.0192 | 0.0838 | 0.147654 | 0.149740 | 0.898440 |
| total_tokens | canonical -> disp_1 | 300 | 23426.2767 | 22428.2000 | -998.0767 | -0.0426 | -0.2317 | 0.000076 | 0.000090 | 0.000450 |
| total_tokens | canonical -> disp_2 | 300 | 23426.2767 | 22256.6633 | -1169.6133 | -0.0499 | -0.2514 | 0.000018 | 0.000020 | 0.000120 |
| total_tokens | canonical -> disp_3 | 300 | 23426.2767 | 24095.3300 | 669.0533 | 0.0286 | 0.1434 | 0.013575 | 0.013270 | 0.053080 |
| total_tokens | canonical -> plan_front | 300 | 23426.2767 | 23006.7933 | -419.4833 | -0.0179 | -0.0897 | 0.121212 | 0.122550 | 0.367650 |
| total_tokens | canonical -> plan_back | 300 | 23426.2767 | 23347.3400 | -78.9367 | -0.0034 | -0.0164 | 0.777126 | 0.777130 | 1.000000 |
| total_tokens | canonical -> plan_scatter | 300 | 23426.2767 | 23357.2300 | -69.0467 | -0.0029 | -0.0141 | 0.806874 | 0.807000 | 1.000000 |
| total_tokens | plan_front -> canonical | 300 | 23006.7933 | 23426.2767 | 419.4833 | 0.0182 | 0.0897 | 0.121212 | 0.122550 | 0.367650 |
| total_tokens | plan_front -> disp_1 | 300 | 23006.7933 | 22428.2000 | -578.5933 | -0.0251 | -0.1252 | 0.030932 | 0.030770 | 0.123080 |
| total_tokens | plan_front -> disp_2 | 300 | 23006.7933 | 22256.6633 | -750.1300 | -0.0326 | -0.1522 | 0.008826 | 0.008740 | 0.043700 |
| total_tokens | plan_front -> disp_3 | 300 | 23006.7933 | 24095.3300 | 1088.5367 | 0.0473 | 0.2357 | 0.000057 | 0.000060 | 0.000360 |
| total_tokens | plan_front -> plan_back | 300 | 23006.7933 | 23347.3400 | 340.5467 | 0.0148 | 0.0732 | 0.205610 | 0.206250 | 0.412500 |
| total_tokens | plan_front -> plan_scatter | 300 | 23006.7933 | 23357.2300 | 350.4367 | 0.0152 | 0.0687 | 0.235348 | 0.235600 | 0.412500 |
| duration_sec | canonical -> disp_1 | 300 | 112.7854 | 105.4029 | -7.3824 | -0.0655 | -0.1678 | 0.003938 | 0.003790 | 0.018950 |
| duration_sec | canonical -> disp_2 | 300 | 112.7854 | 101.4734 | -11.3120 | -0.1003 | -0.2577 | 0.000011 | 0.000010 | 0.000060 |
| duration_sec | canonical -> disp_3 | 300 | 112.7854 | 117.3112 | 4.5258 | 0.0401 | 0.1032 | 0.074865 | 0.073830 | 0.221490 |
| duration_sec | canonical -> plan_front | 300 | 112.7854 | 109.5795 | -3.2059 | -0.0284 | -0.0682 | 0.238737 | 0.238390 | 0.476780 |
| duration_sec | canonical -> plan_back | 300 | 112.7854 | 129.3625 | 16.5771 | 0.1470 | 0.1382 | 0.017270 | 0.006370 | 0.025480 |
| duration_sec | canonical -> plan_scatter | 300 | 112.7854 | 112.1437 | -0.6416 | -0.0057 | -0.0135 | 0.815922 | 0.816080 | 0.816080 |
| duration_sec | plan_front -> canonical | 300 | 109.5795 | 112.7854 | 3.2059 | 0.0293 | 0.0682 | 0.238737 | 0.238390 | 0.476780 |
| duration_sec | plan_front -> disp_1 | 300 | 109.5795 | 105.4029 | -4.1766 | -0.0381 | -0.0903 | 0.118707 | 0.118880 | 0.356640 |
| duration_sec | plan_front -> disp_2 | 300 | 109.5795 | 101.4734 | -8.1061 | -0.0740 | -0.1685 | 0.003792 | 0.003690 | 0.017650 |
| duration_sec | plan_front -> disp_3 | 300 | 109.5795 | 117.3112 | 7.7317 | 0.0706 | 0.1699 | 0.003503 | 0.003530 | 0.017650 |
| duration_sec | plan_front -> plan_back | 300 | 109.5795 | 129.3625 | 19.7830 | 0.1805 | 0.1696 | 0.003567 | 0.000250 | 0.001500 |
| duration_sec | plan_front -> plan_scatter | 300 | 109.5795 | 112.1437 | 2.5642 | 0.0234 | 0.0531 | 0.358842 | 0.356900 | 0.476780 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> canonical | 20 | 0.5933 | 0.6267 | 0.0333 | [-0.0300, 0.1000] | 0.388062 |
| reachability | plan_front -> disp_1 | 20 | 0.5933 | 0.6433 | 0.0500 | [-0.0133, 0.1100] | 0.168640 |
| reachability | plan_front -> disp_2 | 20 | 0.5933 | 0.6233 | 0.0300 | [-0.0300, 0.0933] | 0.416626 |
| reachability | plan_front -> disp_3 | 20 | 0.5933 | 0.4433 | -0.1500 | [-0.2133, -0.0833] | 0.000656 |
| reachability | plan_front -> plan_back | 20 | 0.5933 | 0.5833 | -0.0100 | [-0.0667, 0.0467] | 0.823242 |
| reachability | plan_front -> plan_scatter | 20 | 0.5933 | 0.5867 | -0.0067 | [-0.0733, 0.0533] | 0.922363 |
| executability | plan_front -> canonical | 20 | 0.6133 | 0.6333 | 0.0200 | [-0.0400, 0.0800] | 0.600159 |
| executability | plan_front -> disp_1 | 20 | 0.6133 | 0.6567 | 0.0433 | [-0.0167, 0.1000] | 0.202789 |
| executability | plan_front -> disp_2 | 20 | 0.6133 | 0.6333 | 0.0200 | [-0.0400, 0.0800] | 0.600830 |
| executability | plan_front -> disp_3 | 20 | 0.6133 | 0.4667 | -0.1467 | [-0.2100, -0.0800] | 0.000824 |
| executability | plan_front -> plan_back | 20 | 0.6133 | 0.5867 | -0.0267 | [-0.0767, 0.0233] | 0.385712 |
| executability | plan_front -> plan_scatter | 20 | 0.6133 | 0.6067 | -0.0067 | [-0.0733, 0.0533] | 0.922852 |
| non_executable_failure | plan_front -> canonical | 20 | 0.3867 | 0.3667 | -0.0200 | [-0.0800, 0.0400] | 0.600159 |
| non_executable_failure | plan_front -> disp_1 | 20 | 0.3867 | 0.3433 | -0.0433 | [-0.1000, 0.0167] | 0.202789 |
| non_executable_failure | plan_front -> disp_2 | 20 | 0.3867 | 0.3667 | -0.0200 | [-0.0800, 0.0400] | 0.600830 |
| non_executable_failure | plan_front -> disp_3 | 20 | 0.3867 | 0.5333 | 0.1467 | [0.0800, 0.2100] | 0.000824 |
| non_executable_failure | plan_front -> plan_back | 20 | 0.3867 | 0.4133 | 0.0267 | [-0.0233, 0.0767] | 0.385712 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.3867 | 0.3933 | 0.0067 | [-0.0533, 0.0733] | 0.922852 |
| conditional_reachability | plan_front -> canonical | 20 | 0.9645 | 0.9833 | 0.0188 | [-0.0333, 0.0688] | 0.562500 |
| conditional_reachability | plan_front -> disp_1 | 20 | 0.9645 | 0.9767 | 0.0122 | [-0.0291, 0.0544] | 0.593750 |
| conditional_reachability | plan_front -> disp_2 | 20 | 0.9645 | 0.9811 | 0.0165 | [-0.0123, 0.0471] | 0.375000 |
| conditional_reachability | plan_front -> disp_3 | 19 | 0.9626 | 0.9249 | -0.0377 | [-0.1109, 0.0313] | 0.328125 |
| conditional_reachability | plan_front -> plan_back | 20 | 0.9645 | 0.9833 | 0.0188 | [-0.0333, 0.0688] | 0.562500 |
| conditional_reachability | plan_front -> plan_scatter | 20 | 0.9645 | 0.9430 | -0.0215 | [-0.0877, 0.0291] | 0.593750 |
| plan_length | plan_front -> canonical | 20 | 29.7725 | 29.9733 | 0.2008 | [-0.6306, 0.9742] | 0.635193 |
| plan_length | plan_front -> disp_1 | 20 | 29.7725 | 30.2434 | 0.4709 | [-0.1504, 1.0849] | 0.160828 |
| plan_length | plan_front -> disp_2 | 20 | 29.7725 | 29.9124 | 0.1399 | [-0.5652, 0.8501] | 0.714813 |
| plan_length | plan_front -> disp_3 | 19 | 28.7605 | 29.2132 | 0.4527 | [-0.3469, 1.2895] | 0.309814 |
| plan_length | plan_front -> plan_back | 20 | 29.7725 | 30.1819 | 0.4094 | [-0.6174, 1.4153] | 0.453979 |
| plan_length | plan_front -> plan_scatter | 20 | 29.7725 | 30.2472 | 0.4747 | [-0.1561, 1.0839] | 0.160034 |
| optimality_ratio | plan_front -> canonical | 20 | 1.1637 | 1.1792 | 0.0155 | [-0.0157, 0.0471] | 0.354980 |
| optimality_ratio | plan_front -> disp_1 | 20 | 1.1637 | 1.1789 | 0.0152 | [-0.0075, 0.0369] | 0.205688 |
| optimality_ratio | plan_front -> disp_2 | 20 | 1.1637 | 1.1720 | 0.0083 | [-0.0140, 0.0297] | 0.479401 |
| optimality_ratio | plan_front -> disp_3 | 19 | 1.1620 | 1.1819 | 0.0199 | [-0.0142, 0.0625] | 0.394470 |
| optimality_ratio | plan_front -> plan_back | 20 | 1.1637 | 1.1816 | 0.0179 | [-0.0250, 0.0650] | 0.504395 |
| optimality_ratio | plan_front -> plan_scatter | 20 | 1.1637 | 1.1842 | 0.0205 | [-0.0008, 0.0422] | 0.084015 |
| first_failure_step | plan_front -> canonical | 15 | 13.7224 | 15.4457 | 1.7233 | [-0.6782, 4.0645] | 0.187805 |
| first_failure_step | plan_front -> disp_1 | 14 | 15.5597 | 19.3358 | 3.7760 | [-0.2128, 7.8199] | 0.104004 |
| first_failure_step | plan_front -> disp_2 | 15 | 14.5891 | 14.8833 | 0.2942 | [-2.7009, 3.1298] | 0.852783 |
| first_failure_step | plan_front -> disp_3 | 15 | 15.0558 | 13.2285 | -1.8273 | [-5.8449, 2.1046] | 0.407288 |
| first_failure_step | plan_front -> plan_back | 16 | 14.9273 | 13.9707 | -0.9566 | [-3.3907, 1.1219] | 0.450256 |
| first_failure_step | plan_front -> plan_scatter | 15 | 15.0558 | 13.8408 | -1.2150 | [-4.5579, 1.6065] | 0.507263 |
| prompt_tokens | plan_front -> canonical | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> disp_1 | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> disp_2 | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> disp_3 | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> plan_back | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 10232.0500 | 10232.0500 | 0.0000 | [0.0000, 0.0000] | 1.000000 |
| completion_tokens | plan_front -> canonical | 20 | 12774.7433 | 13194.2267 | 419.4833 | [-293.7450, 1118.3350] | 0.272194 |
| completion_tokens | plan_front -> disp_1 | 20 | 12774.7433 | 12196.1500 | -578.5933 | [-1329.1584, 145.5192] | 0.153612 |
| completion_tokens | plan_front -> disp_2 | 20 | 12774.7433 | 12024.6133 | -750.1300 | [-1606.8670, 32.1977] | 0.096554 |
| completion_tokens | plan_front -> disp_3 | 20 | 12774.7433 | 13863.2800 | 1088.5367 | [448.3750, 1767.7240] | 0.003502 |
| completion_tokens | plan_front -> plan_back | 20 | 12774.7433 | 13115.2900 | 340.5467 | [-404.5667, 1082.4028] | 0.397717 |
| completion_tokens | plan_front -> plan_scatter | 20 | 12774.7433 | 13125.1800 | 350.4367 | [-518.6958, 1166.6555] | 0.442095 |
| reasoning_completion_tokens | plan_front -> canonical | 20 | 12212.7633 | 12623.0133 | 410.2500 | [-292.1844, 1102.8846] | 0.275934 |
| reasoning_completion_tokens | plan_front -> disp_1 | 20 | 12212.7633 | 11624.7533 | -588.0100 | [-1333.5998, 132.7247] | 0.145798 |
| reasoning_completion_tokens | plan_front -> disp_2 | 20 | 12212.7633 | 11457.7333 | -755.0300 | [-1605.4278, 21.6138] | 0.091652 |
| reasoning_completion_tokens | plan_front -> disp_3 | 20 | 12212.7633 | 13308.5400 | 1095.7767 | [458.6331, 1773.3023] | 0.003178 |
| reasoning_completion_tokens | plan_front -> plan_back | 20 | 12212.7633 | 12548.4067 | 335.6433 | [-402.8926, 1072.4479] | 0.400383 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 12212.7633 | 12552.4300 | 339.6667 | [-528.3967, 1153.8208] | 0.454939 |
| raw_completion_tokens | plan_front -> canonical | 20 | 561.9800 | 571.2133 | 9.2333 | [-9.0400, 26.6472] | 0.344376 |
| raw_completion_tokens | plan_front -> disp_1 | 20 | 561.9800 | 571.3967 | 9.4167 | [-2.3368, 20.4068] | 0.127151 |
| raw_completion_tokens | plan_front -> disp_2 | 20 | 561.9800 | 566.8800 | 4.9000 | [-12.5767, 21.6103] | 0.596535 |
| raw_completion_tokens | plan_front -> disp_3 | 20 | 561.9800 | 554.7400 | -7.2400 | [-23.0575, 6.6438] | 0.397911 |
| raw_completion_tokens | plan_front -> plan_back | 20 | 561.9800 | 566.8833 | 4.9033 | [-15.1600, 25.0972] | 0.652435 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 561.9800 | 572.7500 | 10.7700 | [-3.5169, 24.6502] | 0.159943 |
| total_tokens | plan_front -> canonical | 20 | 23006.7933 | 23426.2767 | 419.4833 | [-293.7450, 1118.3350] | 0.272194 |
| total_tokens | plan_front -> disp_1 | 20 | 23006.7933 | 22428.2000 | -578.5933 | [-1329.1584, 145.5192] | 0.153612 |
| total_tokens | plan_front -> disp_2 | 20 | 23006.7933 | 22256.6633 | -750.1300 | [-1606.8670, 32.1977] | 0.096554 |
| total_tokens | plan_front -> disp_3 | 20 | 23006.7933 | 24095.3300 | 1088.5367 | [448.3750, 1767.7240] | 0.003502 |
| total_tokens | plan_front -> plan_back | 20 | 23006.7933 | 23347.3400 | 340.5467 | [-404.5667, 1082.4028] | 0.397717 |
| total_tokens | plan_front -> plan_scatter | 20 | 23006.7933 | 23357.2300 | 350.4367 | [-518.6958, 1166.6555] | 0.442095 |
| duration_sec | plan_front -> canonical | 20 | 109.5795 | 112.7854 | 3.2059 | [-5.0186, 10.7827] | 0.447796 |
| duration_sec | plan_front -> disp_1 | 20 | 109.5795 | 105.4029 | -4.1766 | [-11.4429, 3.0079] | 0.290447 |
| duration_sec | plan_front -> disp_2 | 20 | 109.5795 | 101.4734 | -8.1061 | [-16.7046, -0.9002] | 0.065969 |
| duration_sec | plan_front -> disp_3 | 20 | 109.5795 | 117.3112 | 7.7317 | [2.4495, 13.4401] | 0.013609 |
| duration_sec | plan_front -> plan_back | 20 | 109.5795 | 129.3625 | 19.7830 | [2.5801, 42.0680] | 0.043964 |
| duration_sec | plan_front -> plan_scatter | 20 | 109.5795 | 112.1437 | 2.5642 | [-5.4949, 10.3186] | 0.542824 |
