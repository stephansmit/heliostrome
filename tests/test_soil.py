from heliostrome.data_collection.soil import get_soil_properties
from shapely.geometry import Polygon


def test_get_soil_properties():
    pol = Polygon(
        [
            (-18.6697, 35.5273),
            (-18.6697, 35.5273),
            (-18.6697, 35.5273),
            (-18.6697, 35.5273),
        ]
    )
    datum = get_soil_properties(pol)
    assert datum.layers[0].name == "_0-5cm_mean"
    assert datum.layers[0].weight == 2.5
    assert datum.clay_value + datum.sand_value + datum.silt_value == 100
