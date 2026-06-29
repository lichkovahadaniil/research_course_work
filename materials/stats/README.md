# Statistical Testing

This folder contains reproducible order-effect tests for the saved local `llm_result.json` files. No model/API calls are made.

McNemar and numeric tests are paired within each model by `(problem, run)`: primary tests match each compared order with `canonical`, and the second pass matches each other order with `plan_front`.
The `plan_front` baseline comparisons are included when both orders in the pair are present.
Problem-level tests average runs inside each problem before testing the paired problem differences.

Binary metrics use exact McNemar tests. Conditional reachability uses executable-plan denominators per order and Fisher's exact test. Numeric metrics use paired t-tests and sign-flip permutation tests.

Files:
- `deepseek-v4-flash_stats.json` / `deepseek-v4-flash_stats.md` / `deepseek-v4-flash_tests.csv`
- `gpt-oss-120b_stats.json` / `gpt-oss-120b_stats.md` / `gpt-oss-120b_tests.csv`
- `nemotron-3-super_stats.json` / `nemotron-3-super_stats.md` / `nemotron-3-super_tests.csv`
