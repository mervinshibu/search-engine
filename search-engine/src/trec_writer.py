class TrecWriter:
    """
    Utility for writing search results in TREC format.
    
    The TREC format is:
    query_id Q0 doc_id rank score run_id
    
    Where:
    - query_id: The ID of the query
    - Q0: A constant (historically for "Query 0")
    - doc_id: The ID of the document
    - rank: The rank of the document in the result set (starting from 1)
    - score: The score assigned to the document
    - run_id: An identifier for the run
    """
    
    @staticmethod
    def write_results(results, output_file, run_id):
        """
        Write search results to file in TREC format.
        
        Args:
            results (dict): Dictionary mapping query_id to list of (doc_id, score) tuples
            output_file (str): Path to the output file
            run_id (str): Identifier for this run
        """
        with open(output_file, 'w') as f:
            for query_id, doc_scores in results.items():
                # Sort by score, descending
                doc_scores = sorted(doc_scores, key=lambda x: x[1], reverse=True)
                
                # Write results
                for rank, (doc_id, score) in enumerate(doc_scores, start=1):
                    # Format: query_id Q0 doc_id rank score run_id
                    line = f"{query_id} Q0 {doc_id} {rank} {score:.6f} {run_id}\n"
                    f.write(line) 