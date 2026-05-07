# Statistical Tests: gpt-oss-120b

Baseline order: `canonical`.
Canonical compared orders: `plan_front`, `plan_scatter`.
Extra comparisons: `plan_front` vs `plan_scatter`.

Pairing unit: `(problem, run)` within this model. Each test only uses pairs where both the baseline and compared order have an available value.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while baseline fails; `c` means baseline succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | comparison | n | baseline | compared | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | canonical -> plan_front | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| reachability | canonical -> plan_scatter | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| reachability | plan_front -> plan_scatter | 398 | 0.1055 | 0.0628 | 6 | 23 | -0.0427 | 0.2609 | 0.002316 | 0.002316 |
| executability | canonical -> plan_front | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| executability | canonical -> plan_scatter | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| executability | plan_front -> plan_scatter | 398 | 0.3618 | 0.3693 | 81 | 78 | 0.0075 | 1.0385 | 0.874040 | 0.874040 |
| non_executable_failure | canonical -> plan_front | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| non_executable_failure | plan_front -> plan_scatter | 398 | 0.6382 | 0.6307 | 78 | 81 | -0.0075 | 0.9630 | 0.874040 | 0.874040 |
| conditional_reachability | canonical -> plan_front | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| conditional_reachability | canonical -> plan_scatter | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 66 | 0.4091 | 0.2879 | 0 | 8 | -0.1212 | 0.0000 | 0.007812 | 0.007812 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| plan_length | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| plan_length | plan_front -> plan_scatter | 398 | 10.2412 | 8.0704 | -2.1709 | -0.2120 | -0.1513 | 0.002712 | 0.001670 | 0.001670 |
| optimality_ratio | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| optimality_ratio | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| optimality_ratio | plan_front -> plan_scatter | 19 | 1.0468 | 1.0132 | -0.0336 | -0.0321 | -0.2921 | 0.219145 | 0.375000 | 0.375000 |
| execution_progress | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| execution_progress | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| execution_progress | plan_front -> plan_scatter | 398 | 0.4599 | 0.4491 | -0.0108 | -0.0235 | -0.0188 | 0.707707 | 0.710960 | 0.710960 |
| first_failure_step | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | plan_front -> plan_scatter | 65 | 3.8615 | 2.4308 | -1.4308 | -0.3705 | -0.5782 | 0.000016 | 0.000010 | 0.000010 |
| prompt_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| prompt_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| prompt_tokens | plan_front -> plan_scatter | 398 | 8750.1181 | 8749.9874 | -0.1307 | -0.0000 | -0.0434 | 0.386797 | 0.423850 | 0.423850 |
| completion_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| completion_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| completion_tokens | plan_front -> plan_scatter | 398 | 838.9296 | 709.5980 | -129.3317 | -0.1542 | -0.1860 | 0.000236 | 0.000230 | 0.000230 |
| reasoning_completion_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| reasoning_completion_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| reasoning_completion_tokens | plan_front -> plan_scatter | 398 | 766.1608 | 640.5930 | -125.5678 | -0.1639 | -0.1806 | 0.000355 | 0.000310 | 0.000310 |
| raw_completion_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| raw_completion_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| raw_completion_tokens | plan_front -> plan_scatter | 398 | 72.7688 | 69.0050 | -3.7638 | -0.0517 | -0.0228 | 0.648862 | 0.657680 | 0.657680 |
| total_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| total_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| total_tokens | plan_front -> plan_scatter | 398 | 9589.0477 | 9459.5854 | -129.4623 | -0.0135 | -0.1863 | 0.000232 | 0.000200 | 0.000200 |
| duration_sec | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| duration_sec | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| duration_sec | plan_front -> plan_scatter | 398 | 5.6229 | 4.8514 | -0.7715 | -0.1372 | -0.0564 | 0.261214 | 0.261100 | 0.261100 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> plan_scatter | 20 | 0.1050 | 0.0625 | -0.0425 | [-0.1100, 0.0000] | 0.500000 |
| executability | plan_front -> plan_scatter | 20 | 0.3608 | 0.3689 | 0.0082 | [-0.0900, 0.1032] | 0.883041 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.6392 | 0.6311 | -0.0082 | [-0.1032, 0.0900] | 0.883041 |
| conditional_reachability | plan_front -> plan_scatter | 14 | 0.2063 | 0.1457 | -0.0606 | [-0.1558, 0.0000] | 0.500000 |
| plan_length | plan_front -> plan_scatter | 20 | 10.2046 | 8.0354 | -2.1692 | [-4.4574, 0.1126] | 0.080172 |
| optimality_ratio | plan_front -> plan_scatter | 3 | 1.0228 | 1.0474 | 0.0246 | [-0.0513, 0.1250] | 1.000000 |
| execution_progress | plan_front -> plan_scatter | 20 | 0.4585 | 0.4484 | -0.0100 | [-0.1062, 0.0808] | 0.838749 |
| first_failure_step | plan_front -> plan_scatter | 20 | 3.9993 | 2.4269 | -1.5725 | [-2.2967, -0.9248] | 0.000034 |
| prompt_tokens | plan_front -> plan_scatter | 20 | 8750.9942 | 8750.8642 | -0.1300 | [-0.4200, 0.1658] | 0.418793 |
| completion_tokens | plan_front -> plan_scatter | 20 | 838.3176 | 709.5441 | -128.7736 | [-218.3880, -37.6726] | 0.012922 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 765.9126 | 640.8841 | -125.0286 | [-214.6842, -35.3183] | 0.014843 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 72.4050 | 68.6600 | -3.7450 | [-30.8558, 21.1302] | 0.770294 |
| total_tokens | plan_front -> plan_scatter | 20 | 9589.3118 | 9460.4083 | -128.9036 | [-218.6189, -37.7497] | 0.012875 |
| duration_sec | plan_front -> plan_scatter | 20 | 5.6119 | 4.8506 | -0.7613 | [-2.4559, 0.9493] | 0.408600 |
