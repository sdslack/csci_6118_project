import unittest
import sys
import random
import os
import csv
sys.path.insert(0, '../../src/lkr')  # noqa
from lkr_utils import count_sequences_by_column
from lkr_utils import plot_histogram_from_csv


class TestDaysFromInfectionPlot(unittest.TestCase):

    def test_basic_functionality(self):
        csv_file = '../../test/data/input/Fake_HIV.csv'
        output_file = '../../test/data/output/dfi_output.csv'
        
        count_sequences_by_column(csv_file, 0, output_file)

        self.assertTrue(os.path.isfile(output_file))

        expected_count = 6
        with open(output_file, 'r', newline='') as output:
            reader = csv.reader(output)
            next(reader)  # Skip the header
            for row in reader:
                days_from_infection, count = map(int, row)
                if days_from_infection == 30:
                    self.assertEqual(count, expected_count)
                    break
            else:
                self.fail("Expected count not found in the output file.")
                
    def test_file_not_found(self):
        csv_file = 'DNE.csv'
        output_file = 'DNE_output.csv'
        
        with self.assertRaises(FileNotFoundError):
            count_sequences_by_column(csv_file, 0, output_file)
    
    
    def test_plot_creation(self):
        csv_file = '../../test/data/output/dfi_output.csv'
        output_png = '../../docs/lkr_dfi_histogram.png'

        plot_histogram_from_csv(csv_file, output_png)

        self.assertTrue(os.path.isfile(output_png))

if __name__ == '__main__':
    unittest.main()
