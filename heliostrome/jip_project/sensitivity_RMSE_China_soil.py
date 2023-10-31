import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt

input_file_path = r'heliostrome\jip_project\results\sensitivity_China_soil.xlsx'
output_file_path = r'heliostrome\jip_project\results\sensitivity_RMSE_China_soil.xlsx'

soil_types = [
    "Clay",
    "ClayLoam",
    "Loam",
    "LoamySand",
    "Sand",
    "SandyClay",
    "SandyClayLoam",
    "SandyLoam",
    "Silt",
    "SiltClayLoam",
    "SiltLoam",
    "SiltClay",
    "Paddy",
    "ac_TunisLocal",
]

# read all input and output tables
input_sheet_names = [f"{soil_type}_Input_Parameters" for soil_type in soil_types]
output_sheet_names = [f"{soil_type}_Output_Results" for soil_type in soil_types]

# create an empty excel
writer = pd.ExcelWriter(output_file_path, engine='openpyxl')

# crate an empty DataFrame to store the output of RMSE
rmse_df = pd.DataFrame(columns=['soil type', 'Yield RMSE', 'Yield RMSE Percentage'])

# 
for input_sheet_name, output_sheet_name in zip(input_sheet_names, output_sheet_names):
    
    input_df = pd.read_excel(input_file_path, sheet_name=input_sheet_name)
    output_df = pd.read_excel(input_file_path, sheet_name=output_sheet_name)

    # merge the two table
    matched_data = pd.merge(output_df, input_df, on='Case Study', how='inner')
    
    # Yield RMSE
    yield_rmse = sqrt(mean_squared_error(matched_data['Yield (tonne/ha)'], matched_data['Yield (Ton/HA)']))
    
    # # Water Used RMSE
    # water_used_rmse = sqrt(mean_squared_error(matched_data['Seasonal irrigation (mm)'], matched_data['Water Used (mm)']))
    
    # Yield RMSE Percentage
    yield_rmse_percentage = (yield_rmse / matched_data['Yield (Ton/HA)'].mean()) * 100
    
    # Water Used RMSE Percentage
    # water_used_rmse_percentage = (water_used_rmse / matched_data['Water Used (mm)'].mean()) * 100
    
    soil_type = input_df['Soil Type'].iloc[0]

    # ouput
    df_to_append = pd.DataFrame({'soil type': soil_type, 'Yield RMSE': yield_rmse, 'Yield RMSE Percentage': yield_rmse_percentage}, index=[0])
    rmse_df = pd.concat([rmse_df, df_to_append], ignore_index=True)

# 将 RMSE 结果保存到新 Excel 文件
rmse_df.to_excel(writer, index=False, sheet_name='RMSE Results')

# 关闭 Excel writer
writer.save()
