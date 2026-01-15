# NICE2ASP2: Clinical Guidelines to Answer Set Programming

This repository contains the implementation of a pipeline for translating clinical guidelines (specifically NICE cancer guidelines) into Answer Set Programming (ASP) rules using Large Language Models (LLMs).

## Metadata

**Purpose**: Computational representation of clinical guidelines as formal knowledge bases  
**Clinical Domains**: Pancreatic Cancer (PC), Lung Cancer (LC)  
**Target Users**: Researchers, clinical guideline developers, knowledge engineers, AI in healthcare researchers  
**Programming Languages**: Python 3.12+, Answer Set Programming (ASP)  
**Key Dependencies**: PyTorch, Anthropic/OpenAI APIs, Clingo (ASP solver), NetworkX  
**License**: MIT License (see [LICENSE](LICENSE))

## Table of Contents
- [Metadata](#metadata)
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Pipeline](#running-the-pipeline)
- [Project Structure](#project-structure)
- [Experiments](#experiments)
- [Citation](#citation)
- [License](#license)

## Overview

### Purpose of this Computational Biomedical Knowledge Base (CBK)

This project creates **formal, computable representations of clinical guidelines** as Answer Set Programming (ASP) knowledge bases. The resulting CBK enables:
- **Automated reasoning** about clinical recommendations
- **Patient-specific recommendations** based on their characteristics
- **Validation and verification** of guideline consistency
- **Explainable AI** for clinical decision support

### Clinical Domains

Currently supports two cancer types from NICE (National Institute for Health and Care Excellence) guidelines:
1. **Pancreatic Cancer (PC)**: Full D2K+K2P pipeline with patient vignette evaluation
2. **Lung Cancer (LC)**: D2K pipeline with structural evaluation

### Pipeline Overview

The NICE2ASP2 project implements two main pipelines:

**Data-to-Knowledge (D2K) Pipeline:**
1. Extracts constants from clinical guidelines (medical entities)
2. Identifies predicates and their relationships (connections between entities)
3. Generates ASP rules that formalize the guidelines (logical rules)
4. Evaluates the generated rules against ground truth (structural similarity)

**Knowledge-to-Patient (K2P) Pipeline:**
5. Applies rules to patient vignettes (real-world test cases)
6. Evaluates prediction accuracy (precision, recall, F1)

The system supports multiple LLM backends (GPT, Claude, etc.) and various prompting strategies (zero-shot, in-context learning, and the full D2K pipeline).

### Target Users

- **Researchers**: Studying clinical guideline formalization and LLM capabilities
- **Guideline Developers**: Testing and validating guideline consistency
- **Knowledge Engineers**: Building computable clinical knowledge bases
- **AI in Healthcare Researchers**: Developing explainable clinical decision support systems

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.12** or higher
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Clingo** (ASP solver) - Install via:
  ```bash
  # macOS
  brew install clingo
  
  # Ubuntu/Debian
  sudo apt-get install gringo
  
  # Or download from: https://potassco.org/clingo/
  ```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ashvin-Gupta/NICE2ASP2.git
cd NICE2ASP2
```

### 2. Create a Virtual Environment

It's strongly recommended to use a virtual environment to avoid dependency conflicts:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required packages including:
- LLM APIs (OpenAI, Anthropic, Groq)
- Data processing libraries (pandas, numpy, PyYAML)
- Graph analysis tools (networkx, GraKeL)

### 4. Configure API Keys

**Important:** You need to set up your API keys for the LLM services you plan to use.

Edit the file `src/resources/API_KEYS.py` and add your own API keys:

```python
API_KEYS = {  
    'ANTHROPIC_API_KEY': 'your-anthropic-key-here',
    'GROQ_API_KEY': 'your-groq-key-here',
    'OPENAI_API_KEY': 'your-openai-key-here',
    'OPENROUTER_API_KEY': 'your-openrouter-key-here'
}
```

**Note:** Never commit your API keys to version control. Consider using environment variables or a `.env` file for production use.

## Configuration

The pipeline uses separate configuration files for different cancer types, located in `src/configs/`:

- **`lung_cancer_config.yaml`**: Configuration for lung cancer guidelines
- **`pancreatic_cancer_config.yaml`**: Configuration for pancreatic cancer guidelines

Each configuration file controls:

- **Experiment settings**: model selection, temperature, output directory
- **Cancer type**: which guidelines to process
- **Pipeline mode**: D2K-only, K2P-only, or D2K+K2P
- **Pipeline version**: D2K-Pipeline, In-Context, or No-Pipeline (zero-shot)
- **Input/output file paths**

### Example Configuration (Lung Cancer)

```yaml
experiment:
  name: "lung_cancer_guidelines"
  output_dir: "src/output_files/CLAUDE"
  model: "claude-opus-4-1-20250805"
  family: "claude"
  temperature: 0.0
  version: D2K-Pipeline  # Options: No-Pipeline, In-Context, D2K-Pipeline
  cancer_type: "lung cancer"
  pipeline_mode: "D2K-only"  # Options: D2K-only, K2P-only, D2K+K2P

input_files:
  problem_text: "src/input_files/input_guidelines/lung_cancer_guidelines.txt"
  constant_prompt: "src/input_files/prompt_files/constant_prompt.txt"
  # ... more paths
  ground_truth: "src/input_files/ground_truths/GT_LC.lp"
```

### Pipeline Modes

The pipeline supports three execution modes:

1. **D2K-only**: Runs only the Data-to-Knowledge pipeline (works with both cancer types)
   - Extracts constants, predicates, and generates ASP rules
   - Performs graph analysis against ground truth

2. **K2P-only**: Runs only the Knowledge-to-Prediction pipeline (pancreatic cancer only)
   - Requires pre-existing ASP rules from a previous D2K run
   - Applies rules to patient vignettes and evaluates performance

3. **D2K+K2P**: Runs both pipelines end-to-end (pancreatic cancer only)
   - Generates ASP rules from guidelines
   - Applies rules to patient vignettes
   - Evaluates both structural similarity and prediction accuracy

**Note:** K2P modes only work with pancreatic cancer guidelines as patient vignettes are only available for pancreatic cancer.

## Running the Pipeline

### 1. Verify Installation

First, ensure all imports work correctly:

```bash
python -c "import yaml, pandas, anthropic, openai; print('All dependencies loaded successfully!')"
```

### 2. Run the Main Pipeline

The main pipeline is executed via `main.py` with a required `--config` argument:

```bash
# Run lung cancer pipeline (D2K-only mode)
python main.py --config src/configs/lung_cancer_config.yaml

# Run pancreatic cancer pipeline (D2K+K2P mode)
python main.py --config src/configs/pancreatic_cancer_config.yaml

# Short form using -c flag
python main.py -c src/configs/lung_cancer_config.yaml
```

### 3. View Help and Examples

To see all available options:

```bash
python main.py --help
```

This will display:
```
usage: main.py [-h] --config CONFIG

Run NICE 2 ASP Pipeline for lung or pancreatic cancer guidelines

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to configuration YAML file

Examples:
  # Run lung cancer pipeline with D2K-only mode
  python main.py --config src/configs/lung_cancer_config.yaml
  
  # Run pancreatic cancer pipeline with D2K+K2P mode
  python main.py --config src/configs/pancreatic_cancer_config.yaml
```

### 4. Pipeline Stages

The pipeline executes the following stages:

#### a. D2K Pipeline (Data-to-Knowledge)

1. **Constant Extraction**: Identifies domain constants from guidelines
2. **Predicate Extraction**: Extracts predicates and relationships
3. **Rule Generation**: Generates ASP rules based on constants and predicates

#### b. Baseline Methods

- **Zero-shot**: Direct ASP generation without intermediate steps
- **In-context**: ASP generation with examples

#### c. Graph Analysis

Compares generated ASP programs with ground truth using:
- Structural similarity metric based of adjacency matricies

#### d. K2P Analysis (Knowledge-to-Patient)

1. Extract atoms from patient vignettes
2. Run Clingo solver on patient cases
3. Generate explanations for fired rules

### 5. Output Files

Results are now organized in a structured directory hierarchy:

```
src/output_files/
└── CLAUDE/
    ├── reviews/
    │   ├── structural review D2K/
    │   │   ├── lung cancer_graph_metrics.csv
    │   │   └── pancreatic cancer_graph_metrics.csv
    │   │
    │   └── K2P review/
    │       └── pancreatic cancer_K2P_review.csv
    │
    └── pancreatic cancer/
        ├── config.yaml                # Copy of experiment configuration
        │
        ├── D2K/                       # D2K Pipeline outputs
        │   ├── constant_response.txt
        │   ├── predicate_response.txt
        │   └── rulegen_response.txt
        │
        ├── in-context/                # In-context baseline
        │   └── in_context_response.txt
        │
        ├── zero-shot/                 # Zero-shot baseline
        │   └── zero_shot_response.txt
        │
        └── K2P/                       # K2P Pipeline outputs
            ├── rulegen_response_fired.lp
            ├── atoms.txt
            ├── clingo_output.txt
            └── explanation.txt
```

#### Output File Descriptions

**D2K Pipeline Outputs (in `{cancer_type}/D2K/`):**
- `constant_response.txt`: Extracted domain constants
- `predicate_response.txt`: Identified predicates and relationships
- `rulegen_response.txt`: Generated ASP rules

**K2P Pipeline Outputs (in `{cancer_type}/K2P/`):**
- `rulegen_response_fired.lp`: ASP rules with fired/1 predicates added (non-ASP lines commented out)
- `atoms.txt`: Extracted facts from patient vignettes
- `clingo_output.txt`: Clingo solver output showing which rules fired
- `explanation.txt`: Human-readable explanations of fired rules

**Review Metrics (in `reviews/`):**
- `structural review D2K/{cancer_type}_graph_metrics.csv`: Graph-based similarity metrics comparing generated rules to ground truth
- `K2P review/{cancer_type}_K2P_review.csv`: Per-patient Precision, Recall, F1 scores for rule firing accuracy

## Project Structure

```
NICE2ASP2/
├── main.py                                # Main pipeline entry point
├── requirements.txt                       # Python dependencies
├── README.md                              # This file
├── README_REVIEWER.md                     # Guide for rule reviewers
├── notebooks/
│   └── rule_reviewer.ipynb                # Interactive review interface
├── src/
│   ├── configs/
│   │   ├── lung_cancer_config.yaml        # Lung cancer configuration
│   │   └── pancreatic_cancer_config.yaml  # Pancreatic cancer configuration
│   ├── input_files/
│   │   ├── input_guidelines/              # Clinical guideline texts
│   │   ├── ground_truths/                 # Human-authored ASP ground truth
│   │   │   ├── GT_LC.lp                   # Lung cancer ground truth
│   │   │   ├── GT_PC.lp                   # Pancreatic cancer ground truth
│   │   │   └── K2P_ground_truth.csv       # K2P evaluation ground truth
│   │   ├── prompt_files/                  # LLM prompts
│   │   └── K2P/                           # Patient vignettes
│   ├── output_files/                      # Generated results
│   │   ├── CLAUDE/
│   │   │   ├── reviews/                   # Evaluation metrics
│   │   │   ├── lung cancer/               # Lung cancer outputs
│   │   │   └── pancreatic cancer/         # Pancreatic cancer outputs
│   │   └── GPT/
│   ├── processing/                        # Core processing modules
│   │   ├── LLM_Inferencer.py              # LLM API wrapper
│   │   ├── FileManager.py                 # File I/O utilities
│   │   ├── RuleProcessor.py               # ASP rule processing
│   │   ├── ASPRuleParser.py               # ASP parsing utilities
│   │   ├── graph_analysis.py              # Graph similarity metrics
│   │   ├── graph_utils.py                 # Graph construction
│   │   ├── review_K2P.py                  # K2P evaluation metrics
│   │   └── pipeline_utils.py              # Pipeline configuration and setup utilities
│   ├── resources/
│   │   └── API_KEYS.py                    # API keys (DO NOT COMMIT!)
│   └── review/
│       └── review_data.py                 # Review dataset builder
└── venv/                                  # Virtual environment (not in repo)
```

## Experiments

### Running Different Experiment Variants

Edit your configuration file (e.g., `lung_cancer_config.yaml`) to change the experiment type:

```yaml
experiment:
  version: D2K-Pipeline  # Options: D2K-Pipeline, In-Context, No-Pipeline
```

**Available versions:**
- **D2K-Pipeline**: Full 3-stage pipeline (constants → predicates → rules)
- **In-Context**: Single-stage generation with examples
- **No-Pipeline**: Zero-shot generation

**Example:**
```bash
# After editing the config file
python main.py --config src/configs/lung_cancer_config.yaml
```

## Citation

If you use this work in your research, please cite:

```bibtex
@software{nice2asp2,
  title={NICE2ASP2: Translating Clinical Guidelines to Answer Set Programming},
  author={[Author names]},
  year={2026},
  url={https://github.com/Ashvin-Gupta/NICE2ASP2}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Data

This project uses clinical guidelines from the National Institute for Health and Care Excellence (NICE):
- NICE Pancreatic Cancer Guidelines
- NICE Lung Cancer Guidelines

Please refer to NICE's terms of use for the clinical guideline content: https://www.nice.org.uk/terms-and-conditions
