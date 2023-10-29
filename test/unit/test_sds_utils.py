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
        self.test_file = 'test_file.csv'
        f = open(self.test_file, 'w')
        f.write('Se ID,Sequence Length,Georegion,Subtype,\n')
        f.write('1,2846,Europe,B\n')
        f.write('2,1004,Middle-East,35_A1D\n')
        f.write('3,1004,North America,B\n')
        f.close()
        self.empty_file = "empty_file.csv"
        f = open(self.empty_file, 'w')
        f.close()

    def tearDown(self):
        os.remove(self.test_file)
        os.remove(self.empty_file)

    def test_get_col_all(self):
        r = sds_utils.get_col_all(self.test_file, 2)
        self.assertEqual(r, ['Georegion', 'Europe', 'Middle-East', 'North America'])

    def test_get_col_all_index_error(self):
        self.assertRaises(SystemExit, sds_utils.get_col_all, self.test_file, 10)

    def test_get_col_all_non_int(self):
        self.assertRaises(TypeError, sds_utils.get_col_all, self.test_file, 'a')
    
    def test_get_col_all_empty_file(self):
        r = sds_utils.get_col_all(self.empty_file, 2)
        self.assertEqual(r, [])

    def test_plot_hist(self):
        r = sds_utils.get_col_all(self.test_file, 2)
        sds_utils.plot_hist(r, './')
        self.assertTrue(os.path.exists('./Georegion_hist.png'))

    def test_plot_hist_empty_file(self):
        self.assertRaises(IndexError, sds_utils.plot_hist, [], './')
            # TODO: may want to later handle this error differently