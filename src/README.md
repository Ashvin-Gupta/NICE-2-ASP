# src/ Directory

This directory contains all source code, configuration files, input data, and output results for the NICE 2 ASP pipeline.

## Directory Structure

```
src/
├── configs/           # Pipeline configuration files
├── input_files/       # Input data (guidelines, prompts, ground truths)
├── output_files/      # Generated results and evaluation metrics
├── processing/        # Core pipeline processing modules
├── resources/         # API keys and other resources
└── review/            # Review dataset builders
```

## Key Directories

### `configs/`
Contains YAML configuration files for different cancer types. See [configs/README.md](configs/README.md) for details.

### `input_files/`
Contains all input data including clinical guidelines, prompt templates, and ground truth files. See [input_files/README.md](input_files/README.md) for details.

### `output_files/`
Contains all pipeline outputs organized by model and cancer type. **This is where you'll find all results.** See [output_files/README.md](output_files/README.md) for details.

### `processing/`
Contains the core Python modules that implement the pipeline logic. See [processing/README.md](processing/README.md) for details.

### `resources/`
Contains API keys for LLM services (not committed to version control).

### `review/`
Contains utilities for building review datasets from pipeline outputs.

## Quick Navigation

**To find pipeline results:**
- Generated ASP rules → `output_files/{MODEL}/{cancer_type}/D2K/rulegen_response.txt`
- Graph metrics → `output_files/{MODEL}/reviews/structural review D2K/{cancer_type}_graph_metrics.csv`
- K2P metrics → `output_files/{MODEL}/reviews/K2P review/{cancer_type}_K2P_review.csv`

**To modify pipeline behavior:**
- Configuration → `configs/{cancer_type}_config.yaml`
- Prompts → `input_files/prompt_files/`
- Processing logic → `processing/`

