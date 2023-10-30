import sys

# Create a table which tracks query requests
query = {
    'Search_Options': data.columns,
    'Do you plan to search by this column?': [False] * len(data.columns),
    'How do you want to filter?': [None] * len(data.columns),
    'Filter Value': [None] * len(data.columns)
}

# Create a query function which will change values on the query tracking table
def output_query_summary(column_name_of_interest, filter_param, value):
    while True:
        try:
            column_name_of_interest = input("What is the name of the column you want to search by?: ")
            filter_param = input("How do you want to filter?: ")
            if filter_param ne ("equal to", "less than", "greater than", "contains"):
                continue
            except ValueError:
                print("Please enter: equal to, less than, greater than, or contains.")
            value = input("Filter Value: ")

    for i in range(len(query)):
        if query.loc[i, "Search_Options"] == column_name_of_interest:
            query.at[i, "Do you plan to search by this column?"] = True
            query.at[i, "How do you want to filter?"] = filter_param
            query.at[i, "Filter Value"] = value
    return query

# Create a function to subset our data to only the relevant columns being queried
def subset_dataframe_by_names(data, column_names):
    if column_names in df.columns:
        data_subset = data[column_names]
        return data_subset
    else:
        # Handle the case where no matching columns are found
        print("No matching columns found in the DataFrame.")
        return None
        sys.exit(1)
