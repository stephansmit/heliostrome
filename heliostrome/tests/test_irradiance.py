from heliostrome.data_collection.irradiance import (
    get_irradiance_tmy,
    get_irradiance_daily,
    IrradianceDailyDatum,
    IrradianceDatumTMY,
)

latitude = 52.0917
longitude = 5.1221
year = 2015


def test_get_irradiance_tmy():
    irradiance = get_irradiance_tmy(latitude=latitude, longitude=longitude, year=year)
    assert type(irradiance[0]) == IrradianceDatumTMY
    assert len(irradiance) == 365 * 24
    assert irradiance[0].time.year == 2015
    assert irradiance[0].time.hour == 0


def test_get_irradiance_daily():
    irradiance = get_irradiance_daily(
        longitude=longitude,
        latitude=latitude,
        start_year=year,
        end_year=year,
    )
    assert type(irradiance[0]) == IrradianceDailyDatum
    assert len(irradiance) == 365
    assert irradiance[0].time.year == 2015
    assert irradiance[0].time.hour == 0
