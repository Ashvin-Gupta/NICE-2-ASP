# input_files/ Directory

This directory contains all input data used by the pipeline.

## Directory Structure

```
input_files/
├── input_guidelines/      # Clinical guideline text files
├── ground_truths/         # Human-authored ground truth ASP programs
├── prompt_files/          # LLM prompt templates
└── K2P/                   # Patient vignettes for K2P evaluation
```

## Subdirectories

### `input_guidelines/`
Contains the clinical guideline text files that serve as input to the pipeline.

**Files:**
- `lung_cancer_guidelines.txt`: NICE lung cancer guidelines
- `pancreatic_cancer_guidelines.txt`: NICE pancreatic cancer guidelines

These files contain the natural language clinical guidelines that the LLM will process.

### `ground_truths/`
Contains human-authored ASP programs used for evaluation.

**Files:**
- `GT_LC.lp`: Ground truth ASP rules for lung cancer (for D2K evaluation)
- `GT_PC.lp`: Ground truth ASP rules for pancreatic cancer (for D2K evaluation)
- `K2P_ground_truth.csv`: Ground truth rule firings for patient vignettes (for K2P evaluation)

The `.lp` files are used to evaluate structural similarity of generated rules.
The `.csv` file specifies which rules should fire for each patient vignette.

### `prompt_files/`
Contains LLM prompt templates that guide the model's ASP generation.

**Files:**
- `constant_prompt.txt`: Prompt for extracting constants from guidelines
- `predicate_prompt.txt`: Prompt for extracting predicates from guidelines
- `rule_generation_prompt.txt`: Prompt for generating ASP rules
- `in_context.txt`: In-context learning prompt with examples
- `zero_shot.txt`: Zero-shot prompt for direct ASP generation

**Note:** These prompts use `{ORGAN}` placeholder which is automatically replaced with "lung" or "pancreas" based on the cancer type.

### `K2P/`
Contains patient vignette data for Knowledge-to-Patient evaluation.

**Files:**
- `PC_descriptions.txt`: Patient case descriptions for pancreatic cancer
- `setupProgram.txt`: Prompt for extracting atoms from patient descriptions

**Note:** K2P evaluation is only available for pancreatic cancer.

## Usage

These files are automatically loaded by the pipeline based on the configuration file. Users typically don't need to access these files directly unless:
- Adding new guidelines
- Modifying prompts
- Updating ground truth data
- Adding new patient vignettes

