import csv
import argparse
import matplotlib.pyplot as plt


def get_args():
    """
    Parses command line arguments for extracting data from a CSV file and generating a histogram plot.

    Returns:
    argparse.Namespace: Parsed command-line arguments.

    Arguments:
    - `--csv_file` (str, required): Name of the CSV file.
    - `--column_name` (str, required): Name of the column for histogram plot.
    - `--output_file` (str, required): Name of the output file.
    - `--output_png` (str, optional): Name of PNG file for histogram plot.

    """
    parser = argparse.ArgumentParser(
        description='Pull specified data from a CSV file and generate a histogram plot.',
        prog='lkr_utils'
    )
    parser.add_argument('--csv_file', type=str, help='CSV file name', required=True)
    parser.add_argument('--column_name', type=str, help='Column name for histogram', required=True)
    parser.add_argument('--output_file', type=str, help='Output file name', required=True)
    parser.add_argument('--output_png', type=str, help='PNG file for histogram', required=False)

    args = parser.parse_args()
    return args



import csv

def count_sequences_by_column(csv_file, column_name, output_file):
    """
    Count the occurrences of values in a specified column of a CSV file and write the results to another CSV file.

    Args:
    - csv_file (str): The path to the CSV file.
    - column_name (str): The name of the column to analyze.
    - output_file (str): The path to the output CSV file.

    Output CSV Format:
    - The output CSV will have two columns: the original 'column_name' and 'Counts'.

    """
    # Create a dictionary to store the counts
    counts = {}

    # Read the CSV file
    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            value = row.get(column_name)
            
            if value is not None:
                # Treat the value as a string
                if value not in counts:
                    counts[value] = 1
                else:
                    counts[value] += 1

    # Write the data to a CSV file
    with open(output_file, 'w', newline='') as output:
        writer = csv.writer(output)
        writer.writerow([column_name, 'Counts'])
        for value, count in counts.items():
            writer.writerow([value, count])
