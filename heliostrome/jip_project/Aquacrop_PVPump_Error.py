from modules.waterflux_extraction import *
from modules.Pump_module import *
import pandas as pd

#Import Aquacrop outputs from excel file (IrrDay converted to desired timestep)

# #Crop Results
# aquacrop_excel_results = r'heliostrome\jip_project\results\test_results_Bangladesh.xlsx'
# aquacrop_results = pd.read_excel(aquacrop_excel_results, sheet_name= 'Output Results')
# year_range = 12
# yearly_aquacrop_list = [aquacrop_results[i:i + year_range] for i in range(0, len(aquacrop_results), year_range)]





#yearly_waterflux_list = [waterflux_results[waterflux_results['season_counter'] == i] for i in range(0,year_range)]

#pd.set_option('display.max_rows', None)

#Import PVPump outputs from excel file (Qlpm converted to desired timestep)
#pump_excel_results = r''
#pump_results = pd.read_excel(pump_excel_results)


#Option 1 - Plot timestep on X, flow rate on Y


#Option 2 - Compute error (purely x1-x2) between 2 variables if delta is too small to see on graph







x = pump_compatibility(r"heliostrome/jip_project/results/weekly_WaterFlux_Bangladesh.xlsx",r"heliostrome/jip_project/results/weekly_Pump_Data.xlsx")
print(x)