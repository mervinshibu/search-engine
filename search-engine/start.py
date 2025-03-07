#!/usr/bin/env python3
"""
Startup script for the Cranfield Search Engine.
This script runs all checks and then starts the search engine.
"""

import os
import sys
import subprocess
from test_imports import test_imports
from check_dataset import check_dataset

def main():
    print("="*80)
    print(" Cranfield Search Engine - Startup")
    print("="*80)
    
    # Check imports
    print("\n[1/3] Checking imports...")
    if not test_imports():
        return 1
    
    # Check dataset
    print("\n[2/3] Checking dataset...")
    if not check_dataset():
        return 1
    
    # Run search engine
    print("\n[3/3] Starting search engine...")
    if os.path.exists("./run_search.sh"):
        # Use shell=False to ensure the script runs properly on all systems
        subprocess.run(["bash", "./run_search.sh"], shell=False)
    else:
        print("Error: run_search.sh not found.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 