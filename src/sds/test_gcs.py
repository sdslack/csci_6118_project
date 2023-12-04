from google.oauth2 import service_account
import pandas as pd

# To note: this script uses a service account private key
# to gain access to the Google BigQuery dataset. The service
# account ONLY has access to the BigQuery dataset.

def get_gbq_data(filters, output_columns):
    """Function uses pandas-gbq to get BigQuery data.
    """
    # Format column names to retrieve from BigQuery
    filter_chunks = filters.split(';')
    filter_cols = [chunk.split(':')[-2] for chunk in filter_chunks]
    output_cols = output_columns.split(',')
    cols_set = set(filter_cols + output_cols)

    # Convert filter_cols into a comma-separated string
    cols_set_str = ", ".join([f"`{col}`" for col in cols_set])

    # Query from Google BigQuery using service account
    project_id="csci6118"
    credentials = service_account.Credentials.from_service_account_file(
        '../../etc/csci6118-ee6fa23ab1b7.json')
    query = f"""
    SELECT {cols_set_str}
    FROM csci6118.lanl_hiv_seq_db.results_all
    """
    data = pd.read_gbq(query,
                     project_id=project_id,
                     credentials=credentials)
    return(data)
