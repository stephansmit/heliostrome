import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Literal

import heliostrome
from heliostrome.data_collection.crops import get_crop_data
from heliostrome.data_collection.soil import get_soil_properties
from heliostrome.models.climate import ClimateData
from heliostrome.models.location import Location

from aquacrop import AquaCropModel, Crop, InitialWaterContent, IrrigationManagement
from pandas import DataFrame, date_range
from plotly.subplots import make_subplots
from pvpumpingsystem.consumption import Consumption

from pvlib.iotools import get_pvgis_tmy
from scipy.optimize import fmin
main_folder = os.path.dirname(heliostrome.__file__)  # .replace("\\","/")


latitude = 30.5#50.4958#35.6
longitude = 75.29#4.9016#53.5
start_date = datetime(2006, 1, 1).date()
end_date = datetime(2007, 12, 31).date()

location = Location(latitude=latitude, longitude=longitude)

climate_data = ClimateData(
    location=location,
    start_date=start_date,
    end_date=end_date,
)


class CropModel(object):
    def __init__(self, 
                 climate_data: ClimateData, 
                 crop_name: Literal['Barley'], 
                 sowing_date: datetime,
                 ):
        self.climate_data = climate_data
        self.soil = get_soil_properties(location=climate_data.location).to_aquacrop_soil()
        self.crop = get_crop_data(crop_name)
        self.crop = Crop(self.crop.Name, planting_date=sowing_date.strftime("%m/%d"))
        self.irr_mngt = IrrigationManagement(irrigation_method=1)
        self.init_wc = InitialWaterContent(wc_type='Pct', value=[70])

    def run_model(self, irrigation_management: IrrigationManagement):
        start_date_str = climate_data.climate_daily[0].date.date().strftime("%Y/%m/%d")
        end_date_str = climate_data.climate_daily[-1].date.date().strftime("%Y/%m/%d")
        self.irr_mngt = irrigation_management
        self.aquacrop_model: AquaCropModel = AquaCropModel(
            sim_start_time=start_date_str,
            sim_end_time=end_date_str,
            weather_df=self.climate_data.aquacrop_input,
            soil=self.soil,
            crop=self.crop,
            initial_water_content=self.init_wc,
            irrigation_management=irrigation_management,
        )
        self.aquacrop_model.run_model(till_termination=True)

    def plot(self):
        fig, ax = plt.subplots()
        ax2 = ax.twinx()
        df_water = self.aquacrop_model.get_water_flux()
        df_crop = self.aquacrop_model.get_crop_growth()
        df_crop.drop(['time_step_counter', 'dap','season_counter'], inplace=True, axis=1)

        start_date = self.climate_data.climate_daily[0].date.date()
        end_date = self.climate_data.climate_daily[-1].date.date()
        
        df_water.index = pd.date_range(start_date, end_date, freq='D')
        df_crop.index = pd.date_range(start_date, end_date, freq='D')
        #join the two
        df_water = df_water.join(df_crop)
        df_water['IrrDay'].plot(ax=ax)
        df_water['biomass'].plot(ax=ax2, color='g')
        return fig, ax 


from pvpumpingsystem.mppt import mppt
from pvpumpingsystem.pipenetwork import pipenetwork as pn
from pvpumpingsystem.pump import pump as pp
from pvpumpingsystem.pvgeneration import PVGeneration

from pvpumpingsystem.pvpumpsystem import pvpumpsystem as pvps
from pvpumpingsystem.reservoir import Reservoir

class IrrigationSystem(object):
    def __init__(self, climate_data: ClimateData):
        self.pvgen = PVGeneration(
            weather_data_and_metadata=climate_data.pvpumping_input,
            pv_module_name="Canadian Solar CS5P-220M",
            modules_per_string=4,
            strings_in_parallel=1,
            orientation_strategy="south_at_latitude_tilt",  # or 'flat' or None
        )
        
    def set_pump(self, pump: pp.Pump):
        self.pump = pump



# # mppt1 = mppt.MPPT(efficiency=0.96, idname="PCA-120-BLS-M2")

