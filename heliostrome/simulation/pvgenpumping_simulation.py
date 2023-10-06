import os
from pvlib.iotools import get_pvgis_tmy
import pvpumpingsystem.pvgeneration as pvgen
import pvpumpingsystem.pump as pp
import pvpumpingsystem.mppt as mppt
import pvpumpingsystem.pipenetwork as pn
import pvpumpingsystem.pvpumpsystem as pvps
import heliostrome

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
    weather_data_and_metadata = {'weather_data':data, 'weather_metadata': inputs},
    pv_module_name="Canadian Solar CS5C 80M",  # Name of pv module to model
    modules_per_string=4,
    strings_in_parallel=1,
    orientation_strategy="south_at_latitude_tilt",  # or 'flat' or None
)

mppt1 = mppt.MPPT(efficiency=0.96, idname="PCA-120-BLS-M2")

pump_file = os.path.join(main_folder, "data/pump/SCB_10_150_120_BL.txt")
pump_sunpump = pp.Pump(path=pump_file)

pipes1 = pn.PipeNetwork(
    h_stat=20,  # static head [m]
    l_tot=100,  # length of pipes [m]
    diam=0.05,  # diameter [m]
    material="plastic",
)

pvps1 = pvps.PVPumpSystem(
    pvgen1,
    pump_sunpump,
    coupling="direct",  # to adapt: 'mppt' or 'direct',
    mppt=mppt1,
    pipes=pipes1,
)
pvps1.run_model()

pvps1.calc_efficiency()

print(pvps1)
print("\ntotal water pumped in the year = ", pvps1.flow.Qlpm.sum() * 60)
print(
    "\ndetails on second day of pumping = \n", pvps1.flow[24:200]
)  # pvgen1.plot_model()
