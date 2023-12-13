from contextlib import AbstractContextManager
from typing import Any
import unittest
import sys
sys.path.insert(0, '../../src/sds')  # noqa
import gbq_utils


class TestSdsUtils(unittest.TestCase):

    def test_get_gbq_data_query1(self):
        # To note: this test based on current version of data, would break
        # if version of data on BigQuery was updated
        query = "Days from Infection:=88,=89,=90,=91"
        data = gbq_utils.get_gbq_data(query, 'SE id(SA)')
        data_rows, data_cols = data.shape
        # Expect all rows in data, since no filtering applied yet
        self.assertEqual(data_rows, 1149460)
        # Number of columns should be:
        # total unique in query + get_gbq_data_params
        self.assertEqual(data_cols, 2)

    def test_get_gbq_data_query2(self):
        query = (
            "Days from Infection:=88,=89,=90,=91; "
            "Risk Factor:=Male Sex with Male, =Sex worker, =Heterosexual"
        )
        data = gbq_utils.get_gbq_data(query, 'SE id(SA)')
        data_rows, data_cols = data.shape
        self.assertEqual(data_rows, 1149460)
        self.assertEqual(data_cols, 3)

    def test_get_gqb_data_all_caps(self):
        # Testing pandas_gbq handling of case sensitivity, should
        # still return result
        query = "DAYS FROM INFECTION:=88,=89,=90,=91"
        data = gbq_utils.get_gbq_data(query, 'SE id(SA)')
        data_rows, data_cols = data.shape
        self.assertEqual(data_rows, 1149460)
        self.assertEqual(data_cols, 2)

    def test_get_gqb_data_dne(self):
        # Expect error since querying columns that do not exist
        query = (
            "Days from Infection:=-1; DNE_col1:=80; "
            "DNE_col2:=red; DNE_col3:<100"
        )
        self.assertRaises(
            SystemExit, gbq_utils.get_gbq_data, query, 'SE id(SA)')


if __name__ == '__main__':
    unittest.main()
