"""SDS functions for query and plot

    * get_col_all - returns the values from a given column in a file
    * plot_hist - plots a histogram of values passed in

"""

import sys
import matplotlib
matplotlib.use('Agg')  # noqa
import matplotlib.pyplot as plt

def get_col_all(file_name, categ_col):
    """ Queries the given file and returns all values from
    the requested column.

    Parameters
    ----------
    file_name : str
        Name of the file to query
    categ_col : int
        Number of the column to query

    Returns
    -------
    result : list of str
        List of all values from the requested column
    """
    result = []
    # line_num = 0
    with open(file_name, 'r') as file:
        for line in file:
            # line_num += 1
            # if line_num < 2:  # skip header
                # continue
            line = line.rstrip().split(',')
            try:
                line[categ_col]
            except IndexError:
                print("Query column out of file range.")
                sys.exit(1)
            result.append(line[categ_col])
    return result

def plot_hist(result_col, output_path):
    """Plots histogram of values in a file. Writes out as .png.

    Parameters
    ----------
    result_col : list of str
        List of all values from the requested column
    output_path : str
        Path to write output plot to
    """
    result_col = [val.replace('"', '') for val in result_col]  # remove double quotes
    x_label = result_col[0]  # use column name
    y_label = 'Count'
    title = 'Histogram of ' + x_label + ' Category Counts'  # use column name
    result_col.pop(0)  # remove column name
    data = result_col

    # Check if all values can be converted to numeric
    if all(val.replace('"', '').isdigit() for val in data):
        data = [float(val) for val in data]

    # Make plot
    data.sort()
    fig, ax = plt.subplots()
    ax.hist(data)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    # Rotate x-axis labels
    plt.xticks(rotation=45)

    file_name = x_label + '_hist.png'  # use column name
    
    plt.savefig(output_path + '/' + file_name, bbox_inches='tight')
