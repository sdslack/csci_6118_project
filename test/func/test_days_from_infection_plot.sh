test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

#run <test name> <program> <argument 1> <argument 2> <...>

run count_sequences python ../../src/lkr/days_from_infection_plot.py --operation count --csv_file '../test/data/input/Fake_HIV.csv' --column_number 0 --output_file '../test/data/output/dfi_output.csv'
assert_exit_code 0





