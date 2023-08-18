import requests_mock
from datetime import datetime
from heliostrome.data_collection.precipitation import get_precipitation_data
from requests_mock import Mocker

latitude = -18.6697
longitude = 35.5273
start_date_str = "2019-01-01"
end_date_str = "2019-01-02"

start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")


def test_get_precipitation_data():
    with Mocker() as m:
        with open("heliostrome/tests/data/precipitation_response.json") as f:
            mock_response_text = f.read()
        m.get(requests_mock.ANY, text=mock_response_text)
        precipitation = get_precipitation_data(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
        )

    assert len(precipitation) == 2
