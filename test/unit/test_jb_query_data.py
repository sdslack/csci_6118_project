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
        # simple filter
        df = pd.read_csv('../data/input/Fake_HIV.csv')
        filters = 
        # complex filter 
        
        # error filtering column 
        
        # no matching data to filter 

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
        