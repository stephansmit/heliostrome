import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt

# 定义输入和输出文件的路径
input_file_path = r'heliostrome\jip_project\results\sensitivity_Morocco_soil.xlsx'
output_file_path = r'heliostrome\jip_project\results\sensitivity_RMSE_Morocco_soil.xlsx'

# 定义所使用的土壤类型列表
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

# 获取所有输入和输出表的名称
input_sheet_names = [f"{soil_type}_Input_Parameters" for soil_type in soil_types]
output_sheet_names = [f"{soil_type}_Output_Results" for soil_type in soil_types]

# 创建一个新的 Excel writer 来保存 RMSE 结果
writer = pd.ExcelWriter(output_file_path, engine='openpyxl')

# 创建一个空的 DataFrame 用于保存 RMSE 结果
rmse_df = pd.DataFrame(columns=['soil type', 'RMSE'])

# 循环计算 RMSE 并保存到新 Excel 文件
for input_sheet_name, output_sheet_name in zip(input_sheet_names, output_sheet_names):
    # 读取输入和输出表的数据
    input_df = pd.read_excel(input_file_path, sheet_name=input_sheet_name)
    output_df = pd.read_excel(input_file_path, sheet_name=output_sheet_name)

    # 匹配 'Case Study' 列并计算 RMSE
    matched_data = pd.merge(output_df, input_df, on='Case Study', how='inner')
    rmse = sqrt(mean_squared_error(matched_data['Yield (tonne/ha)'], matched_data['Yield (Ton/HA)']))

    # 获取土壤类型名称
    soil_type = input_df['Soil Type'].iloc[0]

    # 将 RMSE 结果添加到 rmse_df 中
    rmse_df = rmse_df.append({'soil type': soil_type, 'RMSE': rmse}, ignore_index=True)

# 将 RMSE 结果保存到新 Excel 文件
rmse_df.to_excel(writer, index=False, sheet_name='RMSE Results')

# 关闭 Excel writer
writer.save()
