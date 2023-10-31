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
                        help='The name of column to search', required=True)
    parser.add_argument('--query_comparison',
                        help='The comparison to make',
                        required=True)
    parser.add_argument('--query_value',
                        help='Value to evaluate using the query_comparison',
                        required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    file_name = str(args.file_name)
    query_column = str(args.query_column)
    query_comparison = str(args.query_comparison)
    query_value = args.query_value
    # Create a table which tracks query requests
    try:
        # Read in Data
        lanl = pd.read_csv(file_name)
    except FileNotFoundError:
        print("Unable to find .csv file")
        sys.exit(1)
    try:
        query = pd.read_csv('data/query_requests.csv')
    except FileNotFoundError:
        query_pre = {
            'Search_Options': lanl.columns,
            'Search by this column?':
            ["No"] * len(lanl.columns),
            'How do you want to filter?': [None] * len(lanl.columns),
            'Filter Value': [None] * len(lanl.columns)}
        query = pd.DataFrame(query_pre)
        try:
            # Write .csv file tracking query_requests
            query.to_csv('data/query_requests.csv', sep=',', index='False')
        except Exception as e:
            print(f"Unable to write .csv file.")
            sys.exit(1)
    # Call user input function and resave as the query table
    query = qf.output_query_summary("query_column",
                                    "query_comparison", "query_value")
    try:
        # Write .csv file tracking query_requests
        query.to_csv('data/query_requests.csv', sep=',', index='False')
    except Exception as e:
        print(f"Unable to write .csv file.")
        sys.exit(1)


if __name__ == '__main__':
    main()
