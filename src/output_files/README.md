# output_files/

Pipeline outputs are organised by the `output_dir` value set in the config file (e.g. `src/output_files/CLAUDE_TEST/`).

## Directory structure

```
output_files/
└── {output_dir}/
    ├── reviews/
    │   └── K2P review/
    │       └── {cancer_type}_K2P_review.csv
    └── {cancer_type}/
        ├── config.yaml          # copy of the config used for this run
        ├── D2K/
        │   ├── constant_response.txt
        │   ├── predicate_response.txt
        │   └── rulegen_response.txt
        ├── in-context/
        │   └── in_context_response.txt
        ├── zero-shot/
        │   └── zero_shot_response.txt
        └── K2P/
            ├── rulegen_response_fired.lp
            ├── atoms.txt
            ├── clingo_output.txt
            └── explanation.txt
```

## File descriptions

### D2K outputs (`D2K/`)

| File | Contents |
|---|---|
| `constant_response.txt` | Medical domain constants extracted from the guidelines |
| `predicate_response.txt` | Predicates and relationships extracted from the guidelines |
| `rulegen_response.txt` | Generated ASP rules (the main D2K output) |

### K2P outputs (`K2P/`)

| File | Contents |
|---|---|
| `rulegen_response_fired.lp` | ASP rules with `fired/1` tracking predicates added, ready for Clingo |
| `atoms.txt` | ASP facts extracted from each patient vignette |
| `clingo_output.txt` | Clingo solver output showing which rules fired per patient |
| `explanation.txt` | Natural-language explanation of the fired rules per patient |

### Evaluation metrics (`reviews/`)

| File | Contents |
|---|---|
| `K2P review/{cancer_type}_K2P_review.csv` | Per-patient precision, recall, and F1 for rule-firing accuracy |
