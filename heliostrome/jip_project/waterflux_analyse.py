import pandas as pd

# Define the path to your Excel file
excel_file_path = r"heliostrome/jip_project/results/WaterFlux_moroccoWheat.xlsx"

# Load the Excel file
xls = pd.ExcelFile(excel_file_path)

# Create a new Excel writer object to save the cleaned data
writer = pd.ExcelWriter(r'heliostrome/jip_project/results/cleaned_waterfluxdata_morocco.xlsx', engine='openpyxl')

# Iterate through each sheet in the Excel file
for sheet_name in xls.sheet_names:
    # Read the sheet into a DataFrame
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

    # Check if there are any rows where all columns have a value of 0
    zero_rows = (df == 0).all(axis=1)

    # Check if there are any rows where the column 'season_counter' contains -1
    season_counter_minus_one = (df['season_counter'] == -1)

    # Filter out rows where all columns have a value of 0 and rows where 'season_counter' is -1
    df = df[~(zero_rows | season_counter_minus_one)]

    # Write the cleaned DataFrame to the new Excel file
    df.to_excel(writer, sheet_name=sheet_name, index=False)

# Close the Excel writer to ensure proper resource release
writer.close()

print("Data cleaning complete. Cleaned file saved as 'cleaned_data.xlsx'")