# # pump_file = os.path.join(main_folder, "data/pump/SCB_10_150_120_BL.txt")
# # pump_sunpump = pp.Pump(path=pump_file)

# # pipes1 = pn.PipeNetwork(
# #     h_stat=20,  # static head [m]
# #     l_tot=100,  # length of pipes [m]
# #     diam=0.05,  # diameter [m]
# #     material="plastic",
# # )


# # consumption = Consumption(constant_flow=0.1, year=2006)
# # reservoir = Reservoir(water_volume=0)
# # pvps1 = pvps.PVPumpSystem(
# #     pvgen1,
# #     pump_sunpump,
# #     coupling="direct",  # to adapt: 'mppt' or 'direct',
# #     mppt=mppt1,
# #     pipes=pipes1,
# #     consumption=consumption,
# #     reservoir=reservoir,
# # )

# # pvps1.run_model(starting_soc='empty')
# class DesignCase(object):
#     def __init__(self, 
#                  longitude: float, 
#                  latitude: float):
#         self.location = Location(latitude=latitude, longitude=longitude)
#         self.climate_data = ClimateData(
#             location=self.location,
#             start_date=start_date,
#             end_date=end_date,
#         )
    
#     def run_aquacrop_model()


model = CropModel(climate_data, 'Wheat', datetime(2006, 12, 1))
model.run_model(IrrigationManagement(irrigation_method=1, SMT=[100,100,100,100], MaxIrrSeason=None))
model.plot()

# df_water = model.aquacrop_model.get_water_flux()
# df_crop = model.aquacrop_model.get_crop_growth()
# df_crop.drop(['time_step_counter', 'dap','season_counter'], inplace=True, axis=1)
# start_date = model.climate_data.climate_daily[0].date.date()
# end_date = model.climate_data.climate_daily[-1].date.date()

# df_water.index = pd.date_range(start_date, end_date, freq='D')
# df_crop.index = pd.date_range(start_date, end_date, freq='D')
# # df_crop = df_crop.add_suffix('_crop')
# # df_water = df_water.add_suffix('_water')
# df_water = df_water.join(df_crop)

# model.aquacrop_model.get_crop_growth()


# # model.aquacrop_model.
# # model.aquacrop_model.get_simulation_results()
# def run_model(smts, max_irr_season, start_date, end_date):
#     """
#     funciton to run model and return results for given set of soil moisture targets
#     """

#     soil_datum = get_soil_properties(location=location)
#     soil = soil_datum.to_aquacrop_soil()
#     crop = get_crop_data("Wheat")
#     sowing_date = datetime(2005, 12, 1, 0).strftime("%m/%d")
#     crop = Crop(crop.Name, planting_date=sowing_date)
#     init_wc = InitialWaterContent(wc_type='Pct',
#                                   value=[70]) # define initial soil water conditions
#     irr_mngt = IrrigationManagement(irrigation_method=1,
#                                     SMT=smts,
#                                     MaxIrrSeason=max_irr_season) # define irrigation management

#     model = AquaCropModel(
#         sim_start_time=start_date.strftime("%Y/%m/%d"),
#         sim_end_time=end_date.strftime("%Y/%m/%d"),
#         weather_df=climate_data.aquacrop_input,
#         soil=soil,
#         crop=crop,
#         initial_water_content=init_wc,
#         irrigation_management=irr_mngt,
#     )
#     model.run_model(till_termination=True)
#     return model.get_simulation_results()

# run_model([100]*4,3000,start_date=start_date,end_date=end_date)


# import numpy as np # import numpy library

# def evaluate(smts, max_irr_season, test=False):
#     """
#     funciton to run model and calculate reward (yield) for given set of soil moisture targets
#     """
#     # run model
#     out = run_model(smts,
#                     max_irr_season,
#                     start_date=start_date,
#                     end_date=end_date)
#     # get yields and total irrigation
#     yld = out['Yield (tonne/ha)'].mean()
#     tirr = out['Seasonal irrigation (mm)'].mean()

#     reward=yld

#     # return either the negative reward (for the optimization)
#     # or the yield and total irrigation (for analysis)
#     if test:
#         return yld,tirr,reward
#     else:
#         return -reward
# evaluate([70]*4,300)

