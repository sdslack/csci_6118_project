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
    - multiple filters ex. "col:7,<5,9-12"
- for categorical fields, filters are a list of comma separated names
    - ex. "col=banana,red,blue"
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
            for value in values:
                if '<' in value:
                    filtered_data = filtered_data[
                        filtered_data[key] < float(value[1:])]
                elif '>' in value:
                    filtered_data = filtered_data[
                        filtered_data[key] > float(value[1:])]
                elif '-' in value:
                    lower, upper = map(float, value.split('-'))
                    filtered_data = filtered_data[(filtered_data[key] > lower) & (filtered_data[key] < upper)]
                elif '=' in value:
                    filtered_data = filtered_data[filtered_data[key] == float(value[1:])]
    return filtered_data


def main():
    parser = argparse.ArgumentParser(
        description="Query and display data from a CSV file with filters.",
        prog="Project")
    parser.add_argument("--file",
                        type=str,
                        help="Path to the CSV data file")
    parser.add_argument("--categorical_filters",
                        type=str,
                        help="Filter criteria for categorical variables (format in README)",
                        default="")
    parser.add_argument("--numerical_filters",
                        type=str,
                        help="Filter criteria for numerical variables (format in README)",
                        default="")
    parser.add_argument("--output_file",
                        type=str,
                        help="Path to output CSV file",
                        required=True)

    args = parser.parse_args()

    data = load_data(args.file)

    if data is not None:
        # dictionary for filters
        filters = {}

        # if there are any categorical filters
        if args.categorical_filters != "":
            categorical_filters = {}
            filter_args = args.categorical_filters.strip()
            cat_args = filter_args.split('&&')

            for arg in cat_args:
                key, values = arg.split(':')
                # Remove extra spaces
                key = key.strip()
                values = values.split(',')
                values = [val.strip() for val in values]
                categorical_filters[key] = values
            filters.update(categorical_filters)

        # if there are any numerical filters
        if args.numerical_filters != "":
            numerical_filters = {}
            filter_args = args.numerical_filters.strip()
            num_args = filter_args.split('&&')

            for arg in num_args:
                key, values = arg.split(':')
                # Remove extra spaces
                key = key.strip()
                values = values.split(',')
                values = [val.strip() for val in values]  # Remove extra spaces
                values = [val if any(op in val for op in ['<', '>', '-', '=']) else float(val) for val in values]
                numerical_filters[key] = values
            filters.update(numerical_filters)

        # filter the data
        filtered_data = filter_data(data, filters)

        if not filtered_data.empty:
            filtered_data.to_csv(args.output_file, index=False)
            print(f"Filtered data saved to {args.output_file}")
        else:
            print("No matching data found.")


if __name__ == "__main__":
    main()
