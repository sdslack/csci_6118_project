"""Getting the data based on the input by the user to create plots. 

Need to think about:
- need a function that will return values to plot 
    - what columns they want 
    - what and how many filters they want to filter their data by 

"""
import pandas as pd

def filter_df(file_name, filters):
    """ Returns a new data frame with all filtered values 
    - takes in a file name, a dictionary of filters where col is the key and the criteria is the value (this code only accounts for a single criteria for each key col)
    """
    df = pd.read_csv('../../test/data' + file, sep = ',')
    filtered_df = df.copy()
    
    for col, filter_val in filters.items():
        filtered_df = filtered_df[filter_df[col] == filter_val]
        
    return filtered_df
        
    