import pandas as pd
import numpy as np
import sys
import argparse
sys.path.append('src/gg')  # noqa
import query_functions as qf


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', type=str,
                        help='Name of the file', required=True)
    parser.add_argument('--query_summary_file',
                        help='Name of file outputted with .csv extension',
                        required=False)
    parser.add_argument('--consort_input_file',
                        help='Name of .csv file for consort_plot.r file',
                        required=False)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    file_name = str(args.file_name)
    query_summary_file = str(args.query_summary_file)
    consort_input_file = str(args.consort_input_file)

    try:
        query = pd.read_csv(query_summary_file)
    except FileNotFoundError:
        print("No query file found. Run query_parameters.py if haven't")
        sys.exit(1)
    try:
        # Read in Data
        lanl = pd.read_csv(file_name)
    except FileNotFoundError:
        print("Unable to find lanl .csv file")
        sys.exit(1)
    # Subset the query dataset to only the important columns
    query_requests = query[
        query['Do you plan to search by this column?'] == "Yes"]
    # Create subset of query dataset based on search options
    request_query_col = query_requests['Search_Options'].tolist()
    # Create subset of lanl dataset based on search options
    consort_input_df_pre = qf.subset_dataframe_by_names(lanl,
                                                        request_query_col)
    # We will write a loop to make the appropriate changes to our dataframe
    consort_input_df = consort_input_df_pre
    query_requests.reset_index(drop=True, inplace=True)
    consort_input_df.reset_index(drop=True, inplace=True)
    for i in range(len(query_requests)):
        filtered_column = query_requests['Search_Options'][i]
        filter_value = query_requests['Filter Value'][i]
        inclusion_info_name = "Include_Column" + str(i)
        consort_input_df[inclusion_info_name] = "Unknown"
        for q in range(len(consort_input_df)):
            if query_requests.loc[i,
                                  'How do you want to filter?'
                                  ] == "equal to":
                if consort_input_df.loc[q, filtered_column] == filter_value:
                    consort_input_df.loc[q, inclusion_info_name] = "Included"
                else:
                    consort_input_df.loc[q, inclusion_info_name] = "Excluded"
            elif query_requests.loc[i,
                                    'How do you want to filter?'
                                    ] == "not equal to":
                if consort_input_df.loc[q, filtered_column] != filter_value:
                    consort_input_df.loc[q, inclusion_info_name] = "Included"
                else:
                    consort_input_df.loc[q, inclusion_info_name] = "Excluded"
            elif query_requests.loc[i,
                                    'How do you want to filter?'
                                    ] == "greater than":
                if consort_input_df.loc[q, filtered_column] > filter_value:
                    consort_input_df.loc[q, inclusion_info_name] = "Included"
                else:
                    consort_input_df.loc[q, inclusion_info_name] = "Excluded"
            elif query_requests.loc[i,
                                    'How do you want to filter?'
                                    ] == "less than":
                if consort_input_df.loc[q, filtered_column] < filter_value:
                    consort_input_df.loc[q, inclusion_info_name] = "Included"
                else:
                    consort_input_df.loc[q, inclusion_info_name] = "Excluded"
    try:
        # Write .csv file for data
        consort_input_df.to_csv(consort_input_file, index=False)
    except Exception as e:
        print(f"Unable to write .csv files.")
        sys.exit(1)


if __name__ == '__main__':
    main()
