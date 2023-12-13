import unittest
import random
import sys
import pandas as pd
from pandas.testing import assert_frame_equal
sys.path.insert(0, '../../src/jb')  # noqa
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
        df_long_filtered = query_data.filter_data(
            df_long, filters, output_cols, operator)
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
        df_long_filtered = query_data.filter_data(
            df_long, filters, output_cols, operator)
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
        df_long_filtered = query_data.filter_data(
            df_long, filters, output_cols, operator)
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
        df_long_filtered = query_data.filter_data(
            df_long, filters, output_cols, operator)
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
                'Search by this column?': [float("NaN"), 'Yes', float("NaN")]}
        query_request = pd.DataFrame(data)
        actual_df = query_data.make_query_request_summary(filters, df_cols)
        assert_frame_equal(actual_df, query_request)

        # complex
        filters = {'Days from Infection': ['<=22', '!=29'],
                   'Sequence': ['=a', '=b']}
        data = {'Search_Options': ['Days from Infection', 'Sequence', 'Float'],
                'Filter Criteria': ['<=22;!=29', '=a;=b', float("NaN")],
                'Search by this column?': ['Yes', 'Yes', float("NaN")]}
        query_request = pd.DataFrame(data)
        actual_df = query_data.make_query_request_summary(filters, df_cols)
        assert_frame_equal(actual_df, query_request)

    def test_create_numeric_mask(self):
        data_long = pd.DataFrame({
            'Column_1': [
                'Drug', 'Heterosexual', 'unspecified',
                'Mom to Child', 'Sex Worker', 'None'
            ],
            'Column_2': [1, 90, 45, 123, 250],
            'Column_3': [9.2, 5.4, 4, 3.0, 11]
        })

        # Integers
        actual_mask = query_data.create_numeric_mask(
            data_long['Column_2'], ">", 100)
        expected_mask = [False, False, False, True, True]
        self.assertTrue(all(actual_mask == expected_mask))

        # Floats
        actual_mask2 = query_data.create_numeric_mask(
            data_long['Column_3'], "-", "3.0-6.0")
        expected_mask2 = [False, True, True, True, False]
        self.assertTrue(all(actual_mask2 == expected_mask2))

        # Symbol that doesn't make sense
        with self.assertRaises(ValueError):
            query_data.create_numeric_mask(data_long['Column_2'], "!", 100)

    def test_extract_symbol_and_value(self):
        user_input = "= 5"
        expected_symbol = "="
        expected_value = '5'
        actual_symbol, actual_value = query_data.extract_symbol_and_value(
            user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)

        user_input = '!=    5'
        expected_symbol = '!='
        expected_value = '5'
        actual_symbol, actual_value = query_data.extract_symbol_and_value(
            user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)

        user_input = '>=    5'
        expected_symbol = '>='
        expected_value = '5'
        actual_symbol, actual_value = query_data.extract_symbol_and_value(
            user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)

        user_input = '<=  5'
        expected_symbol = '<='
        expected_value = '5'
        actual_symbol, actual_value = (
            query_data.extract_symbol_and_value)(user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)

        user_input = '10 -   20'
        expected_symbol = '-'
        expected_value = '10-20'
        actual_symbol, actual_value = (
            query_data.extract_symbol_and_value)(user_input)
        self.assertEqual(actual_symbol, expected_symbol)
        self.assertEqual(actual_value, expected_value)

    def test_check_for_logical_operator(self):
        # return default
        filters = {'Sequence': ['=q']}
        operator = ''
        actual_operator = query_data.check_for_logical_operator(filters,
                                                                operator)
        expected_operator = '||'
        self.assertEqual(actual_operator, expected_operator)

        # no operator entered
        filters = {'Sequence': ['=q'], 'Column_1': ['>10']}
        operator = ''
        actual_operator = query_data.check_for_logical_operator(filters,
                                                                operator)
        expected_operator = '||'
        self.assertEqual(actual_operator, expected_operator)

        # regular operator entered
        filters = {'Sequence': ['=q'], 'Column_1': ['>10']}
        operator = '&&'
        actual_operator = query_data.check_for_logical_operator(filters,
                                                                operator)
        expected_operator = '&&'
        self.assertEqual(actual_operator, expected_operator)

        # invalid operator
        filters = {'Sequence': ['=q'], 'Column_1': ['>10']}
        operator = '&'
        with self.assertRaises(SystemExit):
            query_data.check_for_logical_operator(filters, operator)


