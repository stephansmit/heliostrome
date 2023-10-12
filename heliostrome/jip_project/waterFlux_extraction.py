import pandas as pd

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

    # Close the Excel writer to ensure proper resource release
    writer.close()

    print(f"Data extraction complete. Extracted data saved as '{output_path}'")


# List of input and output file paths
file_paths = [
    {"input": r"heliostrome/jip_project/results/WaterFlux_moroccoWheat.xlsx", "output": r"heliostrome/jip_project/results/analysed_WaterFlux_morocco.xlsx"},
    {"input": r"heliostrome/jip_project/results/WaterFlux_Bangladesh.xlsx", "output": r"heliostrome/jip_project/results/analysed_WaterFlux_Bangladesh.xlsx"},
    {"input": r"heliostrome/jip_project/results/WaterFlux_northeastCHINA.xlsx", "output": r"heliostrome/jip_project/results/analysed_WaterFlux_NorthEastCHINA.xlsx"},
    {"input": r"heliostrome/jip_project/results/WaterFlux_IranPotato.xlsx", "output": r"heliostrome/jip_project/results/analysed_WaterFlux_IranPotato.xlsx"},
    # Add more file pairs as needed
]

for file_info in file_paths:
    input_path = file_info["input"]
    output_path = file_info["output"]
    extract_rows(input_path, output_path)
