import pandas as pd
import os

def clean_excel_file(input_path, output_path):
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

        # Write the cleaned DataFrame to the new Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Close the Excel writer to ensure proper resource release
    writer.close()

    print(f"Data cleaning complete. Cleaned file saved as '{output_path}'")

# List of input and output file paths
file_paths = [
    {"input": r"heliostrome/jip_project/results/WaterFlux_moroccoWheat.xlsx", "output": r"heliostrome/jip_project/results/cleaned_WaterFlux_morocco.xlsx"},
    {"input": r"heliostrome/jip_project/results/WaterFlux_Bangladesh.xlsx", "output": r"heliostrome/jip_project/results/cleaned_WaterFlux_Bangladesh.xlsx"},
    {"input": r"heliostrome/jip_project/results/WaterFlux_northeastCHINA.xlsx", "output": r"heliostrome/jip_project/results/cleaned_WaterFlux_NorthEastCHINA.xlsx"},
    {"input": r"heliostrome/jip_project/results/WaterFlux_IranPotato.xlsx", "output": r"heliostrome/jip_project/results/cleaned_WaterFlux_IranPotato.xlsx"},
    # Add more file pairs as needed
]

for file_info in file_paths:
    input_path = file_info["input"]
    output_path = file_info["output"]
    clean_excel_file(input_path, output_path)
