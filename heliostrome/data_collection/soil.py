from pydantic import BaseModel
from soilgrids import SoilGrids

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from typing import List
from shapely.geometry import Polygon

LAYER_NAMES = [
    "_0-5cm_mean",
    "_5-15cm_mean",
    "_15-30cm_mean",
    "_30-60cm_mean",
    "_60-100cm_mean",
    "_100-200cm_mean",
]
WEIGHTS = [2.5, 5, 7.5, 15, 20, 50]


class SoilLayer(BaseModel):
    name: Literal[
        "_0-5cm_mean",
        "_5-15cm_mean",
        "_15-30cm_mean",
        "_30-60cm_mean",
        "_60-100cm_mean",
        "_100-200cm_mean",
    ]
    weight: float
    clay_value: float
    sand_value: float

    @property
    def silt_value(self):
        return 100 - self.clay_value - self.sand_value

    @property
    def soil_type(self):
        return get_soil_textural_class(self.sand_value, self.clay_value)


class SoilDatum(BaseModel):
    layers: List[SoilLayer]

    @property
    def silt_value(self):
        return sum([layer.weight * layer.silt_value for layer in self.layers]) / 100

    @property
    def clay_value(self):
        return sum([layer.weight * layer.clay_value for layer in self.layers]) / 100

    @property
    def sand_value(self):
        return sum([layer.weight * layer.sand_value for layer in self.layers]) / 100

    @property
    def soil_type(self):
        return get_soil_textural_class(self.sand_value, self.clay_value)


def get_soil_properties(
    field_polygon: Polygon,
) -> SoilDatum:
    """Returns the soil value for the given service_id and bounding box.

    :type Polygon: shapely.geometry.Polygon
    :rtype: SoilDatum
    """
    west, south, east, north = field_polygon.bounds

    layers = []
    for layer_name, weight in zip(LAYER_NAMES, WEIGHTS):
        sand_value = get_prop_per_layer_type(
            "sand", layer_name, west, east, south, north
        )
        print(sand_value)
        clay_value = get_prop_per_layer_type(
            "clay", layer_name, west, east, south, north
        )
        layers.append(
            SoilLayer(
                name=layer_name,
                weight=weight,
                clay_value=clay_value,
                sand_value=sand_value,
            )
        )

    return SoilDatum(layers=layers)


def get_prop_per_layer_type(
    service_id: Literal["clay", "sand", "silt"],
    layer_name: Literal[
        "_0-5cm_mean",
        "_5-15cm_mean",
        "_15-30cm_mean",
        "_30-60cm_mean",
        "_60-100cm_mean",
        "_100-200cm_mean",
    ],
    west: float,
    east: float,
    south: float,
    north: float,
) -> float:
    """_summary_

    :param service_id: _description_
    :type service_id: Literal[&quot;clay&quot;, &quot;sand&quot;, &quot;silt&quot;]
    :param layer_name: _description_
    :type layer_name: Literal[ &#39;_0
    :param west: _description_
    :type west: float
    :param east: _description_
    :type east: float
    :param south: _description_
    :type south: float
    :param north: _description_
    :type north: float
    :return: _description_
    :rtype: float
    """
    soil_grids = SoilGrids()
    data = soil_grids.get_coverage_data(
        service_id=service_id,
        coverage_id=service_id + layer_name,
        west=west,
        south=south,
        east=east,
        north=north,
        crs="urn:ogc:def:crs:EPSG::4326",
        output="test.tif",
        width=100,
        height=100,
    )
    return data.values.mean()


def get_soil_textural_class(sand: float, clay: float) -> str:
    """Returns the soil textural class based on the sand and clay content.

    :param sand: _description_
    :type sand: _type_
    :param clay: _description_
    :type clay: _type_
    :raises Exception: _description_
    :return: _description_
    :rtype: _type_
    """
    silt = 100 - sand - clay

    if sand + clay > 100 or sand < 0 or clay < 0:
        raise Exception(r"Inputs add up to over 100% or are negative")
    elif silt + 1.5 * clay < 15:
        textural_class = "Sand"
    elif silt + 1.5 * clay >= 15 and silt + 2 * clay < 30:
        textural_class = "LoamySand"
    elif (clay >= 7 and clay < 20 and sand > 52 and silt + 2 * clay >= 30) or (
        clay < 7 and silt < 50 and silt + 2 * clay >= 30
    ):
        textural_class = "SandyLoam"
    elif clay >= 7 and clay < 27 and silt >= 28 and silt < 50 and sand <= 52:
        textural_class = "Loam"
    elif (silt >= 50 and clay >= 12 and clay < 27) or (
        silt >= 50 and silt < 80 and clay < 12
    ):
        textural_class = "SiltLoam"
    elif silt >= 80 and clay < 12:
        textural_class = "Silt"
    elif clay >= 20 and clay < 35 and silt < 28 and sand > 45:
        textural_class = "SandyClayLoam"
    elif clay >= 27 and clay < 40 and sand > 20 and sand <= 45:
        textural_class = "ClayLoam"
    elif clay >= 27 and clay < 40 and sand <= 20:
        textural_class = "SiltyClayLoam"
    elif clay >= 35 and sand > 45:
        textural_class = "SandyClay"
    elif clay >= 40 and silt >= 40:
        textural_class = "SiltClay"
    elif clay >= 40 and sand <= 45 and silt < 40:
        textural_class = "Clay"
    else:
        textural_class = "na"

    return textural_class
