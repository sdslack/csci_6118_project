#!/bin/bash

set -e # stop on error
set -u # raise error if variable is unset
set -o pipefail # fail if any prior step failed

# Example 1 with consort diagram output and no .csv output
python3 src/gg/create_consort.py --consort_input_file_path "test/data/LANL_HIV1_2023_seq_metadata.csv" --filters "Sampling Year:=2023; Country:=IRAN, =SPAIN " --out_consort_png "docs/Run_example_filters_Consort_Plot.png"

# Example 2 with consort diagram and .csv output
python3 src/gg/create_consort.py --consort_input_file_path "test/data/LANL_HIV1_2023_seq_metadata.csv" --query_summary_file "docs/query_request_summary.csv"  --out_consort_png "docs/Run_example2_filters_Consort_Plot.png" --bool_out_csv "docs/Run_example2_filtered_consort_input_df.csv"
