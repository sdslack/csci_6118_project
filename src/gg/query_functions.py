import sys
import pandas as pd


# Create a query function which will change values on the query tracking table
def output_query_summary(column_name_of_interest, filter_param, value):
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

    Returns
    -------
    query
        A pandas dataframe with the search query settings for a given search
        Updated with the search query modifications through this summary
    """
    try:
        query = pd.read_csv('data/query_requests.csv')
    except NameError:
        print("The query dataframe cannot be found.")
        sys.exit(1)
    col_name_list = query.Search_Options.tolist()
    column_name_of_interest_list = [column_name_of_interest]
    if (any(x in column_name_of_interest_list
            for x in column_name_of_interest_list) == 'False'):
        # Handle the case where no matching columns are found
        raise ValueError("No filter criteria found. Please check query df.")
        sys.exit(1)
    column_name_of_interest = str(column_name_of_interest)
    filter_param_valid = ["equal to", "not equal to",
                          "less than", "greater than"]
    filter_param_list = [filter_param]
    if (any(x in filter_param_valid
            for x in filter_param_list) == 'False'):
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
        if data.empty() == TRUE:
            print("Dataframe is empty.")
            sys.exit(1)
    except NameError:
        print("The dataframe cannot be found.")
        sys.error(1)
    column_names_of_interest_list = [column_names]
    col_name_list = data.columns.tolist()
    if (any(x in col_name_list for x in column_name_of_interest_list)):
        data_subset = data[[column_names]]
        return data_subset
    else:
        # Handle the case where no matching columns are found
        print("No matching columns found in the DataFrame.")
        return None
        sys.exit(1)
