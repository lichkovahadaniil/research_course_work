# folding report

Problems covered in summary: p01, p05, p10, p15

Per-problem graphs are stored under `materials/folding/graph/<problem>/`.
Domain summary graphs are stored under `materials/folding/graph/summary/`.

## p01

| variant | model | parsable | plan_length | executability | reachability | conditional_reachability | first_failure_step | optimality_ratio | non_executable_failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| canonical | gpt-5-mini | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| canonical | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| canonical | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| canonical | qwen3-5-35b-a3b-alibaba | 1 | 77.0000 | 0 | 0 | null | 8.0000 | null | state_execution_error |
| optimal | gpt-5-mini | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| optimal | grok-4-1-fast | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| optimal | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| optimal | qwen3-5-35b-a3b-alibaba | 1 | 77.0000 | 0 | 0 | null | 8.0000 | null | state_execution_error |
| frequency | gpt-5-mini | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| frequency | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| frequency | mimo-v2-flash | 1 | 16.0000 | 0 | 0 | null | 10.0000 | null | state_execution_error |
| frequency | qwen3-5-35b-a3b-alibaba | 1 | 77.0000 | 0 | 0 | null | 8.0000 | null | state_execution_error |
| dispersion | gpt-5-mini | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| dispersion | grok-4-1-fast | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| dispersion | mimo-v2-flash | 1 | 16.0000 | 0 | 0 | null | 9.0000 | null | state_execution_error |
| dispersion | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_01 | gpt-5-mini | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| random_01 | grok-4-1-fast | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| random_01 | mimo-v2-flash | 1 | 16.0000 | 0 | 0 | null | 9.0000 | null | state_execution_error |
| random_01 | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_02 | gpt-5-mini | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| random_02 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_02 | mimo-v2-flash | 1 | 17.0000 | 0 | 0 | null | 8.0000 | null | state_execution_error |
| random_02 | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_03 | gpt-5-mini | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| random_03 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_03 | mimo-v2-flash | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_03 | qwen3-5-35b-a3b-alibaba | 1 | 77.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_04 | gpt-5-mini | 1 | 70.0000 | 0 | 0 | null | 44.0000 | null | state_execution_error |
| random_04 | grok-4-1-fast | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| random_04 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_04 | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_05 | gpt-5-mini | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| random_05 | grok-4-1-fast | 1 | 70.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| random_05 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_05 | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |

## p05

| variant | model | parsable | plan_length | executability | reachability | conditional_reachability | first_failure_step | optimality_ratio | non_executable_failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| canonical | gpt-5-mini | 1 | 1.0000 | 1 | 0 | 0 | null | null | null |
| canonical | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| canonical | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| canonical | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
| optimal | gpt-5-mini | 1 | 304.0000 | 0 | 0 | null | 72.0000 | null | state_execution_error |
| optimal | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| optimal | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| optimal | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| frequency | gpt-5-mini | 1 | 303.0000 | 0 | 0 | null | 86.0000 | null | state_execution_error |
| frequency | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| frequency | mimo-v2-flash | 1 | 14.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| frequency | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| dispersion | gpt-5-mini | 1 | 304.0000 | 0 | 0 | null | 86.0000 | null | state_execution_error |
| dispersion | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| dispersion | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| dispersion | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_01 | gpt-5-mini | 1 | 14.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_01 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_01 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_01 | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_02 | gpt-5-mini | 1 | 14.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_02 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_02 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_02 | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_03 | gpt-5-mini | 1 | 292.0000 | 0 | 0 | null | 104.0000 | null | state_execution_error |
| random_03 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_03 | mimo-v2-flash | 1 | 14.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_03 | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_04 | gpt-5-mini | 1 | 304.0000 | 0 | 0 | null | 86.0000 | null | state_execution_error |
| random_04 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_04 | mimo-v2-flash | 1 | 14.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_04 | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_05 | gpt-5-mini | 1 | 14.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_05 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_05 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_05 | qwen3-5-35b-a3b-alibaba | 1 | 306.0000 | 0 | 0 | null | 18.0000 | null | state_execution_error |

## p10

