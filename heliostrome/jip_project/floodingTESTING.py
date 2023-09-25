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
from datetime import date
import pandas as pd
import altair as alt

alt.data_transformers.enable("default", max_rows=None)

location = Location(latitude=23.49, longitude=89.42)
start_date = datetime(2010, 1, 1, 0).date()
end_date = datetime(2013, 12, 31, 0).date()

climate_data = ClimateData(
    location=location,
    start_date=start_date,
    end_date=end_date,
)

soil = Soil("ClayLoam")
crop = get_crop_data("PaddyRice")
sowing_date = datetime(2005, 1, 29, 0).strftime("%m/%d")
crop = Crop(crop.Name, planting_date=sowing_date)
irr_mngt = IrrigationManagement(irrigation_method=1, SMT = [100]*4)
InitWC = InitialWaterContent(value=["SAT"])

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
print(df)