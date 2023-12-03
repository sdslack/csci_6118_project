"""Getting the data based on the input by the user to create plots.
"""

import argparse
import pandas as pd
import re
import sys


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
    user_input = str(user_input)
    cleaned_input = user_input.strip()
    match = re.match(r'([><=!]+)([^><=!]+)', cleaned_input)

    if match:
        symbol = match.group(1)
        value = match.group(2)
        value_cleaned = value.strip()
        return symbol, value
    else:
        return '-', cleaned_input


def filter_data(data, filters, output_cols, logical_operator="&&"):
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

    # Create dictionaries to store masks for each key
    column_masks = {}
    not_equals_masks = {}
    
    for key, values in filters.items():
        if key in existing_cols:
            if key not in column_masks:
                column_masks[key] = []
                not_equals_masks[key] = []
            
            if data[key].dtype == 'object':
                for value in values:
                    symbol, val = extract_symbol_and_value(value)
                    if symbol == '!=':
                        mask = (filtered_data[key] != val)
                        not_equals_masks[key].append(mask)
                    elif symbol == '=':
                        mask = (filtered_data[key] == val)
                        column_masks[key].append(mask)
            else:
                for value in values:
                    symbol, val = extract_symbol_and_value(value)
                    if symbol in ('<=', '>=', '<', '>', '-', '!=', '='):
                        mask = create_numeric_mask(filtered_data[key], symbol, val)
                        if symbol == '!=':
                            not_equals_masks[key].append(mask)
                        else:
                            column_masks[key].append(mask)
    summary_masks = []
    for key in existing_cols:
        column_mask_key_combined = []
        not_equals_mask_key_combined = []
        key_mask_combined = []
        if (key in column_masks) and (column_masks[key]):
            column_mask_key_combined = pd.concat(column_masks[key], axis=1).any(axis=1)
        if (key in not_equals_masks) and (not_equals_masks[key]):
            not_equals_mask_key_combined = pd.concat(not_equals_masks[key], axis=1).all(axis=1)
        if len(column_mask_key_combined)>=1 and len(not_equals_mask_key_combined)>=1:
            key_mask_combined = pd.concat([not_equals_mask_key_combined, column_mask_key_combined],
                                          axis=1).all(axis=1)
        elif len(column_mask_key_combined)>=1:
            key_mask_combined = column_mask_key_combined
        elif len(not_equals_mask_key_combined)>=1:
            key_mask_combined = not_equals_mask_key_combined

        summary_masks.append(key_mask_combined)

    # Combine all summary masks into the final mask
    if summary_masks and logical_operator == '||':
        final_mask = pd.concat(summary_masks, axis=1).any(axis=1)
        filtered_data = filtered_data[final_mask]
    else:
        final_mask = pd.concat(summary_masks, axis=1).all(axis=1)
        filtered_data = filtered_data[final_mask]
    
    # output specific columns if specified
    if len(output_cols) == 1 and output_cols[0] == '':
        return filtered_data
    else:
        col_names = [col.strip() for col in output_cols]
        existing_cols = check_column_exists(col_names, data)
        return filtered_data[existing_cols]

# Helper function for creating numeric masks
def create_numeric_mask(column, symbol, value):
    if symbol == '<=':
        return (column <= float(value))
    elif symbol == '>=':
        return (column >= float(value))
    elif symbol == '<':
        return (column < float(value))
    elif symbol == '>':
        return (column > float(value))
    elif symbol == '-':
        lower, upper = map(float, value.split('-'))
        return ((column >= lower) & (column <= upper))
    elif symbol == '!=':
        return (column != float(value))
    elif symbol == '=':
        return (column == float(value))


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
    filter_args = args.split(';')

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


def check_for_logical_operator(filters, operator):
    """Check to make sure there is a global logical operator
    especially if there are two or more filter columns.

    Parameters
    ----------
    filters: dictionary
        Dictionary of filters.
        Each label is the name of the column.
        Each value are the filter criteria.
    operator: str
        Global logical operator 

    Returns
    -------
    operator 
        || or &&.
    """
    # multiple column filters
    if len(filters.keys()) > 1:
        # default operator if no operator is entered
        if operator == "":
            return '||'
        elif operator == '&&' or operator == '||':
            return operator
        else:
            print(f'Operator {operator} not valid.')
            sys.exit(1)
    # return default 
    else:
        return '||'
            
    