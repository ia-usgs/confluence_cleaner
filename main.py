import pandas as pd
import numpy as np
import os
import re  # For regular expressions

# Set display options
pd.options.display.max_rows = 100000

def clean_dataframe(file_path):
    """
    Loads a CSV file, cleans the dataframe by replacing NaNs and -inf values,
    strips whitespace, and selects specified columns.
    """
    df = pd.read_csv(file_path, encoding='windows-1252')
    df = df.replace([np.nan, -np.inf], "")
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def remove_unwanted_rows(df, column_name, keywords):
    """
    This function removes rows from a DataFrame based on the presence of specified keywords in a given column,
    as well as rows where there is whitespace across all columns.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame from which rows need to be removed.
    column_name (str): The name of the column in the DataFrame to check for keywords.
    keywords (list): A list of keywords to look for in the specified column.
    
    Returns:
    pandas.DataFrame: A new DataFrame with rows removed that contain any of the specified keywords in the given column,
    as well as rows where there is whitespace across all columns.
    """
    # Concatenate keywords into a single string separated by '|'
    print("______________________________________________________________________")
    print("Keywords to be removed:", keywords)
    pattern = '|'.join(keywords)
    print("______________________________________________________________________")
    print("Pattern created:", pattern)

    
    # Check if any of the keywords are present in the specified column
    mask1 = df[column_name].str.contains(pattern, case=False, na=False)
    
    # Check if there is whitespace across all columns
    mask2 = df.apply(lambda row: row.str.strip().str.len().eq(0).all(), axis=1)
    
    # Combine the two masks using the logical OR operator
    mask = mask1 | mask2
    
    # Return a new DataFrame with rows removed that satisfy either condition
    return df[~mask]

def add_information_based_on_id(df):
    """
    For rows where 'ID' contains a number, moves the 'Segment' information to a new column 'Segment'
    and clears the information in the old 'Segment' column for those rows.
    Also renames columns according to new specifications.
    """
    # Detect numeric values in the 'ID' column
    numeric_id_mask = df['ID'].apply(lambda x: bool(re.search(r'\d', str(x))))
    # Initialize a new column with NaN values, will be filled and then renamed to 'Segment'
    df['new column'] = np.nan
    df['new column2'] = np.nan
    
    # Copy the value from 'Segment' to 'new column' for rows with a numeric ID
    df.loc[numeric_id_mask, 'new column'] = df.loc[numeric_id_mask, 'Segment']
    df.loc[numeric_id_mask, 'new column2'] = df.loc[numeric_id_mask, 'ID'] #this was added to include ID
    
    # Clear the old 'Segment' content for these rows (if needed)
    # Assuming you want to clear the 'Segment' content that was copied to 'new column'
    df.loc[numeric_id_mask, 'Segment'] = np.nan
    # Rename columns as specified
    # Renaming columns. 'new column2' is renamed to 'ID', 'ID' to 'requirement type', 'Segment' to 'requirement', 'Functional Requirements' to 'verification method', and 'new column' to 'Segment'.
    # This renaming is done in-place.
    print("Renaming columns...")#debugging
    print("______________________________________________________________________")
    print("Columns before rename:", df.columns)#debugging
    df.rename(
        columns={
            'new column2': 'ID',  # Changing column to ID
            'ID': 'requirement type',  # Renaming 'ID' to 'requirement type'
            'Segment': 'requirement',  # Renaming 'Segment' to 'requirement'
            'Functional Requirements': 'verification method',  # Renaming 'Functional Requirements' to 'verification method'
            'new column': 'Segment'  # Renaming 'new column' to 'Segment'
        },
        inplace=True
    )
    print("______________________________________________________________________")
    print("Columns after rename:", df.columns)#debugging
    # Reorder columns to place 'Segment' at the beginning
    print("______________________________________________________________________")
    print("Rearranging columns...")  # debugging
    print("______________________________________________________________________")
    print("Current column order:", df.columns)  # debugging
    col_order = ['ID', 'Segment', 'requirement type', 'requirement', 'verification method']  # had added ID to make 5 columns
    df.loc[numeric_id_mask, 'requirement type'] = np.nan
    print("______________________________________________________________________")
    print("Column order after rearrangement:", col_order)  # debugging
    df = df[col_order]

    #end result
    # Rename columns for clarity and consistency
    # Note: Comments are added to each line for clarity.
    print("______________________________________________________________________")
    print("Renaming columns before:", df.columns)  # debugging
    df.rename(
        columns={
            'requirement type': 'Requirement Type',  # Renaming 'requirement type' to 'Requirement Type'
            'requirement': 'Requirement',  # Renaming 'requirement' to 'Requirement'
            'verification method': 'Verification Method'  # Renaming 'verification method' to 'Verification Method'
        },
        inplace=True  # Perform the renaming in-place
    )
    print("______________________________________________________________________")
    print("Renaming columns after:", df.columns)  # debugging

    return df

def main():
    # Clean the initial file and select specific columns   CHANGE THE NAME HERE
    df = clean_dataframe('23NetworkMultiLevelGuardOriginal.csv')
    new_df = df[["ID", "Segment", "Functional Requirements"]] 
    new_df.to_csv('tester.csv', sep=',', index=False, encoding='utf-8')
    
    # Further clean the output file
    df_2 = clean_dataframe('tester.csv')
    unwanted_keywords = ["User", "Domain", "IAM", "Keith", "SIEM", "Note", "https", "http", 
                         "Soft", "Commu", "yes", "Recommend cutting", 
                         "not all switches", "#NAME?", "ï", "James", "½", "ï¿½ï¿½"]
    print("______________________________________________________________________")
    print("Removing unwanted keywords from 'ID' column...")
    df_2 = remove_unwanted_rows(df_2, "ID", unwanted_keywords)
    print("______________________________________________________________________")
    print("Removing unwanted keywords from 'Functional Requirements' column...")
    df_2 = remove_unwanted_rows(df_2, "Functional Requirements", unwanted_keywords)


    # Add information to new column based on the presence of numbers in the 'ID' column
    # and adjust columns as specified
    print("______________________________________________________________________")
    print("Adding information to new column based on the presence of numbers in the 'ID' column...")
    df_2 = add_information_based_on_id(df_2)
    print("______________________________________________________________________")
    print("Adding information to new column completed.")# debugging
    print("______________________________________________________________________")
    print("Removing unwanted keywords from 'Requirement Type' column...")# debugging
    df_2 = remove_unwanted_rows(df_2, "Requirement Type", unwanted_keywords)
    print("______________________________________________________________________")
    print("Removing unwanted keywords from 'Requirement Type' column completed.")# debugging
    
    # Save the final DataFrame
    df_2.to_csv('CLEANED_FILE.csv', sep=',', index=False, encoding='utf-8')

    # Display the file location
    file_name = os.path.abspath('CLEANED_FILE.csv')
    print("______________________________________________________________________")
    print("Your cleaned file's location is: ", file_name)

    # Delete the intermediate file
    print("______________________________________________________________________")
    print("Removing 'tester.csv' file...")
    if os.path.isfile("tester.csv"):
        os.remove("tester.csv")
        print("______________________________________________________________________")
        print("'tester.csv' file removed successfully.")
    else:
        print("______________________________________________________________________")
        print("'tester.csv' file not found. Nothing to remove.")

if __name__ == "__main__":
    main()
