# processing/

Core Python modules for the NICE2ASP pipeline.

| Module | Purpose |
|---|---|
| `LLM_Inferencer.py` | Calls the Claude API for constant extraction, predicate extraction, rule generation, and atom extraction |
| `RuleProcessor.py` | Adds `fired/1` tracking predicates to ASP rules, runs Clingo for each patient, and generates natural-language explanations |
| `ASPRuleParser.py` | Parses ASP rule syntax into head/body components for explanation generation |
| `FileManager.py` | Simple file read/write helpers |
| `pipeline_utils.py` | Loads config YAMLs, creates output directories, and substitutes `{ORGAN}` placeholders in prompts |
| `review_K2P.py` | Compares Clingo output against the ground-truth CSV and reports precision, recall, and F1 per patient |
