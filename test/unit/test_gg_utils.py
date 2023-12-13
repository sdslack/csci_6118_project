import unittest
import random
import sys
import pandas as pd
import os
sys.path.insert(0, '../../src/gg')  # noqa
import consort_prep_functions as pf


class test_try_convert_to_fl(unittest.TestCase):

    def test_string(self):
        random_integer = random.randint(1, 100)
        string_conv = pf.try_convert_to_fl(str(random_integer))
        self.assertIsInstance(string_conv, float)

    def test_unconvertiblestring(self):
        string_conv_2 = pf.try_convert_to_fl("String w No Numbers")
        self.assertIsNone(string_conv_2)


class test_query_file_to_filter(unittest.TestCase):

    @classmethod
    def setUp(self):
        data = {'Filter Criteria': ['=IRAN'],
                'Search_Options': ['Country'],
                'Search by this column?': ['Yes']}
        self.query_format = pd.DataFrame(data)
        self.query_format.to_csv(
            '../data/one_query_unittest.csv', index=False)

        data2 = {'Filter Criteria': ["=IRAN; !=FRANCE"],
                 'Search_Options': ['Country'],
                 'Search by this column?': ['Yes']}
        self.query_format2 = pd.DataFrame(data2)
        self.query_format2.to_csv(
            '../data/two_query_unittest.csv', index=False)

        data_wrongcol = {'Filter Criteria': ["=IRAN; !=FRANCE"],
                         'Wrong_Name': ['Country'],
                         'Search by this column?': ['Yes']}
        self.query_format_wrongcol = pd.DataFrame(data_wrongcol)
        self.query_format_wrongcol.to_csv(
            '../data/wrongcol_query_unittest.csv', index=False)

        data3 = {'Filter Criteria': ["=IRAN; !=FRANCE", "=0"],
                 'Search_Options': ['Country',
                                    'Days of Infection'],
                 'Search by this column?': ['Yes', 'Yes']}
        self.query_format3 = pd.DataFrame(data3)
        self.query_format3.to_csv(
            '../data/three_query_unittest.csv', index=False)

        data_empty = ['Filter Criteria', 'Search_Options',
                      'Search by this column?']
        df_empty = pd.DataFrame(columns=data_empty)
        self.empty_query = pd.DataFrame(df_empty)
        self.empty_query.to_csv(
            '../data/empty_query.csv', index=False)

    def test_file_not_found(self):
        with self.assertRaises(SystemExit):
            pf.query_file_to_filter("doesnotexist.csv")

    def test_wrong_colnames(self):
        with self.assertRaises(ValueError):
            pf.query_file_to_filter(
                '../data/wrongcol_query_unittest.csv')

    def test_file_empty(self):
        self.assertEqual(len(pf.query_file_to_filter(
            '../data/empty_query.csv')), 0)

    def test_file_1filter(self):
        self.assertEqual(len(pf.query_file_to_filter(
            '../data/one_query_unittest.csv')), 1)

    def test_file_2filter(self):
        self.assertEqual(len(pf.query_file_to_filter(
            '../data/two_query_unittest.csv')), 1)

    def test_file_3filter(self):
        self.assertEqual(len(pf.query_file_to_filter(
            '../data/three_query_unittest.csv')), 2)

    @classmethod
    def tearDown(self):
        os.remove('../data/one_query_unittest.csv')
        os.remove('../data/two_query_unittest.csv')
        os.remove('../data/three_query_unittest.csv')
        os.remove('../data/empty_query.csv')