# def get_starting_point(num_smts,max_irr_season,num_searches):
#     """
#     find good starting threshold(s) for optimization
#     """

#     # get random SMT's
#     x0list = np.random.rand(num_searches,num_smts)*100
#     rlist=[]
#     # evaluate random SMT's
#     for xtest in x0list:
#         r = evaluate(xtest,max_irr_season,)
#         rlist.append(r)

#     # save best SMT
#     x0=x0list[np.argmin(rlist)]
    
#     return x0

# get_starting_point(4,300,10)

# def optimize(num_smts,max_irr_season,num_searches=100):
#     """ 
#     optimize thresholds to be profit maximising
#     """
#     # get starting optimization strategy
#     x0=get_starting_point(num_smts,max_irr_season,num_searches)
#     # run optimization
#     res = fmin(evaluate, x0,disp=0,args=(max_irr_season,))
#     # reshape array
#     smts= res.squeeze()
#     # evaluate optimal strategy
#     return smts

# smts=optimize(4,300)

# evaluate(smts,300,True)

# from tqdm.notebook import tqdm # progress bar

# opt_smts=[]
# yld_list=[]
# tirr_list=[]
# for max_irr in range(0,800,100):
    

#     # find optimal thresholds and save to list
#     smts=optimize(4,max_irr,num_searches=200)
#     opt_smts.append(smts)

#     # save the optimal yield and total irrigation
#     yld,tirr,_=evaluate(smts,max_irr,True)
#     yld_list.append(yld)
#     tirr_list.append(tirr)


# # create plot
# fig,ax=plt.subplots(1,1,figsize=(13,8))

# # plot results
# ax.scatter(tirr_list,yld_list)
# ax.plot(tirr_list,yld_list)

# # labels
# ax.set_xlabel('Total Irrigation (ha-mm)',fontsize=18)
# ax.set_ylabel('Yield (tonne/ha)',fontsize=18)
# # ax.set_xlim([-20,600])
# # ax.set_ylim([2,15.5])

# # annotate with optimal thresholds
# bbox = dict(boxstyle="round",fc="1")
# offset = [15,15,15, 15,15,-125,-100,  -5, 10,10]
# yoffset= [0,-5,-10,-15, -15,  0,  10,15, -20,10]
# for i,smt in enumerate(opt_smts):
#     smt=smt.clip(0,100)
#     ax.annotate('(%.0f, %.0f, %.0f, %.0f)'%(smt[0],smt[1],smt[2],smt[3]),
#                 (tirr_list[i], yld_list[i]), xytext=(offset[i], yoffset[i]), textcoords='offset points',
#                 bbox=bbox,fontsize=12)

# # soil_datum = get_soil_properties(location=location)
# # soil = Soil('ClayLoam')
# # crop = get_crop_data("Barley")
# # sowing_date = datetime(2005, 6, 1, 0).strftime("%m/%d")
# # crop = Crop(crop.Name, planting_date=sowing_date)
# # irr_mngt = IrrigationManagement(irrigation_method=1)
# # InitWC = InitialWaterContent(value=["FC"])

# # model = AquaCropModel(
# #     sim_start_time=start_date.strftime("%Y/%m/%d"),
# #     sim_end_time=end_date.strftime("%Y/%m/%d"),
# #     weather_df=climate_data.aquacrop_input,
# #     soil=soil,
# #     crop=crop,
# #     initial_water_content=InitWC,
# #     irrigation_management=irr_mngt,
# # )

# # import time
# # start_time = time.time()
# # model.run_model(num_steps=1)
# # end_time = time.time()

# # print(f"Model run time: {end_time-start_time} seconds")
# # pv_module_name = "Canadian Solar CS5P-220M"

# # pvgen1 = pvgen.PVGeneration(
# #     weather_data_and_metadata=climate_data.pvpumping_input,#{"weather_data": df, "weather_metadata": location.to_pvlib_location()},
# #     pv_module_name="Canadian Solar CS5P-220M",  # Name of pv module to model
# #     modules_per_string=4,
# #     strings_in_parallel=1,
# #     orientation_strategy="south_at_latitude_tilt",  # or 'flat' or None
# # )


