import os
from datetime import datetime
import pvpumpingsystem.pvgeneration as pvgen
import pvpumpingsystem.pump as pp
import pvpumpingsystem.mppt as mppt
import pvpumpingsystem.pipenetwork as pn
import pvpumpingsystem.pvpumpsystem as pvps
import heliostrome
from heliostrome.models.location import Location
from heliostrome.models.climate import ClimateData

location = Location(latitude=45.0917, longitude=5.1221)
start_date = datetime(2005, 1, 1, 0).date()
end_date = datetime(2016, 1, 1, 0).date()


data = ClimateData(location=location, start_date=start_date, end_date=end_date)
pvgen1 = pvgen.PVGeneration(
    # Weather data path
    weather_data_and_metadata=data.pvpumping_input,
    pv_module_name="Canadian Solar CS5C 80M",  # Name of pv module to model
    modules_per_string=4,
    strings_in_parallel=1,
    # Models used (check pvlib.modelchain for all available models)
    orientation_strategy="south_at_latitude_tilt",  # or 'flat' or None
)

mppt1 = mppt.MPPT(efficiency=0.96, idname="PCA-120-BLS-M2")

main_folder = os.path.dirname(heliostrome.__file__)  # .replace("\\","/")
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


# pvgen1.plot_model()
