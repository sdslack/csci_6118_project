"""Getting the data based on the input by the user to create plots.
"""

import argparse
import pandas as pd


def load_data(file_path):
    """Make sure the file exists.

    Parameters
    ----------
    file_path : str
        Name of the file to be searched.

    Returns
    -------
    data or None
        Data frame if exists or none if doesn't exist.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("The provided file is empty.")
        return None


def filter_data(data, filters, output_cols):
    """Filter the data based on the provided filters.

    Parameters
    ----------
    data : data frame
        Name of the file to be searched.
    filters: dict
        Dictionary of filters.
        Each label is the name of the column.
        Each value are the filter criteria.
    output_cols: list
        List of columns to output to final df.

    Returns
    -------
    filtered_data
        Final filtered data frame.
    """
    filtered_data = data
    for key, values in filters.items():
        # Categorical variable filter
        if data[key].dtype == 'object':
            filtered_data = filtered_data[filtered_data[key].isin(values)]
        # Numerical variable filter
        else: 
            for value in values:
                if '<' in value:
                    filtered_data = filtered_data[
                        filtered_data[key] < float(value[1:])]
                elif '>' in value:
                    filtered_data = filtered_data[
                        filtered_data[key] > float(value[1:])]
                elif '-' in value:
                    lower, upper = map(float, value.split('-'))
                    filtered_data = filtered_data[
                        (filtered_data[key] > lower)
                        & (filtered_data[key] < upper)]
                elif '!=' in value:
                    filtered_data = filtered_data[filtered_data[key]
                                                  != float(value[2:])]
                elif '=' in value:
                    filtered_data = filtered_data[filtered_data[key]
                                                  == float(value[1:])]

    # output specific columns if specified
    if len(output_cols) == 1 and output_cols[0] == '':
        return filtered_data
    else:
        col_names = [col.strip() for col in output_cols]
        return filtered_data[col_names]
        


def split_arguments(filter_parameter):
    """Split multiple filter arguments by &&.

    Parameters
    ----------
    filter_parameter: str
        User input for the filter arguments.

    Returns
    -------
    filter_args
        List of all filter arguments.
    """
    args = filter_parameter.strip()
    filter_args = args.split('&&')
    return filter_args


def get_numerical_filters(num_args):
    """Split numerical filters.

    Parameters
    ----------
    num_args: list
        List of columns to be filtered and their filter criteria.

    Returns
    -------
    numerical_filters
        List of all the numerical filters.
    """
    numerical_filters = {}
    for arg in num_args:
        key, values = arg.split(':')
        # Remove extra spaces
        key = key.strip()
        values = values.split(',')
        values = [val.strip() for val in values]
        values = [val if any(op in val for op in ['<', '>', '-', '='])
                  else float(val) for val in values]
        numerical_filters[key] = values
    return numerical_filters


def get_categorical_filters(cat_args):
    """Split categorical filters.

    Parameters
    ----------
    cat_args: list
        List of columns to be filtered and their filter criteria.

    Returns
    -------
    categorical_filters
        List of all the categorical filters.
    """
    categorical_filters = {}
    for arg in cat_args:
        key, values = arg.split(':')
        # Remove extra spaces
        key = key.strip()
        values = values.split(',')
        values = [val.strip() for val in values]
        categorical_filters[key] = values
    return categorical_filters


def make_query_request_summary(filters, df_columns):
    """Make a query request summary which is a summary
    of all variables and their filter criteria.

    Parameters
    ----------
    filters: dictionary
        Dictionary of filters.
        Each label is the name of the column.
        Each value are the filter criteria.
    df_columns: list
        List of all column names.

    Returns
    -------
    query_request_df
        Data frame of query request summary.
    """
    col_names = ['Search_Options',
                'How do you want to filter?',
                'Filter Value',
                'Do you plan to search by this column?']
    query_request_df = pd.DataFrame(columns = col_names)
    query_request_df['Search_Options'] = df_columns

    return query_request_summary
