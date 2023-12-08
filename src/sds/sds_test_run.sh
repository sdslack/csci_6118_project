#!/bin/bash

set -e  # stop on error
set -u  # raise error if variable is unset
set -o pipefail  # fail if any prior step failed


# Testing int counts output by LKR
python plot_hist.py \
    --file-name "../../test/data/output/int_count_output.csv" \
    --plot-output "../../test/data/output/int_hist.png"

# Testing float counts output by LKR
python plot_hist.py \
    --file-name "../../test/data/output/float_count_output.csv" \
    --plot-output "../../test/data/output/float_hist.png"

# Testing string counts output by LKR
python plot_hist.py \
    --file-name "../../test/data/output/str_count_output.csv" \
    --plot-output "../../test/data/output/str_hist.png"
