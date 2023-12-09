import csv
import argparse
import matplotlib.pyplot as plt
import pandas as pd


def get_args():
    """
    Purpose of function:
    Parses command line arguments

    Returns:
    argparse.Namespace: Parsed command-line arguments

    Arguments:
    - `--csv_file` (str, required): Name of the CSV file
    - `--column_name` (str, required): Name of the column for histogram plot
    - `--output_file` (str, required): Name of the output file

    """
    parser = argparse.ArgumentParser(
        description='count specified data from a CSV file',
        prog='lkr_utils'
    )
    parser.add_argument('--csv_file',
                        type=str,
                        help='CSV file name',
                        required=False)
    parser.add_argument('--column_name',
                        type=str,
                        help='Column name for histogram',
                        required=False)
    parser.add_argument('--output_file',
                        type=str,
                        help='Output file name',
                        required=False)

    args = parser.parse_args()
    return args


def count_sequences_by_column(csv_file, column_name, output_file):
    """
    Purpose of function:
    1. Count occurrences of strings, floats, or integers in a specified column
    2. write the results to another CSV file

    Args:
    - csv_file (str): The path to the CSV file.
    - column_name (str): The name of the column to analyze.
    - output_file (str): The path to the output CSV file.

    Output CSV Format:
    - The output CSV will have two columns:
            original 'column_name' and 'Counts'

    """
    counts = {}

    # read CSV file
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

    # output data to a CSV file
    with open(output_file, 'w', newline='') as output:
        writer = csv.writer(output)
        writer.writerow([column_name, 'Counts'])
        for value, count in counts.items():
            writer.writerow([value, count])
