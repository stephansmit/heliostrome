
import heliostrome.models.location import Location
from heliostrome.models.climate import ClimateData
from datetime import datetime

location = Location(latitude=45.0917, longitude=5.1221)
start_date = datetime(2005, 1, 1, 0).date()
end_date = datetime(2016, 1, 1, 0).date()


data = ClimateData(location=location, start_date=start_date, end_date=end_date)
# data.plot_data("poa_global_whm2")
import pvpumpingsystem.pvgeneration as pvgen
pvgen1 = pvgen.PVGeneration(
    # Weather data path
    weather_data_and_metadata=data.pvpumping_input,

    # PV array parameters
    pv_module_name='Canadian Solar CS5C 80M',
    price_per_watt=2.5,  # in US dollars
    surface_tilt=50,  # 0 = horizontal, 90 = vertical
    surface_azimuth=180,  # 180 = South, 90 = East
    albedo=0.3,  # between 0 and 1
    modules_per_string=4,  # 4 for mppt, 5 for direct (llp smaller, cheaper)
    strings_in_parallel=1,
    # PV module glazing parameters (not always given in specs)
    glass_params={'K': 4,  # extinction coefficient [1/m]
                  'L': 0.002,  # thickness [m]
                  'n': 1.526},  # refractive index
    racking_model='open_rack',  # or'close_mount' or 'insulated_back'

    # Models used (check pvlib.modelchain for all available models)
    orientation_strategy=None,  # or 'flat', or 'south_at_latitude_tilt'
    clearsky_model='ineichen',
    transposition_model='isotropic',
    solar_position_method='nrel_numpy',
    airmass_model='kastenyoung1989',
    dc_model='desoto',  # 'desoto' or 'cec', must be a single diode model.
    ac_model='pvwatts',
    aoi_model='physical',
    spectral_model='no_loss',
    temperature_model='sapm',
    losses_model='pvwatts'
    )

pvgen1.run_model()