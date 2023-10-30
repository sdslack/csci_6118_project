"""Getting the data based on the input by the user to create plots.

Need to think about:
- need a function that will return values to plot
    - what columns they want
    - what and how many filters they want to filter their data by

Notes:
- takes in the filter as an entire string
- for numerical fields, filters can be taken as:
    - a range ex. "col = 0-7"
    - less than or greater than the field ex. "col<10" or "col>10"
    - multiple filters ex. "col=7,<5,9-12"
- for categorical fields, filters can only be taken as a list of
    comma separated individual names
    - ex. "col=banana,red,blue"
- code can take multiple categorical and numerical varibles comma
    separated but need to have spaces between each different variable
"""

import argparse
import pandas as pd


def load_data(file_path):
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
    filtered_data = data
    for key, values in filters.items():
        # Categorical variable filter
        if isinstance(values[0], str):
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
                        (filtered_data[key] >= lower) &
                        (filtered_data[key] <= upper)]
                else:
                    filtered_data = filtered_data[
                        filtered_data[key] == float(value)]
    return filtered_data


def main():
    parser = argparse.ArgumentParser(
        description="Query and display data from a CSV file with filters.",
        prog="Project")
    parser.add_argument("--file",
                        type=str,
                        help="Path to the CSV data file")
    parser.add_argument(
        "--filter",
        type=str,
        help="Filter criteria (use format specified in README)",
        default="")

    args = parser.parse_args()

    data = load_data(args.file)

    if data is not None:
        # dictionary for filters
        filters = {}
        filter_args = args.filter.split(', ')

        # get the filters and their criteria
        for filter_arg in filter_args:
            key, values = filter_arg.split('=')
            values = values.split(',')
            # split numerical filters
            if any(['<', '>', '-'] in val for val in values):
                values = [val if any(op in val for op in ['<', '>', '=', '-'])
                          else float(val) for val in values]
            filters[key] = values

        # filter the data
        filtered_data = filter_data(data, filters)
        if not filtered_data.empty:
            print(filtered_data)
        else:
            print("No matching data found.")


if __name__ == "__main__":
    main()
