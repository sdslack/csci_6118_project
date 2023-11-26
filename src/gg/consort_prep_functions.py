import sys
import pandas as pd
import numpy as np
import re
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import os


def try_convert_to_fl(value):
    try:
        result = float(value)
        return result
    except (ValueError, TypeError):
        return None  # Return None or any other suitable value when conversion fails


def reformat_query_summary(query_summary_file):
    query_summary_file = pd.read_csv(query_summary_file)
    new_rows = []
    for _, row in query_summary_file.iterrows():
        values = row['Filter Value'].split(',')
        for value in values:
            new_row = row.copy()
            new_row['Filter Value'] = value
            new_rows.append(new_row)
    # Creating a new DataFrame from the list of rows
    query_df_formatted = pd.DataFrame(new_rows)
    return query_df_formatted


# Create a function to subset our data to the relevant columns being queried
def subset_dataframe_by_names(data, column_names):
    """Output is a subsetted dataframe, containing only the queried columns.

    Parameters
    ----------
    data: A pandas dataframe
    column_names: The names of the columns that are being queried

    Returns
    -------
    query
        A pandas dataframe with the search query settings for a given search
        Updated with the search query modifications through this summary
    """
    try:
        if len(data) < 1:
            print("Dataframe is empty.")
            sys.exit(1)
    except NameError:
        print("The dataframe cannot be found.")
        sys.error(1)
    column_names_of_interest_list = column_names
    col_name_list = data.columns.tolist()
    data_subset = pd.DataFrame()
    data_subset['All'] = 1
    for col in column_names_of_interest_list:
        if col in col_name_list:
            data_subset[col] = data[col]
    # Handle the case where no matching columns are found
    if len(data_subset.columns) < 2:
        raise ValueError("No matching columns found in the DataFrame.")
        sys.exit(1)
    return data_subset


def format_consort_input_file(consort_input_df_pre, query_df_formatted):
    consort_input_df_pre = pd.read_csv(consort_input_df_pre)

    # Subset the consort_input_df to only the relevant columns
    request_query_col = set(query_df_formatted['Search_Options'].tolist())
    consort_input_df = subset_dataframe_by_names(consort_input_df_pre,
                                                 request_query_col)

    # Ensure both are zero indexed
    query_df_formatted.reset_index(drop=True, inplace=True)
    consort_input_df.reset_index(drop=True, inplace=True)

    for i in range(len(query_df_formatted)):
        filtered_column = query_df_formatted['Search_Options'][i]
        filter_value = str(query_df_formatted['Filter Value'][i])
        inclusion_info_name = "Include_Column" + str(i)
        consort_input_df[inclusion_info_name] = "Unknown"

        # Remove specified special characters using iteration
        special_chars = ['=', '!', '>', '<', '==', '>=', '<=', '=!']

        filter_no_sp_char = ''.join(char for char in filter_value if char not in special_chars)

        # If possible, convert to numeric
        filter_num = try_convert_to_fl(filter_no_sp_char)  # Get the value after the operator

        # Perform comparison based on the operator
        mask = np.zeros(len(consort_input_df), dtype=bool)
        if '=' in filter_value:
            mask = consort_input_df[filtered_column] == filter_no_sp_char
        elif '!=' in filter_value:
            mask = consort_input_df[filtered_column] != filter_no_sp_char
        elif "-" in filter_value:
            part1, part2 = filter_no_sp_char.split('-')
            part1 = float(part1)
            part2 = float(part2)
            print(part1, part2)
            mask = (
                consort_input_df[filtered_column] >= part1) & (
                consort_input_df[filtered_column] < part2)
        elif '>' in filter_value:
            mask = consort_input_df[filtered_column] > filter_num
        elif '>=' in filter_value:
            mask = consort_input_df[filtered_column] >= filter_num
        elif '<' in filter_value:
            mask = consort_input_df[filtered_column] < filter_num
        elif '<=' in filter_value:
            mask = consort_input_df[filtered_column] <= filter_num

        # Update inclusion_info_name based on the mask
        consort_input_df.loc[mask, inclusion_info_name] = "Included"
        consort_input_df.loc[~mask, inclusion_info_name] = "Excluded"

    return consort_input_df
    # try:
    #     # Write .csv file for data
    #     consort_input_df.to_csv(consort_input_file, index=False)
    # except Exception as e:
    #     print(f"Unable to write .csv files.")
    #     sys.exit(1)


# Create a query function which will change values on the query tracking table
def run_consort_plot_rcode(consort_input_df,
                          query_df_formatted,
                          out_consort_png):
    """Output is a png file of a consort diagram

    Parameters
    ----------
    consort_input_file: A .csv file containing database data
    query_summary_file: A .csv file summarizing query requests
    out_consort_png: A file path ending in .png where consort will be saved

    Returns
    -------
    query
        A pandas dataframe with the search query settings for a given search
        Updated with the search query modifications through this summary
    """
#     # Check if all arguments are correct
#     if not os.path.exists(consort_input_file):
#         raise FileNotFoundError("consort_input_file does not exist.")
#         sys.exit(1)

#     if not os.path.exists(query_summary_file):
#         raise FileNotFoundError("query_summary_file does not exist.")
#         sys.exit(1)

#     if not out_consort_png.endswith(".png"):
#         raise ValueError("out_consort_png does not end with '.png'")
#         sys.exit(1)
    pandas2ri.activate()
    r_consort_input_file = pandas2ri.py2rpy(consort_input_df)
    r_query_summary_file = pandas2ri.py2rpy(query_df_formatted)

    # Read the content of the R script
    with open('src/gg/consort_plot.r', 'r') as file:
        r_code = file.read()
    # Execute r code
    robjects.r(r_code)
    # Call the function
    robjects.r['consort_plot_function'](r_consort_input_file,
                                       r_query_summary_file,
                                       out_consort_png)
    pandas2ri.deactivate()

