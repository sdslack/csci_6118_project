# **Overview**

### **Scientific Background**

The challenge of curing HIV:

+ 1.5 million new infections/year 
+ 42 years since first known cases
+ Current therapies involve taking daily medication
+ We want a vaccine instead

Sequences can help! Why? 

+ Early sequences are more helpful because 
    they represent virus fit enough to transmit and infect a new individual.
+ We can identify countries/geographic areas
    facing a new mutation in the HIV virus
+ We can understand how differences in the virus
    correspond to differences in clinical outcomes
TODO: add more here based on what example we choose?

The Los Alamos National Laboratory HIV Database contains over 1 million
HIV genetic sequences along with comprehensive metadata. It is a goverment-
funded database that is updated biweekly to monthly, and it includes
information about genetic HIV sequences including where they were isolated,
health status of the patient infected, year when collected, virus subtype,
and more. The database can be queried manually at the following link:

https://www.hiv.lanl.gov/components/sequence/HIV/search/search.html

### **Project Rationale**

This project aims to provide the code needed to summarize database query
selections from the Los Alamos HIV Sequence Database. Although the database
can be queried manually at the link included above, this is not necessarily
ideal and can lead to unwanted biases. Our repository aims to filter the
large dataset based on a number of search criteria, then create several plots
based on that search. The goal is to offer the user a better understanding of
the data available in the database before deciding what to download, as well
as to offer an understanding of how different filtering choices would affect
how many and which entries from the dataset are downloaded. 

**What is the problem with manual queries?**

Manual queries require that the user define the query without having
an idea of the distribution of information that is availabe. Additionally,
they are not very reproducible. 

**Why is this important?**

+ Understanding of data availability for research questions
+ Understanding of research gaps and need for novel research
+ Removing unwanted biases in data download from large public portals
    + i.e. database shows multiple results from one person/study
+ Improving reproducibility of searching and data download

**Goal: Understand available data**

Develop a codebase to summarize data from the HIV database:

+ Visualize the available metadata included with genetic sequences
+ Allow for better selection of sequences for download
+ Improve understanding of how query choices narrow available data

TODO: add example plots here?

**Reach Goal: Automate visualization and searching**

TODO: add graphic from pitch slides?

### **Project Function**

Currently, the project is implements the first goal stated above but not
the reach goal. Using a small amount of test data from the Los Alamos HIV
Sequence Database (included at test/data/LANL_HIV1_2023_seq_metadata.csv),
the project provides a summary of the available metadata for the sequences.

# **Installation**

The project source code is written in Python3 but is designed to be
run using bash from the command line. An example bash script is
included in the project repository.

### **Dependencies**

Python3, bash, and R are required to run the code in this project.

The dependencies for Python3 are:
+ Numpy
+ Pandas
+ matplotlib

You can install these with the following code within the terminal:

``` bash
conda install numpy
conda install pandas
conda install matplotlib
```

The dependencies for R are:
+ ggplot2
+ janitor
+ dplyr

You can install these with the following code within the terminal:

``` bash
Rscript -e "install.packages(c('janitor', 'dplyr', 'ggplot2'), repos='https://cran.rstudio.com')"

```

The example bash script sds_test_run.sh should be executed from the top
level of the repository.

### **Step by Step Installation Instructions**

1. Clone this repository to your local machine:

```bash
git clone git@github.com:sdslack/csci_6118_project.git
```

2. Navigate to the directory containing the cloned repository:

```bash
cd csci_6118_project
```

3. View the contents of the repository:

```bash
ls
```
```
LICENSE  README.md  docs/  src/ test/
```

This document is the README.md, docs/ contains any data or plots written
out by the currently implemented code, src/ contains the source code
for this project, and test/ contains the unit and functional tests.

4. The subset of test data download from the Los Alamos HIV Sequence
    Database is located at test/data/LANL_HIV1_2023_seq_metadata.csv.

5. The src/ directory is currently split so that each team member has a
    separate folder. Inside some of these folders, there are bash scripts
    that can be used to run examples:

```bash
cd src/sdslack
bash sds_test_run.sh
```
    Nothing is printed upon successful execution, but a plot is added to the
    docs/ folder, named according to the column that was selected.

# **Testing**

Unit tests are located at test/unit and functional tests (which use the Stupid
Simple Bash Testing Framework) are loated at test/func. They can be run from
inside each respective directory, and are not currently implemented to
automatically run.

Unit tests can be run with the following code:

```bash
cd /test/unit
python -m unittest test_sds_utils.py
```

Functional tests can be run with the following code:

```bash
cd /test/func
bash test_sds_utils.sh
```

Style tests for python (PEP8, tested using pycodestyle), are executed when
any branch is pushed to the GitHub-hosted repository as well as when a pull
request is made on the main branch on GitHub. The code that runs these tests
is located at .github/workflows/tests.yml. In order to run pycodestyle, the
tests sets up mamba environment "csci6118" using its environment file at test/etc/csci6118_env.yml

# **Usage**

### **Examples**

Inside each team member's folder in src/, there is a bash script that can be
run as an example to execute the code. For example:

```bash
cd src/lkr
bash run.sh
```

```bash
cd src/jb
bash run_query_data.sh
```

