import numpy as np
import pandas as pd
import sys
import src/gg/Consort_Data_Functions as cdf


# Read in Data
data = pd.read_csv('LANL_HIV1_2023_seq_metadata.csv')

# Data Clean-Up
data = data.applymap(lambda x: "Unknown" if pd.isna(x) or x == "" else x)
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

#Call user input function
query = cwf.output_query_summary("country", "equal to", "IRAN")

#Create subset of dataset based on search options
columns_of_interest = query.loc[query['Do you plan to search by this column?'] == True, 'Search_Options'].tolist()
consort_input_df_pre = cdf.subset_dataframe_by_names(data, columns_of_interest)

#Subset the query dataset to only the important columns
query_requests = query[query['Do you plan to search by this column?'] == True]


#Now for each row in the query column, 
  #we will write a loop to make the appropriate changes to our dataframe
consort_input_df = consort_input_df_pre
consort_input_df['All'] = 1


for i in range(len(query_requests)):
    filtered_column = query_requests.at[i, 'Search_Options']
    filter_value = query_requests.at[i, 'Filter Value']
    exclude_col_name = "Exclude_Column" + str(i)
    include_col_name = "Include_Column" + str(i)
    consort_input_df[include_col_name] = "Unknown"
    consort_input_df[exclude_col_name] = "Unknown"

    for q in range(len(consort_input_df)):
        if consort_input_df.at[q, filtered_column] == filter_value:
            consort_input_df.at[q, exclude_col_name] = "Included"
            consort_input_df.at[q, include_col_name] = consort_input_df.at[q, filtered_column]
        else:
            consort_input_df.at[q, exclude_col_name] = consort_input_df.at[q, filtered_column]
            consort_input_df.at[q, include_col_name] = "Excluded"
