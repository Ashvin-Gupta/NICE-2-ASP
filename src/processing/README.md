# processing/ Directory

This directory contains all core Python modules that implement the NICE 2 ASP pipeline logic.

## Modules

### Core Pipeline Modules

#### `LLM_Inferencer.py`
Handles all interactions with LLM APIs (Claude, GPT, etc.).

**Key functions:**
- `run_constant_inference()`: Extracts constants from guidelines
- `run_predicate_inference()`: Extracts predicates from guidelines
- `run_rulegen_inference()`: Generates ASP rules
- `extract_atoms()`: Extracts atoms from patient vignettes (K2P)

**Supported LLM families:** Claude, GPT, Groq

#### `RuleProcessor.py`
Processes ASP rules and manages Clingo execution.

**Key functions:**
- `append_fired_rules()`: Adds fired/1 predicates to rules, comments out non-ASP lines
- `run_clingo_for_patients()`: Executes Clingo solver for each patient vignette
- `explain_fired_rules()`: Generates human-readable explanations

**Note:** Automatically comments out any non-ASP text when processing rules.

#### `ASPRuleParser.py`
Parses and analyzes ASP rule syntax.

**Key functions:**
- Parse ASP rules into structured format
- Extract rule components (head, body)
- Validate ASP syntax

#### `FileManager.py`
Handles file I/O operations.

**Key functions:**
- `load_file()`: Read files with proper encoding
- `save_file()`: Write files with proper formatting

### Graph Analysis Modules

#### `graph_utils.py`
Creates graph representations of ASP programs.

**Key functions:**
- `create_program_graph()`: Convert ASP program to graph structure
- Build adjacency matrices for rule dependencies

#### `graph_analysis.py`
Computes graph similarity metrics.

**Key functions:**
- `calculate_graph_similarity()`: Compare generated rules to ground truth
- Compute structural similarity using graph kernels

### Evaluation Modules

#### `review_K2P.py`
Evaluates K2P (Knowledge-to-Patient) performance.

**Key class:** `K2PReviewer`

**Functions:**
- `load_ground_truth()`: Load expected rule firings
- `load_clingo_output()`: Parse Clingo results
- `compute_metrics()`: Calculate Precision, Recall, F1
- `evaluate_and_save()`: Run full evaluation and save results

**Output:** Per-patient metrics saved to `reviews/K2P review/`

### Utility Modules

#### `pipeline_utils.py`
Utility functions for pipeline configuration and setup.

**Key functions:**
- `load_config()`: Load YAML configuration
- `setup_experiment_dir()`: Create output directory structure
- `setup_output_files()`: Configure output file paths
- `validate_pipeline_mode()`: Validate mode compatibility
- `process_prompt_template()`: Replace {ORGAN} placeholders in prompts
- `setup_processed_prompts()`: Create cancer-type-specific prompts

**ORGAN_MAPPING:** Maps cancer types to organ names (lung/pancreas)

## Module Dependencies

```
main.py
├── pipeline_utils.py (configuration & setup)
├── LLM_Inferencer.py (LLM interactions)
│   └── FileManager.py
├── RuleProcessor.py (ASP processing & Clingo)
│   └── FileManager.py
├── graph_utils.py (graph creation)
├── graph_analysis.py (similarity metrics)
│   └── graph_utils.py
└── review_K2P.py (K2P evaluation)
```

## Key Workflows

### D2K Pipeline
1. `LLM_Inferencer` extracts constants, predicates, generates rules
2. `graph_utils` creates graph representation
3. `graph_analysis` computes similarity to ground truth

### K2P Pipeline
1. `RuleProcessor.append_fired_rules()` prepares rules for Clingo
2. `LLM_Inferencer.extract_atoms()` extracts facts from patient vignettes
3. `RuleProcessor.run_clingo_for_patients()` executes solver
4. `RuleProcessor.explain_fired_rules()` generates explanations
5. `review_K2P` evaluates accuracy against ground truth

## Customization

To modify pipeline behavior:
- **Prompt engineering:** Edit prompt files in `input_files/prompt_files/`
- **LLM parameters:** Modify configuration files in `configs/`
- **Evaluation metrics:** Edit `graph_analysis.py` or `review_K2P.py`
- **Rule processing:** Edit `RuleProcessor.py`

