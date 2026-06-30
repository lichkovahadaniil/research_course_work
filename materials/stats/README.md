# Statistical Testing

This folder contains reproducible order-effect tests for the saved local `llm_result.json` files. No model/API calls are made.

McNemar and numeric tests are paired within each model by `(problem, run)`: each compared order is matched with `canonical`.
Problem-level tests average runs inside each problem before testing the paired problem differences.

Binary metrics use exact McNemar tests. Conditional reachability uses executable-plan denominators per order and Fisher's exact test. Numeric metrics use paired t-tests and sign-flip permutation tests.

## Metric Semantics

- `parsable`: strict VAL parse-quality flag saved in `metrics.strict`; it is not itself a statistical-test metric.
- `reachability`: 1 when strict VAL reports `Plan valid`, otherwise 0.
- `executability`: 1 when strict VAL reports successful execution or a valid plan, otherwise 0.
- `non_executable_failure`: 1 when strict validation records a parse error, state execution error, or validator timeout; otherwise 0.
- `conditional_reachability`: reachability among executable plans only. Non-executable plans are excluded from that order's denominator.
- `plan_length`: analysis length used by tests and graphs. For `parsable=true` and `reachability=true`, this is strict VAL plan length from the saved log. For `parsable=false`, `reachability=false`, or missing validation metrics, this is missing and excluded from numeric summaries.
- `optimality_ratio`: legacy VAL cost divided by reference optimal cost; only defined for plans that reached the goal.
- `execution_progress`: strict validation progress. Parse errors are 0; state-execution errors use `first_failure_step / (plan_length + 1)` when available; other strict outcomes with a known plan length are 1.
- `first_failure_step`: first failed execution step parsed from strict VAL output; only defined for state execution failures where VAL reports the step.
- `prompt_tokens`, `completion_tokens`, `reasoning_completion_tokens`, `raw_completion_tokens`, `total_tokens`: provider token usage normalized from the saved response payload.
- `duration_sec`: saved model-call duration in seconds, when available.

Files:
- `deepseek-v4-flash_stats.json` / `deepseek-v4-flash_stats.md` / `deepseek-v4-flash_tests.csv`
- `gpt-oss-120b_stats.json` / `gpt-oss-120b_stats.md` / `gpt-oss-120b_tests.csv`
- `nemotron-3-super_stats.json` / `nemotron-3-super_stats.md` / `nemotron-3-super_tests.csv`
