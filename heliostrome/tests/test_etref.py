from datetime import datetime
from heliostrome.data_collection.etref import get_etref_daily, EtRefDatum

start_datetime = datetime(2005, 1, 1, 0)
end_datetime = datetime(2016, 1, 1, 0)
start_year = start_datetime.year
end_year = end_datetime.year

longitude = 5.1221
latitude = 52.0917


def test_get_etref_daily():
    etref = get_etref_daily(
        longitude=longitude,
        latitude=latitude,
        start_year=start_datetime.year,
        end_year=end_datetime.year,
    )
    assert type(etref[0]) == EtRefDatum
    assert len(etref) == 4383
    assert etref[0].time.year == 2005
    assert etref[0].time.hour == 0
