import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt

# Read the Excel file
input_file_path = r'heliostrome\jip_project\results\test_results_moroccoWheat.xlsx'
output_file_path = r'heliostrome\jip_project\results\RMSE_Percentage_Morocco.xlsx'

# read input and out put input
input_df = pd.read_excel(input_file_path, sheet_name='Input Parameters')
output_df = pd.read_excel(input_file_path, sheet_name='Output Results')

# create an empty excel
writer = pd.ExcelWriter(output_file_path, engine='openpyxl')

# crate an empty DataFrame to store the output of RMSE
rmse_df = pd.DataFrame(columns=['Case Study', 'Yield RMSE', 'Yield RMSE Percentage', 'Water Used RMSE', 'Water Used RMSE Percentage'])

matched_data = pd.merge(output_df, input_df, on='Case Study', how='inner')

# 获取唯一的Case Study列表
case_studies = input_df['Case Study'].unique()

# 循环计算每个Case Study的RMSE和百分比误差
for case_study in case_studies:
    # 选择特定Case Study的数据
    actual_yield= matched_data.loc[matched_data['Case Study'] == case_study, 'Yield (Ton/HA)']
    simulation_yield = matched_data.loc[matched_data['Case Study'] == case_study, 'Yield (tonne/ha)']
    actual_wateruse= matched_data.loc[matched_data['Case Study'] == case_study, 'Water Used (mm)']
    simulation_wateruse= matched_data.loc[matched_data['Case Study'] == case_study, 'Seasonal irrigation (mm)']

    # yield's RMSE and RMSE Percentage
    yield_rmse = sqrt(mean_squared_error(actual_yield, simulation_yield))
    yield_rmse_percentage = (yield_rmse / np.mean(actual_yield)) * 100
    
    # wateruse's RMSE and RMSE Percentage
    water_used_rmse = sqrt(mean_squared_error(actual_wateruse, simulation_wateruse))
    water_used_rmse_percentage = (water_used_rmse / np.mean(actual_wateruse)) * 100
    
    # 将结果添加到rmse_df中
    rmse_df = rmse_df.append({'Case Study': case_study,
                              'Yield RMSE': yield_rmse,
                              'Yield RMSE Percentage': yield_rmse_percentage,
                              'Water Used RMSE': water_used_rmse,
                              'Water Used RMSE Percentage': water_used_rmse_percentage},
                             ignore_index=True)

# 将rmse_df保存到Excel文件中
rmse_df.to_excel(writer, index=False, sheet_name='RMSE_Percentage')

# 保存Excel文件
writer.save()
writer.close()