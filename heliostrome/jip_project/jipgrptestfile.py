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

"""Case study: Solar pump irrigation system for green agriculture
Location: Gazipur
Chapter: 2.6 & 3.4"""

alt.data_transformers.enable("default", max_rows=None)

location = Location(latitude=24.0958, longitude=90.4125)
start_date = datetime(2011, 5, 1, 0).date()
end_date = datetime(2013, 9, 30, 0).date()

climate_data = ClimateData(
    location=location,
    start_date=start_date,
    end_date=end_date,
)

climate_data.plot_data(y_axis='temp_air_max_c')

soil = Soil("ClayLoam")
crop = get_crop_data("Tomato")
sowing_date = datetime(2012, 6, 26, 0).strftime("%m/%d")
crop = Crop(crop.Name, planting_date=sowing_date)
irr_mngt = IrrigationManagement(irrigation_method=1, SMT=[35,35,35,35])
InitWC = InitialWaterContent(wc_type = 'Pct', value=["26"])

# input_data = [location.latitude, location.longitude, start_date, end_date, soil, crop, sowing_date,irr_mngt.irrigation_method, irr_mngt.SMT,InitWC.wc_type ]
# input_df = pd.DataFrame(input_data,columns=['Latitude','Longitude','Start Date','End Date', 'Soil Type', 'Crop Type', 'Sowing Date', 'Irrigation Method', 'SMT', 'IWC'])

input_df = {'Latitude' : location.latitude,
            'Longitude' :location.longitude,
            'Start Date' : start_date,
            'End Date' : end_date,
             'Soil Type' : soil.Name, 
             'Crop Type' : crop.Name,
             'Sowing Date' :sowing_date,
             'Irrigation Method' : irr_mngt.irrigation_method,
             'SMT' : irr_mngt.SMT, 
             'Init WC - WC Type' :InitWC.wc_type,
             'Init WC - Value': InitWC.value}


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
print(input_df)
input_df.to_excel('filename')

model.get_simulation_results()

