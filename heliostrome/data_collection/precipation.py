from __future__ import annotations
from typing import List, Union
from pydantic import BaseModel, validator, parse_raw_as
from urllib.parse import quote
import requests
from datetime import datetime


class PrecipitationDatum(BaseModel):
    """This class contains the data for a precipitation datum.

    :param BaseModel: pydantic base model
    :type BaseModel: Pydantic BaseModel
    :raises ValueError: raised when value is less than 0
    :return: class representing a precipitation datum
    :rtype: PrecipitationDatum
    """

    latitude: float
    longitude: float
    time: datetime
    precip: float

    @validator("precip")
    def validate_precip(cls: PrecipitationDatum, value: float) -> float:
        """Validates the precipitation value.

        :param cls: _description_
        :type cls: PrecipitationDatum
        :param value: precipitation value
        :type value: float
        :raises ValueError: raised when value is less than 0
        :return: validated precipitation value
        :rtype: float
        """

        if value < 0:
            raise ValueError("Precipitation value must be greater than 0.")
        return value


class PrecipationTable(BaseModel):
    """This class contains the data for a precipitation table as returned by NOAA's ERDDAP server.

    :param BaseModel: pydantic base model
    :type BaseModel: Pydantic BaseModel
    :raises ValueError: raised when not within the list of valid strings or correct order
    :return: class representing a precipitation table
    :rtype: PrecipationTable
    """

    columnNames: List[str]
    columnTypes: List[str]
    columnUnits: List[str]
    rows: List[List[Union[float, str]]]

    @validator("columnNames")
    def validate_column_names(cls: PrecipationTable, values: List[str]) -> List[str]:
        """Validates the column names in the response from NOAA's ERDDAP server.

        :param cls: _description_
        :type cls: PrecipationTable
        :param values: list of the column names
        :type values: List[str]
        :raises ValueError: raised when not within the list of valid strings or correct order
        :return: list of the validated column names
        :rtype: List[str]
        """

        expected_strings: List[str] = ["time", "latitude", "longitude", "precip"]
        for value, expected in zip(values, expected_strings):
            if value != expected:
                raise ValueError(
                    f"Invalid string: {value}. Expected value is: {expected}"
                )
        return values

    def get_datums(self) -> List[PrecipitationDatum]:
        """Get the precipitation datums from the table.

        :return: list of precipitation datums
        :rtype: List[PrecipitationDatum]
        """
        datums = []
        for row in self.rows:
            datum = PrecipitationDatum(
                latitude=row[1],
                longitude=row[2],
                time=datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%SZ"),
                precip=row[3],
            )
            datums.append(datum)
        return datums


class PrecipitationResponse(BaseModel):
    """This class contains the response from NOAA's ERDDAP server.

    :param BaseModel: pydantic base model
    :type BaseModel: Pydantic BaseModel
    """

    table: PrecipationTable


def get_precipitation(
    latitude: float,
    longitude: float,
    start_date: datetime.date,
    end_date: datetime.date,
) -> PrecipitationResponse:
    """Get precipitation data from NOAA's ERDDAP server.

    :param latitude: latitude of the location
    :type latitude: float
    :param longitude: longitude of the location
    :type longitude: float
    :param start_date: start date of the data
    :type start_date: datetime.date
    :param end_date: end date of the data
    :type end_date: datetime.date
    :return: Response from NOAA's ERDDAP server
    :rtype: PrecipitationResponse
    """

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    base_url = (
        "https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalDailyP05.json"
    )

    query_param = (
        f"precip[({start_date_str}):1:({end_date_str})]"
        + f"[({latitude}):1:({latitude})][({longitude}):1:({longitude})]"
    )
    encoded_query_param = quote(query_param, safe="():")
    url = f"{base_url}?{encoded_query_param}"

    response = requests.get(url=url, timeout=10)
    return parse_raw_as(PrecipitationResponse, response.text)
