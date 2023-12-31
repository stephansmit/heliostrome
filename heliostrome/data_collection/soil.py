import time
from requests.exceptions import HTTPError
from pydantic import BaseModel
from soilgrids import SoilGrids
from typing import Union
from aquacrop import Soil
from heliostrome.models.location import Location
from functools import lru_cache
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from typing import List
from shapely.geometry import Polygon, Point

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
    """This class contains the data for a soil layer.

    :param BaseModel: pydantic base model
    :type BaseModel: Pydantic BaseModel
    :return: class representing a soil layer
    :rtype: SoilLayer
    """

    name: Literal[
        "_0-5cm_mean",
        "_5-15cm_mean",
        "_15-30cm_mean",
        "_30-60cm_mean",
        "_60-100cm_mean",
        "_100-200cm_mean",
    ]
    weight: float
    clay_gkg: float
    sand_gkg: float
    silt_gkg: float

    @property
    def correction_factor(self):
        return 1000 / (self.clay_gkg + self.sand_gkg + self.silt_gkg)

    @property
    def clay_pct(self):
        return (self.clay_gkg / 1000 * self.correction_factor) * 100

    @property
    def sand_pct(self):
        return (self.sand_gkg / 1000 * self.correction_factor) * 100

    @property
    def silt_pct(self):
        return (self.silt_gkg / 1000 * self.correction_factor) * 100

    @property
    def soil_type(
        self,
    ) -> Literal[
        "Sand",
        "LoamySand",
        "SandyLoam",
        "Loam",
        "SiltLoam",
        "Silt",
        "SandyClayLoam",
        "ClayLoam",
        "SiltyClayLoam",
        "SandyClay",
        "SiltClay",
        "Clay",
    ]:
        return get_soil_textural_class(self.sand_pct, self.clay_pct, self.silt_pct)


class SoilDatum(BaseModel):
    """This class contains the data for a specific soil.
    It consists of different layers and has properties that are avaraged over the layers.

    :param BaseModel: pydantic base model
    :type BaseModel: Pydantic BaseModel
    :return: class representing a soil
    :rtype: SoilDatum
    """

    layers: List[SoilLayer]

    @property
    def silt_pct(self):
        return sum([layer.weight / 100 * layer.silt_pct for layer in self.layers])

    @property
    def clay_pct(self):
        return sum([layer.weight / 100 * layer.clay_pct for layer in self.layers])

    @property
    def sand_pct(self):
        return sum([layer.weight / 100 * layer.sand_pct for layer in self.layers])

    @property
    def soil_type(
        self,
    ) -> Literal[
        "Sand",
        "LoamySand",
        "SandyLoam",
        "Loam",
        "SiltLoam",
        "Silt",
        "SandyClayLoam",
        "ClayLoam",
        "SiltyClayLoam",
        "SandyClay",
        "SiltClay",
        "Clay",
    ]:
        return get_soil_textural_class(self.sand_pct, self.clay_pct, self.silt_pct)

    def to_aquacrop_soil(self) -> Soil:
        return Soil(self.soil_type)


@lru_cache(maxsize=None)
def get_soil_properties(location: Location) -> SoilDatum:
    """Returns the soil content % for the given service_id and bounding box.

    :type Polygon: shapely.geometry.Polygon
    :rtype: SoilDatum
    """

    west, south, east, north = location.field.bounds

    layers = []
    for layer_name, weight in zip(LAYER_NAMES, WEIGHTS):
        sand_gkg = get_prop_per_layer_type("sand", layer_name, west, east, south, north)
        clay_gkg = get_prop_per_layer_type("clay", layer_name, west, east, south, north)
        silt_gkg = get_prop_per_layer_type("silt", layer_name, west, east, south, north)
        layers.append(
            SoilLayer(
                name=layer_name,
                weight=weight,
                clay_gkg=clay_gkg,
                sand_gkg=sand_gkg,
                silt_gkg=silt_gkg,
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

    :param service_id: service id as defined in the SoilGrids API
    :type service_id: Literal['clay', 'sand', 'silt']
    :param layer_name: name of the layer as defined in the SoilGrids API
    :type layer_name: Literal['_0-5cm_mean', '_5-15cm_mean', '_15-30cm_mean', '_30-60cm_mean', '_60-100cm_mean', '_100-200cm_mean']
    :param west: west boundary of the bounding box
    :type west: float
    :param east: east boundary of the bounding box
    :type east: float
    :param south: south boundary of the bounding box
    :type south: float
    :param north: north boundary of the bounding box
    :type north: float
    :return: mean g/kg of the specific class in the layer
    :rtype: float
    """
    soil_grids = SoilGrids()
    n = 0
    while n < 3:
        try:
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
        except HTTPError as e:
            n += 1
            time.sleep(n * 10)
            if e.response.status_code == 500:
                return get_prop_per_layer_type(
                    service_id, layer_name, west, east, south, north
                )
            else:
                raise e


def get_soil_textural_class(sand: float, clay: float, silt: float) -> str:
    """Returns the soil textural class based on the sand and clay content.

    :param sand: sand content in %
    :type sand: float
    :param clay: clay content in %
    :type clay: float
    :raises Exception: raised when inputs add up to over 100% or are negative
    :return: textural class
    :rtype: str
    """

    if ((sand + clay + silt) != 100) or (sand < 0) or (clay < 0) or (silt < 0):
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
