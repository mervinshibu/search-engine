#!/usr/bin/env python3
"""
Check if the Cranfield dataset files exist in the expected locations.
"""

import os
import sys

def check_dataset():
    print("Checking Cranfield dataset files...")
    
    # Expected file paths
    documents_path = "../cranfield-trec-dataset-main/cran.all.1400.xml"
    queries_path = "../cranfield-trec-dataset-main/cran.qry.xml"
    qrels_path = "../cranfield-trec-dataset-main/cranqrel.trec.txt"
    
    # Check if files exist
    files_exist = True
    
    if not os.path.isfile(documents_path):
        print(f"✗ Documents file not found: {documents_path}")
        files_exist = False
    else:
        print(f"✓ Documents file found: {documents_path}")
    
    if not os.path.isfile(queries_path):
        print(f"✗ Queries file not found: {queries_path}")
        files_exist = False
    else:
        print(f"✓ Queries file found: {queries_path}")
    
    if not os.path.isfile(qrels_path):
        print(f"✗ Relevance judgments file not found: {qrels_path}")
        files_exist = False
    else:
        print(f"✓ Relevance judgments file found: {qrels_path}")
    
    if files_exist:
        print("\nAll Cranfield dataset files found!")
    else:
        print("\nSome Cranfield dataset files are missing.")
        print("Please make sure the files are in the correct locations.")
        print("You can modify the paths in run_search.sh if needed.")
    
    return files_exist

if __name__ == "__main__":
    check_dataset() 