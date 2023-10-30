#!/bin/bash

set -e # stop on error
set -u # raise error if variable is unset
set -o pipefail # fail if any prior step failed

python3 src/gg/query_functions.py
python3 src/gg/make_query.py --filename -"src/gg/LANL_HIV1_2023_seq_metadata.csv" --query_column -"country" --query_comparison "equal to" --query_value -"Iran"
python3 src/gg/make_query.py --filename -"src/gg/LANL_HIV1_2023_seq_metadata.csv" --query_column -"sampling_year" --query_comparison "equal to" --query_value -"2023"
python3 src/gg/data_subsetting.py --filename -"src/gg/LANL_HIV1_2023_seq_metadata.csv"
Rscript src/gg/consort_plot.r
