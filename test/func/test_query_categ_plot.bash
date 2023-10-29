test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run query_categ_plot_help python ../../src/sds/query_categ_plot.py -h
assert_exit_code 0
assert_in_stdout "usage: query_categ_plot"

run query_categ_plot python ../../src/sds/query_categ_plot.py \
    --file-name ../data/LANL_HIV1_2023_seq_metadata.csv \
    --categ-column 2 \
    --plot-path ../output
assert_exit_code 0
# TODO: add check for file existence

run query_categ_plot_no_file python ../../src/sds/query_categ_plot.py \
    --file-name ../data/no_file.csv \
    --categ-column 2 \
    --plot-path ../output
assert_exit_code 1
assert_in_stdout "File not found:"