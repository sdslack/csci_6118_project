"""Getting the data based on the input by the user to create plots. 

Need to think about:
- need a function that will return values to plot 
    - what columns they want 
    - what and how many filters they want to filter their data by 

"""
import pandas as pd
import sys
from IPython.display import display


def filter_df(file_name, filters):
    """ Returns a new data frame with all filtered values 
    - takes in a file name, a dictionary of filters where col is the key and the criteria is the value (this code only accounts for a single criteria for each key col)
    """
    df = pd.read_csv(f"../../test/data/{file_name}", sep = ',')
    filtered_df = df.copy()
    
    for col, filter_val in filters.items():
        filtered_df = filtered_df[filtered_df[col] == filter_val]
        
    return filtered_df
    
    
    
def main():
    file_name = input("Enter the name of the file:")
    filters = {}
    
    while True:
        column = input("Enter a column name to filter or type 'done' to finish: ")
        if column == 'done':
            break
        
        filter_value = input(f"Enter filter criteria for column '{column}': ")
        filters[column] = filter_value 
    
    filtered_df = filter_df(file_name, filters)
    result_cols = input("Enter name of the columns you want to plot (comma-separated): ")
    result_cols = result_cols.split(',')
    
    final_df = filtered_df[[result_cols[0], result_cols[1]]]
    
    #return final_df
    display(final_df)

if __name__ == '__main__':
    main()
