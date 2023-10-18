import matplotlib.pyplot as plt
from datetime import datetime
from heliostrome.models.location import Location
from heliostrome.models.climate import ClimateData
from pydantic import BaseModel
from typing import List
from datetime import date
import pandas as pd
import altair as alt

from modules.Load_excel import factors_to_run

alt.data_transformers.enable("default", max_rows=None)

def Precip_data(sheets_factors_to_run): 
    " input a list of sheetnames"
    for i in range(len(sheets_factors_to_run)):
        extracted_rows = factors_to_run(sheets_factors_to_run[i])  # Data extracted from an Excel file containing all data to run ClimateData

        # Create a new Excel file for each sheet in sheets_factors_to_run
        excel_writer = pd.ExcelWriter(f"heliostrome/jip_project/results/precip_data_{sheets_factors_to_run[i]}.xlsx", engine='openpyxl')

        for x in range(len(extracted_rows["Case Study"])):
            Latitude = extracted_rows["Latitude"][x]
            Longitude = extracted_rows["Longitude"][x]
            location = Location(latitude=Latitude, longitude=Longitude)

            start_date = extracted_rows["Start Date"][x].date()
            end_date = extracted_rows["End Date"][x].date()

            climate_data = ClimateData(
                location=location,
                start_date=start_date,
                end_date=end_date,
            )

            # Access precipitation data using the climate_data instance
            precipitation_data = climate_data.climate_daily

            # Create a DataFrame from precipitation_data
            precip_df = pd.DataFrame([{
                "temp_air_min_c": entry.temp_air_min_c,
                "temp_air_max_c": entry.temp_air_max_c,
                "precip_mm": entry.precip_mm,
                "etref_mm": entry.etref_mm,
                "date": entry.date,
                "poa_global_whm2": entry.poa_global_whm2,
            } for entry in precipitation_data])

            # Save the precipitation data for each case study in a separate sheet
            precip_df.to_excel(excel_writer, sheet_name=extracted_rows["Case Study"][x], index=False)

        # Save and close the Excel file for the current sheet
        excel_writer.close()


