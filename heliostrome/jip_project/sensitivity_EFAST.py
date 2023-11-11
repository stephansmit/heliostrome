import numpy as np
from SALib.analyze import fast
from SALib.sample import latin
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

# Define the AquaCrop model setup
location = Location(latitude=31.66111, longitude=-7.60972)
start_date = date(2006, 1, 1)
end_date = date(2010, 12, 31)
climate_data = ClimateData(location=location, start_date=start_date, end_date=end_date)
soil = Soil("ClayLoam")
crop = Crop("Wheat", planting_date="12/17")
irr_mngt = IrrigationManagement(irrigation_method=3, MaxIrr=100)
# irr_mngt = IrrigationManagement(irrigation_method=3, Schedule = IRRschedule(i, B = 5), MaxIrr = 100)
InitWC = InitialWaterContent(value=["FC"])

# Define the parameters to be analyzed
problem = {
    "num_vars": 3,
    "names": ["Irrigation Threshold", "Irrigation Efficiency", "Initial Soil Moisture"],
    "bounds": [[0.3, 0.7], [0.5, 0.9], [0.2, 0.4]],
}

# Generate parameter samples using Latin Hypercube Sampling (LHS)
param_values = latin.sample(problem, 1000)

# Initialize arrays to store model outputs
output = np.zeros((param_values.shape[0], 4))
# breakpoint()

# Run the AquaCrop model for each parameter set
for i, params in enumerate(param_values):
    irr_threshold, irr_efficiency, init_wc = params
    irr_mngt.Schedule = [
        1
    ] * 4  # You can modify the irrigation schedule based on parameters if needed
    InitWC.value = [init_wc]

    model = AquaCropModel(
        sim_start_time=start_date.strftime("%Y/%m/%d"),
        sim_end_time=end_date.strftime("%Y/%m/%d"),
        weather_df=climate_data.aquacrop_input,
        soil=soil,
        crop=crop,
        initial_water_content=InitWC,
        irrigation_management=irr_mngt,
        field_management=FieldMngt(bunds=True, z_bund=0.12, bund_water=30),
    )

    model.run_model(till_termination=True)

    # Store the model output
    output[i, :] = model.get_simulation_results()["Yield (tonne/ha)"].values

# Perform EFAST sensitivity analysis
si = fast.analyze(problem, output)

# Print sensitivity indices
print("First-order indices:")
print(si["S1"])
print("Total-order indices:")
print(si["ST"])
