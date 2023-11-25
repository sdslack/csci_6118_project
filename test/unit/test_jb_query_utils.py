import unittest
import random
import sys
import pandas as pd
sys.path.insert(0, '../../src/jb')
import query_data

class TestQueryData(unittest.TestCase):
    
    def test_load_data(self):
        #invalid file 
        with self.assertRaises(FileNotFoundError):
            query_data.load_data('data.csv')

        #empty file 
        self.assertEqual(query_data.load_data('../data/input/empty.csv'), None)
        
        #normal file
        self.assertNotEqual(query_data.load_data('../data/input/Fake_HIV.csv'), None)
    
    def test_check_column_exists(self):
        df = pd.read_csv('../data/input/Fake_HIV.csv')
        
        # nonexistent column
        col_names = ['Sequences', 'Floats']
        with self.assertRaises(KeyError):
            query_data.check_column_exists(col_names)
        self.assertEqual(query_data.check_column_exists(col_names, df), [])
        
        # existent column
        col_names = ['Sequence', 'Days from Infection']
        self.assertEqual(query_data.check_column_exists(col_names, df), ['Sequence','Days from Infection'])
        
        # empty list of columns
        col_names = []
        self.assertEqual(query_data.check_column_exists(col_names, df), [])
        
    def test_filter_data(self):
        df = pd.read_csv('../data/input/Fake_HIV.csv')
        
        # simple categorical filter
        filters = {'Sequence':['a','b']}
        output_cols = ['Sequence']
        data = {'Sequence': ['a','b','a','b','a','b', 
                             'a', 'b','a','b','a','b', 
                             'a','b','a','b','a','b']}
        filtered_df = pd.DataFrame(data)
        self.assertEqual(query_data.filter_data(df, filters, output_cols), filtered_df)
        
        # simple = filter
        filters = {'Float':['=0.54','=0.88']}
        output_cols = []
        data = {'Days from Infection': [30, 25],
                'Sequence': ['c','a'],
                'Float': [0.88, 0.54]}
        filtered_df = pd.DataFrame(data)
        self.assertEqual(query_data.filter_data(df, filters, output_cols), filtered_df)

        # simple > and < numerical filter
        filters = {'Days from Infection':['<21','>29']}
        output_cols = ['Days from Infection']
        data = {'Days from Infection': [29, 21, 21, 30, 30, 29, 20, 
                                        20, 29, 30, 21, 30, 30, 20,30]}
        filtered_df = pd.DataFrame(data)
        self.assertEqual(query_data.filter_data(df, filters, output_cols), filtered_df)
        
        # simple - numerical filter
        filters = {'Float': ['0.28-0.41']}
        output_cols = ['Float']
        data = {'Float': [0.28, 0.39, 0.40, 0.41, 0.28]}
        filtered_df = pd.DataFrame(data)
        self.assertEqual(query_data.filter_data(df, filters, output_cols), filtered_df)

        # simple != filter
        filters = {'Sequence': ['!= a', '!= b']}
        output_cols = ['Sequence']
        data = {'Sequence': ['c','c','c','c','c','c','c',
                             'c','c','c','c','c','c','c','c','c']}
        filtered_df = pd.DataFrame(data)
        self.assertEqual(query_data.filter_data(df, filters, output_cols), filtered_df)

        # complex filter
        filters = {'Sequence': ['= b'], 'Float': ['>0.60'], 'Days from Infection': ['24-30']}
        output_cols = []
        data = {'Days from Infection': [27], 
               'Sequence': ['b'],
               'Float': [0.61]}
        filtered_df = pd.DataFrame(data)
        self.assertEqual(query_data.filter_data(df, filters, output_cols), filtered_df)

        # no matching data to filter
        filters = {'Sequence': ['= q']}
        output_cols = []
        data = {}
        filtered_df = pd.DataFrame(data)
        self.assertEqual(query_data.filter_data(df, filters, output_cols), filtered_df)

    def test_split_arguments(self):
        # with &&
        filter = ' One: 1,1,1 && Two: 2,2 '
        self.assertEqual(query_data.split_arguments(filter), ['One: 1,1,1 ', ' Two: 2,2'])
        
        # with extra delimiter
        filter = 'One: 1,1,1 && Two: 2,2 &&'
        self.assertEqual(query_data.split_arguments(filter), ['One: 1,1,1 ', ' Two: 2,2 '])
        
        # without &&
        filter = 'One: 1,1'
        self.assertEqual(query_data.split_arguments(filter), ['One: 1,1'])
        
        # empty string input 
        filter = ''
        self.assertEqual(query_data.split_arguments(filter), [])
        
    def test_get_filters(self):
        # simple 
        filter_args = ['Seq : a,b']
        self.assertEqual(query_data.get_filters(filter_args), {'Seq':['a','b']})
        
        # complex
        filter_args = ['Seq: a,b, <10,  !=9,        1-5']
        self.assertEqual(query_data.get_filters(filter_args), {'Seq':['a','b','<10','!=9', '1-5']})
        filter_args = ['Seq: a,b, <10, !=9, 1-5 && Floats : =10.0,']
        cleaned_filter_args = query_data.split_arguments(filter_args)
        self.assertEqual(query_data.get_filters(cleaned_filter_args), {'Seq':['a','b','<10','!=9', '1-5'], 'Floats': ['=10.0']})
        
        # empty filter input
        filter_args = []
        self.assertEqual(query_data.get_filters(filter_args), {})

    def make_query_request_summary(self):
        