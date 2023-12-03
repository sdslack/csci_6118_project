
from google.oauth2 import service_account
import pandas as pd

# To note: this script uses a service account private key
# to gain access to the Google BigQuery dataset. The service
# account ONLY has access to the BigQuery dataset.

def test_gbq_data(project_id="csci6118"):
    """Function uses pandas-gbq to get BigQuery data.
    TODO: need to update to get just specific columns.
    """
    credentials = service_account.Credentials.from_service_account_file(
        '../../etc/csci6118-ee6fa23ab1b7.json')
    query = """
    SELECT *
    FROM csci6118.hiv_test_data.hiv_test_data_table
    """
    data = pd.read_gbq(query,
                     project_id=project_id,
                     credentials=credentials)
    print(data)

if __name__ == '__main__':
    test_gbq_data()
