test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run python3 src/gg/prep_and_create_consort.py --consort_input_file "test/data/LANL_HIV1_2023_seq_metadata.csv" --query_summary_file "test/data/query_requests2.csv" --out_consort_png "test/data/Consort_Plot.png"
assert_exit_code 0
assert_equal $'test/data/Consort_Plot.png' $( ls $'test/data/Consort_Plot.png' )

run python3 src/gg/prep_and_create_consort.py --consort_input_file "test/data/empty_file.csv" --query_summary_file "test/data/query_requests2.csv" --out_consort_png "test/data/Consort_Plot.png"
assert_exit_code 1

run python3 src/gg/prep_and_create_consort.py --consort_input_file "test/data/nomatch_col_file.csv" --query_summary_file "test/data/query_requests2.csv" --out_consort_png "test/data/Consort_Plot.png"
assert_exit_code 1

run python3 src/gg/prep_and_create_consort.py --consort_input_file "test/data/LANL_HIV1_2023_seq_metadata.csv" --query_summary_file "test/data/nomatch_col_file.csv" --out_consort_png "test/data/Consort_Plot.png"
assert_exit_code 1

run python3 src/gg/prep_and_create_consort.py --consort_input_file "test/data/LANL_HIV1_2023_seq_metadata.csv" --query_summary_file "test/data/query_requests2.csv" --out_consort_png "test/data/Consort_Plot.no_ex"
assert_exit_code 1

run python3 src/gg/prep_and_create_consort.py --consort_input_file "test/data/LANL_HIV1_2023_seq_metadata.csv" --query_summary_file "test/data/query_requests_empty.csv" --out_consort_png "test/data/Consort_Plot_No_Requests.png"
assert_exit_code 0
assert_equal $'test/data/Consort_Plot_No_Requests.png' $( ls $'test/data/Consort_Plot_No_Requests.png' )