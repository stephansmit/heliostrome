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

FTR_sheets = [
    #'Morocco Wheat Case Study',
    #'Bangladesh Case Study',
    "Northeast China Case Study",
    #'Iran Potato Case Study'
]

file_paths_waterflux = [
    # r"heliostrome/jip_project/results/WaterFlux_moroccoWheat.xlsx",
    # r"heliostrome/jip_project/results/WaterFlux_Bangladesh.xlsx",
    r"heliostrome/jip_project/results/WaterFlux_NorthEastCHINA.xlsx",
    # r"heliostrome/jip_project/results/WaterFlux_IranPotato.xlsx",
    # Add more file pairs as needed
]

file_paths_precip = [
    # r"heliostrome/jip_project/results/precip_data_Morocco Wheat Case Study.xlsx",
    # r"heliostrome/jip_project/results/precip_data_Bangladesh Case Study.xlsx",
    r"heliostrome/jip_project/results/precip_data_Northeast China Case Study.xlsx",
    # r"heliostrome/jip_project/results/precip_data_Iran Potato Case Study.xlsx",
    # Add more file pairs as needed
]

# Example

start_date = factors_to_run(FTR_sheets[0])["Start Date"][0]
input_path_waterflux = file_paths_waterflux[0]
input_path_precip = file_paths_precip[0]
sheet_name = "A1"

plot_season_data(input_path_waterflux, input_path_precip, sheet_name, start_date)
