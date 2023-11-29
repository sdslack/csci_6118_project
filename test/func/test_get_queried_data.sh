test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run regular_query_data_test python ../../src/jb/get_queried_data.py --file ../data/LANL_HIV1_2023_seq_metadata.csv --filters "Subtype:=35_A1D && Sequence Length:=915" --query_output_file ../data/output/test_filtered_data.csv --output_columns "Sequence Length, Sequence, Name" --query_request_file ../data/output/test_query_summary.csv
assert_exit_code 0
assert_equal $'../data/output/test_filtered_data.csv' $( ls $'../data/output/test_filtered_data.csv')
assert_equal $'../data/output/test_query_summary.csv' $( ls $'../data/output/test_query_summary.csv')

# empty data frame
run empty_data_frame_test python ../../src/jb/get_queried_data.py --file ../data/input/empty.csv --filters "Subtype:=35_A1D && Sequence Length:=915" --query_output_file ../data/output/test_filtered_data.csv --output_columns "Sequence Length, Sequence, Name" --query_request_file ../data/output/test_query_summary.csv
assert_exit_code 1

# file not found
run file_not_found_test python ../../src/jb/get_queried_data.py --file ../data/LANL_HIV1_seq_metadata.csv --filters "Subtype:=35_A1D && Sequence Length:=915" --query_output_file ../data/output/test_filtered_data.csv --output_columns "Sequence Length, Sequence, Name" --query_request_file ../data/output/test_query_summary.csv
assert_exit_code 1

# nonexistent columns
run nonexistent_column_test python ../../src/jb/get_queried_data.py --file ../data/LANL_HIV1_2023_seq_metadata.csv --filters "Subtypes:=35_A1D && Sequence Lengths:=915" --query_output_file ../data/output/test_filtered_data.csv --output_columns "Sequence Length, Sequence, Name" --query_request_file ../data/output/test_query_summary.csv
assert_exit_code 1

run nonexistent_column_1_test python ../../src/jb/get_queried_data.py --file ../data/LANL_HIV1_2023_seq_metadata.csv --filters "Subtypes:=35_A1D && Sequence Lengths:=915" --query_output_file ../data/output/test_filtered_data.csv --output_columns "Sequence Length, Sequence, Names" --query_request_file ../data/output/test_query_summary.csv
assert_exit_code 1

