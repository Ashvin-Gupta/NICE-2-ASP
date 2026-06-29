# configs/

YAML configuration files that control pipeline execution.

## Files

- `lung_cancer_config.yaml` — lung cancer, `D2K-only` mode by default
- `pancreatic_cancer_config.yaml` — pancreatic cancer, `D2K+K2P` mode by default

## Key parameters

| Parameter | Description | Example values |
|---|---|---|
| `model` | Claude model ID | `claude-sonnet-4-6`, `claude-opus-4-8` |
| `family` | Model provider | `claude` |
| `temperature` | Sampling temperature | `0.0` (deterministic) |
| `version` | Prompting strategy | `D2K-Pipeline`, `In-Context`, `No-Pipeline` |
| `pipeline_mode` | Which stages to run | `D2K-only`, `K2P-only`, `D2K+K2P` |
| `cancer_type` | Cancer guideline to process | `lung cancer`, `pancreatic cancer` |
| `output_dir` | Base directory for outputs | `src/output_files/MY_RUN` |

**Note:** `K2P-only` and `D2K+K2P` modes only work with `pancreatic cancer`.
