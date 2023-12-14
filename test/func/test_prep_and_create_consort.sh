test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run functional_run_filters python3 src/gg/create_consort.py --consort_input_file_path "test/data/LANL_HIV1_2023_seq_metadata.csv" --filters "Sampling Year:=2023; Country:=IRAN, =SPAIN " --out_consort_png "test/data/Dec3_filters_Consort_Plot.png"
assert_equal $'test/data/Dec3_filters_Consort_Plot.png' $( ls $'test/data/Dec3_filters_Consort_Plot.png' )
assert_exit_code 0

run functional_run_files python3 src/gg/create_consort.py --consort_input_file_path "test/data/LANL_HIV1_2023_seq_metadata.csv" --query_summary_file "docs/query_request_summary.csv"  --out_consort_png "test/data/Dec3_files_Consort_Plot.png" --bool_out_csv "test/data/Dec3_filtered_consort_input_df.csv"
assert_equal $'test/data/Dec3_files_Consort_Plot.png' $( ls $'test/data/Dec3_files_Consort_Plot.png' )
assert_equal $'test/data/Dec3_filtered_consort_input_df.csv' $( ls $'test/data/Dec3_filtered_consort_input_df.csv' )
assert_exit_code 0

run no_filters python3 src/gg/create_consort.py --consort_input_file_path "test/data/LANL_HIV1_2023_seq_metadata.csv" --filters "" --out_consort_png "test/data/Dec3_filters_Consort_Plot.png"
assert_exit_code 1

run badly_formatted_filters python3 src/gg/create_consort.py --consort_input_file_path "test/data/LANL_HIV1_2023_seq_metadata.csv" --filters "Sampling Year:2023; Country:IRAN, SPAIN " --out_consort_png "test/data/Dec3_filters_Consort_Plot.png"
assert_exit_code 1

run filters_not_in_df python3 src/gg/create_consort.py --consort_input_file_path "test/data/LANL_HIV1_2023_seq_metadata.csv" --filters "Doesntexist:2023; Notcorrect:IRAN, SPAIN " --out_consort_png "test/data/Dec3_filters_Consort_Plot.png"
assert_exit_code 1

run wrong_out_consort_png python3 src/gg/create_consort.py --consort_input_file_path "test/data/LANL_HIV1_2023_seq_metadata.csv" --filters "Sampling Year:=2023; Country:=IRAN, =SPAIN " --out_consort_png "test/data/Dec3_filters_Consort_Plotwrong"
assert_exit_code 1

run wrong_consort_input_file_path python3 src/gg/create_consort.py --consort_input_file_path "test/data/LANL_HIV1_2023_seq_metadatanotexist.csv" --filters "Sampling Year:=2023; Country:=IRAN, =SPAIN " --out_consort_png "test/data/Dec3_filters_Consort_Plot.png"
assert_exit_code 1
