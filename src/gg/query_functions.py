import sys


# Create a query function which will change values on the query tracking table
def output_query_summary(column_name_of_interest, filter_param, value):
    """Output is a pandas dataframe.
    It describes the chosen parametrs for a database search.

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
        query.empty() == FALSE
    except NameError:
        print("The query dataframe cannot be found.")
        sys.error(1)
    if column_name_of_interest not in query.columns:
        # Handle the case where no matching columns are found
        print("No filter criteria found. Please check query df.")
        sys.exit(1)
    column_name_of_interest = str(column_name_of_interest)
    filter_param_valid = ["equal to", "not equal to",
                          "less than", "greater than"]
    if filter_param not in filter_param_valid:
        print("Incorrect input for filter_param")
        sys.exit(1)
    if filter_param == ("less than", "greater than") & isinstance(value, str):
        print("Please input a float or integer datatype for value parameter")
    for i in range(len(query)):
        if query.loc[i, "Search_Options"] == column_name_of_interest:
            query.at[i, "Do you plan to search by this column?"] = True
            query.at[i, "How do you want to filter?"] = filter_param
            query.at[i, "Filter Value"] = value
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
    if column_names in data.columns:
        data_subset = data[column_names]
        return data_subset
    else:
        # Handle the case where no matching columns are found
        print("No matching columns found in the DataFrame.")
        return None
        sys.exit(1)
