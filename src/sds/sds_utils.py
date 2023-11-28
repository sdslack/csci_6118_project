"""SDS functions for query and plot

    * get_col_all - returns the values from a given column in a file
    * plot_hist - plots a histogram of values passed in

"""

import sys
import matplotlib
matplotlib.use('Agg')  # noqa
import matplotlib.pyplot as plt
import pandas as pd


def get_counts(file_name):
    """Reads the given CSV file into a pandas dataframe. Expects
    output from LKR.

    Parameters
    ----------
    file_name : str
        Name of the file to query

    Returns
    -------
    counts : pandas dataframe
        Dataframe of given CSV file with counts of column values
    """
    counts_df = pd.read_csv(file_name)
    # TODO: add code to confirm Counts in second column?
    return counts_df


def plot_hist(counts_df, output_path):
    """Plots histogram of given counts.

    Parameters
    ----------
    counts_df : pandas dataframe
        Dataframe of given CSV file with counts of column values
    output_path : str
        Path to write output plot to
    """

    values = counts_df.iloc[:, 0]
    counts = counts_df.iloc[:, 1]

    x_label = counts_df.columns[0]  # TODO: check assumption with LKR?
    y_label = 'Counts'
    title = 'Histogram of ' + x_label + ' Counts'  # use column name

    # Make plot
    fig, ax = plt.subplots()
    ax.bar(values, counts)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    # Rotate x-axis labels
    plt.xticks(rotation=45)

    file_name = x_label + '_hist.png'  # use column name

    plt.savefig(output_path + '/' + file_name, bbox_inches='tight')
