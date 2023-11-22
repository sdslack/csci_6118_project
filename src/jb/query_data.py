"""Getting the data based on the input by the user to create plots.

Need to think about:
- need a function that will return values to plot
    - what columns they want
    - what and how many filters they want to filter their data by

Notes:
=======
- takes in the filters as an entire string
    - separate parameters for categorical filters vs numerical filters
    - if there are multiple variables, they need to be separated with &&
        ex. --categorical_filter "col1:val1,val2 && col2:val3,val4"
- for numerical filter, filters can be taken as:
    - a range ex. "col:0-7" (exclusive)
    - less than or greater than the field ex. "col<10" or "col>10" (exclusive)
    - not equal ex. "col!=10"
    - multiple filters ex. "col:7,<5,9-12"
- for categorical fields, filters are a list of comma separated names
    - ex. "col:banana,red,blue"
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
        return None
    except pd.errors.EmptyDataError:
        print("The provided file is empty.")
        return None


def filter_data(data, filters):
    """Filter the data based on the provided filters.

    Parameters
    ----------
    data : data frame
                Name of the file to be searched.
    filters: dict
                Dictionary of filters.
                Each label is the name of the column.
                Each value are the filter criteria.
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
            filtered_data[key] = pd.to_numeric(filtered_data[key], errors = 'coerce')
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
    return filtered_data


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
