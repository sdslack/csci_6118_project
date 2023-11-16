import sys
import pandas as pd


# Create a query function which will change values on the query tracking table
def output_query_summary(column_name_of_interest, filter_param,
                         value, query_summary_file):
    """Output is a pandas dataframe.
    It describes the chosen parameters for a database search.

    Parameters
    ----------
    column_name_of_interest: a column in a pandas dataframe
        This column should be specified by name
    filter_param: a string specifying what we want to test
        This value should be:
        "equal to",
        "not equal to",
        "less than",
        or "greater than"
    value: The filter value is what we want to test.
        This should match the same datatype as the column_name_of_interest
    query_out_file: The path to a .csv file containing:
        A column with all column names from the lanl database
        A column with Yes/No for if you want to filter by this column
        A column with the way you want to filter (filter param)
        A column with the value you want to compare the lanl column value to

    Returns
    -------
    query
        A pandas dataframe with the search query settings for a given search
        Updated with the search query modifications through this summary
    """
    try:
        query = pd.read_csv(query_summary_file)
    except NameError:
        print("The query dataframe cannot be found.")
        sys.exit(1)
    col_name_list = query['Search_Options'].tolist()
    column_name_of_interest_list = [column_name_of_interest]
    if (any(x in column_name_of_interest_list
            for x in col_name_list) is False):
        # Handle the case where no matching columns are found
        raise ValueError("No filter criteria found. Please check query df.")
        sys.exit(1)
    column_name_of_interest = str(column_name_of_interest)
    filter_param_valid = ["equal to", "not equal to",
                          "less than", "greater than"]
    filter_param_list = [filter_param]
    if (any(x in filter_param_valid
            for x in filter_param_list) is False):
        raise ValueError("Incorrect input for filter_param")
        sys.exit(1)
    query.loc[query.Search_Options == column_name_of_interest,
              'Do you plan to search by this column?'] = "Yes"
    query.loc[query.Search_Options == column_name_of_interest,
              'How do you want to filter?'] = filter_param
    query.loc[query.Search_Options == column_name_of_interest,
              'Filter Value'] = value
    return query


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


def reset_query(data):
    """Output is a csv file.
    It describes the chosen parameters for a database search.

    Parameters
    ----------
    data_file_name: The path to a .csv file containing LANL data
    query_summary_file: The path to a .csv file containing:
        A column with all column names from the lanl database
        A column with Yes/No for if you want to filter by this column
        A column with the way you want to filter (filter param)
        A column with the value you want to compare the lanl column value to
        All values will be reset to their default values

    Returns
    -------
    query_summary_file
        A .csv file with the default (empty) search query settings
    """
    if len(data) < 1:
        raise ValueError("Dataset not found")
        sys.exit(1)
    else:
        lanl = data
    query_pre = {
        'Search_Options': lanl.columns,
        'Search by this column?':
            ["No"] * len(lanl.columns),
        'How do you want to filter?': [None] * len(lanl.columns),
        'Filter Value': [None] * len(lanl.columns)}
    query = pd.DataFrame(query_pre)
    return query
