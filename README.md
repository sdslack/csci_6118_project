# **Overview**

### **Scientific Background**

The challene of curing HIV:

+ 1.5 million new infections/year 
+ 42 years since first known cases
+ Current therapies involve taking daily medication
+ We want a vaccine instead

Sequences can help! Why? Early sequences are more helpful because
they represent virus fit enough to transmit and infect a new individual.

TODO: add more here based on what example we choose?

The Los Alamos National Laboratory HIV Database contains around 1 million
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

TODO: add R?

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

TODO: need to add function descriptions here!
