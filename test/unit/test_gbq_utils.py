from contextlib import AbstractContextManager
from typing import Any
import unittest
import sys
import random
import os
sys.path.insert(0, '../../src/sds')  # noqa
import gbq_utils


class TestSdsUtils(unittest.TestCase):

    def test_get_gbq_data_query1(self):
        query = "Days from Infection:=88,=89,=90,=91; Risk Factor:=IV Drug User"
        data = get_gbq_data(query, 'SE id(SA)')
        # Check dimensions?
    

    def test_get_gbq_data_query2(self):
        query = "Days from Infection:=88,=89,=90,=91; Risk Factor:=Male Sex with Male, =Sex worker, =Heterosexual"
        data = get_gbq_data(query, 'SE id(SA)')

    def test_get_gqb_data_bad_query(self):
        query = "DAYS FROM INFECTION:=88,=89,=90,=91"
        data = get_gbq_data(query, 'SE id(SA)')

    def test_get_gqb_data_no_results(self):
        query = "Days from Infection:=-1"
        data = get_gbq_data(query, 'SE id(SA)')
        # Empty result?


if __name__ == '__main__':
    unittest.main()
