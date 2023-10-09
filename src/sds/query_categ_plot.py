# TODO: add all code here, then split some to function script

import argparse
import sys

# TODO: update doc once update functions
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
    args = parser.parse_args()
    return args
    

# TODO: eventually integrate this with other query functions
def get_categ_col(args):
    """Runs get_categ_col
    
    Parameters
    ----------
    args : argparse.Namespace
        Arguments from command line
    
    Returns
    -------
    categ_col : list of str
        List of values from the categorical column

    """
    try:
        if args.categ_column < 0:
            raise ValueError
    except ValueError:
        print('Country column must be positive.')
        sys.exit(1)

    result = []
    line_num = 0
    with open(args.file_name, 'r') as f:
        for line in f:
            line_num += 1
            if line_num < 3:
                continue
            line = line.rstrip().split('\t')
            try:
                line[args.categ_column]
            except IndexError:
                print("Query column out of file range.")
                sys.exit(1)
            result.append(line[args.categ_column])
    return result

if __name__ == '__main__':
    """Runs get_args and get_categ_col and prints results.

    """
    args = get_args()
    try:
        f = open(args.file_name, 'r')
    except FileNotFoundError:
        print("File not found: " + args.file_name)
        sys.exit(1)
    except PermissionError:
        print("Could not open: " + args.file_name)
        sys.exit(1)
    print(get_categ_col(args))