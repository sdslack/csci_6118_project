import unittest
import random
import sys
import pandas as pd
from pandas.testing import assert_frame_equal
sys.path.insert(0, '../../src/jb')
import query_utils as query_data


class TestQueryData(unittest.TestCase):

    def test_load_data(self):
        # invalid file
        with self.assertRaises(FileNotFoundError):
            query_data.load_data('data.csv')

        # empty file
        with self.assertRaises(pd.errors.EmptyDataError):
            query_data.load_data('../data/input/empty.csv')

        # normal file
        file_name = '../data/input/Fake_HIV.csv'
        self.assertIsInstance(query_data.load_data(file_name),
                              pd.DataFrame)

    def test_check_column_exists(self):
        df = pd.read_csv('../data/input/Fake_HIV.csv')

        # nonexistent column
        col_names = ['Sequences', 'Floats']
        with self.assertRaises(KeyError):
            query_data.check_column_exists(col_names, df)

        # existent column
        col_names = ['Sequence', 'Days from Infection']
        self.assertEqual(query_data.check_column_exists(col_names, df),
                         ['Sequence', 'Days from Infection'])

        # empty list of columns
        col_names = []
        self.assertEqual(query_data.check_column_exists(col_names, df),
                         [])

    def test_filter_data(self):
        df = pd.read_csv('../data/input/Fake_HIV.csv')

        # simple = categorical filter
        filters = {'Sequence': ['= a', '=b']}
        output_cols = ['Sequence']
        data = {'Sequence': ['a', 'b', 'a', 'b', 'a', 'b',
                             'a', 'b', 'a', 'b', 'a', 'b',
                             'a', 'b', 'a', 'b', 'a', 'b']}
        filtered_df = pd.DataFrame(data)
        operator = '||'
        actual_df = query_data.filter_data(df, filters, output_cols, operator)
        assert_frame_equal(filtered_df,
                           actual_df.reset_index(drop=True))

        # simple = filter
        filters = {'Float': ['=0.54', '=0.88']}
        output_cols = ['']
        data = {'Days from Infection': [30, 25],
                'Sequence': ['c', 'a'],
                'Float': [0.88, 0.54]}
        filtered_df = pd.DataFrame(data)
        operator = '||'
        actual_df = query_data.filter_data(df, filters, output_cols, operator)
        assert_frame_equal(filtered_df,
                           actual_df.reset_index(drop=True))

        # simple > and < numerical filter
        filters = {'Days from Infection': ['<= 21', '>=29']}
        output_cols = ['Days from Infection']
        data = {'Days from Infection': [29, 21, 21, 30, 30, 29, 20,
                                        20, 29, 30, 21, 30, 30, 20, 30]}
        filtered_df = pd.DataFrame(data)
        operator = '||'
        actual_df = query_data.filter_data(df, filters, output_cols, operator)
        assert_frame_equal(filtered_df,
                           actual_df.reset_index(drop=True))

        # simple - numerical filter
        filters = {'Float': ['0.28 - 0.41']}
        output_cols = ['Float']
        data = {'Float': [0.32, 0.28, 0.39, 0.40, 0.41, 0.28]}
        filtered_df = pd.DataFrame(data)
        operator = '||'
        actual_df = query_data.filter_data(df, filters, output_cols, operator)
        assert_frame_equal(filtered_df,
                           actual_df.reset_index(drop=True))

        # simple != filter 
        filters = {'Sequence': ['!=a', '!=b']}
        output_cols = ['Sequence']
        data = {'Sequence': ['c', 'c', 'c', 'c', 'c', 'c', 'c',
                             'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c']}
        filtered_df = pd.DataFrame(data)
        operator = '||'
        actual_df = query_data.filter_data(df, filters, output_cols, operator)
        assert_frame_equal(filtered_df,
                           actual_df.reset_index(drop=True))

        # complex filter
        filters = {'Sequence': ['=b'], 'Float': ['>=0.60'],
                   'Days from Infection': ['24-30']}
        output_cols = ['']
        logical_operator = '&&'
        data = {'Days from Infection': [27],
                'Sequence': ['b'],
                'Float': [0.61]}
        filtered_df = pd.DataFrame(data)
        operator = '&&'
        actual_df = query_data.filter_data(df, filters, output_cols, operator)
        assert_frame_equal(filtered_df,
                           actual_df.reset_index(drop=True))
        
        filters = {'Sequence': ['!=b'], 'Float': ['>=0.80'],
                   'Days from Infection': ['24-30']}
        output_cols = ['']
        logical_operator = '&&'
        data = {'Days from Infection': [29, 25, 30, 24, 30],
                'Sequence': ['c', 'c', 'c', 'c', 'a'],
                'Float': [0.99, 0.91, 0.88, 0.81, 0.86]}
        filtered_df = pd.DataFrame(data)
        operator = '&&'
        actual_df = query_data.filter_data(df, filters, output_cols, operator)
        assert_frame_equal(filtered_df,
                           actual_df.reset_index(drop=True))


        # no matching data to filter
        filters = {'Sequence': ['=q']}
        output_cols = ['']
        column_names = ['Days from Infection', 'Sequence', 'Float']
        column_types = {'Days from Infection': int,
                        'Sequence': object,
                        'Float': float}
        filtered_df = pd.concat([pd.Series(dtype=column_types[col],
                                           name=col) for col in column_names],
                                axis=1)
        operator = '||'
        self.assertEqual(filtered_df.empty,
                         query_data.filter_data(df,
                                                filters,
                                                output_cols,
                                                operator).empty)
        
    # complex filter with not equal to
    def test_filter_data_ne_as_firstfilter(self):
        data_long = {'Column_1': [1.2, 3.5, 4.1, 2.8],
                'Column_2': [2.5, 6.7, 8.9, 1.0],
                'Column_3': [9.2, 5.4, 4, 3.0]}
        data_proper_filter = {
                'Column_3': [5.4, 3.0]}
        df_long = pd.DataFrame(data_long)
        df_proper_filter = pd.DataFrame(data_proper_filter)
        filters = {'Column_3': ['!=4', '<9'], }
        output_cols = ['Column_3']
        operator = '||'
        df_long_filtered = query_data.filter_data(df_long, filters, output_cols, operator)
        df_long_filtered.reset_index(drop=True, inplace=True)
        self.assertEqual(len(df_proper_filter), len(df_long_filtered))
        
    def test_filter_data_multiple_ne(self):
        data_long = {'Column_1': [1.2, 3.5, 4.1, 2.8, 1],
                'Column_2': [2.5, 6.7, 8.9, 1.0, 4],
                'Column_3': [9.2, 5.4, 4, 3.0, 11]}
        data_proper_filter = {
                        'Column_1': [4.1, 1]}
        df_long = pd.DataFrame(data_long)
        df_proper_filter = pd.DataFrame(data_proper_filter)
        filters = {'Column_1': ['!=1.2', '!=3.5', '>=4.1', '=1']}
        output_cols = ['Column_1']
        operator = '||'
        df_long_filtered = query_data.filter_data(df_long, filters, output_cols, operator)
        self.assertEqual(len(df_proper_filter), len(df_long_filtered))

    def test_filter_data_only_ne(self):
        data_long = {'Column_1': [1.2, 3.5, 4.1, 2.8, 1],
                'Column_2': [2.5, 6.7, 8.9, 1.0, 4],
                'Column_3': [9.2, 5.4, 4, 3.0, 11]}
        data_proper_filter = {
                        'Column_1': [4.1, 2.8, 1]}
        df_long = pd.DataFrame(data_long)
        df_proper_filter = pd.DataFrame(data_proper_filter)
        filters = {'Column_1': ['!=1.2', '!=3.5']}
        output_cols = ['Column_1']
        operator = '||'
        df_long_filtered = query_data.filter_data(df_long, filters, output_cols, operator)
        self.assertEqual(len(df_proper_filter), len(df_long_filtered))

    def test_filter_data_only_equal(self):
        data_long = {'Column_1': [1.2, 3.5, 4.1, 2.8, 1],
                    'Column_2': [2.5, 6.7, 8.9, 1.0, 4],
                    'Column_3': [9.2, 5.4, 4, 3.0, 11]}
        data_proper_filter = {
                        'Column_1': [1.2, 3.5]}
        df_long = pd.DataFrame(data_long)
        df_proper_filter = pd.DataFrame(data_proper_filter)
        filters = {'Column_1': ['=1.2', '=3.5']}
        output_cols = ['Column_1']
        operator = '||'
        df_long_filtered = query_data.filter_data(df_long, filters, output_cols, operator)
        self.assertEqual(len(df_proper_filter), len(df_long_filtered))
    
    def test_split_arguments(self):
        # with &&
        filter = ' One: 1,1,1; Two: 2,2 '
        self.assertEqual(query_data.split_arguments(filter),
                         ['One: 1,1,1', 'Two: 2,2'])

        # with extra delimiter
        filter = 'One: 1,1,1 ;Two: 2,2 ;'
        self.assertEqual(query_data.split_arguments(filter),
                         ['One: 1,1,1', 'Two: 2,2'])

        # without &&
        filter = 'One: 1,1'
        self.assertEqual(query_data.split_arguments(filter),
                         ['One: 1,1'])

        # empty string input
        filter = ''
        self.assertEqual(query_data.split_arguments(filter), [])

    def test_get_filters(self):
        # simple
        filter_args = ['Seq : a,b']
        self.assertEqual(query_data.get_filters(filter_args),
                         {'Seq': ['a', 'b']})

        # complex
        filter_args = ['Seq: a,b, <10,  !=9,        1-5']
        self.assertEqual(query_data.get_filters(filter_args),
                         {'Seq': ['a', 'b', '<10', '!=9', '1-5']})
        filter_args = ['Seq: a,b, <10, !=9, 1-5 ; Floats : =10.0,']
        cleaned_filter_args = query_data.split_arguments(filter_args[0])
        self.assertEqual(query_data.get_filters(cleaned_filter_args),
                         {'Seq': ['a', 'b', '<10', '!=9', '1-5'],
                          'Floats': ['=10.0']})

        # empty filter input
        filter_args = []
        self.assertEqual(query_data.get_filters(filter_args), {})

    def test_make_query_request_summary(self):
        df = pd.read_csv('../data/input/Fake_HIV.csv')

        # simple
        filters = {'Sequence': ['=a']}
        df_cols = df.columns
        data = {'Search_Options': ['Days from Infection', 'Sequence', 'Float'],
                'Filter Criteria': [float("NaN"), '=a', float("NaN")],
                'Do you plan to search by this column?': [float("NaN"), 'yes', float("NaN")]}
        query_request = pd.DataFrame(data)
        actual_df = query_data.make_query_request_summary(filters, df_cols)
        assert_frame_equal(actual_df, query_request)

        # complex
        filters = {'Days from Infection': ['<=22', '!=29'],
                   'Sequence': ['=a', '=b']}
        data = {'Search_Options': ['Days from Infection', 'Sequence', 'Float'],
                'Filter Criteria': ['<=22;!=29', '=a;=b', float("NaN")],
                'Do you plan to search by this column?': ['yes', 'yes', float("NaN")]}
        query_request = pd.DataFrame(data)
        actual_df = query_data.make_query_request_summary(filters, df_cols)
        assert_frame_equal(actual_df, query_request)

    def test_extract_symbol_and_value(self):
        user_input = '= 5'
        expected_symbol = '='
        expected_value = '5'
        actual_symbol, actual_value = query_data.extract_symbol_and_value(user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)
        
        user_input = '!=    5'
        expected_symbol = '!='
        expected_value = '5'
        actual_symbol, actual_value = query_data.extract_symbol_and_value(user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)
        
        user_input = '>=    5'
        expected_symbol = '>='
        expected_value = '5'
        actual_symbol, actual_value = query_data.extract_symbol_and_value(user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)
        
        user_input = '<=  5'
        expected_symbol = '<='
        expected_value = '5'
        actual_symbol, actual_value = query_data.extract_symbol_and_value(user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)
        
        user_input = '10 -   20'
        expected_symbol = '-'
        expected_value = '10-20'
        actual_symbol, actual_value = query_data.extract_symbol_and_value(user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)
        
    def test_check_for_logical_operator(self):
        # return default 
        filters = {'Sequence': ['=q']}
        operator = ''
        actual_operator = query_data.check_for_logical_operator(filters, operator)
        expected_operator = '||'
        self.assertEqual(actual_operator, expected_operator)
        
        # no operator entered
        filters = {'Sequence': ['=q'], 'Column_1': ['>10']}
        operator = ''
        actual_operator = query_data.check_for_logical_operator(filters, operator)
        expected_operator = '||'
        self.assertEqual(actual_operator, expected_operator)
        
        # regular operator entered
        filters = {'Sequence': ['=q'], 'Column_1': ['>10']}
        operator = '&&'
        actual_operator = query_data.check_for_logical_operator(filters, operator)
        expected_operator = '&&'
        self.assertEqual(actual_operator, expected_operator)
        
        # invalid operator 
        filters = {'Sequence': ['=q'], 'Column_1': ['>10']}
        operator = '&'
        with self.assertRaises(SystemExit):
            query_data.check_for_logical_operator(filters, operator)
        
        