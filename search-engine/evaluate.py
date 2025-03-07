#!/usr/bin/env python3
import os
import argparse
import subprocess
import csv

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Evaluate Cranfield Search Engine results')
    parser.add_argument('--qrels', required=True, help='Path to the relevance judgments file')
    parser.add_argument('--results_dir', required=True, help='Directory with the search results files')
    parser.add_argument('--trec_eval_path', default='trec_eval', 
                        help='Path to the trec_eval executable (default: assumes it is in PATH)')
    args = parser.parse_args()
    
    # Check if the directories exist
    if not os.path.isfile(args.qrels):
        print(f"Error: Qrels file {args.qrels} not found")
        return
    
    if not os.path.isdir(args.results_dir):
        print(f"Error: Results directory {args.results_dir} not found")
        return
    
    # Get all result files
    result_files = [f for f in os.listdir(args.results_dir) if f.startswith('results_') and f.endswith('.txt')]
    
    if not result_files:
        print(f"Error: No result files found in {args.results_dir}")
        return
    
    # Look for id mapping file
    mapping_file = os.path.join(args.results_dir, "query_id_mapping.txt")
    if os.path.isfile(mapping_file):
        print(f"Found query ID mapping file: {mapping_file}")
        # No need to apply any transformation since our parser already normalizes IDs
        # The mapping file is just for reference/debugging
    else:
        print(f"Warning: Query ID mapping file not found. Assuming sequential IDs are used.")
    
    print(f"Found {len(result_files)} result files to evaluate")
    
    for result_file in result_files:
        model_name = result_file.replace('results_', '').replace('.txt', '')
        print(f"\n{'-'*80}")
        print(f"Evaluating {model_name} model")
        print(f"{'-'*80}")
        
        result_path = os.path.join(args.results_dir, result_file)
        
        try:
            # Run trec_eval
            cmd = [args.trec_eval_path, args.qrels, result_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Print the output
            print(result.stdout)
            
            if result.stderr:
                print(f"Warnings/Errors:\n{result.stderr}")
                
        except subprocess.CalledProcessError as e:
            print(f"Error running trec_eval: {e}")
        except FileNotFoundError:
            print(f"Error: trec_eval executable not found at {args.trec_eval_path}")
            print("Please install trec_eval or provide the correct path")
            return
    
    print("\nEvaluation complete!")

if __name__ == "__main__":
    main() 