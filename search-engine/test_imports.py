#!/usr/bin/env python3
"""
Simple test script to verify that all imports work correctly.
"""

def test_imports():
    print("Testing imports...")
    
    try:
        # Test basic imports
        import os
        import sys
        import argparse
        import time
        print("✓ Basic imports")
        
        # Test NLTK
        import nltk
        print("✓ NLTK")
        
        # Try to find required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            print("✓ NLTK data")
        except LookupError:
            print("! NLTK data not found, downloading...")
            nltk.download('punkt')
            nltk.download('stopwords')
            print("✓ NLTK data downloaded")
        
        # Test project-specific imports
        from src.preprocessor import Preprocessor
        print("✓ Preprocessor")
        
        from src.indexer import Indexer
        print("✓ Indexer")
        
        from src.search import SearchEngine
        print("✓ SearchEngine")
        
        from src.parser import CranfieldParser
        print("✓ CranfieldParser")
        
        from src.trec_writer import TrecWriter
        print("✓ TrecWriter")
        
        print("\nAll imports successful!")
        return True
        
    except ImportError as e:
        print(f"\nImport error: {e}")
        print("\nPlease make sure you have installed all required packages:")
        print("pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    test_imports() 