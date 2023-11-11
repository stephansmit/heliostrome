from typing import List, Literal
from pydantic import BaseModel, computed_field
from datetime import datetime
import pandas as pd
import altair as alt
from heliostrome.models.location import Location
from heliostrome.data_collection.etref import EtRefDailyDatum
from heliostrome.data_collection.irradiance import IrradianceHourlyDatum, IrradianceDailyDatum
from heliostrome.data_collection.irradiance import get_irradiance_hourly, aggregate_to_daily

from heliostrome.data_collection.precipitation import (
    get_precipitation_data,
    PrecipitationDailyDatum,
)


class ClimateDailyDatum(BaseModel):
    temp_air_min_c: float
    temp_air_max_c: float
    precip_mm: float
    etref_mm: float
    date: datetime
    ghi_whm2: float

    @computed_field
    @property
    def etref_clipped_mm(self) -> float:
        return 0.1 if self.etref_mm < 0.1 else self.etref_mm

    @classmethod
    def from_etref_precip(
        cls, etref_datum: EtRefDailyDatum, precip_datum: PrecipitationDailyDatum
    ):
        if etref_datum.time != precip_datum.time:
            raise ValueError("Etref and precipitation data must be for the same date")

        return cls(
            temp_air_min_c=etref_datum.temp_air_min_c,
            temp_air_max_c=etref_datum.temp_air_max_c,
            precip_mm=precip_datum.precip_mm,
            etref_mm=etref_datum.etref_mm,
            date=etref_datum.time,
            ghi_whm2=etref_datum.ghi_whm2,
        )


class ClimateData(BaseModel):
    climate_daily: List[ClimateDailyDatum]
    irradiance_hourly: List[IrradianceHourlyDatum]
    location: Location

    @property
    def aquacrop_input(self):
        records = [datum.model_dump() for datum in self.climate_daily]
        df = pd.DataFrame(data=records)
        df.rename(
            {
                "temp_air_min_c": "MinTemp",
                "temp_air_max_c": "MaxTemp",
                "precip_mm": "Precipitation",
                "etref_clipped_mm": "ReferenceET",
                "date": "Date",
            },
            inplace=True,
            axis="columns",
        )
        df.drop("etref_mm", axis="columns", inplace=True)
        df["Date"] = df["Date"].dt.tz_convert(None)
        return df[["MinTemp", "MaxTemp", "Precipitation", "ReferenceET", "Date"]]

    @property
    def pvpumping_input(self):
        records = [datum.model_dump() for datum in self.irradiance_hourly]
        df = pd.DataFrame(data=records)
        df_final = df.rename(
            {"wind_speed_10m_ms": "windspeed", 
             "temp_air_c": "temp_air",
             'ghi_wm2': 'ghi',
             'dhi_wm2': 'dhi',
             'dni_wm2': 'dni',
             },
            axis="columns",
        ).set_index("time")
        return {
            "weather_data": df_final,
            "weather_metadata": self.location.to_pvlib_location()
        }

    def __init__(
        self, location: Location, start_date: datetime.date, end_date: datetime.date
    ):
        irradiance_hourly: List[IrradianceHourlyDatum] = get_irradiance_hourly(
            location=location, start_date=start_date, end_date=end_date
        )
        irradiance_daily: List[IrradianceDailyDatum] = aggregate_to_daily(
            hourly_data=irradiance_hourly
        )
        etref_data: List[EtRefDailyDatum] = [EtRefDailyDatum.from_irradiance(datum) for datum in irradiance_daily]
        precipitation_data: List[PrecipitationDailyDatum] = get_precipitation_data(
            location=location, start_date=start_date, end_date=end_date
        )
        precipitation_data_dict = {datum.time: datum for datum in precipitation_data}

        climate_daily = [
            ClimateDailyDatum.from_etref_precip(
                etref_datum, precipitation_data_dict[etref_datum.time]
            )
            for etref_datum in etref_data
            if etref_datum.time in precipitation_data_dict
        ]
        super().__init__(
            climate_daily=climate_daily,
            irradiance_hourly=irradiance_hourly,
            location=location
        ) 

    def plot_data(
        self,
        y_axis: Literal[
            "etref_mm",
            "precip_mm",
            "temp_air_max_c",
            "temp_air_min_c",
            "etref_clipped_mm",
            "ghi_whm2",
        ] = "etref_mm",
    ):
        records = [datum.model_dump() for datum in self.climate_daily]
        df = pd.DataFrame(data=records)
        max_y = 1.1 * df[y_axis].max()
        return (
            alt.Chart(df)
            .mark_bar()
            .encode(x="date", y=alt.Y(y_axis, scale=alt.Scale(domain=(0, max_y))))
            .properties(width=800, height=300)
            .interactive(bind_y=False)
        )
