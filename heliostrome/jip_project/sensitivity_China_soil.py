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

sheet_name = "Northeast China Case Study"  # Replace with the name of the sheet containing the data
extracted_rows = factors_to_run(sheet_name)

# Define the list of soil types
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

# Create an Excel writer to save the results
writer = pd.ExcelWriter(
    r"heliostrome\jip_project\results\sensitivity_China_soil.xlsx", engine="openpyxl"
)


alt.data_transformers.enable("default", max_rows=None)


for soil_type in soil_types:
    final_input_df = pd.DataFrame(
        columns=[
            "Case Study",
            "Latitude",
            "Longitude",
            "Start Date",
            "End Date",
            "Soil Type",
            "Crop Type",
            "Sowing Date",
            "Irrigation Method",
            "SMT",
            "Init WC - WC Type",
            "init WC - Value",
            "Yield (Ton/HA)",
            "Water Used (mm)",
        ]
    )
    final_df = pd.DataFrame(
        columns=[
            "Season",
            "crop Type",
            "Harvest Date (YYYY/MM/DD)",
            "Harvest Date (Step)",
            "Yield (tonne/ha)",
            "Seasonal irrigation (mm)",
        ]
    )
    Casestudies = []

    for i in range(4):
        location = Location(latitude=40, longitude=114)
        start_date = extracted_rows["Start Date"][i].date()
        end_date = extracted_rows["End Date"][i].date()

        climate_data = ClimateData(
            location=location,
            start_date=start_date,
            end_date=end_date,
        )

        climate_data.plot_data(y_axis="temp_air_max_c")
        print(extracted_rows["Sowing Date"][i])
        soil = Soil(soil_type)
        crop = get_crop_data(extracted_rows["Crop Type"][i])
        sowing_date = extracted_rows["Sowing Date"][i].strftime("%m/%d")
        crop = Crop(crop.Name, planting_date=sowing_date)
        irr_mngt = IrrigationManagement(
            irrigation_method=1, SMT=[extracted_rows["Irrigation Method"][i]] * 4
        )
        InitWC = InitialWaterContent(
            wc_type="Pct", value=[extracted_rows["Initial Water Content"][i]]
        )

        input_df = {
            "Case Study": [extracted_rows["Case Study"][i]],
            "Latitude": [location.latitude],
            "Longitude": [location.longitude],
            "Start Date": [start_date],
            "End Date": [end_date],
            "Soil Type": [soil.Name],
            "Crop Type": [crop.Name],
            "Sowing Date": [sowing_date],
            "Irrigation Method": [irr_mngt.irrigation_method],
            "SMT": [irr_mngt.SMT],
            "Init WC - WC Type": [InitWC.wc_type],
            "Init WC - Value": [InitWC.value],
            "Yield (Ton/HA)": [extracted_rows["Yield"][i]],
            "Water Used (mm)": [extracted_rows["Water used"][i]],
        }

        model = AquaCropModel(
            sim_start_time=start_date.strftime("%Y/%m/%d"),
            sim_end_time=end_date.strftime("%Y/%m/%d"),
            weather_df=climate_data.aquacrop_input,
            soil=soil,
            crop=crop,
            initial_water_content=InitWC,
            irrigation_management=irr_mngt,
            field_management=FieldMngt(
                mulches=extracted_rows["Mulches"][i], mulch_pct=100
            ),
        )

        model.run_model(till_termination=True)

        df = model.get_simulation_results()

        for x in range(len(df)):
            Casestudies.append(extracted_rows["Case Study"][i])

        final_df = pd.concat([final_df, df], ignore_index=True)
        input_df = pd.DataFrame(input_df)
        final_input_df = pd.concat(
            [final_input_df, pd.DataFrame(input_df)], ignore_index=True
        )

        # waterflux related lines
        water_flux = model._outputs.water_flux
        sheet_name = f"{extracted_rows['Case Study'][i]}"

        # time elapsed
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Iteration {i+1}: Elapsed time = {elapsed_time} seconds")
        start_time = end_time

    for i in range(2):
        location = Location(latitude=40, longitude=114)
        start_date = extracted_rows["Start Date"][i + 4].date()
        end_date = extracted_rows["End Date"][i + 4].date()

        climate_data = ClimateData(
            location=location,
            start_date=start_date,
            end_date=end_date,
        )

        climate_data.plot_data(y_axis="temp_air_max_c")

        soil = Soil(soil_type)
        crop = get_crop_data(extracted_rows["Crop Type"][i + 4])
        sowing_date = extracted_rows["Sowing Date"][i + 4].strftime("%m/%d")
        crop = Crop(crop.Name, planting_date=sowing_date)
        irr_mngt = IrrigationManagement(irrigation_method=0)
        InitWC = InitialWaterContent(
            wc_type="Pct", value=[extracted_rows["Initial Water Content"][i + 4]]
        )

        input_df = {
            "Case Study": [extracted_rows["Case Study"][i + 4]],
            "Latitude": [location.latitude],
            "Longitude": [location.longitude],
            "Start Date": [start_date],
            "End Date": [end_date],
            "Soil Type": [soil.Name],
            "Crop Type": [crop.Name],
            "Sowing Date": [sowing_date],
            "Irrigation Method": [irr_mngt.irrigation_method],
            "SMT": [irr_mngt.SMT],
            "Init WC - WC Type": [InitWC.wc_type],
            "Init WC - Value": [InitWC.value],
            "Yield (Ton/HA)": [extracted_rows["Yield"][i + 4]],
            "Water Used (mm)": [extracted_rows["Water used"][i + 4]],
        }

        model = AquaCropModel(
            sim_start_time=start_date.strftime("%Y/%m/%d"),
            sim_end_time=end_date.strftime("%Y/%m/%d"),
            weather_df=climate_data.aquacrop_input,
            soil=soil,
            crop=crop,
            initial_water_content=InitWC,
            irrigation_management=irr_mngt,
            field_management=FieldMngt(
                mulches=extracted_rows["Mulches"][i + 4], mulch_pct=100
            ),
        )

        model.run_model(till_termination=True)

        df = model.get_simulation_results()

        for x in range(len(df)):
            Casestudies.append(extracted_rows["Case Study"][i + 4])

        final_df = pd.concat([final_df, df], ignore_index=True)
        input_df = pd.DataFrame(input_df)
        final_input_df = pd.concat(
            [final_input_df, pd.DataFrame(input_df)], ignore_index=True
        )

        # waterflux related lines
        water_flux = model._outputs.water_flux
        sheet_name = f"{extracted_rows['Case Study'][i+4]}"
        # water_flux.to_excel(writer1, index=False, sheet_name=sheet_name)

        # time elapsed
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Iteration {i+1}: Elapsed time = {elapsed_time} seconds")
        start_time = end_time

    # Insert the 'Case Study' column to final_df
    final_df.insert(0, "Case Study", Casestudies)

    # Save the results to a separate sheet with the soil type as the sheet name
    final_input_df.to_excel(
        writer, index=False, sheet_name=soil_type + "_Input_Parameters"
    )
    final_df.to_excel(writer, index=False, sheet_name=soil_type + "_Output_Results")

    Casestudies.clear()  # Clear the list for the next soil type

# Close the Excel writer
writer.save()
writer.close()
