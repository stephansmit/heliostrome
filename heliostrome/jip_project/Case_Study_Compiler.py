from datetime import datetime
from heliostrome.models.location import Location
from heliostrome.models.climate import ClimateData
from aquacrop.core import IrrigationManagement
from aquacrop import Crop, InitialWaterContent, Soil, AquaCropModel
from heliostrome.data_collection.crops import get_crop_data
from heliostrome.models.aquacrop_results import (
    SimulationResult,
    CropGrowth,
    WaterFlux,
    WaterStorage,
)
from pydantic import BaseModel
from typing import List
from datetime import datetime
from datetime import date
import pandas as pd 
import altair as alt
from openpyxl import load_workbook #added!
import numpy as np
import time
import matplotlib.pyplot as plt

# Start the timer 
start_time = time.time()


# Load the Excel file
excel_file = excel_file = r'heliostrome\jip_project\results\Factors to run simulation.xlsx'  # Replace with the path to your Excel file
sheet_name = "Bangladesh Case Study"  # Replace with the name of the sheet containing the data
df_bangladesh = pd.read_excel(excel_file, sheet_name=sheet_name)

# Define a mapping of row names to row indices
row_mapping = {
    "Case Study": 0,
    "Longitude": 1,
    "Latitude": 2,
    "Start Date": 3,
    "End Date": 4,
    "Sowing Date": 5,
    "Soil Type": 6,
    "Irrigation Method": 7,
    "Initial Water Content": 8,
    "Crop Type": 9,
    "Yield": 10,
    "Water used": 11
}

# Initialize a dictionary to store the extracted rows with names
extracted_rows = {}

# Initialize an empty list for the Case Study Names
Casestudies = []

# Loop through the row names and extract the rows
for row_name, row_index in row_mapping.items():
    row_data = df_bangladesh.iloc[row_index, 1:].tolist()
    extracted_rows[row_name] = row_data

# Now, the extracted_rows dictionary contains the data with row names as keys
# You can access each list by its corresponding row name, e.g., extracted_rows["Longitude"]

alt.data_transformers.enable("default", max_rows=None)


#changes from here mostly concer date besides the obvious for loop. Dates from excel are already in datetime format, so change the line to compensate
#everything that has a value in the excel sheet is called independently from the code above with exracted_rows["name attribute"][casestudy index number]
#no optimasation yet, but I assume i can figure some cython methods or other stuff. just have to refresh my memory

final_df = pd.DataFrame(columns=['Season', 'crop Type', 'Harvest Date (YYYY/MM/DD)', 'Harvest Date (Step)', 'Yield (tonne/ha)', 'Seasonal irrigation (mm)'])
final_input_df = pd.DataFrame(columns=['Case Study','Latitude','Longitude','Start Date','End Date','Soil Type', 'Crop Type','Sowing Date','Irrigation Method','SMT', 'Init WC - WC Type','init WC - Value',  'Yield (Ton/HA)', 'Water Used (mm)'])
                                       
for i in range(len(extracted_rows["Case Study"])):
    location = Location(latitude=extracted_rows["Latitude"][i], longitude=extracted_rows["Longitude"][i])
    start_date = extracted_rows["Start Date"][i].date()
    end_date = extracted_rows["End Date"][i].date()
    
    climate_data = ClimateData(
        location=location,
        start_date=start_date,
        end_date=end_date,
    )

    climate_data.plot_data(y_axis='temp_air_max_c')

    soil = Soil(extracted_rows["Soil Type"][i])
    crop = get_crop_data(extracted_rows["Crop Type"][i])
    sowing_date = extracted_rows["Sowing Date"][i].strftime("%m/%d")
    crop = Crop(crop.Name, planting_date=sowing_date)
    irr_mngt = IrrigationManagement(irrigation_method=1, SMT=[extracted_rows["Irrigation Method"][i]]*4)
    InitWC = InitialWaterContent(wc_type = 'Pct', value=[extracted_rows["Initial Water Content"][i]])
    
    input_df = {'Case Study': [extracted_rows["Case Study"][i]],
                'Latitude' : [location.latitude],
                'Longitude' :[location.longitude],
                'Start Date' : [start_date],
                'End Date' : [end_date],
                'Soil Type' : [soil.Name], 
                'Crop Type' : [crop.Name],
                'Sowing Date' :[sowing_date],
                'Irrigation Method' : [irr_mngt.irrigation_method],
                'SMT' : [irr_mngt.SMT], 
                'Init WC - WC Type' :[InitWC.wc_type],
                'Init WC - Value': [InitWC.value],
                'Yield (Ton/HA)': [extracted_rows['Yield'][i]],
                'Water Used (mm)': [extracted_rows['Water used'][i]]}


    model = AquaCropModel(
        sim_start_time=start_date.strftime("%Y/%m/%d"),
        sim_end_time=end_date.strftime("%Y/%m/%d"),
        weather_df=climate_data.aquacrop_input,
        soil=soil,
        crop=crop,
        initial_water_content=InitWC,
        irrigation_management=irr_mngt,
    )
    model.run_model(till_termination=True)

    df = model.get_simulation_results()

    for x in range(len(df)):
        Casestudies.append(extracted_rows["Case Study"][i])

    final_df = final_df.append(df, ignore_index=True)
    input_df = pd.DataFrame(input_df)
    final_input_df = final_input_df.append(input_df, ignore_index=True)


    #time elapsed
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Iteration {i+1}: Elapsed time = {elapsed_time} seconds")
    start_time = end_time

    
final_df.insert(0, 'Case Study', Casestudies)

writer = pd.ExcelWriter(r'heliostrome\jip_project\results\test_results.xlsx', engine = 'openpyxl')
final_input_df.to_excel(writer, index=False, sheet_name= "Input Parameters")
final_df.to_excel(writer, index=False, sheet_name= "Output Results")

writer.close()

