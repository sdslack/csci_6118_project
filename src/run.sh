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
python3 jb/get_queried_data.py \
    --file ../test/data/results_1_250000.csv \
    --filters "Days from Infection:0-90" \
    --query_output_file ../docs/filtered_seqlength.csv \
    --output_columns "SE id(SA), Days from Infection" \
    --query_request_file ../docs/query_request_summary.csv \
    --global_logical_operator "&&"
    
# Visualize consort plot for first search
# Note: Can also add the query_request_summary instead of doing filters (documentation being updated)
python3 src/gg/create_consort.py --consort_input_file_path "data/LANL_HIV1_2023_seq_metadata.csv" --filters "Days from Infection:0-90; Risk Factor:=Male sex with male, =Sex Worker, =Sexual Transmission, unspecified, =Heterosexual" --out_consort_png "data/Dec3_filters_Consort_Plot.png" --csv "data/Dec3_filtered_consort_input_df.png"