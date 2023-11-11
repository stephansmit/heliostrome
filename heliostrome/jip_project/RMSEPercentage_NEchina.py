import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt

# Read the Excel file
input_file_path = r"heliostrome\jip_project\results\test_results_northeastCHINA.xlsx"
output_file_path = r"heliostrome\jip_project\results\RMSE_Percentage_NEchina.xlsx"

# Read input and output data
input_df = pd.read_excel(input_file_path, sheet_name="Input Parameters")
output_df = pd.read_excel(input_file_path, sheet_name="Output Results")

# Create an empty Excel file
writer = pd.ExcelWriter(output_file_path, engine="openpyxl")

# Create an empty DataFrame to store the output of RMSE
rmse_df = pd.DataFrame(columns=["Case Study", "Yield RMSE", "Yield RMSE Percentage"])

#'Water Used RMSE', 'Water Used RMSE Percentage'

# Merge the output and input data on 'Case Study'
matched_data = pd.merge(output_df, input_df, on="Case Study", how="inner")

# Get a list of unique Case Studies
case_studies = input_df["Case Study"].unique()

# Loop to calculate RMSE and RMSE Percentage for each Case Study
for case_study in case_studies:
    # Select data for a specific Case Study
    actual_yield = matched_data.loc[
        matched_data["Case Study"] == case_study, "Yield (Ton/HA)"
    ]
    simulation_yield = matched_data.loc[
        matched_data["Case Study"] == case_study, "Yield (tonne/ha)"
    ]
    # actual_water_use = matched_data.loc[matched_data['Case Study'] == case_study, 'Water Used (mm)']
    # simulation_water_use = matched_data.loc[matched_data['Case Study'] == case_study, 'Seasonal irrigation (mm)']

    # Calculate yield's RMSE and RMSE Percentage
    yield_rmse = sqrt(mean_squared_error(actual_yield, simulation_yield))
    yield_rmse_percentage = (yield_rmse / np.mean(actual_yield)) * 100

    # Calculate water use's RMSE and RMSE Percentage
    # water_used_rmse = sqrt(mean_squared_error(actual_water_use, simulation_water_use))
    # water_used_rmse_percentage = (water_used_rmse / np.mean(actual_water_use)) * 100

    # Append the results to rmse_df
    rmse_df = rmse_df.append(
        {
            "Case Study": case_study,
            "Yield RMSE": yield_rmse,
            "Yield RMSE Percentage": yield_rmse_percentage,
        },
        ignore_index=True,
    )


# 'Water Used RMSE': water_used_rmse,
# 'Water Used RMSE Percentage': water_used_rmse_percentage},

# Save rmse_df to an Excel file
rmse_df.to_excel(writer, index=False, sheet_name="RMSE_Percentage")

# Save the Excel file
writer.save()
writer.close()
