from modules.waterflux_extraction import *
from modules.Pump_module import *
import pandas as pd

resample_and_save_weekly(r'heliostrome\jip_project\results\PVPUmp_Data.xlsx',r'heliostrome\jip_project\results\weekly_Pump_Data.xlsx')

waterfluxexcelpath = r'heliostrome\jip_project\results\weekly_WaterFlux_Bangladesh.xlsx'
pump_df_path = r'heliostrome\jip_project\results\weekly_Pump_Data.xlsx'

pump_compatibility(waterfluxexcelpath,pump_df_path)