class test_boolean_filter_functions_in_Query_Utils(unittest.TestCase):

    @classmethod
    def setUp(self):
        data_long = {'Column_1': ["Red", "Blue", "Blue", "Green", "Purple"],
                     'Column_2': [2, 6, 9, 1, 4],
                     'Column_3': [9.2, 5.4, 4, 3.0, 11]}

        # With floats
        self.df_long_df = pd.DataFrame(data_long)
        filters_floats = {'Column_3': ['<=9', '!=4', '>=10']}
        existing_cols_floats = ['Column_3']
        (
            self.df_long_filtered_equals_mask,
            self.df_long_filtered_not_equals_mask
        ) = query_data.create_by_filter_boolean_filter_summary(
            filters_floats,
            self.df_long_df,
            existing_cols_floats
        )
        expected_filter2 = [True, True, False, True, True]
        self.expected_series2 = pd.Series(expected_filter2)
        self.df_long_filtered_not_equals_mask_df = pd.DataFrame(
            self.df_long_filtered_not_equals_mask
        )
        self.df_long_filtered_equals_mask_df = pd.DataFrame(
            self.df_long_filtered_equals_mask
        )
        self.actual_filter2 = (
            self.df_long_filtered_not_equals_mask_df.loc[0, 'Column_3']
        )

        # With integers
        filters_int = {'Column_2': ['!=6', '!=4']}
        existing_cols_int = ['Column_2']
        expected_filter_int1 = [True, False, True, True, True]
        expected_filter_int2 = [True, True, True, True, False]
        self.expected_series_int1 = pd.Series(expected_filter_int1)
        self.expected_series_int2 = pd.Series(expected_filter_int2)
        (
            self.df_long_filtered_equals_mask_int,
            self.df_long_filtered_not_equals_mask_int
        ) = (
            query_data.create_by_filter_boolean_filter_summary
        )(
            filters_int,
            self.df_long_df,
            existing_cols_int
        )
        self.df_long_filtered_not_equals_mask_int_df = pd.DataFrame(
            self.df_long_filtered_not_equals_mask_int
        )
        self.actual_filter_int1 = (
            self.df_long_filtered_not_equals_mask_int_df.loc
        )[0, 'Column_2']
        self.actual_filter_int2 = (
            self.df_long_filtered_not_equals_mask_int_df.loc
        )[1, 'Column_2']

        # With strings
        self.filters_str = {'Column_1': ['=Blue']}
        existing_cols_str = ['Column_1']
        (
            self.df_long_filtered_str,
            self.df_long_filtered_not_equals_mask_str
        ) = (
            query_data.create_by_filter_boolean_filter_summary
        )(
            self.filters_str,
            self.df_long_df,
            existing_cols_str
        )
        expected_filter = [False, True, True, False, False]
        self.expected_series = pd.Series(expected_filter)
        df_long_filtered_str_df = pd.DataFrame(self.df_long_filtered_str)
        self.actual_filter = df_long_filtered_str_df.loc[0, 'Column_1']

        # With empty
        self.empty_equals_mask, self.empty_not_equals_mask = (
            query_data.create_by_filter_boolean_filter_summary
        )(
            self.filters_str,
            self.df_long_df,
            "Column 5")

    def test_create_by_filter_boolean_filter_summary(self):

        # With floats
        self.assertTrue(all(self.actual_filter2 == self.expected_series2))

        # Checking that getting separate equals and not equals masks
        self.assertEqual(len(self.df_long_filtered_equals_mask_df), 2)
        self.assertEqual(len(self.df_long_filtered_not_equals_mask_df), 1)

        # With integers
        self.assertTrue(all
                        (self.actual_filter_int1 == self.expected_series_int1))
        self.assertTrue(all
                        (self.actual_filter_int2 == self.expected_series_int2))

        # With strings
        self.assertTrue(all(self.actual_filter == self.expected_series))

        # With empty
        self.assertDictEqual(self.empty_equals_mask, {})

    def test_create_by_column_boolean_filter_summary(self):

        # With multiple not equals and equals masks needing to be combined
        # And use of floats
        expected_column_filter = [False, True, False, True, True]
        expected_column_series = pd.Series(expected_column_filter)
        actual_column_series = (
            query_data.create_by_column_boolean_filter_summary
        )(
            self.df_long_filtered_equals_mask,
            self.df_long_filtered_not_equals_mask,
            'Column_3')
        self.assertTrue(all(actual_column_series == expected_column_series))

        # Check if get empty subset if incorrect key is provided
        actual_wrong_key_series = (
            query_data.create_by_column_boolean_filter_summary
        )(
            self.df_long_filtered_equals_mask,
            self.df_long_filtered_not_equals_mask,
            'Column_14')
        self.assertEqual(len(actual_wrong_key_series), 0)

        # With multiple not equals masks needing to be combined
        # And use of integers
        expected_column_filter_int = [True, False, True, True, False]
        expected_column_series_int = pd.Series(expected_column_filter_int)
        actual_column_series_int = (
            query_data.create_by_column_boolean_filter_summary
        )(
            self.df_long_filtered_equals_mask_int,
            self.df_long_filtered_not_equals_mask_int,
            'Column_2')
        self.assertTrue(all(
            actual_column_series_int == expected_column_series_int
        ))

        # With just one equals mask needing to be combined and use of strings
        actual_column_series_str = (
            query_data.create_by_column_boolean_filter_summary(
                self.df_long_filtered_str,
                self.df_long_filtered_not_equals_mask_str,
                'Column_1'
            )
        )
        self.assertTrue(all(actual_column_series_str == self.expected_series))

        # With no masks provided
        actual_column_series_empty = (
            query_data.create_by_column_boolean_filter_summary
        )(
            self.empty_equals_mask,
            self.empty_not_equals_mask,
            'Column_1')
        self.assertEqual(len(actual_column_series_empty), 0)

        # Dictionaries not provided
        with self.assertRaises(ValueError):
            query_data.create_by_column_boolean_filter_summary(
                "Random",
                self.empty_not_equals_mask,
                'Column_1'
            )


if __name__ == '__main__':
    unittest.main()
