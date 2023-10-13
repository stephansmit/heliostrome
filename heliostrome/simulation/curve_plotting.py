import os
from pvlib.iotools import get_pvgis_tmy
import pvpumpingsystem.pvgeneration as pvgen
import pvpumpingsystem.pump as pp
import pvpumpingsystem.mppt as mppt
import pvpumpingsystem.pipenetwork as pn
import pvpumpingsystem.pvpumpsystem as pvps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pvlib import pvsystem
from pvpumpingsystem.pump import Pump

import heliostrome

def get_iv_curve_pump(pump: Pump, static_head: float):
    load_fctI, intervalsVH = pump.functIforVH()
    voltage_vec = np.arange(*intervalsVH['V'](static_head))
    current_vec = load_fctI(voltage_vec, static_head, error_raising=False)
    return voltage_vec, current_vec

def get_iv_curve_solar(system: pvsystem, effective_irradiance: float, temp_cell: float):
    IL, I0, Rs, Rsh, nNsVth = system.calcparams_cec(effective_irradiance, temp_cell)
    n_modules_series = system.arrays[0].modules_per_string
    n_modules_parallel = system.arrays[0].strings

    #scale the resistances and currents for the system configuration
    if (n_modules_series, n_modules_parallel) != (1, 1):
        IL = n_modules_series * IL
        I0 = n_modules_parallel * I0
        nNsVth = nNsVth * n_modules_series
        Rs = (n_modules_series / n_modules_parallel) * Rs
        Rsh = (n_modules_series / n_modules_parallel) * Rsh
    
    SDE_params = {
        'photocurrent': IL,
        'saturation_current': I0,
        'resistance_series': Rs,
        'resistance_shunt': Rsh,
        'nNsVth': nNsVth
    }

    curve_info = system.singlediode(**SDE_params)
    voltage_vec = np.linspace(0., curve_info['v_oc'], 100)
    current_vec = pvsystem.i_from_v(voltage=voltage_vec, method='lambertw', **SDE_params)
    return voltage_vec, current_vec


main_folder = os.path.dirname(heliostrome.__file__)  # .replace("\\","/")


latitude = 35.6
longitude = 53.5
name = 'Chokwe'
tz = 'UTC'

data, months_selected, inputs, metadata = get_pvgis_tmy(latitude, longitude, outputformat='csv', usehorizon=True, userhorizon=None, startyear=None, endyear=None, map_variables=True, url='https://re.jrc.ec.europa.eu/api/', timeout=30)

inputs['Name'] = name
inputs['TZ'] = tz
inputs['altitude'] = inputs['elevation']
pvgen1 = pvgen.PVGeneration(
    # Weather data path
    weather_data_and_metadata = {'weather_data': data, 'weather_metadata': inputs},
    pv_module_name="Canadian Solar CS5C 80M",  # Name of pv module to model
    modules_per_string=4,
    strings_in_parallel=2,
    orientation_strategy="south_at_latitude_tilt",  # or 'flat' or None
)

mppt1 = mppt.MPPT(efficiency=0.96, idname="PCA-120-BLS-M2")

pump_file = os.path.join(main_folder, "data/pump/Lorentz_ps1200.txt")

pump_sunpump = pp.Pump(path=pump_file)


pipes1 = pn.PipeNetwork(
    h_stat=20,  # static head [m]
    l_tot=100,  # length of pipes [m]
    diam=0.05,  # diameter [m]
    material="plastic",
)


# load_fctI, intervalsVH = pump_sunpump.functIforVH()
# Vrange_load = np.arange(*intervalsVH['V'](pipes1.h_stat))
# I_fromVH = load_fctI(Vrange_load, pipes1.h_stat, error_raising=False)
# iv_pump = pd.DataFrame()
# iv_pump["v"] = Vrange_load
# iv_pump["i"] = I_fromVH


pvps1 = pvps.PVPumpSystem(
    pvgen1,
    pump_sunpump,
    coupling="direct",  # to adapt: 'mppt' or 'direct',
    mppt=mppt1,
    pipes=pipes1,
    
)
# voltage_solar, get_iv_curve_pump(pvps1.motorpump, pipes1.h_stat)

voltage_pump, current_pump = get_iv_curve_pump(pvps1.motorpump, pipes1.h_stat)
voltage_solar, current_solar = get_iv_curve_solar(pvps1.pvgeneration.system, 1000, 25)

fig, ax = plt.subplots()
ax.plot(voltage_pump, current_pump)
ax.plot(voltage_solar, current_solar)
ax.set_xlabel("Voltage [V]")
ax.set_ylabel("Current [A]")
plt.show()

# result
# pvps1.operating_point(plot=True)
# pvps1.calc_efficiency()

# print(pvps1)
# print("\ntotal water pumped in the year = ", pvps1.flow.Qlpm.sum() * 60)
# print(
#     "\ndetails on second day of pumping = \n", pvps1.flow[24:200]
# )  # pvgen1.plot_model()

