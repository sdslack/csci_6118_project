import pandas as pd
import numpy as np
import query_functions as qf
import sys
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', type=str,
                        help='Name of the file', required=True)
    parser.add_argument('--query_column',
                        help='The name of column to search', required=False)
    parser.add_argument('--query_comparison',
                        help='The comparison to make',
                        required=False)
    parser.add_argument('--query_value',
                        help='Value to evaluate using the query_comparison',
                        required=False)
    parser.add_argument('--query_summary_file',
                        help='Name of file outputted with .csv extension',
                        required=True)
    parser.add_argument('--reset_query',
                        help='True if want to reset query',
                        required=False)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    file_name = str(args.file_name)
    query_column = str(args.query_column)
    query_comparison = str(args.query_comparison)
    query_summary_file = str(args.query_summary_file)
    reset_query = args.reset_query
    query_value = args.query_value
    # Read in lanl data as a pandas dataframe
    try:
        # Read in Data
        lanl = pd.read_csv(file_name)
    except FileNotFoundError:
        print("Unable to find .csv file")
        sys.exit(1)
    # Read in list of query requests for every column
    try:
        query = pd.read_csv(query_summary_file)
    # If can't find then make the query_requests file
    except FileNotFoundError:
        query = qf.reset_query(lanl)
    if reset_query == "True":
        query = qf.reset_query(lanl)
    # If no reset, call user input function
    elif reset_query != "True":
        query = qf.output_query_summary(query_column,
                                        query_comparison,
                                        query_value,
                                        query_summary_file)
    try:
        # Write .csv file tracking query_requests
        query.to_csv(query_summary_file, sep=',', index='False')
    except Exception as e:
        print(f"Unable to write .csv file.")
        sys.exit(1)


if __name__ == '__main__':
    main()
