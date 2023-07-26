from heliostrome.data_collection.irradiance import get_irradiance

latitude = 52.0917
longitude = 5.1221
year = 2019


def test_get_irradiance():
    irradiance = get_irradiance(latitude=latitude, longitude=longitude, year=year)
    assert len(irradiance) == 365 * 24
    assert irradiance[0].time.year == 2019
    assert irradiance[0].time.hour == 0
