# from heliostrome.data_collection.soil import get_soil_properties
from heliostrome.models.location import Location
from datetime import datetime


location = Location(latitude=48.0917, longitude=5.1221)
soil_datum = get_soil_properties(location=location)

aquacrop_soil = soil_datum.to_aquacrop_soil()
sowing_date = datetime(2005, 6, 1, 0).strftime("%m/%d")
crop = Crop(crop.Name, planting_date=sowing_date)
irr_mngt = IrrigationManagement(irrigation_method=0)
InitWC = InitialWaterContent(value=["FC"])

model = AquaCropModel(
    sim_start_time=start_date.strftime("%Y/%m/%d"),
    sim_end_time=end_date.strftime("%Y/%m/%d"),
    weather_df=climate_data.aquacrop_input,
    soil=aquacrop_soil,
    crop=crop,
    initial_water_content=InitWC,
    irrigation_management=irr_mngt,
)
