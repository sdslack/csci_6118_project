import pandas as pd
import numpy as np
import sys
import argparse
import src/gg/query_functions as qf


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', type=str,
                        help='Name of the file', required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    file_name = str(args.file_name)
    try:
        query = pd.read_csv("src/gg/query_requests.csv")
    except FileNotFound:
        print("No queries made. Please run query_parameters.py")
        sys.exit(1)
    try:
        # Read in Data
        lanl = pd.read_csv(file_name)
    except FileNotFound:
        print("Unable to find .csv file")
        sys.exit(1)
    # Create subset of dataset based on search options
    lanl_query_col = query.loc[
        query['Search by this column?'] == "Yes",
        'Search_Options'].tolist()
    consort_input_df_pre = qf.subset_dataframe_by_names(lanl, lanl_query_col)
    # Subset the query dataset to only the important columns
    query_requests = query[query['Search by this column?'] == "Yes"]
    # We will write a loop to make the appropriate changes to our dataframe
    consort_input_df = consort_input_df_pre
    consort_input_df['All'] = 1
    for i in range(len(query_requests)):
        filtered_column = query_requests.at[i, 'Search_Options']
        filter_value = query_requests.at[i, 'Filter Value']
        exclude_col_name = "Exclude_Column" + str(i)
        include_col_name = "Include_Column" + str(i)
        consort_input_df[include_col_name] = "Unknown"
        consort_input_df[exclude_col_name] = "Unknown"
        for q in range(len(consort_input_df)):
            if query['How do you want to filter?'] == "equal to":
                if consort_input_df.at[q, filtered_column] == filter_value:
                    consort_input_df.at[q, exclude_col_name] = "Included"
                    consort_input_df.at[q, include_col_name] =
                    consort_input_df.at[q, filtered_column]
                else:
                    consort_input_df.at[q, exclude_col_name] =
                    consort_input_df.at[q, filtered_column]
                    consort_input_df.at[q, include_col_name] = "Excluded"
            elif query['How do you want to filter?'] == "not equal to":
                if consort_input_df.at[q, filtered_column] != filter_value:
                    consort_input_df.at[q, exclude_col_name] = "Included"
                    consort_input_df.at[q, include_col_name] =
                    consort_input_df.at[q, filtered_column]
                else:
                    consort_input_df.at[q, exclude_col_name] =
                    consort_input_df.at[q, filtered_column]
                    consort_input_df.at[q, include_col_name] = "Excluded"
            elif query['How do you want to filter?'] > "greater than":
                if consort_input_df.at[q, filtered_column] != filter_value:
                    consort_input_df.at[q, exclude_col_name] = "Included"
                    consort_input_df.at[q, include_col_name] =
                    consort_input_df.at[q, filtered_column]
                else:
                    consort_input_df.at[q, exclude_col_name] =
                    consort_input_df.at[q, filtered_column]
                    consort_input_df.at[q, include_col_name] = "Excluded"
            elif query['How do you want to filter?'] == "less than":
                if consort_input_df.at[q, filtered_column] < filter_value:
                    consort_input_df.at[q, exclude_col_name] = "Included"
                    consort_input_df.at[q, include_col_name] =
                    consort_input_df.at[q, filtered_column]
                else:
                    consort_input_df.at[q, exclude_col_name] =
                    consort_input_df.at[q, filtered_column]
                    consort_input_df.at[q, include_col_name] = "Excluded"
    try:
        # Write .csv file for data
        consort_input_df = 'src/gg/consort_input_df.csv'
        df.to_csv(consort_input_df, index=False)
    except Exception as e:
        print(f"Unable to write .csv files.")
        sys.exit(1)


if __name__ == '__main__':
    main()
