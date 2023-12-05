import unittest
import sys
import math
import os
import csv
sys.path.insert(0, '../../src/lkr')  # noqa
from lkr_utils import count_sequences_by_column


class TestDaysFromInfectionPlot(unittest.TestCase):

    def test_integer_counts(self):
        csv_file = '../../test/data/input/Fake_HIV.csv'
        output_file = '../../test/data/output/int_count_output.csv'
        column_name = 'Days from Infection'

        count_sequences_by_column(csv_file, column_name, output_file)

        self.assertTrue(os.path.isfile(output_file))

        expected_count = 6
        with open(output_file, 'r', newline='') as output:
            reader = csv.reader(output)
            next(reader)
            for row in reader:
                value, count = map(int, row)
                if value == 30:
                    self.assertEqual(count, expected_count)
                    break
            else:
                self.fail("Expected count not found in the output file.")

    def test_string_counts(self):
        csv_file = '../../test/data/input/Fake_HIV.csv'
        output_file = '../../test/data/output/str_count_output.csv'
        column_name = 'Sequence'

        count_sequences_by_column(csv_file, column_name, output_file)

        self.assertTrue(os.path.isfile(output_file))

        expected_count_a = 9
        expected_count_b = 9
        expected_count_c = 16

        with open(output_file, 'r', newline='') as output:
            reader = csv.reader(output)
            next(reader)
            for row in reader:
                sequence, count = row
                if sequence == 'a':
                    self.assertEqual(int(count), expected_count_a)
                elif sequence == 'b':
                    self.assertEqual(int(count), expected_count_b)
                elif sequence == 'c':
                    self.assertEqual(int(count), expected_count_c)

    def test_float_counts(self):
        csv_file = '../../test/data/input/Fake_HIV.csv'
        output_file = '../../test/data/output/float_count_output.csv'
        column_name = 'Float'

        count_sequences_by_column(csv_file, column_name, output_file)

        self.assertTrue(os.path.isfile(output_file))

        expected_counts = {
            0.91: 1,
            0.28: 2,
            0.53: 2,
            0.39: 1,
            0.06: 1,
        }

        tolerance = 1e-6

        with open(output_file, 'r', newline='') as output:
            reader = csv.reader(output)
            next(reader)

            for expected_value, expected_count in expected_counts.items():
                found = False
                for row in reader:
                    value, count = map(float, row)
                    if math.isclose(value, expected_value, rel_tol=tolerance):
                        found = True
                        self.assertEqual(int(count), expected_count)
                        break

                self.assertTrue(found, expected_value)

    def test_file_not_found(self):
        csv_file = 'DNE.csv'
        output_file = 'DNE_output.csv'

        with self.assertRaises(FileNotFoundError):
            count_sequences_by_column(csv_file, 0, output_file)


if __name__ == '__main__':
    unittest.main()
