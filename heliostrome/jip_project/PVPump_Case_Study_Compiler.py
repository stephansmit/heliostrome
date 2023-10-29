import os
from pvlib.iotools import get_pvgis_tmy
import pvpumpingsystem.pvgeneration as pvgen
import pvpumpingsystem.pump as pp
import pvpumpingsystem.mppt as mppt
import pvpumpingsystem.pipenetwork as pn
import pvpumpingsystem.pvpumpsystem as pvps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pvlib import pvsystem
from pvpumpingsystem.pump import Pump
import heliostrome
import altair as alt
from modules.Load_excel import factors_to_run
from modules.waterflux_extraction import *
from modules.Pump_module import convert_Qlpm, pump_solar_voltage_current_plot,pump_solar_voltage_power_plot
from heliostrome.simulation.curve_plotting import get_iv_curve_pump, get_iv_curve_solar
from openpyxl import load_workbook #added!

main_folder = os.path.dirname(heliostrome.__file__)  # .replace("\\","/")

#Extracting the data from the factors to run simulation file excel
# Load the Excel file
sheet_name = "Case study pump"  # Replace with the name of the sheet containing the data
extracted_rows = factors_to_run(sheet_name) # You can access each list by its corresponding row name, e.g., extracted_rows["Longitude"]

alt.data_transformers.enable("default", max_rows=None)

#Initialise emtpy dataframe from results
PVPump_results_df = pd.DataFrame()

#Looping through all the case studies to simulate different aquacrop inputs as well as pump inputs
#for i in range(len(extracted_rows["Case Study"])):
#for i in range(len(extracted_rows['Case Study'])):
for i in range(2):
    latitude = extracted_rows["Latitude"][i]
    longitude = extracted_rows["Longitude"][i]
    name = extracted_rows['Case Study'][i]
    tz = 'UTC'

    data, months_selected, inputs, metadata = get_pvgis_tmy(latitude, longitude, outputformat='csv', usehorizon=True, userhorizon=None, startyear=None, endyear=None, map_variables=True, url='https://re.jrc.ec.europa.eu/api/', timeout=30)

    inputs['Name'] = name
    inputs['TZ'] = tz
    inputs['altitude'] = inputs['elevation']
    pvgen1 = pvgen.PVGeneration(
        # Weather data path
        weather_data_and_metadata = {'weather_data': data, 'weather_metadata': inputs},
        pv_module_name=extracted_rows['PV Module Name'][i],  # Name of pv module to model
        modules_per_string=extracted_rows['Modules Per String'][i],
        strings_in_parallel=extracted_rows['Strings in Parallel'][i],
        orientation_strategy="south_at_latitude_tilt",  # or 'flat' or None
    )

    mppt1 = mppt.MPPT(efficiency=0.96, idname="PCA-120-BLS-M2")

    pump_file_string = "data/pump/" + extracted_rows['Pump Name'][i] + ".txt"
    pump_file = os.path.join(main_folder, pump_file_string)

    pump_sunpump = pp.Pump(path=pump_file)

    pipes1 = pn.PipeNetwork(
        h_stat=extracted_rows['Static Head'][i],  # static head [m]
        l_tot=extracted_rows['Total Length of Pipes'][i],  # length of pipes [m]
        diam=extracted_rows['Diameter of Pipes'][i],  # diameter [m]
        material=extracted_rows['Material of Pipes'][i],
    )

    pvps1 = pvps.PVPumpSystem(
        pvgen1,
        pump_sunpump,
        coupling="direct",  # to adapt: 'mppt' or 'direct',
        mppt=mppt1,
        pipes=pipes1,
    )

    voltage_pump, current_pump = get_iv_curve_pump(pvps1.motorpump, pipes1.h_stat)
    voltage_solar, current_solar = get_iv_curve_solar(pvps1.pvgeneration.system, 1000, 25)

    pump_df = pd.DataFrame(voltage_pump, columns = ['Voltage Pump'])
    pump_df['Current Pump'] = current_pump
    pump_df['Case Study'] = [extracted_rows["Case Study"][i] for _ in range(len(pump_df))]
    solar_df = pd.DataFrame(voltage_solar, columns = ['Voltage Solar'])
    solar_df['Current Solar'] = current_solar
    solar_df['Case Study'] = [extracted_rows["Case Study"][i] for _ in range(len(solar_df))]
   
    power_pump = voltage_pump * current_pump
    power_solar = voltage_solar * current_solar

    #pump_solar_voltage_current_plot(voltage_pump,current_pump,voltage_solar,current_solar)

    #pump_solar_voltage_power_plot(voltage_pump,power_pump,voltage_solar,power_solar)

    pvps1.run_model()

    efficiency = pvps1.calc_efficiency()

    #pump_setup = str(extracted_rows['Pump Name'][i]) + ' (' + str(extracted_rows['Modules Per String'][i]) + ',' + str(extracted_rows['Strings in Parallel'][i]) + ')'
    pump_setup = 'Pump ' + str(i+1)
    daily_data = convert_Qlpm(pvps1.flow,field_size=extracted_rows['Area of Field'][0])
   
    PVPump_results_df[pump_setup] = daily_data['Water_depth_mm']
   

