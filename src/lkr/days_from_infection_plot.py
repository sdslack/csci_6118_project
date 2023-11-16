import sys
from lkr_utils import count_sequences_by_column, plot_histogram_from_csv

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  For counting sequences: python main_script.py count <input_csv_file> <column_number> <output_csv_file>")
        print("  For plotting histogram: python main_script.py plot <input_csv_file> <output_png_file>")
        sys.exit(1)

    operation = sys.argv[1]

    if operation == "count" and len(sys.argv) == 5:
        csv_file = sys.argv[2]
        column_number = int(sys.argv[3])
        output_file = sys.argv[4]

        count_sequences_by_column(csv_file, column_number, output_file)
        print("Analysis complete. Results saved to", output_file)

    elif operation == "plot" and len(sys.argv) == 4:
        input_csv = sys.argv[2]
        output_png = sys.argv[3]

        plot_histogram_from_csv(input_csv, output_png)
        print("Histogram plot saved as", output_png)

    else:
        print("Invalid usage. Please check the provided arguments.")
        sys.exit(1)

