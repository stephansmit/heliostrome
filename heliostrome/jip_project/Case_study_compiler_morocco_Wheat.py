from datetime import datetime
from heliostrome.models.location import Location
from heliostrome.models.climate import ClimateData
from aquacrop.core import IrrigationManagement
from aquacrop.entities.irrigationManagement import IrrMngtStruct
from aquacrop import Crop, InitialWaterContent, Soil, AquaCropModel, FieldMngt
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
from openpyxl import load_workbook
import numpy as np
import time
import matplotlib.pyplot as plt
from modules.irrigation_schedule_morrocco_wheat import IRRschedule
from modules.Load_excel import factors_to_run

# Start the timer 
start_time = time.time()

sheet_name = "Morocco Wheat Case Study"  # Replace with the name of the sheet containing the data
extracted_rows = factors_to_run(sheet_name)


# Initialize an empty list for the Case Study Names
Casestudies = []

alt.data_transformers.enable("default", max_rows=None)

final_df = pd.DataFrame(columns=['Season', 'crop Type', 'Harvest Date (YYYY/MM/DD)', 'Harvest Date (Step)', 'Yield (tonne/ha)', 'Seasonal irrigation (mm)'])
final_input_df = pd.DataFrame(columns=['Case Study','Latitude','Longitude','Start Date','End Date','Soil Type', 'Crop Type','Sowing Date','Irrigation Method','SMT', 'Init WC - WC Type','init WC - Value',  'Yield (Ton/HA)', 'Water Used (mm)'])

#waterflux excel file
writer1 = pd.ExcelWriter(r'heliostrome\jip_project\results\WaterFlux_moroccoWheat.xlsx', engine='openpyxl')


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

    soil = Soil("ClayLoam")
    crop = get_crop_data("Wheat")
    sowing_date = extracted_rows["Sowing Date"][i].strftime("%m/%d")
    crop = Crop(crop.Name, planting_date=sowing_date)
    
    print(IRRschedule(i), sowing_date, start_date, end_date)

    irr_mngt = IrrigationManagement(irrigation_method=3, Schedule = IRRschedule(i, B = 10), MaxIrr = 100)
    InitWC = InitialWaterContent(value = ['FC'])
    
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
        field_management= FieldMngt(bunds=True, z_bund=0.12, bund_water=30),

        )
    
    model.run_model(till_termination=True)
    
    #end simulation run


    ####data storage lines-----------------------------------------------------------
    
    df = model.get_simulation_results()

    for x in range(len(df)):
        Casestudies.append(extracted_rows["Case Study"][i])
    
    # Append data to final_df and final_input_df using concat
    final_df = pd.concat([final_df, df], ignore_index=True)
        #final_df = final_df.append(df, ignore_index=True)

    input_df = pd.DataFrame(input_df)

    final_input_df = pd.concat([final_input_df, pd.DataFrame(input_df)], ignore_index=True)
    #final_input_df = final_input_df.append(input_df, ignore_index=True)

    #waterflux related lines
    water_flux = model._outputs.water_flux
    sheet_name = f"{extracted_rows['Case Study'][i]}"
    water_flux.to_excel(writer1, index=False, sheet_name=sheet_name)





    #time elapsed
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Iteration {i+1}: Elapsed time = {elapsed_time} seconds")
    start_time = end_time



writer1.close()

# Insert the 'Case Study' column to final_df
final_df.insert(0, 'Case Study', Casestudies)

writer = pd.ExcelWriter(r'heliostrome\jip_project\results\test_results_moroccoWheat.xlsx', engine = 'openpyxl')
final_input_df.to_excel(writer, index=False, sheet_name= "Input Parameters")
final_df.to_excel(writer, index=False, sheet_name= "Output Results")


writer.close()


