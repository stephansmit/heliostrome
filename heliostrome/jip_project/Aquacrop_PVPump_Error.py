from modules.waterflux_extraction import *
from modules.Pump_module import *
import pandas as pd



waterfluxexcelpath = r'heliostrome\jip_project\results\cleaned_WaterFlux_Bangladesh.xlsx'
pump_df_path = r'heliostrome\jip_project\results\PVPUmp_Data.xlsx'
output_file_path = 'heliostrome\\jip_project\\results\\pump_compatibility\\'
 #csv location

#merged_df = pump_compatibility(waterfluxexcelpath, pump_df_path, output_file_path)

###CSV Inputs
mpe_df_avg_list = []

for i in range (16):
    csv_pump_file = r'heliostrome\jip_project\results\pump_compatibility\_Pump ' + str(i+1) + '.csv'
    df = pd.read_csv(csv_pump_file)
    print(df)
    mpe_indiv, mpe_df_avg = mean_percentage_error(df,'Pump',df,'Pump')

    mpe_df_avg_list.append(mpe_df_avg)
    print(mpe_indiv)
   
print(mpe_df_avg_list)

# waterflux_df = pd.read_excel(waterfluxexcelpath)
# pump_df = pd.read_excel(pump_df_path)



