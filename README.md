# Indian-District-Court-Data-DDL

A database of ~80 million Indian district court data across states from the Development Data Lab has been downloaded from here:  
https://www.dropbox.com/sh/hkcde3z2l1h9mq1/AAB2U1dYf6pR7qij1tQ5y11Fa/csv?dl=0&subfolder_nav_tracking=1

Due to the large nature of the dataset, only the data from the last 5 years have been taken.

The codebase contains separate directories for the Analysis and the Classification tasks.

## Execute Instructions

Download the dataset and put it in the same directory as the repository so that the directory structure looks like this:

```
.
|-- Indian-District-Court-Data-DDL
|   |-- Analysis
|   |-- Classification
|   `-- README.md
|-- csv
|   |-- acts_sections.csv
|   |-- acts_sections.tar.gz
|   |-- cases
|   |   |-- cases
|   |   |   |-- cases_2010.csv
|   |   |   |-- cases_2011.csv
|   |   |   |-- cases_2012.csv
|   |   |   |-- cases_2013.csv
|   |   |   |-- cases_2014.csv
|   |   |   |-- cases_2015.csv
|   |   |   |-- cases_2016.csv
|   |   |   |-- cases_2017.csv
|   |   |   `-- cases_2018.csv
|   |   `-- cases.tar.gz
|   |-- judges_clean.csv
|   |-- judges_clean.tar.gz
|   `-- keys
|       |-- keys
|       |   |-- act_key.csv
|       |   |-- cases_court_key.csv
|       |   |-- cases_district_key.csv
|       |   |-- cases_state_key.csv
|       |   |-- disp_name_key.csv
|       |   |-- judge_case_merge_key.csv
|       |   |-- purpose_name_key.csv
|       |   |-- section_key.csv
|       |   `-- type_name_key.csv
|       `-- keys.tar.gz
```
