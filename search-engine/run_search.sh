#!/bin/bash

# Path to the Cranfield dataset files
DOCUMENTS_PATH="../cranfield-trec-dataset-main/cran.all.1400.xml"
QUERIES_PATH="../cranfield-trec-dataset-main/cran.qry.xml"
QRELS_PATH="../cranfield-trec-dataset-main/cranqrel.trec.txt"

# Output directory
OUTPUT_DIR="./output"

# Run ID
RUN_ID="cranfield_search"

# Create output directory if it doesn't exist
mkdir -p ${OUTPUT_DIR}

# Run the search engine
echo "Running search engine..."
python3 src/main.py --documents ${DOCUMENTS_PATH} --queries ${QUERIES_PATH} --output_dir ${OUTPUT_DIR} --run_id ${RUN_ID}

# # Check if trec_eval is installed
# if command -v trec_eval &> /dev/null; then
#     echo "Running evaluation with trec_eval..."
#     python3 evaluate.py --qrels ${QRELS_PATH} --results_dir ${OUTPUT_DIR}
# else
#     echo "trec_eval not found. To evaluate the results, install trec_eval and run:"
#     echo "python3 evaluate.py --qrels ${QRELS_PATH} --results_dir ${OUTPUT_DIR}"
# fi

echo "Done!" 