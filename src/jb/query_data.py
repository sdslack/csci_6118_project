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
        return None
    except pd.errors.EmptyDataError:
        print("The provided file is empty.")
        return None


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
            print(f"The column '{col_name}' is not present in the DataFrame.")

    return existing_columns


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
                'How do you want to filter?',
                'Filter Value',
                'Do you plan to search by this column?']
    query_request_df = pd.DataFrame(columns = col_names)
    query_request_df['Search_Options'] = df_columns

    return query_request_summary