PVPump_results_df['Date'] = daily_data['Date']

PVPump_results_df['Date'] = pd.to_datetime(PVPump_results_df['Date'])

PVPump_results_df = PVPump_results_df.set_index('Date')

sim_start_year = 2005
sim_end_year = 2016

#########Run the following code if you just want 1 years worth of data all in the sim_start_year
PVPump_results_df.index = PVPump_results_df.index.map(lambda x: x.replace(year=sim_start_year))


PVPump_results_df.index = pd.to_datetime(PVPump_results_df.index)
PVPump_results_df = PVPump_results_df.sort_index()

writer = pd.ExcelWriter(r'heliostrome\jip_project\results\PVPUmp_Data.xlsx', engine = 'openpyxl')
    
# Write each column to a new sheet
for column_name in PVPump_results_df.columns:
    PVPump_subset_df = pd.DataFrame()
    PVPump_subset_df = PVPump_results_df[[column_name]]
    PVPump_subset_df = PVPump_subset_df.rename(columns={column_name: 'Pump'})
    PVPump_subset_df.index = PVPump_results_df.index
    PVPump_subset_df.to_excel(writer, sheet_name=column_name, index=True)
    date_format = 'yyyy-mm-dd'  # You can change this format to suit your needs
    writer.sheets[column_name].column_dimensions['A'].number_format = date_format

writer.close()


#########Run the following code if you just want multiple years worth of data in the yearly range (10 years)

# PVPump_full_df = pd.DataFrame(columns=PVPump_results_df.columns)
# for year in range(sim_start_year, sim_end_year + 1):
#     # Duplicate the original DataFrame and update the 'Date' column
#     current_year_df = PVPump_results_df.copy()
#     current_year_df.index = current_year_df.index.map(lambda x: x.replace(year=year))

#     # Append the current year's data to the repeated DataFrame
#     PVPump_full_df = PVPump_full_df.append(current_year_df, ignore_index=False)


# PVPump_full_df = PVPump_full_df.set_index(pd.to_datetime(PVPump_full_df.index))
# PVPump_results_df = PVPump_results_df.sort_index()


# writer = pd.ExcelWriter(r'heliostrome\jip_project\results\PVPUmp_Data.xlsx', engine = 'openpyxl')

# # Write each column to a new sheet
# for column_name in PVPump_full_df.columns:
#     PVPump_subset_df = pd.DataFrame()
#     PVPump_subset_df = PVPump_full_df[[column_name]]
#     PVPump_subset_df = PVPump_subset_df.rename(columns={column_name: 'Pump'})
#     PVPump_subset_df.index = PVPump_full_df.index
#     PVPump_subset_df.to_excel(writer, sheet_name=column_name, index=True)
#     date_format = 'yyyy-mm-dd'  # You can change this format to suit your needs
#     writer.sheets[column_name].column_dimensions['A'].number_format = date_format

# writer.close()


