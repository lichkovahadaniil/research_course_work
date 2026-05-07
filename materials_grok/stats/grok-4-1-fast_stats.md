# Statistical Tests: grok-4.1-fast

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
| reachability | plan_front -> plan_scatter | 100 | 0.7300 | 0.7700 | 17 | 13 | 0.0400 | 1.3077 | 0.584665 | 0.584665 |
| executability | canonical -> plan_front | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| executability | canonical -> plan_scatter | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| executability | plan_front -> plan_scatter | 100 | 0.7400 | 0.7900 | 18 | 13 | 0.0500 | 1.3846 | 0.473130 | 0.473130 |
| non_executable_failure | canonical -> plan_front | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| non_executable_failure | canonical -> plan_scatter | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| non_executable_failure | plan_front -> plan_scatter | 100 | 0.2600 | 0.2100 | 13 | 18 | -0.0500 | 0.7222 | 0.473130 | 0.473130 |
| conditional_reachability | canonical -> plan_front | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| conditional_reachability | canonical -> plan_scatter | 0 | NA | NA | 0 | 0 | NA | NA | 1.000000 | 1.000000 |
| conditional_reachability | plan_front -> plan_scatter | 61 | 1.0000 | 0.9836 | 0 | 1 | -0.0164 | 0.0000 | 1.000000 | 1.000000 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | comparison | n | baseline mean | compared mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| plan_length | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| plan_length | plan_front -> plan_scatter | 60 | 20.9500 | 21.0667 | 0.1167 | 0.0056 | 0.0535 | 0.679870 | 0.729820 | 0.729820 |
| optimality_ratio | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| optimality_ratio | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| optimality_ratio | plan_front -> plan_scatter | 60 | 1.0670 | 1.0715 | 0.0044 | 0.0042 | 0.0480 | 0.711248 | 0.713710 | 0.713710 |
| first_failure_step | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| first_failure_step | plan_front -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| prompt_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| prompt_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| prompt_tokens | plan_front -> plan_scatter | 100 | 8639.9000 | 8672.9100 | 33.0100 | 0.0038 | 0.1000 | 0.319748 | 1.000000 | 1.000000 |
| completion_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| completion_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| completion_tokens | plan_front -> plan_scatter | 100 | 10833.2100 | 10983.4900 | 150.2800 | 0.0139 | 0.0164 | 0.869763 | 0.992310 | 0.992310 |
| reasoning_completion_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| reasoning_completion_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| reasoning_completion_tokens | plan_front -> plan_scatter | 100 | 10526.3100 | 10668.8300 | 142.5200 | 0.0135 | 0.0156 | 0.876385 | 0.992630 | 0.992630 |
| raw_completion_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| raw_completion_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| raw_completion_tokens | plan_front -> plan_scatter | 100 | 306.9000 | 314.6600 | 7.7600 | 0.0253 | 0.0408 | 0.683917 | 0.690370 | 0.690370 |
| total_tokens | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| total_tokens | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| total_tokens | plan_front -> plan_scatter | 100 | 19473.1100 | 19656.4000 | 183.2900 | 0.0094 | 0.0201 | 0.840831 | 0.991510 | 0.991510 |
| duration_sec | canonical -> plan_front | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| duration_sec | canonical -> plan_scatter | 0 | NA | NA | NA | NA | NA | NA | NA | NA |
| duration_sec | plan_front -> plan_scatter | 100 | 139.7285 | 169.2018 | 29.4733 | 0.2109 | 0.2919 | 0.004347 | 0.002160 | 0.002160 |

## Problem-Level Tests

Runs are averaged within each problem first. The test unit is the problem, not an individual run. `mean diff` is compared minus baseline, with a paired sign-flip permutation p-value and a bootstrap 95% CI over problems.

| metric | comparison | n problems | baseline mean | compared mean | mean diff | 95% CI | p perm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | plan_front -> plan_scatter | 20 | 0.7300 | 0.7700 | 0.0400 | [-0.0600, 0.1300] | 0.573242 |
| executability | plan_front -> plan_scatter | 20 | 0.7400 | 0.7900 | 0.0500 | [-0.0400, 0.1300] | 0.366211 |
| non_executable_failure | plan_front -> plan_scatter | 20 | 0.2600 | 0.2100 | -0.0500 | [-0.1300, 0.0400] | 0.366211 |
| conditional_reachability | plan_front -> plan_scatter | 18 | 1.0000 | 0.9722 | -0.0278 | [-0.0833, 0.0000] | 1.000000 |
| plan_length | plan_front -> plan_scatter | 19 | 27.3904 | 27.4719 | 0.0816 | [-0.4483, 0.6053] | 0.775391 |
| optimality_ratio | plan_front -> plan_scatter | 19 | 1.0853 | 1.0892 | 0.0038 | [-0.0114, 0.0191] | 0.635986 |
| first_failure_step | plan_front -> plan_scatter | 0 | NA | NA | NA | [NA, NA] | NA |
| prompt_tokens | plan_front -> plan_scatter | 20 | 8639.9000 | 8672.9100 | 33.0100 | [0.0000, 99.0300] | 1.000000 |
| completion_tokens | plan_front -> plan_scatter | 20 | 10833.2100 | 10983.4900 | 150.2800 | [-1872.6442, 1437.5255] | 0.966522 |
| reasoning_completion_tokens | plan_front -> plan_scatter | 20 | 10526.3100 | 10668.8300 | 142.5200 | [-1873.3273, 1440.9110] | 0.967468 |
| raw_completion_tokens | plan_front -> plan_scatter | 20 | 306.9000 | 314.6600 | 7.7600 | [-32.8503, 52.1312] | 0.740082 |
| total_tokens | plan_front -> plan_scatter | 20 | 19473.1100 | 19656.4000 | 183.2900 | [-1835.1525, 1454.3893] | 0.959467 |
| duration_sec | plan_front -> plan_scatter | 20 | 139.7285 | 169.2018 | 29.4733 | [0.2041, 59.4597] | 0.074080 |
