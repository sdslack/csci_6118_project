import sys
import pandas as pd
import numpy as np
import re
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import os
sys.path.append('../jb')  # noqa
sys.path.append('../src/jb')  # noqa
sys.path.append('src/jb')  # noqa
sys.path.insert(0, '../../src/jb')  # noqa # THIS ONE
sys.path.insert(0, 'jb')  # noqa
sys.path.insert(0, '../src/gg')  # noqa
sys.path.insert(0, 'gg')  # noqa
import query_utils as query


def try_convert_to_fl(value):
    """This function will check if a value can be
    converted to a float without raising an error.
    Outputs a float if it is possible.

    Parameters
    ----------
    value: Any datatype

    Returns
    -------
    float_val: A float
    """
    try:
        float_val = float(value)
        return float_val
    except (ValueError, TypeError):
        return None


# Create a function to subset our data to the relevant columns being queried
def subset_dataframe_by_names(data, column_names):
    """Output is a subsetted dataframe, containing only the queried columns.

    Parameters
    ----------
    data: A pandas dataframe of the database data
    column_names: The names of the columns that are being queried

    Returns
    -------
    data_subset
        A pandas dataframe of database data
        Subset to include only the columns relevant to a given query
    """
    try:
        if not isinstance(data, pd.DataFrame):
            raise ValueError(data + " should be a pandas dataframe")
            sys.exit(1)
    except NameError:
        print(data + " cannot be found.")
        sys.error(1)
    if len(data) < 1:
        raise ValueError(data + " is empty.")
        sys.exit(1)
    if not isinstance(column_names, list):
        raise ValueError(column_names, "is not a list")
        sys.exit(1)
    column_names_of_interest_list = column_names
    col_name_list = data.columns.tolist()
    data_subset = pd.DataFrame()
    for col in column_names_of_interest_list:
        if col in col_name_list:
            data_subset[col] = data[col]
    # Handle the case where no matching columns are found
    if len(data_subset.columns) < 1:
        raise ValueError("No matching columns found in the DataFrame.")
        sys.exit(1)
    return data_subset


