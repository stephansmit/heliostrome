from typing import List, Union
from datetime import datetime, date
from pvlib.iotools import get_pvgis_tmy, get_pvgis_hourly
from pandas import date_range
from pydantic import BaseModel
import pandas as pd
from functools import lru_cache
from heliostrome.models.location import Location

class IrradianceHourlyDatum(BaseModel):
    time: datetime
    ghi_wm2: float
    dni_wm2: float
    dhi_wm2: float
    temp_air_c: float
    wind_speed_10m_ms: float
    altitude_m: float
    solar_elevation_deg: float


class IrradianceDailyDatum(BaseModel):
    time: datetime
    ghi_whm2: float
    solar_elevation_deg: float
    temp_air_min_c: float
    temp_air_c: float
    temp_air_max_c: float
    wind_speed_10m_ms: float
    altitude_m: float

@lru_cache(maxsize=None)
def get_irradiance_hourly(
    location: Location, start_date: date, end_date: date
) -> List[IrradianceHourlyDatum]:
    """Gets the irradiance data for a given location and year.

    :param longitude: longitude of the location
    :type longitude: float
    :param latitude: latitude of the location
    :type latitude: float

    :return: list of the irradiance data
    :rtype: List[IrradianceDatum]
    """

    df_year, metadata, _ = get_pvgis_hourly(
        location.latitude,
        location.longitude,
        start=start_date.year,
        end=end_date.year,
        components=True,
        surface_tilt=0,
        surface_azimuth=0,
        optimalangles=True,
        outputformat="csv",
        url="https://re.jrc.ec.europa.eu/api/",
        timeout=60,
    )
    # filter
    df_year.reset_index(inplace=True)
    end_date_filter = pd.to_datetime(end_date).tz_localize("UTC") + pd.Timedelta(
        hours=23
    )
    start_date_filter = pd.to_datetime(start_date).tz_localize("UTC")
    df_year["time"] = pd.to_datetime(df_year["time"]).round("H")
    df = df_year[df_year["time"].between(start_date_filter, end_date_filter)].copy()
    df["dhi_wm2"] = df["poa_sky_diffuse"] + df["poa_ground_diffuse"]
    df["ghi_wm2"] = df["poa_ground_diffuse"] + df["poa_sky_diffuse"] + df["poa_direct"]
    df["altitude_m"] = metadata["elevation"]
    df.rename(
        columns={
            "temp_air": "temp_air_c",
            "wind_speed": "wind_speed_10m_ms",
            "poa_direct": "dni_wm2",
            "solar_elevation": "solar_elevation_deg",
        },
        inplace=True,
    )
    data = df.to_dict(orient="records")
    return [IrradianceHourlyDatum(**item) for item in data]


def aggregate_to_daily(
    hourly_data: List["IrradianceHourlyDatum"],
) -> List[IrradianceDailyDatum]:
    df_hourly = pd.DataFrame([item.model_dump() for item in hourly_data]).set_index(
        "time"
    )
    df_daily = (
        df_hourly.rename({"ghi": "poa_global_wm2"}, axis=1)
        .resample("D")
        .agg(
            {
                "temp_air_c": ["min", "mean", "max"],
                "ghi_wm2": ["sum"],
                "wind_speed_10m_ms": ["mean"],
                "solar_elevation_deg": ["mean"],
                "altitude_m": ["mean"],
            }
        )
    )
    df_daily.columns = ["_".join(col).strip() for col in df_daily.columns.values]
    df_daily.rename(
        columns={
            "temp_air_c_min": "temp_air_min_c",
            "temp_air_c_mean": "temp_air_c",
            "temp_air_c_max": "temp_air_max_c",
            "ghi_wm2_sum": "ghi_whm2",
            "wind_speed_10m_ms_mean": "wind_speed_10m_ms",
            "solar_elevation_deg_mean": "solar_elevation_deg",
            "altitude_m_mean": "altitude_m",
        },
        inplace=True,
    )
    df_daily.reset_index(inplace=True)

    data = df_daily.to_dict(orient="records")
    return [IrradianceDailyDatum(**item) for item in data]


# def get_irradiance_daily(
#     location: Location, start_date: date, end_date: datetime
# ) -> List[IrradianceDailyDatum]:
#     hourly_data = get_irradiance_hourly(
#         location=location, start_date=start_date, end_date=end_date
#     )
#     df_hourly = pd.DataFrame([item.model_dump() for item in hourly_data]).set_index(
#         "time"
#     )
#     df_daily = (
#         df_hourly.rename({"ghi": "poa_global_wm2"}, axis=1)
#         .resample("D")
#         .agg(
#             {
#                 "temp_air_c": ["min", "mean", "max"],
#                 "poa_global_wm2": ["sum"],
#                 "wind_speed_10m_ms": ["mean"],
#                 "solar_elevation_deg": ["mean"],
#                 "altitude_m": ["mean"],
#             }
#         )
#     )
#     df_daily.columns = ["_".join(col).strip() for col in df_daily.columns.values]
#     df_daily.rename(
#         columns={
#             "temp_air_c_min": "temp_air_min_c",
#             "temp_air_c_mean": "temp_air_c",
#             "temp_air_c_max": "temp_air_max_c",
#             "poa_global_wm2_sum": "poa_global_whm2",
#             "wind_speed_10m_ms_mean": "wind_speed_10m_ms",
#             "solar_elevation_deg_mean": "solar_elevation_deg",
#             "altitude_m_mean": "altitude_m",
#         },
#         inplace=True,
#     )
#     df_daily.reset_index(inplace=True)

#     data = df_daily.to_dict(orient="records")
#     return [IrradianceDailyDatum(**item) for item in data]
