from typing import List, Literal
from pydantic import BaseModel, computed_field
from datetime import datetime
import pandas as pd
import altair as alt
from heliostrome.models.location import Location
from heliostrome.data_collection.etref import get_etref_daily, EtRefDailyDatum
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

    @computed_field
    @property
    def etref_clipped_mm(self) -> float:
        return 0.1 if self.etref_mm < 0.1 else self.etref_mm


class ClimateData(BaseModel):
    climate_daily: List[ClimateDailyDatum]

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

    def __init__(
        self, location: Location, start_date: datetime.date, end_date: datetime.date
    ):
        etref_data: List[EtRefDailyDatum] = get_etref_daily(
            location=location, start_year=start_date.year, end_year=end_date.year
        )
        precipitation_data: List[PrecipitationDailyDatum] = get_precipitation_data(
            location=location, start_date=start_date, end_date=end_date
        )
        precipitation_data_dict = {datum.time: datum for datum in precipitation_data}

        climate_daily = [
            ClimateDailyDatum(
                temp_air_min_c=etref_datum.temp_air_min_c,
                temp_air_max_c=etref_datum.temp_air_max_c,
                precip_mm=precipitation_data_dict[etref_datum.time].precip_mm,
                etref_mm=etref_datum.etref_mm,
                date=etref_datum.time,
            )
            for etref_datum in etref_data
            if etref_datum.time in precipitation_data_dict
        ]
        super().__init__(climate_daily=climate_daily)

    def plot_data(
        self,
        y_axis: Literal[
            "etref_mm", "precip_mm", "temp_air_max_c", "temp_air_min_c"
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


# location = Location(latitude=45.0917, longitude=5.1221)
# start_date = datetime(2005, 1, 1, 0).date()
# end_date = datetime(2016, 1, 1, 0).date()


# data = ClimateData(location=location, start_date=start_date, end_date=end_date)
