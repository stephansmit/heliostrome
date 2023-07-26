import random
from datetime import datetime
from heliostrome.data_collection.precipation import get_precipitation

latitude = -18.6697 + 0.05 * (random.random() - 0.5)
longitude = 35.5273 + 0.05 * (random.random() - 0.5)
start_date_str = "2019-01-01"
end_date_str = "2019-01-02"

start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")


def test_get_precipation():
    precipation = get_precipitation(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
    )
    datums = precipation.table.get_datums()
    assert len(datums) == 2
