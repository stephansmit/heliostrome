from typing import List
from datetime import datetime
from pvlib.iotools import get_pvgis_tmy
from pandas import date_range
from pydantic import BaseModel


class IrradianceDatum(BaseModel):
    time: datetime
    time: datetime
    ghi: float
    dni: float
    dhi: float
    temp_air: float
    relative_humidity: float
    wind_speed: float
    wind_direction: float
    pressure: float


def get_irradiance(
    longitude: float, latitude: float, year: int
) -> List[IrradianceDatum]:
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
    data = df.to_dict(orient="records")
    irradiance_data = []
    for item in data:
        irradiance_data.append(IrradianceDatum(**item))

    return irradiance_data
