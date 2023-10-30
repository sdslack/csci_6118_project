import csv


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


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python count_sequences.py <input_csv_file> " +
              "<column_number> <output_csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    column_number = int(sys.argv[2])
    output_file = sys.argv[3]

    count_sequences_by_column(csv_file, column_number, output_file)

print("Analysis complete. Results saved to", output_file)
