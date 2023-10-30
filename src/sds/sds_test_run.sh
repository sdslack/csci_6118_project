#!/bin/bash

set -e  # stop on error
set -u  # raise error if variable is unset
set -o pipefail  # fail if any prior step failed

# Script runs print_fires.py given file name, column to query
# (int), value to query, and optional result column (int).

# Set parameters
file_name="test/data/LANL_HIV1_2023_seq_metadata.csv"
categ_column=24  # subtype

# Run current code
python src/sds/query_categ_plot.py \
    --file-name "$file_name" --categ-column $categ_column \
    --plot-path "test/output" \