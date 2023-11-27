import unittest
import random
import sys
import pandas as pd
import os
sys.path.insert(0, '../../src/gg')
import prep_and_create_consort as pcc
import consort_prep_functions as pf


class test_try_convert_to_fl(unittest.TestCase):
    
    def test_string(self):
        random_integer = random.randint(1, 100)
        string_conv = pf.try_convert_to_fl(str(random_integer))
        self.assertIsInstance(string_conv, float)

    def test_unconvertiblestring(self):
        string_conv_2 = pf.try_convert_to_fl("String w No Numbers")
        self.assertIsNone(string_conv_2)
    
class test_reformat_query_summary(unittest.TestCase):
    
    @classmethod
    def setUp(self):
        data = {'Filter Value': ['=IRAN'], 'Search_Options':['Country']}
        original_df = pd.DataFrame(data)
        new_rows = []
        for _, row in original_df.iterrows():
            values = row['Filter Value'].split(',')
            for value in values:
                new_row = row.copy()
                new_row['Filter Value'] = value
                new_rows.append(new_row)
        self.query_format = pd.DataFrame(new_rows)
        self.query_format.to_csv('../data/one_query_unittest.csv', index=False)
        
        data2 = {'Filter Value': ["=IRAN, !=FRANCE"], 'Search_Options':['Country']}
        original_df2 = pd.DataFrame(data2)
        new_rows2 = []
        for _, row in original_df2.iterrows():
            values = row['Filter Value'].split(',')
            for value in values:
                new_row = row.copy()
                new_row['Filter Value'] = value
                new_rows2.append(new_row)
        self.query_format2 = pd.DataFrame(new_rows2)
        self.query_format2.to_csv('../data/two_query_unittest.csv', index=False)

        
        data_empty = ['Filter Value', 'Search_Options']
        df_empty = pd.DataFrame(columns=data_empty)
        self.empty_query = pd.DataFrame(df_empty)
        self.empty_query.to_csv('../data/empty_query.csv', index=False)

    def test_file_not_found(self):
        with self.assertRaises(SystemExit):
            pf.reformat_query_summary("doesnotexist.csv")
    
    def test_file_empty(self):
        self.assertEqual(len(pf.reformat_query_summary('../data/empty_query.csv')), 0)
        
    def test_file_1filter(self):
        self.assertEqual(len(pf.reformat_query_summary('../data/one_query_unittest.csv')), 1)

    def test_file_2filter(self):
        self.assertEqual(len(pf.reformat_query_summary('../data/two_query_unittest.csv')), 2)

    @classmethod
    def tearDown(self):
        os.remove('../data/one_query_unittest.csv')
        os.remove('../data/two_query_unittest.csv')
        os.remove('../data/empty_query.csv')

class test_subset_dataframe_by_names(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.colname_example = ['Country']
        self.colname_notexist = ['Strange']
        self.data_empty = pd.DataFrame(columns = ['Patient', 'Country'])
        self.data = pd.DataFrame({'Patient': [0, 1, 2, 3], 'Country': ['IRAN', 'IRAN', 'FRANCE', 'EGYPT']})

    def test_pandas_df_input(self):
        with self.assertRaises(ValueError):
            pf.subset_dataframe_by_names(
                "../data/LANL_HIV1_2023_seq_metadata.csv", self.colname_example)
            
    def test_no_df_input(self):
        with self.assertRaises(NameError):
            pf.subset_dataframe_by_names(
                doesntexist, self.colname_example)

    def test_pandas_df_size(self):
        with self.assertRaises(ValueError):
            pf.subset_dataframe_by_names(
                self.data_empty, self.colname_example)

    def test_pandas_df_size(self):
        with self.assertRaises(ValueError):
            pf.subset_dataframe_by_names(
                self.data_empty, self.colname_example)

    def test_colnames_list(self):
        with self.assertRaises(ValueError):
            pf.subset_dataframe_by_names(
                self.data, "Wrong")

    def test_colnames_notexist(self):
        with self.assertRaises(ValueError):
            pf.subset_dataframe_by_names(
                self.data, self.colname_notexist)

    def test_subset_works(self):
        subset_example = pf.subset_dataframe_by_names(
                self.data, self.colname_example)
        self.assertEqual(len(subset_example.columns), 2)
        self.assertEqual(len(subset_example), len(self.data))

class test_format_consort_input_file(unittest.TestCase):
    
    def test_file_not_found(self):
        with self.assertRaises(SystemExit):
            pf.reformat_query_summary("doesnotexist.csv")
    

# Not running bc of file path for r; maybe this shouldn't be a function?
# Could put in prep_and_create_consort
class test_run_consort_plot_rcode(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.colname_example = ['Country']
        self.colname_notexist = ['Strange']
        self.data_empty = pd.DataFrame(columns = ['Patient', 'Country'])
        self.data = pd.DataFrame({'Patient': [0, 1, 2, 3], 'Country': ['IRAN', 'IRAN', 'FRANCE', 'EGYPT']})

        data2 = {'Filter Value': ["=IRAN, !=FRANCE"], 'Search_Options':['Country']}
        original_df2 = pd.DataFrame(data2)
        new_rows2 = []
        for _, row in original_df2.iterrows():
            values = row['Filter Value'].split(',')
            for value in values:
                new_row = row.copy()
                new_row['Filter Value'] = value
                new_rows2.append(new_row)
        self.query_format2 = pd.DataFrame(new_rows2)

    def test_make_png(self):
        pf.run_consort_plot_rcode(self.data, self.query_format2, "../data/output.png")
        file_exists = os.path.exists("../data/output.png")
        self.assertEqual(file_exists, True)
        
    # @classmethod
    # def tearDown(self):
    #     os.remove("../data/output.png")