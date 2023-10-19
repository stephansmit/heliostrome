import pandas as pd
import os


def extract_rows(input_path, output_path):
    # Create a new Excel writer object to save the extracted data
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    # Load the Excel file
    xls = pd.ExcelFile(input_path)

    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(input_path, sheet_name=sheet_name)

        # Extract rows with a value in the 'IrrDay' column
        extracted_df = df[df['IrrDay'] != 0]

        if not extracted_df.empty:
            # Write the extracted DataFrame to the new Excel file
            extracted_df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Close the Excel writer to ensure proper resource releasegigit 
    writer.close()

    print(f"Data extraction complete. Extracted data saved as '{output_path}'")




def clean_excel_file(input_path, output_path):
    # Load the Excel file
    xls = pd.ExcelFile(input_path)

    # Create a new Excel writer object to save the cleaned data
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(input_path, sheet_name=sheet_name)

        # Check for rows with all columns equal to 0
        #zero_rows = (df == 0).all(axis=1)

        # Check for rows where the 'season_counter' column is -1
        season_counter_minus_one = (df['season_counter'] == -1)

        # Filter out unwanted rows
        #df = df[~(zero_rows | season_counter_minus_one)]
        df = df[~(season_counter_minus_one)]


        # Write the cleaned DataFrame to the new Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Close the Excel writer to ensure proper resource release
    writer.close()

    print(f"Data cleaning complete. Cleaned file saved as '{output_path}'")


