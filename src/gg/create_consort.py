import pandas as pd
import numpy as np
import rpy2.robjects as robjects
import os
import sys
import argparse
sys.path.append('src/gg')  # noqa
import consort_prep_functions as pf
sys.path.append('../jb')  # noqa
import query_utils as query


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--consort_input_file_path',
                        help='Name of .csv file containing data',
                        required=True)
    parser.add_argument('--query_summary_file',
                        help='Name of file outputted with .csv extension',
                        required=False, default=None)
    parser.add_argument('--filters',
                        help='How to filter the data',
                        required=False, default=None)
    parser.add_argument('--global_logical_operator',
                        help='Combine column filters with logical && or ||',
                        required=False, default='&&')
    parser.add_argument('--bool_out_csv',
                        help='The file path if want to save consort_input_df',
                        required=False, default=None)
    parser.add_argument('--out_consort_png',
                        help='Path and name of .png file containing consort',
                        required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    consort_input_file_path = str(args.consort_input_file_path)
    consort_input_data = query.load_data(consort_input_file_path)
    filters = args.filters
    query_summary_file = args.query_summary_file
    query_df_formatted, filters_provided = pf.make_query_df_formatted(
        filters, query_summary_file, consort_input_data)
    logical_operator = str(args.global_logical_operator)
    bool_out_csv = args.bool_out_csv
    out_consort_png = str(args.out_consort_png)
    consort_input_df = pf.consort_filter_data(consort_input_data,
                                              filters_provided,
                                              bool_out_csv)
    pf.run_consort_plot_rcode(consort_input_df, query_df_formatted,
                              out_consort_png, logical_operator)


if __name__ == '__main__':
    main()