| variant | model | parsable | plan_length | executability | reachability | conditional_reachability | first_failure_step | optimality_ratio | non_executable_failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| canonical | gpt-5-mini | 1 | 179.0000 | 0 | 0 | null | 31.0000 | null | state_execution_error |
| canonical | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| canonical | mimo-v2-flash | 1 | 10.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| canonical | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| optimal | gpt-5-mini | 1 | 178.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| optimal | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| optimal | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| optimal | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| frequency | gpt-5-mini | 1 | 28.0000 | 1 | 0 | 0 | null | null | null |
| frequency | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| frequency | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| frequency | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| dispersion | gpt-5-mini | 1 | 178.0000 | 0 | 0 | null | 30.0000 | null | state_execution_error |
| dispersion | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| dispersion | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| dispersion | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_01 | gpt-5-mini | 1 | 10.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_01 | grok-4-1-fast | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_01 | mimo-v2-flash | 1 | 10.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_01 | qwen3-5-35b-a3b-alibaba | 1 | 442.0000 | 0 | 0 | null | 14.0000 | null | state_execution_error |
| random_02 | gpt-5-mini | 1 | 28.0000 | 1 | 0 | 0 | null | null | null |
| random_02 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_02 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_02 | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_03 | gpt-5-mini | 1 | 178.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| random_03 | grok-4-1-fast | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_03 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_03 | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_04 | gpt-5-mini | 1 | 28.0000 | 1 | 0 | 0 | null | null | null |
| random_04 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_04 | mimo-v2-flash | 1 | 10.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_04 | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_05 | gpt-5-mini | 1 | 178.0000 | 0 | 0 | null | 30.0000 | null | state_execution_error |
| random_05 | grok-4-1-fast | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_05 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_05 | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |

## p15

| variant | model | parsable | plan_length | executability | reachability | conditional_reachability | first_failure_step | optimality_ratio | non_executable_failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| canonical | gpt-5-mini | 1 | 124.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| canonical | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| canonical | mimo-v2-flash | 1 | 7.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| canonical | qwen3-5-35b-a3b-alibaba | 1 | 29.0000 | 0 | 0 | null | 14.0000 | null | state_execution_error |
| optimal | gpt-5-mini | 1 | 1.0000 | 1 | 0 | 0 | null | null | null |
| optimal | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| optimal | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| optimal | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
| frequency | gpt-5-mini | 1 | 124.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| frequency | grok-4-1-fast | 1 | 124.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| frequency | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| frequency | qwen3-5-35b-a3b-alibaba | 1 | 131.0000 | 0 | 0 | null | 14.0000 | null | state_execution_error |
| dispersion | gpt-5-mini | 1 | 127.0000 | 0 | 0 | null | 66.0000 | null | state_execution_error |
| dispersion | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| dispersion | mimo-v2-flash | 1 | 7.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| dispersion | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_01 | gpt-5-mini | 1 | 7.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_01 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_01 | mimo-v2-flash | 1 | 7.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_01 | qwen3-5-35b-a3b-alibaba | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_02 | gpt-5-mini | 1 | 124.0000 | 1 | 1 | 1 | null | 1.0000 | null |
| random_02 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_02 | mimo-v2-flash | 1 | 7.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_02 | qwen3-5-35b-a3b-alibaba | 1 | 131.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_03 | gpt-5-mini | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_03 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_03 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_03 | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_04 | gpt-5-mini | 1 | 124.0000 | 0 | 0 | null | 42.0000 | null | state_execution_error |
| random_04 | grok-4-1-fast | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_04 | mimo-v2-flash | 1 | 0.0000 | 1 | 0 | 0 | null | null | null |
| random_04 | qwen3-5-35b-a3b-alibaba | 1 | 131.0000 | 0 | 0 | null | 14.0000 | null | state_execution_error |
| random_05 | gpt-5-mini | 1 | 131.0000 | 0 | 0 | null | 14.0000 | null | state_execution_error |
| random_05 | grok-4-1-fast | 0 | null | 0 | 0 | null | null | null | parse_error |
| random_05 | mimo-v2-flash | 1 | 7.0000 | 0 | 0 | null | 2.0000 | null | state_execution_error |
| random_05 | qwen3-5-35b-a3b-alibaba | 0 | null | 0 | 0 | null | null | null | parse_error |
