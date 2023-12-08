"""SDS functions for query and plot

    * get_counts - reads counts of values from query column
        in format output by src/lkr into dataframe
    * plot_hist - plots a histogram of values passed in

"""

import sys
import matplotlib
matplotlib.use('Agg')  # noqa
import matplotlib.pyplot as plt
import pandas as pd


def get_counts(file_name):
    """Reads the given CSV file with counts of values from query
    column into a pandas dataframe, in format output by src/lkr.

    Parameters
    ----------
    file_name : str
        Name of the file to query

    Returns
    -------
    counts : pandas dataframe
        Dataframe of given CSV file with counts of column values
    """
    try:
        counts_df = pd.read_csv(file_name)
    except pd.errors.EmptyDataError:
        sys.exit("Input data is empty.")
    return counts_df


def plot_hist(counts_df, output):
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

    x_label = counts_df.columns[0]
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

    x_label = x_label.replace(" ", "_")
    # output = output_prefix + '_' + x_label + '_hist.png'  # use column name

    plt.savefig(output, bbox_inches='tight')
