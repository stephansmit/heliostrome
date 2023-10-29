from modules.waterflux_extraction import *
from modules.Pump_module import *
import pandas as pd



waterfluxexcelpath = r'heliostrome\jip_project\results\cleaned_WaterFlux_Bangladesh.xlsx'
pump_df_path = r'heliostrome\jip_project\results\PVPUmp_Data.xlsx'

merged_df = pump_compatibility(waterfluxexcelpath,pump_df_path)

waterflux_df = pd.read_excel(waterfluxexcelpath)
pump_df = pd.read_excel(pump_df_path)

mpe_indiv, mpe_df_avg = mean_percentage_error(merged_df,'IrrDay',merged_df,'Pump 1')

