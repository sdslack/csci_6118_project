import csv
import matplotlib.pyplot as plt


def plot_histogram_from_csv(csv_file, output_png):
    # Read the CSV file and extract data
    days = []
    counts = []
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            day, count = map(int, row)
            days.append(day)
            counts.append(count)

    # Create a histogram plot
    plt.figure(figsize=(10, 6))
    plt.bar(days, counts, align='center', width=1.0)
    plt.xlabel('Days from Infection')
    plt.ylabel('Number of Sequences')
    plt.title('Sequence Counts by Days from Infection')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the plot as a PNG file
    plt.savefig(output_png, format='png')
    plt.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python plot_histogram.py <input_csv_file> " +
              "<output_png_file>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_png = sys.argv[2]

    plot_histogram_from_csv(input_csv, output_png)

print("Histogram plot saved as", output_png)
