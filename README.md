# research_course_work

Local pipeline for preparing shuffled PDDL domain variants, validating already generated plans, and building evaluation summaries and plots.

## Requirements

- Python 3
- VAL available on `PATH` as `validate`
- IPC 2023 benchmark files already present under `ipc2023-dataset-main/opt`
- Python dependencies from [requirements.txt](/Users/daniillickovaha/Documents/research/requirements.txt)

Install the Python packages with:

```bash
python3 -m pip install -r requirements.txt
```

## Sampling policy

The default experimental profile is a 5-problem sample per domain:

```text
p01,p05,p10,p15,p20
```

This is intentional experimental design, not a bug. You can override it with `--problems`, but every command defaults to that profile.

## Validation modes

The evaluator uses two VAL passes for different purposes:

- `validate -v`: strict scientific validation. Used for `parsable`, `executability`, `reachability`, `first_failure_step`, `non_executable_failure`, and `strict_final_value`.
- `validate -c`: legacy compatibility validation. Used only for legacy cost/gap metrics and for keeping continuity with the earlier pipeline.

Legacy `gap` and other cost-based comparisons are only computed for goal-reaching plans with a real VAL cost. Invalid plans, parse errors, execution failures, and executable-but-goal-not-reached plans now keep those values as `null`.

## Workflow

### 1. Prepare data

This copies the selected benchmark problems into `materials/` and generates the shuffled domain variants.

```bash
python3 main.py prepare --domains folding --problems p01,p05,p10,p15,p20
```

### 2. Print manual model-run commands

This only prints commands. It does not call any model provider on its own.

```bash
python3 main.py print-run-commands --domains folding --variants all --models openai/gpt-5-mini,x-ai/grok-4.1-fast
```

The printed commands call [manual_model_run.py](/Users/daniillickovaha/Documents/research/manual_model_run.py), which is the explicit opt-in entrypoint for model execution.

### 3. Run models manually

Take any printed command and run it yourself when you actually want a model call. Example:

```bash
python3 manual_model_run.py \
  --domain-path materials/folding/p01/canonical/domain.pddl \
  --problem-path materials/folding/p01/p01.pddl \
  --optimal-plan-path materials/folding/p01/p01.plan \
  --variant-dir materials/folding/p01/canonical \
  --model openai/gpt-5-mini
```

### 4. Recompute local metrics from existing artifacts

This revalidates the plans already stored in `materials/` and rewrites local `llm_result.json`, `llm_summary.json`, and `materials/metric.json`. No model calls are made here.

```bash
python3 main.py aggregate --domains folding
```

### 5. Build reports and plots

This reads the aggregated metrics and writes plots plus `report.md` per domain.

```bash
python3 main.py report --domains folding
```

## Artifact layout

- `llm_result.json`
  - `metrics.strict`: strict scientific metrics from `validate -v`
  - `metrics.legacy`: legacy cost/gap metrics from `validate -c`
  - `metrics.order`: corrected sequence-order distance metrics
- `llm_summary.json`
  - `strict_summary`
  - `legacy_summary`
  - `order_summary`
- `materials/metric.json`
  - domain-wide collected summaries used by reporting

## Shuffle metadata

Each `shuffle_meta.json` now records:

- `seed`
- `problem_id`
- `sampling_profile`
- `variant_generation_version`

This makes shuffled-domain generation reproducible and explicit.
