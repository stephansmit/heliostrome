import numpy as np
import pandas as pd

# Read the Excel file
excel_file = r"heliostrome\jip_project\results\test_results_northeastCHINA.xlsx"
sheet_name = "Output Results"
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Group the data by 'Case Study' and calculate the average 'Yield (tonne/ha)'
average_yields = df.groupby("Case Study")["Yield (tonne/ha)"].mean().reset_index()
experimental_yields = pd.read_excel(excel_file, sheet_name="Input Parameters")

# Extract the 'Yield (tonne/ha)' values as lists
average_yields_list = average_yields["Yield (tonne/ha)"].tolist()
experimental_yields_list = experimental_yields["Yield (Ton/HA)"].tolist()


def calculate_rmse_percentage(average_yields_list, experimental_yields_list):
    if len(average_yields_list) != len(experimental_yields_list):
        raise ValueError("Input lists must have the same length")

    squared_errors = [
        (actual - predicted) ** 2
        for actual, predicted in zip(average_yields_list, experimental_yields_list)
    ]
    mean_squared_error = np.mean(squared_errors)
    rmse = np.sqrt(mean_squared_error)

    # Calculate the range of the observed data
    # data_range = max(average_yields_list) - min(average_yields_list)

    denominator = np.mean(average_yields_list)

    # Calculate RMSE as a percentage of the data range
    rmse_percentage = (rmse / denominator) * 100

    return rmse_percentage


rmse_percentage = calculate_rmse_percentage(
    average_yields_list, experimental_yields_list
)
print("RMSE Percentage:", rmse_percentage)
