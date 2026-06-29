# input_files/

All input data used by the pipeline. These files are loaded automatically based on the config — you don't need to edit them unless you are adding new guidelines or modifying prompts.

| Folder | Contents |
|---|---|
| `input_guidelines/` | NICE guideline text files (`lung_cancer_guidelines.txt`, `pancreatic_cancer_guidelines.txt`) |
| `ground_truths/` | Human-authored ground truth: `GT_LC.lp` and `GT_PC.lp` (D2K evaluation), `K2P_ground_truth.csv` (K2P evaluation) |
| `D2K/` | LLM prompt templates for constant extraction, predicate extraction, rule generation, in-context, and zero-shot modes. Prompts use `{ORGAN}` which is replaced at runtime with `lung` or `pancreas`. |
| `K2P/` | Patient vignette descriptions (`PC_descriptions.txt`) and the atom-extraction prompt (`setupProgram.txt`). K2P is only available for pancreatic cancer. |
