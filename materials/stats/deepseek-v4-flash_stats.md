# Statistical Tests: deepseek/deepseek-v4-flash

Baseline order: `canonical`.
Canonical compared orders: `disp_1`, `disp_2`, `disp_3`, `plan_front`, `plan_scatter`.
Extra comparisons: `plan_front` vs `plan_scatter`.

Pairing unit for McNemar and numeric tests: `(problem, run)` within this model. Conditional reachability is summarized per order among executable plans only.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> disp_1 | 300 | 0.5367 | 0.5733 | 60 | 49 | 0.0367 | 1.2245 | 0.338185 | 1.000000 |
| reachability | canonical -> disp_2 | 300 | 0.5367 | 0.5600 | 53 | 46 | 0.0233 | 1.1522 | 0.546713 | 1.000000 |
| reachability | canonical -> disp_3 | 300 | 0.5367 | 0.3933 | 34 | 77 | -0.1433 | 0.4416 | 0.000055 | 0.000275 |
| reachability | canonical -> plan_front | 300 | 0.5367 | 0.4867 | 50 | 65 | -0.0500 | 0.7692 | 0.191496 | 0.765984 |
| reachability | canonical -> plan_scatter | 300 | 0.5367 | 0.5100 | 49 | 57 | -0.0267 | 0.8596 | 0.496754 | 1.000000 |
| reachability | plan_front -> plan_scatter | 300 | 0.4867 | 0.5100 | 52 | 45 | 0.0233 | 1.1556 | 0.542610 | 0.542610 |
| executability | canonical -> disp_1 | 300 | 0.6433 | 0.6667 | 57 | 50 | 0.0233 | 1.1400 | 0.562093 | 1.000000 |
| executability | canonical -> disp_2 | 300 | 0.6433 | 0.7033 | 57 | 39 | 0.0600 | 1.4615 | 0.082193 | 0.328772 |
| executability | canonical -> disp_3 | 300 | 0.6433 | 0.5467 | 41 | 70 | -0.0967 | 0.5857 | 0.007585 | 0.037924 |
| executability | canonical -> plan_front | 300 | 0.6433 | 0.6167 | 48 | 56 | -0.0267 | 0.8571 | 0.492645 | 1.000000 |
| executability | canonical -> plan_scatter | 300 | 0.6433 | 0.6400 | 50 | 51 | -0.0033 | 0.9804 | 1.000000 | 1.000000 |
| executability | plan_front -> plan_scatter | 300 | 0.6167 | 0.6400 | 60 | 53 | 0.0233 | 1.1321 | 0.572656 | 0.572656 |
| non_executable_failure | canonical -> disp_1 | 300 | 0.3567 | 0.3333 | 50 | 57 | -0.0233 | 0.8772 | 0.562093 | 1.000000 |
| non_executable_failure | canonical -> disp_2 | 300 | 0.3567 | 0.2967 | 39 | 57 | -0.0600 | 0.6842 | 0.082193 | 0.328772 |
| non_executable_failure | canonical -> disp_3 | 300 | 0.3567 | 0.4533 | 70 | 41 | 0.0967 | 1.7073 | 0.007585 | 0.037924 |
| non_executable_failure | canonical -> plan_front | 300 | 0.3567 | 0.3833 | 56 | 48 | 0.0267 | 1.1667 | 0.492645 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 300 | 0.3567 | 0.3600 | 51 | 50 | 0.0033 | 1.0200 | 1.000000 | 1.000000 |
| non_executable_failure | plan_front -> plan_scatter | 300 | 0.3833 | 0.3600 | 53 | 60 | -0.0233 | 0.8833 | 0.572656 | 0.572656 |

## Conditional Binary Metrics

`conditional_reachability` is computed as goal reached among executable plans for each order separately. Non-executable plans are excluded from that order's denominator. The comparison table uses Fisher's exact test on those executable-plan counts.

