import pandas as pd
import os
from openpyxl import Workbook


def extract_rows(input_path, output_path, start_date = None, field_size=None):
    # Create a new Excel writer object to save the extracted data
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    # Load the Excel file
    xls = pd.ExcelFile(input_path)

    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(input_path, sheet_name=sheet_name)

        # Extract rows with a value in the 'IrrDay' column
        extracted_df = df[df['IrrDay'] != 0]

        if start_date is not None:
            # Add a new column with the calculated dates
            extracted_df['Date'] = pd.to_datetime(start_date) + pd.to_timedelta(extracted_df['time_step_counter'], unit='D')

        # if field_size is not None:
        #     # Convert 'IrrDay' from mm to m
        #     extracted_df['IrrDay'] *= 0.001  # 1 mm = 0.001 m

        #     # Convert volume to m³ based on the field size
        #     extracted_df['IrrDay'] *= field_size

        #     print("Field size provided. 'IrrDay' values have been converted to m³.")

        if not extracted_df.empty:
            # Write the extracted DataFrame to the new Excel file
            extracted_df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Close the Excel writer to ensure proper resource releasegigit 
    writer.close()

    print(f"Data extraction complete. Extracted data saved as '{output_path}'")




def clean_excel_file(input_path, output_path, start_date = None):
    # Load the Excel file
    xls = pd.ExcelFile(input_path)

    # Create a new Excel writer object to save the cleaned data
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(input_path, sheet_name=sheet_name)

        # Check for rows with all columns equal to 0
        zero_rows = (df == 0).all(axis=1)

        # Check for rows where the 'season_counter' column is -1
        season_counter_minus_one = (df['season_counter'] == -1)

        # Filter out unwanted rows
        df = df[~(zero_rows | season_counter_minus_one)]
        #df = df[~(season_counter_minus_one)]
        
        if start_date is not None:
            # Add a new column with the calculated dates
            df['Date'] = pd.to_datetime(start_date) + pd.to_timedelta(df['time_step_counter'], unit='D')


        # Write the cleaned DataFrame to the new Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Close the Excel writer to ensure proper resource release
    writer.close()

    print(f"Data cleaning complete. Cleaned file saved as '{output_path}'")




def min_max_irrigation(excel_file, field_size=None):
    """takes cleaned waterflux for precaution in future. season -1 might give problems
    fieldsize in m2"""
    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame(columns=["variation", "max_irrigation", "min_irrigation"])

    # Read the Excel file with multiple sheets
    xls = pd.ExcelFile(excel_file)

    for sheet_name in xls.sheet_names:
        # Read data from the current sheet
        df_waterflux = pd.read_excel(excel_file, sheet_name)

        # Calculate the max and min IrrDay
        max_irrigation = df_waterflux['IrrDay'].max()
        min_irrigation = df_waterflux['IrrDay'].min()

        # If field_size is provided, convert IrrDay to volume (in cubic meters)
        if field_size is not None:
            # Convert mm to m (1 mm = 0.001 m)
            max_irrigation_m3 = max_irrigation * 0.001
            min_irrigation_m3 = min_irrigation * 0.001

            # Convert volume to cubic meters
            max_irrigation_m3 *= field_size
            min_irrigation_m3 *= field_size

            # Update max_irrigation and min_irrigation
            max_irrigation = max_irrigation_m3
            min_irrigation = min_irrigation_m3

        # Append the results to the DataFrame
        result_df = result_df.append({"variation": sheet_name, "max_irrigation": max_irrigation, "min_irrigation": min_irrigation}, ignore_index=True)

    return result_df

# # Example usage:
# excel_file_path = "your_waterflux_data.xlsx"  # Replace with the actual file path
# field_size_ha = 5.0  # Replace with the actual field size in hectares

# result = process_waterflux_excel(excel_file_path, field_size=field_size_ha)
# print(result)



def summarize_monthly_data(input_path, output_path):
    """use analysed_waterflux from extracted_rows function. make an output location where you want the data stored. Make sure the input waterflux is made with a startdate (fieldsize is optional)"""
    # Create a new Excel writer object to save the summarized data
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    # Load the Excel file
    xls = pd.ExcelFile(input_path)

    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(input_path, sheet_name=sheet_name)

        if 'Date' in df.columns:
            # Ensure the 'Date' column is in datetime format
            df['Date'] = pd.to_datetime(df['Date'])

            # Group by year and month, sum the 'IrrDay' values, and reset the index
            monthly_summary = df.groupby([df['Date'].dt.year, df['Date'].dt.month])['IrrDay'].sum().reset_index()

            # Rename the columns for clarity
            monthly_summary.columns = ['Year', 'Month', 'Total_IrrDay']

            # Create a new Excel sheet for the summarized data
            monthly_summary.to_excel(writer, sheet_name=sheet_name, index=False)

    # Close the Excel writer to ensure proper resource release
    writer.close()

    print(f"Data summarization complete. Summarized data saved as '{output_path}'")

# Example usage:
# summarize_monthly_data('input_data.xlsx', 'output_summary.xlsx')


def resample_and_save_weekly(clean_input_file, output_file):
    xls = pd.ExcelFile(clean_input_file)
    writer = pd.ExcelWriter(output_file, engine='openpyxl')

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(clean_input_file, sheet_name=sheet_name)
        
        # Assuming you have a 'Date' column, set it as the index
        if 'Date' in df.columns:
        # Set the index to be the 'Date' column
            df.set_index('Date', inplace=True)
        else:
        # If 'Date' column doesn't exist, do nothing
            pass
        
        # Resample the data to weekly frequency and calculate the sum
        weekly_data = df.resample('W').sum()

        # Check for rows with all columns equal to 0
        zero_rows = (weekly_data == 0).all(axis=1)
        # Filter out unwanted rows
        weekly_data = weekly_data[~(zero_rows)]
        # Save the resampled data to a new sheet in the output Excel file
        weekly_data.to_excel(writer, sheet_name=sheet_name)

    writer.close()

def mean_percentage_error(dataframe_actual,actual_column_name,dataframe_optimal,optimal_column_name):
    '''Determines the mean percentage error both on an row basis (for weekly purposes)
       as well as a whole to deteremine the whole systems suitability. Allows specific 
       columns to be compared for flexibility.
    '''
    mpe_df_individ = 100* (dataframe_optimal[optimal_column_name]-dataframe_actual[actual_column_name])/dataframe_optimal[optimal_column_name]
    
    mpe_df_average = mpe_df_individ.mean()

    return mpe_df_individ, mpe_df_average

def average_waterflux(excel_file_path):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path)

    # Extract day and month from the "Date" column while ignoring the year
    df['Date (no year)'] = df['Date'].dt.strftime('%m-%d')

    # Calculate the average values for each day/month
    avg_df = df.groupby('Date (no year)')['IrrDay'].mean().reset_index()

    return avg_df
