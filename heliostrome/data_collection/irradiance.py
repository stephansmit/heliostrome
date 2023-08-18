from typing import List
from datetime import datetime
from pvlib.iotools import get_pvgis_tmy, get_pvgis_hourly
from pandas import date_range
from pydantic import BaseModel
import pandas as pd


class IrradianceDatumTMY(BaseModel):
    time: datetime
    ghi: float
    dni: float
    dhi: float
    temp_air_c: float
    relative_humidity: float
    wind_speed_10m_ms: float
    wind_direction: float
    pressure: float


class IrradianceHourlyDatum(BaseModel):
    time: datetime
    poa_global_wm2: float
    solar_elevation_deg: float
    temp_air_c: float
    wind_speed_10m_ms: float
    altitude_m: float


class IrradianceDailyDatum(BaseModel):
    time: datetime
    poa_global_whm2: float
    solar_elevation_deg: float
    temp_air_min_c: float
    temp_air_c: float
    temp_air_max_c: float
    wind_speed_10m_ms: float
    altitude_m: float


def get_irradiance_tmy(
    longitude: float, latitude: float, year: int
) -> List[IrradianceDatumTMY]:
    """Gets the irradiance data for a given location and year.

    :param longitude: longitude of the location
    :type longitude: float
    :param latitude: latitude of the location
    :type latitude: float
    :param year: year of the data
    :type year: int
    :return: list of the irradiance data
    :rtype: List[IrradianceDatum]
    """

    df, _, _, _ = get_pvgis_tmy(
        latitude,
        longitude,
        outputformat="csv",
        usehorizon=True,
        userhorizon=None,
        startyear=2007,
        endyear=2016,
        url="https://re.jrc.ec.europa.eu/api/",
        timeout=60,
        map_variables=True,
    )

    start_date = datetime(year, 1, 1, 0)
    end_date = datetime(year, 12, 31, 23)
    df["time"] = date_range(start=start_date, end=end_date, freq="H")
    df.rename(
        columns={
            "wind_speed": "wind_speed_10m_ms",
            "temp_air": "temp_air_c",
            "pressure": "pressure",
            "relative_humidity": "relative_humidity",
            "wind_direction": "wind_direction",
            "ghi": "ghi",
            "dni": "dni",
            "dhi": "dhi",
        },
        inplace=True,
    )
    data = df.to_dict(orient="records")
    return [IrradianceDatumTMY(**item) for item in data]


def get_irradiance_hourly(
    longitude: float, latitude: float, start_year: int, end_year: int
) -> List[IrradianceHourlyDatum]:
    """Gets the irradiance data for a given location and year.

    :param longitude: longitude of the location
    :type longitude: float
    :param latitude: latitude of the location
    :type latitude: float

    :return: list of the irradiance data
    :rtype: List[IrradianceDatum]
    """

    df, metadata, _ = get_pvgis_hourly(
        latitude,
        longitude,
        start=start_year,
        end=end_year,
        components=False,
        surface_tilt=0,
        surface_azimuth=0,
        optimalangles=True,
        outputformat="csv",
        url="https://re.jrc.ec.europa.eu/api/",
        timeout=60,
    )
    df["altitude_m"] = metadata["elevation"]
    df.rename(
        columns={
            "temp_air": "temp_air_c",
            "wind_speed": "wind_speed_10m_ms",
            "poa_global": "poa_global_wm2",
            "solar_elevation": "solar_elevation_deg",
        },
        inplace=True,
    )
    df.reset_index(inplace=True)
    data = df.to_dict(orient="records")
    return [IrradianceHourlyDatum(**item) for item in data]


def get_irradiance_daily(
    longitude: float, latitude: float, start_year: int, end_year: int
) -> List[IrradianceDailyDatum]:
    hourly_data = get_irradiance_hourly(
        longitude=longitude, latitude=latitude, start_year=start_year, end_year=end_year
    )
    df_hourly = pd.DataFrame([item.model_dump() for item in hourly_data]).set_index(
        "time"
    )
    df_daily = df_hourly.resample("D").agg(
        {
            "temp_air_c": ["min", "mean", "max"],
            "poa_global_wm2": ["sum"],
            "wind_speed_10m_ms": ["mean"],
            "solar_elevation_deg": ["mean"],
            "altitude_m": ["mean"],
        }
    )
    df_daily.columns = ["_".join(col).strip() for col in df_daily.columns.values]
    df_daily.rename(
        columns={
            "temp_air_c_min": "temp_air_min_c",
            "temp_air_c_mean": "temp_air_c",
            "temp_air_c_max": "temp_air_max_c",
            "poa_global_wm2_sum": "poa_global_whm2",
            "wind_speed_10m_ms_mean": "wind_speed_10m_ms",
            "solar_elevation_deg_mean": "solar_elevation_deg",
            "altitude_m_mean": "altitude_m",
        },
        inplace=True,
    )
    df_daily.reset_index(inplace=True)

    data = df_daily.to_dict(orient="records")
    return [IrradianceDailyDatum(**item) for item in data]
