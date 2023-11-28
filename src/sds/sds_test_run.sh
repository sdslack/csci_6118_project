#!/bin/bash

set -e  # stop on error
set -u  # raise error if variable is unset
set -o pipefail  # fail if any prior step failed


### Testing int counts
# Set parameters
file_name="../../test/data/output/int_count_output.csv"

# Run code
python plot_hist.py \
    --file-name "$file_name" --plot-path "../../docs"

### Testing float counts
# Set parameters
file_name="../../test/data/output/float_count_output.csv"

# Run code
python plot_hist.py \
    --file-name "$file_name" --plot-path "../../docs"

### Testing string counts
# Set parameters
file_name="../../test/data/output/str_count_output.csv"

# Run code
python plot_hist.py \
    --file-name "$file_name" --plot-path "../../docs"