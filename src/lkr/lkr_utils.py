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

# Example usage:
# count_sequences_by_column('your_input_file.csv', 'your_column_name', 'output_file.csv')



def plot_histogram_from_csv(output_file, output_png):
    """
    Read data from a CSV file and create a histogram plot, saving it as a PNG file.

    Args:
    - output_file (str): Path to the CSV file containing data.
    - output_png (str): Path to save the output PNG file.

    CSV File Format:
    - The input CSV file should have two columns: 'Days from Infection' and 'Number of Sequences'.

    Plot Details:
    - The function creates a histogram plot using Matplotlib.
    - X-axis: 'Days from Infection'
    - Y-axis: 'Number of Sequences'
    - The plot is saved as a PNG file.

    """
    # Read the CSV file and extract data
    days = []
    counts = []
    with open(output_file, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            day, count = map(int, row)
            days.append(day)
            counts.append(count)

    # Create a histogram plot
    plt.figure(figsize=(4, 2))
    plt.bar(days, counts, align='center', width=1.0)
    plt.xlabel('Days from Infection')
    plt.ylabel('Number of Sequences')
    plt.title('Sequence Counts by Days from Infection')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Hide the top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Save the plot as a PNG file
    plt.savefig(output_png, dpi=300, format='png')
    plt.close()