class test_subset_dataframe_by_names(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.colname_example = ['Country']
        self.colname_notexist = ['Strange']
        self.data_empty = pd.DataFrame(columns=['Patient',
                                                'Country'])
        self.data = pd.DataFrame({'Patient': [0, 1, 2, 3],
                                  'Country': ['IRAN', 'IRAN',
                                              'FRANCE', 'EGYPT']})

    def test_pandas_df_input(self):
        with self.assertRaises(ValueError):
            pf.subset_dataframe_by_names(
                "../data/LANL_HIV1_2023_seq_metadata.csv",
                self.colname_example)

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
        self.assertEqual(len(subset_example.columns), 1)
        self.assertEqual(len(subset_example), len(self.data))


class test_consort_filter_data(unittest.TestCase):

    @classmethod
    def setUp(self):
        # For test with floats
        data_long = {'Column_1': [1.2, 3.5, 4.1, 2.8, 1],
                     'Column_2': [2.5, 6.7, 8.9, 1.0, 4],
                     'Column_3': [9.2, 5.4, 4, 3.0, 11]}
        data_proper_filter = {'Column_1': [1.2, 3.5, 4.1, 2.8, 1],
                              'Column_3': [9.2, 5.4, 4, 3.0, 11],
                              'Filtered_Column_Column_1':
                              [False, True, True, False, False],
                              'Filtered_Column_Column_3':
                              [False, True, True, False, False]}
        self.df_long = pd.DataFrame(data_long)
        self.df_proper_filter = pd.DataFrame(data_proper_filter)
        self.filters = {'Column_1': ['>3'],
                        'Column_3': ['!=4', '<=9', '>=10']}
        self.wrongcol_filters = {'Column_14': ['!=4', '<=9', '>=10']}
        self.data_long_filtered = pf.consort_filter_data(self.df_long,
                                                         self.filters)
        # For test with strings and integers
        data_strint = {'Column_1': [1, 2, 4, 2, 1],
                       'Column_2': ["Red", "Blue",
                                    "Blue", "Green", "Purple"]}
        data_strint_proper_filter = {'Column_1': [1, 2, 4, 2, 1],
                                     'Column_2': ["Red", "Blue",
                                                  "Blue", "Green", "Purple"],
                                     'Filtered_Column_Column_1':
                                     [False, False, True, False, False],
                                     'Filtered_Column_Column_2':
                                     [True, True, True, False, True]}
        self.df_long_strint = pd.DataFrame(data_strint)
        self.df_strint_proper_filter = pd.DataFrame(data_strint_proper_filter)
        self.filters_strint = {'Column_1': ['>3'], 'Column_2': ['!=Green']}
        self.data_long_filtered_strint = pf.consort_filter_data(
            self.df_long_strint, self.filters_strint)
        # Create a file
        pf.consort_filter_data(self.df_long,
                               self.filters,
                               "../data/test_consort_filter_bool_csv.csv")

    def test_pddf_not_found(self):
        with self.assertRaises(NameError):
            pf.consort_filter_data(doesnt_exist_df)

    def test_col_not_found(self):
        with self.assertRaises(KeyError):
            pf.consort_filter_data(self.df_long,
                                   self.wrongcol_filters)

    def test_consort_filtered_floats(self):
        self.assertEquals(len(self.data_long_filtered),
                          len(self.df_proper_filter))
        self.assertTrue(all(self.data_long_filtered.columns
                            == self.df_proper_filter.columns))
        self.assertTrue(
            all(self.data_long_filtered['Filtered_Column_Column_1']
                == self.df_proper_filter['Filtered_Column_Column_1']))

    def test_consort_filtered_string_int(self):
        self.assertEqual(len(self.data_long_filtered_strint),
                         len(self.df_strint_proper_filter))
        self.assertTrue(all(self.data_long_filtered_strint.columns
                            == self.df_strint_proper_filter.columns))
        self.assertTrue(
            all(self.data_long_filtered_strint['Filtered_Column_Column_1']
                == self.df_strint_proper_filter['Filtered_Column_Column_1']))

    def test_consort_filtered_or(self):
        self.assertEqual(len(self.data_long_filtered_strint),
                         len(self.df_strint_proper_filter))
        self.assertTrue(all(self.data_long_filtered_strint.columns
                            == self.df_strint_proper_filter.columns))
        self.assertTrue(
            all(self.data_long_filtered_strint['Filtered_Column_Column_1']
                == self.df_strint_proper_filter['Filtered_Column_Column_1']))

    def test_write_boolean_csv(self):
        self.assertTrue(os.path.exists(
            "../data/test_consort_filter_bool_csv.csv"))

    def test_wrong_write_boolean_csv(self):
        with self.assertRaises(KeyError):
            pf.consort_filter_data(self.df_long,
                                   self.filters, "wrongoutput")

    def test_wrong_write_boolean_csv(self):
        with self.assertRaises(SystemExit):
            pf.consort_filter_data(self.df_long,
                                   self.filters,
                                   "../data/wrongoutput/no\
                                   path/outbool_csv.csv")

    @classmethod
    def tearDown(self):
        os.remove("../data/test_consort_filter_bool_csv.csv")


class test_make_query_df_formatted(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.filters = "Subtype:=35_A1D; Sequence Length:=915"
        self.emptyfilters = ""
        self.consort_input_data = pd.read_csv(
            '../data/LANL_HIV1_2023_seq_metadata.csv')
        self.empty_consort_input_data = pd.DataFrame()

    def test_nofilter_nosummary(self):
        with self.assertRaises(ValueError):
            pf.make_query_df_formatted(self.consort_input_data)

    def test_nofilter_nosummary(self):
        with self.assertRaises(ValueError):
            pf.make_query_df_formatted(
                filters=self.filters,
                query_summary_file="../data/example_request_summary.csv",
                consort_input_data=self.consort_input_data)

    def test_nofilter_wrongsummary(self):
        with self.assertRaises(SystemExit):
            pf.make_query_df_formatted(
                query_summary_file="../data/doesntexist_request_summary.csv")

    def test_not_pd_consort_input(self):
        with self.assertRaises(ValueError):
            pf.make_query_df_formatted(
                filters=self.filters,
                consort_input_data='../data/LANL_HIV1_2023_seq_metadata.csv')

    def test_empty_input(self):
        query_df_formatted, filters_provided \
            = pf.make_query_df_formatted(
            filters=self.filters,
            consort_input_data=self.empty_consort_input_data)
        self.assertEqual(len(query_df_formatted), 0)
        query_df_formatted_e2, \
            filters_provided_e2 = pf.make_query_df_formatted(
            filters=self.emptyfilters,
            consort_input_data=self.consort_input_data)
        self.assertEqual(len(query_df_formatted_e2), 0)
        (query_df_formatted_e3, filters_provided_e3) = pf.make_query_df_formatted(
            query_summary_file="../data/query_requests_empty.csv")
        self.assertEqual(len(query_df_formatted_e3), 0)

    def test_success_filter_querydf(self):
        query_df_formatted, filters_provided = pf.make_query_df_formatted(
            filters=self.filters,
            consort_input_data=self.consort_input_data)
        self.assertEqual(len(query_df_formatted), 2)
        self.assertEqual(len(query_df_formatted.columns), 3)
        self.assertTrue(isinstance(filters_provided, dict))

    def test_success_query_summary_file(self):
        query_df_formatted, filters_provided = pf.make_query_df_formatted(
            query_summary_file="../data/example_request_summary.csv")
        self.assertEqual(len(query_df_formatted), 2)
        self.assertEqual(len(query_df_formatted.columns), 3)
        self.assertTrue(isinstance(filters_provided, dict))


class test_run_consort_plot_rcode(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.query_empty = pd.DataFrame(columns=['Search_Options',
                                                 'Filter Criteria',
                                                 "Search by this column?"])
        self.data = pd.DataFrame({'Country':
                                  ['IRAN', 'IRAN', 'FRANCE', 'EGYPT'],
                                  'Filtered_Column_Country':
                                  [True, True, False, False]})

        query_r = {'Filter Criteria': ["=IRAN"], 'Search_Options': ['Country']}
        self.query_format_r = pd.DataFrame(query_r)
        # Generate a png file
        pf.run_consort_plot_rcode(self.data,
                                  self.query_format_r, "../data/output.png")

    def test_input_r_pd_df(self):
        with self.assertRaises(ValueError):
            pf.run_consort_plot_rcode("NotDF",
                                      self.query_format_r,
                                      "../data/output.png")

        with self.assertRaises(NameError):
            pf.run_consort_plot_rcode(self.data,
                                      NotDF,
                                      "../data/output.png")

    def test_empty_pd_df(self):
        with self.assertRaises(ValueError):
            pf.run_consort_plot_rcode(self.data,
                                      self.query_empty,
                                      "../data/output.png")

    def test_wrong_logical_operator(self):
        with self.assertRaises(ValueError):
            pf.run_consort_plot_rcode(self.data, self.query_format_r,
                                      "../data/output.png", "&")

    def test_make_wrong_png(self):
        with self.assertRaises(ValueError):
            pf.run_consort_plot_rcode(self.data, self.query_format_r,
                                      "../data/outputpng")

    def test_make_png(self):
        self.assertTrue(os.path.exists("../data/output.png"))

    @classmethod
    def tearDown(self):
        os.remove("../data/output.png")


if __name__ == '__main__':
    unittest.main()
