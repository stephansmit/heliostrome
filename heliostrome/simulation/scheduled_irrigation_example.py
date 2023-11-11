from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent
from aquacrop.utils import prepare_weather, get_filepath
from aquacrop.entities.irrigationManagement import IrrigationManagement
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = get_filepath("champion_climate.txt")
wdf = prepare_weather(path)

sim_start = "1982/05/01"
sim_end = "2018/10/30"


soil = Soil("SandyLoam")

crop = Crop("Maize", planting_date="05/01")

initWC = InitialWaterContent(value=["FC"])

import pandas as pd  # import pandas library

all_days = pd.date_range(sim_start, sim_end)  # list of all dates in simulation period

new_month = True
dates = []
# iterate through all simulation days
for date in all_days:
    # check if new month
    if date.is_month_start:
        new_month = True

    if new_month:
        # check if tuesday (dayofweek=1)
        if date.dayofweek == 1:
            # save date
            dates.append(date)
            new_month = False

depths = [25] * len(dates)  # depth of irrigation applied
schedule = pd.DataFrame([dates, depths]).T  # create pandas DataFrame
schedule.columns = ["Date", "Depth"]  # name columns
rainfed = IrrigationManagement(irrigation_method=0)
irrigate_schedule = IrrigationManagement(irrigation_method=3, Schedule=schedule)
interval_7 = IrrigationManagement(irrigation_method=2, IrrInterval=7)
net_irrigation = IrrigationManagement(irrigation_method=4, NetIrrSMT=70)
threshold4_irrigate = IrrigationManagement(
    irrigation_method=1, SMT=[40, 60, 70, 30] * 4
)


# define labels to help after
labels = ["rainfed", "four thresholds", "interval", "schedule", "net"]
strategies = [
    rainfed,
    threshold4_irrigate,
    interval_7,
    irrigate_schedule,
    net_irrigation,
]

outputs = []
for i, irr_mngt in enumerate(strategies):  # for both irrigation strategies...
    crop.Name = labels[i]  # add helpfull label
    model = AquaCropModel(
        sim_start,
        sim_end,
        wdf,
        soil,
        crop,
        initial_water_content=initWC,
        irrigation_management=irr_mngt,
    )  # create model
    model.run_model(till_termination=True)  # run model till the end
    outputs.append(model._outputs.final_stats)  # save results


dflist = outputs
outlist = []
for i in range(len(dflist)):
    temp = pd.DataFrame(dflist[i][["Yield (tonne/ha)", "Seasonal irrigation (mm)"]])
    temp["label"] = labels[i]
    outlist.append(temp)

all_outputs = pd.concat(outlist, axis=0)

results = pd.concat(outlist)
# import plotting libraries
import matplotlib.pyplot as plt
import seaborn as sns

# create figure consisting of 2 plots
fig, ax = plt.subplots(2, 1, figsize=(10, 14))

# create two box plots
sns.boxplot(data=results, x="label", y="Yield (tonne/ha)", ax=ax[0])
sns.boxplot(data=results, x="label", y="Seasonal irrigation (mm)", ax=ax[1])

# labels and font sizes
ax[0].tick_params(labelsize=15)
ax[0].set_xlabel(" ")
ax[0].set_ylabel("Yield (t/ha)", fontsize=18)

ax[1].tick_params(labelsize=15)
ax[1].set_xlabel(" ")
ax[1].set_ylabel("Total Irrigation (ha-mm)", fontsize=18)

plt.legend(fontsize=18)
