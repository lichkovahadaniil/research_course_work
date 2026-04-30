# Statistical Tests: glm-4.7-flash

Baseline order: `canonical`.
Compared orders: `disp_1`, `disp_2`, `disp_3`.

Pairing unit: `(problem, run)` within this model. Each test only uses pairs where both the baseline and compared order have an available value.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while canonical fails; `c` means canonical succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | order | n | canonical | order | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | disp_1 | 40 | 0.0500 | 0.1000 | 3 | 1 | 0.0500 | 3.0000 | 0.625000 | 1.000000 |
| reachability | disp_2 | 40 | 0.0500 | 0.1000 | 3 | 1 | 0.0500 | 3.0000 | 0.625000 | 1.000000 |
| reachability | disp_3 | 40 | 0.0500 | 0.0250 | 0 | 1 | -0.0250 | 0.0000 | 1.000000 | 1.000000 |
| executability | disp_1 | 40 | 0.5250 | 0.6000 | 10 | 7 | 0.0750 | 1.4286 | 0.629059 | 1.000000 |
| executability | disp_2 | 40 | 0.5250 | 0.6500 | 14 | 9 | 0.1250 | 1.5556 | 0.404873 | 1.000000 |
| executability | disp_3 | 40 | 0.5250 | 0.4750 | 4 | 6 | -0.0500 | 0.6667 | 0.753906 | 1.000000 |
| non_executable_failure | disp_1 | 40 | 0.4750 | 0.4000 | 7 | 10 | -0.0750 | 0.7000 | 0.629059 | 1.000000 |
| non_executable_failure | disp_2 | 40 | 0.4750 | 0.3500 | 9 | 14 | -0.1250 | 0.6429 | 0.404873 | 1.000000 |
| non_executable_failure | disp_3 | 40 | 0.4750 | 0.5250 | 6 | 4 | 0.0500 | 1.5000 | 0.753906 | 1.000000 |
| conditional_reachability | disp_1 | 14 | 0.1429 | 0.2143 | 2 | 1 | 0.0714 | 2.0000 | 1.000000 | 1.000000 |
| conditional_reachability | disp_2 | 12 | 0.0833 | 0.0833 | 0 | 0 | 0.0000 | NA | 1.000000 | 1.000000 |
| conditional_reachability | disp_3 | 15 | 0.0667 | 0.0667 | 0 | 0 | 0.0000 | NA | 1.000000 | 1.000000 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | order | n | canonical mean | order mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | disp_1 | 1 | 8.0000 | 8.0000 | 0.0000 | 0.0000 | NA | NA | 1.000000 | 1.000000 |
| plan_length | disp_2 | 1 | 6.0000 | 8.0000 | 2.0000 | 0.3333 | NA | NA | 1.000000 | 1.000000 |
| plan_length | disp_3 | 1 | 6.0000 | 6.0000 | 0.0000 | 0.0000 | NA | NA | 1.000000 | 1.000000 |
| optimality_ratio | disp_1 | 1 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | NA | NA | 1.000000 | 1.000000 |
| optimality_ratio | disp_2 | 1 | 1.0000 | 1.3333 | 0.3333 | 0.3333 | NA | NA | 1.000000 | 1.000000 |
| optimality_ratio | disp_3 | 1 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | NA | NA | 1.000000 | 1.000000 |
| first_failure_step | disp_1 | 3 | 2.0000 | 2.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| first_failure_step | disp_2 | 3 | 3.6667 | 3.6667 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| first_failure_step | disp_3 | 6 | 5.6667 | 3.8333 | -1.8333 | -0.3235 | -0.8579 | 0.089589 | 0.187500 | 0.562500 |
| prompt_tokens | disp_1 | 40 | 8542.3000 | 8542.3000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | disp_2 | 40 | 8542.3000 | 8542.3000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | disp_3 | 40 | 8542.3000 | 8542.3000 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| completion_tokens | disp_1 | 40 | 14159.3750 | 13714.8000 | -444.5750 | -0.0314 | -0.1178 | 0.460752 | 0.468400 | 0.468400 |
| completion_tokens | disp_2 | 40 | 14159.3750 | 13128.5000 | -1030.8750 | -0.0728 | -0.2717 | 0.093609 | 0.092590 | 0.185180 |
| completion_tokens | disp_3 | 40 | 14159.3750 | 13016.3750 | -1143.0000 | -0.0807 | -0.3354 | 0.040303 | 0.039940 | 0.119820 |
| reasoning_completion_tokens | disp_1 | 40 | 14159.3750 | 13714.8000 | -444.5750 | -0.0314 | -0.1178 | 0.460752 | 0.468400 | 0.468400 |
| reasoning_completion_tokens | disp_2 | 40 | 14159.3750 | 13128.5000 | -1030.8750 | -0.0728 | -0.2717 | 0.093609 | 0.092590 | 0.185180 |
| reasoning_completion_tokens | disp_3 | 40 | 14159.3750 | 13016.3750 | -1143.0000 | -0.0807 | -0.3354 | 0.040303 | 0.039940 | 0.119820 |
| raw_completion_tokens | disp_1 | 40 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | disp_2 | 40 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| raw_completion_tokens | disp_3 | 40 | 0.0000 | 0.0000 | 0.0000 | NA | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| total_tokens | disp_1 | 40 | 22701.6750 | 22257.1000 | -444.5750 | -0.0196 | -0.1178 | 0.460752 | 0.468400 | 0.468400 |
| total_tokens | disp_2 | 40 | 22701.6750 | 21670.8000 | -1030.8750 | -0.0454 | -0.2717 | 0.093609 | 0.092590 | 0.185180 |
| total_tokens | disp_3 | 40 | 22701.6750 | 21558.6750 | -1143.0000 | -0.0503 | -0.3354 | 0.040303 | 0.039940 | 0.119820 |
| duration_sec | disp_1 | 40 | 304.1427 | 298.9207 | -5.2220 | -0.0172 | -0.0289 | 0.855959 | 0.856050 | 0.856050 |
| duration_sec | disp_2 | 40 | 304.1427 | 241.4105 | -62.7322 | -0.2063 | -0.4256 | 0.010418 | 0.009850 | 0.029550 |
| duration_sec | disp_3 | 40 | 304.1427 | 276.7300 | -27.4128 | -0.0901 | -0.1779 | 0.267531 | 0.268470 | 0.536940 |
