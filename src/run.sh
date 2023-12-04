#!/bin/bash

# 1. Get data from BigQuery and filter

# Search 1:
    # risk factor = IV Drug User
    # days from infection = 0-90
    # global AND

# Set up days from infection filter
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
# python jb/get_queried_data.py \
    # --filters "Days from Infection:${num_list}; Risk Factor:=Male Sex with Male, =Sex worker, =Heterosexual" \
    # --query_output_file ../docs/query_2_filtered_data.csv \
    # --output_columns "SE id(SA), Days from Infection, Risk Factor" \
    # --query_request_file ../docs/query_2_request_summary.csv \
    # --global_logical_operator "&&"

# 2. Visualize consort plot

# Search 1
# Note: Can also add the query_request_summary instead of doing filters (documentation being updated)
# python3 gg/create_consort.py \
    # --consort_input_file_path "data/LANL_HIV1_2023_seq_metadata.csv" \
    # --filters "Days from Infection:0-90; Risk Factor:=Male sex with male, =Sex Worker, =Sexual Transmission, unspecified, =Heterosexual" \
    # --out_consort_png "data/Dec3_filters_Consort_Plot.png" \
    # --csv "data/Dec3_filtered_consort_input_df.png"

# SDS attempt to use outputs from Step 1 above - error with 'Filter Value'
# TODO: revisit this!
# python3 gg/prep_and_create_consort.py \
    # --consort_input_file "../docs/query_1_filtered_data.csv" \
    # --query_summary_file "../docs/query_1_request_summary.csv" \
    # --out_consort_png "../docs/query_1_consort_plot.png"

python3 gg/create_consort.py \
    --consort_input_file_path "../docs/query_1_filtered_data.csv" \
    --query_summary_file "../docs/query_1_request_summary.csv" \
    --out_consort_png "../docs/query_1_consort_plot.png" \
    --bool_out_csv "../docs/query_1_filtered_consort_input.csv"

# 3. Make CSVs with counts of results

# Search 1 - Days from Infection, Risk Factor
# python lkr/days_from_infection_plot.py \
#     --csv_file '../docs/query_1_filtered_data.csv' \
#     --column_name 'Days from Infection' \
#     --output_file '../docs/query_1_days_from_inf_counts.csv'

# python lkr/days_from_infection_plot.py \
#     --csv_file '../docs/query_1_filtered_data.csv' \
#     --column_name 'Risk Factor' \
#     --output_file '../docs/query_1_risk_factor_counts.csv'

# Search 2 - Days from Infection, Risk Factor
# python lkr/days_from_infection_plot.py \
#     --csv_file '../docs/query_2_filtered_data.csv' \
#     --column_name 'Days from Infection' \
#     --output_file '../docs/query_2_days_from_inf_counts.csv'

# python lkr/days_from_infection_plot.py \
#     --csv_file '../docs/query_2_filtered_data.csv' \
#     --column_name 'Risk Factor' \
#     --output_file '../docs/query_2_risk_factor_counts.csv'

# 4. Make plots summarizing counts of results

# Search 1 - Days from Infection, Risk Factor
# python sds/plot_hist.py \
#     --file-name '../docs/query_1_days_from_inf_counts.csv' \
#     --plot-prefix "../docs/query_1"

# python sds/plot_hist.py \
#     --file-name '../docs/query_1_risk_factor_counts.csv' \
#     --plot-prefix "../docs/query_1"

# Search 2 - Days from Infection, Risk Factor
# python sds/plot_hist.py \
#     --file-name '../docs/query_2_days_from_inf_counts.csv' \
#     --plot-prefix "../docs/query_2"

# python sds/plot_hist.py \
#     --file-name '../docs/query_2_risk_factor_counts.csv' \
#     --plot-prefix "../docs/query_2"
