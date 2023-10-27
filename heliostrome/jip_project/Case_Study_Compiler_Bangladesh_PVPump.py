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
from modules.Pump_module import convert_Qlpm

def get_iv_curve_pump(pump: Pump, static_head: float):
    load_fctI, intervalsVH = pump.functIforVH()
    voltage_vec = np.arange(*intervalsVH['V'](static_head))
    current_vec = load_fctI(voltage_vec, static_head, error_raising=False)
    return voltage_vec, current_vec

def get_iv_curve_solar(system: pvsystem, effective_irradiance: float, temp_cell: float):
    IL, I0, Rs, Rsh, nNsVth = system.calcparams_cec(effective_irradiance, temp_cell)
    n_modules_series = system.arrays[0].modules_per_string
    n_modules_parallel = system.arrays[0].strings

    #scale the resistances and currents for the system configuration
    if (n_modules_series, n_modules_parallel) != (1, 1):
        IL = n_modules_series * IL
        I0 = n_modules_parallel * I0
        nNsVth = nNsVth * n_modules_series
        Rs = (n_modules_series / n_modules_parallel) * Rs
        Rsh = (n_modules_series / n_modules_parallel) * Rsh
    
    SDE_params = {
        'photocurrent': IL,
        'saturation_current': I0,
        'resistance_series': Rs,
        'resistance_shunt': Rsh,
        'nNsVth': nNsVth
    }

    curve_info = system.singlediode(**SDE_params)
    voltage_vec = np.linspace(0., curve_info['v_oc'], 100)
    current_vec = pvsystem.i_from_v(voltage=voltage_vec, method='lambertw', **SDE_params)
    return voltage_vec, current_vec


main_folder = os.path.dirname(heliostrome.__file__)  # .replace("\\","/")

#Extracting the data from the factors to run simulation file excel

# Load the Excel file
sheet_name = "Case study pump"  # Replace with the name of the sheet containing the data
extracted_rows = factors_to_run(sheet_name) # You can access each list by its corresponding row name, e.g., extracted_rows["Longitude"]

# Initialize an empty list for the Case Study Names
Casestudies = []

alt.data_transformers.enable("default", max_rows=None)

#for i in range(len(extracted_rows['Case Study'])):

PVPump_results_df = pd.DataFrame()

# for i in range(len(extracted_rows["Case Study"])):

for i in range(0,3):

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
   
    # writer = pd.ExcelWriter(r'heliostrome\jip_project\results\test_results_Bangladesh.xlsx', engine = 'openpyxl')
    # pump_df.to_excel(writer, index=False, sheet_name= "Pump Outputs")
    # solar_df.to_excel(writer, index=False, sheet_name= "Solar Outputs")
    
    # writer.close()

    power_pump = voltage_pump * current_pump
    power_solar = voltage_solar * current_solar

    #Voltage versus Current Plot
    # fig, ax = plt.subplots()
    # ax.plot(voltage_pump, current_pump, label="Pump")
    # ax.plot(voltage_solar, current_solar, label="Solar")
    # ax.set_xlabel("Voltage [V]")
    # ax.set_ylabel("Current [A]")
    # ax.legend()
    # plt.show()

    #Voltage versus Power Plot
    # fig, ax = plt.subplots()
    # ax.plot(voltage_pump, power_pump, label="Pump")
    # ax.plot(voltage_solar, power_solar, label="Solar")
    # ax.set_xlabel("Voltage [V]")
    # ax.set_ylabel("Power [W]")
    # ax.legend()
    # plt.show()

    pvps1.run_model()

    pvps1.calc_efficiency()

    #print(pvps1)
   # print("\ntotal water pumped in the year = ", pvps1.flow.Qlpm.sum() * 60)
    # print(
    #     "\ndetails on second day of pumping = \n", pvps1.flow[24:200]
    # )  #pvgen1.plot_model()

    # pvps1.flow.Qlpm.plot()
    # plt.show()
    #plt.plot(, pvps.flow.Qlpm)

    #monthly_data = pvps1.flow.groupby(pvps1.flow.index.month).sum()
    daily_data = pvps1.flow.groupby(pvps1.flow.index.date).mean()
    pump_setup = str(extracted_rows['Pump Name'][i]) + ' (' + str(extracted_rows['Modules Per String'][i]) + ',' + str(extracted_rows['Strings in Parallel'][i]) + ')'
    
    daily_data = convert_Qlpm(daily_data,field_size=extracted_rows['Area of Field'][0])
    #PVPump_results_df.index = daily_data.index
    PVPump_results_df[pump_setup] = daily_data['Water_depth_mm']

    

PVPump_results_df['Date'] = daily_data['Date']


# Plot multiple columns on the same plot
plt.figure(figsize=(10, 6))  # Optional: Adjust the figure size

def pumpname(pumpno, modno,strno):
    pumpn = str(extracted_rows['Pump Name'][pumpno]) + ' (' + str(extracted_rows['Modules Per String'][modno]) + ',' + str(extracted_rows['Strings in Parallel'][strno]) + ')'

    return pumpn


############## Getting Aquacrop Bangladesh Data -> Water Per Month Needed
clean_excel_file(r"heliostrome/jip_project/results/WaterFlux_Bangladesh.xlsx",r"heliostrome/jip_project/results/cleaned_WaterFlux_Bangladesh.xlsx",start_date=extracted_rows['Start Date'][0])

results_excel_file = r'heliostrome\jip_project\results\cleaned_WaterFlux_Bangladesh.xlsx'
aquacrop_results = pd.read_excel(results_excel_file)

PVPump_results_df['Aquacrop Daily Irrigation'] = aquacrop_results['IrrDay']

print(PVPump_results_df)

# Plot Column1
plt.plot(PVPump_results_df['Date'], PVPump_results_df.iloc[:,1], label=pumpname(0,0,0))

# Plot Column2
plt.plot(PVPump_results_df['Date'], PVPump_results_df.iloc[:,2], label=pumpname(0,1,1))

# Plot Column3
plt.plot(PVPump_results_df['Date'], PVPump_results_df.iloc[:,3], label=pumpname(0,2,2))

# Plot Column4
plt.plot(PVPump_results_df['Date'], PVPump_results_df['Aquacrop Daily Irrigation'], label="Aquacrop Results")

# Customize the plot
plt.title('Variation of ability to pump water over a year in Bangladesh Columns')
plt.xlabel('Date')
plt.ylabel('mm per Day')
plt.legend()

# Show the plot
plt.show()


#############################
# extract_rows(r"heliostrome/jip_project/results/WaterFlux_Bangladesh.xlsx",r"heliostrome/jip_project/results/analysed_WaterFlux_Bangladesh.xlsx",start_date=extracted_rows['Start Date'][0])
# result = min_max_irrigation(r"heliostrome/jip_project/results/WaterFlux_Bangladesh.xlsx", field_size=extracted_rows['Area of Field'][0])

# print(result)
