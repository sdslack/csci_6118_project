"""Plots histogram of column specificed by user input

        * get_args - gets command line arguments.
        * main - runs get_args, thenruns run_plot_hist to write out plot of results.

"""

import os
import argparse
import sys
import sds_utils


def get_args():
    """Get command line arguments.

    Returns
    -------
    args : argparse.Namespace
        Arguments from command line

    """
    parser = argparse.ArgumentParser(
        description=('Queries and plots histogram of values from ' +
                     'any column from the input data.'),
        prog='query_categ_plot'
    )
    parser.add_argument('--file-name',
                        type=str,
                        required=True,
                        help='Name of the data file to read. Expects ' +
                        'output from LKR, unique values from queried ' +
                        'column in first column and counts of those ' +
                        'values in second column')
    parser.add_argument('--plot-prefix',
                        type=str,
                        required=True,
                        help='Path and prefix for output plot')
    args = parser.parse_args()
    return args


def run_get_counts(args):
    """Runs get_counts and returns results. Expects output from LKR.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments from command line

    Returns
    -------
    result : list of str
        List of all values from the requested column

    """
    try:
        f = open(args.file_name, 'r')
    except FileNotFoundError:
        print("File not found: " + args.file_name)
        sys.exit(1)
    except PermissionError:
        print("Could not open: " + args.file_name)
        sys.exit(1)

    counts_df = sds_utils.get_counts(args.file_name)
    return counts_df


def run_plot_hist(args, counts_df):
    """Runs plot_hist and writes out plot.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments from command line
    counts_df : pandas dataframe
        Dataframe of given CSV file with counts of column values

    """
    output_prefix = args.plot_prefix
    try:
        f = open(output_prefix + '_test.txt', 'w')
    except FileNotFoundError:
        print("Output path not found: " + output_path)
        sys.exit(1)
    except PermissionError:
        print("No permissions for output path: " + output_path)
        sys.exit(1)
    else:
        f.close()
        os.remove(output_prefix + '_test.txt')
    sds_utils.plot_hist(counts_df, output_prefix)


if __name__ == '__main__':
    """Runs get_args, run_get_col_all, and run_plot_hist.

    """
    args = get_args()
    counts_df = run_get_counts(args)
    run_plot_hist(args, counts_df)
