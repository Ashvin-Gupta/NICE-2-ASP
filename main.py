import argparse
import tempfile
import shutil
from pathlib import Path
from src.processing.LLM_Inferencer import LLMInferencer
from src.processing.FileManager import FileManager
from src.processing.RuleProcessor import RuleProcessor
from src.processing.review_K2P import K2PReviewer
from src.processing.pipeline_utils import (
    load_config, 
    setup_experiment_dir, 
    setup_output_files, 
    validate_pipeline_mode,
    setup_processed_prompts
)

def main(config_path):
    """
    Main pipeline execution function.
    
    Args:
        config_path: Path to the configuration YAML file
    """
    # Load configuration
    print(f"Loading configuration from: {config_path}")
    config = load_config(config_path)
    
    # Validate pipeline mode
    pipeline_mode = config['experiment'].get('pipeline_mode', 'D2K-only')
    cancer_type = config['experiment']['cancer_type']
    
    # Validate K2P requirements
    if not validate_pipeline_mode(pipeline_mode, cancer_type):
        return
    
    print(f'Running Pipeline in {pipeline_mode} mode for {cancer_type}!')
    
    # Setup directories
    exp_dir, d2k_dir, in_context_dir, zero_shot_dir, k2p_dir = setup_experiment_dir(config, config_path)
    
    # Setup output file paths
    output_files = setup_output_files(exp_dir, d2k_dir, in_context_dir, zero_shot_dir, k2p_dir, config)

    # Process prompt templates with cancer-type-specific organ terms
    temp_dir = tempfile.mkdtemp(prefix='nice2asp_prompts_')
    processed_prompts = setup_processed_prompts(config, temp_dir)
    print(f"Processed prompts created in: {temp_dir}\n")

    llmExtractor = LLMInferencer(config['experiment']['model'], config['experiment']['temperature'], config['experiment']['family'])
    fileManager = FileManager()

    # Get pipeline mode
    pipeline_mode = config['experiment'].get('pipeline_mode', 'D2K-only')
    
    # ------------------------------------------------------------
    # D2K-Pipeline (Data to Knowledge)
    # ------------------------------------------------------------
    
    # Run D2K if mode is D2K-only or D2K+K2P
    if pipeline_mode in ['D2K-only', 'D2K+K2P']:
        if config['experiment']['version'] == 'D2K-Pipeline':
            # Constant extraction (using processed prompt)
            llmExtractor.run_constant_inference(
                processed_prompts['constant_prompt'],
                config['input_files']['problem_text'],
                str(output_files['constant_response']),
            )
            print(f"Constants extracted and saved to: {output_files['constant_response']}\n")

            # Extracting the predicates (using processed prompt)
            llmExtractor.run_predicate_inference(
                processed_prompts['predicate_prompt'],
                config['input_files']['problem_text'],
                str(output_files['constant_response']),
                str(output_files['predicate_response']),
            )
            print(f"Predicates extracted and saved to: {output_files['predicate_response']}\n")
            # Rule generation (using processed prompt)
            llmExtractor.run_rulegen_inference(
                processed_prompts['rule_generation_prompt'],
                config['input_files']['problem_text'],
                str(output_files['constant_response']),
                str(output_files['predicate_response']),
                str(output_files['rulegen_response']),
            )
            print(f"Rules extracted and saved to: {output_files['rulegen_response']}\n")
        elif config['experiment']['version'] == 'In-Context':
            print("Running in context inference")
            llmExtractor.run_constant_inference(
                processed_prompts['in_context_prompt'],
                config['input_files']['problem_text'],
                str(output_files['in_context_response'])
            )
            print(f"In-context rules extracted and saved to: {output_files['in_context_response']}\n")
        elif config['experiment']['version'] == 'No-Pipeline':
            print("Running zero shot inference")
            llmExtractor.run_constant_inference(
                processed_prompts['zero_shot_prompt'],
                config['input_files']['problem_text'],
                str(output_files['zero_shot_response'])
            )
            print(f"Zero shot rules extracted and saved to: {output_files['zero_shot_response']}\n")
        else:
            print("Invalid experiment version")
            return

    # ------------------------------------------------------------
    # K2P Analysis (Knowledge to Prediction)
    # Only runs for K2P-only or D2K+K2P modes (pancreatic cancer only)
    # ------------------------------------------------------------
    
    if pipeline_mode in ['K2P-only', 'D2K+K2P']:
        print("\n\nStarting K2P Analysis")
        
        # For K2P-only mode, we need to use a pre-existing rulegen_response file
        if pipeline_mode == 'K2P-only':
            # Check if rulegen_response file exists
            if not output_files['rulegen_response'].exists():
                print(f"ERROR: K2P-only mode requires a pre-existing rule generation file.")
                print(f"Expected file: {output_files['rulegen_response']}")
                print("Please run D2K-only mode first or use D2K+K2P mode.")
                return
            print(f"Using existing rules from: {output_files['rulegen_response']}")
        
        ruleProcessor = RuleProcessor(config['input_files']['problem_text'])

        # Add fired({rule number}) to the rules
        ruleProcessor.append_fired_rules(str(output_files['rulegen_response']), str(output_files['rulegen_response_fired']))

        # Extract the atoms in patient vignettes from the rules generated by the program
        llmExtractor.extract_atoms(
            prompt_template=config['input_files']['extract_atoms'], 
            rules=str(output_files['rulegen_response']), 
            descriptions=config['input_files']['patient_vignettes'], 
            output_file=str(output_files['atoms'])
            )

        # Run clingo for each patient vignette
        ruleProcessor.run_clingo_for_patients(str(output_files['rulegen_response_fired']), str(output_files['atoms']), str(output_files['clingo_output']))

        # Explain the clingo output
        ruleProcessor.explain_fired_rules(str(output_files['rulegen_response_fired']), str(output_files['clingo_output']), str(output_files['explanation']))
        
        # Evaluate K2P performance against ground truth
        print("\nEvaluating K2P performance...")
        k2p_reviewer = K2PReviewer(
            ground_truth_path=str(output_files['k2p_ground_truth']),
            clingo_output_path=str(output_files['clingo_output'])
        )
        per_patient_df, global_metrics = k2p_reviewer.evaluate_and_save(
            output_csv_path=str(output_files['k2p_metrics'])
        )
    
    # Cleanup temporary prompt files
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"Cleaned up temporary files from: {temp_dir}")
    
    print(f"\nPipeline completed successfully in {pipeline_mode} mode!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run NICE 2 ASP Pipeline for lung or pancreatic cancer guidelines',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run lung cancer pipeline with D2K-only mode
  python main.py --config src/configs/lung_cancer_config.yaml
  
  # Run pancreatic cancer pipeline with D2K+K2P mode
  python main.py --config src/configs/pancreatic_cancer_config.yaml
  
  # Using short form
  python main.py -c src/configs/lung_cancer_config.yaml
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        required=True,
        help='Path to configuration YAML file (e.g., src/configs/lung_cancer_config.yaml)'
    )
    
    args = parser.parse_args()
    
    try:
        main(args.config)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nAvailable config files:")
        print("  - src/configs/lung_cancer_config.yaml")
        print("  - src/configs/pancreatic_cancer_config.yaml")
        exit(1)
    except Exception as e:
        print(f"Error running pipeline: {e}")
        import traceback
        traceback.print_exc()
        exit(1)