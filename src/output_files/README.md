# output_files/ Directory

This directory contains all pipeline outputs, including generated ASP rules, evaluation metrics, and review data.

## Directory Structure

```
output_files/
└── {MODEL}/                          # e.g., CLAUDE, GPT
    ├── reviews/                      # EVALUATION METRICS (START HERE)
    │   ├── structural review D2K/
    │   │   └── {cancer_type}_graph_metrics.csv
    │   └── K2P review/
    │       └── {cancer_type}_K2P_review.csv
    │
    └── {cancer_type}/                # RAW PIPELINE OUTPUTS
        ├── config.yaml
        ├── D2K/
        ├── in-context/
        ├── zero-shot/
        └── K2P/
```

## Key Results Locations

### 📊 **Evaluation Metrics** (Primary Results)

**Human Review D2K**
- Location: `{MODEL}/reviews/human review D2K/`
- Files: Independent reviewers results
- Contains: Resulting program annotated with categorial score and comments from each reviewer for each guideline 

**Structural Similarity (D2K evaluation):**
- Location: `{MODEL}/reviews/structural review D2K/`
- Files: `{cancer_type}_graph_metrics.csv`
- Contains: Graph-based similarity metrics comparing generated ASP rules to ground truth

**K2P Performance (Patient-level evaluation):**
- Location: `{MODEL}/reviews/K2P review/`
- Files: `{cancer_type}_K2P_review.csv`
- Contains: Precision, Recall, F1 scores for each patient vignette

### 📝 **Generated ASP Rules**

**D2K Pipeline Output:**
- Location: `{MODEL}/{cancer_type}/D2K/rulegen_response.txt`
- This is the **final generated ASP program** from the D2K pipeline

**In-Context Output:**
- Location: `{MODEL}/{cancer_type}/in-context/in_context_response.txt`

**Zero-Shot Output:**
- Location: `{MODEL}/{cancer_type}/zero-shot/zero_shot_response.txt`

## Subdirectory Details

### `{MODEL}/reviews/`
**This is where reviewers should look first** - contains all evaluation metrics organized for easy access.

### `{MODEL}/{cancer_type}/`
Contains raw pipeline outputs for a specific cancer type.

#### `config.yaml`
Copy of the configuration used for this experiment run.

#### `D2K/` (D2K Pipeline Outputs)

**`constant_response.txt`**: Extracted constants
- **Expected output**: Medical domain constants organized by categories
- Categories include: Disease, Symptoms, Imaging, Procedures, Finding_of_{organ}, Genetic_disease, Management, Treatments, Anatomical_structures, Information_about_patient, General_findings
- Format: Each constant listed with its category (e.g., `Disease: "pancreatic cancer"`)

**`predicate_response.txt`**: Extracted predicates
- **Expected output**: Connecting terms/relationships with constants as arguments
- Format: Predicate definitions with typed arguments (e.g., `has_symptom(P, S)` where P is Patient, S is Symptom)
- Includes short descriptions of what each predicate represents

**`rulegen_response.txt`**: **Generated ASP rules** (main output)
- **Expected output**: Complete ASP program with rule numbers and rules
- Format: Rule number markers `[X.X.X]` followed by ASP rules
- Rules use predicates and constants from previous steps
- May include explanatory text (which will be commented out in processing)
- Example: `offer_imaging(X) :- patient(X), has_symptom(X, jaundice).`

#### `in-context/` (In-Context Baseline)
- `in_context_response.txt`: ASP rules generated using in-context learning

#### `zero-shot/` (Zero-Shot Baseline)
- `zero_shot_response.txt`: ASP rules generated using zero-shot prompting

#### `K2P/` (K2P Pipeline Outputs)

**`rulegen_response_fired.lp`**: ASP rules with fired/1 predicates (ready for Clingo)
- **Expected output**: Valid ASP program with tracking predicates
- Original ASP rules preserved
- Added `fired("X.X.X")` predicates to track which rules fire
- Non-ASP lines automatically commented out with `%`
- Includes `#show fired/1.` directive at the end
- Example: After rule `offer_imaging(X) :- ...`, adds `fired("1.1.4") :- ...`

**`atoms.txt`**: Facts extracted from patient vignettes
- **Expected output**: ASP facts for each patient case
- Organized by patient number (`=== Patient X ===`)
- Facts describe patient characteristics using extracted predicates
- Example: `patient(1). has_symptom(1, jaundice). age(1, 65).`

**`clingo_output.txt`**: Clingo solver output showing which rules fired
- **Expected output**: Solver results for each patient
- Shows which `fired("X.X.X")` atoms are true for each patient
- Format: Patient headers followed by list of fired rules
- Used to compare against ground truth

**`explanation.txt`**: Human-readable explanations of fired rules
- **Expected output**: Natural language explanations for each patient
- Organized by patient number
- For each fired rule, explains what the rule means and why it fired
- Provides clinical context for the recommendations

## Quick Access

**To review D2K results:**
1. Check graph metrics: `reviews/structural review D2K/{cancer_type}_graph_metrics.csv`
2. View generated rules: `{cancer_type}/D2K/rulegen_response.txt`

**To review K2P results:**
1. Check K2P metrics: `reviews/K2P review/{cancer_type}_K2P_review.csv`
2. View explanations: `{cancer_type}/K2P/explanation.txt`

## File Naming Convention

All review metric files follow this pattern:
- `{cancer_type}_graph_metrics.csv` (e.g., `lung cancer_graph_metrics.csv`)
- `{cancer_type}_K2P_review.csv` (e.g., `pancreatic cancer_K2P_review.csv`)

This makes it easy to compare results across different cancer types.

