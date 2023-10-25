from datetime import datetime
from heliostrome.data_collection.etref import get_etref_daily, EtRefDailyDatum
from heliostrome.models.location import Location

start_date = datetime(2005, 1, 1, 0).date()
end_date = datetime(2016, 1, 1, 0).date()
start_year = start_date.year
end_year = end_date.year

longitude = 5.1221
latitude = 48.0917
location = Location(longitude=longitude, latitude=latitude)


def test_get_etref_daily():
    etref = get_etref_daily(
        location=location,
        start_year=start_date.year,
        end_year=end_date.year,
    )
    assert isinstance(etref[0], EtRefDailyDatum)
    assert len(etref) == 4383
    assert etref[0].time.year == 2005
    assert etref[0].time.hour == 0
