# configs/ Directory

This directory contains YAML configuration files that control pipeline execution.

## Files

### `lung_cancer_config.yaml`
Configuration for running the pipeline on lung cancer guidelines.

**Key settings:**
- `cancer_type`: "lung cancer"
- `pipeline_mode`: "D2K-only" (default, as K2P only works for pancreatic cancer)
- `version`: "D2K-Pipeline", "In-Context", or "No-Pipeline"
- `ground_truth`: Points to GT_LC.lp

### `pancreatic_cancer_config.yaml`
Configuration for running the pipeline on pancreatic cancer guidelines.

**Key settings:**
- `cancer_type`: "pancreatic cancer"
- `pipeline_mode`: "D2K+K2P" (default, can use all three modes)
- `version`: "D2K-Pipeline", "In-Context", or "No-Pipeline"
- `ground_truth`: Points to GT_PC.lp

## Configuration Parameters

### Experiment Settings
- `name`: Experiment identifier
- `output_dir`: Base directory for outputs (e.g., "src/output_files/CLAUDE")
- `model`: LLM model name (e.g., "claude-opus-4-1-20250805")
- `family`: Model family ("claude", "gpt", etc.)
- `temperature`: Sampling temperature (0.0 for deterministic)
- `version`: Pipeline version (D2K-Pipeline, In-Context, No-Pipeline)
- `cancer_type`: Cancer type ("lung cancer" or "pancreatic cancer")
- `pipeline_mode`: Execution mode (D2K-only, K2P-only, D2K+K2P)

### Input Files
All paths to input data including:
- Guidelines text files
- Prompt templates
- Ground truth files
- Patient vignettes (for K2P)

## Usage

To use a configuration file:

```bash
python main.py --config src/configs/lung_cancer_config.yaml
```

## Pipeline Modes

- **D2K-only**: Generates ASP rules and evaluates structural similarity
- **K2P-only**: Uses existing rules to predict patient outcomes (pancreatic cancer only)
- **D2K+K2P**: Full end-to-end pipeline (pancreatic cancer only)

## Customization

To create a custom configuration:
1. Copy an existing config file
2. Modify the parameters as needed
3. Run with: `python main.py --config src/configs/your_config.yaml`

