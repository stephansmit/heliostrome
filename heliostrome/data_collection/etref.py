from typing import List
from datetime import datetime, date
from pydantic import BaseModel
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
    IrradianceDailyDatum
)
from heliostrome.models.location import Location


class EtRefDailyDatum(BaseModel):
    time: datetime
    ghi_whm2: float
    solar_elevation_deg: float
    temp_air_min_c: float
    temp_air_c: float
    temp_air_max_c: float
    wind_speed_10m_ms: float
    altitude_m: float

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
        return self.ghi_whm2 * 3.6e-3

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

    @classmethod
    def from_irradiance(cls, irradiance: IrradianceDailyDatum):
        return cls(
            time=irradiance.time,
            ghi_whm2=irradiance.ghi_whm2,
            solar_elevation_deg=irradiance.solar_elevation_deg,
            temp_air_min_c=irradiance.temp_air_min_c,
            temp_air_c=irradiance.temp_air_c,
            temp_air_max_c=irradiance.temp_air_max_c,
            wind_speed_10m_ms=irradiance.wind_speed_10m_ms,
            altitude_m=irradiance.altitude_m,
        )