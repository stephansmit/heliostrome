
import matplotlib.pyplot as plt
from datetime import datetime
from heliostrome.models.location import Location
from heliostrome.models.climate import ClimateData
from pydantic import BaseModel
from typing import List
from datetime import date
import pandas as pd
import altair as alt

from modules.JIP_plots import plot_season_data
from modules.Load_excel import factors_to_run

sheets = ['Morocco Wheat Case Study','Bangladesh Case Study','Northeast China Case Study', 'Iran Potato Case Study']
file_paths_waterflux = [
     r"heliostrome/jip_project/results/cleaned_WaterFlux_morocco.xlsx",
     r"heliostrome/jip_project/results/cleaned_WaterFlux_Bangladesh.xlsx",
    r"heliostrome/jip_project/results/cleaned_WaterFlux_NorthEastCHINA.xlsx",
    r"heliostrome/jip_project/results/cleaned_WaterFlux_IranPotato.xlsx",
    # Add more file pairs as needed
]

file_paths_precip = [
     r"heliostrome/jip_project/results/precip_data_{sheets_factors_to_run[0]}.xlsx",
     r"heliostrome/jip_project/results/precip_data_{sheets_factors_to_run[1]}.xlsx",
    r"heliostrome/jip_project/results/precip_data_{sheets_factors_to_run[2]}.xlsx",
    r"heliostrome/jip_project/results/precip_data_{sheets_factors_to_run[3]}.xlsx",
    # Add more file pairs as needed
]


for i in range(len(file_paths)):
    extracted_rows = factors_to_run(sheets[i])


    # List of input file paths and start dates

    file_start_dates = [
        {"input": file_paths[i], "start_date": extracted_rows['Start Date']}
    ]

    # Iterate through input files and start dates to extract and plot data
    for file_info in file_start_dates:
        input_path = file_info["input"]
        start_date = file_info["start_date"]
        plot_season_data(input_path, start_date)

