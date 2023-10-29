from modules.waterflux_extraction import *
from modules.Pump_module import *
import pandas as pd



waterfluxexcelpath = r'heliostrome\jip_project\results\cleaned_WaterFlux_Bangladesh.xlsx'

pump_df_path = r'heliostrome\jip_project\results\PVPUmp_Data.xlsx'

pump_compatibility(waterfluxexcelpath,pump_df_path)