| metric | comparison | baseline n | compared n | baseline | compared | baseline success/fail | compared success/fail | risk diff | OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conditional_reachability | canonical -> disp_1 | 193 | 200 | 0.8342 | 0.8600 | 161/32 | 172/28 | 0.0258 | 1.2209 | 0.486936 | 1.000000 |
| conditional_reachability | canonical -> disp_2 | 193 | 211 | 0.8342 | 0.7962 | 161/32 | 168/43 | -0.0380 | 0.7765 | 0.370531 | 1.000000 |
| conditional_reachability | canonical -> disp_3 | 193 | 164 | 0.8342 | 0.7195 | 161/32 | 118/46 | -0.1147 | 0.5099 | 0.010201 | 0.051006 |
| conditional_reachability | canonical -> plan_front | 193 | 185 | 0.8342 | 0.7892 | 161/32 | 146/39 | -0.0450 | 0.7441 | 0.292967 | 1.000000 |
| conditional_reachability | canonical -> plan_scatter | 193 | 192 | 0.8342 | 0.7969 | 161/32 | 153/39 | -0.0373 | 0.7797 | 0.360440 | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 185 | 192 | 0.7892 | 0.7969 | 146/39 | 153/39 | 0.0077 | 1.0479 | 0.899117 | 0.899117 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> disp_1 | 112 | 18.5804 | 18.1696 | -0.4107 | -0.0221 | -0.1036 | 0.275080 | 0.294450 | 1.000000 |
| plan_length | canonical -> disp_2 | 115 | 18.7043 | 18.9304 | 0.2261 | 0.0121 | 0.0477 | 0.609628 | 0.630380 | 1.000000 |
| plan_length | canonical -> disp_3 | 84 | 14.6071 | 14.7500 | 0.1429 | 0.0098 | 0.0326 | 0.765740 | 0.792053 | 1.000000 |
| plan_length | canonical -> plan_front | 96 | 16.4792 | 16.0938 | -0.3854 | -0.0234 | -0.0939 | 0.359925 | 0.379320 | 1.000000 |
| plan_length | canonical -> plan_scatter | 104 | 17.5000 | 16.8942 | -0.6058 | -0.0346 | -0.1572 | 0.111892 | 0.120740 | 0.603700 |
| plan_length | plan_front -> plan_scatter | 101 | 16.7822 | 16.6634 | -0.1188 | -0.0071 | -0.0395 | 0.692208 | 0.746230 | 0.746230 |
| optimality_ratio | canonical -> disp_1 | 112 | 1.1305 | 1.1185 | -0.0120 | -0.0106 | -0.0483 | 0.610553 | 0.625680 | 1.000000 |
| optimality_ratio | canonical -> disp_2 | 115 | 1.1268 | 1.1442 | 0.0174 | 0.0154 | 0.0578 | 0.536835 | 0.544970 | 1.000000 |
| optimality_ratio | canonical -> disp_3 | 84 | 1.0579 | 1.0781 | 0.0202 | 0.0191 | 0.0733 | 0.503523 | 0.503750 | 1.000000 |
| optimality_ratio | canonical -> plan_front | 96 | 1.0927 | 1.0780 | -0.0147 | -0.0135 | -0.0553 | 0.588893 | 0.620440 | 1.000000 |
| optimality_ratio | canonical -> plan_scatter | 104 | 1.1304 | 1.0930 | -0.0374 | -0.0331 | -0.1599 | 0.106061 | 0.108430 | 0.542150 |
| optimality_ratio | plan_front -> plan_scatter | 101 | 1.0743 | 1.0633 | -0.0110 | -0.0102 | -0.0652 | 0.513764 | 0.623190 | 0.623190 |
| first_failure_step | canonical -> disp_1 | 48 | 18.9167 | 17.3333 | -1.5833 | -0.0837 | -0.1236 | 0.396192 | 0.408080 | 0.816160 |
| first_failure_step | canonical -> disp_2 | 46 | 17.6087 | 24.4783 | 6.8696 | 0.3901 | 0.4096 | 0.007952 | 0.007710 | 0.038550 |
| first_failure_step | canonical -> disp_3 | 65 | 16.9077 | 13.8769 | -3.0308 | -0.1793 | -0.2105 | 0.094543 | 0.096300 | 0.288900 |
| first_failure_step | canonical -> plan_front | 57 | 15.0526 | 15.4386 | 0.3860 | 0.0256 | 0.0260 | 0.844871 | 0.852090 | 0.852090 |
| first_failure_step | canonical -> plan_scatter | 57 | 15.1930 | 11.9123 | -3.2807 | -0.2159 | -0.2724 | 0.044432 | 0.044550 | 0.178200 |
| first_failure_step | plan_front -> plan_scatter | 53 | 15.2453 | 11.3396 | -3.9057 | -0.2562 | -0.2693 | 0.055290 | 0.054950 | 0.054950 |
| prompt_tokens | canonical -> disp_1 | 300 | 10234.7433 | 10229.0500 | -5.6933 | -0.0006 | -0.0577 | 0.318119 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_2 | 300 | 10234.7433 | 10234.7600 | 0.0167 | 0.0000 | 0.0001 | 0.998355 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> disp_3 | 300 | 10234.7433 | 10229.0500 | -5.6933 | -0.0006 | -0.0577 | 0.318119 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_front | 300 | 10234.7433 | 10240.3833 | 5.6400 | 0.0006 | 0.0331 | 0.567018 | 1.000000 | 1.000000 |
| prompt_tokens | canonical -> plan_scatter | 300 | 10234.7433 | 10240.4200 | 5.6767 | 0.0006 | 0.0332 | 0.565340 | 0.750000 | 1.000000 |
| prompt_tokens | plan_front -> plan_scatter | 300 | 10240.3833 | 10240.4200 | 0.0367 | 0.0000 | 0.0002 | 0.997429 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> disp_1 | 300 | 15848.5600 | 13803.0333 | -2045.5267 | -0.1291 | -0.0858 | 0.138274 | 0.109340 | 0.546700 |
| completion_tokens | canonical -> disp_2 | 300 | 15848.5600 | 14715.0433 | -1133.5167 | -0.0715 | -0.0369 | 0.522954 | 0.531210 | 1.000000 |
| completion_tokens | canonical -> disp_3 | 300 | 15848.5600 | 16509.9067 | 661.3467 | 0.0417 | 0.0289 | 0.617135 | 0.700850 | 1.000000 |
| completion_tokens | canonical -> plan_front | 300 | 15848.5600 | 18220.1400 | 2371.5800 | 0.1496 | 0.0595 | 0.303326 | 0.308530 | 1.000000 |
| completion_tokens | canonical -> plan_scatter | 300 | 15848.5600 | 15970.2233 | 121.6633 | 0.0077 | 0.0038 | 0.947584 | 0.938270 | 1.000000 |
| completion_tokens | plan_front -> plan_scatter | 300 | 18220.1400 | 15970.2233 | -2249.9167 | -0.1235 | -0.0570 | 0.324002 | 0.328810 | 0.328810 |
| reasoning_completion_tokens | canonical -> disp_1 | 300 | 15286.5600 | 13242.2300 | -2044.3300 | -0.1337 | -0.0856 | 0.139198 | 0.111160 | 0.555800 |
| reasoning_completion_tokens | canonical -> disp_2 | 300 | 15286.5600 | 13934.9033 | -1351.6567 | -0.0884 | -0.0443 | 0.443558 | 0.481600 | 1.000000 |
| reasoning_completion_tokens | canonical -> disp_3 | 300 | 15286.5600 | 15950.7700 | 664.2100 | 0.0435 | 0.0290 | 0.615912 | 0.698200 | 1.000000 |
| reasoning_completion_tokens | canonical -> plan_front | 300 | 15286.5600 | 17676.6567 | 2390.0967 | 0.1564 | 0.0599 | 0.300321 | 0.305350 | 1.000000 |
| reasoning_completion_tokens | canonical -> plan_scatter | 300 | 15286.5600 | 15420.7900 | 134.2300 | 0.0088 | 0.0042 | 0.942305 | 0.931490 | 1.000000 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 300 | 17676.6567 | 15420.7900 | -2255.8667 | -0.1276 | -0.0571 | 0.323580 | 0.325720 | 0.325720 |
| raw_completion_tokens | canonical -> disp_1 | 300 | 562.0000 | 560.8033 | -1.1967 | -0.0021 | -0.0104 | 0.857115 | 0.859740 | 1.000000 |
| raw_completion_tokens | canonical -> disp_2 | 300 | 562.0000 | 780.1400 | 218.1400 | 0.3881 | 0.0584 | 0.312203 | 0.376450 | 1.000000 |
| raw_completion_tokens | canonical -> disp_3 | 300 | 562.0000 | 559.1367 | -2.8633 | -0.0051 | -0.0182 | 0.752395 | 0.753950 | 1.000000 |
| raw_completion_tokens | canonical -> plan_front | 300 | 562.0000 | 543.4833 | -18.5167 | -0.0329 | -0.1162 | 0.045110 | 0.043410 | 0.217050 |
| raw_completion_tokens | canonical -> plan_scatter | 300 | 562.0000 | 549.4333 | -12.5667 | -0.0224 | -0.0706 | 0.222239 | 0.226880 | 0.907520 |
| raw_completion_tokens | plan_front -> plan_scatter | 300 | 543.4833 | 549.4333 | 5.9500 | 0.0109 | 0.0419 | 0.468574 | 0.470850 | 0.470850 |
| total_tokens | canonical -> disp_1 | 300 | 26083.3033 | 24032.0833 | -2051.2200 | -0.0786 | -0.0857 | 0.138591 | 0.109340 | 0.546700 |
| total_tokens | canonical -> disp_2 | 300 | 26083.3033 | 24949.8033 | -1133.5000 | -0.0435 | -0.0368 | 0.524685 | 0.532020 | 1.000000 |
| total_tokens | canonical -> disp_3 | 300 | 26083.3033 | 26738.9567 | 655.6533 | 0.0251 | 0.0285 | 0.621364 | 0.705530 | 1.000000 |
| total_tokens | canonical -> plan_front | 300 | 26083.3033 | 28460.5233 | 2377.2200 | 0.0911 | 0.0594 | 0.304092 | 0.308900 | 1.000000 |
| total_tokens | canonical -> plan_scatter | 300 | 26083.3033 | 26210.6433 | 127.3400 | 0.0049 | 0.0040 | 0.945360 | 0.935510 | 1.000000 |
| total_tokens | plan_front -> plan_scatter | 300 | 28460.5233 | 26210.6433 | -2249.8800 | -0.0791 | -0.0568 | 0.325950 | 0.330290 | 0.330290 |
| duration_sec | canonical -> disp_1 | 300 | 154.1733 | 143.3374 | -10.8359 | -0.0703 | -0.0474 | 0.412285 | 0.532200 | 1.000000 |
| duration_sec | canonical -> disp_2 | 300 | 154.1733 | 150.0250 | -4.1483 | -0.0269 | -0.0143 | 0.804040 | 0.791070 | 1.000000 |
| duration_sec | canonical -> disp_3 | 300 | 154.1733 | 177.3149 | 23.1416 | 0.1501 | 0.1010 | 0.081176 | 0.075820 | 0.379100 |
| duration_sec | canonical -> plan_front | 300 | 154.1733 | 179.2586 | 25.0853 | 0.1627 | 0.0678 | 0.241148 | 0.251830 | 1.000000 |
| duration_sec | canonical -> plan_scatter | 300 | 154.1733 | 162.3651 | 8.1918 | 0.0531 | 0.0266 | 0.645776 | 0.626930 | 1.000000 |
| duration_sec | plan_front -> plan_scatter | 300 | 179.2586 | 162.3651 | -16.8934 | -0.0942 | -0.0467 | 0.419466 | 0.423470 | 0.423470 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> plan_scatter | 20 | 0.4867 | 0.5100 | 0.0233 | [-0.0500, 0.1000] | 0.605469 |
| executability | plan_front -> plan_scatter | 20 | 0.6167 | 0.6400 | 0.0233 | [-0.0500, 0.1033] | 0.631592 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.3833 | 0.3600 | -0.0233 | [-0.1033, 0.0500] | 0.631592 |
| conditional_reachability | plan_front -> plan_scatter | 20 | 0.7096 | 0.7522 | 0.0427 | [-0.0549, 0.1438] | 0.427353 |
| plan_length | plan_front -> plan_scatter | 19 | 30.1367 | 30.5054 | 0.3687 | [-0.5371, 1.4382] | 0.530762 |
| optimality_ratio | plan_front -> plan_scatter | 19 | 1.1645 | 1.1665 | 0.0020 | [-0.0321, 0.0391] | 0.917725 |
| first_failure_step | plan_front -> plan_scatter | 15 | 15.2341 | 12.5829 | -2.6512 | [-6.3796, 0.6981] | 0.178101 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 10240.3833 | 10240.4200 | 0.0367 | [-17.0800, 17.1900] | 1.000000 |
| completion_tokens | plan_front -> plan_scatter | 20 | 18220.1400 | 15970.2233 | -2249.9167 | [-7882.0585, 2862.9553] | 0.450377 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 17676.6567 | 15420.7900 | -2255.8667 | [-7884.2796, 2862.9456] | 0.448883 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 543.4833 | 549.4333 | 5.9500 | [-10.9077, 23.9842] | 0.531036 |
| total_tokens | plan_front -> plan_scatter | 20 | 28460.5233 | 26210.6433 | -2249.8800 | [-7885.4038, 2885.8753] | 0.450821 |
| duration_sec | plan_front -> plan_scatter | 20 | 179.2586 | 162.3651 | -16.8934 | [-64.1019, 27.6286] | 0.484985 |
