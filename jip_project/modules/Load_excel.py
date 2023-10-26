import pandas as pd
import altair as alt

def factors_to_run(sheet_name):
    # Load the Excel file
    excel_file = r'heliostrome\jip_project\results\Factors to run simulation.xlsx'
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Define a mapping of row names to row indices
    row_mapping = {
        "Case Study": 0,
        "Longitude": 1,
        "Latitude": 2,
        "Start Date": 3,
        "End Date": 4,
        "Sowing Date": 5,
        "Soil Type": 6,
        "Irrigation Method": 7,
        "Initial Water Content": 8,
        "Crop Type": 9,
        "Yield": 10,
        "Water used": 11,
        "Mulches": 12,
        "Maximum Flow Rate": 13,
        "Average Flow Rate": 14,
        "Modules Per String": 15,
        "Strings in Parallel": 16,
        "PV Module Name": 17,
        "Pump Name": 18,
        "Static Head": 19,
        "Total Length of Pipes": 20,
        "Diameter of Pipes": 21,
        "Material of Pipes": 22 
    }

    # Initialize a dictionary to store the extracted rows with names
    extracted_rows = {}

    # Loop through the row names and extract the rows
    for row_name, row_index in row_mapping.items():
        # Check if the row index is within the valid range
        if row_index < df.shape[0]:
            row_data = df.iloc[row_index, 1:].tolist()
            extracted_rows[row_name] = row_data
        else:
            # Handle the case where the row is missing or out of bounds
            extracted_rows[row_name] = None

    # Now, the extracted_rows dictionary contains the data with row names as keys
    return extracted_rows