# # mppt1 = mppt.MPPT(efficiency=0.96, idname="PCA-120-BLS-M2")

# # pump_file = os.path.join(main_folder, "data/pump/SCB_10_150_120_BL.txt")
# # pump_sunpump = pp.Pump(path=pump_file)

# # pipes1 = pn.PipeNetwork(
# #     h_stat=20,  # static head [m]
# #     l_tot=100,  # length of pipes [m]
# #     diam=0.05,  # diameter [m]
# #     material="plastic",
# # )


# # consumption = Consumption(constant_flow=0.1, year=2006)
# # reservoir = Reservoir(water_volume=0)
# # pvps1 = pvps.PVPumpSystem(
# #     pvgen1,
# #     pump_sunpump,
# #     coupling="direct",  # to adapt: 'mppt' or 'direct',
# #     mppt=mppt1,
# #     pipes=pipes1,
# #     consumption=consumption,
# #     reservoir=reservoir,
# # )

# # pvps1.run_model(starting_soc='empty')

# # import plotly.graph_objs as go
# # from plotly.subplots import make_subplots

# # pvgen1_results = pvgen1.modelchain.results.dc
# # pvps1_results = pvps1.efficiency

# # fig = make_subplots(specs=[[{"secondary_y": True}]])
# # fig.add_trace(go.Scatter(x=pvgen1_results.index, y=pvgen1_results['p_mp'], name="PV Generation"), secondary_y=False)
# # fig.add_trace(go.Scatter(x=pvps1_results.index, y=pvps1_results['pump_efficiency'], name="Pump Efficiency"), secondary_y=True)

# # fig.update_layout(title="PV Generation and Pump Efficiency",
# #                   xaxis_title="Time",
# #                   yaxis_title="Power (Watt)")

# # fig.show()
# # pvgen1.modelchain.results.dc.iloc[:24]['p_mp'].plot(ax=ax2, color='r',s)
# # pvps1.efficiency.iloc[:24]['pump_efficiency'].plot(ax=ax)


# # pvps1.flow.Qlpm.plot()


# # df = pd.DataFrame(item.model_dump() for item in weather_data_hourly)
# # df.rename(
# #     {
# #         'ghi_wm2': 'ghi',
# #         'dni_wm2': 'dni',
# #         'dhi_wm2': 'dhi',

# #     }, inplace=True, axis=1
# # )
# # # df['time'] = df['time']+pd.Timedelta(minutes=9)
# # df.set_index("time", inplace=True)
# # df.rename(
# #     {
# #         "wind_speed_10m_ms": "wind_speed",
# #         "temp_air_c": "temp_air",
# #     }, axis=1, inplace=True
# # )




# # name = "Chokwe"  # put the name of your location
# # tz = "UTC"  # always uses UTC for now, timezonefinder package causes dependency conflict
# # year = "2005"  # Has to be 2005 - doesn't work for other years. Need to fix this

# # data, months_selected, inputs, metadata = get_pvgis_tmy(
# #     latitude,
# #     longitude,
# #     outputformat="csv",
# #     usehorizon=True,
# #     userhorizon=None,
# #     startyear=None,
# #     endyear=None,
# #     map_variables=True,
# #     url="https://re.jrc.ec.europa.eu/api/",
# #     timeout=30,
# # )

# # # Puts all the datetimes of the data to the specified year
# # data.index = date_range(
# #     start="00:00 01/01/" + year, end="23:00 31/12/" + year, freq="H"
# # )

# # inputs["Name"] = name
# # inputs["TZ"] = tz
# # inputs["altitude"] = inputs["elevation"]

# # pvgen1 = pvgen.PVGeneration(
# #     # Weather data path
# #     weather_data_and_metadata={"weather_data": data, "weather_metadata": inputs},
# #     pv_module_name="Canadian Solar CS5C 80M",  # Name of pv module to model
# #     modules_per_string=4,
# #     strings_in_parallel=1,
# #     orientation_strategy="south_at_latitude_tilt",  # or 'flat' or None
# # )

