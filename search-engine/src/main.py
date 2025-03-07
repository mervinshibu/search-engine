import os
import argparse
import time
from preprocessor import Preprocessor
from indexer import Indexer
from search import SearchEngine
from parser import CranfieldParser
from trec_writer import TrecWriter

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Cranfield Search Engine')
    parser.add_argument('--documents', required=True, help='Path to the documents XML file')
    parser.add_argument('--queries', required=True, help='Path to the queries XML file')
    parser.add_argument('--output_dir', required=True, help='Directory to store the output files')
    parser.add_argument('--run_id', default='my_search_engine', help='Identifier for this run')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("Initializing search engine components...")
    
    # Initialize preprocessor, indexer, and search engine
    preprocessor = Preprocessor()
    indexer = Indexer(preprocessor)
    
    # Parse documents
    print(f"Parsing documents from {args.documents}...")
    start_time = time.time()
    documents = CranfieldParser.parse_documents(args.documents)
    print(f"Parsed {len(documents)} documents in {time.time() - start_time:.2f} seconds")
    
    # Index documents
    print("Indexing documents...")
    start_time = time.time()
    for doc in documents:
        indexer.add_document(doc.doc_id, doc.text)
    
    # Finalize index
    indexer.finalize_index()
    print(f"Indexed {indexer.doc_count} documents in {time.time() - start_time:.2f} seconds")
    print(f"Vocabulary size: {len(indexer.inverted_index)} terms")
    print(f"Average document length: {indexer.avg_doc_length:.2f} terms")
    
    # Create search engine
    search_engine = SearchEngine(indexer, preprocessor)
    
    # Parse queries
    print(f"Parsing queries from {args.queries}...")
    queries, id_mapping = CranfieldParser.parse_queries(args.queries)
    print(f"Parsed {len(queries)} queries")
    
    # Save ID mapping for reference (useful for debugging)
    mapping_file = os.path.join(args.output_dir, "query_id_mapping.txt")
    with open(mapping_file, 'w') as f:
        f.write("sequential_id,original_id\n")
        for seq_id, orig_id in id_mapping.items():
            f.write(f"{seq_id},{orig_id}\n")
    print(f"Query ID mapping saved to {mapping_file}")
    
    # Process queries with all three models
    models = [
        ('vsm', search_engine.search_vsm),
        ('bm25', search_engine.search_bm25),
        ('lm_dirichlet', search_engine.search_lm_dirichlet)
    ]
    
    for model_name, search_function in models:
        print(f"Processing queries with {model_name} model...")
        start_time = time.time()
        
        results = {}
        for query in queries:
            results[query.query_id] = search_function(query.text)
        
        # Write results to file
        output_file = os.path.join(args.output_dir, f"results_{model_name}.txt")
        run_id = f"{args.run_id}_{model_name}"
        TrecWriter.write_results(results, output_file, run_id)
        
        print(f"Completed {model_name} search in {time.time() - start_time:.2f} seconds")
        print(f"Results written to {output_file}")
    
    print("Search engine execution completed.")

if __name__ == "__main__":
    main() 