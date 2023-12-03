#!/bin/bash


# Test query function with final options
# TODO: need to implement Google BigQuery

# Search 1:
    # risk factor = IV Drug User
    # days from infection = 0-90
    # global AND
# Search 2:
    # risk factor = Male sex with male | Sex worker | Sexual Transmission, unspecified | Heterosexual
    # days from infection = 0-90
    # global AND

# Start with Search 1 only
    # Risk Factor:=IV Drug User; 
python jb/get_queried_data.py \
    --file ../test/data/results_1_250000.csv \
    --filters "Days from Infection:0-90" \
    --query_output_file ../docs/filtered_seqlength.csv \
    --output_columns "SE id(SA), Days from Infection" \
    --query_request_file ../docs/query_request_summary.csv \
    --global_logical_operator "&&"
    
