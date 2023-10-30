import pandas as pd
import numpy as np
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
    except FileNotFound:
        print("Unable to find .csv file")
        sys.exit(1)
    try:
        if isinstance(query, pd.DataFrame):
            return query
    except (NameError, AttributeError):
        query = {
            'Search_Options': lanl.columns,
            'Search by this column?':
            ["No"] * len(lanl.columns),
            'How do you want to filter?': [None] * len(lanl.columns),
            'Filter Value': [None] * len(lanl.columns)}
        query_pd = pd.DataFrame(query)
    # Call user input function and resave as the query table
    query = cwf.output_query_summary("query_column",
                                     "query_comparison", "query_value")
    try:
        # Write .csv file tracking query_requests
        query_requests = 'src/gg/query_requests.csv'
        df.to_csv(query_requests, index=False)
    except Exception as e:
        print(f"Unable to write .csv file.")
        sys.exit(1)


if __name__ == '__main__':
    main()
