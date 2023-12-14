import argparse
import query_utils as query
import sys
import pandas as pd
sys.path.insert(0, '../../src/sds')  # noqa
import gbq_utils as gbq_utils
sys.path.insert(0, 'sds')  # noqa
sys.path.insert(0, '../sds')  # noqa
sys.path.insert(0, '../src/sds')  # noqa

# add global && and || between different columns
# keep OR operation between multiple filters within a column
# user can only enter only && or only || otherwise there will be an error

parser = argparse.ArgumentParser(
    description="Query and display data with filters. Automatically " +
                "queries full dataset stored on Google BigQuery. Use " +
                "optional --file argument with path to CSV file if " +
                "want to query local file instead.",
    prog="get_queried_data.py")
parser.add_argument("--file",
                    type=str,
                    help="Optional path to CSV data file, if not given " +
                    "will query full data on Google BigQuery",
                    required=False)
parser.add_argument("--filters",
                    type=str,
                    help="Filter criteria for variables",
                    default="")
parser.add_argument("--query_output_file",
                    type=str,
                    help="Path to output CSV file",
                    required=True)
parser.add_argument("--query_cols_all_data_file",
                    type=str,
                    help="Path to output CSV file with all values from " +
                    "the queried and requested columns, before filtering",
                    required=False)
parser.add_argument("--output_columns",
                    type=str,
                    help="Columns to output to queried data file",
                    default="")
parser.add_argument("--query_request_file",
                    type=str,
                    help="Name and path of query request file",
                    required=True)
parser.add_argument("--global_logical_operator",
                    type=str,
                    help="|| or && if multiple filter columns",
                    default="")

args = parser.parse_args()


def main():
    # Check if getting full data from Google BigQuery or if local
    # path to CSV was given
    if args.file is not None:
        data = query.load_data(args.file)
    else:
        # Get only columns of interest using Google BigQuery
        data = gbq_utils.get_gbq_data(args.filters, args.output_columns)

    if args.query_cols_all_data_file is not None:
        data.to_csv(args.query_cols_all_data_file, index=False)
        print(f"All data for queried and requested columns saved to " +
              f"{args.query_cols_all_data_file}")

    if data is not None:
        # if there are any filters
        if args.filters != "":
            filter_args = query.split_arguments(args.filters)
            filters = query.get_filters(filter_args)

        # check for logical operator
        operator = query.check_for_logical_operator(
            filters, args.global_logical_operator)

        # filter the data
        output_cols = args.output_columns.split(',')
        filtered_data = query.filter_data(
            data, filters, output_cols, operator.strip())

        # make the query request summary data frame
        query_request_df = query.make_query_request_summary(filters,
                                                            data.columns)

        if not filtered_data.empty:
            filtered_data.to_csv(args.query_output_file, index=False)
            query_request_df.to_csv(args.query_request_file, index=False)
            print(f"Filtered data saved to {args.query_output_file}")
            print(f"Query request summary saved to {args.query_request_file}")
        else:
            print("No matching data found.")

    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
