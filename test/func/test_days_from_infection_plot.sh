test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

#run <test name> <program> <argument 1> <argument 2> <...>

run count_and_plot python ../../src/lkr/days_from_infection_plot.py --csv_file '../../test/data/input/Fake_HIV.csv' --column_number 0  --output_file '../../test/data/output/dfi_output.csv' --output_png '../../docs/lkr_dfi_histogram.png'
assert_exit_code 0

run file_DNE_count_and_plot python ../../src/lkr/days_from_infection_plot.py --csv_file '../../test/data/input/DNE.csv' --column_number 0  --output_file '../../test/data/output/DNE.csv' --output_png '../../docs/lkr_dfi_histogram.png'
assert_exit_code 1
