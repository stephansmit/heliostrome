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

alt.data_transformers.enable("default", max_rows=None)

location = Location(latitude=48.0917, longitude=5.1221)
start_date = datetime(2014, 1, 1, 0).date()
end_date = datetime(2016, 12, 31, 0).date()

climate_data = ClimateData(
    location=location,
    start_date=start_date,
    end_date=end_date,
)

soil = Soil("ClayLoam")
crop = get_crop_data("Barley")
sowing_date = datetime(2005, 6, 1, 0).strftime("%m/%d")
crop = Crop(crop.Name, planting_date=sowing_date)
irr_mngt = IrrigationManagement(irrigation_method=0)
InitWC = InitialWaterContent(value=["FC"])

model = AquaCropModel(
    sim_start_time=start_date.strftime("%Y/%m/%d"),
    sim_end_time=end_date.strftime("%Y/%m/%d"),
    weather_df=climate_data.aquacrop_input,
    soil=soil,
    crop=crop,
    initial_water_content=InitWC,
    irrigation_management=irr_mngt,
)


class SimulationResultV2(BaseModel):
    crop_growth: List[CropGrowth]
    simulation_result: List[SimulationResult]
    water_flux: List[WaterFlux]
    water_storage: List[WaterStorage]

    def __init__(self, model):
        start_datetime: date = datetime.strptime(model.sim_start_time, "%Y/%m/%d")
        end_datetime = datetime.strptime(model.sim_end_time, "%Y/%m/%d")
        datetime_range = pd.date_range(start_datetime, end_datetime)
        mapping = {
            "crop_growth": {
                "function": model.get_crop_growth,
                "type": CropGrowth,
            },
            "water_flux": {
                "function": model.get_water_flux,
                "type": WaterFlux,
            },
            "water_storage": {
                "function": model.get_water_storage,
                "type": WaterStorage,
            },
            "simulation_result": {
                "function": model.get_simulation_results,
                "type": SimulationResult,
            },
        }
        results = {}
        for key, value in mapping.items():
            df = value["function"]()
            if key != "simulation_result":
                df["time"] = datetime_range
            records = df.to_dict(orient="records")
            sub_results = [value["type"](**item) for item in records]
            results[key] = sub_results

        super().__init__(
            crop_growth=results["crop_growth"],
            simulation_result=results["simulation_result"],
            water_flux=results["water_flux"],
            water_storage=results["water_storage"],
        )

    def plot_water_storage(self):
        df = pd.DataFrame(item.model_dump() for item in self.water_storage)
        df_melted = df.melt(
            id_vars=["time"],
            value_vars=[
                "th1",
                "th2",
                "th3",
                "th4",
                "th5",
                "th6",
                "th7",
                "th8",
                "th9",
                "th10",
                "th11",
                "th12",
            ],
            var_name="category",
            value_name="value",
        )
        selection = alt.selection_multi(fields=["category"], bind="legend")
        chart = (
            alt.Chart(df_melted)
            .mark_line()
            .encode(
                x="time:T",
                y=alt.Y("value:Q"),
                color="category:N",
                opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
            )
            .add_selection(selection)
            .interactive(bind_y=False)
        )
        return chart


# chart.properties(width=600, height=400)


model.run_model(till_termination=True)


results = SimulationResultV2(model)


crop_growth = results.crop_growth
water_flux = results.water_flux
water_storage = results.water_storage


df = pd.DataFrame(item.model_dump() for item in water_storage)
df_melted = df.melt(
    id_vars=["time"],
    value_vars=[
        "th1",
        "th2",
        "th3",
        "th4",
        "th5",
        "th6",
        "th7",
        "th8",
        "th9",
        "th10",
        "th11",
        "th12",
    ],
    var_name="category",
    value_name="value",
)


selection = alt.selection_multi(fields=["category"], bind="legend")


chart = (
    alt.Chart(df_melted)
    .mark_line()
    .encode(
        x="time:T",
        y=alt.Y("value:Q"),
        color="category:N",
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    )
    .add_selection(selection)
    .interactive(bind_y=False)
)

chart.propertieswidth=600, height=400
chart

# df = model.get_simulation_results()
# records = df.to_dict(orient="records")
# results = [SimulationResult(**item) for item in records]


# df = model.get_crop_growth()
# records = df.to_dict(orient="records")
# results = [CropGrowth(**item) for item in records]


# df = model.get_water_flux()
# records = df.to_dict(orient="records")
# results = [WaterFlux(**item) for item in records]


# df = model.get_water_storage()
# records = df.to_dict(orient="records")
# results = [WaterStorage(**item) for item in records]


# import altair as alt
# from vega_datasets import data

# source = data.movies()
# import altair as alt
# from vega_datasets import data

# source = data.stocks()

# alt.Chart(source).mark_line().encode(
#     x=alt.X("time_step_counter").bin(),
#     y=alt.Y(alt.repeat('layer')).aggregate('mean').title("Mean of US and Worldwide Gross"),
#     color=alt.ColorDatum(alt.repeat('layer'))
# ).repeat(layer=["US_Gross", "Worldwide_Gross"])
