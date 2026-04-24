# research_course_work

Minimal local pipeline for the IPC 2023 `labyrinth` domain.

## Scope

- Domain: `labyrinth`
- Problems: `p01`-`p20`
- Models: `gpt-5-mini`, `deepseek-v3.2`
- Variants per problem:
  - `canonical`
  - `frequency`
  - `disp_1`
  - `disp_2`
  - `disp_3`

## Requirements

- Python 3
- VAL on `PATH` as `validate`
- IPC 2023 data under `ipc2023-dataset-main/opt`
- Packages from [requirements.txt](/Users/daniillickovaha/Documents/research/requirements.txt)

## Commands

Prepare base files and generate all variants:

```bash
python3 main.py prepare
python3 main.py prepare --force
```

Run model jobs:

```bash
python3 main.py models-run --models gpt-5-mini --orders frequency disp_3 --problems p01
python3 main.py models-run --models gpt-5-mini deepseek-v3.2 --orders canonical frequency disp_3 --runs 5
python3 main.py models-run --models deepseek-v3.2 --orders canonical --problems p01 p05 --runs 4 --force
```

For `gpt-5-mini`, the runtime resolves to `openai/gpt-5-mini`, pins the OpenRouter provider to `OpenAI`, and disables fallbacks.

Build reports:

```bash
python3 main.py report
```

## Output layout

Each model run writes `llm_result.json`, `llm.plan`, and `run_status.json` under:

```text
materials/<domain>/<problem>/<variant>/<run>/<model_dir>/
```

Per-order aggregates are refreshed under:

```text
materials/<domain>/<problem>/<variant>/aggregate/<model_dir>.json
```

Reports are written to:

```text
materials/<domain>/graph/
├── p01/
├── p02/
├── ...
└── p20/
```

Only per-problem barplots are generated.
