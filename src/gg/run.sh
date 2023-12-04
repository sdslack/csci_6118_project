#!/bin/bash

set -e # stop on error
set -u # raise error if variable is unset
set -o pipefail # fail if any prior step failed

python3 src/gg/create_consort.py --consort_input_file_path "data/LANL_HIV1_2023_seq_metadata.csv" --filters "Sampling Year:=2023; Country:=IRAN, =SPAIN " --out_consort_png "data/Dec3_filters_Consort_Plot.png" --csv "data/Dec3_filtered_consort_input_df.png"

#python3 src/gg/prep_and_create_consort.py --consort_input_file "data/LANL_HIV1_2023_seq_metadata.csv" --query_summary_file "data/query_requests2.csv" --out_consort_png "data/Consort_Plot.png"
