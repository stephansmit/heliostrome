from heliostrome.data_collection.irradiance import (
    get_irradiance_tmy,
    get_irradiance_daily,
    IrradianceDailyDatum,
    IrradianceDatumTMY,
)
from heliostrome.models.location import Location

location = Location(latitude=47.0917, longitude=5.1221)
year = 2015


def test_get_irradiance_tmy():
    irradiance = get_irradiance_tmy(location=location, year=year)
    assert isinstance(irradiance[0], IrradianceDatumTMY)
    assert len(irradiance) == 365 * 24
    assert irradiance[0].time.year == 2015
    assert irradiance[0].time.hour == 0


def test_get_irradiance_daily():
    irradiance = get_irradiance_daily(
        location=location,
        start_year=year,
        end_year=year,
    )
    assert isinstance(irradiance[0], IrradianceDailyDatum)
    assert len(irradiance) == 365
    assert irradiance[0].time.year == 2015
    assert irradiance[0].time.hour == 0
