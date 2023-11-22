import argparse
import query_data as query

parser = argparse.ArgumentParser(
    description="Query and display data from a CSV file with filters.",
    prog="Project")
parser.add_argument("--file",
                    type=str,
                    help="Path to the CSV data file",
                    required=True)
parser.add_argument("--categorical_filters",
                    type=str,
                    help="Filter criteria for categorical variables",
                    default="")
parser.add_argument("--numerical_filters",
                    type=str,
                    help="Filter criteria for numerical variables",
                    default="")
parser.add_argument("--output_file",
                    type=str,
                    help="Path to output CSV file",
                    required=True)
parser.add_argument("--output_columns",
                    type=str,
                    help="Columns to output to queried data file",
                    default="")

args = parser.parse_args()

def main():

    data = query.load_data(args.file)

    if data is not None:
        # dictionary for filters
        filters = {}

        # if there are any categorical filters
        if args.categorical_filters != "":
            cat_args = query.split_arguments(args.categorical_filters)

            categorical_filters = query.get_categorical_filters(cat_args)
            filters.update(categorical_filters)

        # if there are any numerical filters
        if args.numerical_filters != "":
            num_args = query.split_arguments(args.numerical_filters)

            numerical_filters = query.get_numerical_filters(num_args)
            filters.update(numerical_filters)

        # filter the data
        output_cols = args.output_columns.split(',')
        filtered_data = query.filter_data(data, filters, output_cols)

        if not filtered_data.empty:
            filtered_data.to_csv(args.output_file, index=False)
            print(f"Filtered data saved to {args.output_file}")
        else:
            print("No matching data found.")


if __name__ == "__main__":
    main()
