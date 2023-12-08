from contextlib import AbstractContextManager
from typing import Any
import unittest
import sys
import random
import os
sys.path.insert(0, '../../src/sds')  # noqa
import sds_utils


class TestSdsUtils(unittest.TestCase):
    def setUp(self):
        self.test_int_file = 'test_int_file.csv'
        f = open(self.test_int_file, 'w')
        f.write('Days from Infection,Counts\n')
        f.write('20,3\n')
        f.write('22,10\n')
        f.write('23,2\n')
        f.close()
        self.test_float_file = 'test_float_file.csv'
        f = open(self.test_float_file, 'w')
        f.write('Float,Counts\n')
        f.write('1.25,3\n')
        f.write('0.04,10\n')
        f.write('0.88,2\n')
        f.close()
        self.test_str_file = 'test_str_file.csv'
        f = open(self.test_str_file, 'w')
        f.write('Sequence,Counts\n')
        f.write('a,3\n')
        f.write('b,10\n')
        f.write('c,2\n')
        f.close()
        self.empty_file = "empty_file.csv"
        f = open(self.empty_file, 'w')
        f.close()
        self.test_int_messy_file = 'test_int_messy_file.csv'
        f = open(self.test_int_messy_file, 'w')
        f.write('Days,Counts\n')
        f.write('11,3\n')
        f.write('b,10\n')
        f.write('13,2\n')
        f.close()

    def tearDown(self):
        os.remove(self.test_int_file)
        os.remove(self.test_float_file)
        os.remove(self.test_str_file)
        os.remove(self.empty_file)
        os.remove(self.test_int_messy_file)

    def test_get_counts(self):
        r_int = sds_utils.get_counts(self.test_int_file)
        r_int_rows, r_int_cols = r_int.shape
        self.assertEqual(r_int_rows, 3)
        self.assertEqual(r_int_cols, 2)
        r_str = sds_utils.get_counts(self.test_str_file)
        r_str_rows, r_str_cols = r_str.shape
        self.assertEqual(r_str_rows, 3)
        self.assertEqual(r_str_cols, 2)
        r_float = sds_utils.get_counts(self.test_float_file)
        r_float_rows, r_float_cols = r_float.shape
        self.assertEqual(r_float_rows, 3)
        self.assertEqual(r_float_cols, 2)

    def test_get_counts_empty_file(self):
        self.assertRaises(SystemExit, sds_utils.get_counts, self.empty_file)

    def test_get_counts_dne_file(self):
        self.assertRaises(FileNotFoundError,
                          sds_utils.get_counts,
                          'file_dne.txt')

    def test_plot_hist(self):
        r_int = sds_utils.get_counts(self.test_int_file)
        sds_utils.plot_hist(r_int, 'test_int_hist.png')
        self.assertTrue(os.path.exists('test_int_hist.png'))

    def test_plot_hist_int_messy_file(self):
        # Because all essentially treated like strings, expect this
        # mix of integers & strings to still make plot output
        r_int_messy = sds_utils.get_counts(self.test_int_messy_file)
        sds_utils.plot_hist(r_int_messy, 'test_int_messy_hist.png')
        self.assertTrue(os.path.exists('test_int_messy_hist.png'))


if __name__ == '__main__':
    unittest.main()
