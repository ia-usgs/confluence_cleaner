# Purpose

This script allows you to extract specific columns of data from tables copied from Confluence, and save them in a .csv file. This .csv file can then be imported into DOORS, a software tool used for test case management. The script is designed to extract data that includes an ID, Segment, Requirement Type, Requirement, and Verification Method. It makes the process of obtaining this data from Confluence easier and more efficient.

Included in this repository is an example original file, `23NetworkMultiLevelGuardOriginal.csv`, and its final version, `CLEANED_FILE.csv`, with the desired columns included.

## Instructions

To use this script, you can follow these steps:

1. Copy a table from Confluence and paste it into an Excel spreadsheet.
2. In the table, create a new row at the very top and add the following columns: ID, Segment, Functional Requirements.
3. Save the file as a .csv file with whatever name you prefer. This file name will replace `original_file.csv` on line 106. In this case, `23NetworkMultiLevelGuardOriginal.csv`.
4. Make sure the original file is in the same directory as this script.
5. Open a terminal or command prompt and navigate to the directory where the script is located.
6. Run the following command: `python last_script.py`
7. The script will create a new file, `CLEANED_FILE.csv`, with the desired columns included. This file still requires a little bit of cleanup, such as removing any unnecessary rows or columns.


