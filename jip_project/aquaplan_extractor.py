import pandas as pd
import numpy as np

def aquaplan_data():
    A1_df = pd.read_csv(r'heliostrome\jip_project\results\A1-Northern_China.csv')
    A2_df = pd.read_csv(r'heliostrome\jip_project\results\A2-Norhtern_China.csv')
    B1_df = pd.read_csv(r'heliostrome\jip_project\results\B1-Northern_China.csv')
    B2_df = pd.read_csv(r'heliostrome\jip_project\results\B2-Northern_China.csv')
    C1_df = pd.read_csv(r'heliostrome\jip_project\results\C1-Northern_China.csv')
    C2_df = pd.read_csv(r'heliostrome\jip_project\results\C2-Northern_China.csv')

    # Create a new DataFrame by concatenating the selected columns
    aquaplan_df = pd.concat([
        A1_df['Yield (t/ha)'],
        A2_df['Yield (t/ha)'],
        B1_df['Yield (t/ha)'],
        B2_df['Yield (t/ha)'],
        C1_df['rainfed_yield (tonne/ha)'],
        C2_df['rainfed_yield (tonne/ha)']
    ], axis=1)

    # Rename columns for clarity
    case_study = ['A1', 'A2', 'B1', 'B2','C1','C2']
    aquaplan_df.columns = case_study

    # Sort each column in ascending order
    for column in aquaplan_df.columns:
        aquaplan_df[column] = aquaplan_df[column].sort_values().values

    # Calculate the average of the last 4 rows for each column in aquaplan_df
    average_first_4_rows = aquaplan_df.head(4).mean()

    # Create a new DataFrame with the averages
    averages_df = pd.DataFrame({'Average_Yield': average_first_4_rows})
    averages_df['Case Study'] = case_study

    # Print the new DataFrame
    return averages_df

result = aquaplan_data()
print(result)