def consort_filter_data(data, filters,
                        bool_out_csv=None):
    """Filter the data based on the provided filters
    and create input for the consort plot

    Parameters
    ----------
    data : Pandas dataframe.
        Name of the file to be searched.
    filters: dict
        Dictionary of filters.
        Each label is the name of the column.
        Each value are the filter criteria.
    logical operator:
        How to combine filters from multiple columns
        Defaults to logical "and" ("&&").
        Other possibility is logical "or" ("||").
    bool_out_csv:
        Optional.
        If would like a copy of the consort_input_df as a csv,
        Include file path where it should be saved

    Returns
    -------
    consort_input_df:
        Input pandas dataframe for the create_consort_plot function
        With information about how each column has been filtered
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Data must be in a pandas dataframe")
        sys.exit(1)
    try:
        consort_input_df_pre = data
    except (NameError):
        print("Pandas dataframe data not found")
        sys.exit(1)

    # check if column is in data
    existing_cols = query.check_column_exists(filters.keys(),
                                              consort_input_df_pre)

    # Subset consort_input_df to only the relevant columns
    request_query_col = list(filters.keys())
    consort_input_df = subset_dataframe_by_names(consort_input_df_pre,
                                                 request_query_col)

    column_masks, not_equals_masks = \
        query.create_by_filter_boolean_filter_summary(filters,
                                                      consort_input_df,
                                                      existing_cols)

    for key in existing_cols:
        key_mask_combined = query.create_by_column_boolean_filter_summary(
            column_masks, not_equals_masks, key)
        column_name = f'Filtered_Column_{key}'
        consort_input_df[column_name] = key_mask_combined

    # Give option to write consort_input_df into a csv file
    if bool_out_csv is not None:
        try:
            bool_out_csv_str = str(bool_out_csv)
        except (ValueError):
            print("bool_out_csv must be a file path string")
        if not bool_out_csv_str.endswith(".csv"):
            raise KeyError("File path must end with .csv")
            sys.exit(1)
        try:
            consort_df_file_path = bool_out_csv_str
            consort_input_df.to_csv(consort_df_file_path, index=False)
        except (FileNotFoundError, OSError):
            print("File path not found. Please check bool_out_csv")
            sys.exit(1)

    # Output pandas dataframe for use in R
    return consort_input_df


def query_file_to_filter(query_summary_file):
    """This function will prepare a user query request file
    For the creation of a consort diagram. It is called
    in the make_query_df_formatted function.

    Parameters
    ----------
    query_summary_file:
        .csv file generated by query_utils.py

    Returns
    -------
    filters: A dictionary
        Listing how data should be filtered.
    """
    try:
        query_summary_file_pd = pd.read_csv(query_summary_file)
    except (FileNotFoundError, NameError):
        print("Cannot find " + query_summary_file)
        sys.exit(1)
    # Ensure correct format
    desired_columns = ["Search_Options", "Filter Criteria",
                       'Search by this column?']
    if not all(col in query_summary_file_pd.columns
               for col in desired_columns):
        raise ValueError("Incorrect column names in query_summary_file")
        sys.exit(1)

    query_summary_file_short = query_summary_file_pd[
        query_summary_file_pd['Search by this column?'] == 'Yes']

    filters = {}
    for index, row in query_summary_file_short.iterrows():
        new_filters = {}
        key_name = query_summary_file_short.loc[index, 'Search_Options']
        criteria_pre = query_summary_file_short.loc[index, 'Filter Criteria']
        if isinstance(criteria_pre, str):
            criteria = criteria_pre.split(';')
        else:
            criteria = criteria_pre
        new_filters = {key_name: criteria}
        filters.update(new_filters)
    return filters


# Format query summary
def make_query_df_formatted(filters=None, query_summary_file=None,
                            consort_input_data=None):
    """This function will use provided filters or a query summary file
    to format the query summary correctly for use for the R consort
    diagram code.

    Parameters
    ----------
    filters:
        Optional.
        A dictionary with keys as column names and values as
        filters you want to search by.

    query_summary_file:
        Optional.
        .csv file generated by query_utils.py

    consort_input_data:
        Must be specified when filters are given.
        The data to filter, in a pandas dataframe.

    Returns
    -------
    query_df_formatted: A formatted pandas df
        Ready for input into the run_consort_plot_rcode function.
    filters: A dictionary
        Listing how data should be filtered
    """
    if (filters is not None) & (query_summary_file is not None):
        raise ValueError("Cannot specify query_summary file and filters")
        sys.exit(1)
    elif filters is not None:
        if consort_input_data is None:
            raise ValueError("Must specify consort_input_data")
            sys.exit(1)
        elif isinstance(consort_input_data, pd.DataFrame):
            column_names = consort_input_data.columns.tolist()
            filter_args = query.split_arguments(filters)
            filters_provided = query.get_filters(filter_args)
            query_df_formatted_long = query.make_query_request_summary(
                filters_provided, column_names)
        else:
            raise ValueError("consort_input_data must be a pandas dataframe.")
    elif query_summary_file is not None:
        try:
            query_df_formatted_long = pd.read_csv(query_summary_file)
        except (FileNotFoundError, NameError):
            print("Cannot find " + query_summary_file)
            sys.exit(1)
        filters_provided = query_file_to_filter(query_summary_file)

    else:
        raise ValueError("Must specify either query_summary_file or filters")
        sys.exit(1)
    query_df_formatted = query_df_formatted_long[
        query_df_formatted_long['Search by this column?'] == 'Yes']
    return query_df_formatted, filters_provided


# Create a query function which will change values on the query tracking table
def run_consort_plot_rcode(consort_input_df,
                           query_df_formatted,
                           out_consort_png,
                           logical_operator="&&"):
    """Output is a png file of a consort diagram

    Parameters
    ----------
    consort_input_df: A pandas dataframe containing database data
    query_df_formatted: A pandas dataframe summarizing query requests
    out_consort_png: A file path ending in .png where consort will be saved
    logical operator:
        "&&" if data should be filtered to include
        entries which only satisfy ALL column filters
        There will be subsetting of the data in the consort diagram;
        the order of the filters will matter for visualization
        "||" if data should be filtered to include entries which satisfy
        at least one column filter
        There will be no subsetting of the data in the consort diagram
        between column filters.

    Returns
    -------
    out_consort_png is saved at the file path
    It contains a consort diagram with filters specified in query_df_formatted
    """
    try:
        if not isinstance(consort_input_df, pd.DataFrame):
            raise ValueError(
                consort_input_df + " should be a pandas dataframe")
            sys.exit(1)
    except NameError:
        print(consort_input_df + " cannot be found.")
        sys.exit(1)
    if len(consort_input_df) < 1:
        raise ValueError(consort_input_df + " is empty")

    try:
        if not isinstance(query_df_formatted, pd.DataFrame):
            raise ValueError(
                query_df_formatted + " should be a pandas dataframe")
            sys.exit(1)
    except NameError:
        print(query_df_formatted + " cannot be found.")
        sys.exit(1)
    if len(query_df_formatted) < 1:
        raise ValueError(query_df_formatted + " is empty")

    out_consort_png = str(out_consort_png)
    if not out_consort_png.endswith(".png"):
        raise ValueError("File path must end in .png")
        sys.exit(1)

    if logical_operator != "&&" and logical_operator != "||":
        raise ValueError("logical_operator must be equal to && or ||")
        sys.exit(1)

    pandas2ri.activate()

    r_consort_input_file = pandas2ri.py2rpy(consort_input_df)
    r_query_summary_file = pandas2ri.py2rpy(query_df_formatted)

    # Read the content of the R script
    if os.path.exists('consort_plot.r'):
        with open('consort_plot.r', 'r') as file:
            r_code = file.read()
    elif os.path.exists('gg/consort_plot.r'):
        with open('gg/consort_plot.r', 'r') as file:
            r_code = file.read()
    elif os.path.exists('src/gg/consort_plot.r'):
        with open('src/gg/consort_plot.r', 'r') as file:
            r_code = file.read()
    elif os.path.exists('../src/gg/consort_plot.r'):
        with open('../src/gg/consort_plot.r', 'r') as file:
            r_code = file.read()
    else:
        with open('../../src/gg/consort_plot.r', 'r') as file:
            r_code = file.read()
    # Execute r code
    robjects.r(r_code)
    # Call the function
    robjects.r['consort_plot_function'](r_consort_input_file,
                                        r_query_summary_file,
                                        out_consort_png,
                                        logical_operator)
    pandas2ri.deactivate()
