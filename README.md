# research_course_work

Minimal local pipeline for two IPC 2023 domains: `folding` and `labyrinth`.

## Scope

- Domains: `folding`, `labyrinth`
- Problems: `p01`-`p20`
- Models: `gpt-5-mini`, `grok-4.1-fast`, `qwen/qwen3.5-35b-a3b:alibaba`
- Variants per problem:
  - `frequency`
  - `dispersion_01`
  - `dispersion_02`
  - `dispersion_03`
  - `dispersion_04`
  - `dispersion_05`

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
python3 main.py models-run --domain folding
python3 main.py models-run --domain labyrinth --problems p01 p05 p20
python3 main.py models-run --all
```

Build reports:

```bash
python3 main.py report
```

## Output layout

Each model run writes `llm_result.json`, `llm.plan`, and `run_status.json` under:

```text
materials/<domain>/<problem>/<variant>/<model_dir>/
```

Reports are written to:

```text
materials/<domain>/graph/
├── p01/
├── p02/
├── ...
├── p20/
└── summary/
```

Only barplots are generated.
