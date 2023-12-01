#!/bin/bash

set -e  # stop on error
set -u  # raise error if variable is unset
set -o pipefail  # fail if any prior step failed

python get_queried_data.py \
    --file ../../test/data/LANL_HIV1_2023_seq_metadata.csv \
    --filters "Subtype:=35_A1D; Sequence Length:=915" \
    --query_output_file ../../docs/filtered_seqlength.csv \
    --output_columns "Sequence Length, Sequence, Name" \
    --query_request_file ../../docs/query_request_summary.csv \
    --global_logical_operator "||"
    
    