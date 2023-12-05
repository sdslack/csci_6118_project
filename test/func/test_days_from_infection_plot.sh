test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

#run <test name> <program> <argument 1> <argument 2> <...>

#run count_and_plot python ../../src/lkr/days_from_infection_plot.py --csv_file '../../test/data/input/Fake_HIV.csv' ----column_name 'Days from Infection'  --output_file '../../test/data/output/real.csv'
#assert_exit_code 0

run test_int python ../../src/lkr/days_from_infection_plot.py --csv_file '../../test/data/input/Fake_HIV.csv' --column_name 'Days from Infection' --output_file '../../test/data/output/int_count_output.csv'
assert_exit_code 0

run test_string python ../../src/lkr/days_from_infection_plot.py --csv_file '../../test/data/input/Fake_HIV.csv' --column_name 'Sequence' --output_file '../../test/data/output/str_count_output.csv'
assert_exit_code 0

run test_float python ../../src/lkr/days_from_infection_plot.py --csv_file '../../test/data/input/Fake_HIV.csv' --column_name 'Float' --output_file '../../test/data/output/float_count_output.csv'
assert_exit_code 0

run file_DNE_count_and_plot python ../../src/lkr/days_from_infection_plot.py --csv_file '../../test/data/input/DNE.csv' --column_name 'Days from Infection'  --output_file '../../test/data/output/DNE.csv' 
assert_exit_code 1
