import requests_mock
from datetime import datetime
from heliostrome.data_collection.precipation import (
    get_precipitation,
)
from requests_mock import Mocker

latitude = -18.6697
longitude = 35.5273
start_date_str = "2019-01-01"
end_date_str = "2019-01-02"

start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")


def test_get_precipation():
    with Mocker() as m:
        with open("heliostrome/tests/data/precipation_response.json") as f:
            mock_response_text = f.read()
        m.get(requests_mock.ANY, text=mock_response_text)
        precipation = get_precipitation(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
        )
    datums = precipation.table.get_datums()
    assert len(datums) == 2
