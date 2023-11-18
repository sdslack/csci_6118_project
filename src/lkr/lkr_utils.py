import csv
import argparse
import matplotlib.pyplot as plt


def get_args():
    parser = argparse.ArgumentParser(
        description='pull specified data from csv file',
        prog='lkr_utils')
    parser.add_argument('--csv_file',
                        type=str,
                        help='name of the file',
                        required=True)
    parser.add_argument('--column_number',
                        type=int,
                        help='name of the column you want make hist plot for',
                        required=True)
    parser.add_argument('--output_file',
                        type=str,
                        help='name of file output data will go in',
                        required=True)
    parser.add_argument('--output_png',
                        type=str,
                        help='name of png file for histogram',
                        required=False)

    args = parser.parse_args()
    return args


def count_sequences_by_column(csv_file, column_number, output_file):
    # Create a dictionary to store the counts
    counts = {}

    # Read the CSV file
    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header

        for row in reader:
            if column_number < len(row):
                try:
                    days_from_infection = int(row[column_number])
                    if days_from_infection not in counts:
                        counts[days_from_infection] = 1
                    else:
                        counts[days_from_infection] += 1
                except ValueError:
                    # Handle non-integer values gracefully
                    pass

    # Write the data to a CSV file
    with open(output_file, 'w', newline='') as output:
        writer = csv.writer(output)
        writer.writerow(['Days from Infection', 'Number of Sequences'])
        for days, count in counts.items():
            writer.writerow([days, count])


def plot_histogram_from_csv(output_file, output_png):
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
