# Statistical Testing

This folder contains reproducible order-effect tests for the saved local `llm_result.json` files. No model/API calls are made.

Pairing is done within each model by `(problem, run)`: each compared order is matched with `canonical` for the same problem and run.

Binary metrics use exact McNemar tests. Numeric metrics use paired t-tests and sign-flip permutation tests.

Files:
- `deepseek-v4-flash_stats.json` / `deepseek-v4-flash_stats.md` / `deepseek-v4-flash_tests.csv`
- `glm-4-7-flash_stats.json` / `glm-4-7-flash_stats.md` / `glm-4-7-flash_tests.csv`
