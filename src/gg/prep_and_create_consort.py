import pandas as pd
import numpy as np
import rpy2.robjects as robjects
import os
import sys
import argparse
sys.path.append('src/gg')  # noqa
import consort_prep_functions as pf



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--query_summary_file',
                        help='Name of file outputted with .csv extension',
                        required=True)
    parser.add_argument('--consort_input_file',
                        help='Name of .csv file for consort_plot.r file',
                        required=True)
    parser.add_argument('--out_consort_png',
                        help='Path and name of .png file containing consort',
                        required=False)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    consort_input_file = str(args.consort_input_file)
    query_summary_file = str(args.query_summary_file)
    out_consort_png = str(args.out_consort_png)
    query_df_formatted = pf.reformat_query_summary(query_summary_file)
    consort_input_df = pf.format_consort_input_file(consort_input_file,
                                                    query_df_formatted)
    pf.run_consort_plot_rcode(consort_input_df, query_df_formatted,
                              out_consort_png)


if __name__ == '__main__':
    main()

