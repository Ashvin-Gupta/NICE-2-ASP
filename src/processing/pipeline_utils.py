"""
Utility functions for the NICE 2 ASP pipeline.

This module contains helper functions for configuration loading,
directory setup, and pipeline orchestration.
"""

import yaml
from pathlib import Path


# Mapping of cancer types to organ names
ORGAN_MAPPING = {
    "lung cancer": "lung",
    "pancreatic cancer": "pancreas"
}


def load_config(config_path):
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration YAML file
        
    Returns:
        dict: Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def setup_experiment_dir(config, config_path):
    """
    Create experiment output directory structure.
    
    Creates the following directory structure:
    - Main cancer type directory
    - D2K subdirectory (for D2K pipeline outputs)
    - in-context subdirectory (for in-context baseline)
    - zero-shot subdirectory (for zero-shot baseline)
    - K2P subdirectory (for K2P pipeline outputs)
    
    Args:
        config: Configuration dictionary
        config_path: Path to the config file (for copying to output directory)
        
    Returns:
        tuple: (exp_dir, d2k_dir, in_context_dir, zero_shot_dir, k2p_dir)
    """
    # Create experiment output directory
    base_output_dir = Path(config['experiment']['output_dir'])
    cancer_type = config['experiment']['cancer_type']
    exp_dir = base_output_dir / cancer_type
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for organized outputs
    d2k_dir = exp_dir / 'D2K'
    in_context_dir = exp_dir / 'in-context'
    zero_shot_dir = exp_dir / 'zero-shot'
    k2p_dir = exp_dir / 'K2P'
    
    d2k_dir.mkdir(exist_ok=True)
    in_context_dir.mkdir(exist_ok=True)
    zero_shot_dir.mkdir(exist_ok=True)
    k2p_dir.mkdir(exist_ok=True)
    
    # Save config to the main cancer type directory
    config_copy_path = exp_dir / 'config.yaml'
    with open(config_path, 'r') as src, open(config_copy_path, 'w') as dst:
        lines = src.readlines()
        dst.writelines(lines)

    return exp_dir, d2k_dir, in_context_dir, zero_shot_dir, k2p_dir


def setup_output_files(exp_dir, d2k_dir, in_context_dir, zero_shot_dir, k2p_dir, config):
    """
    Setup output file paths for the pipeline.
    
    Args:
        exp_dir: Main experiment directory
        d2k_dir: D2K subdirectory
        in_context_dir: In-context subdirectory
        zero_shot_dir: Zero-shot subdirectory
        k2p_dir: K2P subdirectory
        config: Configuration dictionary
        
    Returns:
        dict: Dictionary mapping output file types to paths
    """
    cancer_type = config['experiment']['cancer_type']
    base_output_dir = Path(config['experiment']['output_dir'])
    
    # Create reviews directory structure for metrics
    k2p_review_dir = base_output_dir / 'reviews' / 'K2P review'
    k2p_review_dir.mkdir(parents=True, exist_ok=True)
    
    output_files = {
        # D2K-Pipeline outputs (in D2K subdirectory)
        'constant_response': d2k_dir / 'constant_response.txt',
        'predicate_response': d2k_dir / 'predicate_response.txt',
        'rulegen_response': d2k_dir / 'rulegen_response.txt',

        # K2P outputs (in K2P subdirectory)
        'rulegen_response_fired': k2p_dir / 'rulegen_response_fired.lp',
        'atoms': k2p_dir / 'atoms.txt',
        'clingo_output': k2p_dir / 'clingo_output.txt',
        'explanation': k2p_dir / 'explanation.txt',

        # Baseline responses (in their own subdirectories)
        'in_context_response': in_context_dir / 'in_context_response.txt',
        'zero_shot_response': zero_shot_dir / 'zero_shot_response.txt',

        # Review metrics (in reviews subdirectories)
        'k2p_metrics': k2p_review_dir / f'{cancer_type}_K2P_review.csv',
        
        # Input files
        'k2p_ground_truth': Path(config['input_files'].get('k2p_ground_truth', 
                                                            'src/input_files/ground_truths/K2P_ground_truth.csv')),
    }
    
    return output_files


def validate_pipeline_mode(pipeline_mode, cancer_type):
    """
    Validate that the pipeline mode is compatible with the cancer type.
    
    K2P modes (K2P-only and D2K+K2P) only work with pancreatic cancer
    as patient vignettes are only available for pancreatic cancer.
    
    Args:
        pipeline_mode: Pipeline mode (D2K-only, K2P-only, D2K+K2P)
        cancer_type: Cancer type (lung cancer, pancreatic cancer)
        
    Returns:
        bool: True if valid, False otherwise
    """
    if pipeline_mode in ['K2P-only', 'D2K+K2P']:
        if cancer_type != 'pancreatic cancer':
            print(f"ERROR: Pipeline mode '{pipeline_mode}' only works with pancreatic cancer guidelines.")
            print(f"Current cancer type: '{cancer_type}'")
            print("Please change cancer_type to 'pancreatic cancer' or use 'D2K-only' pipeline mode.")
            return False
    return True


def process_prompt_template(prompt_path, cancer_type):
    """
    Process a prompt template file by replacing {ORGAN} placeholder.
    
    Only replaces the category name "Finding_of_{ORGAN}" with the appropriate
    organ name (e.g., "Finding_of_lung" or "Finding_of_pancreas").
    Examples in the prompt remain unchanged.
    
    Args:
        prompt_path: Path to the prompt template file
        cancer_type: Cancer type (lung cancer, pancreatic cancer)
        
    Returns:
        str: Processed prompt content with {ORGAN} placeholder replaced
        
    Raises:
        ValueError: If cancer type is not recognized
    """
    if cancer_type not in ORGAN_MAPPING:
        raise ValueError(f"Unknown cancer type: {cancer_type}. Supported types: {list(ORGAN_MAPPING.keys())}")
    
    # Get organ name
    organ = ORGAN_MAPPING[cancer_type]
    
    # Read the prompt template
    with open(prompt_path, 'r') as f:
        prompt_content = f.read()
    
    # Replace only the {ORGAN} placeholder
    prompt_content = prompt_content.replace("{ORGAN}", organ)
    
    return prompt_content


def setup_processed_prompts(config, temp_dir):
    """
    Create processed versions of prompt templates with organ-specific terms.
    
    This function reads the prompt template files, replaces placeholders with
    cancer-type-specific terms, and saves them to temporary files.
    
    Args:
        config: Configuration dictionary
        temp_dir: Directory to store processed prompt files
        
    Returns:
        dict: Dictionary mapping prompt types to processed file paths
    """
    import tempfile
    cancer_type = config['experiment']['cancer_type']
    
    # Create temp directory for processed prompts
    temp_dir = Path(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    processed_prompts = {}
    
    # List of prompts that need processing
    prompt_keys = [
        'constant_prompt',
        'predicate_prompt',
        'rule_generation_prompt',
        'in_context_prompt',
        'zero_shot_prompt'
    ]
    
    for key in prompt_keys:
        if key in config['input_files']:
            original_path = config['input_files'][key]
            
            # Process the template
            processed_content = process_prompt_template(original_path, cancer_type)
            
            # Save to temporary file
            temp_path = temp_dir / Path(original_path).name
            with open(temp_path, 'w') as f:
                f.write(processed_content)
            
            processed_prompts[key] = str(temp_path)
    
    return processed_prompts

