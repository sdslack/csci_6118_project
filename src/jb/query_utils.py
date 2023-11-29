"""Getting the data based on the input by the user to create plots.
"""

import argparse
import pandas as pd
import re


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
        raise FileNotFoundError("File not found. Please provide a valid file path.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("The provided file is empty.")
        sys.exit(1)

def check_column_exists(col_names, df):
    """Make sure the column exists in the data frame.

    Parameters
    ----------
    col_names : list
        Name of the columns to be searched for.

    df: data frame
        Data frame to search
    Returns
    -------
    existing_columns
        A list of all existing columns.
    """
    existing_columns = []

    for col_name in col_names:
        try:
            df[col_name]
            existing_columns.append(col_name)
        except KeyError:
            raise KeyError(f"The column '{col_name}' is not present in the DataFrame.")
            sys.exit(1)

    return existing_columns


def extract_symbol_and_value(user_input):
    """Extract the filter symbol and value, removing extra spacing
    
    Parameters
    ----------
    user_input : str
        String of the filter criteria.

    Returns
    -------
    symbol
        Filter symbol.
    value
        Filter value.
    cleaned_input
        Cleaned spacing for range values. 
    """
    cleaned_input = re.sub(r'\s', '', user_input)
    match = re.match(r'([><=!]+)([^><=!]+)', cleaned_input)

    if match:
        symbol = match.group(1)
        value = match.group(2)
        return symbol, value
    else:
        return '-', cleaned_input


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
    # check if column is in data
    existing_cols = check_column_exists(filters.keys(), data)
    for key, values in filters.items():
        if key in existing_cols:
            column_masks = []
            not_equals_masks = []
            if data[key].dtype == 'object':
                for value in values:
                    # remove any extra spacing between symbol and value
                    symbol, val = extract_symbol_and_value(value)
                    if symbol == '!=':
                        mask = (filtered_data[key] != val)
                        not_equals_masks.append(mask)
                    elif symbol == '=':
                        mask = (filtered_data[key] == val)
                        column_masks.append(mask)
            else:
            # Numerical variable filter
                for value in values:
                    # remove any extra spacing between symbol and value
                    symbol, val = extract_symbol_and_value(value)
                    if symbol == '<=':
                        mask = (filtered_data[key] <= float(val))
                        column_masks.append(mask)
                    elif symbol == '>=':
                        mask = (filtered_data[key] >= float(val))
                        column_masks.append(mask)
                    elif symbol == '<':
                        mask = (filtered_data[key] < float(val))
                        column_masks.append(mask)
                    elif symbol == '>':
                        mask = (filtered_data[key] > float(val))
                        column_masks.append(mask)
                    elif symbol == '-':
                        lower, upper = map(float, val.split('-'))
                        mask = ((filtered_data[key] >= lower) &
                                (filtered_data[key] <= upper))
                        column_masks.append(mask)
                    elif symbol == '!=':
                        mask = (filtered_data[key] != float(val))
                        not_equals_masks.append(mask)
                    elif symbol == '=':
                        mask = (filtered_data[key] == float(val))
                        column_masks.append(mask)

         # get filtered data for that column and deal with != last
        if column_masks and not_equals_masks:
            combined_column_mask = pd.concat(column_masks, axis=1).any(axis=1)
            combined_not_equals_mask = pd.concat(not_equals_masks, axis=1).all(axis=1)
            summary_mask = pd.concat([combined_column_mask, combined_not_equals_mask],
                                     axis=1).all(axis=1)
        elif not_equals_masks:
            combined_not_equals_mask = pd.concat(not_equals_masks, axis=1).all(axis=1)
            summary_mask = combined_not_equals_mask
        elif column_masks:
            combined_column_mask = pd.concat(column_masks, axis=1).any(axis=1)
            summary_mask = combined_column_mask

        filtered_data = filtered_data[summary_mask]
    # output specific columns if specified
    if len(output_cols) == 1 and output_cols[0] == '':
        return filtered_data
    else:
        # check that these column names exist
        col_names = [col.strip() for col in output_cols]
        existing_cols = check_column_exists(col_names, data)

        return filtered_data[existing_cols]

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

    # cleans list for any empty values in case extra && is included
    cleaned_args = [filter.strip() for filter in filter_args if filter]
    return cleaned_args


def get_filters(filter_args):
    """Split filters.

    Parameters
    ----------
    filter_args: list
        List of columns to be filtered and their filter criteria.

    Returns
    -------
    filters
        Dictionary of all filters.
    """
    filters = {}
    for arg in filter_args:
        key, values = arg.split(':')
        # Remove extra spaces
        key = key.strip()
        values = values.split(',')
        # cleans list for any empty values in case extra , is added
        values = [val.strip() for val in values if val]
        filters[key] = values
    return filters


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
                 'Filter Criteria',
                 'Do you plan to search by this column?']
    query_request_df = pd.DataFrame(columns=col_names)
    query_request_df['Search_Options'] = df_columns

    for col, criteria in filters.items():
        # make sure user specified column is an actual column
        if col in df_columns:
            variable = query_request_df['Search_Options'] == col
            # join filters by ;
            joined_filters = ';'.join(criteria)
            query_request_df.loc[variable, 'Filter Criteria'] = joined_filters
            plan_to_search = 'Do you plan to search by this column?'
            query_request_df.loc[variable, plan_to_search] = 'yes'

    return query_request_df
