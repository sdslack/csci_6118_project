#!/bin/bash

set -e  # stop on error
set -u  # raise error if variable is unset
set -o pipefail  # fail if any prior step failed

python query_data.py \
    --file ../../test/data/LANL_HIV1_2023_seq_metadata.csv \
    --categorical_filters "Subtype:35_A1D" \
    --numerical_filters "Sequence Length:=915" \
    --output_file ../../docs/filtered_seqlength.csv
    --output_columns "Sequence Length, Sequence, Name"
    