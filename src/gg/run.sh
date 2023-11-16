#!/bin/bash

set -e # stop on error
set -u # raise error if variable is unset
set -o pipefail # fail if any prior step failed

# Clear queries
# python3 src/gg/make_query.py --file_name "data/LANL_HIV1_2023_seq_metadata.csv" --reset_query 'True' --query_summary_file "data/query_requests.csv"
# Actual Pipeline
python3 src/gg/make_query.py --file_name "data/LANL_HIV1_2023_seq_metadata.csv" --query_column "Country" --query_comparison "equal to" --query_value "IRAN" --query_summary_file "data/query_requests.csv"
python3 src/gg/data_subsetting.py --file_name "data/LANL_HIV1_2023_seq_metadata.csv" --query_summary_file "data/query_requests.csv" --consort_input_file "data/consort_input_df.csv"
Rscript src/gg/consort_plot.r
