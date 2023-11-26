import unittest
import random
import sys
import pandas as pd
sys.path.insert(0, '../../src/gg')
import prep_and_create_consort as pcc
import consort_prep_functions as pf


class Test_prep_and_create(unittest.TestCase):

    @classmethod
    def setUp(self):
        # Example DataFrame with a column containing comma-separated values
        data = {'Filter Value': ['=IRAN'], 'Search_Options':['Country']}
        original_df = pd.DataFrame(data)

        new_rows = []
        for _, row in original_df.iterrows():
            values = row['Filter Value'].split(',')
            for value in values:
                new_row = row.copy()
                new_row['Filter Value'] = value
                new_rows.append(new_row)

        # Creating a new DataFrame from the list of rows
        query_format = pd.DataFrame(new_rows)

        query_format.to_csv("../data/query_requests2.csv", index=False)

