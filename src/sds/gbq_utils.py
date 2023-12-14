"""Function to get partial dataset from Google BigQuery

    * get_gbq_data - Uses pandas-gbq to get specific columns

"""

from google.oauth2 import service_account
import pandas as pd
import os
import sys
sys.path.insert(0, '../.github')  # noqa
sys.path.insert(0, '../../.github')  # noqa
import pandas_gbq.exceptions

# To note: this script uses a service account private key
# to gain access to the Google BigQuery dataset. The service
# account ONLY has access to the BigQuery dataset.


def get_gbq_data(filters, output_columns):
    """Uses pandas-gbq to download only columns of interest from
    the table stored on Google BigQuery. Uses a service account
    with access limited to only the sequence database dataset.
    """
    # Format column names to retrieve from BigQuery
    filter_chunks = filters.strip().split(';')
    filter_cols = [chunk.strip().split(':')[-2] for chunk in filter_chunks]
    output_cols = [col.strip() for col in output_columns.split(',')]
    cols_set = set(filter_cols + output_cols)

    # Update column names had to change for BigQuery formatting
    rename = [
        ('SE id(SA)', 'SE_id_SA'),
        ('PAT id(SSAM)', 'PAT_id_SSAM'),
        ('SE id(SSAM)', 'SE_id_SSAM')
    ]
    for old_val, new_val in rename:
        cols_set = [new_val if x == old_val else x for x in cols_set]

    # Convert filter_cols into a comma-separated string
    cols_set_str = ", ".join([f"`{col}`" for col in cols_set])

    # Query from Google BigQuery using service account
    project_id = "csci6118"

    # Read the content of the R script
    if os.path.exists('csci6118-ee6fa23ab1b7.json'):
        file = 'csci6118-ee6fa23ab1b7.json'
    elif os.path.exists('.github/csci6118-ee6fa23ab1b7.json'):
        file = '.github/csci6118-ee6fa23ab1b7.json'
    elif os.path.exists('../.github/csci6118-ee6fa23ab1b7.json'):
        file = '../.github/csci6118-ee6fa23ab1b7.json'
    else:
        file = '../../.github/csci6118-ee6fa23ab1b7.json'
    credentials = service_account.Credentials.from_service_account_file(file)
    # '../.github/csci6118-ee6fa23ab1b7.json')
    query = f"""
    SELECT {cols_set_str}
    FROM csci6118.lanl_hiv_seq_db.results_all
    """
    try:
        data = pd.read_gbq(query,
                           project_id=project_id,
                           credentials=credentials)
    except pandas_gbq.exceptions.GenericGBQException:
        sys.exit("Pandas GBQ error, likely unrecognized column name.")
    return data

    # Switch column names back into user-queried format
    revert = [
        ('SE_id_SA', 'SE id(SA)'),
        ('PAT_id_SSAM', 'PAT id(SSAM)'),
        ('SE_id_SSAM', 'SE id(SSAM)')
    ]
    for old_val, new_val in revert:
        data.rename(columns={old_val: new_val}, inplace=True)
    return data
