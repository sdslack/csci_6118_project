import argparse
import query_utils as query
import sys
sys.path.insert(0, 'sds')  # noqa
import gbq_utils as gbq_utils

#### add global && and || between different columns and keep OR operation between multiple filters within a column 
#### user can only enter only && or only || otherwise there will be an error 

parser = argparse.ArgumentParser(
    description="Query and display data from a CSV file with filters.",
    prog="Project")
parser.add_argument("--file",
                    type=str,
                    help="Path to the CSV data file",
                    required=True)
parser.add_argument("--filters",
                    type=str,
                    help="Filter criteria for variables",
                    default="")
parser.add_argument("--query_output_file",
                    type=str,
                    help="Path to output CSV file",
                    required=True)
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
                    default = "")

args = parser.parse_args()


def main():
    # Get only columns of interest using Google BigQuery
    data = gbq_utils.get_gbq_data(args.filters, args.output_columns)

    if data is not None:
        # if there are any filters
        if args.filters != "":
            filter_args = query.split_arguments(args.filters)
            filters = query.get_filters(filter_args)

        # check for logical operator 
        operator = query.check_for_logical_operator(filters, args.global_logical_operator)
        
        # filter the data
        output_cols = args.output_columns.split(',')
        filtered_data = query.filter_data(data, filters, output_cols, operator.strip())

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
