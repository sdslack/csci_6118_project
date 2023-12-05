import sys
import lkr_utils



def main():
    # Use the get_args function to parse command-line arguments
    args = lkr_utils.get_args()

    # Run count_sequences_by_column and plot_histogram_from_csv
    lkr_utils.count_sequences_by_column(args.csv_file,
                                        args.column_name,
                                        args.output_file)

    print(f"Output CSV file saved to: {args.output_file}")

if __name__ == "__main__":
    main()