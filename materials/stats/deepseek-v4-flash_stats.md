# Statistical Tests: deepseek-v4-flash

Baseline order: `canonical`.
Compared orders: `disp_1`, `disp_2`, `disp_3`.

Pairing unit: `(problem, run)` within this model. Each test only uses pairs where both the baseline and compared order have an available value.

## Binary Metrics

Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while canonical fails; `c` means canonical succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.

| metric | order | n | canonical | order | b | c | risk diff | matched OR | p | p Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reachability | disp_1 | 100 | 0.6200 | 0.5800 | 13 | 17 | -0.0400 | 0.7647 | 0.584665 | 1.000000 |
| reachability | disp_2 | 100 | 0.6200 | 0.5900 | 17 | 20 | -0.0300 | 0.8500 | 0.742829 | 1.000000 |
| reachability | disp_3 | 100 | 0.6200 | 0.5200 | 11 | 21 | -0.1000 | 0.5238 | 0.110184 | 0.330552 |
| executability | disp_1 | 100 | 0.7600 | 0.6500 | 7 | 18 | -0.1100 | 0.3889 | 0.043285 | 0.129856 |
| executability | disp_2 | 100 | 0.7600 | 0.7600 | 17 | 17 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| executability | disp_3 | 100 | 0.7600 | 0.6900 | 14 | 21 | -0.0700 | 0.6667 | 0.310505 | 0.621009 |
| non_executable_failure | disp_1 | 100 | 0.2400 | 0.3500 | 18 | 7 | 0.1100 | 2.5714 | 0.043285 | 0.129856 |
| non_executable_failure | disp_2 | 100 | 0.2400 | 0.2400 | 17 | 17 | 0.0000 | 1.0000 | 1.000000 | 1.000000 |
| non_executable_failure | disp_3 | 100 | 0.2400 | 0.3100 | 21 | 14 | 0.0700 | 1.5000 | 0.310505 | 0.621009 |
| conditional_reachability | disp_1 | 58 | 0.8793 | 0.8966 | 7 | 6 | 0.0172 | 1.1667 | 1.000000 | 1.000000 |
| conditional_reachability | disp_2 | 59 | 0.8136 | 0.8305 | 7 | 6 | 0.0169 | 1.1667 | 1.000000 | 1.000000 |
| conditional_reachability | disp_3 | 55 | 0.8727 | 0.7818 | 2 | 7 | -0.0909 | 0.2857 | 0.179688 | 0.539062 |

## Numeric Metrics

Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.

| metric | order | n | canonical mean | order mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plan_length | disp_1 | 45 | 21.4889 | 19.5333 | -1.9556 | -0.0910 | -0.3169 | 0.039189 | 0.036480 | 0.109440 |
| plan_length | disp_2 | 42 | 21.0952 | 19.4048 | -1.6905 | -0.0801 | -0.2699 | 0.087802 | 0.107400 | 0.214800 |
| plan_length | disp_3 | 41 | 19.0244 | 17.3415 | -1.6829 | -0.0885 | -0.2672 | 0.094852 | 0.117580 | 0.214800 |
| optimality_ratio | disp_1 | 45 | 1.2147 | 1.0874 | -0.1273 | -0.1048 | -0.3220 | 0.036279 | 0.025267 | 0.075800 |
| optimality_ratio | disp_2 | 42 | 1.2403 | 1.1180 | -0.1223 | -0.0986 | -0.3036 | 0.055925 | 0.049830 | 0.099660 |
| optimality_ratio | disp_3 | 41 | 1.2183 | 1.0954 | -0.1229 | -0.1008 | -0.2984 | 0.063231 | 0.062660 | 0.099660 |
| first_failure_step | disp_1 | 17 | 23.0588 | 16.4118 | -6.6471 | -0.2883 | -0.3909 | 0.126549 | 0.132690 | 0.398071 |
| first_failure_step | disp_2 | 7 | 18.4286 | 19.7143 | 1.2857 | 0.0698 | 0.0538 | 0.891387 | 0.921875 | 1.000000 |
| first_failure_step | disp_3 | 10 | 18.1000 | 14.5000 | -3.6000 | -0.1989 | -0.2005 | 0.541761 | 0.556641 | 1.000000 |
| prompt_tokens | disp_1 | 100 | 10223.0500 | 10223.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | disp_2 | 100 | 10223.0500 | 10223.0500 | 0.0000 | 0.0000 | 0.0000 | 1.000000 | 1.000000 | 1.000000 |
| prompt_tokens | disp_3 | 100 | 10223.0500 | 10239.9700 | 16.9200 | 0.0017 | 0.1000 | 0.319748 | 1.000000 | 1.000000 |
| completion_tokens | disp_1 | 100 | 12927.4700 | 12227.8400 | -699.6300 | -0.0541 | -0.1633 | 0.105723 | 0.108400 | 0.325200 |
| completion_tokens | disp_2 | 100 | 12927.4700 | 12674.0500 | -253.4200 | -0.0196 | -0.0607 | 0.545219 | 0.544830 | 0.544830 |
| completion_tokens | disp_3 | 100 | 12927.4700 | 13609.3200 | 681.8500 | 0.0527 | 0.1489 | 0.139665 | 0.140640 | 0.325200 |
| reasoning_completion_tokens | disp_1 | 100 | 12346.0400 | 11677.9600 | -668.0800 | -0.0541 | -0.1567 | 0.120248 | 0.123210 | 0.369630 |
| reasoning_completion_tokens | disp_2 | 100 | 12346.0400 | 12111.5700 | -234.4700 | -0.0190 | -0.0563 | 0.574617 | 0.574510 | 0.574510 |
| reasoning_completion_tokens | disp_3 | 100 | 12346.0400 | 13048.8500 | 702.8100 | 0.0569 | 0.1546 | 0.125297 | 0.125980 | 0.369630 |
| raw_completion_tokens | disp_1 | 100 | 581.4300 | 549.8800 | -31.5500 | -0.0543 | -0.2908 | 0.004485 | 0.003450 | 0.010350 |
| raw_completion_tokens | disp_2 | 100 | 581.4300 | 562.4800 | -18.9500 | -0.0326 | -0.1919 | 0.057807 | 0.056780 | 0.113560 |
| raw_completion_tokens | disp_3 | 100 | 581.4300 | 560.4700 | -20.9600 | -0.0360 | -0.1688 | 0.094644 | 0.097470 | 0.113560 |
| total_tokens | disp_1 | 100 | 23150.5200 | 22450.8900 | -699.6300 | -0.0302 | -0.1633 | 0.105723 | 0.108400 | 0.325200 |
| total_tokens | disp_2 | 100 | 23150.5200 | 22897.1000 | -253.4200 | -0.0109 | -0.0607 | 0.545219 | 0.544830 | 0.544830 |
| total_tokens | disp_3 | 100 | 23150.5200 | 23849.2900 | 698.7700 | 0.0302 | 0.1537 | 0.127576 | 0.128660 | 0.325200 |
| duration_sec | disp_1 | 100 | 168.3130 | 148.0273 | -20.2857 | -0.1205 | -0.2458 | 0.015721 | 0.007060 | 0.021180 |
| duration_sec | disp_2 | 100 | 168.3130 | 155.2605 | -13.0525 | -0.0775 | -0.1531 | 0.128957 | 0.124540 | 0.249080 |
| duration_sec | disp_3 | 100 | 168.3130 | 165.9254 | -2.3876 | -0.0142 | -0.0270 | 0.787758 | 0.818630 | 0.818630 |
