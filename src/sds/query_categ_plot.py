"""Queries and prints column specificed by user input

        * get_args - gets command line arguments.
        * run_get_col_all - runs get_col_all from sds_utils
        * main - runs get_args, run_get_col_all, then run_plot_hist
        to write out plot of results.

"""

import os
import argparse
import sys
import sds_utils

# TODO: need to query by col name, not position
def get_args():
    """Get command line arguments.
    
    Returns
    -------
    args : argparse.Namespace
        Arguments from command line

    """
    parser = argparse.ArgumentParser(
        description=('Default prints integer list all results).'),
        prog='print_fires'
    )
    parser.add_argument('--file-name',
                        type=str,
                        required=True,
                        help='Name of the data file to read')
    parser.add_argument('--categ-column',
                        type=int,
                        required=True,
                        help='Number of categorical column to query')
    parser.add_argument('--plot-path',
                        type=str,
                        required=True,
                        help='Path to write output plot to')
    args = parser.parse_args()
    return args
    
def run_get_col_all(args):
    """Runs get_col_all and returns results.
    
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
    try:
        if args.categ_column < 0:
            raise ValueError
    except ValueError:
        print('Column number must be positive.')
        sys.exit(1)

    result = sds_utils.get_col_all(args.file_name, args.categ_column)
    return result

def run_plot_hist(args, col):
    """Runs plot_hist and writes out plot.
    
    Parameters
    ----------
    col : list of str
        List of all values from the requested column

    """
    output_path = args.plot_path
    try:
        f = open(output_path + '/test.txt', 'w')
    except FileNotFoundError:
        print("Output path not found: " + output_path)
        sys.exit(1)
    except PermissionError:
        print("No permissions for output path: " + output_path)
        sys.exit(1)
    else:
        f.close()
        os.remove(output_path + '/test.txt')
    sds_utils.plot_hist(col, output_path)
   

if __name__ == '__main__':
    """Runs get_args, run_get_col_all, and run_plot_hist.

    """
    args = get_args()
    col = run_get_col_all(args)
    run_plot_hist(args, col)