```bash
cd src/gg
bash run.sh
```

# **Functions**

### **Plotting Code**

*To note: queries to make the plots are currently implemented separately*
*by each team member, but the goal is to eventually have all queries*
*implemented by the main querying code (described in the next section)*
*located at src/jb/query_data.py.*

**src/gg**

Within the src/gg folder, all scripts help create 
    a .png file containing a consort diagram. This diagram helps explain
    which sequences were excluded or included based on given search criteria.
    A run.sh file has been provided as an example.
    The scripts must be run in the following order:
    1. query_functions.py to allow for creation of important functions
        There are two different functions within this file.
        subset_dataframe_by_names() will subset a dataset by column name.
        output_query_summary() changes the query.csv file to reflect
            query parameters.
    2. make_query.py to create queries for the database
    3. data_subsetting.py to prepare the data for the R scropt
    4. consort_plot.r which will generate the consort plot
    
**src/sds**

In the src/sds folder, sds_test_run.sh runs an example of the code that
will create a histogram plot of the HIV subtypes in the test data. This is
the plot that is created based on the selection of column 24 in the test
data, but selecting a different column would cause the data in that column
to be plotting instead, and would update plot labels as well as plot title.

The test bash script can be run as follows:

```bash
cd src/sds
bash sds_test_run.sh
```

This will run query_categ_plot.py with the inputs given in the bash script
(the path to the test data file and the column number to query). The help
information for query_categ_plot.py clarifies this:

``` bash
python query_categ_plot.py --help
```

```
usage: query_categ_plot [-h] --file-name FILE_NAME --categ-column CATEG_COLUMN --plot-path PLOT_PATH

Queries and plots histogram of values from any column from the input data.

options:
  -h, --help            show this help message and exit
  --file-name FILE_NAME
                        Name of the data file to read
  --categ-column CATEG_COLUMN
                        Number of categorical column to query
  --plot-path PLOT_PATH
                        Path to write output plot to
```

The output plot is written to the docs/ folder and is named according to the
name of the column selected. The query_categ_plot.py script calls on the
functions in sds_utils.py:

+ get_col_all - returns the values from a given column in a file
+ plot_hist - plots a histogram of values passed in

The docustring for these functions can be accessed with the following code:

```bash
cd src/sds
python
import sds_utils
sds_utils.get_col_all.__doc__
sds_utils.plot_hist.__doc__
```

```bash
# For get_col_all
Queries the given file and returns all values from
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

# For plot_hist
Plots histogram of values in a file. Writes out as .png.

Parameters
----------
result_col : list of str
    List of all values from the requested column
output_path : str
    Path to write output plot to   
```

### **Main Querying Code**

**src/jb**

In the jb folder within the source folder, is the query_data.py script that will execute the main querying functionalities for the data. The code will essentially query an inputted data file based on provided querying filters for the data and then output a csv file of the filtered data. The way filter criteria are inputted must follow the correct format. 

- For the filter parameters, inputs must be provided in quotations when providing multiple filters.
- Each individual variable to be filterd must be written with a semicolon in between the name of variable and filter criteria/value like this --> "col_name:value1"
- If there are multiple variables to be filtered, then each different variable must be separated with a && --> "col_name1:value1 && col_name2:value2"
- If the variable/column(s) to be filtered are not in the data frame or has been typed incorrectly, the code will query only the columns found in the dataframe and spit out a message indicating which columns where not in the found. 

The code will take in four main parameters:

1. --file: Name of file and path to file
    - Only takes in a csv.
2. --filters: Filters for any variables both categorical and numerical. 
    - This is not a required filter.
    - This parameter also takes in the input as a string. 
    - Both numerical and categorical filters can be taken as:
        - Numerical: 
            - a range (inclusive) --> "col_name:0-7"
            - an inequality (inclusive) --> "col_name:>=7" or "col_name:<=7"
            - a single numerical number --> "col_name:=7"
            - not equal to a certain number --> "col_name: !=7"
        - Categorical: 
            - single values equal to --> "col_name: =United States"
            - single values not equal to --> "col_name: !=United States"
    - The code can also take multiple variable filter criteria for each individual variable to filter and must be comma separated --> "col_name1:=7,9-15,>20 && col_name2:Europe,United States"
4. --query_output_file: Name of output file and path to file
    - File is written out as a csv.
5. --output_columns: Names of the columns that will be outputted to the queried data file.
    - This is not a required field.
    - If not provided, the code will output all of the columns in the data frame.
    - If provided, columns need to be comma separated.
6. --query_request_file: Name of query request summary and path to file
    - File is written out as csv.


**Example Input**
This is an example to show ways input can be written. This can be used on the test data file but will come up with nothing and there are a limited number of examples that can be provided with this many filters since the data file is small. 
```
python query_data.py --file ../../test/data/LANL_HIV1_2023_seq_metadata.csv 
--filters "Subtype:B,35_A1D && Georegion: =North America && Sequence Length:1035-2025,<915 && Percent non-ACGT:=0.0" --output_file ../../doc/filtered_data.csv --output_columns "Sequence Length, Sequence --query_request_file ../../doc/query_summary_request.csv"
```

### **Change Log***

TODO: update this!
