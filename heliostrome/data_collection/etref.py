from typing import List
from pvlib.atmosphere import alt2pres
from pyeto import (
    wind_speed_2m,
    celsius2kelvin,
    svp_from_t,
    avp_from_tmin,
    delta_svp,
    psy_const,
    fao56_penman_monteith,
)
from heliostrome.data_collection.irradiance import (
    IrradianceDailyDatum,
    get_irradiance_daily,
)
from heliostrome.models.location import Location


class EtRefDailyDatum(IrradianceDailyDatum):
    @property
    def wind_speed_2m_ms(self):
        """Wind speed at 2m (m/s)"""
        return wind_speed_2m(self.wind_speed_10m_ms, 10)

    @property
    def temp_air_min_K(self):
        """Minimum air temperature (K)"""
        return celsius2kelvin(self.temp_air_min_c)

    @property
    def temp_air_k(self):
        """Mean air temperature (K)"""
        return celsius2kelvin(self.temp_air_c)

    @property
    def temp_air_max_k(self):
        """Maximum air temperature (K)"""
        return celsius2kelvin(self.temp_air_max_c)

    @property
    def poa_global_mjm2(self):
        """Plane of array global irradiance (MJ/m2)"""
        return self.poa_global_whm2 * 3.6e-3

    @property
    def svp_kpa(self):
        """Saturation vapour pressure (kPa)"""
        return svp_from_t(self.temp_air_c)

    @property
    def avp_kpa(self):
        """Actual vapour pressure (kPa)"""
        return avp_from_tmin(self.temp_air_min_c)

    @property
    def delta_svp_kpa(self):
        """Slope of saturation vapour pressure curve (kPa/degC)"""
        return delta_svp(self.temp_air_c)

    @property
    def psy_kpa(self):
        """Psychrometric constant (kPa/degC)"""
        return psy_const(self._pascal_to_kpa(alt2pres(self.altitude_m)))

    @property
    def etref_mm(self):
        """Reference evapotranspiration (mm/day)"""
        return fao56_penman_monteith(
            net_rad=self.poa_global_mjm2,
            t=self.temp_air_k,
            ws=self.wind_speed_2m_ms,
            svp=self.svp_kpa,
            avp=self.avp_kpa,
            delta_svp=self.delta_svp_kpa,
            psy=self.psy_kpa,
        )

    def _pascal_to_kpa(self, pascal: float) -> float:
        return pascal / 1000


def get_etref_daily(
    location: Location, start_year: int, end_year: int
) -> List[EtRefDailyDatum]:
    daily_date = get_irradiance_daily(
        location=location,
        start_year=start_year,
        end_year=end_year,
    )
    return [EtRefDailyDatum(**datum.model_dump()) for datum in daily_date]
