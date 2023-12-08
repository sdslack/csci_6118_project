test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run plot_hist_help python ../../src/sds/plot_hist.py -h
assert_exit_code 0
assert_in_stdout "usage: plot_hist"

run plot_hist_float python ../../src/sds/plot_hist.py \
    --file-name ../data/output/float_count_output.csv \
    --plot-output ../data/output/float_hist.png
assert_exit_code 0
assert_equal "../data/output/float_hist.png" $(ls "../data/output/float_hist.png")

run plot_hist_int python ../../src/sds/plot_hist.py \
    --file-name ../data/output/int_count_output.csv \
    --plot-output ../data/output/int_hist.png
assert_exit_code 0
assert_equal "../data/output/int_hist.png" $(ls "../data/output/int_hist.png")

run plot_hist_str python ../../src/sds/plot_hist.py \
    --file-name ../data/output/str_count_output.csv \
    --plot-output ../data/output/str_hist.png
assert_exit_code 0
assert_equal "../data/output/str_hist.png" $(ls "../data/output/str_hist.png")

run plot_hist_dne python ../../src/sds/plot_hist.py \
    --file-name ../data/output/no_file.csv \
    --plot-output ../data/output/no_file_hist.png
assert_exit_code 1
assert_in_stdout "File not found:"
