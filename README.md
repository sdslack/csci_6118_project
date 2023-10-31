# **Overview**

### **Scientific Background**

The challene of curing HIV:

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
funded database that is updated biweekly to monthly. The database can be
queried manually at the following link:

https://www.hiv.lanl.gov/components/sequence/HIV/search/search.html

### **Project Rationale**

This project provides the code needed to summarize database query
selections from the Los Alamos HIV Sequence Database. Although the database
can be queried manually at the link included above, this is not necessarily
ideal and can lead to unwanted biases.

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

TODO: add example plot here?

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

Python3 and bash are required to run the code in this project.

The dependencies for Python3 are:
+ Numpy
+ Pandas

You can install these with the following code within the terminal:
```
conda install numpy
conda install pandas

```

The dependencies for R are:
+ ggplot2
+ janitor
+ dplyr

You can install these with the following code within the terminal:

```
Rscript -e 'install.packages("ggplot2", repos="https://cloud.r-project.org")'
Rscript -e 'install.packages("janitor", repos="https://cloud.r-project.org")'
Rscript -e 'install.packages("dplyr", repos="https://cloud.r-project.org")'

```

The example bash script sds_teset_run.sh should be executed from the top
level of the repository.

Unit tests (located at test/unit), functional tests (test/func), and style
tests for python (PEP8, tested using pycodestyle), are executed when
any branch is pushed to the GitHub-hosted repository as well as when a pull
request is made on the main branch on GitHub. 

TODO: need to actually include tests and set up workflows file?

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
LICENSE  README.md  sds_test_run.sh  src/ test/
```

This document is the README.md, sds_test_run.sh is a bash script that runs
examples, and src/ contains the source code for this project.

4. The subset of test data download from the Los Alamos HIV Sequence
    Database is located at test/data/LANL_HIV1_2023_seq_metadata.csv.
    This file can be downloaded from the following link

5. The example bash script can be run with the following code:

```bash
bash sds_test_run.sh
```

# **Usage**

### **Examples**

The bash script sds_test_run.sh includes TBD:

```bash
bash run.sh
```
TODO: update this if we want to keep it?


### **Functions**

Within the gg folder, all scripts help create 
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
    

TODO: need to add function descriptions here!

### **Main Querying Code**

In the jb folder within the source folder, is the query_data.py script that will execute the main querying functionalities for the data. The code will essentially query an inputted data file based on provided querying filters for the data and then output a csv file of the filtered data. The way filter criteria are inputted must follow the correct format. 

- For the filter parameters, inputs must be provided in quotations when providing multiple filters.
- Each individual variable to be filterd must be written with a semicolon in between the name of variable and filter criteria/value like this --> "col_name:value1"
- If there are multiple variables to be filtered, then each different variable must be separated with a && --> "col_name1:value1 && col_name2:value2"

The code will take in four main parameters:

1. --file: Name of file and path to file
2. --categorical_filters: Filters for any categorical variables 
    - This is not required.
    - This parameter takes in the input as a string.
    - It can also take multiple filter criteria for each variable to filter but these must be comma separated.
    - Example of command line input: --categorical_filters "col_name1:value1,value2 && col_name2:value3,value4"
3. --numerical_filters: Filters for any numerical variables 
    - This is not a required filter.
    - This parameter also takes in the input as a string. 
    - Filters can be taken as:
        - a range (exclusive) --> "col_name:0-7"
        - an inequality (exclusive) --> "col_name:>7" or "col_name:<7"
        - a single numerical number --> "col_name:=7"
    - The code can also take multiple variable filter criteria for each individual variable to filter and must be comma separated --> "col_name:=7,9-15,>20"
4. --output_file: Name of output file

**Example Input**
This is an example to show ways input can be written. This can be used on the test data file but will come up with nothing and there are a limited number of examples that can be provided with this many filters since the data file is small. 
```
python query_data.py --file ../../test/data/LANL_HIV1_2023_seq_metadata.csv --categorical_filters "Subtype:B,35_A1D && Georegion:North America" --numerical_filters "Sequence Length:1035-2025,<915 && Percent non-ACGT:=0.0" --output_file ../../doc/filtered_data.csv
```
### **Change Log***

