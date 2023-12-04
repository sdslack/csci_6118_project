#!/bin/bash

# 1. Get data from BigQuery and filter

# Search 1:
    # risk factor = IV Drug User
    # days from infection = 0-90
    # global AND

# Set up days from infection filter
# days_from_inf_filter="Days from Infection:="
num_list="=0"
for ((i=1; i<=90; i++))
do
    num_list+=", =$i"
done

# python jb/get_queried_data.py \
    # --filters "Days from Infection:${num_list}; Risk Factor:=IV Drug User" \
    # --query_output_file ../docs/query_1_filtered_data.csv \
    # --output_columns "SE id(SA), Days from Infection, Risk Factor" \
    # --query_request_file ../docs/query_1_request_summary.csv \
    # --global_logical_operator "&&"

# Search 2:
    # risk factor = Male sex with male | Sex worker | Sexual Transmission, unspecified | Heterosexual
    # days from infection = 0-90
    # global AND
    # TODO: for now, leaving out: =Sexual transmission,<br> unspecified type
python jb/get_queried_data.py \
    --filters "Days from Infection:${num_list}; Risk Factor:=Male Sex with Male, =Sex worker, =Heterosexual" \
    --query_output_file ../docs/query_2_filtered_data.csv \
    --output_columns "SE id(SA), Days from Infection, Risk Factor" \
    --query_request_file ../docs/query_2_request_summary.csv \
    --global_logical_operator "&&"

# 2. Visualize consort plot
# Visualize consort plot for first search
# Note: Can also add the query_request_summary instead of doing filters (documentation being updated)
python3 gg/create_consort.py --consort_input_file_path "data/LANL_HIV1_2023_seq_metadata.csv" --filters "Days from Infection:0-90; Risk Factor:=Male sex with male, =Sex Worker, =Sexual Transmission, unspecified, =Heterosexual" --out_consort_png "data/Dec3_filters_Consort_Plot.png" --csv "data/Dec3_filtered_consort_input_df.png"

# 3. Make CSVs with counts of results

# 4. Make plots summarizing counts of results