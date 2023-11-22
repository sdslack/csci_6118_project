import argparse
import query_data as query

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
# parser.add_argument("--query_request_file",
#                     type=str,
#                     help="Name and path of query request file",
#                     required=True)

args = parser.parse_args()

def main():

    data = query.load_data(args.file)

    if data is not None :
        # if there are any categorical filters
        if args.filters != "":
            filter_args = query.split_arguments(args.filters)
            filters = query.get_filters(filter_args)

        # filter the data
        output_cols = args.output_columns.split(',')
        filtered_data = query.filter_data(data, filters, output_cols)

        # # make the query request summary data frame
        # query_request_df = query.make_query_request_summary(filters, data.columns)

        if not filtered_data.empty:
            filtered_data.to_csv(args.query_output_file, index=False)
            # query_request_df.to_csv(args.query_request_file, index=False)
            print(f"Filtered data saved to {args.query_output_file}")
            # print(f"Query request summary saved to {args.query_request_file}")
        else:
            print("No matching data found.")
    
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
